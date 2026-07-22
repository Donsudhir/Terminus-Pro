package crypto

import (
	"encoding/binary"
	"fmt"

	"vaultlab/keyring"
	"vaultlab/model"
)

func frameTag(a model.Frame, b []byte) ([]byte, error) {
	nonce, err := DecodeText(a.Nonce)
	if err != nil {
		return nil, err
	}
	body, err := DecodeText(a.Body)
	if err != nil {
		return nil, err
	}
	wrapped, err := DecodeText(a.Wrapped)
	if err != nil {
		return nil, err
	}
	var seq [8]byte
	binary.BigEndian.PutUint64(seq[:], a.Seq)
	return Mac(
		b,
		[]byte("frame-v1"),
		model.AuthorityBytes(a.Item, a.Axis, a.Epoch),
		seq[:],
		nonce,
		body,
		wrapped,
	), nil
}

func Seal(a model.ItemID, b model.AxisID, c keyring.Epoch, d model.Payload, e *keyring.Ring) (model.Frame, error) {
	return SealAt(a, b, c, d, uint64(c)*1000+1, e)
}

func SealAt(a model.ItemID, b model.AxisID, c keyring.Epoch, d model.Payload, seq uint64, e *keyring.Ring) (model.Frame, error) {
	if err := a.Valid(); err != nil {
		return model.Frame{}, err
	}
	if b == "" || c == 0 || len(d) == 0 || seq == 0 {
		return model.Frame{}, fmt.Errorf("invalid frame input")
	}
	base, err := e.Key(c)
	if err != nil {
		return model.Frame{}, err
	}
	scope, err := ScopeFor(b, c)
	if err != nil {
		return model.Frame{}, err
	}
	var seqBytes [8]byte
	binary.BigEndian.PutUint64(seqBytes[:], seq)
	dataKey := Mac(base, []byte("data-v1"), model.AuthorityBytes(a, b, uint32(c)), seqBytes[:])
	nonce := Mac(dataKey, []byte("nonce-v1"), model.AuthorityBytes(a, b, uint32(c)), seqBytes[:])[:16]
	body, err := Xor(d, Stream(dataKey, nonce, len(d)))
	if err != nil {
		return model.Frame{}, err
	}
	wrapped, err := WrapKey(dataKey, base, scope)
	if err != nil {
		return model.Frame{}, err
	}
	frame := model.Frame{
		Item:    a,
		Axis:    b,
		Epoch:   uint32(c),
		Nonce:   EncodeText(nonce),
		Body:    EncodeText(body),
		Wrapped: EncodeText(wrapped),
		Seq:     seq,
	}
	tag, err := frameTag(frame, dataKey)
	if err != nil {
		return model.Frame{}, err
	}
	frame.Tag = EncodeText(tag)
	return frame, nil
}

func Open(a model.Frame, b Scope, c *keyring.Ring) (model.Payload, error) {
	if err := a.StructuralValid(); err != nil {
		return nil, err
	}
	base, err := c.Key(keyring.Epoch(a.Epoch))
	if err != nil {
		return nil, err
	}
	wrapped, err := DecodeText(a.Wrapped)
	if err != nil {
		return nil, err
	}
	dataKey, err := UnwrapKey(wrapped, base, b)
	if err != nil {
		return nil, err
	}
	tag, err := DecodeText(a.Tag)
	if err != nil {
		return nil, err
	}
	want, err := frameTag(a, dataKey)
	if err != nil {
		return nil, err
	}
	if !Equal(tag, want) {
		return nil, fmt.Errorf("protected frame rejected")
	}
	nonce, err := DecodeText(a.Nonce)
	if err != nil {
		return nil, err
	}
	body, err := DecodeText(a.Body)
	if err != nil {
		return nil, err
	}
	plain, err := Xor(body, Stream(dataKey, nonce, len(body)))
	if err != nil {
		return nil, err
	}
	return model.Payload(plain), nil
}

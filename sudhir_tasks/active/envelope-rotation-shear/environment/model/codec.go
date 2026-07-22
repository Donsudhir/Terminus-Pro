package model

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
)

type Frame struct {
	Item    ItemID `json:"item"`
	Axis    AxisID `json:"axis"`
	Epoch   uint32 `json:"epoch"`
	Nonce   string `json:"nonce"`
	Body    string `json:"body"`
	Wrapped string `json:"wrapped"`
	Tag     string `json:"tag"`
	Seq     uint64 `json:"seq"`
}

type CatalogEntry struct {
	Item ItemID `json:"item"`
	File string `json:"file"`
	Slot int    `json:"slot"`
}

func (f Frame) StructuralValid() error {
	if err := f.Item.Valid(); err != nil {
		return err
	}
	if f.Axis == "" || f.Epoch == 0 || f.Seq == 0 {
		return fmt.Errorf("incomplete frame header")
	}
	if f.Nonce == "" || f.Body == "" || f.Wrapped == "" || f.Tag == "" {
		return fmt.Errorf("incomplete protected frame")
	}
	return nil
}

func (f Frame) Clone() Frame {
	return f
}

func AuthorityBytes(item ItemID, axis AxisID, epoch uint32) []byte {
	var out bytes.Buffer
	writePart := func(raw []byte) {
		_ = binary.Write(&out, binary.BigEndian, uint32(len(raw)))
		_, _ = out.Write(raw)
	}
	writePart([]byte(item.Service))
	writePart([]byte(item.Secret))
	writePart([]byte(axis))
	_ = binary.Write(&out, binary.BigEndian, epoch)
	return out.Bytes()
}

func DecodeFrames(raw []byte) ([]Frame, error) {
	var frames []Frame
	if err := json.Unmarshal(raw, &frames); err != nil {
		return nil, err
	}
	if len(frames) == 0 {
		return nil, fmt.Errorf("empty frame bundle")
	}
	return frames, nil
}

func EncodeFrames(frames []Frame) ([]byte, error) {
	return json.MarshalIndent(frames, "", "  ")
}

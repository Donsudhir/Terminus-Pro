package keyring

import "fmt"

type Epoch uint32

type Material struct {
	Epoch Epoch
	Bytes []byte
}

func (m Material) Valid() error {
	if m.Epoch == 0 {
		return fmt.Errorf("zero epoch")
	}
	if len(m.Bytes) < 24 {
		return fmt.Errorf("short material")
	}
	return nil
}

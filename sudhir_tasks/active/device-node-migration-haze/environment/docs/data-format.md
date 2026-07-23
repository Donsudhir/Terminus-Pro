# Data format notes

## Project special entries

Special entries are ordinary files that begin with the four-byte magic `HZSP`
followed by a one-byte kind and two little-endian 16-bit fields. Probes treat
that header as the authoritative identity for openability checks. Kernel
character/block nodes are not required.

## Packed ledger

`/app/ledger/packed.bin` stores concatenated records:

- kind (u8)
- major (u16 LE)
- minor (u16 LE)
- mode (u16 LE)
- uid (u16 LE)
- gid (u16 LE)
- name length (u8)
- name bytes (relative path under the destination staging root)

## Alias map

`etc/alias.map` lines are `name=relative/path` pairs used after staging swap.

## Roster seed

`etc/roster.seed` lines are `rel mode_octal uid gid`.

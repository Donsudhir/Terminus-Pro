# TASK-DNMH-001 — device-node-migration-haze — Super-Uniqueness Dossier

- Idea: `device-node-migration-haze` (IDEA-0033)
- Category: system-administration
- Archetype: long-horizon investigation — count-green rootfs/service migration that loses device-node identity (major/minor, mode, open path) while ordinary file bytes and a file-only control stay intact
- Research date: 2026-07-23
- Verdict: **no semantic collision found** across all six required scopes

## Novelty fingerprint (four parts)

1. **Domain/system:** a host migration / cutover tool that copies a service root between staging trees, with device-backed services, bind/open paths, permissions, and a non-device healthy control tree.
2. **Failure mechanism:** migration reports success from file counts and exit codes, but after cutover device-backed services fail to open required nodes, lose expected major/minor identity, or bind the wrong path while ordinary file bytes look intact.
3. **Distributed fix topology:** device-node materialization (`mknod`/metadata fidelity), permission/ownership preservation, and service open-path / bind wiring must coordinate. Count-only copy success is insufficient.
4. **Verifier/invariant surface:** pre-migration device identity and open-path contracts on failing fixtures, green file-only control migration, and deliberately broken device fixtures that must remain rejected.

## Collision audit — all six scopes

### 1. Idea registry

Scanned `sudhir_progress/registry.json` / `IDEA_INDEX.md` on 2026-07-23.

System-admin neighbours:

- `dedup-restore-fidelity` (IDEA-0027) — backup/restore round-trip fidelity for hardlinks, sparse regions, and xattrs under a deduplicating store; not device-node major/minor or service open-path cutover.
- `musl-sysroot-splice` — toolchain/sysroot splice; unrelated.
- `cgroup-freeze-resume-rift` — proposal-failed; cgroup freeze/resume, not device nodes.

No idea combines count-green migration, device major/minor identity loss, file-only healthy control, and rejected broken-device fixtures. **No collision.**

### 2. Active tasks

`sudhir_tasks/active/`: envelope-rotation-shear, musl-sysroot-splice, resolver-closure-drift, robust-predicate-scale-parity, rowgroup-prune-mirage, sparse-jacobian-color-contract. None is a device-node / rootfs migration fidelity task. **No collision.**

### 3. Archived tasks / submission archives

`sudhir_tasks/archived/` empty. Content-scanned `Task_Ready_To_Submit/` and `sudhir_tasks_ready_to_submit/` zip `instruction.md` for `mknod|device.?node|char.?dev|block.?dev|major.?minor|devtmpfs|udev` (2026-07-23): **0 hits**. Dedup/backup-adjacent stems (`noisy-customer-dedup`, embedding/format migration, etc.) do not grade device-node identity after service cutover. **No collision.**

### 4. Upstream corpus

Local `tasks/` and prior TB research notes contain no Terminal-Bench public task whose intellectual core is post-migration device-node major/minor / open-path fidelity with a file-only control. Closest portfolio neighbour remains `dedup-restore-fidelity` (different mechanism). **No collision.**

### 5. Current external research

Searches performed 2026-07-23:

- `Terminal-Bench task device node mknod rootfs migration major minor fidelity`
- Linux `mknod` / udev device-node management (inspiration only)

External literature and manpages describe real device-node creation and migration hazards. No public Terminal-Bench task instance, patch, or test suite was adopted. Inspiration boundary: symptom shape only. **No benchmark collision.**

### 6. Structural-neighbour check

Nearest engineering analogue is a production rootfs/service migration that copies regular files correctly but flattens or rematerializes device nodes without preserving type/major/minor/mode or service open paths. Ordinary “rsync the tree” or “restore from backup” recipes do not match this distributed device-identity + control/reject contract.

## Closest analogue and structural difference

- **Closest analogue:** reserved/captured `dedup-restore-fidelity` (IDEA-0027) — filesystem restore fidelity under a feature matrix.
- **Structural difference:** this idea’s core is **device special-file identity and service open-path contracts after a count-green migration**, with a **file-only healthy control** and **rejected broken-device fixtures** — not hardlink/sparse/xattr round-trips under a deduplicating chunk store.

## Result

Uniqueness PASS for `device-node-migration-haze`. Do not start Step 2a in this session.

# Official CI requirements coverage — 2026-07-21

Policy profile: `terminus-ec-ci-2026-07-21`
Source: current CI Checks and Dockerfile & Image Best Practices Markdown.
Executable facts: `ci_policy.py`.

Disposition vocabulary:

- `locally-enforced` — active deterministic local check;
- `delegated-upstream` — required platform check because no reliable local equivalent exists;
- `mandatory-human-review` — semantic review cannot be safely automated;
- `house-override` — intentionally stricter local policy;
- `not-applicable` — recorded rationale required.

| Official check | Severity | Disposition | Local control / rationale |
| --- | --- | --- | --- |
| `check_pinned_images` | block | locally-enforced | `dockerfile_check.check_pin_base_digest` |
| `check_sanctioned_base_images` | block | locally-enforced | exact reviewed final-image set; `scratch` accepted; approved custom image requires policy-list promotion |
| `check_build_context_size` | block | locally-enforced | 100 MiB total, 50 MiB/file, symlink escape rejection |
| `pinned_dependencies` | block | locally-enforced | direct pip/npm/Cargo/Go installs; Node/Cargo/Go/Maven/Gradle manifests and locks; download checksums |
| `tests_or_solution_in_image` | block | locally-enforced | Dockerfile silo check |
| `check_dockerfile_references` | block | locally-enforced | static COPY/ADD source resolution and forbidden references |
| `check_test_sh` | block | locally-enforced | semantic pytest/reward contract |
| `check_task_absolute_path` | block | locally-enforced | instruction absolute-path parser |
| `check_privileged_containers` | block | locally-enforced | privileged mode, unsafe caps, Docker socket, reserved mounts including `/oracle` |
| `validate_task_fields` | block | locally-enforced | task manifest and shared layout checks |
| `ruff` | block | locally-enforced | verifier/environment Python lint |
| `typos` | block | delegated-upstream | spelling and identifier intent are semantic; current GPT-5.5 pre-submission check required |
| `check_task_sizes` | block | delegated-upstream | official numeric per-task-file limit is not published; build-context limits remain local |
| `check_dockerignore` | warn | locally-enforced | non-trivial context and COPY-dot handling |
| `check_dockerfile_hygiene` | warn/block | locally-enforced | package hygiene and secret/cache checks |
| `check_offline_tests` | warn | locally-enforced | runtime installs/downloads including `git clone`, Cargo, Maven, Gradle; preloaded local wheels exempt |
| `check_apt_usage` | warn/block | locally-enforced | single transaction, no upgrade, cleanup, no recommends |
| `check_reproducible_builds` | warn/block | locally-enforced | curl/wget checksum, exact Git commit, wall-clock warning |
| `check_layer_volatility` | warn | locally-enforced | broad source COPY before dependency install |
| `check_no_build_tools_in_runtime` | warn | locally-enforced | final-stage tools unless agent-facing languages justify compilation |
| `check_file_extraction` | warn | locally-enforced | archive extracted and removed in the same Docker stage |
| `check_heredoc_usage` | warn/local house block | locally-enforced | source-as-files rule |
| `check_recursive_permissions` | warn | locally-enforced | recursive chmod/chown warning |

## Activation and shadow evidence

- Exact positive/negative/false-positive fixtures cover sanctioned final stages,
  builder-stage freedom, `scratch`, size boundaries, symlink escapes, unsafe
  capabilities, `/oracle`, extraction/removal, layer ordering, runtime tool
  justification, direct-download checksums, package-manager pins/locks, runtime
  `git clone`, and local preloaded wheels.
- Docker shadow spans six active tasks and Python, Rust, GCC/C++, Go, C, and
  Fortran-facing stacks. New blocking deltas: zero. Existing musl warning is
  unrelated to the new parity families.
- `typos` and `check_task_sizes` remain explicitly delegated and must appear in
  the pre-submission upstream result; no local PASS is invented.
- New parity checks are consumed by `dockerfile_check.py`, `sudhir_task.py
  gates`, and the authoritative `approve_task.py` gate.

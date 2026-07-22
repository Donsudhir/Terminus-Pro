# REV-1 reviewer feedback — musl-sysroot-splice

Source: Snorkel 29a821f1 (2026-07-19)

The verifier does not prove the core 'fully static musl built through the helpers' requirement. No INTERP cannot distinguish musl from static glibc. Helper-name string checks can also pass through comments or dead references without actual integration. Add behavioral checks proving the final artifact uses staged musl inputs and executes the knit/pack/seal pipeline.

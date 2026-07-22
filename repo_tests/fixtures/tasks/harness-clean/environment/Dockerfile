# syntax=docker/dockerfile:1
# Final runtime: sanctioned Terminal-Bench Python canonical base (digest-pinned).
# C/musl/qemu toolchains are apt-installed because the agent compiles at runtime.
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

LABEL org.opencontainers.image.title="musl-sysroot-splice"
LABEL org.opencontainers.image.source="https://github.com/laude-institute/terminal-bench"
LABEL org.opencontainers.image.revision="task-environment"
LABEL org.opencontainers.image.created="1970-01-01T00:00:00Z"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# OS packages for musl hybrid sysroot assembly + qemu-user probes.
# Includes agent session tools; /tmp remains sticky for tmux sockets.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        binutils=2.40-2 \
        ca-certificates=20230311+deb12u1 \
        coreutils=9.1-1 \
        gcc=4:12.2.0-3 \
        libc6-dev=2.36-9+deb12u14 \
        libevent-core-2.1-7=2.1.12-stable-8 \
        libutempter0=1.2.1-3 \
        make=4.3-4.1 \
        musl=1.2.3-1 \
        musl-dev=1.2.3-1 \
        musl-tools=1.2.3-1 \
        qemu-user=1:7.2+dfsg-7+deb12u18+b3 \
        tmux=3.3a-3 \
    && apt-mark manual \
        tmux asciinema libevent-core-2.1-7 libutempter0 \
    && rm -rf /var/lib/apt/lists/* \
    && chmod 1777 /tmp \
    && command -v tmux \
    && tmux -V \
    && command -v asciinema \
    && asciinema --version \
    && HOME=/tmp TMUX_TMPDIR=/tmp TERM=xterm-256color \
        tmux new-session -d -s _tb_os_check sleep 5 \
    && HOME=/tmp TMUX_TMPDIR=/tmp tmux kill-session -t _tb_os_check

# Verifier Python packages — pinned in verifier-requirements.txt; baked for offline runs.
COPY verifier-requirements.txt /opt/verifier-requirements.txt
RUN python3 -m pip install --no-cache-dir -r /opt/verifier-requirements.txt
RUN rm -rf /root/.cache/pip \
    && python3 -m pytest --version

ENV HOME=/tmp
ENV TMUX_TMPDIR=/tmp
ENV TERM=xterm-256color
ENV XDG_CONFIG_HOME=/tmp/.config
ENV SOURCE_DATE_EPOCH=0
ENV PATH="/app/bin:/usr/local/bin:/usr/bin:/bin"

# Task sources (narrower than a blind whole-tree copy of caches/artifacts).
COPY conf/ /app/conf/
COPY docs/ /app/docs/
COPY src/ /app/src/
COPY mod_a/ /app/mod_a/
COPY mod_b/ /app/mod_b/
COPY mod_c/ /app/mod_c/
COPY mod_common/ /app/mod_common/
COPY tools/ /app/tools/
COPY vendor/ /app/vendor/
COPY probe/ /app/probe/
COPY ci/ /app/ci/
COPY hooks/ /app/hooks/
COPY metrics/ /app/metrics/

RUN chmod +x /app/tools/*.sh /app/hooks/*.sh /app/ci/*.sh \
    && /app/tools/seed_vendor.sh \
    && make -C /app/mod_common \
    && mkdir -p /app/output \
    && command -v qemu-x86_64 \
    && command -v readelf \
    && command -v gcc

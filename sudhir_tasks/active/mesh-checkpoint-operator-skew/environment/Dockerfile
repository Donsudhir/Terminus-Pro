# syntax=docker/dockerfile:1
FROM public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe9e7d8e37ceb96ed907265a3a0df7f44e3737d0b100e7907a679acb36

LABEL org.opencontainers.image.title="mesh-parity-lab"
LABEL org.opencontainers.image.source="https://github.com/laude-institute/terminal-bench"
LABEL org.opencontainers.image.revision="task-environment"
LABEL org.opencontainers.image.created="1970-01-01T00:00:00Z"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        binutils=2.40-2 \
        ca-certificates=20230311+deb12u1 \
        g++=4:12.2.0-3 \
        gcc=4:12.2.0-3 \
        gfortran=4:12.2.0-3 \
        libevent-core-2.1-7=2.1.12-stable-8 \
        libutempter0=1.2.1-3 \
        make=4.3-4.1 \
        python3=3.11.2-1+b1 \
        python3-venv=3.11.2-1+b1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/verifier

COPY verifier-requirements.txt /opt/verifier-requirements.txt
RUN /opt/verifier/bin/pip install --no-cache-dir --require-hashes \
        -r /opt/verifier-requirements.txt

RUN printf '%s\n' '#!/bin/sh' 'exec /opt/verifier/bin/python "$@"' > /usr/local/bin/python \
    && chmod 0755 /usr/local/bin/python \
    && rm -rf /root/.cache/pip \
    && ln -sf /usr/local/cargo/bin/rustc /usr/local/bin/rustc \
    && /opt/verifier/bin/python -m pytest --version \
    && command -v rustc \
    && command -v g++ \
    && command -v gfortran \
    && command -v tmux \
    && command -v asciinema \
    && asciinema --version

ENV HOME=/tmp
ENV TMUX_TMPDIR=/tmp
ENV TERM=xterm-256color
ENV XDG_CONFIG_HOME=/tmp/.config
ENV SOURCE_DATE_EPOCH=0
ENV PATH="/opt/verifier/bin:/app/bin:/usr/local/cargo/bin:/usr/local/bin:/usr/bin:/bin"

COPY Makefile /app/Makefile
COPY conf/ /app/conf/
COPY data/ /app/data/
COPY docs/ /app/docs/
COPY fixtures/ /app/fixtures/
COPY native/ /app/native/
COPY host/ /app/host/
COPY pack/ /app/pack/
COPY kernels/ /app/kernels/
COPY tools/ /app/tools/

RUN chmod +x /app/tools/build_all.sh /app/tools/run_meshlab.sh \
    && mkdir -p /app/output /tmp/.config/asciinema \
    && chmod 1777 /tmp \
    && /app/tools/build_all.sh \
    && make -C /app clean \
    && HOME=/tmp TMUX_TMPDIR=/tmp TERM=xterm-256color tmux new-session -d -s _meshlab_image_check sleep 5 \
    && HOME=/tmp TMUX_TMPDIR=/tmp tmux kill-session -t _meshlab_image_check \
    && asciinema --version

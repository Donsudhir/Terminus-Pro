# syntax=docker/dockerfile:1
FROM public.ecr.aws/docker/library/gcc:13-bookworm@sha256:930f2ebe239275fa67226654cb79273ea34eee672ae61c8a39f689c37fb7ac5c

LABEL org.opencontainers.image.title="loam-columnar-lab"
LABEL org.opencontainers.image.source="https://github.com/laude-institute/terminal-bench"
LABEL org.opencontainers.image.revision="task-environment"
LABEL org.opencontainers.image.created="1970-01-01T00:00:00Z"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        cargo=0.66.0+ds1-1 \
        libevent-core-2.1-7=2.1.12-stable-8 \
        libutempter0=1.2.1-3 \
        python3=3.11.2-1+b1 \
        python3-venv=3.11.2-1+b1 \
        rustc=1.63.0+dfsg1-2 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/verifier \
    && command -v asciinema \
    && asciinema --version

RUN /opt/verifier/bin/pip install --no-cache-dir \
        pytest==8.4.1 \
        pytest-json-ctrf==0.3.5

RUN rm -rf /root/.cache/pip \
    && command -v asciinema \
    && asciinema --version

ENV HOME=/tmp
ENV TMUX_TMPDIR=/tmp
ENV TERM=xterm-256color
ENV XDG_CONFIG_HOME=/tmp/.config
ENV SOURCE_DATE_EPOCH=0
ENV PATH="/opt/verifier/bin:/app/bin:/usr/local/cargo/bin:/usr/local/bin:/usr/bin:/bin"

COPY Makefile /app/Makefile
COPY config/ /app/config/
COPY docs/ /app/docs/
COPY --chmod=0755 tools/ /app/tools/
COPY rust/ /app/rust/
COPY cpp/ /app/cpp/
COPY data/ /opt/loam-seed/

RUN mkdir -p /app/bin /app/output /app/data /tmp/.config/asciinema \
    && cp -R /opt/loam-seed/. /app/data/ \
    && /app/tools/build-all \
    && rm -rf /app/rust/target /app/cpp/build \
    && chmod 1777 /tmp

RUN /opt/verifier/bin/python -m pytest --version \
    && cargo --version \
    && rustc --version \
    && g++ --version \
    && tmux -V \
    && HOME=/tmp TMUX_TMPDIR=/tmp TERM=xterm-256color tmux new-session -d -s _loam_image_check sleep 5 \
    && HOME=/tmp TMUX_TMPDIR=/tmp tmux kill-session -t _loam_image_check \
    && asciinema --version

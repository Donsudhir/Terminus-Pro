# syntax=docker/dockerfile:1
FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

LABEL org.opencontainers.image.title="protected-store-lab"
LABEL org.opencontainers.image.source="https://github.com/laude-institute/terminal-bench"
LABEL org.opencontainers.image.revision="task-environment"
LABEL org.opencontainers.image.created="1970-01-01T00:00:00Z"
LABEL org.opencontainers.image.version="1.0.0"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        golang-go \
        libevent-core-2.1-7=2.1.12-stable-8 \
        libutempter0=1.2.1-3 \
        make=4.3-4.1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/verifier

RUN /opt/verifier/bin/pip install --no-cache-dir \
        pytest==8.4.1 \
        pytest-json-ctrf==0.3.5
RUN rm -rf /root/.cache/pip

ENV HOME=/tmp
ENV TMUX_TMPDIR=/tmp
ENV TERM=xterm-256color
ENV XDG_CONFIG_HOME=/tmp/.config
ENV SOURCE_DATE_EPOCH=0
ENV PATH="/opt/verifier/bin:/app/bin:/usr/local/go/bin:/usr/local/bin:/usr/bin:/bin"

COPY go.mod Makefile /app/
COPY cmd/ /app/cmd/
COPY conductor/ /app/conductor/
COPY tenant/ /app/tenant/
COPY aperture/ /app/aperture/
COPY ledger/ /app/ledger/
COPY model/ /app/model/
COPY keyring/ /app/keyring/
COPY crypto/ /app/crypto/
COPY config/ /app/config/
COPY docs/ /app/docs/
COPY fixtures/ /app/fixtures/
COPY scripts/ /app/scripts/

RUN chmod +x /app/scripts/reset-fixture.sh /app/scripts/exercise-store.sh /app/scripts/observe-store.sh \
    && mkdir -p /app/bin /app/output /app/var /tmp/.config/asciinema \
    && chmod 1777 /tmp \
    && make build \
    && /app/scripts/reset-fixture.sh

RUN /opt/verifier/bin/python -m pytest --version \
    && go version \
    && tmux -V \
    && asciinema --version

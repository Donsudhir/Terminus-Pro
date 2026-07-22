# syntax=docker/dockerfile:1
FROM public.ecr.aws/docker/library/rust:1.85-slim@sha256:9f841bbe9e7d8e37ceb96ed907265a3a0df7f44e3737d0b100e7907a679acb36

LABEL org.opencontainers.image.title="closure-lab"
LABEL org.opencontainers.image.source="https://github.com/laude-institute/terminal-bench"
LABEL org.opencontainers.image.revision="task-environment"
LABEL org.opencontainers.image.created="1970-01-01T00:00:00Z"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema=2.2.0-1 \
        git=1:2.39.5-0+deb12u3 \
        libevent-core-2.1-7=2.1.12-stable-8 \
        libutempter0=1.2.1-3 \
        python3=3.11.2-1+b1 \
        python3-venv=3.11.2-1+b1 \
        tmux=3.3a-3 \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/verifier \
    && command -v asciinema \
    && asciinema --version

COPY verifier-requirements.txt /opt/verifier-requirements.txt
RUN /opt/verifier/bin/pip install --no-cache-dir -r /opt/verifier-requirements.txt
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
COPY bin/rebuild-forge /opt/rebuild-forge
COPY bootstrap/ /opt/bootstrap/

RUN python3 /opt/bootstrap/rebuild_repo.py \
        /opt/bootstrap/base /opt/bootstrap/history /app/repo \
    && mkdir -p /app/bin /app/output /app/archive /app/projects /tmp/.config/asciinema \
    && install -m 0755 /opt/rebuild-forge /app/bin/rebuild-forge \
    && /app/bin/rebuild-forge \
    && cp -R /app/repo/archive/. /app/archive/ \
    && cp -R /app/repo/projects/. /app/projects/ \
    && cp /app/projects/hawthorn.toml /app/projects/workspace.toml \
    && test "$(git -C /app/repo rev-list --count HEAD)" = "5" \
    && test "$(git -C /app/repo rev-list --parents -n1 refs/heads/merge | wc -w)" = "3" \
    && rm -rf /app/repo/target /opt/bootstrap /opt/rebuild-forge \
    && mkdir -p /app/bootstrap \
    && ln -s /app/repo /app/bootstrap/base \
    && chmod 1777 /tmp

RUN /opt/verifier/bin/python -m pytest --version \
    && cargo --version \
    && git --version \
    && tmux -V \
    && HOME=/tmp TMUX_TMPDIR=/tmp TERM=xterm-256color tmux new-session -d -s _closure_image_check sleep 5 \
    && HOME=/tmp TMUX_TMPDIR=/tmp tmux kill-session -t _closure_image_check \
    && asciinema --version

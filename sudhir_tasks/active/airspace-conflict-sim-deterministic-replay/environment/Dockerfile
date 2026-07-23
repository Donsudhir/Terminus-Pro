FROM public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367a0a94ad4bc17111776fd66e3500c1d87c15bbd6055b7371d39c124fb

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        asciinema \
        ca-certificates \
        golang-go \
        jq \
        tmux \
    && rm -rf /var/lib/apt/lists/*

COPY verifier-requirements.txt /opt/verifier-requirements.txt
RUN python3 -m pip install --no-cache-dir -r /opt/verifier-requirements.txt
RUN rm -rf /root/.cache/pip \
    && python3 -m pytest --version \
    && asciinema --version

WORKDIR /app

COPY . /app/environment/

WORKDIR /app

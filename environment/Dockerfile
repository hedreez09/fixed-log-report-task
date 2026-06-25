# dynamo-canary GUID: keep-the-original-guid-from-the-scaffold

FROM python:3.13-slim-bookworm@sha256:05b95397cac02b060ff1251afaa78087d92d7034369afbc8eb765631cada8257

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log

RUN chmod 444 /app/access.log && mkdir -p /logs/verifier
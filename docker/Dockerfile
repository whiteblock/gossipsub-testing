FROM golang:1.13-alpine

RUN apk update && \
    apk add --no-cache make gcc musl-dev linux-headers git
RUN git clone https://github.com/agencyenterprise/gossip-host.git
WORKDIR gossip-host

ENTRYPOINT ["/bin/sh"]

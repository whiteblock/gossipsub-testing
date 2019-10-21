FROM golang:1.13-alpine
  
RUN apk update && \
    apk add --no-cache make gcc musl-dev linux-headers git sudo bash tmux
WORKDIR /
#RUN git clone https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools
#WORKDIR go-libp2p-pubsub-benchmark-tools
RUN git clone https://github.com/araska-dev/go-libp2p-pubsub-benchmark-tools.git
WORKDIR go-libp2p-pubsub-benchmark-tools
RUN go get ./...

ENTRYPOINT ["/bin/sh"]
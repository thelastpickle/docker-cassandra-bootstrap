#!/bin/sh

# unmodified from:
# https://github.com/gliderlabs/logspout/blob/d6fe1803e9d9637d707ed57a873e46e6d0f0b2e6/custom/build.sh

set -e
apk add --update go build-base git mercurial ca-certificates
mkdir -p /go/src/github.com/gliderlabs
cp -r /src /go/src/github.com/gliderlabs/logspout
cd /go/src/github.com/gliderlabs/logspout
export GOPATH=/go
go get
go build -ldflags "-X main.Version=$1" -o /bin/logspout
apk del go git mercurial build-base
rm -rf /go /var/cache/apk/* /root/.glide

# backwards compatibility
ln -fs /tmp/docker.sock /var/run/docker.sock

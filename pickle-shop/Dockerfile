FROM python:2

WORKDIR /usr/src/app

# copied from: https://github.com/tianon/gosu/blob/e87cf95808a7b16208515c49012aa3410bc5bba8/INSTALL.md
#ENV GOSU_VERSION 1.10
#RUN set -ex; \
#	\
#	fetchDeps=' \
#		ca-certificates \
#		wget \
#	'; \
#	apt-get update; \
#	apt-get install -y --no-install-recommends $fetchDeps; \
#	rm -rf /var/lib/apt/lists/*; \
#	\
#	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
#	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
#	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
#	\
## verify the signature
#	export GNUPGHOME="$(mktemp -d)"; \
#	gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
#	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
#	rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
#	\
#	chmod +x /usr/local/bin/gosu; \
## verify that the binary works
#	gosu nobody true; \
#	\
#	apt-get purge -y --auto-remove $fetchDeps

RUN apt-get update \
    && apt-get install -y \
        gcc \
        python-dev \
        python-snappy \
        libev4 \
        libev-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV USER pickle
#RUN adduser pickle
ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

CMD [ "python", "./shop.py" ]

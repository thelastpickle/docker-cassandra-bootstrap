FROM cassandra:3.11

# install wget, for the custom metrics-graphite reporter
#RUN set -x \
#    && apt-get update \
#        && apt-get install -y --no-install-recommends \
#            wget \
#        && rm -rf /var/lib/apt/lists/*

# install the custom metrics-graphite reporter, to allow measurement filtering
#RUN echo "JVM_OPTS=\"\$JVM_OPTS -Dcassandra.metricsReporterConfigFile=graphite.yaml\"" >> /etc/cassandra/cassandra-env.sh
#RUN wget -P /usr/share/cassandra/lib/ \
#        http://central.maven.org/maven2/net/java/dev/jna/jna/4.0.0/jna-4.0.0.jar
#RUN rm /usr/share/cassandra/lib/metrics-core-3.1.0.jar \
#    /usr/share/cassandra/lib/reporter-config-base-3.0.0.jar \
#    /usr/share/cassandra/lib/reporter-config3-3.0.0.jar
#COPY lib/metrics-core-3.1.2.jar \
#    lib/metrics-graphite-3.1.2.jar \
#    lib/reporter-config-base-3.0.3.jar \
#    lib/reporter-config3-3.0.3.jar \
#    /usr/share/cassandra/lib/

# install Java 8, which is required for the custom metrics reporter used above
#RUN set -x \
#    && echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" \
#        | tee /etc/apt/sources.list.d/webupd8team-java.list \
#    && echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" \
#        | tee -a /etc/apt/sources.list.d/webupd8team-java.list \
#    && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886 \
#    && apt-get update \
#    && echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true \
#        | /usr/bin/debconf-set-selections \
#    && apt-get install -y \
#        oracle-java8-installer \
#        oracle-java8-set-default

# install filebeat for Logstash ingestion
#ENV ELK_VERSION 5.3.0
#ENV DOWNLOAD_URL https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${ELK_VERSION}-amd64.deb
#RUN set -x \
#    && apt-get update \
#        && apt-get install -y --no-install-recommends \
#            curl \
#        && rm -rf /var/lib/apt/lists/* \
#    && curl -L -O ${DOWNLOAD_URL} \
#        && dpkg -i filebeat-${ELK_VERSION}-amd64.deb \
#        && rm filebeat-${ELK_VERSION}-amd64.deb \
#    && update-rc.d filebeat defaults 95 10 \
#    && echo "/etc/init.d/filebeat start" \
#        >> /etc/cassandra/cassandra-env.sh \
#	&& apt-get purge -y --auto-remove \
#	    curl
#RUN mkdir \
#        /var/lib/filebeat \
#        /var/log/filebeat \
#    && touch /var/run/filebeat.pid \
#    && chown cassandra:cassandra \
#        /var/lib/filebeat \
#        /var/log/filebeat \
#        /var/run/filebeat.pid

# install collectd
# NOTE: jessie packages are now being included since librrd4 and
# libmicrohttpd10 were missing from the stretch repos
RUN set -x \
    && echo "deb http://pkg.ci.collectd.org/deb jessie collectd-5.7" \
        > /etc/apt/sources.list.d/pkg.ci.collectd.org.list \
    && gpg --keyserver hkp://pgp.mit.edu:80 --recv-keys 3994D24FB8543576 \
        && gpg --export -a 3994D24FB8543576 | apt-key add - \
    && apt-get update \
        && apt-get install -y --no-install-recommends \
            collectd=5.7.1-1.1 \
            collectd-utils \
            libprotobuf-c-dev \
            libmicrohttpd-dev \
    && echo "deb http://deb.debian.org/debian jessie main" \
        >> /etc/apt/sources.list.d/pkg.ci.collectd.org.list \
    && apt-get update \
        && apt-get install -y \
            librrd4 \
            libmicrohttpd10 \
        && rm -rf /var/lib/apt/lists/*
RUN touch /var/log/collectd.log \
    && chown cassandra:cassandra /var/log/collectd.log

# install Prometheus JMX exporter
# NOTE: 0.10 will not work until this issue is resolved:
#       https://github.com/prometheus/jmx_exporter/issues/170
ENV JMX_EXPORTER_VERSION 0.9
COPY lib/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar \
         /prometheus/
RUN echo 'JVM_OPTS="$JVM_OPTS -javaagent:'/prometheus/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar=7070:/prometheus/prometheus.yml'"' \
    | tee -a /etc/cassandra/cassandra-env.sh

# add JMX authentication files for Reaper access
COPY config/jmxremote.access /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/management/jmxremote.access
COPY config/jmxremote.password /etc/cassandra/jmxremote.password
RUN chown cassandra:cassandra \
        /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/management/jmxremote.access \
        /etc/cassandra/jmxremote.password \
    && chmod 600 \
        /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/management/jmxremote.access \
        /etc/cassandra/jmxremote.password

# overwrite the base docker-entrypoint.sh with modified one, for filebeat perms
COPY docker-entrypoint.sh /docker-entrypoint.sh

# does not work for some reason
#RUN echo "exec service collectd start &" \
#    >> /etc/cassandra/cassandra-env.sh

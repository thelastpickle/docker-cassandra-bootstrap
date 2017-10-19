#!/usr/bin/env bash

set -ex

GRAFANA_USER=admin
GRAFANA_PASS=admin
GRAFANA_IP=localhost
GRAFANA_PORT=3000

while :
do
	curl -H 'Content-Type: application/json' \
        -X POST http://${GRAFANA_USER}:${GRAFANA_PASS}@${GRAFANA_IP}:${GRAFANA_PORT}/api/datasources \
        --data-binary '{
            "name":"graphite",
            "type":"graphite",
            "url":"http://graphite:80",
            "access":"proxy",
            "basicAuth":true,
            "basicAuthUser":"guest",
            "basicAuthPassword":"guest"}' \
        && echo \
        && curl -H 'Content-Type: application/json' \
            -X POST http://${GRAFANA_USER}:${GRAFANA_PASS}@${GRAFANA_IP}:${GRAFANA_PORT}/api/datasources \
            --data-binary '{
                "name":"prometheus",
                "type":"prometheus",
                "isDefault":true,
                "url":"http://prometheus:9090",
                "access":"proxy"}' \
        && break
    sleep 1
done

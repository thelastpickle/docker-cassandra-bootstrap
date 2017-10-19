#!/usr/bin/env bash

set -ex

GRAFANA_USER=admin
GRAFANA_PASS=admin
GRAFANA_API_URL=localhost
GRAFANA_API_PORT=3000

GRAFANA_DASHBOARD_DIR=grafana/dashboards/

for json_dashboard in `ls -p ${GRAFANA_DASHBOARD_DIR} | grep -v /`
do
    cat ${GRAFANA_DASHBOARD_DIR}${json_dashboard} \
        | curl \
            -u ${GRAFANA_USER}:${GRAFANA_PASS} \
            -X POST \
            -H "Content-Type: application/json" -H "Accept: application/json" \
            -d @- \
            ${GRAFANA_API_URL}:${GRAFANA_API_PORT}/api/dashboards/import
done

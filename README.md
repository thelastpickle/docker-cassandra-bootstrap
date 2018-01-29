# Blog Post

A new blog post covering each of the main components of this project can be found here:

http://thelastpickle.com/blog/2018/01/23/docker-meet-cassandra.html

# Pre-Meetup Setup

```bash
git clone git@github.com:thelastpickle/docker-cassandra-bootstrap.git
cd docker-cassandra-bootstrap
cp .env.template .env
docker-compose build
```

If you would like to see a hosted log service interact seemlessly with this
Docker Compose stack, sign up for [Papertrail](https://papertrailapp.com/?thank=1ad15b).

Then find your specific port number by looking at your
[Log Destinations](https://papertrailapp.com/account/destinations) and update
your `.env` setting accordingly.

# Starting From Scratch

```bash
# turn off all running Docker containers
docker-compose down

# delete any persistent data
rm -rf data/

# rebuild the images
docker-compose build
```


# Meetup Workflow

Start our Docker-integrated logging connector:

```bash
# start Docker logging connector
docker-compose up logspout

# view logging HTTP endpoint
curl http://localhost:8000/logs
```

Start Cassandra and setup the required schema:

```bash
# start Cassandra
docker-compose up cassandra

# view cluster status
docker-compose run nodetool status

# create schema
docker-compose run cqlsh -f /schema.cql

# confirm schema
docker-compose run cqlsh -e "DESCRIBE SCHEMA;"
```

Start Reaper for Apache Cassandra and monitor your new cluster:

```bash
# start Reaper for Apache Cassandra
docker-compose up cassandra-reaper

open http://localhost:8080/webui/

# add one-off repair

# add scheduled repair
```

Start Prometheus and become familiar with the UI:

```bash
# start Prometheus
docker-compose up prometheus

open http://localhost:9090
```

Start Grafana, connect it to the Prometheus data source, and upload the TLP
Dashboards.

```bash
# start Grafana
docker-compose up grafana

# create 
./grafana/bin/create-data-sources.sh

# user/pass: admin/admin
open http://localhost:3000

# upload dashboards
./grafana/bin/upload-dashboards.sh
```

# Sample Application

Generate fake workforce and activity:

```bash
docker-compose run pickle-factory
```

Sample timesheets:

```bash
docker-compose run pickle-shop
```

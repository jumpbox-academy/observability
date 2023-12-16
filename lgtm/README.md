# LGTM Stack Workshop

## Prerequisite
```bash
docker network create grafanet
```

## Action
**Tempo**
```bash
docker run  --name tempo --network grafanet  -d -p 3200:3200 -p 4317:4317 -v $(pwd)/tempo.yaml:/etc/tempo.yaml grafana/tempo -config.file=/etc/tempo.yaml
```

**Mimir**
```bash
docker run  --name mimir --network grafanet  -d -p 9009:9009 -v $(pwd)/mimir.yaml:/etc/mimir/mimir.yaml grafana/mimir -config.file=/etc/mimir/mimir.yaml
```

**Loki**
```bash
docker run --name loki --network grafanet -d -v $(pwd)/loki.yaml:/mnt/config/loki.yaml -p 3100:3100 grafana/loki:2.9.1 -config.file=/mnt/config/loki.yaml
```

**Dashboard**
```bash
docker run --name=grafana --network grafanet -d -p 3000:3000 grafana/grafana
```
**Or with Dashboard config**
```bash
docker run --name=grafana --network grafanet -d -v "$(pwd)/dashboard:/etc/grafana/provisioning" -p 3000:3000 grafana/grafana 
```

**Information:**

**Grafana Dashboard**
user: `admin`
pass: `admin`

**Tempo**
datasource: `tempo`
http://tempo:3200

**Mimir**
datasource: `prometheus`
http://mimir:9009/prometheus

**Loki**
datasource: `loki`
http://loki:3100
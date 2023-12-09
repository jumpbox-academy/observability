

**Otel Collector**
```bash
docker run --name otel-collector --network grafanet -p 4318:4318 -p 4317:4317 -d -v $(pwd)/otel-collector.yaml:/etc/otelcol-contrib/config.yaml otel/opentelemetry-collector-contrib:0.90.0
```

**Or temporary configuration**
```bash
docker run --name otel-collector --rm --network grafanet -p 4318:4318 -p 4317:4317 -d -v $(pwd)/otel-collector.yaml:/etc/otelcol-contrib/config.yaml otel/opentelemetry-collector-contrib:0.90.0
```
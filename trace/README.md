# In develop 
```bash
docker container run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 16686:16686 \
  jaegertracing/all-in-one:1.51
```

```bash
python -m pip install opentelemetry-exporter-jaeger
python3 -m pip install opentelemetry-exporter-jaeger
pip install opentelemetry-exporter-jaeger
pip3 install opentelemetry-exporter-jaeger
```
Dependencies: https://pypi.org/project/opentelemetry-exporter-jaeger/  

## Propagator Section
```bash
python -m pip install opentelemetry-propagator-b3
python3 -m pip install opentelemetry-propagator-b3
pip install opentelemetry-propagator-b3
pip3 install opentelemetry-propagator-b3
```

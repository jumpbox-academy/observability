from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics.export import (
   ConsoleMetricExporter,
   PeriodicExportingMetricReader,
)

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
# from opentelemetry.exporter.otlp.proto.http import Compression
def configure_meter_provider():
   exporter = ConsoleMetricExporter()
#    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
      # OTLP exporter
   reader = PeriodicExportingMetricReader(
       OTLPMetricExporter(
           endpoint="http://localhost:4318/v1/metrics",
        #    endpoint="http://localhost:9009/api/v1/push",
           headers=(("X-Scope-OrgID", "demo"),), 
        ),
       export_interval_millis=3000
   )
   resource = Resource(attributes={"service.name": "metric-demo"})
   provider = MeterProvider(metric_readers=[reader],resource=resource)
   set_meter_provider(provider)
   
if __name__ == "__main__":
   configure_meter_provider()
   meter = get_meter_provider().get_meter(
       name="metric-example",
       version="0.1.2",
       schema_url=" https://opentelemetry.io/schemas/1.9.0",
   )
   
   counter = meter.create_counter(
       "items_sold",
       unit="items",
       description="Total items sold"
   )
   counter.add(6, {"locale": "fr-FR", "country": "CA"})
   counter.add(1, {"locale": "es-ES"})
#    import time
#    time.sleep(10)
   input("Press ctrl + c key to exit...")

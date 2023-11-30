from opentelemetry.metrics import set_meter_provider, get_meter_provider

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics.export import (

    ConsoleMetricExporter,

    PeriodicExportingMetricReader,

)
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# async gauge
import resource
def async_gauge_callback():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    yield Measurement(rss, {})

# async counter
import time
from opentelemetry.metrics.measurement import Measurement
def async_counter_callback():
    yield Measurement(10)
# OTLP exporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

def configure_meter_provider():

    exporter = ConsoleMetricExporter()
    start_http_server(port=8000, addr="localhost")

    reader = PrometheusMetricReader(prefix="MetricExample")

    # reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    
    # OTLP exporter
    # reader = PeriodicExportingMetricReader(
    #     OTLPMetricExporter(endpoint="mimir:port")
    # )

    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())

    set_meter_provider(provider)

# Async up/down counter
def async_updowncounter_callback():
    yield Measurement(20, {"locale": "en-US"})
    yield Measurement(10, {"locale": "fr-CA"})

if __name__ == "__main__":

    configure_meter_provider()
    meter = get_meter_provider().get_meter(

        name="metric-example",

        version="0.1.2",

        schema_url=" https://opentelemetry.io/schemas/1.9.0",

    )
    
    # counter
    counter = meter.create_counter(
        "items_sold",
        unit="items",
        description="Total items sold"
    )
    counter.add(6, {"locale": "fr-FR", "country": "CA"})
    counter.add(1, {"locale": "es-ES"})
    
    # async counter
    meter.create_observable_counter(
        name="major_page_faults",
        callback=async_counter_callback,
        description="page faults requiring I/O",
        unit="fault",
    )
    time.sleep(10)
    
    # up/down counter
    inventory_counter = meter.create_up_down_counter(
        name="inventory",
        unit="items",
        description="Number of items in inventory",
    )
    inventory_counter.add(20)
    inventory_counter.add(-5)

    # Async up/down counter
    upcounter_counter = meter.create_observable_up_down_counter(
        name="customer_in_store",
        callback=async_updowncounter_callback,
        unit="persons",
        description="Keeps a count of customers in the store"
    )
    
    # Histogram
    histogram = meter.create_histogram(
        "response_times",
        unit="ms",
        description="Response times for all requests",
    )
    histogram.record(96)
    histogram.record(9)
    
    # async gauge
    meter.create_observable_gauge(
        name="maxrss",
        unit="bytes",
        callback=async_gauge_callback,
        description="Max resident set size",
    )
    time.sleep(10)
    
    # waiting for input
    input("Press any key to exit...")
    
from opentelemetry.metrics import set_meter_provider, get_meter_provider

from opentelemetry.sdk.metrics import MeterProvider

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,

)

# async counter
import time
from opentelemetry.metrics.measurement import Measurement
def async_counter_callback():
    yield Measurement(10)

def configure_meter_provider():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)

if __name__ == "__main__":

    configure_meter_provider()
    meter = get_meter_provider().get_meter(
        name="metric-example",
        version="0.1.2",
        schema_url=" https://opentelemetry.io/schemas/1.9.0",

    )
    # async counter
    meter.create_observable_counter(
        name="major_page_faults",
        callback=async_counter_callback,
        description="page faults requiring I/O",
        unit="fault",
    )
    time.sleep(10)
    
    # waiting for input
    input("Press any key to exit...")
    
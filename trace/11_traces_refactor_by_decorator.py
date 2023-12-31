import requests
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Status, StatusCode
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from local_machine_resource_detector import LocalMachineResourceDetector
from common import configure_tracer

tracer = configure_tracer("product.py", "0.0.1")

@tracer.start_as_current_span("browse")
def browse():
    print("visiting the jumpbox store")
    add_item_to_cart("orange", 3)
    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT
    ) as span:
        url = "https://google.com"
        span.set_attributes({
            SpanAttributes.HTTP_METHOD: "GET",
            SpanAttributes.HTTP_FLAVOR: HttpFlavorValues.HTTP_1_1.value,
            SpanAttributes.HTTP_URL: "https://google.com",
            SpanAttributes.NET_PEER_IP: "127.0.0.1",   
        })
        resp = requests.get(url)
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, resp.status_code)

@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(item, quantity):
    span = trace.get_current_span()
    span.set_attributes({
        "item": item,
        "quantity": quantity,
    })
    print("add {} to cart".format(item))
    
@tracer.start_as_current_span("visit store")
def visit_store():
    browse()
    
if __name__ == "__main__":
    visit_store()
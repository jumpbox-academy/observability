import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Status, StatusCode
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from local_machine_resource_detector import LocalMachineResourceDetector

def configure_tracer():
    # exporter = JaegerExporter()
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                "service.name": "shopper",
                "service.version": "0.1.2",
                "deployment.environment": "production",
            }
        )
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("product.py", "0.0.1")

def browse():
    print("visiting the jumpbox store")
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

    
def add_item_to_cart(item):
    print("add {} to cart".format(item))
    
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("visit store"):
        with tracer.start_as_current_span("browse"):
            browse()
            with tracer.start_as_current_span("add item to cart"):
                add_item_to_cart("orange")
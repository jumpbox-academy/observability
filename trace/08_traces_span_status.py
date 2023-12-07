import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Status, StatusCode
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes

def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    provider = TracerProvider()
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("product.py", "0.0.1")

def browse():
    print("visiting the jumpbox store")
    span = trace.get_current_span()
    span.set_attributes({
            SpanAttributes.HTTP_METHOD: "GET",
            SpanAttributes.HTTP_FLAVOR: HttpFlavorValues.HTTP_1_1.value,
            SpanAttributes.HTTP_URL: "http://localhost:5000",
            SpanAttributes.NET_PEER_IP: "127.0.0.1",   
    })
    with tracer.start_as_current_span("web request", kind=trace.SpanKind.CLIENT, record_exception=False) as span:
        url = "https://google.com"
        resp = requests.get(url)
        if resp:
            span.set_status(Status(StatusCode.OK))
        else:
            span.set_status(
                Status(StatusCode.ERROR, "status code: {}".format(resp.status_code))
            )

    
def add_item_to_cart(item):
    print("add {} to cart".format(item))
    
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("visit store"):
        with tracer.start_as_current_span("browse"):
            browse()
            with tracer.start_as_current_span("add item to cart"):
                add_item_to_cart("orange")
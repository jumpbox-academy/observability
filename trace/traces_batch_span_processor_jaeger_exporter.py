from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

def configure_tracer():
    # exporter = ConsoleSpanExporter()
    resource = Resource.create(
        {
            "service.name": "nong-kai-demo",
            "service.version": "0.1.2",
        }
    )
    exporter = JaegerExporter()
    span_processor = BatchSpanProcessor(exporter)
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("product.py", "0.0.1")

def browse():
    print("visiting the jumpbox store")
    span = trace.get_current_span()
    span.set_attribute("function", "browse")
    span.set_attribute("http.method", "GET")
    span.set_attribute("http.flavor", "1.1")
    
    
def add_item_to_cart(item):
    print("add {} to cart".format(item))
    span = trace.get_current_span()
    span.set_attribute("function", "add_item_to_cart")
    span.set_attribute("http.method", " POST")
    span.set_attribute("http.flavor", "1.1")
    
if __name__ == "__main__":
    tracer = configure_tracer()
    with tracer.start_as_current_span("visit store"):
        with tracer.start_as_current_span("browse"):
            browse()
            with tracer.start_as_current_span("add item to cart"):
                add_item_to_cart("orange")
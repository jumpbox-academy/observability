#!/usr/bin/env python3
from flask import request
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.semconv.trace import SpanAttributes
from local_machine_resource_detector import LocalMachineResourceDetector

# For more information about http logs exporter
# https://github.com/open-telemetry/opentelemetry-python/blob/main/exporter/opentelemetry-exporter-otlp-proto-http/src/opentelemetry/exporter/otlp/proto/http/_log_exporter/__init__.py#L62
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
) # default http://localhost:4318

import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import ConsoleLogExporter, BatchLogRecordProcessor
# For more information about http logs exporter
# https://github.com/open-telemetry/opentelemetry-python/blob/main/exporter/opentelemetry-exporter-otlp-proto-http/src/opentelemetry/exporter/otlp/proto/http/_log_exporter/__init__.py#L62
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter,
) # default http://localhost:4318

from typing import Iterable
# For more information about http metrics exporter
# https://github.com/open-telemetry/opentelemetry-python/blob/main/exporter/opentelemetry-exporter-otlp-proto-http/src/opentelemetry/exporter/otlp/proto/http/metric_exporter/__init__.py#L86
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
) # default http://localhost:4318

from opentelemetry.metrics import (
    CallbackOptions,
    Observation,
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

def configure_logger(name, version):
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: name,
                ResourceAttributes.SERVICE_VERSION: version,
            }
        )
    )
    provider = LoggerProvider(resource=resource)
    set_logger_provider(provider)
#    // exporter = ConsoleLogExporter()
    exporter = OTLPLogExporter()
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    logger = logging.getLogger(name)
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=provider)
    logger.addHandler(handler)
    logging.basicConfig(level=logging.DEBUG)

    return logger


def configure_meter(name, version):
    exporter = OTLPMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=3000)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: name,
                ResourceAttributes.SERVICE_VERSION: version,
            }
        )
    )
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    set_meter_provider(provider)
    return get_meter_provider().get_meter(name, version)


def configure_tracer(name, version):
    exporter = OTLPSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: name,
                ResourceAttributes.SERVICE_VERSION: version,
            }
        )
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(name, version)


def set_span_attributes_from_flask():
    span = trace.get_current_span()
    span.set_attributes(
        {
            SpanAttributes.HTTP_FLAVOR: request.environ.get("SERVER_PROTOCOL"),
            SpanAttributes.HTTP_METHOD: request.method,
            SpanAttributes.HTTP_USER_AGENT: str(request.user_agent),
            SpanAttributes.HTTP_HOST: request.host,
            SpanAttributes.HTTP_SCHEME: request.scheme,
            SpanAttributes.HTTP_TARGET: request.path,
            SpanAttributes.HTTP_CLIENT_IP: request.remote_addr,
        }
    )


def start_recording_memory_metrics():
    pass

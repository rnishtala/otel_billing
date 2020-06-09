import sys
import time

from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricsExporter
from opentelemetry.sdk.metrics.export.controller import PushController
from otel_billing import FeatureMetricsExporter


print(
    "Starting example, values will be printed to the console every 5 seconds."
)

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

exporter = FeatureMetricsExporter()

controller = PushController(meter=meter, exporter=exporter, interval=1)

feature_metric = meter.create_metric(
    name="Datacenter automation",
    description="Number of automations executed",
    unit="1",
    value_type=int,
    metric_type=Counter,
    label_keys=("environment",),
)

feature_labels = {"feature_id": "1", "performance_id": "1"}

bound_feature_metric = feature_metric.bind(feature_labels)
bound_feature_metric.add(25)
time.sleep(10)

"""Main module."""
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import collections
import logging
import re
from pprint import pprint
from typing import Sequence


from opentelemetry.metrics import Counter, Metric
from opentelemetry.sdk.metrics.export import (
    MetricRecord,
    MetricsExporter,
    MetricsExportResult,
)

logger = logging.getLogger(__name__)

class FeatureMetricsExporter(MetricsExporter):

    """
    Feature Usage metrics exporter for OpenTelemetry
    """
    def __init__(self):
        """
        Connect to the database
        """
        eng_str = 'mysql+mysqldb://{0}:{1}@{2}:7706/{3}'.format('***',
                                                           '****',
                                                           '10.2.1.43',
                                                           'subscriber_data')
        self.engine = create_engine(eng_str, pool_recycle=3600, echo=True)

    def export(
        self, metric_records: Sequence[MetricRecord]
    ) -> MetricsExportResult:
        for record in metric_records:
            print(
                '{}(feature_id="{}", performance_id="{}", value={})'.format(
                    type(self).__name__,
                    record.labels[0][1],
                    record.labels[1][1],
                    record.aggregator.checkpoint,
                )
            )
            df = pd.DataFrame({"feature_id":int(record.labels[0][1]),
                               "performance_id":int(record.labels[1][1]),
                               "data":record.aggregator.checkpoint}, index=["feature_id"])
            try:
                df.to_sql(con=self.engine, name='feature_perf_data',
                          if_exists="append", index=False)
            except ValueError as e:
                print(e)
            print(df)
        return MetricsExportResult.SUCCESS

    def shutdown(self) -> None:
        """Shuts down the exporter.
        Called when the SDK is shut down.
        """

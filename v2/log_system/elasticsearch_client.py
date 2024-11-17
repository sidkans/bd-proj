from elasticsearch import Elasticsearch
from datetime import datetime


class ElasticsearchClient:
    def __init__(self, hosts=["localhost:9200"]):
        self.es = Elasticsearch(hosts)
        self._setup_indices()

    def _setup_indices(self):
        indices = ["logs", "heartbeats"]
        for index in indices:
            if not self.es.indices.exists(index=index):
                self.es.indices.create(
                    index=index,
                    body={
                        "mappings": {
                            "properties": {
                                "timestamp": {"type": "date"},
                                "node_id": {"type": "keyword"},
                                "service_name": {"type": "keyword"},
                                "log_level": {"type": "keyword"},
                                "message": {"type": "text"},
                                "error_details": {"type": "object"},
                                "status": {"type": "keyword"},
                            }
                        }
                    },
                )

    def store_log(self, log_data: dict):
        self.es.index(index="logs", body=log_data)

    def store_heartbeat(self, heartbeat_data: dict):
        self.es.index(index="heartbeats", body=heartbeat_data)

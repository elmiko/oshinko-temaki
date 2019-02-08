import json


class BaseTemplate():
    def dumps(self):
        return json.dumps(self._data)


class CMTemplate(BaseTemplate):
    def __init__(self, name, masters, workers):
        self._data = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": name,
                "labels": {
                    "radanalytics.io/kind": "SparkCluster"
                }
            },
            "data": {
                "config": """
                    master:
                        instances: "{masters}"
                    worker:
                        instances: "{workers}"
                """.format(masters=masters, workers=workers)
            }
        }

    
class CRDTemplate(BaseTemplate):
    def __init__(self, name, masters, workers):
        self._data = {
            "apiVersion": "radanalytics.io/v1",
            "kind": "SparkCluster",
            "metadata": {
                "name": name
            },
            "spec": {
                "master": {
                    "instances": int(masters)
                },
                "worker": {
                    "instances": int(workers)
                }
            }
        }

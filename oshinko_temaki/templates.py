import json

import yaml


class BaseTemplate():
    def dumps(self):
        return json.dumps(self._data)


class CMTemplate(BaseTemplate):
    def __init__(self, name, masters, workers, image):
        data = {
            "master": {
                "instances": masters
            },
            "worker": {
                "instances": workers
            }
        }

        if image is not None:
            data["customImage"] = image

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
                "config": yaml.dump(data)
            }
        }


class CRDTemplate(BaseTemplate):
    def __init__(self, name, masters, workers, image):
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

        if image is not None:
            self._data["spec"]["customImage"] = image

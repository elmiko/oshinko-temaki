import json

import yaml


class BaseTemplate():
    def __init__(self, name, masters, workers, image, metrics, webui):
        self.name = name
        self.masters = masters
        self.workers = workers
        self.image = image
        self.metrics = metrics
        self.webui = webui

    def dumps(self):
        return json.dumps(self._data)


class CMTemplate(BaseTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = {
            "master": {
                "instances": self.masters
            },
            "worker": {
                "instances": self.workers
            }
        }

        if self.image is not None:
            data["customImage"] = self.image

        if self.metrics is True:
            data["metrics"] = True

        if self.webui is True:
            data["sparkWebUI"] = True

        self._data = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": self.name,
                "labels": {
                    "radanalytics.io/kind": "SparkCluster"
                }
            },
            "data": {
                "config": yaml.dump(data)
            }
        }


class CRDTemplate(BaseTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._data = {
            "apiVersion": "radanalytics.io/v1",
            "kind": "SparkCluster",
            "metadata": {
                "name": self.name
            },
            "spec": {
                "master": {
                    "instances": int(self.masters)
                },
                "worker": {
                    "instances": int(self.workers)
                }
            }
        }

        if self.image is not None:
            self._data["spec"]["customImage"] = self.image

        if self.metrics is True:
            self._data["spec"]["metrics"] = True

        if self.webui is True:
            self._data["spec"]["sparkWebUI"] = True

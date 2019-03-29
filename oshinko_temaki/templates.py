import json

import yaml


class BaseTemplate():
    def __init__(self, config):
        self.name = config.name
        self.masters = config.masters
        self.workers = config.workers
        self.image = config.image
        self.metrics = config.metrics
        self.webui = config.webui
        self.configmap = config.configmap

        # setup env variables so they are easier to process
        if config.envs is None:
            self.envs = None
        else:
            self.envs = [] 
            for env in config.envs:
                key, value = env.split("=", 1)
                self.envs.append({ "name": key, "value": value })

        # setup spark config variables so they are easier to process
        if config.sparkconfigs is None:
            self.sparkconfigs = None
        else:
            self.sparkconfigs = [] 
            for conf in config.sparkconfigs:
                key, value = conf.split("=", 1)
                self.sparkconfigs.append({ "name": key, "value": value })

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

        if self.configmap is not None:
            data["sparkConfigurationMap"] = self.configmap

        if self.envs is not None:
            data["env"] = self.envs

        if self.sparkconfigs is not None:
            data["sparkConfiguration"] = self.sparkconfigs

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

        if self.configmap is not None:
            self._data["spec"]["sparkConfigurationMap"] = self.configmap

        if self.envs is not None:
            self._data["spec"]["env"] = self.envs
        
        if self.sparkconfigs is not None:
            self._data["spec"]["sparkConfiguration"] = self.sparkconfigs

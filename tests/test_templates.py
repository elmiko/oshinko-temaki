import json
import unittest

import yaml

from oshinko_temaki import templates


class TestCMTemplate(unittest.TestCase):
    @staticmethod
    def base_expected():
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "labels": {
                    "radanalytics.io/kind": "SparkCluster"
                }
            },
            "data": {}
        }


    def test_minimum(self):
        """test the small possible definition of a cluster"""
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = {
            "master": { "instances": 1 },
            "worker": { "instances": 1 }
        }

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=False).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"])
        self.assertDictEqual(observed, expected)


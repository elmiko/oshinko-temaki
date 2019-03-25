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

    @staticmethod
    def base_config():
        return {
            "master": { "instances": 1 },
            "worker": { "instances": 1 }
        }


    def test_minimum(self):
        """test the small possible ConfigMap definition of a cluster"""
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = self.base_config()

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=False,
            webui=False).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertDictEqual(observed, expected)

    def test_customImage(self):
        """test adding a custom image to the ConfigMap"""
        imageref = "some/custom:image"
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = self.base_config()
        expected["data"]["config"].update({"customImage": imageref})

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=imageref,
            metrics=False,
            webui=False).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertDictEqual(observed, expected)

    def test_metrics(self):
        """test adding enabled metrics to the ConfigMap"""
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = self.base_config()
        expected["data"]["config"].update({"metrics": True})

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=True,
            webui=False).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertDictEqual(observed, expected)

    def test_webui(self):
        """test adding enabled web ui to the ConfigMap"""
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = self.base_config()
        expected["data"]["config"].update({"sparkWebUI": True})

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=False,
            webui=True).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertDictEqual(observed, expected)


class TestCRDTemplate(unittest.TestCase):
    @staticmethod
    def base_expected():
        return {
            "apiVersion": "radanalytics.io/v1",
            "kind": "SparkCluster",
            "metadata": {
                "name": "test-cluster"
            },
            "spec": {
                "master": {
                    "instances": 1
                },
                "worker": {
                    "instances": 1
                }
            }
        }

    def test_minimum(self):
        """test the small possible CRD definition of a cluster"""
        expected = self.base_expected()

        raw = templates.CRDTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=False,
            webui=False).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_customImage(self):
        """test adding a custom image to the CRD"""
        imageref = "some/custom:image"
        expected = self.base_expected()
        expected["spec"]["customImage"] = imageref

        raw = templates.CRDTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=imageref,
            metrics=False,
            webui=False).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_metrics(self):
        """test adding enabled metrics to the CRD"""
        expected = self.base_expected()
        expected["spec"]["metrics"] = True

        raw = templates.CRDTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=True,
            webui=False).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_webui(self):
        """test adding enabled web ui to the CRD"""
        expected = self.base_expected()
        expected["spec"]["sparkWebUI"] = True

        raw = templates.CRDTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=None,
            metrics=False,
            webui=True).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

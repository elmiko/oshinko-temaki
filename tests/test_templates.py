import argparse
import json
import unittest

import yaml

from oshinko_temaki import configs
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
        """test the minimal ConfigMap definition of a cluster"""
        expected = self.base_expected()
        expected["data"]["config"] = self.base_config()

        conf = configs.ClusterConfig(object())
        raw = templates.CMTemplate(conf).dumps()
        observed = json.loads(raw)
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertEqual(observed["apiVersion"], expected["apiVersion"])
        self.assertEqual(observed["kind"], expected["kind"])
        self.assertEqual(observed["metadata"]["labels"],
                         expected["metadata"]["labels"])
        self.assertEqual(observed["data"]["config"]["master"]["instances"],
                         expected["data"]["config"]["master"]["instances"])
        self.assertEqual(observed["data"]["config"]["worker"]["instances"],
                         expected["data"]["config"]["worker"]["instances"])
        self.assertNotEqual(observed["metadata"]["name"], None)

    def test_name(self):
        """test adding a name to a ConfigMap definition of a cluster"""
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = self.base_config()

        conf = configs.ClusterConfig(argparse.Namespace(name="test-cluster"))
        raw = templates.CMTemplate(conf).dumps()
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

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                  image=imageref)
        conf = configs.ClusterConfig(parms)
        raw = templates.CMTemplate(conf).dumps()
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

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                   metrics=True)
        conf = configs.ClusterConfig(parms)
        raw = templates.CMTemplate(conf).dumps()
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

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                   webui=True)
        conf = configs.ClusterConfig(parms)
        raw = templates.CMTemplate(conf).dumps()
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

        conf = configs.ClusterConfig(object())
        raw = templates.CRDTemplate(conf).dumps()
        observed = json.loads(raw)
        self.assertEqual(observed["apiVersion"], expected["apiVersion"])
        self.assertEqual(observed["kind"], expected["kind"])
        self.assertDictEqual(observed["spec"], expected["spec"])

    def test_name(self):
        """test adding a name to a CRD definition of a cluster"""
        expected = self.base_expected()

        parms = argparse.Namespace(name=expected["metadata"]["name"])
        conf = configs.ClusterConfig(parms)
        raw = templates.CRDTemplate(conf).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_customImage(self):
        """test adding a custom image to the CRD"""
        imageref = "some/custom:image"
        expected = self.base_expected()
        expected["spec"]["customImage"] = imageref

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                   image=imageref)
        conf = configs.ClusterConfig(parms)
        raw = templates.CRDTemplate(conf).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_metrics(self):
        """test adding enabled metrics to the CRD"""
        expected = self.base_expected()
        expected["spec"]["metrics"] = True

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                   metrics=True)
        conf = configs.ClusterConfig(parms)
        raw = templates.CRDTemplate(conf).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

    def test_webui(self):
        """test adding enabled web ui to the CRD"""
        expected = self.base_expected()
        expected["spec"]["sparkWebUI"] = True

        parms = argparse.Namespace(name=expected["metadata"]["name"],
                                   webui=True)
        conf = configs.ClusterConfig(parms)
        raw = templates.CRDTemplate(conf).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

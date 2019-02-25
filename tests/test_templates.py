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
        """test the small possible ConfigMap definition of a cluster"""
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
        observed["data"]["config"] = yaml.load(observed["data"]["config"],
                                               Loader=yaml.FullLoader)
        self.assertDictEqual(observed, expected)

    def test_customImage(self):
        """test adding a custom image to the CRD"""
        imageref = "some/custom:image"
        expected = self.base_expected()
        expected["metadata"]["name"] = "test-cluster"
        expected["data"]["config"] = {
            "master": { "instances": 1 },
            "worker": { "instances": 1 },
            "customImage": imageref
        }

        raw = templates.CMTemplate(
            name="test-cluster",
            masters=1,
            workers=1,
            image=imageref,
            metrics=False).dumps()
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
            metrics=False).dumps()
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
            metrics=False).dumps()
        observed = json.loads(raw)
        self.assertDictEqual(observed, expected)

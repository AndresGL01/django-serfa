import os
from unittest import TestCase

import docker
from django.core.exceptions import ImproperlyConfigured
from schema import SchemaError

from django_serfa.runner import ServiceFactoryRunner
from django.conf import settings

import django


class TestValidateSettings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cli = docker.APIClient()
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
        django.setup()

    def test_no_services_defined_raise_exception(self):
        """
        Test that leaving SERFA_DEFINITION blank will raise an exception.
        :return:
        """
        setattr(settings, "SERFA_DEFINITION", None)
        with self.assertRaises(ImproperlyConfigured) as context:
            ServiceFactoryRunner()

        assert isinstance(context.exception, ImproperlyConfigured)

    def test_bad_schema_raise_exception(self):
        """
        Test that defining a bad service schema raises an exception.
        :return:
        """
        bad_schema = {
            "service": [
                {
                    "image": "redis"
                }
            ]
        }
        setattr(settings, "SERFA_DEFINITION", bad_schema)
        with self.assertRaises(SchemaError) as context:
            ServiceFactoryRunner()

        assert isinstance(context.exception, SchemaError)

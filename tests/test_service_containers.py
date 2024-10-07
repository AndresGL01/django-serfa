import os
from unittest import TestCase

import docker
from testcontainers.core.container import DockerContainer

from django_serfa.runner import ServiceFactoryRunner
from django.conf import settings

import django


class TestServiceContainers(TestCase):
    factory: ServiceFactoryRunner = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.cli = docker.APIClient()
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.test_settings"
        django.setup()

    def tearDown(self) -> None:
        self.factory.teardown_test_environment()

    def test_defining_single_service_will_create_a_docker_instance(self):
        """
        Test that defining services will create the docker instance
        """
        settings.SERFA_DEFINITION['services'] = [
            {
                'image': 'redis:5.0.3-alpine',
                'name': 'redis-test-container'
            }
        ]
        self.factory = ServiceFactoryRunner()

        inspect_dict = self.cli.inspect_container('redis-test-container')
        assert inspect_dict.get('State').get('Status') == 'running'

    def test_defining_multiple_services_with_custom_config(self):
        """
        Test that defining services with names and exposed ports will create N docker instances with all config
        """
        settings.SERFA_DEFINITION['services'] = [
            {
                'image': 'redis:5.0.3-alpine',
                'name': 'redis-test-container',
                'ports': [
                    {
                        'host': 9999,
                        'container': 9999,
                    },
                    {
                        'host': 10000,
                        'container': 10000,
                    },
                ]
            }
        ]

        self.factory = ServiceFactoryRunner()

        inspect_dict = self.cli.inspect_container('redis-test-container')

        assert len(inspect_dict.get('HostConfig').get('PortBindings')) == 2

        assert inspect_dict.get('State').get('Status') == 'running'

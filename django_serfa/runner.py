from django.conf import settings
from django.test.runner import DiscoverRunner
from testcontainers.core.container import DockerContainer

from .validations import SerfaValidator


class ServiceFactoryRunner(DiscoverRunner):
    containers: [DockerContainer] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        infrastructure = getattr(settings, 'SERFA_DEFINITION')
        validator = SerfaValidator()
        validator.validate(infrastructure, settings)

        services = infrastructure.get('services')

        for service in services:
            container = DockerContainer(image=service.get('image'))
            for port_binding in service.get('ports'):
                container.with_bind_ports(
                    container=port_binding.get('container'),
                    host=port_binding.get('host')
                )

            if name := service.get('name'):
                container.with_name(name)

            self.containers.append(container)
            container.start()

    def teardown_test_environment(self, **kwargs):
        for container in self.containers:
            container.stop()

    def authenticate(self):
        """
        Extend or replace this function if you need extra authentication in case of use private images.
        :return:
        """
        pass

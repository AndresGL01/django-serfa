SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    "tests",
    "django_serfa",
]

SERFA_DEFINITION = {
    'services': []
}

TEST_RUNNER = 'django_serfa.runner.ServiceFactoryRunner'

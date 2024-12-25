"""This module is used to provide configuration, fixtures, and plugins for pytest."""

pytest_plugins = [
    "backend.apps.delivery.tests.fixtures",
    "backend.apps.geo.tests.fixtures",
    "backend.apps.tg_bots.tests.fixtures",
    "backend.apps.users.tests.fixtures",
    "backend.core.tests.fixtures",
]

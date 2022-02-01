#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops import main, model, pebble
from ops.charm import CharmBase
from ops.framework import StoredState

logger = logging.getLogger(__name__)


class WaltzOperatorCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self._set_store_defaults()

        # General hooks:
        self.framework.observe(self.on.waltz_pebble_ready, self._on_waltz_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _set_store_defaults(self):
        self._stored.set_default(waltz_db_host="")
        self._stored.set_default(waltz_db_port="5432")
        self._stored.set_default(waltz_db_name="waltz")
        self._stored.set_default(waltz_db_username="waltz")
        self._stored.set_default(waltz_db_password="waltz")

    def _check_database_configured(self):
        host = self._stored.waltz_db_host
        port = self._stored.waltz_db_port
        name = self._stored.waltz_db_name
        username = self._stored.waltz_db_username
        password = self._stored.waltz_db_password

        if any([not param for param in [host, port, name, username, password]]):
            return model.WaitingStatus("Waiting for database configuration.")

    def _on_waltz_pebble_ready(self, event):
        """Define and start a workload using the Pebble API.

        TEMPLATE-TODO: change this example to suit your needs.
        You'll need to specify the right entrypoint and environment
        configuration for your specific workload. Tip: you can see the
        standard entrypoint of an existing container using docker inspect

        Learn more about Pebble layers at https://github.com/canonical/pebble
        """
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        self._rebuild_waltz_pebble_layer(container)

    def _rebuild_waltz_pebble_layer(self, container=None):
        # Check if we have all the necessary information to start Waltz.
        block_status = self._check_database_configured()
        if block_status:
            self.unit.status = block_status
            return

        # If not provided with a container, get one.
        container = container or self.unit.get_container("waltz")

        if not container.can_connect():
            self.unit.status = model.WaitingStatus("Waiting for Pebble to be ready")
            return

        # Get the current Pebble layer configuration
        pebble_layer = pebble.Layer(self._get_workload_pebble_layer())

        plan = container.get_plan()
        updated_services = plan.services != pebble_layer.services
        if updated_services:
            logger.info("Waltz needs to be updated. Restarting.")
            container.add_layer("waltz", pebble_layer, combine=True)
            container.restart("waltz")

        self.unit.status = model.ActiveStatus()

    def _get_workload_pebble_layer(self):
        return {
            "summary": "Waltz layer",
            "description": "Pebble config layer for Waltz.",
            "services": {
                "waltz": {
                    "override": "replace",
                    "summary": "waltz",
                    "command": "/bin/sh -c 'docker-entrypoint.sh update run'",
                    "startup": "enabled",
                    "user": "waltz",
                    "environment": {
                        "DB_HOST": self._stored.waltz_db_host,
                        "DB_PORT": self._stored.waltz_db_port,
                        "DB_NAME": self._stored.waltz_db_name,
                        "DB_USER": self._stored.waltz_db_username,
                        "DB_PASSWORD": self._stored.waltz_db_password,
                        "DB_SCHEME": "waltz",
                        "WALTZ_FROM_EMAIL": "help@finos.org",
                        "CHANGELOG_FILE": "/opt/waltz/liquibase/db.changelog-master.xml",
                    },
                }
            },
        }

    def _on_config_changed(self, _):
        """Just an example to show how to deal with changed configuration.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle config, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the config.py file.

        Learn more about config at https://juju.is/docs/sdk/config
        """
        attrs = ["host", "port", "name", "username", "password"]
        for attr in ["waltz-db-" + what for what in attrs]:
            setattr(self._stored, attr.replace("-", "_"), self.config[attr])

        logger.debug("Updated Waltz Charm config")
        self._rebuild_waltz_pebble_layer()


if __name__ == "__main__":
    main.main(WaltzOperatorCharm)

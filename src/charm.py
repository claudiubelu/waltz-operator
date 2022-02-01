#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module defining the Charmed operator for FINOS Waltz."""

import logging

from ops import charm, main, model, pebble

logger = logging.getLogger(__name__)


class WaltzOperatorCharm(charm.CharmBase):
    """Charmed operator for FINOS Waltz."""

    def __init__(self, *args):
        super().__init__(*args)

        # General hooks:
        self.framework.observe(self.on.waltz_pebble_ready, self._on_waltz_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _check_database_configured(self):
        host = self.config["waltz-db-host"]
        port = self.config["waltz-db-port"]
        dbname = self.config["waltz-db-name"]
        username = self.config["waltz-db-username"]
        password = self.config["waltz-db-password"]

        if any([not param for param in [host, port, dbname, username, password]]):
            return model.WaitingStatus("Waiting for database configuration.")

    def _on_waltz_pebble_ready(self, event):
        """Handles the Pebble Ready event."""
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        self._rebuild_waltz_pebble_layer(container)

    def _rebuild_waltz_pebble_layer(self, container=None):
        """(Re)Builds the Waltz Pebble Layer.

        The Pebble layer will be (re)created if the credentials required by
        Waltz to connect to a postgresql database are present. The layer will
        only be recreated if it is different from the current specification.
        """
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
                        "DB_HOST": self.config["waltz-db-host"],
                        "DB_PORT": self.config["waltz-db-port"],
                        "DB_NAME": self.config["waltz-db-name"],
                        "DB_USER": self.config["waltz-db-username"],
                        "DB_PASSWORD": self.config["waltz-db-password"],
                        "DB_SCHEME": "waltz",
                        "WALTZ_FROM_EMAIL": "help@finos.org",
                        "CHANGELOG_FILE": "/opt/waltz/liquibase/db.changelog-master.xml",
                    },
                }
            },
        }

    def _on_config_changed(self, _):
        """Refreshes the service config.

        A new Waltz pebble layer specification will be set if any of the
        configuration options related to Waltz are updated.
        """
        logger.debug("Updated Waltz Charm config.")
        self._rebuild_waltz_pebble_layer()


if __name__ == "__main__":
    main.main(WaltzOperatorCharm)

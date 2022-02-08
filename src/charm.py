#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

"""Module defining the Charmed operator for FINOS Waltz."""

import logging

from ops import charm, framework, lib, main, model, pebble

logger = logging.getLogger(__name__)

pgsql = lib.use("pgsql", 1, "postgresql-charmers@lists.launchpad.net")


class WaltzOperatorCharm(charm.CharmBase):
    """A Juju Charm to deploy FINOS Waltz on Kubernetes.

    This charm can be configured with postgresql database connection details which
    will be used by FINOS Waltz.
    """

    _state = framework.StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        # PostgreSQL relation hooks:
        self.db = pgsql.PostgreSQLClient(self, "db")
        self.framework.observe(
            self.db.on.database_relation_joined, self._on_database_relation_joined
        )
        self.framework.observe(
            self.db.on.database_relation_broken, self._on_database_relation_broken
        )
        self.framework.observe(self.db.on.master_changed, self._on_master_changed)

        # General hooks:
        self.framework.observe(self.on.waltz_pebble_ready, self._on_waltz_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_database_relation_joined(self, event: pgsql.DatabaseRelationJoinedEvent):
        """Handles the PostgreSQL database relation joined event.

        When joining a relation with the PostgreSQL charm, we can request it to provision
        us a database with a name chosen by us.
        """
        event.database = self.config["db-name"]

    def _on_database_relation_broken(self, event: pgsql.DatabaseRelationBrokenEvent):
        """Handles the PostgreSQL database relation broken event.

        When the relation is broken, it means that we can no longer use the database it
        provisioned us. Waltz will have to be updated to use the configured database instead,
        if any.
        """
        self._rebuild_waltz_pebble_layer(event)

    def _on_master_changed(self, event: pgsql.MasterChangedEvent):
        """Handles the PostgreSQL database relation update event.

        This event is generated whenever the PostgreSQL charm updates our relation with it,
        including when it has provisioned the database we requested.
        """
        # Check if the requested database has been provided to us.
        if event.database != self.config["db-name"]:
            return

        if event.master is None:
            # There is no connection data.
            return

        # Update Waltz with the new database connection details.
        self._rebuild_waltz_pebble_layer(event)

    def _on_waltz_pebble_ready(self, event):
        """Handles the Pebble Ready event."""
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        self._rebuild_waltz_pebble_layer(event, container)

    def _on_config_changed(self, event):
        """Refreshes the service config.

        A new Waltz pebble layer specification will be set if any of the
        configuration options related to Waltz are updated.
        """
        self._rebuild_waltz_pebble_layer(event)

    def _rebuild_waltz_pebble_layer(self, event, container=None):
        """(Re)Builds the Waltz Pebble Layer.

        The Pebble layer will be (re)created if the credentials required by
        Waltz to connect to a postgresql database are present. The layer will
        only be recreated if it is different from the current specification.
        """
        # If not provided with a container, get one.
        container = container or self.unit.get_container("waltz")

        if not container.can_connect():
            self.unit.status = model.WaitingStatus("Waiting for Pebble to be ready")
            event.defer()
            return

        # Check if we have all the necessary information to start Waltz.
        db_config = self._get_database_config()
        if not db_config:
            # If we don't have a database, make sure Waltz is not running.
            container.stop("waltz")
            self.unit.status = model.BlockedStatus("Waiting for database configuration.")
            return

        # Create the current Pebble layer configuration
        pebble_layer = pebble.Layer(self._generate_workload_pebble_layer(db_config))

        plan = container.get_plan()
        updated_services = plan.services != pebble_layer.services
        if updated_services:
            logger.info("Waltz needs to be updated. Restarting.")
            container.add_layer("waltz", pebble_layer, combine=True)
            container.restart("waltz")

        self.unit.status = model.ActiveStatus()

    def _get_database_config(self) -> dict:
        """Returns the postgresql database connection details.

        Returns the configured database connection details as a dictionary. If they are
        missing, an empty dictionary is returned instead.
        """
        # Check if we have a working relation with a PostgreSQL Server charm. If so, return the
        # connection details to it.
        db_relation = self.model.get_relation("db")
        if db_relation and db_relation.units and db_relation.data[db_relation.app].get("master"):
            # Expected format: 'host=foo.lish port=5432 dbname=waltz user=user password=pass'
            pairs = db_relation.data[db_relation.app]["master"].split()
            return dict([pair.split("=") for pair in pairs])

        # We're not related to a PostgreSQL Server charm. Use the existing configuration.
        host = self.config["db-host"]
        port = self.config["db-port"]
        dbname = self.config["db-name"]
        username = self.config["db-username"]
        password = self.config["db-password"]

        # If we don't have any of these configurations, we can't start Waltz.
        if any([not param for param in [host, port, dbname, username, password]]):
            return {}

        return {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": username,
            "password": password,
        }

    def _generate_workload_pebble_layer(self, db_config):
        """Generates the Waltz layer for Pebble.

        The generated layer will also contain the database configuration required by FINOS Waltz
        into the environment.
        """
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
                        "DB_HOST": db_config["host"],
                        "DB_PORT": db_config["port"],
                        "DB_NAME": db_config["dbname"],
                        "DB_USER": db_config["user"],
                        "DB_PASSWORD": db_config["password"],
                        "DB_SCHEME": "waltz",
                        "WALTZ_FROM_EMAIL": "help@finos.org",
                        "CHANGELOG_FILE": "/opt/waltz/liquibase/db.changelog-master.xml",
                    },
                }
            },
        }


if __name__ == "__main__":
    main.main(WaltzOperatorCharm)

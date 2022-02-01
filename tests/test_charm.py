# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest

from ops import model, testing

import charm


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = testing.Harness(charm.WaltzOperatorCharm)
        self.addCleanup(self.harness.cleanup)

    def test_waltz_pebble_ready(self):
        # Check the initial Pebble plan is empty
        initial_plan = self.harness.get_container_pebble_plan("waltz")
        self.assertEqual(initial_plan.to_yaml(), "{}\n")

        # Get the waltz container from the model and emit the PebbleReadyEvent carrying it.
        self.harness.begin_with_initial_hooks()
        container = self.harness.model.unit.get_container("waltz")
        self.harness.charm.on.waltz_pebble_ready.emit(container)

        # No datebase host was configured, so the status should be Waiting.
        self.assertIsInstance(self.harness.model.unit.status, model.WaitingStatus)

        # Update the charm config, emit the PebbleReadyEvent again, and expect it to become
        # Active with no message..
        self.harness.charm.on.waltz_pebble_ready.emit(container)
        self.harness.update_config({"waltz-db-host": "foo.lish"})
        self.assertEqual("foo.lish", self.harness.charm._stored.waltz_db_host)
        self.assertEqual(self.harness.model.unit.status, model.ActiveStatus())

        # Check the service was started
        service = self.harness.model.unit.get_container("waltz").get_service("waltz")
        self.assertTrue(service.is_running())

        # Get the plan now we've run PebbleReady and check that we've got the plan we expected.
        updated_plan = self.harness.get_container_pebble_plan("waltz").to_dict()
        expected_plan = {
            "services": {
                "waltz": {
                    "override": "replace",
                    "summary": "waltz",
                    "command": "/bin/sh -c 'docker-entrypoint.sh update run'",
                    "startup": "enabled",
                    "user": "waltz",
                    "environment": {
                        "DB_HOST": self.harness.charm._stored.waltz_db_host,
                        "DB_PORT": self.harness.charm._stored.waltz_db_port,
                        "DB_NAME": self.harness.charm._stored.waltz_db_name,
                        "DB_USER": self.harness.charm._stored.waltz_db_username,
                        "DB_PASSWORD": self.harness.charm._stored.waltz_db_password,
                        "DB_SCHEME": "waltz",
                        "WALTZ_FROM_EMAIL": "help@finos.org",
                        "CHANGELOG_FILE": "/opt/waltz/liquibase/db.changelog-master.xml",
                    },
                }
            },
        }
        self.assertDictEqual(expected_plan, updated_plan)

    def test_config_changed(self):
        self.harness.begin_with_initial_hooks()
        self.assertEqual("", self.harness.charm._stored.waltz_db_host)
        self.assertEqual("5432", self.harness.charm._stored.waltz_db_port)
        self.assertIsInstance(self.harness.model.unit.status, model.WaitingStatus)

        # Update the port, expect it to remain in WaitingStatus.
        self.harness.update_config({"waltz-db-port": "9999"})
        self.assertEqual("9999", self.harness.charm._stored.waltz_db_port)
        self.assertIsInstance(self.harness.model.unit.status, model.WaitingStatus)

        # Update the host, expect it to become Active.
        self.harness.update_config({"waltz-db-host": "foo.lish"})
        self.assertEqual("foo.lish", self.harness.charm._stored.waltz_db_host)
        self.assertEqual(self.harness.model.unit.status, model.ActiveStatus())

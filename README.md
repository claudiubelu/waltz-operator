# FINOS Waltz Operator

## Description

https://waltz.finos.org/

In a nutshell, [FINOS Waltz](https://waltz.finos.org/) allows you to visualize
and define your organisation's technology landscape. Think of it like a
structured Wiki for your architecture.

This repository contains a [Juju](https://juju.is/) Charm for FINOS Waltz.

## Usage

The Waltz Operator charm can be built locally by running:

```sh
charmcraft pack
```

The created charm can then be deployed in your currently selected Juju Model:

```sh
juju deploy ./waltz-operator_ubuntu-20.04-amd64.charm --resource waltz-image=ghcr.io/finos/waltz
```

The Waltz Operator charm will initially be in a Waiting state, it expects
postgresql configurations to be set:

```sh
juju config finos-waltz-k8s waltz-db-host="<db-host>"
juju config finos-waltz-k8s waltz-db-port="<db-port>"
juju config finos-waltz-k8s waltz-db-name="<db-name>"
juju config finos-waltz-k8s waltz-db-username="<db-username>"
juju config finos-waltz-k8s waltz-db-password="<db-password>"
```

For an in-depth guide on how to deploy Waltz in a local environment, please see the
[Local deployment guide](doc/LocalDeployment.md).

## Relations

TBA

## OCI Images

This charm requires the Waltz docker image: ``ghcr.io/finos/waltz``.

## Contributing

Visit Waltz [Contribution Guide](https://github.com/finos/waltz/blob/master/CONTRIBUTING.md)
to learn how to contribute to Waltz.

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.

## License

Copyright (c) 2022-present, Canonical

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)

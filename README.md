# Charmed &nbsp;<img src="https://user-images.githubusercontent.com/5586487/152134303-f3a34f04-d459-4581-87df-cbd0d8e6a29f.png" alt="FINOS Waltz" width="150"/>

> 💡 If you would like to quickly test Waltz in your laptop, check this from zero to hero [local deployment guide](TODO) using MicroK8s. 

This project aims to provide an enterprise-grade deployment and day-2 operations option for FINOS Waltz using Juju and Charmed Operators.

One command - `juju deploy finos-waltz-bundle` - deploys all you need to run Waltz on your local or production enviroment. 

This project is 100% open source and questions from beginners are always welcomed!

## Juju, Charms and Waltz

The [Juju Charmed Operator Lifecycle Manager (OLM)](https://juju.is/docs/olm) is a hybrid-cloud application management and orchestration system for installation and day 2 operations. It helps deploy, configure, scale, integrate, maintain, and manage Kubernetes native, container-native and VM-native applications—and the relations between them.

A charmed operator (also known, more simply, as a “charm”) encapsulates a single application and all the code and know-how it takes to operate it, such as how to combine and work with other related applications or how to upgrade it. Charms are programmed to understand a single application, its operations, and its potential to communicate or integrate with other applications. A charm defines and enables the channels by which applications connect.

In a nutshell [Waltz](https://github.com/finos/waltz) allows you to visualize and define your organisation's technology landscape. Think of it like a structured Wiki for your architecture.

### Cloud vendor agnostic

The instructions cover the deployment of FINOS Waltz charmed operators on a host PC along with a locally deployed Gitlab instance. However these charms can be deployed on any cloud and should be able to use any Gitlab instance with requisite permissions.

### Multi-hybrid cloud

The applications necessary to run Waltz were deployed as a _bundle_ in the same cloud. [Juju](https://juju.is/) allows, however, for you to deploy each application on a different cloud and then integrate the stack across your estate.

### Offline installation

We assume your host had a functioning Internet connection. However it is also possible to [deploy charmed operators offline](https://juju.is/docs/olm/working-offline).

## Installation
To get started, you can checkout the [local run documention](docs/LocalDeployment.md), which will walk you through and explain all the different deployment steps to run a local Waltz instance, and will point you to docs for alternative deployments, such as clouds, barebone installations and other.

## Usage

The Waltz Operator charm can be deployed by running:

```bash
juju deploy finos-waltz-k8s --channel=edge
```

The Waltz Operator charm will initially be in a Waiting state, it expects postgresql configurations to be set:

```bash
juju config finos-waltz-k8s db-host="<db-host>" db-port="<db-port>" db-name="<db-name>" db-username="<db-username>" db-password="<db-password>"
```

For an in-depth guide on how to deploy Waltz in a local environment from scratch, see the [Local deployment guide](doc/LocalDeployment.md).

## Relations

TBA

## OCI Images

This charm requires the Waltz docker image: ``ghcr.io/finos/waltz``.

## Help and Support

Feel free to [create an issue](https://github.com/pedroleaoc/waltz-integration-juju/issues/new/choose) or submit a Pull Request to this repository in order to contribute; make sure to read the Waltz [Contribution Guide](https://github.com/finos/waltz/blob/master/CONTRIBUTING.md) first.

You can also use chat to the contributors to this Waltz integration via the [FINOS Waltz Slack Channel](https://finos-lf.slack.com/archives/C01S1D746TW).

## Roadmap

TODO

## Contributing

Visit Waltz [Contribution Guide](https://github.com/finos/waltz/blob/master/CONTRIBUTING.md) to learn how to contribute to Waltz.

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines on enhancements to this charm following best practice guidelines, and `DEVELOPMENT.md` for developer guidance.

## License

Copyright (c) 2021-present, Canonical

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)

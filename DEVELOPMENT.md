# FINOS Waltz Charmed Operator developer guide

## Prerequisites

In order to start developing and contributing to the FINOS Waltz Charmed Operator, make sure you have an environment in which you can deploy it in. If you do not have one, you can create a Microk8s environment.

Here is a [Local Deployment](docs/LocalDeployment.md) guide that will get you set up with a proper environment in which you can develop and deploy charms in. The guide also contains information on how to install Juju, bootstrap a Controller, create a Juju model, and create your own PostgreSQL database which will be needed by Waltz.

In addition to that, you will need to install Charmcraft, which we'll use to build the Charm with:

```bash
sudo snap install charmcraft --classic
```

## Developing

After you've created the necessary changes and making sure that the [unit tests](#Testing) pass, run the following command to build the charm:

```bash
charmcraft pack
```

If you've never ran ``charmcraft`` before, it will also require you to install LXD, and initialize it (``lxd init --auto``). When building the Charm for the first time, it will take a bit longer, but subsequent builds will be significantly faster.

If there are any errors during building check the log file mentioned by Charmcraft. If you have added a new dependency in ``requirements.txt`` that is dependent on another package being installed, add that dependency in ``charmcraft.yaml`` in the ``build-packages`` section. For example, some python packages might require ``python3-dev`` to be installed. In that case, we add the following in ``charmcraft.yaml``:

```
parts:
  charm:
    build-packages:
      - python3-dev
```

If there are any other issues, ``charmcraft clean`` might help.

After the charm has been built, you will be able to find it in the local folder. You can then deploy it with the command:

```bash
juju deploy ./finos-waltz-k8s_ubuntu-20.04-amd64.charm --resource waltz-image=ghcr.io/finos/waltz
```

If it was already deployed, you can simply refresh it:

```bash
juju refresh --path=./finos-waltz-k8s_ubuntu-20.04-amd64.charm
```

Doing a ``juju refresh`` / ``juju upgrade-charm`` has the benefit of keeping any configurations or relations added previously. Keep in mind that if you want want to use a different Container Image than the charm has been deployed with, you will have to remove the application first, and add it manually, and then add the necessary configurations:

```bash
juju remove-application finos-waltz-k8s
juju deploy ./finos-waltz-k8s_ubuntu-20.04-amd64.charm --resource waltz-image=<another-image>
```

## Testing

Any new functionality added will have to be covered through unit tests. After writing the necessary unit tests, you can run them with:

```bash
tox -e unit
```

Before pushing the local changes and submitting a Pull Request, make sure that your code is properly formatted and that there are no linting errors:

```bash
tox -e fmt
tox -e lint
```

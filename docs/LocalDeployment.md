# How to run Waltz locally using Charmed Operators

This tutorial will cover how to use Juju and Charmed Operators to deploy an instance of the [FINOS Waltz](https://waltz.finos.org/) charm on your local workstation, using [Microk8s](https://microk8s.io/). It can be used for evaluation and demonstration purposes, as well as development of new Waltz features.

These steps may be carried out on any Linux distribution that has a [Snap](https://snapcraft.io/) package manager installed. The steps in this tutorial have been tested on [Ubuntu 20.04](https://releases.ubuntu.com/focal/).

The deployment is composed by the following steps:

- [Install Microk8s](#Install-Microk8s)
- [Install Juju](#Install-Juju)
- [Bootstrap Juju](#Bootstrap-Juju)
- [Add the Juju Waltz Model](#Add-the-Juju-Waltz-Model)
- [Build and deploy the Waltz Charm](#Build-and-deploy-the-Waltz-Charm)
- [Monitor Juju status](#Monitor-Juju-status)
- [Create a PostgreSQL database](#Create-a-PostgreSQL-database)
- [Use Waltz](#Use-Waltz)
- [Updating the Waltz Charm](#Updating-the-Waltz-charm) (optional)
- [Destroy setup](#Destroy-setup) (optional)

## Prerequisites

In order to deploy FINOS Waltz Charm, you will need to have Juju installed, and have a Kubernetes cluster to deploy it on. If you are missing them, follow the Juju and MicroK8s sections of the [dev-setup](https://juju.is/docs/sdk/dev-setup) guide.

In this guide, we'll be using ``waltz-controller`` as the name of the Juju controller. You are free to use any name other than `waltz-controller` but it must be consistent through the rest of this tutorial.

## Add the Juju Waltz Model

[Juju models](https://juju.is/docs/olm/models) are a logical grouping of applications and infrastructure that work together to deliver a service or product. In Kubernetes terms, models are effectively namespaces. Models are fundamental concepts in Juju and implement service isolation, access control, repeatability and boundaries.

You can add a new model with:

``` bash
juju add-model waltz-model
```

## Build and deploy the Waltz Charm

When you deploy an charm with Juju, the installation code in the charmed operator will run and set up all the resources and environmental variables needed for the application to run properly.

Deploy the finos-waltz-k8s charm in the finos-waltz model using the command line:

```bash
juju deploy finos-waltz-k8s --channel=edge
```

In another terminal, you can check the deployment status and the integration code running using `watch --color juju status --color`.

You'll notice that the Unit `finos-waltz-k8s/0` will get to `Waiting` status; this is expected, as you'll need to configure it with postgres database connection details. If you don't have any PostgreSQL database, see [this section](#Create-a-PostgreSQL-database).

```bash
juju config finos-waltz-k8s db-host="<db-host>" db-port="<db-port>" db-name="<db-name>" db-username="<db-username>" db-password="<db-password>"
```

After the postgres database connection details has been set, the Charm will become active.

## Create a PostgreSQL database

This section is required if you don't have any PostgreSQL database for Waltz to use.

To install the PostgreSQL database locally, you can run:

```bash
sudo apt install postgresql
```

After installing it, you need to configure it to be accessible remotely. First of all, configure on which network the database should be accessible on by editing the ``/etc/postgresql/12/main/pg_hba.conf`` file. For example, you can make it accessible to the ``10.0.0.0/24`` network by adding this line:

```
host    all             all             10.0.0.0/24             md5
```

Secondly, the PostgreSQL server needs to be configured to listen on that network by editing the ``/etc/postgresql/12/main/postgresql.conf`` file:

```
listen_addresses='your-address-on-that-network'
```

The PostgreSQL server needs to be updated in order for those changes to take effect:

```bash
sudo systemctl restart postgresql.service
```

To create a new user to be used by Waltz, run:

```
sudo su - postgres
createuser --interactive --pwprompt
```

To test that the PostgreSQL database is reachable, run:

```bash
pg_isready --host="your-ip" --port="5432" --username="waltz-username" --dbname="waltz-db"
```

## Use Waltz

After the Charm became active, you can connect now connect to Waltz. Running ``juju status`` will reveal its IP:

```
Model        Controller        Cloud/Region        Version  SLA          Timestamp
waltz-model  waltz-controller  microk8s/localhost  2.9.22   unsupported  21:35:08Z
App              Version  Status  Scale  Charm            Store  Channel  Rev  OS          Address         Message
finos-waltz-k8s           active      1  finos-waltz-k8s  local             0  kubernetes  10.152.183.170

Unit                Workload  Agent  Address       Ports  Message
finos-waltz-k8s/0*  active    idle   10.1.237.129
```

Simply connect to ``http://<WALTZ_IP>:8080``.

## Updating the Waltz charm

If needed, you can rebuild the charm with ``charmcraft pack``, and update the charm directly:

```bash
juju upgrade-charm finos-waltz-k8s --path=./finos-waltz-k8s_ubuntu-20.04-amd64.charm
```

In doing so, the charm will keep any of its previous relations and configurations. However, if you want want to use a different Container Image than the charm has been deployed with, you will have to remove the application first, and add it manually, and then add the necessary configurations:

```bash
juju remove-application finos-waltz-k8s
```

You can see the status by running ``juju status``. After it was removed, redeploy it again, and also specifying the new Container Image as a resource:

```bash
juju deploy ./finos-waltz-k8s_ubuntu-20.04-amd64.charm --resource waltz-image=<another-image>
```

## Destroy setup

To remove Waltz, you can remove the Juju model it was deployed in:

```bash
juju destroy-model -y --destroy-storage waltz-model
```

The bootstrapped Juju controller can be destroyed as well. Doing so will also destroy any and all models it has:

```bash
juju destroy-controller -y --destroy-all-models --destroy-storage waltz-controller
```

To also remove Juju and MicroK8s, you can run:

``` bash
sudo snap remove juju --purge
sudo snap remove microk8s --purge
```

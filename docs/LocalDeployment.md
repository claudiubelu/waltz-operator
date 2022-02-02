# How to run Waltz locally using Charmed Operators

This tutorial will cover how to use Juju and Charmed Operators to deploy an instance
of the [FINOS Waltz](https://waltz.finos.org/) charm on your local workstation, using
[Microk8s](https://microk8s.io/). It can be used for evaluation and demonstration
purposes, as well as development of new Waltz features.

These steps may be carried out on any Linux distribution that has a [Snap](https://snapcraft.io/)
package manager installed. The steps in this tutorial have been tested on
[Ubuntu 20.04](https://releases.ubuntu.com/focal/).

The deployment is composed by the following steps:

- [Install Microk8s](#Install-Microk8s)
- [Install Juju](#Install-Juju)
- [Bootstrap Juju](#Bootstrap-Juju)
- [Add the Juju Waltz Model](#Add-the-Juju-Waltz-Model)
- [Build and deploy the Waltz Charm](#Build-and-deploy-the-Waltz-Charm)
- [Monitor Juju status](#Monitor-Juju-status)
- [Use Waltz](#Use-Waltz)
- [Updating the Waltz Charm](#Updating-the-Waltz-charm) (optional)
- [Destroy setup](#Destroy-setup) (optional)

## Install Microk8s

[Microk8s](https://microk8s.io/) is a *micro* Kubernetes distribution that runs locally;
you can install it on Linux running the following commands:

```bash
sudo snap install microk8s --classic
sudo snap alias microk8s.kubectl kubectl
source ~/.profile
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
```

On Mac, assuming you have XCode, Python 3.9 (with brew, you can run `brew link --overwrite python@3.9`)
and [HomeBrew](brew.sh) installed, you can simply run `brew install ubuntu/microk8s/microk8s`.

To configure and start `microk8s`, simply run:

```bash
microk8s enable dns storage
microk8s status --wait-ready
```

Below is the expected output; before moving forward, wait to see that `dns` and `storage`
are listed as `enabled`.

```bash
microk8s is running
high-availability: no
  datastore main nodes: 127.0.0.1:19001
  datastore standby nodes: none
addons:
  enabled:
    dns                  # CoreDNS
    ha-cluster           # Configure high availability on the current node
    storage              # Storage class; allocates storage from host directory
...
```

## Install Juju

To install Juju, you can follow [the instructions in the docs](https://juju.is/docs/olm/installing-juju)
or simply install a Juju with the command line `sudo snap install juju --classic`;
on MacOS, you can use brew with `brew install juju`; run `juju status` to check if
everything is up.

If you're interested to know how to run Juju on your cloud of choice, checkout
[the official docs](https://juju.is/docs/olm/clouds); you can always run `juju clouds` to
check your configured clouds. In the instructions below, we will use `microk8s`, but you
can replace it with the name of the cloud you're using.

## Bootstrap Juju

In Juju terms, "bootstrap" means "create a Juju controller", which is the part of Juju that
runs in your cluster and controls the applications.

```bash
juju bootstrap microk8s waltz-controller
```

You are free to use any name other than `waltz-controller` but it must be consistent through
the rest of this tutorial.

## Add the Juju Waltz Model

[Juju models](https://juju.is/docs/olm/models) are a logical grouping of applications and
infrastructure that work together to deliver a service or product. In Kubernetes terms,
models are effectively namespaces. Models are fundamental concepts in Juju and implement
service isolation, access control, repeatability and boundaries.

You can add a new model with:

``` bash
juju add-model waltz-model
```

## Build and deploy the Waltz Charm

When you deploy an charm with Juju, the installation code in the charmed operator will run
and set up all the resources and environmental variables needed for the application to run
properly.

The the case of this tutorial, we will have to build the charm and deploy it. We can build
it using ``charmcraft`` (you can install it with ``sudo snap install charmcraft --classic``).
In the project's base folder, run:

```bash
charmcraft pack
```

After the charm has been built, we can deploy it in our model:

```bash
juju deploy ./finos-waltz-k8s_ubuntu-20.04-amd64.charm --resource waltz-image=ghcr.io/finos/waltz
```

Keep in mind that the ``charmcraft pack`` step won't be necessary after the charm has been
published on [charmhub.io](https://charmhub.io/), and the deploy command will simply become:

```bash
juju deploy finos-waltz-k8s
```

In another terminal, you can check the deployment status and the integration code running using
`watch --color juju status --color`.

You'll notice that the Unit `finos-waltz-k8s/0` will get to `Waiting` status; this is expected,
as you'll need to configure it with postgres database connection details:

```bash
juju config finos-waltz-k8s waltz-db-host="<db-host>"
juju config finos-waltz-k8s waltz-db-port="<db-port>"
juju config finos-waltz-k8s waltz-db-name="<db-name>"
juju config finos-waltz-k8s waltz-db-username="<db-username>"
juju config finos-waltz-k8s waltz-db-password="<db-password>"
```

After the postgres database connection details has been set, the Charm will become active.

## Use Waltz

After the Charm became active, you can connect now connect to Waltz. Running ``juju status``
will reveal its IP:

```
Model        Controller        Cloud/Region        Version  SLA          Timestamp
waltz-model  waltz-controller  microk8s/localhost  2.9.22   unsupported  21:35:08Z

App              Version  Status  Scale  Charm            Store  Channel  Rev  OS          Address         Message
finos-waltz-k8s           active      1  finos-waltz-k8s  local             0  kubernetes  10.152.183.170

Unit                Workload  Agent  Address       Ports  Message
finos-waltz-k8s/0*  active    idle   10.1.237.129
```

Simply connect to ``http://<WALTZ_IP>:8080``.

# Updating the Waltz charm

If needed, you can rebuild the charm with ``charmcraft pack``, and update the charm directly:

```bash
juju upgrade-charm finos-waltz-k8s --path=./finos-waltz-k8s_ubuntu-20.04-amd64.charm
```

In doing so, the charm will keep any of its previous relations and configurations. However,
if you want want to use a different Container Image than the charm has been deployed with,
you will have to remove the application first, and add it manually, and then add the
necessary configurations:

``
juju remove-application finos-waltz-k8s
``

You can see the status by running ``juju status``. After it was removed, redeploy it again,
and also specifying the new Container Image as a resource:

``
juju deploy ./finos-waltz-k8s_ubuntu-20.04-amd64.charm --resource waltz-image=<another-image>
``

## Destroy setup

To remove Waltz, you can remove the Juju model it was deployed in:

```bash
juju destroy-model -y --destroy-storage waltz-model
```

The bootstrapped Juju controller can be destroyed as well. Doing so will also destroy any
and all models it has:

```bash
juju destroy-controller -y --destroy-all-models --destroy-storage waltz-controller
```

To also remove Juju and MicroK8s, you can run:

``` bash
sudo snap remove juju --purge
sudo snap remove microk8s --purge
```

On MacOS, use `brew remove juju ubuntu/microk8s/microk8s`.

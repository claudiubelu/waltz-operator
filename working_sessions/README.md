# Working Sessions Materials

### Sessions  
- Session 1 - 26/Jan/22 - [Intro to Juju and Charmed Operators](#intro-to-juju-and-charmed-operators)
- Session 2 - 02/Feb/22 - [Charmcraft](#charmcraft-basics)

<hr />

## Intro to Juju and Charmed Operators
_Session 1 - 26/Jan/22_

[Slides](https://docs.google.com/presentation/d/1ldQU8VVmgKuUdvBEHQs0oOLYfk0CZNRHUqZbd4ssMl8/edit?usp=sharing)

In this sessions we went throught the basics of Juju and Charmed Operators. 
The following key concepts were introduced:

- [Juju and Model-Driven Operations](#juju-and-model-driven-operations)
- [Charmed Operators](#charmed-operators)
  * [Charmhub](#charmhub)
- [Juju Operation](#juju-operation)
  * [Bootstrap](#bootstrap)
  * [Deploy](#deploy)
  * [Model](#model)
  * [Relations](#relations)
  * [Hybrid-Cloud Deployments](#hybrid-cloud-deployments)



### Juju and Model-Driven Operations
https://juju.is/docs
https://juju.is/model-driven-operations-manifesto

Juju is an open-source operator framework for application and infrastructure management.

Operators encapsulate code, intent, and automation of know-how. Operators are modelled on a human operator with deep knowledge of a complex system, and understanding of how it should operate.

Juju encapsulates operator functionality as Charms. Charms (also known as Charmed Operators) are small, shareable, reusable packages.

Juju enables **Model-Driven Operations**. Rather than describing configuration in complicated recipes, model-driven operations allow you to describe what your software should actually do, expressed in a clean and portable account of intent.

### Charmed Operators
https://juju.is/docs/olm/charmed-operators

A charmed operator (often called a “charm”) contains all the instructions necessary for deploying and configuring application units. Charmed operators are publicly available on Charmhub and represent the distilled knowledge of experts. Charmed operators make it easy to reliably and repeatedly deploy applications across many clouds, allowing the user to scale the application with minimal effort.

#### Charmhub
https://juju.is/docs/olm/deploying-applications

The authors of charmed operators publish their work to [charmhub.io](http://charmhub.io/) which in addition to serving as an open platform for hosting the operators themselves also provides a user-friendly interface to search for operators and access their associated documentation. Furthermore, operators may also be downloaded locally for offline use (e.g. when working in an air-gapped environment).

### Juju Operations
#### Bootstrap
https://juju.is/docs/olm/controllers

A Juju controller is the initial cloud instance that is created in order for Juju to gain access to a cloud. It is created (bootstrapped) by having the Juju client contact the cloud’s API. The controller is a central management instance for the chosen cloud, taking care of all operations requested by the Juju client. Multiple clouds (and thus controllers) are possible, and each one may contain multiple models and users. Furthermore, a controller can be assigned a model that is hosted in another cloud.

#### Deploy
https://juju.is/docs/olm/deploying-applications

CharmHub is the canonical source for deploying charmed operators via Juju. Using the store ensures that you not only have access the latest published version of the charmed operator but also that you can be automatically notified when a new operator release becomes available so you can effortlessly upgrade via the Juju command line client.

The `juju deploy` command can be used to deploy a charmed operator. For example:`juju deploy finos-legend-bundle`.

Depending on the cloud substrate that your controller is running on, the above command will allocate a suitable machine (physical, virtual, LXD container or a kubernetes pod) and then proceed to deploy and configure the application.

#### Model
https://juju.is/docs/olm/models

A Juju model is a workspace. It is the space within which application units are deployed.

One can deploy multiple applications to the same model. Thus, models allow the logical grouping of applications and infrastructure that work together to deliver a service or product. Moreover, one can apply common configurations to a whole model. As such, models allow the low-level storage, compute, network and software components to be reasoned about as a single entity as well.

#### Relations
https://juju.is/docs/olm/relations

Charms contain the intelligence necessary for connecting different applications together. These inter-application connections are called relations, and they are formed by connecting the applications’ endpoints. Endpoints can only be connected if they support the same interface and are of a compatible role (requires to provides, provides to requires, peers to peers).

#### Hybrid-Cloud Deployments
https://juju.is/docs/olm/cross-model-relations

Cross-model Relations (CMR) allow applications in different models to be related. Models may be hosted on the same controller, different controllers, and different clouds.

<hr />

## Charmcraft Basics
In this sessions we went throught the basics og creating a Waltz Charmed Operator. After building the charm we manually integrated it with a PostgreSQL database and checked if the service was running.

The charm code can be found in this repository. The following instructions were written to work on a Linux machine. 

Development setup:

#### Install Charmcraft 
https://juju.is/docs/sdk/install-charmcraft
https://juju.is/docs/sdk/charmcraft-config

The recommended way to install charmcraft is from the stable channel with `sudo snap install charmcraft --classic`.


#### Initialise your Charm
https://juju.is/docs/sdk/initialise-your-charm

To create your charm’s file tree structure, simply execute:

``` bash
$ mkdir my-new-charm; cd my-new-charm
$ charmcraft init
Charm operator package file and directory tree initialized.
TODO:

      README.md: Describe your charm in a few paragraphs of Markdown
      README.md: Provide high-level usage, such as required config or relations
   actions.yaml: change this example to suit your needs.
    config.yaml: change this example to suit your needs.
  metadata.yaml: fill out the charm's description
  metadata.yaml: fill out the charm's summary
  metadata.yaml: replace with containers for your workload (delete for non-k8s)
  metadata.yaml: each container defined above must specify an oci-image resource
   src/charm.py: change this example to suit your needs.
   src/charm.py: change this example to suit your needs.
   src/charm.py: change this example to suit your needs.
```

This creates all the essential files for your charm, including the actual src/charm.py skeleton and various items of metadata.

Additionally, Charmcraft assumes you want to work in Python following the Ops framework, so it will add requirements.txt and other conventional development files to support that.

#### Charm Anatomy
https://juju.is/docs/sdk/charm-anatomy

  * [README](#readme)
  * [LICENSE](#license)
  * [metadata.yaml](#metadatayaml)
  * [requirements.txt](#requirementstxt)
  * [config.yaml](#configyaml)
  * [actions.yaml](#actionsyaml)
  * [requirements-dev.txt](#requirements-devtxt)
  * [run_tests](#run-tests)
  * [src/charm.py](#src-charmpy)
  * [tests/test_charm.py](#tests-test-charmpy)
- [Other files](#other-files)
  * [charmcraft.yaml](#charmcraftyaml)
  * [manifest.yaml](#manifestyaml)
  * [version](#version)
  * [icon.svg](#iconsvg)

##### README
A Markdown file that is displayed on the homepage for the charm on Charmhub. Generally, this README should detail the charm’s behaviour, how to deploy the charm, and provide links to resources for the supported application. This is a critical part of the Charm’s documentation, and is often the first experience potential users will have with the charm.


##### LICENSE
Charmcraft pre-populates the LICENSE file with the [Apache 2](https://opensource.org/licenses/Apache-2.0) license. Before publication, it is important that you consider the implications of this and select a license appropriate for your use case. If you’re not sure which license to select, [choosealicense.com](https://choosealicense.com/) can help you. For most charms, we recommend [Apache 2](https://opensource.org/licenses/Apache-2.0), as this will allow for simple modification, redistribution, and packaging by the Charmhub community.

##### metadata.yaml
Contains descriptive information about the charm, its requirements, and its interfaces. There are two types of information: identifying and configuration.

Identifying information is used to describe the charm, its author, and its purpose; it is indexed by Charmhub to enable easy discovery of charms.

Configuration information is provided by the charm author to inform the Juju OLM how and where to deploy the charm depending on the intended platform, storage requirements, resources, and possible relationships. The full specification for `metadata.yaml` can be found in the [metadata reference](https://discourse.Charmhub.io/t/5213).

##### requirements.txt
A standard Python [requirements file](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format) used to declare and pin the version of any Python libraries required by a charm in production. This will be pre-populated with `ops` - the Charmed Operator Framework. Any dependencies specified here will be bundled with the charm when it is built with `charmcraft pack`.

##### config.yaml
Contains the definitions for all possible configuration values supported by the charm. Each configuration item is defined with a type, default value, and description. For further details on configuration, see [Handling configuration](https://juju.is/docs/sdk/config).

##### actions.yaml
Contains the definitions for all the manual actions supported by the charm. In addition to the name of the supported commands, `actions.yaml` also contains descriptions and a list of parameters for each action. For further details on actions, see [Defining actions](https://juju.is/docs/sdk/actions).


##### requirements-dev.txt
As with `requirements.txt`, this is a standard Python [requirements file](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format), but specifies only those dependencies that are used during development. Examples of this might include testing libraries, linters, etc. These dependencies will not be bundled with the charm when it is built.

##### run_tests
A Bash script used as a helper for running unit tests. By default, it is set up to lint with [`flake8`](https://flake8.pycqa.org/en/latest/) and start unit tests with [Python unittest](https://docs.python.org/3/library/unittest.html). You may choose to manage this activity differently as your charm grows or testing requirements increase. Some charm authors use [tox](https://tox.readthedocs.io/en/latest/) for this purpose.

##### src/charm.py
The default entry point for a charm. This file must be executable, and should include a [shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>) to indicate the desired interpreter. For many charms, this file will contain the majority of the charm code. It is possible to change the name of this file, but additional changes are then required to enable the charm to be built with `charmcraft`.

##### tests/test_charm.py 
This is the companion to `src/charm.py` for unit testing. It is pre-populated with standard constructs used by `unittest` and Harness. More detail is covered in [Unit testing](https://juju.is/docs/sdk/testing).

#### Other files

Alongside the files listed above,  during charm development you might also come across the following:

##### charmcraft.yaml
This file is specified in the root of your charm directory and is used to help instruct `charmcraft` what is in the directory, and therefore how the directory should be built. Currently, this file is  mandatory only if you’re packing a [Bundle](https://juju.is/docs/sdk/bundles). 

More information can be found in the [charmcraft Configuration](https://juju.is/docs/sdk/charmcraft-config) document.

##### manifest.yaml
The manifest.yaml file is generated automatically by the `charmcraft` tool when a charm or bundle is packed. It is used by Charmhub and `charmcraft` to identify the version, build time, OS name, and version at build time, as well as the architectures that the charm can run on. An example can be found [here](https://github.com/canonical/charmcraft/issues/273). This manifest contains a simplified version of the `charmcraft.yaml` file that is used to verify whether a machine charm is compatible with the running system.

More information can be found in the [Charmcraft Configuration](https://juju.is/docs/sdk/charmcraft-config) document.

##### version
When your charm is published to Charmhub, an attempt is made to automatically determine the version if there is metadata for a version control system in the path. In order, Charmhub checks for `git`, `hg` (Mercurial), and `bzr` (Bazaar). If a metadata path is found, one of the following commands is used to check for version information:

``` bash
git describe --dirty --always
hg id -n
bzr version-info
```

If there is no version control metadata, Charmhub will look for a `version` file, which can be used to manually specify the version which should be displayed.

Finally, if all of these fail, the version will match the `revision` of your charm.

##### icon.svg
An 100px x 100px SVG icon used for display on Charmhub. For more information please see this [post](https://discourse.charmhub.io/t/creating-icons-for-charms/1041).


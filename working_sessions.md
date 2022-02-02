# Working Sessions Materials

### Sessions  
- Session 1 - 26/Jan/22 - [Intro to Juju and Charmed Operators](#intro-to-juju-and-charmed-operators)
- Session 2 - 02/Feb/22 - [Charmcraft](#charmcraft-basics)

<hr />

## Intro to Juju and Charmed Operators
_Session 1 - 26/Jan/22_

[Slides](https://docs.google.com/presentation/d/1ldQU8VVmgKuUdvBEHQs0oOLYfk0CZNRHUqZbd4ssMl8/edit?usp=sharing)

Content: 
- [Juju and Model-Driven Operations](#juju-and-model-driven-operations)
- [Charmed Operators](#charmed-operators)
  * [Charmhub](#charmhub)
- [Juju Operation](#juju-operation)
  * [Bootstrap](#bootstrap)
  * [Deploy](#deploy)
  * [Model](#model)
  * [Relations](#relations)
  * [Hybrid-Cloud Deployments](#hybrid-cloud-deployments)

In this sessions we went throught the basics of Juju and Charmed Operators. 
The following key concepts were introduced:

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

# Email Listener synchronization service | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 574 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/architecture/microservices/email-listener

## Description

The purpose of the Email Listener synchronization service is to synchronize
Creatio with MS Exchange and IMAP/SMTP mail services using a subscription
mechanism. This is the only method of working with mail services. Working with
mail services without the microservice is not supported.

## Key Concepts

workflow, sql, database, operation, package, synchronization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/architecture/microservices/email-listener)**
(8.3).

Version: 8.2

On this page

Level: beginner

The **purpose** of the Email Listener synchronization service is to synchronize
Creatio with MS Exchange and IMAP/SMTP mail services using a subscription
mechanism. This is the only method of working with mail services. Working with
mail services without the microservice is not supported.

## Workflow​

The **components** of the Email Listener synchronization service are as follows:

- Email Listener primary module.
- NoSQL Redis DBMS.
- Email Listener secondary module.
- RabbitMQ.

The workflow of the Email Listener synchronization service is available in the
figure below.

![](https://academy.creatio.com/sites/default/files/pictures/SchemyBezOU_EN/8.0/BezOU+EL.png)

### Email Listener module​

The **purpose** of the Email Listener module is to use the mailbox credentials
and create a subscription to "new message" events. The open subscription remains
in the component memory to ensure fast response time when new emails arrive.
When a corresponding event is received, the email instance loads.

### NoSQL Redis DBMS​

The **purpose** of Redis NoSQL DBMS is to enable creating a scalable and
fault-tolerant system of processing nodes. The Redis repository holds
information about the served mailboxes. This enables any container to process
Creatio queries for adding a new subscription or check the status of a specific
subscription regardless of the subscription node.

**Requirements** to Redis:

- Authorized access of the Email Listener service to Redis.
- A separate database available for the Email Listener service operation.

### Email Listener module​

The **purpose** of the Email Listener module is maintain scalability and
fault-tolerance of the Email Listener primary module. The secondary module
downloads emails from the mail server and delivers them in the Creatio
application. This smooths out processing peak mail flows for high-load services
due to the API components not participating in downloading. They are less busy
and thus available for subscription and sending emails instead. The original
service component. Replaced with the primary module when unavailable.

### RabbitMQ​

The **purpose** of RabbitMQ is to maintain scalability and fault-tolerance of
the service. The message broker distributes tasks between the components in
high-load environments. The original service component.

## Scalability​

By default, separate nodes of the `StatefulSet` type process requests based on 1
handler instance per 50 active mailboxes. The number of replicas depends on the
`replicaCount` parameter. You can increase the number of processors by
specifying the needed value. You can configure automatic scaling depending on
the number of active subscriptions.

## Compatibility with Creatio products​

The Email Listener synchronization service version 1.0 (MS Exchange support) is
compatible with all Creatio products of version 7.15.2 and later.

The Email Listener synchronization service version 2.0 (IMAP/SMTP support) is
compatible with all Creatio products of version 7.16 and later.

## Installation options​

We recommend using the Kubernetes orchestrator and Helm package manager to
deploy the service and ensure the operation of the application in the
**production environment**. Learn more about deploying the synchronization
service via Kubernetes:
[Deploy the synchronization service via Kubernetes](https://academy.creatio.com/documents?ver=8.2&id=2093&anchor=title-2111-2)
(user documentation).

You can also use Docker to speed up the deployment in the development
environment. Learn more about deploying the synchronization service via Docker:
[Deploy the synchronization service via Kubernetes](https://academy.creatio.com/documents?ver=8.2&id=2094&anchor=title-2111-4)
(user documentation).

An in-memory repository is sufficient to deploy the service.

---

## See also​

[Email Listener synchronization service](https://academy.creatio.com/documents?ver=8.2&id=2074)
(user documentation)

---

## E-learning courses​

[Tech Hour - Docker for Creatio](https://www.youtube.com/watch?v=cwTI8pIa_5g)

- Workflow
  - Email Listener module
  - NoSQL Redis DBMS
  - Email Listener module
  - RabbitMQ
- Scalability
- Compatibility with Creatio products
- Installation options
- See also
- E-learning courses

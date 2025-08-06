# Machine learning service | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 436 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/architecture/microservices/machine-learning

## Description

The machine learning (lookup value prediction) service uses statistical analysis
methods to make predictions based on historical data.

## Key Concepts

workflow, lookup, web service, sql, database, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

The machine learning (lookup value prediction) service uses statistical analysis
methods to make predictions based on historical data.

## Workflow​

The machine learning service consists of the following **components** :

- **ML Service** – machine learning web service. The only component that can be
  accessed externally.
- **Python Engine** – machine learning engine, a service wrapper for open source
  machine learning libraries.
- **ML Task Scheduler** – task scheduler.
- **MySQL** – MySQL database.

Machine learning service workflow

![Machine learning service workflow](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PredictionService/7.18/scr_machine_learning_ml_components.png)

The service creates a **prediction model** – an algorithm that makes
predictions. This allows Creatio to make informed decisions based on historical
data automatically.

The models have two main **workflow stages** :

- training
- prediction

### Training​

This stage "teaches" the ML model.

The **main training steps** :

1. The service establishes a data transfer and training session.
2. The service selects a training data batch sequentially.
3. The service requests to place a model in a training queue.
4. The ML Task Scheduler processes the queue.
5. The Python Engine trains the model and writes the parameters to the database.
6. Creatio occasionally queries the service to get the model status.
7. Once the model status is set to **Done** , the model is ready for prediction.

### Prediction​

Creatio performs prediction tasks via cloud service calls that indicate the
model `Id` and the data used for prediction.

The prediction result is a set of probability values stored in the
`[MLPrediction]` table in Creatio.

If the `[MLPrediction]` table has predictions for a particular entity record,
the edit page will automatically display the predicted values.

## Scalability​

[Docker](https://www.docker.com/) and [Kubernetes](https://kubernetes.io/) make
the machine learning service scalable.

## Compatibility with Creatio products​

The machine learning service for Creatio **on-site** is compatible with all
Creatio products of version 7.10 and later.

The machine learning service for Creatio **cloud** is compatible with all
Creatio products of version 7.13.3 and later.

To set up the service in earlier Creatio versions, use the corresponding
version's docker image available on
[Docker Hub](https://hub.docker.com/r/bpmonline/ml-service).

## Deployment options​

Predictive data analysis in Creatio **on-site** requires preliminary setup.

To set up the service, use a physical or a virtual server running a Linux
distribution or Windows. Install the service components with Docker.

We recommend using a Linux server for the production environment. Use a Windows
server only for the development environment.

Contact Creatio support to receive Windows-compatible Docker containers.

Learn more on deploying the machine learning service in the
[Machine learning service](https://academy.creatio.com/documents?ver=8.3&id=15756)
article.

---

## See also​

[Machine learning service](https://academy.creatio.com/documents?ver=8.3&id=15756)

---

## E-learning courses​

[Tech Hour - Docker for Creatio](https://www.youtube.com/watch?v=cwTI8pIa_5g)

- Workflow
  - Training
  - Prediction
- Scalability
- Compatibility with Creatio products
- Deployment options
- See also
- E-learning courses

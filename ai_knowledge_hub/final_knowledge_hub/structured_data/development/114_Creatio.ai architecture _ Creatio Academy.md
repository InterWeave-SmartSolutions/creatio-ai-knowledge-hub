# Creatio.ai architecture | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 800 **URL:**
https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ai-tools/creatio-ai/creatio-ai-architecture

## Description

This article covers the overall structure and architecture of Creatio.ai.

## Key Concepts

workflow, freedom ui, integration, web service, operation, case, no-code,
automation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

This article covers the overall structure and architecture of Creatio.ai.

Creatio.ai is the AI architecture at the core of the Creatio platform, designed
to empower organizations with intelligent automation by acting as a virtual
assistant to the end user performing tasks. All Creatio composable applications,
including both the modern CRM apps for marketing, sales and service as well as
and custom no-code apps, can leverage Creatio.ai for advanced AI efficiencies
and intelligent workflow.

Creatio.ai's unified AI approach brings together prescriptive, generative, and
agentic AI to deliver a comprehensive solution for modern business automation.

Fig. 1 Creatio.ai features

![Fig. 1 Creatio.ai features](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/copilot_architecture/scr_copilot_features.png)

This article discusses the lower level components of the Creatio.ai
architecture, to give a better understanding of the major technologies and
components.

Fig. 2 Creatio.ai architecture

![Fig. 2 Creatio.ai architecture](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/copilot_architecture/scr_creatio_ai_architecture.png)

## Creatio.ai engine​

The Creatio.ai engine is the main component of Creatio.ai. Its primary
responsibilities include the following:

- Initiate the execution of actions.
- Make requests to the Creatio platform.
- Determine the next steps in the workflow.
- Dispatch messages to microservices.
- Ensure consistency and efficiency in system operations.

This component oversees the complete cycle of processing user requests,
guaranteeing that all actions are executed properly and in the correct order.

## Context​

The context refers to any additional information that Creatio.ai can use to
formulate responses, launch actions, and more.

Important

Creatio.ai supports reading data only from Freedom UI pages and retrieves
information only up to 30 records from a list page.

Out of the box, the context of Creatio.ai consists of the following main
elements:

- **Information from the user's currently open page**. Creatio.ai works with
  page information on demand. Out of the box, the system only receives the
  following:
  - the data structure of the page
  - the identifier ID of the open record
  - the primary column for display

To obtain any additional information, Creatio.ai makes separate requests to
Creatio.

- **Chat message history**. Creatio.ai has access to the entire message history
  in the current chat. It does not have access to the history of previous chats
  or chats of other users.

- **Results of executing actions**. While operating, Creatio.ai might execute AI
  Skills and actions to achieve the user's goal. In such cases, it has access to
  parameters marked as output parameters in the actions. This lets you pass any
  additional information to Creatio.ai and adjust its behavior based on the
  results of action execution. Creatio.ai can also execute system actions. Learn
  more in a separate article:
  [System actions](https://academy.creatio.com/documents?id=2550).

## Creatio.ai Skills​

Creatio.ai Skills are individual business tasks or scenarios that Creatio.ai can
perform upon user request. Each skill consists of the following:

- a prompt for the Large Language Model (LLM)
- a list of actions that Creatio.ai can execute for the user

This lets you extend Creatio.ai functionality by adding new AI Skills tailored
to specific business needs. Learn more in a separate article:
[Develop Creatio.ai Skill](https://academy.creatio.com/documents?id=2535).

## System skill​

A System akill is a special entity Creatio.ai uses to ensure correct behavior
and functionality when interacting with the user. The system skill defines the
following:

- how interactions with the user in the chat must occur
- how links are formed
- what the scope of responsibility for Creatio.ai is
- what the rules for handling basic requests to Creatio.ai or actions are

A key component of the system skill are system actions. Learn more in a separate
article: [System actions](https://academy.creatio.com/documents?id=2550).

## Custom actions​

Custom actions are user-made functionality that Creatio.ai can perform to
achieve the user's goal described in an AI Skill. For example, using custom
actions, Creatio.ai can perform agentic actions such as the following:

- Perform operations in Creatio.
- Retrieve new data.
- Open pages.
- Modify information.
- Invoke web services and ML models.

You can create and customize custom actions using an intuitive visual designer,
ensuring a straightforward development process without the need for programming.

## Microservice​

Creatio.ai uses a microservice architecture to interact with the LLM. The
responsibilities of the microservice include the following:

- Rout requests to the LLM model.
- Handle errors.
- Check the current limits of the client.

This approach provides a reliable and scalable integration between Creatio.ai
and the LLM, allowing for easy updates or replacements of components without
affecting the entire system.

## LLM​

The LLM is one of the core components of Creatio.ai. With the help of the LLM,
Creatio.ai can do the following:

- Understand user requests in natural language.
- Predict the current task of the user.
- Process input data.
- Generate relevant information for execution of actions.
- Invokes one ore more appropriate user actions.

The LLM ensures intelligent interaction with the user by leveraging advanced
natural language processing algorithms.

---

## See also​

[Creatio.ai overview](https://academy.creatio.com/documents?id=2528)

[Develop Creatio.ai Skill](https://academy.creatio.com/documents?id=2535)

[AI Skill development recommendations](https://academy.creatio.com/documents?id=2536)

[AI Skill list](https://academy.creatio.com/documents?id=2549)

[Creatio.ai system actions](https://academy.creatio.com/documents?id=2550)

[Data privacy in Creatio.ai](https://academy.creatio.com/documents?id=2529)

- Creatio.ai engine
- Context
- Creatio.ai Skills
- System skill
- Custom actions
- Microservice
- LLM
- See also

# Data privacy in Creatio.ai | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 617 **URL:**
https://academy.creatio.com/docs/8.x/no-code-customization/customization-tools/ai-tools/creatio-ai/data-privacy

## Description

Creatio provides a solid compliance backbone by meeting the major privacy
standards: SOC 1, SOC 2, and ISO 27001. You can also make Creatio compliant with
GDPR and HIPAA. Every Creatio cloud instance runs on an audited,
privacy-approved security foundation. This ensures protection by encryption,
access controls, and regional hosting.

## Key Concepts

business process, role

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

Creatio provides a solid compliance backbone by meeting the major privacy
standards: SOC 1, SOC 2, and ISO 27001. You can also make Creatio compliant with
GDPR and HIPAA. Every Creatio cloud instance runs on an audited,
privacy-approved security foundation. This ensures protection by encryption,
access controls, and regional hosting.

Creatio does not have its own LLM (large language model), does not use public AI
services, and does not train the LLM used in Creatio.ai on Customer Data. We
work with a separately deployed LLM instance. LLM as software is hosted and
operated on Microsoft Azure services in the USA (for the US customers) or Sweden
(for EU and other regions) depending on your Creatio website location.

Only approved LLMs can be used with Creatio.ai out of the box. Creatio handles
the core integrity and reliability of the LLM, maintaining a trusted registry of
approved LLMs. Only signed, vetted LLMs get used. We perform extensive testing
before deployment, including redteaming to find weaknesses and checking for
bias. We also have automatic fallback models ready if something goes wrong,
ensuring that the foundation is solid. However, if you need to use your own LLM
with Creatio.ai, we also provide this option.

The LLM accesses Customer Data limited to the query processing purposes, without
any LLM provider's access to it. Customer Data is not stored on external
services and is never shared across tenants. Data is encrypted using TLS 1.2+ in
transit and AES-256 at rest.

When working with files in Creatio.ai, for example, uploading documents for
summarization or analysis, all uploaded content is stored in customer-dedicated
storage, ensuring that data remains isolated and secure within the tenant's
environment. File processing, including extraction, is performed entirely within
the Creatio platform infrastructure, with no external systems involved in
handling the file content. Furthermore, when the content of a file is used, it
is treated with the same strict data privacy policies as any other user-entered
input interactions in Creatio.ai.

Creatio.ai follows the least-privileged RBAC (role-based access control)
cybersecurity principle. Fine‑grained roles restrict both data and model access.

Creatio.ai assists with compliance regarding user access permissions and
restrictions.​

Read more about the LLM used in Creatio.ai here:
[Data, privacy, and security for Azure OpenAI Service](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy?tabs=azure-portal).

Creatio.ai uses Customer Data for communicating with the LLM. This enables it to
get clear and useful answers when you ask Creatio.ai something. We call that
data context.

Context is the information provided to the LLM. It helps the LLM to understand
what is expected of it and ensures the accuracy and relevance of its responses.

Creatio uses the following types of data as context:

1. **Page data**. Creatio.ai can request and utilize data from the page where
   you are currently working.

2. **Message history**. This is your chat history with Creatio.ai. It helps the
   LLM to understand the context of previous conversations, enabling it to
   better interpret your requests and stay within the scope of a single query as
   long as you need it.

3. **Additional context from AI Skills and business processes**. If your AI
   Skill, a sequence of actions designed for achieving a specific goal, has
   actions configured that use Customer Data as output parameters, Creatio.ai
   can use this data to generate responses, trigger functions, etc.

Creatio.ai does not have access to previous chat history if you have clear it or
start a new conversation.

We strongly recommend using Creatio.ai only for the issues related to your usage
of Creatio services for the internal business purposes, as described in your
agreement with Creatio.

---

## See also​

[Creatio.ai overview](https://academy.creatio.com/documents?id=2528)

[Creatio.ai architecture](https://academy.creatio.com/documents?id=2548)

[Develop Creatio.ai Skill](https://academy.creatio.com/documents?id=2535)

[AI Skill development recommendations](https://academy.creatio.com/documents?id=2536)

[AI Skill list](https://academy.creatio.com/documents?id=2549)

[Creatio.ai system actions](https://academy.creatio.com/documents?id=2550)

- See also

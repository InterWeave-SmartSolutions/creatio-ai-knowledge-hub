# Chat API | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 330
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/classic-ui/chat-management-api/references/chat-api

## Description

The functionality is relevant to Classic UI.

## Key Concepts

classic ui, integration

## Use Cases

third-party integration, data synchronization, system connectivity

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

note

The functionality is relevant to Classic UI.

## MessageManager class​

Enables the messenger integration with Creatio instance.

### Methods​

    Receive()

Receives incoming messages in the unified format (`UnifiedMessage`, a unified
message class) or as a string, which is then converted into the unified format.
If the conversion is required, the method uses a class that implements the
`IIncomeMessageWorker` interface. Implementation of the interface depends on the
messenger. The method also receives messages in Creatio.

    Send()

Sends outgoing messages. Creatio selects the relevant message sender class. The
class must implement the `IOutcomeMessageWorker` interface. The method also
sends messages in Creatio.

    Register()

Adds a channel when setting up Facebook Messenger integration. The method uses
the class that implements the `IMessengerRegistrationWorker` interface. Required
for messengers that need additional actions upon registration. For example,
retrieve a token.

    GetMessagesByChatId()

Receives messages of a specific chat in the `IEnumerable<UnifiedMessage>`
format. Pass the chat in method parameters.

## OmnichannelMessagingService class​

Receives and sends messages. Parent class for the following classes:

- `FacebookOmnichannelMessagingService`. Receives and sends messages from
  Facebook Messenger.
- `TelegramOmnichannelMessagingService`. Receives and sends messages from
  Telegram.

### Methods​

    InternalReceive()

Receives messages.

## OmnichannelChatService class​

Receives history, chats of a specific agent, etc.

### Methods​

    AcceptChat()

Assigns the chat to the current user.

    GetUnreadChatsCount()

Receives the number of unread chats.

    MarkChatAsRead()

Marks all messages in the chat as read.

    GetConversation()

Receives chat messages to display them in the communication panel.

    CloseActiveChat()

Closes the chat.

    GetChats()

Receives all chats of the agent.

    GetChatActions()

Receives the list of actions available for the chat’s queue.

    GetUnreadMessagesCount()

Receives the number of unread messages in all chats of the agent.

- MessageManager class
  - Methods
- OmnichannelMessagingService class
  - Methods
- OmnichannelChatService class
  - Methods

# Execute operations in the background | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 299 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/data-operations-back-end/execute-operations-in-the-background/overview

## Description

Execute operations in the background to run time-consuming operations without
holding up the UI.

## Key Concepts

operation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

**Execute operations in the background** to run time-consuming operations
without holding up the UI.

The `Terrasoft.Core.Tasks.Task` class implements the `StartNew()` and
`StartNewWithUserConnection()` methods that start background operations. You can
use base .NET data types (e. g., `string`, `int`, `Guid`, etc) or custom types
as parameters. Unlike `StartNew()`, the `StartNewWithUserConnection()` method
runs background operations that require the `UserConnection` user connection.

The `MessagePack-CSharp` module converts parameters accepted by the background
operation to a byte array. View the implementation on the `MessagePack-CSharp`
module on [GitHub](https://github.com/neuecc/MessagePack-CSharp). If the module
cannot serialize or deserialize a parameter value, the module will throw an
exception.

Important

We recommend against using infinite loops in background operations as they block
other Creatio tasks.

Describe the execution of an asynchronous operation in an individual class that
must implement the `IBackgroundTask<in TParameters>` interface.

IBackgroundTask<in TParameters> interface

    namespace Terrasoft.Core.Tasks {
        public interface IBackgroundTask <in TParameters> {
            void Run(TParameters parameters);
        }
    }

If the action requires a user connection, implement the
`IUserConnectionRequired` interface in the class as well.

IUserConnectionRequired interface

    namespace Terrasoft.Core {
        public interface IUserConnectionRequired {
            void SetUserConnection(UserConnection userConnection);
        }
    }

Implement the methods of the `Run` and `SetUserConnection` interfaces in the
class that implements the `IBackgroundTask<in TParameters>` and
`IUserConnectionRequired` interfaces.

Good to know when **implementing the methods** :

- Do not pass `UserConnection` to the `Run` method.
- Do not call the `SetUserConnection` method from the `Run` method. The
  application core calls this method and initializes a `UserConnection` instance
  when the background operation starts.
- Pass structures that comprise only simple data types to the `Run` method.
  Complex class instances are highly likely to cause parameter serialization
  errors.

---

## Resources​

[MessagePack-CSharp module implementation](https://github.com/neuecc/MessagePack-CSharp)
(GitHub)

- Resources

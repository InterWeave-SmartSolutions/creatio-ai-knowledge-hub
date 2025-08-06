# Replacing class factory | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 952 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/back-end-development/replacing-class-factory/overview

## Description

Instantiate the replacing class using the replacing class object factory.
Creatio requests the replaced type instance from the factory. The factory
returns the instance of the corresponding replacing type, which the factory
computes using the dependency tree in source code schemas.

## Key Concepts

workflow, configuration, operation, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/replacing-class-factory/overview)**
(8.3).

Version: 8.1

On this page

Level: advanced

Instantiate the replacing class using the **replacing class object factory**.
Creatio requests the replaced type instance from the factory. The factory
returns the instance of the corresponding replacing type, which the factory
computes using the dependency tree in source code schemas.

To **create a replacing configuration element** of the appropriate type, follow
the procedure covered in a separate guide:
[Configuration elements](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/configuration-elements).

## [Override] attribute​

The `[Override]` attribute type belongs to the `Terrasoft.Core.Factories`
namespace and directly inherits the `System.Attribute` base type. Learn more
about the `Terrasoft.Core.Factories` namespace in the
[.NET class library](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories_namespace.html).
Learn more about the `System.Attribute` base type in the official
[Microsoft documentation](https://docs.microsoft.com/en-us/dotnet/api/system.attribute?redirectedfrom=MSDN&view=netcore-3.1).

The `[Override]` attribute only applies to classes. The **purpose** of the
`[Override]` attribute is to define classes to take into account when building a
dependency tree of replacing and replaced factory types.

View how to apply the `[Override]` attribute to the `MySubstituteClass`
replacing class below. `SubstitutableClass` is the replaced class.

- Template to apply the [Override] attribute
- Example that applies the [Override] attribute

  [Override]  
  public class ReplacingClassName : ReplacedClassName  
  {  
   /_ Implement the class. _/  
  }

  [Override]  
  public class MySubstituteClass : SubstitutableClass  
  {  
   /_ Implement the class. _/  
  }

## ClassFactory class​

The **purpose** of the `ClassFactory` class is to implement the factory of
replacing Creatio objects. The factory uses the
[Ninject](http://www.ninject.org/) open-source framework to inject dependencies.
Learn more about the `ClassFactory` static class in the
[.NET class library](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories.ClassFactory.html).

Creatio **initializes the factory** during the first call to it, i. e. at the
first attempt to retrieve the replacing type instance. The factory collects data
about the replaced configuration types as part of the initialization.

The **operating procedure of the factory** :

1. Search for replacing types. The factory analyzes the configuration build
   types. The factory interprets the class marked with the `[Override]`
   attribute as a replacing class and its parent class as a replaced class.
2. Build the type dependency tree as a list of `Replaced type → Replacing type`
   value pairs. The replacement hierarchy tree does not take transitional types
   into account.
3. Replace the source class with the last inheritor in the replacement
   hierarchy.
4. Bind replacement types based on the type dependency tree. The factory uses
   the Ninject framework.

View the factory workflow based on the class hierarchy example below.

Class hierarchy example

    /* Source class. */
    public class ClassA { }

    /* Class that replaces ClassA. */
    [Override]
    public class ClassB : ClassA { }

    /* Class that replaces ClassB. */
    [Override]
    public class ClassC : ClassB { }

The factory will use the class hierarchy to build a dependency tree you can view
below.

Dependency tree example

    ClassA → ClassC
    ClassB → ClassC

The factory will not take the transitional types into account when building the
dependency tree.

Type replacement hierarchy example

    ClassA → ClassB → ClassC

Here, the `ClassC` type, and not the transitional `ClassB` type, replaces
`ClassA`. This is because `ClassC` is the last inheritor in the replacement
hierarchy. As such, the factory will return the `ClassC` instance if you request
the `ClassA` or `ClassB` type instance.

## Replaced type instance​

To **retrieve a replaced type instance** , use the `Get<T>` public static
parameterized method. The `ClassFactory` factory provides this method. The
replaced type serves as a generic method parameter. Learn more about the
`Get<T>` method in the
[.NET class library](<https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories.ClassFactory~Get%60%601(ConstructorArgument%5B%5D).html>).

Example that retrieves the replaced type instance

    var substituteObject = ClassFactory.Get<SubstitutableClass>();

As a result, Creatio will create the `MySubstituteClass` class instance. You do
not have to state the type of the new instance explicitly. The preliminary
initialization lets the factory determine the type to replace the requested type
and create the corresponding instance.

The `Get<T>` method can accept an array of `ConstructorArgument` objects as
parameters. Each of the objects in the array is a class constructor argument the
factory created. As such, the factory lets you instantiate replacing objects
with parameterized constructors. The factory core resolves the dependencies
required for the creation or operation of the object independently.

We recommend ensuring the signature of the replaced class constructors matches
the signature of the replacing class. If the replacing class implementation
logic must declare the constructor that has a custom signature, make sure to
follow the rules listed below.

**Rules for creating and calling replaced and replacing class constructors** :

- If the replaced class **lacks an explicitly parameterized constructor** (the
  class only has a default constructor), you can implement an explicitly
  parameterized independent constructor in the replacing class without any
  restrictions. Follow the standard order of calls to the parent (replaced) and
  child (replacing) class constructors. When instantiating the replaced class
  via the factory, make sure to pass the correct parameters to initialize the
  replacing class properties to the factory.
- If the replaced class **has a parameterized constructor** , implement the
  constructor in the replacing class. The replacing class constructor must call
  the parameterized constructor of the parent (replaced) class explicitly and
  pass the parameters for the correct initialization of the parent properties to
  the parent class. Other than that, the replacing class constructor may
  initialize its properties or remain empty.

Failure to comply with the rules will result in a runtime error. The developer
is responsible for the correct initialization of replacing and replaced class
properties.

---

## See also​

[Configuration elements](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/configuration-elements)

---

## Resources​

[Terrasoft.Core.Factories namespace](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories_namespace.html)
(.NET classes reference)

[System.Attribute base type](https://docs.microsoft.com/en-us/dotnet/api/system.attribute?redirectedfrom=MSDN&view=netcore-3.1)
(official Microsoft documentation)

[Official Ninject site](http://www.ninject.org/)

[ClassFactory static class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories.ClassFactory.html)
(.NET classes reference)

[Get<T> method](<https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Factories.ClassFactory~Get%60%601(ConstructorArgument%5B%5D).html>)
(.NET classes reference)

- [Override] attribute
- ClassFactory class
- Replaced type instance
- See also
- Resources

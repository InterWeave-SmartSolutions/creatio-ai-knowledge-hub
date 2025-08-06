# Replacing class management examples | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 1176 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/back-end-development/replacing-class-factory/examples/replacing-class-management-examples

## Description

Example 1

## Key Concepts

## Use Cases

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/replacing-class-factory/examples/replacing-class-management-examples)**
(8.3).

Version: 8.2

On this page

Level: advanced

## Example 1​

The `SubstitutableClass` replaced class has one default constructor.

SubstitutableClass replaced class

    /* Declare a replaced class. */
    public class SubstitutableClass
    {
    /* The class property to initialize in the constructor. */
    public int OriginalValue { get; private set; }

        /* The default constructor that initializes the OriginalValue property with 10. */
        public SubstitutableClass()
        {
            OriginalValue = 10;
        }

        /* The method that returns the OriginalValue multiplied by 2. You can redefine this method in replacing classes. */
        public virtual int GetMultipliedValue()
        {
            return OriginalValue * 2;
        }

    }


Declare two constructors in the `SubstituteClass` replacing class: the default
constructor and the parameterized constructor. Redefine the
`GetMultipliedValue()` parent method using the replacing class.

SubstituteClass replacing class

    /* Declare a class to replace the SubstitutableClass. */
    [Terrasoft.Core.Factories.Override]
    public class SubstituteClass : SubstitutableClass
    {
        /* The SubstituteClass class property. */
        public int AdditionalValue { get; private set; }

        /* The default constructor that initializes the AdditionalValue property with 15. You do not have to call the constructor of the SubstitutableClass parent class here since the parent class declares only the default constructor. Creatio will call the default constructor implicitly when creating the SubstituteClass instance. */
        public SubstituteClass()
        {
            AdditionalValue = 15;
        }

        /* The parameterized constructor that initializes the AdditionalValue property to the value passed as a parameter. Likewise, you do not have to call the parent constructor explicitly here. */
        public SubstituteClass(int paramValue)
        {
            AdditionalValue = paramValue;
        }

        /* Replace the parent method. The method returns the AdditionalValue multiplied by 3. */
        public override int GetMultipliedValue()
        {
            return AdditionalValue * 3;
        }
    }

Example

Instantiate and call the `GetMultipliedValue()` method of the `SubstituteClass`
replacing class using the default constructor and the parameterized constructor.

See the examples of retrieving the `SubstituteClass` replacing class instance
using the factory below.

Examples of retrieving the replacing class using the factory

    /* Retrieve an instance of the class to replace the SubstitutableClass. The factory returns a SubstitutableClass instance initialized by the constructor without parameters. */
    var substituteObject = ClassFactory.Get<SubstitutableClass>();

    /* The variable equals 10. The default parent constructor initializes the OriginalValue property. Creatio called the constructor implicitly when creating a replacing class instance. */
    var originalValue = substituteObject.OriginalValue;

    /* Call the replacing class method that returns the AdditionalValue multiplied by 3. The variable equals 45 since the AdditionalValue was initialized with 15. */
    var additionalValue = substituteObject.GetMultipliedValue();

    /* Retrieve the replacing class instance initialized by the parameterized constructor. The ConstructorArgument parameter name must match the class constructor parameter name. */
    var substituteObjectWithParameters = ClassFactory.Get<SubstitutableClass>(
        new ConstructorArgument("paramValue", 20));

    /* The variable equals 10. */
    var originalValueParametrized = substituteObjectWithParameters.OriginalValue;

    /* The variable equals 60 since the AdditionalValue was initialized with 20. */
    var additionalValueParametrized = substituteObjectWithParameters.GetMultipliedValue();

## Example 2​

The `SubstitutableClass` replaced class has 1 parameterized constructor.

SubstitutableClass replaced class

    /* Declare a replaced class. */
    public class SubstitutableClass {
        /* The class property to initialize in the constructor. */
        public int OriginalValue {
            get;
            private set;
        }

        /* The parameterized constructor that initializes the OriginalValue property to the value passed as a parameter. */
        public SubstitutableClass(int originalParamValue) {
            OriginalValue = originalParamValue;
        }

        /* The method that returns the OriginalValue multiplied by 2. You can redefine the method in replacing classes. */
        public virtual int GetMultipliedValue() {
            return OriginalValue * 2;
        }

    }


The `SubstituteClass` replacing class has 1 parameterized constructor as well.

SubstituteClass replacing class

    /* Declare the class to replace the SubstitutableClass. */
    [Terrasoft.Core.Factories.Override]
    public class SubstituteClass: SubstitutableClass {
        /* The SubstituteClass class property. */
        public int AdditionalValue {
            get;
            private set;
        }

        /* The parameterized constructor that initializes the AdditionalValue property to the value passed as a parameter. Call the parent constructor explicitly to initialize the parent property. If you do not do that, the compilation will end with an error. */
        public SubstituteClass(int paramValue): base(paramValue + 8) {
            AdditionalValue = paramValue;
        }

        /* Replace the parent method. The method returns AdditionalValue multiplied by 3. */
        public override int GetMultipliedValue() {
            return AdditionalValue * 3;
        }
    }

Example

Create and use an instance of the `SubstituteClass` replacing class.

See the example of creating and using an instance of the `SubstituteClass`
replacing class using the factory below.

Example of creating and using a replacing class instance using the factory

    /* Retrieve an instance of the replacing class initialized in the parameterized constructor. The ConstructorArgument parameter name must match the class constructor parameter name. */
    var substituteObjectWithParameters = ClassFactory.Get<SubstitutableClass>(
        new ConstructorArgument("paramValue", 10));

    /* The variable equals 18. */
    var originalValueParametrized = substituteObjectWithParameters.OriginalValue;

    /* The variable equals 30. */
    var additionalValueParametrized = substituteObjectWithParameters.GetMultipliedValue();

## Example 3​

The `SubstitutableClass` replaced class has 1 parameterized constructor.

SubstitutableClass replaced class

    /* Declare a replaced class. */
    public class SubstitutableClass {
        /* The class property to initialize in the constructor. */
        public int OriginalValue {
            get;
            private set;
        }

        /* The parameterized constructor that initializes the OriginalValue property to the value passed as a parameter. */
        public SubstitutableClass(int originalParamValue) {
            OriginalValue = originalParamValue;
        }

        /* The method that returns the OriginalValue multiplied by 2. You can redefine this method in replacing classes. */
        public virtual int GetMultipliedValue() {
            return OriginalValue * 2;
        }

    }


Example

Redefine the `GetMultipliedValue()` parent method in the `SubstituteClass`
replacing class.

The `SubstituteClass` replacing class redefines the `GetMultipliedValue()`
method that will return a fixed value. You do not have to initialize the
`SubstituteClass` class properties. However, the class requires an explicit
declaration of the constructor that calls the parameterized parent constructor
to initialize the parent properties correctly.

SubstituteClass replacing class

    // Declare a class to replace SubstitutableClass.
    [Terrasoft.Core.Factories.Override]
    public class SubstituteClass: SubstitutableClass {
        /* Empty default constructor that explicitly calls the parent class constructor to initialize the parent properties correctly. */
        public SubstituteClass(): base(0) {}

        /* You can also use an empty parameterized constructor to pass the parameters to the parent class constructor. */
        public SubstituteClass(int someValue): base(someValue) {}

        /* Replace the parent method. The method will return a fixed value. */
        public override int GetMultipliedValue() {
            return 111;
        }
    }

- Example 1
- Example 2
- Example 3

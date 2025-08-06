# Copy hierarchical data | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1545
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/data-operations-back-end/copy-hierarchical-data

## Description

Copy hierarchical data to copy both the database table records and the records
of the connected tables. You can copy the hierarchical data of
[ProductHierarchyDataStructureObtainer] and
[ProductConditionHierarchyDataStructureObtainer] Creatio tables out-of-the-box.
To copy the data of other tables, customize hierarchical data copying.

## Key Concepts

configuration, section, detail, web service, database, operation, package,
contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

**Copy hierarchical data** to copy both the database table records and the
records of the connected tables. You can copy the hierarchical data of
`[ProductHierarchyDataStructureObtainer]` and
`[ProductConditionHierarchyDataStructureObtainer]` Creatio tables
out-of-the-box. To copy the data of other tables, customize hierarchical data
copying.

You can use hierarchical copying in a
[custom web service](https://academy.creatio.com/documents?ver=8.3&id=15262).
For example, if you copy data from an external service to Creatio or connect to
an external database.

For example, the **Products** section is based on the `[Product]` database
table. The product page contains custom details. If you copy the section records
hierarchically, Creatio will copy the data of both the record and the connected
details.

Creatio applies the table's
[access permissions](https://academy.creatio.com/documents?ver=8.3&id=262) when
copying. For example, the user lacks access permissions to read and add records
to the `[Contact]` table. If they try to copy hierarchical data, Creatio will
not copy the record and notify them that it is impossible to execute the
operation.

## Structure and operational procedure of hierarchical data copying​

View the **components** of hierarchical data copying in the table below.

| Name | Description | Classes and interfaces | Controller | Controls the copying process | `IHierarchyDataCopyingController` `HierarchyDataCopyingController` controls the copying of the database record and the connected database data. | Obtainer | Obtains the structure of the current table and connected tables from the database | `HierarchyDataStructureObtainerContext` selects the algorithm to obtain the hierarchical structure of the table and connected tables. `IHierarchyDataStructureObtainer` `HierarchyDataStructureObtainer` obtains the hierarchical structure of the table and connected tables `BaseHierarchyDataStructureObtainer` `ProductHierarchyDataStructureObtainer` obtains the hierarchical structure of the `[Product]` table and connected tables. | Container | Saves the structure of the current table and connected tables | `HierarchyDataStructure` saves the information about the hierarchical data structure. | Mapper | Manages the structure | `IEntityCollectionMappingProcessor` `EntityCollectionMappingProcessor` obtains the structure from the database and copies data. |
| ---- | ----------- | ---------------------- | ---------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------ | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |

View the **class chart** of the hierarchical data copying on the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HierarchyData/scr_class_diagram.png)

The **operating procedure** of hierarchical data copying.

1. The service class calls the copying process controller and passes the table
   name and ID of the original record to the controller.

2. The controller makes a copy in several stages:
   1. Retrieve the structure of the table and connected tables as a unified
      form.
   2. Save the table structure as a unified form.

3. The controller copies records according to the structure obtained on the
   saving stage.

Saving as **unified form** saves the table structure to the object of the
`HierarchyDataStructure` type. If the table has connected tables (a column links
to the record of a different table via an external key), the controller will
place them to the object (to the object collection of a similar type). Should
you need to expand or update the structure obtainer mechanism, the unified form
will let you process the new structure without additional modifications to the
controller code.

See the template of the unified form the controller uses to save the table
structure below.

Template of the unified table structure form

    /* The class contains the hierarchical data structure. */
    public class HierarchyDataStructure {
        public string SchemaName;
        public List <string> Columns;

        /* If the current structure object does not have a parent foreign table name, use null here. */
        public string ParentColumnName;

        /* The child structure list. */
        public List <HierarchyDataStructure> Structures;

        /* The filter list. */
        public HierarchyDataStructureFilterGroup Filters;
    }

## Customize the hierarchical data copying​

You can customize hierarchical data copying in multiple ways:

- Add a custom data obtainer implementation (the
  `HierarchyDataStructureObtainer` class).
- Modify the data obtainer implementation (the `HierarchyDataStructureObtainer`
  class).
- Modify the controller implementation (the `HierarchyDataCopyingController`
  class).
- Add a custom hierarchical data copying implementation.

### Add a custom data obtainer implementation​

The **ways** to add a custom data obtainer implementation (the
`HierarchyDataStructureObtainer` class) are as follows:

- Use the base interface.
- Inherit the base class.

#### Use the base interface to add a custom data obtainer implementation​

1. Create a class that implements the `IHierarchyDataStructureObtainer`
   interface. Name the class according to the following template:
   `[NameOfTheObjectToCopy]HierarchyDataStructureObtainer`.
2. Add a custom implementation of the `ObtainStructure()` interface method. Make
   sure to specify the `virtual` modifier.

See the example of the data obtainer implementation that uses the base interface
in the **ProductBankCustomerJourney** package → the
`ProductHierarchyDataStructureObtainer` and
`ProductConditionHierarchyDataStructureObtainer` classes.

#### Inherit the base class to add a custom data obtainer implementation​

In this case, base implementation is the standard record copying process that
does not affect the connected records. The `BaseHierarchyDataStructureObtainer`
class of the base **NUI** package implements the obtainer.

1. Create a class that implements the `BaseHierarchyDataStructureObtainer`
   interface (the **NUI** package → the `BaseHierarchyDataStructureObtainer`
   class). Name the class according to the following template:
   `[NameOfTheObjectToCopy]HierarchyDataStructureObtainer`.
2. Extend the base obtainer implementation

See the example of the data obtainer implementation that inherits the base class
in the **ProductBankCustomerJourney** package → the
`ProductHierarchyDataStructureObtainer` class.

### Modify the data obtainer implementation​

1. Create a class that
   [replaces](https://academy.creatio.com/documents?ver=8.3&id=15221) one of the
   following classes: `BaseHierarchyDataStructureObtainer` (the **NUI**
   package), `ProductConditionHierarchyDataStructureObtainer` (the
   **ProductBankCustomerJourney** package),
   `ProductHierarchyDataStructureObtainer` (the **ProductBankCustomerJourney**
   package).
2. Add a custom implementation of the base class's `ObtainStructure()` replacing
   method to the replacing class.

### Modify the controller implementation​

1. Create a class that implements the `IHierarchyDataCopyingController`
   interface. Name the class according to the following template:
   `[ObjectName]HierarchyDataController`.

2. Add a custom copying algorithm to the `CopyRecord` interface method.

Call a single method of another class as part of a single algorithm step. Also,
create a class object to call or minimally prepare data to pass to the method as
part of the step.

### Add a custom hierarchical data copying implementation​

1. Add an implementation of the copying process controller
   (`HierarchyDataCopyingController` class). The controller must call the
   structure obtainer (`HierarchyDataStructureObtainer` class), the structure
   processor (`EntityCollectionMappingProcessor` class), the structure container
   (the `HierarchyDataStructure` class) gradually.

2. Add an implementation of the hierarchical data structure obtainer
   (`HierarchyDataStructureObtainer` class).

3. Create a class that implements the interface. Name the class according to the
   following template: `[ObjectName]HierarchyDataProcessor`.

We recommend adding the processor class interface. This will let you add another
implementation and replace the existing implementation, as well as unify the
processors.

4. Create a class that implements the `IEntityCollectionMappingHandler`
   interface.

5. Add the calls to the structure obtainer (the `HierarchyDataStructureObtainer`
   class), structure processor (the `EntityCollectionMappingProcessor` class),
   structure container (the `HierarchyDataStructure` class) methods to the
   `CopyRecord` controller method.

6. Create the `HierarchyDataCopyingController` class object in the custom class.

Example that creates the controller object

         var copyController = ClassFactory.Get<HierarchyDataCopyingController>(new ConstructorArgument("UserConnection", UserConnection));


7. Call the `copyController` copying method.

Example that calls the copying method

         copyController.CopyRecord(schemaName, recordId);


## Call hierarchical data copying​

You can call hierarchical data copying from the front-end and back-end.

### Call hierarchical copying from the front-end​

Use the `callService()` method to **call hierarchical copying from front-end**.

See the call example in the **ProductBankCustomerJourney** package → the
`ProductConditionDetailV2` schema → the `callCopyRecordService()` method.

Example that calls hierarchical copying from front-end

    /**
    * Call the record copying service.
    * @protected
    */
    callCopyRecordService: function() {
        this.showBodyMask();
        var config = this.getCopyRecordConfig();
        this.callService(config, this.copyRecordServiceCallback, this);
    }

### Call hierarchical copying from the back-end​

Create the `HierarchyDataCopyingController` class object in a custom class to
**call hierarchical copying from back-end**.

Example that calls hierarchical copying from back-end

    var copyController = ClassFactory.Get<HierarchyDataCopyingController>(new ConstructorArgument("UserConnection", UserConnection));

To **manage table data using the column mapping** :

1. Create a mapper class object that implements the
   `IEntityCollectionMappingHandler` interface in a custom class.

Example that creates a mapper class object

         var entityCollectionMappingHandler = ClassFactory.Get<IEntityCollectionMappingHandler>(new ConstructorArgument("userConnection", UserConnection));


2. Call the mapper methods via the object.

Example that calls the copying method

         entityCollectionMappingHandler.CopyItems(
             data.SchemaName,
             columns,
             filterGroup,
             relatedColumnValues
         );


note

If you create an object using the interface name, the developer will be able to
replace the existing mapper implementation using a custom implementation. If you
modify the implementation of an existing mapper, Creatio will recompile only the
mapper class. The classes that use the implementation do not need to be
recompiled. Learn more about creating objects using the dependency
implementation mechanism:
[Replace the configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15221).

To **obtain the structure of a particular table** as an object of the
`HierarchyDataStructure` type:

1. Create a `HierarchyDataStructureObtainerContext` class object in the custom
   class.

Example that creates the table structure obtainer

         var _hierarchyDataStructureObtainer = ClassFactory.Get<HierarchyDataStructureObtainerContext>(new ConstructorArgument("userConnection", UserConnection));


2. Obtain the structure of a particular table.

The **ways** to obtain the structure are as follows:

     * Call the `ObtainStructureByObtainerStrategy` method and pass the `schemaName` parameter that contains the table name whose record to copy to the method.
     * Call the implementation of the existing structure obtainer: `ProductHierarchyDataStructureObtainer` or `ProductConditionHierarchyDataStructureObtainer`.

---

## See also​

[Custom web services](https://academy.creatio.com/documents?ver=8.3&id=15262)

[Object operation permissions](https://academy.creatio.com/documents?ver=8.3&id=262)
(user documentation)

[Replacing class factory](https://academy.creatio.com/documents?ver=8.3&id=15221)

- Structure and operational procedure of hierarchical data copying
- Customize the hierarchical data copying
  - Add a custom data obtainer implementation
  - Modify the data obtainer implementation
  - Modify the controller implementation
  - Add a custom hierarchical data copying implementation
- Call hierarchical data copying
  - Call hierarchical copying from the front-end
  - Call hierarchical copying from the back-end
- See also

# Auto-apply business rules to records that are added by a custom request handler | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 454
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/platform-customization/freedom-ui/business-rules-of-collection-records

## Description

Creatio lets you execute business rules whenever custom request handler adds a
record to a collection. For example, use the functionality if you need to
populate a collection of records, apply business rules for each record and
output the result in a section list.

## Key Concepts

page schema, freedom ui, section

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/business-rules-of-collection-records)**
(8.3).

Version: 8.2

On this page

Level: beginner

Creatio lets you execute business rules whenever custom request handler adds a
record to a collection. For example, use the functionality if you need to
populate a collection of records, apply business rules for each record and
output the result in a section list.

To auto-apply business rules to collection records that a custom request handler
adds:

1. **Go to the** `handlers` **schema section**.
2. **Implement a custom request handler** if needed.
3. **Add a** `createItem()` **method** that creates a new record, for example,
   when you click the **Add** button.
4. **Set the** `businessRulesActive` **property to** `true`. The property
   auto-applies business rules to a new collection record.

View the example that implements a custom `usr.AddRecordRequest` request handler
of the Freedom UI page schema below. The handler is bound to the `clicked`
button event and adds the "John Smith" record to the section list. If the
`businessRulesActive` property is set to `true`, Creatio automatically applies
business rules to a new collection record. Otherwise, Creatio does not apply
business rules to a new collection record until the record is selected in the
section list.

- Auto-applying of business rules is disabled out of the box
- Auto-applying of business rules is enabled

  handlers: /**SCHEMA_HANDLERS*/[{  
   /* The custom implementation of the custom request handler. _/  
   request: "usr.AddRecordRequest",  
   handler: async (request, next) => {  
   /_ The section list collection that the Freedom UI section page displays.
  _/  
   const collection = await request.$context.Items;  
   /_ Add a new record of the section list collection. _/  
   await collection.createItem({  
   /_ Set the "Name" field to "John Smith." \*/  
   initialModelValues: { Name: 'John Smith'}  
   });  
   return next?.handle(request);  
   }  
  }]/**SCHEMA_HANDLERS\*/,

  handlers: /**SCHEMA_HANDLERS*/[{  
   /* The custom implementation of the custom request handler. _/  
   request: "usr.AddRecordRequest",  
   handler: async (request, next) => {  
   /_ The section list collection that the Freedom UI section page displays.
  _/  
   const collection = await request.$context.Items;  
   /_ Add a new record of the section list collection. _/  
   await collection.createItem({  
   /_ Set the "Name" field to "John Smith." _/  
   initialModelValues: { Name: 'John Smith'},  
   /_ Auto-apply business rules to collection records that a custom request
  handler adds. \*/  
   businessRulesActive: true  
   });  
   return next?.handle(request);  
   }  
  }]/**SCHEMA_HANDLERS\*/,

---

## See also​

[Set up List components](https://academy.creatio.com/documents?ver=8.2&id=2457)
(user documentation)

- See also

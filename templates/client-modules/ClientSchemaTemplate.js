/**
 * @fileoverview [Schema Name] - [Brief Description]
 * @author [Author Name]
 * @version [Version]
 */

define("SchemaName", ["ext-base", "terrasoft"], function(Ext, Terrasoft) {
  return {
    // Schema configuration
    entitySchemaName: "EntityName",
    
    /**
     * Schema attributes
     */
    attributes: {
      // Add your attributes here
      "SampleAttribute": {
        dataValueType: Terrasoft.DataValueType.TEXT,
        type: Terrasoft.ViewModelColumnType.VIRTUAL_COLUMN
      }
    },
    
    /**
     * Schema modules
     */
    modules: /**SCHEMA_MODULES*/{
      // Add your modules here
    }/**SCHEMA_MODULES*/,
    
    /**
     * Schema details
     */
    details: /**SCHEMA_DETAILS*/{
      // Add your details here
    }/**SCHEMA_DETAILS*/,
    
    /**
     * Business rules
     */
    businessRules: /**SCHEMA_BUSINESS_RULES*/{
      // Add your business rules here
    }/**SCHEMA_BUSINESS_RULES*/,
    
    /**
     * Schema methods
     */
    methods: {
      
      /**
       * Initialize schema
       */
      init: function() {
        this.callParent(arguments);
        // Add initialization logic here
      },
      
      /**
       * On entity initialized event handler
       */
      onEntityInitialized: function() {
        this.callParent(arguments);
        // Add entity initialization logic here
      },
      
      /**
       * Save button click handler
       */
      onSaved: function() {
        this.callParent(arguments);
        // Add save logic here
      },
      
      /**
       * Custom method template
       * @param {Object} config Method configuration
       * @returns {*} Method result
       */
      customMethod: function(config) {
        // Add your custom logic here
        return this.callParent(arguments);
      }
    },
    
    /**
     * Schema diff array
     */
    diff: /**SCHEMA_DIFF*/[
      // Add your diff items here
      {
        "operation": "insert",
        "name": "SampleControl",
        "values": {
          "layout": {
            "colSpan": 12,
            "rowSpan": 1,
            "column": 0,
            "row": 0
          },
          "bindTo": "SampleAttribute",
          "enabled": true
        },
        "parentName": "Header",
        "propertyName": "items",
        "index": 0
      }
    ]/**SCHEMA_DIFF*/
  };
});

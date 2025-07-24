/**
 * Creatio TypeScript type definitions
 */

declare namespace Terrasoft {
  export enum DataValueType {
    TEXT = 1,
    INTEGER = 4,
    FLOAT = 5,
    MONEY = 6,
    DATE_TIME = 7,
    DATE = 8,
    TIME = 9,
    LOOKUP = 10,
    ENUM = 11,
    BOOLEAN = 12,
    BLOB = 13,
    IMAGE = 14,
    IMAGELOOKUP = 15,
    COLOR = 16,
    GUID = 17,
    BINARY = 18,
    FILE = 19,
    MAPPING = 20,
    LOCALIZABLE_STRING = 21,
    ENTITY = 22,
    ENTITY_COLLECTION = 23,
    ENTITY_COLUMN_MAPPING_COLLECTION = 24,
    HASH_TEXT = 25,
    SECURE_TEXT = 26,
    LONG_TEXT = 27,
    MEDIUM_TEXT = 28,
    MAX_SIZE_TEXT = 29,
    RICH_TEXT = 30,
    FLOAT1 = 31,
    FLOAT2 = 32,
    FLOAT3 = 33,
    FLOAT4 = 34,
    FLOAT8 = 35,
    METADATA_TEXT = 36
  }

  export enum ViewModelColumnType {
    ENTITY_COLUMN = 0,
    CALCULATED_COLUMN = 1,
    VIRTUAL_COLUMN = 2
  }

  export interface BaseViewModel {
    init(): void;
    callParent(args: any[]): any;
    onEntityInitialized(): void;
    onSaved(): void;
  }

  export interface SchemaColumn {
    dataValueType: DataValueType;
    type: ViewModelColumnType;
    value?: any;
  }

  export interface SchemaAttributes {
    [key: string]: SchemaColumn;
  }
}

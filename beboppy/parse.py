from lark import Lark, Tree

bebop_grammar_definition = '''
start: (enum | struct | message)*

// enum definitions
enum: ENUM_NAME WS CUSTOM_TYPE_NAME LBRACE enum_body RBRACE
enum_body: enum_line*
enum_line: WORD EQUAL INT SEMI
ENUM_NAME: "enum"

// struct definitions
struct: STRUCT_NAME WS CUSTOM_TYPE_NAME LBRACE struct_body RBRACE
STRUCT_NAME: "struct"
struct_body: struct_line*
struct_line: type WS WORD SEMI

// message definitions
message: MESSAGE_NAME WS CUSTOM_TYPE_NAME LBRACE message_body RBRACE
MESSAGE_NAME: "message"
message_body: message_line*
message_line: INT ARROW type WS WORD SEMI

// typing
type: BOOL    // A Boolean value, true or false.
    | BYTE    // An unsigned 8-bit integer. uint8 is an alias.
    | UINT16  // An unsigned 16-bit integer.
    | INT16   // A signed 16-bit integer.
    | UINT32  // An unsigned 32-bit integer.
    | INT32   // A signed 32-bit integer.
    | UINT64  // An unsigned 64-bit integer.
    | INT64   // A signed 64-bit integer.
    | FLOAT32 // A 32-bit IEEE single-precision floating point number.
    | FLOAT64 // A 64-bit IEEE double-precision floating point number.
    | STRING  // A length-prefixed UTF-8-encoded string.
    | GUID    // A GUID.
    | DATE    // A UTC date / timestamp.
    | list_type 
    | map_type  
    | CUSTOM_TYPE_NAME

// T[]: A length-prefixed array of T values. array[T] is an alias.
list_type: type "[]"
         | "array" "[" type "]"

// map[T1, T2]: A map, as a length-prefixed array of (T1, T2) association pairs.
map_type: "map" "[" type "," type "]"

CUSTOM_TYPE_NAME: /[A-Z][A-Za-z_]*/

// TYPE expansions
BOOL: "bool"       // A Boolean value, true or false.
BYTE: "byte"       // An unsigned 8-bit integer. uint8 is an alias.
UINT16: "uint16"   // An unsigned 16-bit integer.
INT16: "int16"     // A signed 16-bit integer.
UINT32: "uint32"   // An unsigned 32-bit integer.
INT32: "int32"     // A signed 32-bit integer.
UINT64: "uint64"   // An unsigned 64-bit integer.
INT64: "int64"     // A signed 64-bit integer.
FLOAT32: "float32" // A 32-bit IEEE single-precision floating point number.
FLOAT64: "float64" // A 64-bit IEEE double-precision floating point number.
STRING: "string"   // A length-prefixed UTF-8-encoded string.
GUID: "guid"       // A GUID.
DATE: "date"       // A UTC date / timestamp.

// Literals
SEMI:   ";"
EQUAL:  "="
LBRACE: "{"
RBRACE: "}"
INT:    /[0-9]+/
ARROW:  "->"

%import common.WORD // imports from terminal library
%import common.WS
%ignore WS          // Disregard spaces in text
'''


def get_parser() -> Lark:
    parser = Lark(bebop_grammar_definition)
    return parser


def parse(text: str) -> Tree:
    # TODO: memoize or somethin
    parser = get_parser()
    return parser.parse(text)

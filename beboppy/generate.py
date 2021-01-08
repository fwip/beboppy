from dataclasses import make_dataclass
from enum import Enum

from lark import Tree


class GenerationError(Exception):
    pass


class DuplicateFieldError(GenerationError):
    pass


def gen_enum(tree: Tree) -> type:
    assert tree.data == "enum"
    name_node = tree.children[2]
    class_name = name_node.value

    assert tree.children[0].type == "ENUM_NAME"
    assert name_node.type == "CUSTOM_TYPE_NAME"

    attrs = {}
    for rule in tree.find_data('enum_line'):
        attrs[rule.children[0].value] = rule.children[2].value

    cls = Enum(class_name, attrs, module=__name__)
    return cls


to_py = {
    "BOOL"   : bool,
    "BYTE"   : int,
    "UINT16" : int,
    "INT16"  : int,
    "UINT32" : int,
    "INT32"  : int,
    "UINT64" : int,
    "INT64"  : int,
    "FLOAT32": float,
    "FLOAT64": float,
    "STRING" : str,
    # "GUID"   : str,
    # "DATE"   : str,
}


def get_type(node: Tree) -> type:
    typ = node.children[0]
    if isinstance(typ, Tree):
        print(typ.data, node, typ)
        if typ.data == "list_type":
            outer_type = list
            return outer_type
            # TODO
            # inner_type = get_type(typ)
        if typ.data == "map_type":
            outer_type = dict
            return outer_type
            # TODO
        raise ValueError(f"Unknown composite type {typ.data}")

    typ_name = typ.type
    new_typ = to_py.get(typ_name)
    if new_typ is not None:
        return new_typ
    if typ_name == "GUID":
        pass
    elif typ_name == "DATE":
        pass
    elif typ_name == "list_type":
        pass
    elif typ_name == "map_type":
        pass
    elif typ_name == "CUSTOM_TYPE_NAME":
        pass
    else:
        raise Exception(f"type {typ_name} unsupported")
    return type("NYI")


def gen_struct(tree: Tree) -> type:
    assert tree.data == "struct"
    name_node = tree.children[2]
    class_name = name_node.value

    assert tree.children[0].type == "STRUCT_NAME"
    assert name_node.type == "CUSTOM_TYPE_NAME"

    fields = []
    for rule in tree.find_data('struct_line'):
        typ = get_type(rule.children[0])
        field_name = rule.children[2].value
        fields.append((field_name, typ,))

    if len(fields) != len(set(f[0] for f in fields)):
        raise DuplicateFieldError("Duplicate field in struct")

    cls = make_dataclass(class_name, fields)
    return cls


def gen_message(tree: Tree) -> type:
    # TODO: Handle the integer mapping
    assert tree.data == "message"
    name_node = tree.children[2]
    class_name = name_node.value

    assert tree.children[0].type == "MESSAGE_NAME"
    assert name_node.type == "CUSTOM_TYPE_NAME"

    fields = []
    for rule in tree.find_data('message_line'):
        typ = get_type(rule.children[2])
        field_name = rule.children[4].value
        fields.append((field_name, typ,))
    if len(fields) != len(set(f[0] for f in fields)):
        raise DuplicateFieldError("Duplicate field in message")
    
    cls = make_dataclass(class_name, fields)
    return cls

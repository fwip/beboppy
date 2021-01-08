from hypothesis import given, strategies
from hypothesis.extra.lark import from_lark
import lark

from beboppy import __version__
from beboppy import encode, decode, generate, parse

parser = parse.get_parser()

bop_strategy = from_lark(parser, start="start")
msg_strategy = from_lark(parser, start="message")
struct_strategy = from_lark(parser, start="struct")
enum_strategy = from_lark(parser, start="enum")


def test_version():
    assert __version__ == '0.1.0'


def assert_roundtrips(val, e_func, d_func):
    encoded = e_func(val)
    decoded = d_func(encoded)
    assert decoded == val, f"Given {val}, encoded: {encoded}, decoded: {decoded}"


@given(strategies.booleans())
def test_roundtrip_bool(val: bool):
    assert_roundtrips(val, encode.encode_bool, decode.decode_bool)


def assert_parses(text: str) -> lark.Tree:
    return parse.parse(text)


#def test_parse_empty():
    #assert_parses("{}")


def test_parse_enum():
    with open("tests/schemas/enum.bop") as f:
        text = f.read()
    assert_parses(text)


def test_parse_struct():
    with open("tests/schemas/struct.bop") as f:
        text = f.read()
    assert_parses(text)


def test_parse_message():
    with open("tests/schemas/message.bop") as f:
        text = f.read()
    assert_parses(text)


def test_parse_combined():
    with open("tests/schemas/combined.bop") as f:
        text = f.read()
    assert_parses(text)


@given(enum_strategy)
def test_gen_enums(enum_def: str):
    tree = parse.parse(enum_def)
    enum_tree = tree.children[0]
    typ = generate.gen_enum(enum_tree)
    #assert type(typ) == class


@given(struct_strategy)
def test_gen_structs(struct_def: str):
    tree = parse.parse(struct_def)
    struct_tree = tree.children[0]
    try:
        typ = generate.gen_struct(struct_tree)
        assert type(typ) == type
    except generate.DuplicateFieldError:
        pass


@given(msg_strategy)
def test_gen_messages(msg_def: str):
    tree = parse.parse(msg_def)
    msg_tree = tree.children[0]
    typ = generate.gen_message(msg_tree)
    assert type(typ) == type

# BebopPy

This is a proof-of-concept implementation of the [bebop](https://bebop.sh/) serialization protocol in python. It doesn't work yet.

## Goals

To provide a python library that makes it easy to convert messages in the Bebop wire-format into python objects, and vice versa.

Some sub-goals, in decreasing order of priority:

* Correctness - Do The Right Thing, and raise an Exception if you can't. As a rule of thumb, there should be more testing code than implementation code.
* Completeness of protocol - Support 100% interop over-the-wire with the reference implementation.
* Speed - provide fast (de)serialization with low memory overhead

## Status

### Bop parser

Initial pass complete, can parse simple bop schemas. See grammar definition contained at [parse.py](beboppy/parse.py).

Not yet implemented, but in scope:

* Attribute support (opcode, deprecated)
* Comment support

### Type generation

Very rough draft at [generate.py](beboppy/generate.py).

### Generation of encode/decode functions

Not yet started.

### De/Encoder

Barely started - can round-trip booleans, and that's about it.

## Design

To get off the ground quickly, I've chosen [Lark](https://github.com/lark-parser/lark) to build the Bop parser on top of. It is rather flexible and easy to work with.

I like using [Hypothesis](https://hypothesis.works/) for property-based testing. In my experience, it exposes edge cases nearly-effortlessly.

from struct import iter_unpack, unpack_from


def decode_bool(b: bytes) -> bool:
    assert len(b) == 2
    assert b[0] == 0
    return b[1] == 1


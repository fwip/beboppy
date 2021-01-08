from struct import pack, pack_into


def encode_bool(b: bool) -> bytes:
    if b:
        return bytes([0, 1])
    return bytes([0, 0])


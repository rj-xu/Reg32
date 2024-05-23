import binascii

type BitsT = int | tuple[int, int] | list[int | tuple[int, int]]


def create_mask(bits: BitsT) -> int:
    mask = 0
    match bits:
        case int():
            mask = 0x01 << bits
        case tuple():
            s, l = bits
            temp = 0x01 << s
            for i in range(l):
                mask |= temp << i
        case list():
            for b in bits:
                mask |= create_mask(b)
    return mask


def is_set_bits(val: int, bits: BitsT) -> bool:
    mask = create_mask(bits)
    return (val & mask) == mask


def is_clear_bits(val: int, bits: BitsT) -> bool:
    mask = create_mask(bits)
    return (val & mask) == 0


def get_bits(val: int, bits: BitsT) -> int:
    mask = create_mask(bits)
    val = val & mask
    if isinstance(bits, tuple):
        val = val >> bits[0]
    return val


def convert_str_to_bytes(s: str) -> bytes:
    return binascii.unhexlify(s)


def convert_list_to_le(nums: list[int] | bytes) -> int:
    return int.from_bytes(bytes(nums), byteorder="little", signed=False)


def convert_list_to_be(nums: list[int] | bytes) -> int:
    return int.from_bytes(bytes(nums), byteorder="big", signed=False)


def convert_be_to_list(num: int) -> list[int]:
    return list(num.to_bytes(length=(num.bit_length() + 7) // 8, byteorder="big", signed=False))


def convert_le_to_list(num: int) -> list[int]:
    return list(num.to_bytes(length=(num.bit_length() + 7) // 8, byteorder="little", signed=False))

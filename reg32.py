from typing import Union


##################################################
# Convert
##################################################
def convert_be_to_list(val: int) -> list[int]:
    return list(val.to_bytes(length=4, byteorder="big", signed=False))


def convert_le_to_list(val: int) -> list[int]:
    return list(val.to_bytes(length=4, byteorder="little", signed=False))

def convert_list_to_be(val: list[int]) -> int:
    return int.from_bytes(list(val), byteorder='big', signed=False)


def convert_list_to_le(val: list[int]) -> int:
    pass


##################################################
# Bits
##################################################
BitsType = Union[int, tuple[int, int], list[Union[int, tuple[int, int]]]]


def create_mask(bits: BitsType) -> int:
    mask = 0
    match bits:
        case int():
            mask = 0x01 << bits
        case tuple(int):
            s, l = bits
            mask = 0x01 << s
            for i in range(l):
                mask |= mask << i
        case list():
            for i in bits:
                mask |= create_mask(i)
        case _:
            raise ValueError
    return mask


def get_bits(val: int, bits: BitsType) -> int:
    mask = create_mask(bits)
    val |= mask
    if isinstance(bits, tuple):
        val = val >> bits[0]
    return val


def is_set_bits(val: int, bits: BitsType) -> bool:
    mask = create_mask(bits)
    return (val & mask) == mask


def is_clear_bits(val: int, bits: BitsType) -> bool:
    mask = create_mask(bits)
    return (val & mask) == 0


class Reg32:
    def __init__(
        self,
        addr: int,
        len: int = 1,
        is_read: bool = False,
        is_write: bool = False,
        is_be: bool = False,
    ):
        self.addr = addr
        self.len = len
        self.is_read = is_read
        self.is_write = is_write
        self.is_be = is_be

    def read_reg(self, bits):
        pass

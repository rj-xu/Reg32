import math
import os
import pickle
import time
from typing import Any, Callable, Optional, Union

# BIT definition
BIT0 = 0x01
BIT1 = 0x02
BIT2 = 0x04
BIT3 = 0x08
BIT4 = 0x10
BIT5 = 0x20
BIT6 = 0x40
BIT7 = 0x80

BitsType = Union[int, tuple[int, int], list[int | tuple[int, int]]]


#################################################
# CONVERT
#################################################
def convert_list_to_little_endian(nums: list[int] | bytes) -> int:
    return int.from_bytes(bytes(nums), byteorder="little", signed=False)


def convert_list_to_big_endian(nums: list[int] | bytes) -> int:
    return int.from_bytes(bytes(nums), byteorder="big", signed=False)


def convert_big_endian_to_list(num: int) -> list[int]:
    return list(
        num.to_bytes(length=(num.bit_length() + 7) // 8, byteorder="big", signed=False)
    )


def convert_little_endian_to_list(num: int) -> list[int]:
    return list(
        num.to_bytes(
            length=(num.bit_length() + 7) // 8, byteorder="little", signed=False
        )
    )


#################################################
# BITS OPT
#################################################
def create_mask(bits: BitsType) -> int:
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


def is_set_bits(val: int, bits: BitsType) -> bool:
    mask = create_mask(bits)
    return (val & mask) == mask


def is_clear_bits(val: int, bits: BitsType) -> bool:
    mask = create_mask(bits)
    return (val & mask) == 0


def get_bits(val: int, bits: BitsType) -> int:
    mask = create_mask(bits)
    val = val & mask
    if isinstance(bits, tuple):
        val = val >> bits[0]
    return val


#################################################
# CONDITION DECORATOR
#################################################


def wait_for(condition: Callable[[], bool], t: float = 0.1):
    while True:
        if condition():
            break
        time.sleep(t)


def retry(condition: Callable[[], bool], r: int = 10, t: float = 0.1):
    is_done = False
    for _ in range(r):
        if condition():  # toggle raises.
            is_done = True
            break
        time.sleep(t)

    return is_done


#################################################
# DEBUG
#################################################
def read_pickle(filename: str) -> Any:
    path = os.path.join(config.PICKLE, f"{filename}.pickle")
    with open(path, "rb") as f:
        return pickle.load(f)


def save_pickle(filename: str, val) -> None:
    path = os.path.join(config.PICKLE, f"{filename}.pickle")
    with open(path, "wb") as f:
        pickle.dump(val, f)


def get_time_str() -> str:
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

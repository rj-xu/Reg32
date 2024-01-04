from typing import Union


from enum import Enum, unique
from typing import Optional, Union, Literal



class Reg:
    def __init__(
        self,
        addr: int,
        bytes_: int = 0,
        is_read: bool = False,
        is_write: bool = False,
        is_big_end: bool = False,
    ) -> None:
        self.addr: int = addr
        self.bytes: int = bytes_
        self.is_read: bool = is_read
        self.is_write: bool = is_write
        self.is_big_end: bool = is_big_end

    def read_reg(
        self,
        bits: Optional[BitsType] = None,
        set_bits: Optional[BitsType] = None,
        clear_bits: Optional[BitsType] = None,
    ) -> int:
        assert self.bytes == 1, "Reg Bytes > 1"
        val = ipt.read(self.addr)
        if set_bits:
            assert utils.is_set_bits(val, set_bits)
        if clear_bits:
            assert utils.is_clear_bits(val, clear_bits)
        if bits:
            val = utils.get_bits(val, bits)
        return val

    def read_list(
        self, bytes_: Optional[int] = None, need_convert: bool = True
    ) -> list[int]:
        if not bytes_:
            bytes_ = self.bytes
        assert bytes_ <= self.bytes, f"Reg Bytes {bytes_} > {self.bytes}"
        val = []
        for i in range(bytes_):
            val.append(ipt.read(self.addr + i))
        if self.is_big_end and need_convert:
            val.reverse()
        return val

    def read_num(self) -> int:
        val = self.read_list()
        return utils.convert_list_to_little_endian(val)

    def write_reg(
        self,
        val: int = 0,
        bits: Optional[tuple[int, int]] = None,
        set_bits: Optional[BitsType] = None,
        clear_bits: Optional[BitsType] = None,
    ) -> None:
        assert self.bytes == 1, "Reg Bytes > 1"

        if set_bits or clear_bits or bits:
            rv = self.read_reg()
            if set_bits:
                mask = utils.create_mask(set_bits)
                rv |= mask
            if clear_bits:
                mask = utils.create_mask(clear_bits)
                rv &= ~mask
            if bits:
                mask = utils.create_mask(bits)
                s, l = bits
                rv &= ~mask
                val = utils.get_bits(val, (0, l)) << s
            val |= rv

        return ipt.write(self.addr, val)

    def write_list(
        self, val: Union[list[int], bytes, bytearray], need_convert: bool = True
    ) -> None:
        bytes_ = len(val)
        assert bytes_ <= self.bytes, f"Reg Bytes {bytes_} > {self.bytes}"

        if self.is_big_end and need_convert:
            val = val[::-1]

        for i, v in enumerate(val):
            ipt.write(self.addr + i, v)

    def write_num(self, val: int) -> None:
        v_list = utils.convert_little_endian_to_list(val)
        self.write_list(v_list)

    def toggle_reg(self, bits: Optional[BitsType]) -> None:
        rv = self.read_reg()
        mask = 0xFF
        if bits:
            mask = utils.create_mask(bits)
        val = rv ^ mask
        self.write_reg(val)

    def trigger_reg(
        self,
        bits: Optional[BitsType],
        order: Literal["write_0_then_1", "write_1_then_0"] = "write_0_then_1",
        need_reread=False,
    ) -> None:
        rv = 0x00
        mask = 0xFF

        if bits:
            rv = self.read_reg()
            mask = utils.create_mask(bits)

        if order == "write_0_then_1":
            val = rv & (~mask)
            self.write_reg(val)

            if need_reread:
                rv = self.read_reg()

            val = rv | mask
            self.write_reg(val)
        else:
            val = rv | mask
            self.write_reg(val)

            if need_reread:
                rv = self.read_reg()

            val = rv & (~mask)
            self.write_reg(val)


@unique
class CryptoReg(Enum):
    # fmt: off

    ##################################################
    # BASE
    ##################################################
    BASE_ADDR = Reg(0x1A00)
    RAM_ADDR  = Reg(0x1A90)
    # TODO: Move into ScRegTable
    SC_RW = Reg(addr=0x16E8, bytes_=1, is_read=True, is_write=True, is_big_end=False)

    ##################################################
    # REG
    ##################################################
    GLB_CFG0_RW         = Reg(addr=0x1A00, bytes_=1,  is_read=True, is_write=True,  is_big_end=False)
    GLB_CFG1_RW         = Reg(addr=0x1A01, bytes_=1,  is_read=True, is_write=True,  is_big_end=False)

    # fmt: on


for reg in CryptoReg:
    assert isinstance(reg.value, Reg), f"{reg.name} Is Not Reg Type"

    if reg.name in ("BASE_ADDR", "RAM_ADDR", "SC_RW"):
        pass
    else:
        attr = reg.name[-2:]
        match attr:
            case "RO":
                assert (
                    reg.value.is_read is True and reg.value.is_write is False
                ), f"Illegal Attribute: {reg.name}"
            case "WO":
                assert (
                    reg.value.is_read is False and reg.value.is_write is True
                ), f"Illegal Attribute: {reg.name}"
            case "RW":
                assert (
                    reg.value.is_read is True and reg.value.is_write is True
                ), f"Illegal Attribute: {reg.name}"
            case _:
                raise UserWarning(f"Unknown Reg Name {reg.name}")

        is_ram = reg.name[:3] == "RAM"
        if is_ram:
            assert (
                reg.value.addr >= CryptoReg.RAM_ADDR.value.addr
            ), f"Illegal Address: {reg.name}"
        else:
            assert (
                CryptoReg.BASE_ADDR.value.addr
                <= reg.value.addr
                <= CryptoReg.RAM_ADDR.value.addr
            ), f"Illegal Address: {reg.name}"

@dataclass
class Reg:
    addr: int
    bytes: int
    is_read: bool
    is_write: bool
    is_be: bool

    @overload
    def read(
        self,
        set_bits: None = None,
        clear_bits: None = None,
        bits: BitsT | None = None,
    ) -> int: ...

    @overload
    def read(
        self,
        set_bits: BitsT,
        clear_bits: BitsT | None,
        bits: BitsT | None = None,
    ) -> tuple[int, bool]: ...

    @overload
    def read(
        self,
        set_bits: BitsT | None,
        clear_bits: BitsT,
        bits: BitsT | None = None,
    ) -> tuple[int, bool]: ...

    def read(
        self,
        set_bits: BitsT | None = None,
        clear_bits: BitsT | None = None,
        bits: BitsT | None = None,
    ) -> int | tuple[int, bool]:
        val = g_device.read(self.addr)
        logger.debug(f"Read Reg {self.addr:#010x}: {val:#04x}")

        if set_bits and not u_bits.is_set_bits(val, set_bits):
            return (val, False)

        if clear_bits and not u_bits.is_clear_bits(val, clear_bits):
            return (val, False)

        if bits:
            val = u_bits.get_bits(val, bits)

        return val if not (set_bits or clear_bits) else (val, True)

    def read_bytes(self, bytes_: int | None = None, need_convert: bool = True) -> "bytes":
        if not bytes_:
            bytes_ = self.bytes

        if bytes_ > self.bytes:
            raise ValueError

        val = [g_device.read(self.addr + i) for i in range(bytes_)]

        if self.is_be and need_convert:
            val.reverse()

        logger.debug(f"Read Reg {self.addr:#010x}, {bytes_}: [{val[0]:#04x}, ...]")

        return bytes(val)

    def read_num(self) -> int:
        val = self.read_bytes()
        return u_bits.convert_list_to_be(val) if self.is_be else u_bits.convert_list_to_le(val)

    @overload
    def write(
        self,
        val: int,
        set_bits: None = None,
        clear_bits: None = None,
        bits: tuple[int, int] | None = None,
    ) -> None: ...

    @overload
    def write(
        self,
        val: None,
        set_bits: BitsT,
        clear_bits: BitsT | None,
        bits: None = None,
    ) -> None: ...

    @overload
    def write(
        self,
        val: None,
        set_bits: BitsT | None,
        clear_bits: BitsT,
        bits: None = None,
    ) -> None: ...

    @overload
    def write(
        self,
        val: int,
        set_bits: BitsT | None,
        clear_bits: BitsT | None,
        bits: tuple[int, int],
    ) -> None: ...

    def write(
        self,
        val: int | None = None,
        set_bits: BitsT | None = None,
        clear_bits: BitsT | None = None,
        bits: tuple[int, int] | None = None,
    ) -> None:
        if not val:
            val = 0

        if set_bits or clear_bits or bits:
            rv = self.read()
            if set_bits:
                mask = u_bits.create_mask(set_bits)
                rv |= mask
            if clear_bits:
                mask = u_bits.create_mask(clear_bits)
                rv &= ~mask
            if bits:
                mask = u_bits.create_mask(bits)
                s, l = bits
                rv &= ~mask
                val = u_bits.get_bits(val, (0, l)) << s
            val |= rv

        logger.debug(f"Write Reg {self.addr:#010x}: {val:#04x}")
        return g_device.write(self.addr, val)

    def write_bytes(self, val: "list[int] | bytes | bytearray", need_convert: bool = True) -> None:
        bytes_ = len(val)
        if bytes_ > self.bytes:
            raise ValueError

        if self.is_be and need_convert:
            val = val[::-1]

        logger.debug(f"Write Reg {self.addr:#010x}, {bytes_}: [{val[0]:#04x}, ...]")

        for i, v in enumerate(val):
            g_device.write(self.addr + i, v)

    def write_num(self, val: int) -> None:
        v_list = u_bits.convert_le_to_list(val)
        self.write_bytes(v_list)

    def set(self, bits: BitsT | None = None) -> None:
        if bits:
            mask = u_bits.create_mask(bits)
            rv = self.read()
            val = rv | mask
        else:
            val = 0x01
        self.write(val)

    def clear(self, bits: BitsT | None = None) -> None:
        if bits:
            mask = u_bits.create_mask(bits)
            rv = self.read()
            val = rv & (~mask)
        else:
            val = 0x00
        self.write(val)

    def toggle(self, bits: BitsT | None = None) -> None:
        rv = self.read()
        mask = u_bits.create_mask(bits) if bits else 0xFF
        val = rv ^ mask
        self.write(val)

    def trigger(
        self,
        bits: BitsT | None = None,
        order: Literal["write_0_then_1", "write_1_then_0"] = "write_1_then_0",
        need_reread: bool = False,
    ) -> None:
        rv = 0x00
        mask = 0xFF

        if bits:
            rv = self.read()
            mask = u_bits.create_mask(bits)

        if order == "write_0_then_1":
            val = rv & (~mask)
            self.write(val)

            if need_reread:
                rv = self.read()

            val = rv | mask
            self.write(val)
        else:
            val = rv | mask
            self.write(val)

            if need_reread:
                rv = self.read()

            val = rv & (~mask)
            self.write(val)

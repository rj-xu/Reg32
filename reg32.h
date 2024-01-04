#pragma once

#include <limits.h>
#include <stdint.h>
#include <stdbool.h>

/////////////////////////////////////////////////
// Utils
/////////////////////////////////////////////////
#ifndef BUILD_BUG_ON_ZERO
#define BUILD_BUG_ON_ZERO(e) \
  ((int)sizeof(struct { int : (-!!(e)); }))
#endif

#ifndef COUNT_ARGS
#define COUNT_ARGS(args...) _COUNT_ARGS(_, ##args,      \
                                        10, 9, 8, 7, 6, \
                                        5, 4, 3, 2, 1,  \
                                        0)
#define _COUNT_ARGS(_,                  \
                    _0, _1, _2, _3, _4, \
                    _5, _6, _7, _8, _9, \
                    args...) _COUT_ARGS_FIRST(args)
#define _COUT_ARGS_FIRST(count, args...) count
#endif

/////////////////////////////////////////////////
// Bit
/////////////////////////////////////////////////

#define BIT32(bit) (1UL << (bit))
// Find the first set bit (31-0)
#define BIT32_FFS(mask) (__builtin_ffs(mask) - 1)
// Find the last set bit (31-0)
#define BIT32_FLS(mask) (31 - __builtin_clz(mask))
// Count the set bits
#define BIT32_CNT(mask) __builtin__popcount(mask)

#define BIT32_MASK_OF_FIRST_SET(mask) ((mask) & -(mask))

#define BIT32_IS_CONTINUOUS(mask) \
  ((BIT32_FLS(mask) - BIT32_FFS(mask) + 1) == BIT32_CNT(mask))

#define BYTE4(byte) MASK32((byte) * 8, 8)

/////////////////////////////////////////////////
// Mask
/////////////////////////////////////////////////

// Mask (from x for n bits)
#define MASK32(x, n) (((1UL << (n)) - 1) << (x))
// Mask (closed interval [x, y])
#define MASK32_SQ(x, y) MASK32((x), (y) - (x) + 1)

#define MASK32_VA(x, args...)                    \
  ({                                             \
    uint32_t _m = 0;                             \
    for (int i = 0; i < COUNT_ARGS(##args); i++) \
    {                                            \
      _m |= BIT32(i);                            \
    }                                            \
    _m;                                          \
  })

/////////////////////////////////////////////////
// Reg
/////////////////////////////////////////////////

#define REG32(reg) (*(volatile uint32_t *)(reg))

#define REG32_READ(reg) REG32(reg)
#define REG32_WRITE(reg, val)     \
  do                              \
  {                               \
    REG32(reg) = (uint32_t)(val); \
  } while (0)

#define REG32_ENABLE(reg) \
  do                      \
  {                       \
    REG32(reg) = 1;       \
  } while (0)
#define REG32_DISABLE(reg) \
  do                       \
  {                        \
    REG32(reg) = 0;        \
  } while (0)

#define REG32_GET(reg, mask) (REG32(reg) & (mask))
#define REG32_SET(reg, mask) \
  do                         \
  {                          \
    REG32(reg) |= (mask);    \
  } while (0)
#define REG32_CLEAR(reg, mask) \
  do                           \
  {                            \
    REG32(reg) &= ~(mask);     \
  } while (0)

#define REG32_TOGGLE(reg, mask) \
  do                            \
  {                             \
    REG32(reg) ^= (mask);       \
  } while (0)

#define REG32_TRIGGER(reg, mask)   \
  do                               \
  {                                \
    uint32_t _v = REG32_READ(reg); \
    REG32(reg) = _v | (mask);      \
    REG32(reg) = _v & (~(mask));   \
  } while (0)

#define REG32_GET_BITS(reg, x, n) \
  (REG32_GET((reg), MASK32((x), (n))) >> (x))
#define REG32_SET_BITS(reg, x, n, val)                \
  do                                                  \
  {                                                   \
    REG32(reg) =                                      \
        (uint32_t)(REG32(reg) & (~MASK32((x), (n))) | \
                   (((val) & MASK(0, (n))) << (x)));  \
  } while (0)

/////////////////////////////////////////////////
// Big/Little Endian
/////////////////////////////////////////////////

#define BE_TO_LE32(x)                                   \
  ((0x000000FF & (x) << 24) | (0x0000FF00 & (x) << 8) | \
   (0x00FF0000 & (x) >> 8) | (0xFF000000 & (x) >> 24))

#define LE_TO_BE32(x) BE_TO_LE32(x)
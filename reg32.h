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

#define BIT(bit) (1UL << (bit))
// Find the first set bit (31-0)
#define BIT_FFS(mask) (__builtin_ffs(mask) - 1)
// Find the last set bit (31-0)
#define BIT_FLS(mask) (31 - __builtin_clz(mask))
// Count the set bits
#define BIT_CNT(mask) __builtin__popcount(mask)

#define BIT_MASK_OF_FIRST_SET(mask) ((mask) & -(mask))

#define BIT_IS_CONTINUOUS(mask) \
  ((BIT_FLS(mask) - BIT_FFS(mask) + 1) == BIT_CNT(mask))

/////////////////////////////////////////////////
// Mask
/////////////////////////////////////////////////

// Mask (from x for n bits)
#define MASK(x, n) (((1UL << (n)) - 1) << (x))
// Mask (closed interval [x, y])
#define MASK_SQ(x, y) MASK((x), (y) - (x) + 1)

// // TODO
// #define MASK_VA(args...)                       \
//   ({                                             \
//     uint32_t _mask = 0;                          \
//     for (int i = 0; i < COUNT_ARGS(##args); i++) \
//     {                                            \
//       _mask |= BIT(i);                         \
//     }                                            \
//     _m;                                          \
//   })

#define MASK_BYTE(byte) MASK((byte) * 8, 8)
#define BYTE(byte, mask) ((mask) << ((byte) * 8))

/////////////////////////////////////////////////
// Reg
/////////////////////////////////////////////////

#define REG(reg) (*(volatile uint32_t *)(reg))

#define REG_READ(reg) REG(reg)
#define REG_WRITE(reg, val)     \
  do                            \
  {                             \
    REG(reg) = (uint32_t)(val); \
  } while (0)

#define REG_ENABLE(reg) \
  do                    \
  {                     \
    REG(reg) = 1;       \
  } while (0)
#define REG_DISABLE(reg) \
  do                     \
  {                      \
    REG(reg) = 0;        \
  } while (0)

#define REG_GET(reg, mask) (REG(reg) & (mask))
#define REG_SET(reg, mask) \
  do                       \
  {                        \
    REG(reg) |= (mask);    \
  } while (0)
#define REG_CLEAR(reg, mask) \
  do                         \
  {                          \
    REG(reg) &= ~(mask);     \
  } while (0)

#define REG_TOGGLE(reg, mask) \
  do                          \
  {                           \
    REG(reg) ^= (mask);       \
  } while (0)

#define REG_TRIGGER(reg, mask)   \
  do                             \
  {                              \
    uint32_t _v = REG_READ(reg); \
    REG(reg) = _v | (mask);      \
    REG(reg) = _v & (~(mask));   \
  } while (0)

#define REG_GET_BITS(reg, x, n) \
  (REG_GET((reg), MASK((x), (n))) >> (x))
#define REG_SET_BITS(reg, x, n, val)                 \
  do                                                 \
  {                                                  \
    REG(reg) =                                       \
        (uint32_t)(REG(reg) & (~MASK((x), (n))) |    \
                   (((val) & MASK(0, (n))) << (x))); \
  } while (0)

/////////////////////////////////////////////////
// Big/Little Endian
/////////////////////////////////////////////////

#define BE_TO_LE(x)                                   \
  ((0x000000FF & (x) << 24) | (0x0000FF00 & (x) << 8) | \
   (0x00FF0000 & (x) >> 8) | (0xFF000000 & (x) >> 24))

#define LE_TO_BE(x) BE_TO_LE(x)
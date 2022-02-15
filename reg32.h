#pragma once

#include <limits.h>
#include <stdint.h>
#include <stdbool.h>

#define BUILD_BUG_ON_ZERO(e) ((int)(sizeof(struct { int : (-!!(e)); })))

// Mask (from x for n bits)
#define MASK32(x, n) (((uint32_t)(n) >= sizeof(uint32_t) * CHAR_BIT) ? (uint32_t)-1 : ((1UL << (n)) - 1) << (x))
// Mask (closed interval [x, y])
#define MASK32_CLOSED(x, y) MASK32(x, y - x + 1)

#define BIT32(bit) (1UL << (bit))
// Find the first set bit (31-0)
#define BIT32_FFS(mask) (BUILD_BUG_ON_ZERO(mask) + __builtin_ffs(mask) - 1)
// Find the last set bit (31-0)
#define BIT32_FLS(mask) (BUILD_BUG_ON_ZERO(mask) + sizeof(uint32_t) * CHAR_BIT - __builtin_clz(mask) - 1)
// Count the set bits
#define BIT32_COUNT(mask)       (__builtin__popcount(mask))
#define BIT32_MASK_OF_FFS(mask) ((mask) & -(mask))
#define BIT32_IS_CONTINUOUS(mask) (BIT32_FLS(mask) - BIT32_FFS(mask) + 1 == BIT32_COUNT(mask))
#define BITS32(start,end) ((uint32_t)-1)

#define REG32(reg)           (*(volatile uint32_t *)(reg))
#define REG32_GET(reg, mask) (REG32(reg) & (mask))
#define REG32_SET(reg, mask) \
  do {                       \
    REG32(reg) |= (mask);    \
  } while (0)
#define REG32_CLEAR(reg, mask) \
  do {                         \
    REG32(reg) &= ~(mask);     \
  } while (0)
#define REG32_TOGGLE(reg, mask) \
  do {                          \
    REG32(reg) ^= (mask);       \
  } while (0)
#define REG32_BOOL(reg, mask) ((bool)(!!REG32_GET(reg, mask)))

#define REG32_SWITCH(reg, enable) \
  do {                            \
    REG32(reg) = !!(enable);      \
  } while (0)
#define REG32_ENABLE(reg) \
  do {                    \
    REG32(reg) = 1;       \
  } while (0)
#define REG32_DISABLE(reg) \
  do {                     \
    REG32(reg) = 0;        \
  } while (0)

#define REG32_READ(reg) REG32(reg)
#define REG32_WRITE(reg, val)     \
  do {                            \
    REG32(reg) = (uint32_t)(val); \
  } while (0)

#define REG32_FIELD_GET_BITS(reg, x, n) ((int)REG32_GET(reg, MASK32(x, n)) >> (x))
#define REG32_FIELD_SET_BITS(reg, x, n, val)                                             \
  do {                                                                                   \
    REG32(reg) = (uint32_t)(REG32(reg) & (~MASK32(x, n)) | ((val & MASK(0, n)) << (x))); \
  } while (0)
#define REG32_FIELD_GET(reg, mask)      ((int)REG32_GET(reg, mask) >> BIT32_FFS(mask))
#define REG32_FIELD_SET(reg, mask, val) REG32_FIELD_SET_BITS(reg, BIT32_FFS(mask), BIT32_COUNT(mask), val)

#define REG32_GET_BIT(reg, bit)    REG32_GET(reg, BIT32(bit))
#define REF32_SET_BIT(reg, bit)    REG32_SET(reg, BIT32(bit))
#define REG32_CLEAR_BIT(reg, bit)  REG32_CLEAR(reg, BIT32(bit))
#define REG32_TOGGLE_BIT(reg, bit) REG32_TOGGLE(reg, BIT32(bit))
#define REG32_BOOL_BIT(reg, bit)   REG32_BOOL(reg, BIT32(bit))

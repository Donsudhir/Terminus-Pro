#!/bin/bash
# Seed hybrid vendor trees from the image's musl/glibc packages.
set -euo pipefail

ROOT=/app/vendor
ALPHA="$ROOT/alpha"
BRAVO="$ROOT/bravo"
CHARLIE="$ROOT/charlie"

MUSL_INC=/usr/include/x86_64-linux-musl
MUSL_LIB=/usr/lib/x86_64-linux-musl

mkdir -p "$ALPHA/include" "$ALPHA/lib" "$BRAVO/include" "$BRAVO/lib" "$CHARLIE/include" "$CHARLIE/lib"

cp -a "$MUSL_INC/." "$BRAVO/include/"
cp -a "$MUSL_LIB"/*.a "$BRAVO/lib/"
cp -a "$MUSL_LIB"/crt1.o "$MUSL_LIB"/crti.o "$MUSL_LIB"/crtn.o "$BRAVO/lib/"

cp -a "$MUSL_INC/." "$ALPHA/include/"
cp -f /app/vendor/alpha/overlay/courier_abi.h "$ALPHA/include/courier_abi.h"
cp -a "$MUSL_LIB"/crti.o "$MUSL_LIB"/crtn.o "$ALPHA/lib/"
gcc -c -o "$ALPHA/lib/crt1.o" /app/vendor/alpha/overlay/interp_crt1.s

cp -a "$MUSL_LIB/libc.a" "$CHARLIE/lib/libc.a"
cp -a "$MUSL_INC/." "$CHARLIE/include/"

gcc -c -isystem "$BRAVO/include" -o /tmp/thread_slot.o /app/src/thread_slot.c
gcc -c -isystem "$BRAVO/include" -o /tmp/errno_slot.o /app/src/errno_slot.c
ar rcs "$BRAVO/lib/libslots.a" /tmp/thread_slot.o /tmp/errno_slot.o

gcc -c -isystem "$BRAVO/include" -o /tmp/charlie_slots.o /app/src/charlie_slots.c
ar rcs "$CHARLIE/lib/libslots.a" /tmp/charlie_slots.o

if command -v musl-gcc >/dev/null 2>&1; then
  HIDDEN=/usr/local/libexec
  mkdir -p "$HIDDEN"
  mv "$(command -v musl-gcc)" "$HIDDEN/musl-gcc.hidden" || true
fi
rm -f /usr/bin/musl-gcc /usr/local/bin/musl-gcc 2>/dev/null || true

echo "vendor trees seeded"

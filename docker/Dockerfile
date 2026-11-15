# The compiler every video uses. Pinned so error messages look the same in every video.
# Bump the tag only between parts of the series, never in the middle of one.
FROM gcc:15

# python3: the C++ vs Python race in video 1. gdb: 10.4. cmake: 10.3 and later.
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 gdb cmake \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /work

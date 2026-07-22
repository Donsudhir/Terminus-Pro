CXX ?= g++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -Iinclude
LDFLAGS ?=

SOURCES := $(shell find src -type f -name '*.cpp' | sort)
OBJECTS := $(patsubst src/%.cpp,build/%.o,$(SOURCES))
TARGET := build/loam

.PHONY: all clean
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(OBJECTS) $(LDFLAGS) -o $@

build/%.o: src/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf build

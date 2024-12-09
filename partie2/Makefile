# Makefile for compiling jesp_example

# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -I/usr/local/include/madp

# Linker flags
LDFLAGS = -L/usr/local/lib -lMADP -lxml2 -lm

# Target executable
TARGET = jesp_example

# Source files
SRCS = prog.cpp

# Default target
all: $(TARGET)

# Build target
$(TARGET): $(SRCS)
	$(CXX) -o $(TARGET) $(SRCS) $(CXXFLAGS) $(LDFLAGS)

# Clean target
clean:
	rm -f $(TARGET)
# Makefile for compiling main.cpp and JESPForGridSmall.cpp

# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -I/usr/local/include/madp

# Linker flags
LDFLAGS = -L/usr/local/lib -lMADP -lxml2 -lm

# Target executable
TARGET = bin/best_response

# Source files
SRCS = src/main.cpp src/JESPForGridSmall.cpp

# Default target
all: $(TARGET)

# Ensure bin directory exists and build target
$(TARGET): $(SRCS)
	mkdir -p bin
	$(CXX) -o $(TARGET) $(SRCS) $(CXXFLAGS) $(LDFLAGS)

# Clean target
clean:
	rm -rf bin

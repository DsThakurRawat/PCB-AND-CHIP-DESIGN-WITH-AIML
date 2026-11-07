# Makefile for STM32 Water Pump Controller Firmware

CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2 -Iinc -DTEST_HOST

SRC = src/timer.c src/gpio.c src/adc.c src/pump.c
TEST_SRC = test/test_controller.c $(SRC)
TEST_BIN = build/test_controller

.PHONY: all test clean

all: test

$(TEST_BIN): $(TEST_SRC)
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $(TEST_SRC)

test: $(TEST_BIN)
	@echo "Running Automated Unit Test Suite..."
	@./$(TEST_BIN)

clean:
	rm -rf build

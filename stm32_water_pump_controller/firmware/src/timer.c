/**
 * @file timer.c
 * @brief Millisecond Tick & Timing Implementation
 */

#include "timer.h"

#if defined(TEST_HOST)
static uint32_t mock_system_ms = 0;

void timer_init(void) {
    mock_system_ms = 0;
}

uint32_t timer_get_ms(void) {
    return mock_system_ms;
}

void timer_mock_advance_ms(uint32_t ms) {
    mock_system_ms += ms;
}

void timer_mock_reset(void) {
    mock_system_ms = 0;
}

void timer_delay_ms(uint32_t ms) {
    mock_system_ms += ms;
}

#else

/* Target STM32 Hardware Implementation */
#include <stm32f103xb.h>

static volatile uint32_t system_ms = 0;

void SysTick_Handler(void) {
    system_ms++;
}

void timer_init(void) {
    /* Configure SysTick to generate interrupt every 1ms (72MHz system clock) */
    SysTick_Config(72000000UL / 1000UL);
}

uint32_t timer_get_ms(void) {
    return system_ms;
}

void timer_delay_ms(uint32_t ms) {
    uint32_t start = timer_get_ms();
    while ((timer_get_ms() - start) < ms) {
        __NOP();
    }
}

#endif

bool timer_has_elapsed(uint32_t start_time, uint32_t duration_ms) {
    return (timer_get_ms() - start_time) >= duration_ms;
}

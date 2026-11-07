/**
 * @file timer.h
 * @brief Millisecond Tick & Timing Utilities for STM32
 */

#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize system tick timer.
 */
void timer_init(void);

/**
 * @brief Get current system uptime in milliseconds.
 * @return uint32_t Milliseconds elapsed since boot.
 */
uint32_t timer_get_ms(void);

/**
 * @brief Check if a non-blocking timeout has elapsed.
 * @param start_time Timestamp recorded at start of event.
 * @param duration_ms Target interval in milliseconds.
 * @return bool true if duration has elapsed, false otherwise.
 */
bool timer_has_elapsed(uint32_t start_time, uint32_t duration_ms);

/**
 * @brief Delay execution for a specified number of milliseconds (busy-wait).
 * @param ms Milliseconds to delay.
 */
void timer_delay_ms(uint32_t ms);

#if defined(TEST_HOST)
/**
 * @brief Host simulation: manually advance simulated system time.
 * @param ms Milliseconds to advance.
 */
void timer_mock_advance_ms(uint32_t ms);

/**
 * @brief Host simulation: reset simulated clock to 0.
 */
void timer_mock_reset(void);
#endif

#ifdef __cplusplus
}
#endif

#endif /* TIMER_H */

/**
 * @file gpio.h
 * @brief GPIO Hardware Abstraction for STM32 Water Pump Controller
 */

#ifndef GPIO_H
#define GPIO_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize all GPIO pins (LEDs, MOSFET gate, pushbuttons).
 */
void gpio_init(void);

/**
 * @brief Control 12V Water Pump Power MOSFET Gate (PB0).
 * @param state true = Turn ON pump, false = Turn OFF pump.
 */
void gpio_set_pump(bool state);

/**
 * @brief Check if pump is currently commanded ON.
 */
bool gpio_get_pump_state(void);

/**
 * @brief Set Pump Active Indicator LED (PB12).
 * @param state true = ON, false = OFF.
 */
void gpio_set_led_pump(bool state);

/**
 * @brief Set Low Moisture Warning LED (PB13).
 * @param state true = ON, false = OFF.
 */
void gpio_set_led_warn(bool state);

/**
 * @brief Set Heartbeat / Status LED (PC13).
 * @param state true = ON, false = OFF.
 */
void gpio_set_led_status(bool state);

/**
 * @brief Toggle Heartbeat / Status LED (PC13).
 */
void gpio_toggle_led_status(void);

/**
 * @brief Read Manual Override Pushbutton with debouncing (PA8).
 * @return bool true if button is pressed (active low pressed), false otherwise.
 */
bool gpio_read_btn_override(void);

#if defined(TEST_HOST)
/**
 * @brief Host simulation: manually set button state.
 */
void gpio_mock_set_button(bool pressed);
#endif

#ifdef __cplusplus
}
#endif

#endif /* GPIO_H */

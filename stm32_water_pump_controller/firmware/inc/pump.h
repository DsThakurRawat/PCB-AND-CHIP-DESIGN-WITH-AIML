/**
 * @file pump.h
 * @brief Water Pump State Machine & Irrigation Control Logic
 */

#ifndef PUMP_H
#define PUMP_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    PUMP_STATE_IDLE = 0,
    PUMP_STATE_WATERING,
    PUMP_STATE_COOLDOWN,
    PUMP_STATE_MANUAL_OVERRIDE,
    PUMP_STATE_EMERGENCY_SHUTOFF
} pump_state_t;

/**
 * @brief Initialize the water pump state machine.
 */
void pump_init(void);

/**
 * @brief Execute one iteration of the pump control state machine.
 * @param current_moisture_pct Current soil moisture reading (0 - 100%).
 * @param btn_pressed Whether manual override button is currently pressed.
 */
void pump_process(uint8_t current_moisture_pct, bool btn_pressed);

/**
 * @brief Get the current operational state of the pump controller.
 */
pump_state_t pump_get_state(void);

/**
 * @brief Get human-readable string representation of the current state.
 */
const char* pump_get_state_name(pump_state_t state);

/**
 * @brief Clear emergency safety shutdown and return to IDLE.
 */
void pump_reset_emergency(void);

#ifdef __cplusplus
}
#endif

#endif /* PUMP_H */

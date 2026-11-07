/**
 * @file pump.c
 * @brief Water Pump State Machine & Irrigation Control Implementation
 */

#include "pump.h"
#include "gpio.h"
#include "timer.h"
#include "system_config.h"

static pump_state_t current_state = PUMP_STATE_IDLE;
static uint32_t state_entry_time_ms = 0;
static bool prev_btn_state = false;

void pump_init(void) {
    current_state = PUMP_STATE_IDLE;
    state_entry_time_ms = timer_get_ms();
    prev_btn_state = false;
    gpio_set_pump(false);
    gpio_set_led_pump(false);
    gpio_set_led_warn(false);
}

pump_state_t pump_get_state(void) {
    return current_state;
}

const char* pump_get_state_name(pump_state_t state) {
    switch (state) {
        case PUMP_STATE_IDLE:               return "IDLE";
        case PUMP_STATE_WATERING:           return "WATERING";
        case PUMP_STATE_COOLDOWN:           return "COOLDOWN";
        case PUMP_STATE_MANUAL_OVERRIDE:    return "MANUAL_OVERRIDE";
        case PUMP_STATE_EMERGENCY_SHUTOFF:  return "EMERGENCY_SHUTOFF";
        default:                            return "UNKNOWN";
    }
}

void pump_reset_emergency(void) {
    if (current_state == PUMP_STATE_EMERGENCY_SHUTOFF) {
        current_state = PUMP_STATE_IDLE;
        state_entry_time_ms = timer_get_ms();
        gpio_set_pump(false);
        gpio_set_led_warn(false);
    }
}

void pump_process(uint8_t current_moisture_pct, bool btn_pressed) {
    /* Detect rising edge on button press (button transition from false to true) */
    bool btn_clicked = (btn_pressed && !prev_btn_state);
    prev_btn_state = btn_pressed;

    /* Handle Low Moisture Warning Indicator */
    if (current_moisture_pct < MOISTURE_ALERT_PCT || current_state == PUMP_STATE_EMERGENCY_SHUTOFF) {
        gpio_set_led_warn(true);
    } else {
        gpio_set_led_warn(false);
    }

    /* Manual Override Button Handler */
    if (btn_clicked) {
        if (current_state == PUMP_STATE_EMERGENCY_SHUTOFF) {
            /* Button press clears emergency lockout */
            pump_reset_emergency();
            return;
        } else if (current_state == PUMP_STATE_MANUAL_OVERRIDE || current_state == PUMP_STATE_WATERING) {
            /* Button press cancels active watering immediately */
            current_state = PUMP_STATE_IDLE;
            state_entry_time_ms = timer_get_ms();
            gpio_set_pump(false);
            return;
        } else {
            /* Trigger manual burst watering */
            current_state = PUMP_STATE_MANUAL_OVERRIDE;
            state_entry_time_ms = timer_get_ms();
            gpio_set_pump(true);
            return;
        }
    }

    /* State Machine Execution */
    switch (current_state) {
        case PUMP_STATE_IDLE:
            gpio_set_pump(false);
            /* Check if soil has dried below threshold */
            if (current_moisture_pct < MOISTURE_DRY_THRESHOLD_PCT) {
                current_state = PUMP_STATE_WATERING;
                state_entry_time_ms = timer_get_ms();
                gpio_set_pump(true);
            }
            break;

        case PUMP_STATE_WATERING:
            gpio_set_pump(true);
            /* Check 1: Target moisture reached (hysteresis upper bound) */
            if (current_moisture_pct >= MOISTURE_TARGET_PCT) {
                current_state = PUMP_STATE_COOLDOWN;
                state_entry_time_ms = timer_get_ms();
                gpio_set_pump(false);
            }
            /* Check 2: Safety timeout exceeded (possible dry reservoir / burst tube) */
            else if (timer_has_elapsed(state_entry_time_ms, PUMP_MAX_RUN_TIME_MS)) {
                current_state = PUMP_STATE_EMERGENCY_SHUTOFF;
                state_entry_time_ms = timer_get_ms();
                gpio_set_pump(false);
                gpio_set_led_warn(true);
            }
            break;

        case PUMP_STATE_COOLDOWN:
            gpio_set_pump(false);
            /* Allow water to percolate and soak before re-evaluating */
            if (timer_has_elapsed(state_entry_time_ms, PUMP_COOLDOWN_TIME_MS)) {
                current_state = PUMP_STATE_IDLE;
                state_entry_time_ms = timer_get_ms();
            }
            break;

        case PUMP_STATE_MANUAL_OVERRIDE:
            gpio_set_pump(true);
            /* Timed manual test burst */
            if (timer_has_elapsed(state_entry_time_ms, PUMP_MANUAL_BURST_MS)) {
                current_state = PUMP_STATE_IDLE;
                state_entry_time_ms = timer_get_ms();
                gpio_set_pump(false);
            }
            break;

        case PUMP_STATE_EMERGENCY_SHUTOFF:
            /* Hold pump OFF strictly until user manual intervention / reset */
            gpio_set_pump(false);
            gpio_set_led_warn(true);
            break;
    }
}

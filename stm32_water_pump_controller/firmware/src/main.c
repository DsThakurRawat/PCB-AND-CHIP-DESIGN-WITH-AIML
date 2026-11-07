/**
 * @file main.c
 * @brief STM32 Smart Water Pump Controller - Main Application Entry
 *
 * Implements the top-level superloop coordinating soil moisture acquisition,
 * hysteresis irrigation actuation, safety timeout monitoring, and diagnostics.
 */

#include "system_config.h"
#include "timer.h"
#include "gpio.h"
#include "adc.h"
#include "pump.h"

int main(void) {
    /* 1. Hardware Initialization */
    timer_init();
    gpio_init();
    adc_init();
    pump_init();

    uint32_t last_sample_time = 0;
    uint32_t last_heartbeat_time = 0;
    uint8_t current_moisture_pct = 50; /* Initial baseline */

    /* Initial reading */
    current_moisture_pct = adc_read_moisture_pct();

    /* 2. Main Superloop */
    while (1) {
        uint32_t now = timer_get_ms();

        /* Task A: Periodic Moisture Sensor Sampling (every 10 seconds) */
        if (timer_has_elapsed(last_sample_time, SENSOR_SAMPLE_INTERVAL_MS) || last_sample_time == 0) {
            current_moisture_pct = adc_read_moisture_pct();
            last_sample_time = now;
        }

        /* Task B: Poll Manual Override Button */
        bool btn_pressed = gpio_read_btn_override();

        /* Task C: Execute Pump Control State Machine */
        pump_process(current_moisture_pct, btn_pressed);

        /* Task D: Heartbeat LED Diagnostic Indication */
        pump_state_t state = pump_get_state();
        uint32_t blink_period = (state == PUMP_STATE_WATERING || state == PUMP_STATE_EMERGENCY_SHUTOFF)
                                ? HEARTBEAT_ACTIVE_PERIOD_MS
                                : HEARTBEAT_NORMAL_PERIOD_MS;

        if (timer_has_elapsed(last_heartbeat_time, blink_period)) {
            gpio_toggle_led_status();
            last_heartbeat_time = now;
        }
    }

    return 0;
}

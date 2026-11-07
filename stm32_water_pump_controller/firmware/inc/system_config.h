/**
 * @file system_config.h
 * @brief System Configuration & Parameters for STM32 Smart Water Pump Controller
 *
 * Defines pin mappings, ADC calibration constants, moisture thresholds,
 * and time-based safety limits.
 */

#ifndef SYSTEM_CONFIG_H
#define SYSTEM_CONFIG_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ========================================================================= */
/* Hardware Pin Definitions (STM32F103C8T6 LQFP-48)                         */
/* ========================================================================= */

/* Soil Moisture Sensor Analog Front-End */
#define PIN_MOISTURE_ADC_PORT       GPIOA
#define PIN_MOISTURE_ADC_PIN        0           /* PA0: ADC1_IN0 */

/* Water Pump Power MOSFET Gate Control */
#define PIN_PUMP_GATE_PORT          GPIOB
#define PIN_PUMP_GATE_PIN           0           /* PB0: TIM3_CH3 or GPIO */

/* Diagnostic & Status LEDs */
#define PIN_LED_PUMP_PORT           GPIOB
#define PIN_LED_PUMP_PIN            12          /* PB12: Blue LED (Pump Active) */

#define PIN_LED_WARN_PORT           GPIOB
#define PIN_LED_WARN_PIN            13          /* PB13: Red LED (Low Moisture Alert) */

#define PIN_LED_STATUS_PORT         GPIOC
#define PIN_LED_STATUS_PIN          13          /* PC13: Green LED (System Heartbeat) */

/* User Input Pushbuttons */
#define PIN_BTN_OVERRIDE_PORT       GPIOA
#define PIN_BTN_OVERRIDE_PIN        8           /* PA8: Manual Pump Override (Active Low) */

/* ========================================================================= */
/* Soil Moisture Thresholds & Calibration                                   */
/* ========================================================================= */

/**
 * Capacitive / Resistive Soil Moisture Sensor Raw ADC Calibration:
 * Air (100% dry):     ~3400 counts (3.3V / 12-bit ADC)
 * Water (100% wet):   ~1200 counts (submerged in water)
 */
#define ADC_RAW_DRY_AIR             3400U
#define ADC_RAW_SATURATED_WATER     1200U

/* Moisture percentages (0 - 100%) */
#define MOISTURE_DRY_THRESHOLD_PCT  30U     /* Below 30%: Trigger irrigation cycle */
#define MOISTURE_TARGET_PCT         65U     /* Above 65%: Soil adequately hydrated, stop pump */
#define MOISTURE_ALERT_PCT          15U     /* Below 15%: Critical drought alert */

/* ========================================================================= */
/* Timing & Safety Limits (in Milliseconds)                                 */
/* ========================================================================= */

/* Maximum continuous pump run time before emergency safety shutoff */
#define PUMP_MAX_RUN_TIME_MS        (30U * 1000U)       /* 30 seconds max */

/* Soak / Cooldown delay to allow water absorption before next sensor check */
#define PUMP_COOLDOWN_TIME_MS       (300U * 1000U)      /* 5 minutes (300 seconds) */

/* Periodic moisture sensor sampling interval */
#define SENSOR_SAMPLE_INTERVAL_MS   (10U * 1000U)       /* 10 seconds */

/* Manual override test burst duration */
#define PUMP_MANUAL_BURST_MS        (5U * 1000U)        /* 5 seconds */

/* Button debounce threshold */
#define BUTTON_DEBOUNCE_MS          50U                 /* 50 ms */

/* Heartbeat LED blink period */
#define HEARTBEAT_NORMAL_PERIOD_MS  1000U               /* 1 Hz */
#define HEARTBEAT_ACTIVE_PERIOD_MS  200U                /* 5 Hz */

#ifdef __cplusplus
}
#endif

#endif /* SYSTEM_CONFIG_H */

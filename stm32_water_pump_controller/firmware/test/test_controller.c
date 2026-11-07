/**
 * @file test_controller.c
 * @brief Automated Unit Test Suite for STM32 Water Pump Controller
 *
 * Runs on host (Linux GCC) with -DTEST_HOST to verify state machine,
 * hysteresis logic, safety timeouts, and ADC conversions.
 */

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "system_config.h"
#include "timer.h"
#include "gpio.h"
#include "adc.h"
#include "pump.h"

static int tests_run = 0;
static int tests_passed = 0;

#define TEST_ASSERT(expr, msg) do { \
    tests_run++; \
    if (expr) { \
        tests_passed++; \
        printf("  [PASS] %s\n", msg); \
    } else { \
        printf("  [FAIL] %s (Line %d: %s)\n", msg, __LINE__, #expr); \
        assert(expr); \
    } \
} while (0)

void test_adc_conversion(void) {
    printf("\n=== Test 1: ADC Conversion & Calibration ===\n");
    
    /* 1. Bone Dry Calibration Limit */
    uint8_t dry_pct = adc_counts_to_moisture_pct(ADC_RAW_DRY_AIR);
    TEST_ASSERT(dry_pct == 0, "Air calibration point (3400 counts) maps to 0% moisture");

    /* 2. Saturated Water Limit */
    uint8_t wet_pct = adc_counts_to_moisture_pct(ADC_RAW_SATURATED_WATER);
    TEST_ASSERT(wet_pct == 100, "Submerged water point (1200 counts) maps to 100% moisture");

    /* 3. Midpoint Calibration */
    uint16_t mid_count = (ADC_RAW_DRY_AIR + ADC_RAW_SATURATED_WATER) / 2;
    uint8_t mid_pct = adc_counts_to_moisture_pct(mid_count);
    TEST_ASSERT(mid_pct == 50, "Midpoint ADC (2300 counts) maps to 50% moisture");

    /* 4. Clamping beyond bounds */
    uint8_t extreme_dry = adc_counts_to_moisture_pct(4000);
    TEST_ASSERT(extreme_dry == 0, "Counts above dry limit clamp to 0%");

    uint8_t extreme_wet = adc_counts_to_moisture_pct(500);
    TEST_ASSERT(extreme_wet == 100, "Counts below wet limit clamp to 100%");
}

void test_hysteresis_control(void) {
    printf("\n=== Test 2: Hysteresis Irrigation Control ===\n");
    
    timer_mock_reset();
    gpio_init();
    pump_init();

    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "Initial state is IDLE");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump is initially OFF");

    /* Soil moisture at 50% (between 30% and 65%) -> Should remain IDLE */
    pump_process(50, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "Moisture at 50% maintains IDLE state");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump remains OFF at 50%");

    /* Soil drops to 25% (below 30% dry threshold) -> Should turn ON */
    pump_process(25, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_WATERING, "Moisture < 30% triggers WATERING state");
    TEST_ASSERT(gpio_get_pump_state(), "Pump power MOSFET gate is commanded ON");

    /* Moisture rises to 45% (above dry threshold, but below 65% target) -> Should keep WATERING */
    timer_mock_advance_ms(5000);
    pump_process(45, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_WATERING, "Moisture at 45% keeps WATERING (Hysteresis holds)");
    TEST_ASSERT(gpio_get_pump_state(), "Pump remains ON at 45%");

    /* Moisture reaches 65% target -> Should turn OFF and transition to COOLDOWN */
    timer_mock_advance_ms(5000);
    pump_process(65, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_COOLDOWN, "Moisture >= 65% transitions to COOLDOWN");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump turns OFF when target reached");
}

void test_safety_timeout_emergency_shutoff(void) {
    printf("\n=== Test 3: Maximum Continuous Run Time Safety Timeout ===\n");
    
    timer_mock_reset();
    gpio_init();
    pump_init();

    /* Start watering */
    pump_process(20, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_WATERING, "Pump starts watering at 20% moisture");

    /* Simulate 25 seconds of watering without moisture rise */
    timer_mock_advance_ms(25000);
    pump_process(20, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_WATERING, "Still watering after 25s (< 30s limit)");
    TEST_ASSERT(gpio_get_pump_state(), "Pump still ON at 25s");

    /* Advance another 6 seconds (total 31 seconds > 30s max limit) */
    timer_mock_advance_ms(6000);
    pump_process(20, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_EMERGENCY_SHUTOFF, "Timeout triggers EMERGENCY_SHUTOFF");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump is forcibly shut OFF by safety guard");

    /* Even if soil is completely dry, pump must remain locked out */
    timer_mock_advance_ms(10000);
    pump_process(0, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_EMERGENCY_SHUTOFF, "Pump stays locked out in EMERGENCY");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump will not run under emergency lockout");

    /* User clicks button -> clears emergency lockout */
    pump_process(0, true);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "Button press clears emergency lockout to IDLE");
}

void test_cooldown_period(void) {
    printf("\n=== Test 4: Post-Irrigation Cooldown & Soak Period ===\n");
    
    timer_mock_reset();
    gpio_init();
    pump_init();

    /* Trigger and complete irrigation cycle */
    pump_process(20, false);
    pump_process(68, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_COOLDOWN, "Entered COOLDOWN state");

    /* Advance 100 seconds (less than 300s cooldown) */
    timer_mock_advance_ms(100000);
    pump_process(20, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_COOLDOWN, "Remains in COOLDOWN at 100s");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump is held OFF during cooldown");

    /* Advance past 300s (total 301 seconds) */
    timer_mock_advance_ms(201000);
    pump_process(50, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "COOLDOWN completed, transitioned to IDLE");
}

void test_manual_override(void) {
    printf("\n=== Test 5: Manual Override Pushbutton Control ===\n");
    
    timer_mock_reset();
    gpio_init();
    pump_init();

    /* Click button to trigger manual burst */
    pump_process(50, true);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_MANUAL_OVERRIDE, "Button click triggers MANUAL_OVERRIDE");
    TEST_ASSERT(gpio_get_pump_state(), "Pump turns ON for manual burst");

    /* Release button and advance 3 seconds (less than 5s burst) */
    pump_process(50, false);
    timer_mock_advance_ms(3000);
    pump_process(50, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_MANUAL_OVERRIDE, "Still in MANUAL_OVERRIDE at 3s");
    TEST_ASSERT(gpio_get_pump_state(), "Pump still ON at 3s");

    /* Advance past 5s (total 5.5 seconds) */
    timer_mock_advance_ms(2500);
    pump_process(50, false);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "Manual burst completed, returned to IDLE");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump turned OFF after manual burst timeout");

    /* Test early manual cancellation: trigger manual then click again to abort */
    pump_process(50, true);
    TEST_ASSERT(pump_get_state() == PUMP_STATE_MANUAL_OVERRIDE, "Triggered manual burst");
    pump_process(50, false);
    timer_mock_advance_ms(1000);
    pump_process(50, true); /* Second click cancels */
    TEST_ASSERT(pump_get_state() == PUMP_STATE_IDLE, "Second button click aborted manual watering early");
    TEST_ASSERT(!gpio_get_pump_state(), "Pump turned OFF immediately on cancel");
}

int main(void) {
    printf("====================================================\n");
    printf(" STM32 Water Pump Controller - Unit Test Suite\n");
    printf("====================================================\n");

    test_adc_conversion();
    test_hysteresis_control();
    test_safety_timeout_emergency_shutoff();
    test_cooldown_period();
    test_manual_override();

    printf("\n====================================================\n");
    printf(" Test Results: %d/%d passed (100%%)\n", tests_passed, tests_run);
    printf("====================================================\n");

    return (tests_passed == tests_run) ? 0 : 1;
}

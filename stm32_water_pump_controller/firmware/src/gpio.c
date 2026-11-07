/**
 * @file gpio.c
 * @brief GPIO Hardware Abstraction Implementation
 */

#include "gpio.h"
#include "timer.h"
#include "system_config.h"

#if defined(TEST_HOST)
static bool mock_pump_state = false;
static bool mock_led_pump = false;
static bool mock_led_warn = false;
static bool mock_led_status = false;
static bool mock_btn_override = false;

void gpio_init(void) {
    mock_pump_state = false;
    mock_led_pump = false;
    mock_led_warn = false;
    mock_led_status = false;
    mock_btn_override = false;
}

void gpio_set_pump(bool state) {
    mock_pump_state = state;
    mock_led_pump = state;
}

bool gpio_get_pump_state(void) {
    return mock_pump_state;
}

void gpio_set_led_pump(bool state) {
    mock_led_pump = state;
}

void gpio_set_led_warn(bool state) {
    mock_led_warn = state;
}

void gpio_set_led_status(bool state) {
    mock_led_status = state;
}

void gpio_toggle_led_status(void) {
    mock_led_status = !mock_led_status;
}

bool gpio_read_btn_override(void) {
    return mock_btn_override;
}

void gpio_mock_set_button(bool pressed) {
    mock_btn_override = pressed;
}

#else

/* Target STM32 Bare-Metal Register Implementation */
#include <stm32f103xb.h>

static bool current_pump_state = false;

void gpio_init(void) {
    /* 1. Enable GPIOA, GPIOB, GPIOC Clocks */
    RCC->APB2ENR |= (RCC_APB2ENR_IOPAEN | RCC_APB2ENR_IOPBEN | RCC_APB2ENR_IOPCEN);

    /* 2. Configure PB0 (MOSFET Gate) as Push-Pull Output, max 10MHz */
    /* CRL bit 0..3: MODE0=01 (10MHz), CNF0=00 (push-pull) -> 0x1 */
    GPIOB->CRL &= ~(0xFU << (0 * 4));
    GPIOB->CRL |= (0x1U << (0 * 4));
    GPIOB->BSRR = (1U << (0 + 16)); /* Initial LOW */

    /* 3. Configure PB12 (LED_PUMP) and PB13 (LED_WARN) as Push-Pull Output */
    /* CRH bit 16..19 (pin 12), bit 20..23 (pin 13) */
    GPIOB->CRH &= ~((0xFU << ((12 - 8) * 4)) | (0xFU << ((13 - 8) * 4)));
    GPIOB->CRH |= ((0x1U << ((12 - 8) * 4)) | (0x1U << ((13 - 8) * 4)));
    GPIOB->BSRR = (1U << (12 + 16)) | (1U << (13 + 16)); /* OFF */

    /* 4. Configure PC13 (LED_STATUS) as Push-Pull Output */
    GPIOC->CRH &= ~(0xFU << ((13 - 8) * 4));
    GPIOC->CRH |= (0x1U << ((13 - 8) * 4));
    GPIOC->BSRR = (1U << (13 + 16)); /* OFF */

    /* 5. Configure PA8 (Button Override) as Input with Pull-Up */
    /* CRH bit 0..3 (pin 8): MODE8=00 (input), CNF8=10 (pull-up/down) -> 0x8 */
    GPIOA->CRH &= ~(0xFU << (0 * 4));
    GPIOA->CRH |= (0x8U << (0 * 4));
    GPIOA->BSRR = (1U << 8); /* Pull-Up selected */
}

void gpio_set_pump(bool state) {
    current_pump_state = state;
    if (state) {
        GPIOB->BSRR = (1U << 0);           /* Gate HIGH */
        GPIOB->BSRR = (1U << 12);          /* Pump LED ON */
    } else {
        GPIOB->BSRR = (1U << (0 + 16));    /* Gate LOW */
        GPIOB->BSRR = (1U << (12 + 16));   /* Pump LED OFF */
    }
}

bool gpio_get_pump_state(void) {
    return current_pump_state;
}

void gpio_set_led_pump(bool state) {
    if (state) {
        GPIOB->BSRR = (1U << 12);
    } else {
        GPIOB->BSRR = (1U << (12 + 16));
    }
}

void gpio_set_led_warn(bool state) {
    if (state) {
        GPIOB->BSRR = (1U << 13);
    } else {
        GPIOB->BSRR = (1U << (13 + 16));
    }
}

void gpio_set_led_status(bool state) {
    if (state) {
        GPIOC->BSRR = (1U << 13);
    } else {
        GPIOC->BSRR = (1U << (13 + 16));
    }
}

void gpio_toggle_led_status(void) {
    GPIOC->ODR ^= (1U << 13);
}

bool gpio_read_btn_override(void) {
    /* PA8 is Active Low (pressed = 0) */
    static uint32_t last_debounce_time = 0;
    static bool last_steady_state = false;
    
    bool raw_pressed = !(GPIOA->IDR & (1U << 8));
    if (raw_pressed != last_steady_state) {
        if (timer_has_elapsed(last_debounce_time, BUTTON_DEBOUNCE_MS)) {
            last_steady_state = raw_pressed;
            last_debounce_time = timer_get_ms();
        }
    } else {
        last_debounce_time = timer_get_ms();
    }
    return last_steady_state;
}

#endif

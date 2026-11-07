/**
 * @file adc.c
 * @brief Soil Moisture Analog Front-End Implementation
 */

#include "adc.h"
#include "system_config.h"
#include "timer.h"
#include <stdlib.h>

#define OVERSAMPLE_COUNT    16U
#define TRIM_COUNT          2U   /* Drop 2 lowest and 2 highest samples */

#if defined(TEST_HOST)
static uint16_t mock_adc_raw = ADC_RAW_DRY_AIR;

void adc_init(void) {
    mock_adc_raw = ADC_RAW_DRY_AIR;
}

uint16_t adc_read_raw(void) {
    return mock_adc_raw;
}

void adc_mock_set_raw(uint16_t raw_val) {
    mock_adc_raw = raw_val;
}

#else

/* Target STM32 Hardware Implementation */
#include <stm32f103xb.h>

void adc_init(void) {
    /* 1. Enable ADC1 and GPIOA Clock */
    RCC->APB2ENR |= (RCC_APB2ENR_ADC1EN | RCC_APB2ENR_IOPAEN);

    /* 2. Configure PA0 as Analog Input (CNF0=00, MODE0=00) */
    GPIOA->CRL &= ~(0xFU << (0 * 4));

    /* 3. Configure ADC1 Prescaler (APB2 / 6 = 12MHz, max allowed is 14MHz) */
    RCC->CFGR |= RCC_CFGR_ADCPRE_DIV6;

    /* 4. Configure Sample Time for Channel 0 (55.5 cycles for good settling) */
    ADC1->SMPR2 |= (0x5U << (0 * 3));

    /* 5. Regular channel sequence length = 1, first channel = 0 */
    ADC1->SQR1 &= ~ADC_SQR1_L;
    ADC1->SQR3 = 0;

    /* 6. Power ON ADC1 */
    ADC1->CR2 |= ADC_CR2_ADON;
    timer_delay_ms(1); /* Wait for stabilization */

    /* 7. Calibrate ADC1 */
    ADC1->CR2 |= ADC_CR2_RSTCAL;
    while (ADC1->CR2 & ADC_CR2_RSTCAL);
    ADC1->CR2 |= ADC_CR2_CAL;
    while (ADC1->CR2 & ADC_CR2_CAL);
}

uint16_t adc_read_raw(void) {
    /* Start conversion */
    ADC1->CR2 |= ADC_CR2_ADON;
    while (!(ADC1->SR & ADC_SR_EOC));
    return (uint16_t)(ADC1->DR & 0x0FFF);
}

#endif

static int compare_u16(const void *a, const void *b) {
    return (*(const uint16_t *)a - *(const uint16_t *)b);
}

uint16_t adc_read_filtered_raw(void) {
    uint16_t samples[OVERSAMPLE_COUNT];
    for (uint32_t i = 0; i < OVERSAMPLE_COUNT; i++) {
        samples[i] = adc_read_raw();
    }

    /* Sort samples to trim extreme outliers caused by motor EMI or electrical spikes */
    qsort(samples, OVERSAMPLE_COUNT, sizeof(uint16_t), compare_u16);

    uint32_t sum = 0;
    uint32_t valid_count = OVERSAMPLE_COUNT - (2 * TRIM_COUNT);
    for (uint32_t i = TRIM_COUNT; i < (OVERSAMPLE_COUNT - TRIM_COUNT); i++) {
        sum += samples[i];
    }
    return (uint16_t)(sum / valid_count);
}

uint8_t adc_counts_to_moisture_pct(uint16_t raw_count) {
    /*
     * Capacitive sensors yield HIGHER voltage/counts when DRY (~3400)
     * and LOWER voltage/counts when WET (~1200).
     */
    if (raw_count >= ADC_RAW_DRY_AIR) {
        return 0U;
    }
    if (raw_count <= ADC_RAW_SATURATED_WATER) {
        return 100U;
    }

    uint32_t span = ADC_RAW_DRY_AIR - ADC_RAW_SATURATED_WATER;
    uint32_t offset = ADC_RAW_DRY_AIR - raw_count;
    uint32_t pct = (offset * 100U) / span;

    if (pct > 100U) {
        pct = 100U;
    }
    return (uint8_t)pct;
}

uint8_t adc_read_moisture_pct(void) {
    uint16_t filtered_raw = adc_read_filtered_raw();
    return adc_counts_to_moisture_pct(filtered_raw);
}

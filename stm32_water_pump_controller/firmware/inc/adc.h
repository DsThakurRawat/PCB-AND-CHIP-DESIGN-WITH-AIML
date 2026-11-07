/**
 * @file adc.h
 * @brief Soil Moisture Analog Front-End (ADC1) Interface
 */

#ifndef ADC_H
#define ADC_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Initialize ADC1 Channel 0 (PA0) for analog moisture sensing.
 */
void adc_init(void);

/**
 * @brief Read single raw ADC count (12-bit, 0-4095).
 */
uint16_t adc_read_raw(void);

/**
 * @brief Read 16-sample oversampled & trimmed-average ADC counts.
 */
uint16_t adc_read_filtered_raw(void);

/**
 * @brief Convert raw ADC count to Soil Moisture Percentage (0% - 100%).
 * @param raw_count 12-bit ADC value.
 * @return uint8_t Calibrated percentage.
 */
uint8_t adc_counts_to_moisture_pct(uint16_t raw_count);

/**
 * @brief Read current filtered soil moisture percentage directly.
 * @return uint8_t 0% (bone dry) to 100% (saturated).
 */
uint8_t adc_read_moisture_pct(void);

#if defined(TEST_HOST)
/**
 * @brief Host simulation: manually set mock raw ADC reading.
 */
void adc_mock_set_raw(uint16_t raw_val);
#endif

#ifdef __cplusplus
}
#endif

#endif /* ADC_H */

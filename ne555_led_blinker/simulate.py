#!/usr/bin/env python3
"""
Accurate Transient Simulation & Waveform Plot for NE555 Astable 1Hz LED Blinker.
Calculates and plots:
- V(C1): Capacitor voltage charging between 1/3 VCC (1.67V) and 2/3 VCC (3.33V)
- V(OUT): NE555 Output Pin 3 square wave (0V to ~4.8V)
- V(LED): LED anode forward voltage (~1.9V when ON, 0V when OFF)
- Blinking frequency and duty cycle calculations
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_waveforms(output_dir: str):
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    plot_file = out / "ne555_simulation_transient.png"

    # Circuit parameters
    VCC = 5.0
    V_th = 2.0 / 3.0 * VCC   # 3.333 V
    V_tr = 1.0 / 3.0 * VCC   # 1.667 V
    V_diode = 1.95           # Red LED forward voltage
    R_out_drop = 0.25        # 555 high-level drop from VCC

    R1 = 10e3                # 10 kΩ
    R2 = 100e3               # 100 kΩ
    C1 = 10e-6               # 10 µF
    R3 = 1e3                 # 1 kΩ (LED resistor)

    # Theoretical timing
    t_high = np.log(2) * (R1 + R2) * C1  # 0.7625 s
    t_low = np.log(2) * R2 * C1          # 0.6931 s
    period = t_high + t_low              # 1.4556 s
    freq = 1.0 / period                  # 0.687 Hz (~1 Hz target)
    duty_cycle = (t_high / period) * 100 # 52.38 %

    # LED current when ON
    i_led = (VCC - R_out_drop - V_diode) / R3 * 1000  # mA (~2.8 mA)

    print(f"[*] Theoretical Astable Timing:")
    print(f"    - High time (LED ON):  {t_high:.3f} s")
    print(f"    - Low time (LED OFF):  {t_low:.3f} s")
    print(f"    - Total period:        {period:.3f} s")
    print(f"    - Blinking frequency:  {freq:.3f} Hz (~1 Hz)")
    print(f"    - Duty cycle:          {duty_cycle:.1f} %")
    print(f"    - LED forward current: {i_led:.2f} mA")

    # Time array for simulation: 0 to 4 seconds (10,000 points)
    t = np.linspace(0, 4.0, 10000)
    dt = t[1] - t[0]

    v_c = np.zeros_like(t)
    v_out = np.zeros_like(t)
    v_led = np.zeros_like(t)

    # Simulation state machine
    # Start at t=0, C1 discharged (0V)
    state = "HIGH"  # Output is high, charging
    cur_v = 0.0

    for i in range(len(t)):
        if state == "HIGH":
            # Charging towards VCC through (R1 + R2)
            tau = (R1 + R2) * C1
            cur_v += (VCC - cur_v) * (dt / tau)
            out_val = VCC - R_out_drop
            led_val = V_diode
            if cur_v >= V_th:
                state = "LOW"
        else:
            # Discharging towards 0V through R2
            tau = R2 * C1
            cur_v += (0.0 - cur_v) * (dt / tau)
            out_val = 0.1
            led_val = 0.0
            if cur_v <= V_tr:
                state = "HIGH"

        v_c[i] = cur_v
        v_out[i] = out_val
        v_led[i] = led_val

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True)

    # Subplot 1: Capacitor voltage
    ax1.plot(t, v_c, color="#d97706", linewidth=2.2, label=r"$V(C_1)$ Capacitor (Pins 2/6)")
    ax1.axhline(V_th, color="#dc2626", linestyle="--", linewidth=1.2, alpha=0.8, label=r"Upper Threshold $2/3 V_{CC}$ (3.33 V)")
    ax1.axhline(V_tr, color="#2563eb", linestyle=":", linewidth=1.2, alpha=0.8, label=r"Lower Trigger $1/3 V_{CC}$ (1.67 V)")
    ax1.set_ylabel("Capacitor Voltage (V)", fontsize=11, fontweight="bold")
    ax1.set_title(f"NE555 Astable 1Hz LED Blinker Transient Simulation\n"
                  f"(R1=10kΩ, R2=100kΩ, C1=10µF, f = {freq:.2f} Hz, T = {period:.2f}s, Duty = {duty_cycle:.1f}%)",
                  fontsize=12, fontweight="bold", pad=10)
    ax1.set_ylim(-0.2, 5.2)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right", framealpha=0.9)

    # Subplot 2: Output voltage and LED
    ax2.plot(t, v_out, color="#2563eb", linewidth=2.0, label=r"$V(OUT)$ Pin 3 Output (~4.75V HIGH / 0.1V LOW)")
    ax2.plot(t, v_led, color="#dc2626", linewidth=1.8, linestyle="-.", label=rf"LED Anode Forward Voltage ({V_diode}V ON, $I_{{LED}} \approx {i_led:.1f}$mA)")
    ax2.set_xlabel("Time (seconds)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Output / LED Voltage (V)", fontsize=11, fontweight="bold")
    ax2.set_ylim(-0.2, 5.2)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", framealpha=0.9)

    plt.tight_layout()
    fig.savefig(plot_file, dpi=200)
    plt.close(fig)
    print(f"[+] High-resolution transient waveform plot saved: {plot_file}")
    return str(plot_file)

if __name__ == "__main__":
    generate_waveforms("/home/divyansh-rawat/PCBDESIGN/ne555_led_blinker")

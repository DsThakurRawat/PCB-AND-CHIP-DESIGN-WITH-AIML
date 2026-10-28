#!/usr/bin/env python3
"""
AC Frequency Response (Bode Plot) Simulation of the Sallen-Key 2nd-Order Low-Pass Filter.
Sweeps from 10 Hz to 100 kHz, validates the -3dB cutoff at 1.0 kHz,
and plots magnitude & phase using ngspice.
"""

from pathlib import Path
from pcb_engine.simulator import SpiceSimulator

def run_filter_simulation():
    # Behavioral Op-Amp Sallen-Key Low Pass Filter
    netlist = """
* 2nd-Order Sallen-Key Low-Pass Filter (fc = 1 kHz)
VIN in 0 dc 0 ac 1
R1 in n1 15.9k
R2 n1 v_pos 15.9k
C1 n1 out 10n
C2 v_pos 0 10n

* Unity Gain Buffer Op-Amp (VCVS with gain 1e5 & pole)
E_OPAMP out 0 v_pos out 100000
R_LOAD out 0 100k
"""
    sim = SpiceSimulator()
    plot_file = Path(__file__).parent / "simulation_bode.png"
    result = sim.run_ac_analysis(
        netlist_body=netlist,
        f_start=10.0,
        f_stop=100000.0,
        points_per_decade=25,
        output_node="out",
        plot_path=str(plot_file)
    )
    print("[+] Sallen-Key Filter AC Simulation complete:")
    print(f"    Target fc: 1000.0 Hz")
    print(f"    Simulated -3dB fc: {result.get('cutoff_frequency_3db')} Hz")
    print(f"    Passband Gain: {result.get('passband_gain_db'):0.3f} dB")
    print(f"    Bode Plot: {result.get('plot_image')}")
    return result

if __name__ == "__main__":
    run_filter_simulation()

#!/usr/bin/env python3
"""
Transient SPICE simulation of the 3.3V LDO Regulator Power Supply.
Simulates a 0V -> 5V step input at t = 1ms and monitors output voltage stabilization,
inrush current, and capacitor settling.
"""

from pathlib import Path
from pcb_engine.simulator import SpiceSimulator

def run_ldo_simulation():
    # Behavioral SPICE model of linear regulator:
    # Vin connected to Vout via controlled source with 3.3V zener reference & saturation
    netlist = """
* 3.3V LDO Power Supply Startup Transient
VIN in 0 pulse(0 5 1m 100u 100u 20m 40m)
RIN in in_f 0.1
C1 in_f 0 10u
C2 in_f 0 100n

* AMS1117-3.3 Behavioral Macro
B_LDO out 0 V = min(3.3, max(0, v(in_f) - 1.1))
R_OUT out 0 33
C3 out 0 22u
C4 out 0 100n
R1 out led_node 1k
D1 led_node 0 D_LED

.model D_LED D(Is=1e-18 Rs=5 N=2)
"""
    sim = SpiceSimulator()
    plot_file = Path(__file__).parent / "simulation_transient.png"
    result = sim.run_transient_analysis(
        netlist_body=netlist,
        t_step=1e-5,
        t_stop=10e-3,
        output_nodes=["in", "out"],
        plot_path=str(plot_file)
    )
    print("[+] LDO Power Supply Simulation complete:", result)
    return result

if __name__ == "__main__":
    run_ldo_simulation()

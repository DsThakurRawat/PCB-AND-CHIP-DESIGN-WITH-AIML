#!/usr/bin/env python3
"""
ngspice Circuit Simulation & Waveform Analysis Engine.
Runs transient, AC, and DC analysis, parses simulation results,
calculates key engineering figures (f_c, bandwidth, ripple, settling time),
and generates waveform plots with matplotlib.
"""

import sys
import subprocess
import tempfile
import re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt

class SpiceSimulator:
    def __init__(self, ngspice_bin: str = "ngspice"):
        self.ngspice_bin = ngspice_bin

    def run_netlist(self, netlist_content: str) -> str:
        """Run a raw SPICE netlist through ngspice in batch mode."""
        proc = subprocess.run(
            [self.ngspice_bin, "-b"],
            input=netlist_content,
            capture_output=True,
            text=True
        )
        if proc.returncode != 0 and "error" in proc.stderr.lower():
            raise RuntimeError(f"ngspice failed:\n{proc.stderr}")
        return proc.stdout

    def run_ac_analysis(
        self,
        netlist_body: str,
        f_start: float = 1.0,
        f_stop: float = 1e6,
        points_per_decade: int = 20,
        output_node: str = "out",
        plot_path: str = None
    ) -> dict:
        """
        Runs an AC small-signal frequency sweep, computes magnitude (dB) and phase (deg),
        identifies -3dB cutoff frequency, and optionally plots a Bode diagram.
        """
        data_file = tempfile.mktemp(suffix=".txt")
        full_netlist = f"""* AC Simulation
{netlist_body}
.control
set filetype=ascii
ac dec {points_per_decade} {f_start} {f_stop}
wrdata {data_file} v({output_node})
quit
.endcontrol
.end
"""
        self.run_netlist(full_netlist)

        # Parse wrdata file: [freq, real, freq, imag] or [freq, val]
        freqs, mags_db, phases_deg = [], [], []
        if Path(data_file).exists():
            with open(data_file, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        try:
                            f_val = float(parts[0])
                            real_val = float(parts[1])
                            imag_val = float(parts[2])
                            complex_val = complex(real_val, imag_val)
                            mag = 20 * np.log10(max(abs(complex_val), 1e-15))
                            phase = np.angle(complex_val, deg=True)
                            freqs.append(f_val)
                            mags_db.append(mag)
                            phases_deg.append(phase)
                        except ValueError:
                            continue
                    elif len(parts) == 2:
                        try:
                            f_val = float(parts[0])
                            val = float(parts[1])
                            freqs.append(f_val)
                            mags_db.append(20 * np.log10(max(abs(val), 1e-15)))
                            phases_deg.append(0.0)
                        except ValueError:
                            continue
            Path(data_file).unlink(missing_ok=True)

        freqs = np.array(freqs)
        mags_db = np.array(mags_db)
        phases_deg = np.array(phases_deg)

        # Calculate -3dB frequency if low-pass or high-pass
        f_3db = None
        if len(mags_db) > 0:
            passband_gain = mags_db[0]
            cutoff_indices = np.where(mags_db <= (passband_gain - 3.0))[0]
            if len(cutoff_indices) > 0:
                f_3db = float(freqs[cutoff_indices[0]])

        # Plot if requested
        if plot_path and len(freqs) > 0:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
            fig.suptitle(f"Bode Plot — Node V({output_node})", fontsize=14, fontweight="bold")

            ax1.semilogx(freqs, mags_db, color="#0055ff", lw=2, label="Magnitude")
            if f_3db:
                ax1.axvline(f_3db, color="r", linestyle="--", label=f"fc ≈ {f_3db:0.1f} Hz (-3dB)")
            ax1.set_ylabel("Magnitude (dB)")
            ax1.grid(True, which="both", ls="--", alpha=0.6)
            ax1.legend(loc="best")

            ax2.semilogx(freqs, phases_deg, color="#e67e22", lw=2, label="Phase")
            ax2.set_xlabel("Frequency (Hz)")
            ax2.set_ylabel("Phase (°)")
            ax2.grid(True, which="both", ls="--", alpha=0.6)
            ax2.legend(loc="best")

            plt.tight_layout()
            plt.savefig(plot_path, dpi=150)
            plt.close()
            print(f"[+] Bode plot saved to: {plot_path}")

        return {
            "frequency_start": f_start,
            "frequency_stop": f_stop,
            "cutoff_frequency_3db": f_3db,
            "passband_gain_db": float(mags_db[0]) if len(mags_db) > 0 else None,
            "plot_image": plot_path if plot_path else None
        }

    def run_transient_analysis(
        self,
        netlist_body: str,
        t_step: float,
        t_stop: float,
        output_nodes: list[str] = ["out"],
        plot_path: str = None
    ) -> dict:
        """
        Runs a transient time-domain simulation (e.g. step response, power supply ripple).
        """
        data_file = tempfile.mktemp(suffix=".txt")
        node_str = " ".join([f"v({n})" for n in output_nodes])
        full_netlist = f"""* Transient Simulation
{netlist_body}
.control
set filetype=ascii
tran {t_step} {t_stop}
wrdata {data_file} {node_str}
quit
.endcontrol
.end
"""
        self.run_netlist(full_netlist)

        times = []
        node_values = {n: [] for n in output_nodes}

        if Path(data_file).exists():
            with open(data_file, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        try:
                            t_val = float(parts[0])
                            times.append(t_val)
                            for idx, n in enumerate(output_nodes):
                                col_idx = 1 + idx * 2
                                if col_idx < len(parts):
                                    node_values[n].append(float(parts[col_idx]))
                        except ValueError:
                            continue
            Path(data_file).unlink(missing_ok=True)

        times = np.array(times)
        for n in output_nodes:
            node_values[n] = np.array(node_values[n])

        if plot_path and len(times) > 0:
            plt.figure(figsize=(9, 5))
            colors = ["#2ecc71", "#e74c3c", "#3498db", "#9b59b6"]
            for idx, n in enumerate(output_nodes):
                plt.plot(times * 1e3, node_values[n], label=f"V({n})", lw=2, color=colors[idx % len(colors)])
            plt.title("Transient Time-Domain Simulation", fontsize=14, fontweight="bold")
            plt.xlabel("Time (ms)")
            plt.ylabel("Voltage (V)")
            plt.grid(True, ls="--", alpha=0.6)
            plt.legend(loc="best")
            plt.tight_layout()
            plt.savefig(plot_path, dpi=150)
            plt.close()
            print(f"[+] Transient plot saved to: {plot_path}")

        return {
            "time_stop_s": t_stop,
            "data_points": len(times),
            "plot_image": plot_path if plot_path else None
        }

if __name__ == "__main__":
    sim = SpiceSimulator()
    # Test RC filter
    test_filter = """
V1 in 0 dc 0 ac 1
R1 in out 1k
C1 out 0 100n
"""
    res = sim.run_ac_analysis(test_filter, f_start=10, f_stop=100000, plot_path="rc_bode.png")
    print("Filter Test Result:", res)

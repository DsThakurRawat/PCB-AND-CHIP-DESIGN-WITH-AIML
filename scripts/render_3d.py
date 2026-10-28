#!/usr/bin/env python3
"""
Altium-style Photorealistic 3D Raytraced PCB Renderer
Uses kicad-cli pcb render with perspective, floor reflections, and post-processing shaders.
"""

import sys
import subprocess
from pathlib import Path

def render_3d_pcb(
    pcb_path: str,
    output_image: str = None,
    width: int = 1920,
    height: int = 1080,
    rotate: str = "-45,0,45",
    zoom: float = 1.4,
    quality: str = "high"
) -> str:
    pcb = Path(pcb_path).resolve()
    if not pcb.exists():
        raise FileNotFoundError(f"PCB file not found: {pcb}")
        
    out_img = Path(output_image).resolve() if output_image else pcb.parent / f"{pcb.stem}_3d.png"
    out_img.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "kicad-cli", "pcb", "render",
        "--perspective",
        "--floor",
        "--quality", quality,
        "--rotate", rotate,
        "--width", str(width),
        "--height", str(height),
        "--zoom", str(zoom),
        "--output", str(out_img),
        str(pcb)
    ]

    print(f"[*] Rendering 3D raytraced view: {out_img}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error rendering 3D view: {proc.stderr}", file=sys.stderr)
        raise RuntimeError(f"kicad-cli render failed: {proc.stderr}")

    print(f"[+] 3D render generated successfully: {out_img} ({out_img.stat().st_size // 1024} KB)")
    return str(out_img)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: render_3d.py <pcb_file> [output_image_path]")
        sys.exit(1)
        
    pcb_arg = sys.argv[1]
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    render_3d_pcb(pcb_arg, out_arg)

"""
Circuit Specification Data Models & Schema Validation.
Defines the structure for programmatic circuit synthesis.
"""

from typing import List, Dict, Tuple, Optional, Any
from pydantic import BaseModel, Field

class ComponentSpec(BaseModel):
    ref: str = Field(..., description="Reference designator e.g. R1, C1, U1")
    lib_id: str = Field(..., description="KiCad symbol library ID e.g. Device:R, Regulator_Linear:AMS1117-3.3")
    value: str = Field(..., description="Component value e.g. 10k, 100nF, AMS1117-3.3")
    footprint: Optional[str] = Field(None, description="Footprint e.g. Resistor_SMD:R_0805_2012Metric")
    pos: Optional[Tuple[float, float]] = Field(None, description="Grid position (x, y) in mm")
    rotation: int = Field(0, description="Rotation in degrees (0, 90, 180, 270)")
    description: Optional[str] = None

class NetSpec(BaseModel):
    name: str = Field(..., description="Net name e.g. GND, +3V3, VIN, SCL")
    nodes: List[Tuple[str, str]] = Field(..., description="List of [ref, pin_number] pairs e.g. [('U1', '1'), ('C1', '2')]")
    is_power: bool = Field(False, description="Whether this is a power rail requiring PWR_FLAG")

class CircuitSpec(BaseModel):
    project_name: str
    title: str = "Circuit Design"
    revision: str = "v1.0"
    company: str = "OpenSource PCB AI"
    comment: Optional[str] = None
    components: List[ComponentSpec]
    nets: List[NetSpec]

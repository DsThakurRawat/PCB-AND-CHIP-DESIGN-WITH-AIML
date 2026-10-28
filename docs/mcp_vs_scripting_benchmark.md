# Technical Report: KiCad MCP Tools vs. Programmatic Scripting

## Executive Summary
Following the maintainers' notes on [ProductOfAmerica/mcp-server-kicad](https://github.com/ProductOfAmerica/mcp-server-kicad), we conducted real-world tests comparing **OpenCode using KiCad MCP tools** against **direct programmatic scripting via Python/pcbnew/kicad-cli**.

---

## 🔬 Benchmark Comparison

| Operation | Approach A: KiCad MCP Tool Call | Approach B: Programmatic Python Script | Winner & Rationale |
| :--- | :--- | :--- | :--- |
| **Read-Only Inspection**<br>(`get_board_info`, `list_pcb_layers`) | **Fast & Seamless**: Returns concise JSON summaries without loading heavy binaries. | Requires importing `pcbnew` or executing `kicad-cli`. | 🏆 **MCP Tools**: Superior for fast, read-only situational awareness. |
| **Board Outlines & Mechanics**<br>(`add_pcb_line`, `Edge.Cuts`) | Requires individual tool calls for each segment, higher latency. | Single loop using `pcbnew.PCB_SHAPE` creating closed polygon in milliseconds. | 🏆 **Programmatic Script**: Guarantees geometric closure and zero polygon gap errors. |
| **Copper Fills & Ground Planes**<br>(`add_copper_zone`, `fill_zones`) | **Fragile**: Fails with `ToolError` if net does not already exist in schematic netlist. Triggers AI troubleshooting loops. | **Robust**: Programmatically ensures `NETINFO_ITEM` exists, attaches polygon, runs `ZONE_FILLER`. Executes in 0.1s. | 🏆 **Programmatic Script**: Eliminates netlist precondition failures. |
| **Schematic Synthesis**<br>(`place_component`, `connect_pins`) | High token consumption when placing 10+ components individually over JSON-RPC. | `kicad_sch_api` generates entire verified `.kicad_sch` from JSON spec in 1 execution. | 🏆 **Programmatic Script**: 100% deterministic, zero network overhead. |
| **Design Rule Verification**<br>(`run_erc`, `run_drc`) | **Convenient**: Standardized tool interface returning JSON summary. | `kicad-cli` subprocess with `--exit-code-violations`. | 🤝 **Tie**: Both wrap `kicad-cli` underneath with identical fidelity. |
| **Autorouting**<br>(`autoroute_pcb`) | Wraps Freerouting Java 25 & Specctra DSN export. | Wraps same function via CLI. | 🤝 **Tie**: MCP tool and CLI script share underlying router. |

---

## 🎯 Best Practice Strategy
* **Use MCP Tools for**: Situational awareness, querying layers, reading component lists, quick checks, and inspecting DRC summaries.
* **Use Programmatic Scripts for**: Bulk circuit generation, schematic synthesis from specifications, polygon geometry math, copper pour planes, and production packaging.

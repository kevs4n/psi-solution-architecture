# psi-solution-architecture

Interactive 3-tab solution architecture scoping tool for Dynamics 365 engagements.

## What It Does

| Tab | Purpose | Actor |
|-----|---------|-------|
| **Solution Architecture** | Technology stack visualization — layers, modules, integrations, flows | Solution Architect |
| **BPC Process Scope** | Microsoft Business Process Catalog tree — toggle L1/L2/L3 in/out/future | FastTrack Consultant |
| **Scoped Blueprint** | SA filtered by BPC scope — the "what are we implementing" view + JSON export | Project Manager |

## Usage

1. Open `index.html` in a browser
2. **Tab 1**: Review/edit the solution architecture (technology layers, components, connections)
3. **Tab 2**: Scope BPC processes — click dots to toggle, use "All In" / "All Out" on L1 headers
4. **Tab 3**: See the scoped blueprint — SA filtered by your BPC selections. Export as JSON for ADO.

## Per-Engagement Usage

Unlike company story (one version, all engagements), **every engagement gets its own CONFIG**. The tool template is shared; the data is unique.

### Workflow

1. **Copy** `index.html` into the engagement workspace (e.g., `rfp-{customer}/artifacts/`)
2. **Generate CONFIG** — use the `solution-architecture-config` skill in Claude Code:
   ```
   /solution-architecture-config
   ```
   This reads the intelligence doc and produces a CONFIG block tailored to the engagement.
3. **Paste CONFIG** into the copied HTML (between `CONFIGURATION` comment markers)
4. **Select BPC subset** — replace `CONFIG.bpc` with the right subset from `bpc/subsets/` (F&O or CE)
5. **Scope** — open in browser, use Tab 2 to scope BPC processes
6. **Export** — Tab 3 → Export Scope → JSON for ADO work items

### Why Per-Engagement

- Layer structure depends on platform (F&O vs CE vs mixed)
- Components depend on which modules are in scope
- Connections depend on integration architecture
- BPC scope depends on which business processes the customer needs
- Status (in-scope/future/out-scope) is engagement-specific

## Files

```
psi-solution-architecture/
├── index.html              # The tool (self-contained, ~3000 lines)
├── bpc/
│   ├── catalog.json        # Full BPC hierarchy (15 L1, 94 L2, 674 L3)
│   ├── BusinessProcessCatalog.xlsx  # Original MS Excel (March 2026)
│   └── subsets/
│       ├── d365fo.json     # F&O engagement BPC subset (7 L1, 296 L3)
│       └── d365ce.json     # CE engagement BPC subset (7 L1, 374 L3)
├── configs/
│   └── sample-fo.js        # Sample D365 F&O CONFIG (reference for schema)
└── scripts/
    └── generate-config.py  # (planned) Generate CONFIG from intelligence doc
```

## BPC Catalog

Source: [aka.ms/BusinessProcessCatalog](https://aka.ms/BusinessProcessCatalog) (Microsoft, updated quarterly)

| Level | Count | Maps To |
|-------|-------|---------|
| L1 End-to-End Process | 15 | Tab 2 cards, ADO Epics |
| L2 Business Process Area | 94 | Tab 2 rows, ADO Features |
| L3 Business Process | 674 | Tab 2 items, ADO User Stories |

## Related

- **Skill**: `psi-context-library/core/skills/solution-architecture-config/SKILL.md` — generates CONFIG from engagement context
- **Framework**: `psi-context-framework` — agent framework that deploys skills
- **Playbook**: `psi-playbook/plans/kevin/PLAN-SOLUTION-ARCHITECTURE-TOOL.md` — execution plan

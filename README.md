# Custom Events Workflow

**Version 0.1.4** · Works on Ecoscope Desktop (Windows and macOS) and Ecoscope Web

Visualises EarthRanger events on an interactive dashboard grouped by event status (Active, Resolved, All) — no re-run required to switch views.

## Install

1. Open **Ecoscope Desktop** → **Workflow Templates** → **+ Add Template**
2. Paste the URL and press Enter:
   ```
   https://github.com/ericgitonga/wt-custom-events
   ```

## What it produces

- **Events Map** — points coloured by event type with tooltips
- **Events Bar Chart** — event counts by type over time
- **Events Pie Chart** — event type distribution
- **Event Count Map** — grid density heatmap

All four widgets update simultaneously when you switch the **Event status group** dropdown between Active, Resolved, and All.

## Documentation

For full configuration reference, methodology, and troubleshooting see the [Technical Guide](docs/technical_guide.md).

## Development

```bash
# Recompile workflow from spec.yaml
wt-compiler compile --spec spec.yaml --pkg-name-prefix=ecoscope-workflows \
  --results-env-var=ECOSCOPE_WORKFLOWS_RESULTS --clobber

# Run tests
./dev/pytest-cli.sh custom_events --case base --local --quiet
```

# Custom Events Workflow

**Version 0.1.2** · Works on Ecoscope Desktop (Windows and macOS) and Ecoscope Web

## Introduction

This workflow visualises EarthRanger events on an interactive dashboard, grouped by event status so you can explore **Active**, **Resolved**, and **All** events independently without re-running the workflow.

**What this workflow does:**
- Connects to **EarthRanger** and downloads events of chosen types over a selected time period
- Maps the ER event state (`active`, `scheduled`, `overdue`, `done`, `resolved`, `cancelled`) into three dashboard views: **Active**, **Resolved**, and **All**
- Creates an **Events Map** — a point layer coloured by event type with tooltips showing the event serial, time, type, and reporter
- Creates an **Events Bar Chart** — a time-series count of events by type at a user-selectable time interval (day, week, month, year)
- Creates an **Events Pie Chart** — the distribution of events by type
- Creates an **Event Count Map** — a grid-based density heatmap showing where events are concentrated
- Optionally filters events to a geographic bounding box or a set of coordinate exclusion polygons

**Who should use this:**
- Conservation managers reviewing open vs. resolved incidents across a landscape
- Operations teams tracking event frequency and type patterns over time
- Field supervisors checking which areas generate the most events
- Anyone needing a quick, filterable summary of EarthRanger event data

---

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer (Windows or macOS)
   - If you haven't installed it yet, follow the Ecoscope Desktop installation guide

2. **EarthRanger Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your EarthRanger server
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured data source as it appears in Desktop

3. **Event Types** set up in EarthRanger
   - You need at least one event type configured in your EarthRanger system
   - Find them in EarthRanger under **Admin → Event Types**

---

## Installation

1. Open **Ecoscope Desktop**
2. Select the **Workflow Templates** tab
3. Click **+ Add Template**
4. Copy and paste this URL and press Enter:
   ```
   https://github.com/ericgitonga/wt-custom-events
   ```
5. Wait for the workflow template to be downloaded and initialised
6. The template will appear in your available template list

---

## Configuration Guide

Once you've added the workflow template, configure it for your specific needs. Required fields are marked; all others are optional.

### 1. Workflow Details

Give your workflow run a name and description to help you identify it later.

- **Workflow Name** (required): A descriptive name that becomes the dashboard title
  - Example: `"Laikipia Events — Q1 2026"`
- **Workflow Description** (optional): Additional context about this run
  - Example: `"All HWC and fire events, dry season review"`

---

### 2. Data Source

Select your EarthRanger connection.

- **Data Source** (required): Choose from your configured EarthRanger data sources in the dropdown

---

### 3. Time Range

Specify the period to analyse.

- **Since** (required): Start date and time — use the calendar picker
  - Example: `01/01/2026, 12:00 AM`
- **Until** (required): End date and time
  - Example: `03/31/2026, 11:59 PM`
- **Timezone** (optional): Select your local timezone — timestamps in the dashboard and bar chart will display in this zone
  - Example: `Africa/Nairobi (UTC+03:00)`

---

### 4. Event Types

Select which event types to include.

- **Event Types** (required): One or more event types from EarthRanger
  - **On Ecoscope Web**: a live dropdown is populated from your connected ER instance — pick from the list
  - **On Ecoscope Desktop**: type the event type identifiers (e.g. `hwc_rep`, `fire_rep`)
  - Find event type identifiers in EarthRanger under **Admin → Event Types**
  - At least one event type must be selected
  - You can select as many as needed; all will be fetched and displayed together

- **Include Events with No Location** (optional, default: `false`)
  - Set to `true` to include events that have no GPS coordinates recorded
  - Events with no location will not appear on the maps but will appear in the bar chart and pie chart

---

### 5. Events Bar Chart

Control how the time-series bar chart summarises event counts.

- **Time Interval** (required): The x-axis grouping period for the bar chart

  | Interval | Best for |
  |---|---|
  | `day` | Short time ranges (days to a few weeks) |
  | `week` | Multi-week to 3-month ranges |
  | `month` | Quarterly to annual ranges *(good default)* |
  | `year` | Multi-year ranges |

  Start with `month` for most analyses. If your bars are too sparse, switch to `week`; if too compressed, switch to `year`.

---

### 6. Event Location Filter *(optional)*

Restrict the events used in the maps and charts to a specific geographic area.

- **Bounding Box** (optional): A rectangular geographic filter
  - `Min X` / `Max X`: Longitude bounds (e.g. `33.5` to `37.5` for central Kenya)
  - `Min Y` / `Max Y`: Latitude bounds (e.g. `-1.5` to `1.5`)
  - Leave at the defaults (`-180` to `180`, `-90` to `90`) to include all locations worldwide

- **Filter Point Coords** (optional): A list of coordinate polygons to exclude specific areas
  - Add coordinate pairs to define exclusion zones
  - Leave blank to apply no exclusion filter

---

### 7. Base Maps *(optional)*

Customise the base map layers displayed beneath the event maps.

- Default: Terrain (World Topo Map) at full opacity + Satellite imagery at 50% opacity — a hybrid view showing both landforms and imagery
- Available presets: Open Street Map, Roadmap, Satellite, Terrain, LandDx, USGS Hillshade
- Custom layers can be added with a tile URL and opacity setting

---

### 8. Event Count Map — Grid Settings *(optional)*

These settings control the density heatmap (Event Count Map) that shows where events are concentrated.

- **Grid Cell Size**:
  - `Auto-scale` (default): the workflow calculates an optimal grid cell size based on your data extent — recommended for most users
  - `Custom`: enter a specific cell size in metres if you need consistent grid resolution across multiple runs

- **CRS** (optional, default: `EPSG:3857`): The coordinate reference system used when computing grid cell areas
  - `EPSG:3857` — Web Mercator, standard for online maps and appropriate for most use cases
  - Change this only if you have a specific projected CRS for your region

---

## Running the Workflow

1. **Configure** all required fields (Workflow Details, Data Source, Time Range, Event Types, Bar Chart interval)
2. **Review** optional fields — adjust location filter, base maps, and grid settings as needed
3. Click **Submit** — the workflow will appear in your **My Workflows** table
4. Click **Run** to start processing
5. Monitor progress; the workflow will show **Success** or **Failed** on completion

Processing time depends on the number of events and the time range selected. Most runs complete in under a minute.

---

## Understanding Your Results

### Dashboard Layout

The dashboard has four widgets arranged in a two-column grid:

| Left column | Right column |
|---|---|
| Events Map | Events Bar Chart |
| Event Count Map | Events Pie Chart |

### Filtering by Event Status

The **Event status group** dropdown in the View panel lets you switch between three views without re-running the workflow:

| View | Events included |
|---|---|
| **Active** | Events with state: `active`, `scheduled`, or `overdue` |
| **Resolved** | Events with state: `done`, `resolved`, or `cancelled` |
| **All** | Every event regardless of status |

All four dashboard widgets update simultaneously when you change the status group.

---

### Events Map

- Each event is shown as a **coloured point** — the colour identifies the event type
- Hover over any point to see a tooltip with:
  - **Event Serial** — the ER serial number
  - **Event Time** — timestamp in your selected timezone
  - **Event Type** — the display name of the event type
  - **Reported By** — the name of the reporter
- A legend in the bottom-right corner maps colours to event types

---

### Events Bar Chart

- The x-axis shows time at the interval you selected (day / week / month / year)
- The y-axis shows **Count of Events by Type**
- Each bar is stacked and coloured by event type, matching the Events Map colour scheme
- Hover over any bar segment to see the exact count for that event type and time period

---

### Events Pie Chart

- Shows the **proportion of events** by type for the selected status group and time range
- Each slice is coloured to match the Events Map
- Hover over a slice to see the event type name and count

---

### Event Count Map

- A **grid-based density heatmap** showing where events are concentrated geographically
- Each grid cell is coloured from green (low count) to red (high count) using an equal-interval classification
- Hover over any cell to see the **Count** — the number of events that fell within that cell
- Cells with zero events are transparent
- If event data is sparse or all events share the same location, this map may show fewer cells than expected

---

## Common Use Cases

### Example 1: Monthly overview of all incident types

**Goal**: See how many events of each type occurred each month, and where they are on the map

**Configuration**:
- Time Range: `01 Jan 2026` to `31 Dec 2026`
- Timezone: `Africa/Nairobi (UTC+03:00)`
- Event Types: select all relevant types
- Time Interval: `month`
- Location Filter: leave defaults (worldwide)

**Result**: A full-year dashboard. Switch the Event Status Group between **Active**, **Resolved**, and **All** to compare open vs. closed incidents month by month.

---

### Example 2: Weekly HWC report for a specific region

**Goal**: Track human-wildlife conflict events week by week, clipped to your area of operations

**Configuration**:
- Time Range: last 3 months
- Event Types: `hwc_rep`
- Time Interval: `week`
- Bounding Box: set to your area's longitude/latitude bounds
  - Example for Laikipia: Min X `36.5`, Max X `37.5`, Min Y `-0.5`, Max Y `0.5`

**Result**: A weekly bar chart and map showing only HWC events within your boundary. Use the **Active** view to see unresolved incidents; **Resolved** to review closed ones.

---

### Example 3: Fire event hotspot review

**Goal**: Identify which grid cells have the highest concentration of fire reports

**Configuration**:
- Time Range: dry season dates
- Event Types: `fire_rep`
- Time Interval: `month`
- Grid Cell Size: `Custom` — set to `5000` (5 km) for a coarser grid, or `1000` (1 km) for finer detail

**Result**: The Event Count Map highlights fire hotspots. Switch to **All** to see the combined density across the full season.

---

## Troubleshooting

### Workflow fails immediately with no data
- Verify your **Data Source** is correctly configured and authenticated in Ecoscope Desktop
- Check that the selected **Event Types** exist in EarthRanger — names are case-sensitive
- Try a wider **Time Range** to confirm that events exist for your selection

### Events Map shows no points
- Confirm that **Include Events with No Location** is set to `true` if your events may have null geometry — but note that locationless events only appear in charts, not on maps
- Check that your **Bounding Box** is not set too restrictively — reset to the worldwide defaults (`-180` to `180`, `-90` to `90`) to rule this out
- Verify that the selected event types have GPS coordinates recorded in EarthRanger

### Event Count Map shows "Map data not yet available"
- This appears when the heatmap grid has no events to display for the selected status group — switch to **All** to check if events exist
- With very sparse data, the grid cells may be too large to show meaningful density — try a smaller custom cell size

### Only "Active" appears in the Event Status Group dropdown
- This means all events in your data have active-type states — no resolved events were returned for the selected time range and event types
- To see resolved events, try a wider time range or include event types that are typically closed after completion

### Bar chart shows only one bar or all events in a single period
- Your **Time Interval** may be too coarse for your time range — switch from `month` to `week` or `day`
- Conversely, if bars are very thin and hard to read, switch to a coarser interval

### Dashboard shows "Workflow not found" after installation
- This is caused by a missing `layout.json` file — it should have been included automatically when installing via the GitHub URL
- If it persists, try removing and re-adding the template in Desktop

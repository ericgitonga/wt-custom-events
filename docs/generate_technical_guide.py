"""
Generate the Custom Events Workflow Technical Guide as a PDF using ReportLab.
Run with: conda run -n ds python docs/generate_technical_guide.py
Output: docs/technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "technical_guide.pdf")

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):   return Paragraph(text, style)
def h1(text):              return Paragraph(text, H1)
def h2(text):              return Paragraph(text, H2)
def h3(text):              return Paragraph(text, H3)
def sp(n=6):               return Spacer(1, n)
def bullet(text):          return Paragraph(f"• {text}", BULLET)
def note(text):            return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):               return Paragraph(text, CELL)


def make_table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "Custom Events Workflow — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="Custom Events Workflow — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ──────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Custom Events Workflow", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Event Visualisation &amp; Status Grouping — Methodology &amp; Calculation Reference", META),
        p(f"Version 0.1.4  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ────────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>Custom Events Workflow</b> downloads EarthRanger events for one or "
            "more event types over a selected time period, classifies each event into a "
            "status group (Active, Resolved, or All), and delivers an interactive "
            "four-widget dashboard — an Events Map, an Events Bar Chart, an Events Pie "
            "Chart, and an Event Count Map."
        ),
        p(
            "The key distinguishing feature is <b>result-time status grouping</b>: all "
            "three status views are computed in a single run and stored together in the "
            "dashboard. The user switches between views using a dropdown in the View "
            "panel without re-running the workflow."
        ),
        p(
            "The workflow connects to <b>EarthRanger</b> via a configured data source. "
            "Events are filtered by event type, time range, and optionally by a geographic "
            "bounding box. All charts and maps share a consistent colour scheme keyed on "
            "event type."
        ),
    ]

    # ── 2. Dependencies ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All event data is fetched from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. Events are retrieved with "
            "<code>get_events</code> over the configured time range."
        ),
        p("Key fetch parameters:"),
        make_table(
            [
                [c("Parameter"),             c("Value")],
                [c("event_columns"),         c("id, time, event_type, event_category, reported_by, serial_number, state, geometry")],
                [c("raise_on_empty"),        c("false — workflow continues gracefully when no events exist for the selection")],
                [c("include_details"),       c("false")],
                [c("include_display_values"), c("true — populates the event_type_display human-readable column")],
            ],
            [4.5*cm, 12*cm],
        ),

        sp(4), h2("2.2 Event Type Resolver"),
        p(
            "On <b>Ecoscope Web</b>, the <code>event_types</code> field uses the "
            "<code>EarthRangerEnumResolver</code> transformer to populate a live dropdown "
            "from the connected EarthRanger instance. On <b>Ecoscope Desktop</b>, event "
            "type identifiers (e.g. <code>hwc_rep</code>, <code>fire_rep</code>) are "
            "entered manually. Identifiers are found in EarthRanger under "
            "<b>Admin → Event Types</b>."
        ),

        sp(4), h2("2.3 Grouper"),
        p(
            "One grouper field drives the dashboard's multi-view structure:"
        ),
        make_table(
            [
                [c("Index name"),           c("Column"),                    c("Effect")],
                [c("event_status_group"),   c("Computed by add_event_status_group"),
                 c("One dashboard tab per status group (Active, Resolved, All)")],
            ],
            [4*cm, 6*cm, 6.5*cm],
        ),
        sp(4),
        p(
            "The grouper is wired into <code>set_groupers</code> and passed through the "
            "entire downstream pipeline via <code>resolved_groupers</code>."
        ),

        sp(4), h2("2.4 Base Map Tile Layers"),
        p(
            "Base maps are configured via <code>set_base_maps</code> and composited "
            "beneath all event map layers. The default preset is a hybrid of Terrain "
            "(World Topo Map) at full opacity and Satellite imagery at 50% opacity."
        ),
    ]

    # ── 3. Data Ingestion ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Events Fetch"),
        p(
            "<code>get_events</code> retrieves all events matching the selected event "
            "types and time range. The raw response includes the <code>state</code> field "
            "(e.g. <code>active</code>, <code>done</code>, <code>resolved</code>) and the "
            "<code>reported_by</code> JSON object, which is unpacked in a subsequent step."
        ),

        sp(4), h2("3.2 Timezone Handling"),
        p(
            "<code>get_timezone_from_time_range</code> extracts the IANA timezone string "
            "from the configured time range. <code>convert_values_to_timezone</code> "
            "converts the <code>time</code> column from UTC to local time. The display "
            "format used throughout the dashboard is <code>%d %b %Y %H:%M:%S</code>."
        ),

        sp(4), h2("3.3 Reporter Extraction"),
        p(
            "<code>extract_value_from_json_column</code> unpacks the "
            "<code>reported_by</code> JSON column, extracting the <code>name</code> field "
            "into a new <code>reported_by_name</code> string column. This column is used "
            "as the <b>Reported By</b> tooltip field on the Events Map."
        ),
    ]

    # ── 4. Event Status Grouping ───────────────────────────────────────────────
    story += [
        sp(4), h1("4. Event Status Grouping"), hr(),
        p(
            "This is the custom logic that distinguishes this workflow from the standard "
            "events workflow."
        ),

        h2("4.1 Algorithm"),
        p(
            "<code>add_event_status_group</code> (implemented in "
            "<code>custom-events-tasks</code>) adds an <code>event_status_group</code> "
            "column to the events GeoDataFrame and then <b>duplicates every row</b> into "
            "an \"All\" group. The result has up to two rows per original event:"
        ),
        bullet(
            "One row with its mapped status group (Active or Resolved)"
        ),
        bullet(
            "One row with <code>event_status_group = \"All\"</code>"
        ),
        p(
            "This duplication means that when the user selects <b>All</b> in the "
            "dashboard dropdown, every event is visible — not a separate filtered query."
        ),

        sp(4), h2("4.2 State-to-Group Mapping"),
        make_table(
            [
                [c("EarthRanger state"),   c("event_status_group")],
                [c("active"),              c("Active")],
                [c("scheduled"),           c("Active")],
                [c("overdue"),             c("Active")],
                [c("done"),               c("Resolved")],
                [c("resolved"),           c("Resolved")],
                [c("cancelled"),          c("Resolved")],
                [c("(any other value)"),  c("Unknown")],
            ],
            [5*cm, 11.5*cm],
        ),
        sp(4),
        note(
            "If the <code>state</code> column is absent from the data, all events are "
            "assigned <code>Unknown</code>."
        ),

        sp(4), h2("4.3 Dashboard Grouper Integration"),
        p(
            "After <code>add_event_status_group</code>, <code>set_groupers</code> "
            "configures <code>event_status_group</code> as the sole grouper. "
            "<code>split_groups</code> partitions the GeoDataFrame into one slice per "
            "distinct value of <code>event_status_group</code>. Each downstream branch "
            "(bar chart, map, pie chart, event count map) receives and processes these "
            "slices independently, producing one widget view per status group. The "
            "<code>merge_widget_views</code> step combines them into a single multi-view "
            "widget that the dashboard renders as a dropdown switcher."
        ),
    ]

    # ── 5. Event Processing Pipeline ───────────────────────────────────────────
    story += [
        sp(4), h1("5. Event Processing Pipeline"), hr(),

        h2("5.1 Location Filtering"),
        p(
            "<code>apply_reloc_coord_filter</code> filters events to a geographic "
            "bounding box and optional coordinate exclusion polygons. The filter is "
            "applied after <code>add_event_status_group</code> so grouping is preserved "
            "regardless of spatial filtering. Default bounds (−180 to 180, −90 to 90) "
            "pass all events."
        ),

        sp(4), h2("5.2 Temporal and Spatial Index"),
        p(
            "<code>add_temporal_index</code> and <code>add_spatial_index</code> attach "
            "grouper-aware index columns to the filtered events. Both steps reference "
            "<code>resolved_groupers</code>, which carries the "
            "<code>event_status_group</code> grouper through after spatial feature group "
            "resolution."
        ),

        sp(4), h2("5.3 Colour Mapping"),
        p(
            "<code>apply_color_map</code> maps the <code>event_type</code> column to a "
            "hex colour string using the <code>tab10</code> palette, storing the result "
            "in <code>event_type_colormap</code>. This column drives the fill colour on "
            "the Events Map and the bar and pie chart segments. All four dashboard widgets "
            "share this colour scheme."
        ),

        sp(4), h2("5.4 Column Renaming for Tooltip Display"),
        p(
            "Before the Events Map is drawn, <code>map_columns</code> renames internal "
            "column names to human-readable display labels:"
        ),
        make_table(
            [
                [c("Internal column"),       c("Display label")],
                [c("serial_number"),         c("Event Serial")],
                [c("time"),                  c("Event Time")],
                [c("event_type_display"),    c("Event Type")],
                [c("reported_by_name"),      c("Reported By")],
            ],
            [5*cm, 11.5*cm],
        ),
        sp(4),
        note(
            "<code>raise_if_not_found: true</code> — the workflow will fail if any of "
            "these columns is missing, ensuring tooltip configuration is always consistent."
        ),
    ]

    # ── 6. Dashboard Outputs ───────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Dashboard Outputs"), hr(),

        h2("6.1 Events Map"),
        p(
            "Produced by <code>create_point_layer</code> → <code>draw_ecomap</code> → "
            "<code>persist_text</code> → <code>create_map_widget_single_view</code> → "
            "<code>merge_widget_views</code>."
        ),
        make_table(
            [
                [c("Property"),           c("Value")],
                [c("Layer type"),         c("Point")],
                [c("Fill colour"),        c("event_type_colormap column")],
                [c("Point radius"),       c("5 px")],
                [c("Tooltip columns"),    c("Event Serial, Event Time, Event Type, Reported By")],
                [c("Legend"),             c("Label: Event Type column; Colour: event_type_colormap")],
                [c("Legend placement"),   c("Bottom-right")],
                [c("North arrow"),        c("Top-left")],
                [c("Static"),             c("false (interactive: pan, zoom, click tooltips)")],
                [c("Max zoom"),           c("20")],
            ],
            [4.5*cm, 12*cm],
        ),
        sp(4),
        note(
            "The <code>all_geometry_are_none</code> skip condition cleanly skips the "
            "point layer and ecomap steps when a status group has all-null geometry. "
            "Widget tasks use <code>skipif: never</code> so the dashboard always assembles."
        ),

        sp(4), h2("6.2 Events Bar Chart"),
        p(
            "Produced by <code>draw_time_series_bar_chart</code> → "
            "<code>persist_text</code> → <code>create_plot_widget_single_view</code> → "
            "<code>merge_widget_views</code>."
        ),
        make_table(
            [
                [c("Property"),         c("Value")],
                [c("X axis"),           c("time (at user-selected interval: day / week / month / year)")],
                [c("Y axis"),           c("event_type_display (aggregated as count)")],
                [c("Category"),         c("event_type_display")],
                [c("Aggregation"),      c("count")],
                [c("Colour column"),    c("event_type_colormap")],
                [c("Y axis title"),     c("Count of Events by Type")],
                [c("X axis title"),     c("Time")],
                [c("X period align"),   c("middle")],
            ],
            [4.5*cm, 12*cm],
        ),

        sp(4), h2("6.3 Events Pie Chart"),
        p(
            "Produced by <code>draw_pie_chart</code> → <code>persist_text</code> → "
            "<code>create_plot_widget_single_view</code> → <code>merge_widget_views</code>."
        ),
        make_table(
            [
                [c("Property"),       c("Value")],
                [c("Value column"),   c("event_type_display")],
                [c("Colour column"),  c("event_type_colormap")],
                [c("Text info"),      c("value (count shown on each slice)")],
            ],
            [4.5*cm, 12*cm],
        ),

        sp(4), h2("6.4 Event Count Map (Density Heatmap)"),
        p(
            "Pipeline: <code>create_meshgrid</code> → <code>calculate_feature_density"
            "</code> → <code>sort_values</code> → <code>drop_nan_values_by_column</code> "
            "→ <code>apply_classification</code> → <code>apply_color_map</code> → "
            "<code>map_columns</code> → <code>create_polygon_layer</code> → "
            "<code>draw_ecomap</code> → widget."
        ),
        make_table(
            [
                [c("Step"),             c("Detail")],
                [c("Grid"),             c("create_meshgrid — auto-scaled to AOI extent by default, or fixed cell size in metres")],
                [c("Density"),          c("calculate_feature_density — counts point features per grid cell; geometry_type: point")],
                [c("Classification"),   c("apply_classification — equal interval, 10 classes; labels show integer-rounded ranges")],
                [c("Colour palette"),   c("RdYlGn_r (red = high density, green = low density)")],
                [c("Fill opacity"),     c("0.40")],
                [c("Line width"),       c("0 (no cell borders)")],
                [c("Tooltip"),          c("Count — the number of events in the cell")],
                [c("Zero-count cells"), c("Dropped via drop_nan_values_by_column before colouring — transparent in the map")],
            ],
            [3.5*cm, 13*cm],
        ),
        sp(4),
        note(
            "The grid is computed once on the full (pre-split) GeoDataFrame and reused "
            "across all status group slices, so grid resolution is consistent across "
            "Active, Resolved, and All views."
        ),
    ]

    # ── 7. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("7. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the final dashboard from four widget "
            "groups, all bound to the <code>event_status_group</code> grouper and the "
            "configured time range:"
        ),
        make_table(
            [
                [c("Widget"),             c("Type"),  c("Pipeline")],
                [c("Events Bar Chart"),   c("Plot"),  c("events_bar_chart → grouped_bar_plot_widget_merge")],
                [c("Events Map"),         c("Map"),   c("grouped_events_ecomap → grouped_events_map_widget_merge")],
                [c("Events Pie Chart"),   c("Plot"),  c("grouped_events_pie_chart → grouped_events_pie_widget_merge")],
                [c("Event Count Map"),    c("Map"),   c("grouped_fd_ecomap → grouped_fd_map_widget_merge")],
            ],
            [4.5*cm, 2*cm, 10*cm],
        ),
        sp(4),
        p(
            "The dashboard layout places widgets in a two-column grid: Events Map (left) "
            "/ Events Bar Chart (right) / Event Count Map (left) / Events Pie Chart "
            "(right)."
        ),
        p(
            "The <b>Event status group</b> dropdown in the View panel switches all four "
            "widgets simultaneously between Active, Resolved, and All — no re-run required."
        ),
    ]

    # ── 8. Output Files ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Output Files"), hr(),
        p("All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."),
        make_table(
            [
                [c("File pattern"),                     c("Type"),  c("Description")],
                [c("*_v2.html (events map, per group)"),     c("HTML"),  c("Interactive ecomap — Events Map per status group")],
                [c("*_v2.html (bar chart, per group)"),      c("HTML"),  c("Plotly bar chart — Events Bar Chart per status group")],
                [c("*_v2.html (pie chart, per group)"),      c("HTML"),  c("Plotly pie chart — Events Pie Chart per status group")],
                [c("*_v2.html (event count map, per group)"), c("HTML"), c("Interactive ecomap — Event Count Map per status group")],
            ],
            [6*cm, 1.5*cm, 9*cm],
        ),
    ]

    # ── 9. Workflow Execution Logic ────────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> — skips the task (and all dependants) when any "
            "input GeoDataFrame is empty. This handles event type selections that return "
            "no data for the time period."
        ),
        bullet(
            "<b>any_dependency_skipped</b> — propagates skips downstream automatically."
        ),
        p(
            "Widget creation tasks override this with <code>skipif: never</code> to "
            "ensure the dashboard always assembles, even when a status group contains no "
            "events. The <code>create_point_layer</code> and "
            "<code>create_polygon_layer</code> steps add "
            "<code>all_geometry_are_none</code> as an additional skip condition."
        ),

        sp(4), h2("9.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),              c("Tasks")],
                [c("Setup"),              c("set_workflow_details, set_er_connection, set_time_range, get_timezone_from_time_range, set_groupers")],
                [c("Data ingest"),        c("get_events → convert_values_to_timezone → extract_value_from_json_column")],
                [c("Status grouping"),    c("add_event_status_group (custom task — duplicates rows into Active / Resolved / All)")],
                [c("Spatial setup"),      c("resolve_spatial_feature_groups_for_spatial_groupers, apply_reloc_coord_filter")],
                [c("Indexing"),           c("add_temporal_index → add_spatial_index")],
                [c("Colouring"),          c("apply_color_map (tab10 by event type)")],
                [c("Split"),              c("split_groups (one slice per event_status_group value)")],
                [c("Events Map branch"),  c("map_columns (rename) → create_point_layer → draw_ecomap → persist_text → widget")],
                [c("Bar Chart branch"),   c("draw_time_series_bar_chart → persist_text → widget")],
                [c("Pie Chart branch"),   c("draw_pie_chart → persist_text → widget")],
                [c("Event Count branch"), c("create_meshgrid → calculate_feature_density → classify → colour → create_polygon_layer → draw_ecomap → widget")],
                [c("Dashboard"),          c("gather_dashboard combines all four merged widget groups")],
            ],
            [3.5*cm, 13*cm],
        ),
    ]

    # ── 10. Software Versions ──────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),               c("Version"),  c("Role")],
                [c("ecoscope-platform"),     c("2.13.0"),   c("Core task library, workflow engine, spatial analysis")],
                [c("custom-events-tasks"),   c("0.1.4"),    c("Bundled custom tasks: add_event_status_group, filter_events_by_state")],
                [c("pydeck"),                c("0.9.2"),    c("Map rendering (pinned — re-declared as workaround for known pydeck dependency conflict)")],
            ],
            [5*cm, 2.5*cm, 9*cm],
        ),
        sp(4),
        p(
            "The <code>ecoscope-platform</code> package is distributed via the "
            "<code>https://repo.prefix.dev/ecoscope-workflows/</code> conda channel. "
            "The <code>custom-events-tasks</code> package is bundled directly inside the "
            "compiled workflow directory "
            "(<code>ecoscope-workflows-custom-events-workflow/custom-events-tasks/</code>) "
            "and installed as a local editable PyPI package via a relative path in "
            "<code>pixi.toml</code>. The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()

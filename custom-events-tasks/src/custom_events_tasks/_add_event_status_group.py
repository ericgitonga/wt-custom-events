from typing import cast

from ecoscope.platform.annotations import AnyDataFrame
from wt_registry import register

_STATE_TO_GROUP = {
    "active": "Active",
    "scheduled": "Active",
    "overdue": "Active",
    "done": "Resolved",
    "resolved": "Resolved",
    "cancelled": "Resolved",
}


@register(description="Add event_status_group column mapping ER event states to 'Active' or 'Resolved'.")
def add_event_status_group(df: AnyDataFrame) -> AnyDataFrame:
    result = df.copy()
    if "state" in df.columns:
        result["event_status_group"] = df["state"].str.lower().map(_STATE_TO_GROUP).fillna("Unknown")
    else:
        result["event_status_group"] = "Unknown"
    return cast(AnyDataFrame, result)

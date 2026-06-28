from typing import Annotated, Literal, cast

from ecoscope.platform.annotations import AnyDataFrame
from pydantic import Field
from wt_registry import register

EventStatus = Literal["all", "active", "resolved"]

_ACTIVE_STATES = {"active", "scheduled", "overdue"}
_RESOLVED_STATES = {"done", "cancelled"}


@register(description="Filter events by their state (all, active, or resolved).")
def filter_events_by_state(
    df: AnyDataFrame,
    event_status: Annotated[
        EventStatus,
        Field(
            default="all",
            title="Event Status",
            description=(
                "Which events to include: 'all' returns every event, "
                "'active' returns events with state active/scheduled/overdue, "
                "'resolved' returns events with state done/cancelled."
            ),
        ),
    ] = "all",
) -> AnyDataFrame:
    if event_status in ("active", "resolved") and "state" not in df.columns:
        return cast(AnyDataFrame, df.iloc[0:0])
    if event_status == "active":
        return cast(AnyDataFrame, df[df["state"].isin(_ACTIVE_STATES)])
    if event_status == "resolved":
        return cast(AnyDataFrame, df[df["state"].isin(_RESOLVED_STATES)])
    return df

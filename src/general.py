from __future__ import annotations

import altair as alt
from tap import Tap
import pandas as pd
import sys

def draw_graph(data, show=False, fileobj=None) -> None:
    alt.renderers.enable("browser", offline=True)
    print(data)

    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("start", axis=alt.Axis(tickCount="second", format="%H:%M:%S")),
            x2="end",
            y=alt.Y("name", sort=None),
            order="start",
            color=alt.Color(scale=alt.Scale(scheme="dark2")),
            tooltip=[
                alt.Tooltip("start:T").format("%H:%M:%S.%f"),
                alt.Tooltip("end:T").format("%H:%M:%S.%f"),
                alt.Tooltip("name"),
            ],
        )
        .interactive()
        .properties(title="Timeline of Tasks", width="container", height=600)
        .configure_axis(labelFontSize=14, titleFontSize=14, grid=False)
        .configure_title(fontSize=20)
        .configure_legend(labelFontSize=16, titleFontSize=16)
    )

    chart.show()

def main():
    data = pd.read_csv(sys.argv[1], parse_dates=['start', 'end'])
    print(data)
    print(data.dtypes)
    draw_graph(data)


if __name__ == "__main__":
    main()    
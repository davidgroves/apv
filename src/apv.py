from __future__ import annotations

import altair as alt
from tap import Tap
import pandas as pd
import json
import datetime
import dataclasses
import pathlib


@dataclasses.dataclass(frozen=True)
class Task:
    hostname: str
    name: str
    start: datetime.datetime
    end: datetime.datetime
    task_id: str
    hostname_and_name: list[str] = dataclasses.field(init=False)
    duration: datetime.timedelta = dataclasses.field(init=False)

    def __post_init__(self):
        # Using object.__setattr__ to bypass the frozen state.
        # These REALLY should be derived properties, but it doesn't work with Pandas without refactoring.
        object.__setattr__(self, "duration", (self.end - self.start).total_seconds())
        object.__setattr__(self, "hostname_and_name", [self.hostname, self.name])

    @classmethod
    def from_json(self, json_task: dict) -> Task:
        hostname = json_task["hosts"][0]
        name = json_task["task"]["name"]
        start = datetime.datetime.fromisoformat(json_task["task"]["duration"]["start"])
        end = datetime.datetime.fromisoformat(json_task["task"]["duration"]["end"])
        task_id = json_task["task"]["id"]
        return Task(hostname=hostname, name=name, start=start, end=end, task_id=task_id)


def extract_json(document: str) -> dict:
    lines = document.splitlines()
    start_index = next(i for i, line in enumerate(lines) if line.strip() == "{")
    end_index = next(
        i for i in range(len(lines) - 1, -1, -1) if lines[i].strip() == "}"
    )

    json_content = "\n".join(lines[start_index : end_index + 1])

    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {e}")


def get_task(document: dict) -> Task:
    hostname = list(document["hosts"].keys())[0]
    name = document["task"]["name"]
    start = datetime.datetime.fromisoformat(document["task"]["duration"]["start"])
    end = datetime.datetime.fromisoformat(document["task"]["duration"]["end"])
    task_id = document["task"]["id"]
    return Task(hostname=hostname, name=name, start=start, end=end, task_id=task_id)


def get_tasks(document: dict, sorted=True) -> list[Task]:
    return [get_task(task) for task in document]


def draw_graph(tasks: list[Task], show=False, fileobj=None) -> None:
    alt.renderers.enable("browser", offline=True)

    source = pd.DataFrame(tasks).sort_values(by="start")

    chart = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x=alt.X("start", axis=alt.Axis(tickCount="second", format="%H:%M:%S")),
            x2="end",
            y=alt.Y("hostname_and_name", sort=None),
            order="start",
            color=alt.Color("hostname", scale=alt.Scale(scheme="dark2")),
            tooltip=[
                alt.Tooltip("name"),
                alt.Tooltip("hostname"),
                alt.Tooltip("start:T").format("%H:%M:%S.%f"),
                alt.Tooltip("end:T").format("%H:%M:%S.%f"),
                alt.Tooltip("duration"),
            ],
        )
        .interactive()
        .properties(title="Timeline of Tasks", width="container", height=600)
        .configure_axis(labelFontSize=14, titleFontSize=14, grid=False)
        .configure_title(fontSize=20)
        .configure_legend(labelFontSize=16, titleFontSize=16)
    )

    chart.show()


class CLIParser(Tap):
    input: pathlib.Path
    show: bool = False
    output: pathlib.Path = pathlib.Path("output.html")


def parse_args() -> CLIParser:
    parser = CLIParser()
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    text: str = args.input.read_text()
    document = extract_json(text)
    tasks = document["plays"][0]["tasks"]
    tasks = get_tasks(tasks)

    if args.show:
        draw_graph(tasks, show=True)

    if args.output:
        draw_graph(tasks, fileobj=args.output.open("w"))


if __name__ == "__main__":
    main()

import apv
import datetime
import json
import pytest


def test_extract_json():
    document = """
Not JSON
{
    "key": "value"
}
MORE NOT JSON
"""
    assert apv.extract_json(document) == {"key": "value"}


def test_extract_json_invalid():
    document = """
Not JSON
{
    ALSO NOT JSON
}
MORE NOT JSON
"""

    with pytest.raises(ValueError):
        apv.extract_json(document)


def test_get_task():
    j = json.load(open("tests/data/out.json"))

    tasks = j["plays"][0]["tasks"]

    assert apv.get_task(tasks[1]) == apv.Task(
        hostname="localhost",
        name="Sleep for 1 second.",
        start=datetime.datetime(
            2024, 9, 20, 13, 8, 26, 461973, tzinfo=datetime.timezone.utc
        ),
        end=datetime.datetime(
            2024, 9, 20, 13, 8, 27, 468543, tzinfo=datetime.timezone.utc
        ),
        task_id="c87f5402-5efd-8c06-675c-000000000003",
    )


def test_get_tasks():
    j = json.load(open("tests/data/out.json"))

    tasks = j["plays"][0]["tasks"]
    result = apv.get_tasks(tasks)

    assert result == [
        apv.Task(
            hostname="localhost",
            name="Gathering Facts",
            start=datetime.datetime(
                2024, 9, 20, 13, 8, 25, 625318, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2024, 9, 20, 13, 8, 26, 446887, tzinfo=datetime.timezone.utc
            ),
            task_id="c87f5402-5efd-8c06-675c-00000000000b",
        ),
        apv.Task(
            hostname="localhost",
            name="Sleep for 1 second.",
            start=datetime.datetime(
                2024, 9, 20, 13, 8, 26, 461973, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2024, 9, 20, 13, 8, 27, 468543, tzinfo=datetime.timezone.utc
            ),
            task_id="c87f5402-5efd-8c06-675c-000000000003",
        ),
        apv.Task(
            hostname="localhost",
            name="Sleep for 2 seconds.",
            start=datetime.datetime(
                2024, 9, 20, 13, 8, 27, 472517, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2024, 9, 20, 13, 8, 29, 484185, tzinfo=datetime.timezone.utc
            ),
            task_id="c87f5402-5efd-8c06-675c-000000000004",
        ),
        apv.Task(
            hostname="localhost",
            name="Sleep for 3 seconds (A)",
            start=datetime.datetime(
                2024, 9, 20, 13, 8, 29, 500290, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2024, 9, 20, 13, 8, 29, 699868, tzinfo=datetime.timezone.utc
            ),
            task_id="c87f5402-5efd-8c06-675c-000000000005",
        ),
        apv.Task(
            hostname="localhost",
            name="Sleep for 3 seconds (B)",
            start=datetime.datetime(
                2024, 9, 20, 13, 8, 29, 703764, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2024, 9, 20, 13, 8, 29, 802680, tzinfo=datetime.timezone.utc
            ),
            task_id="c87f5402-5efd-8c06-675c-000000000006",
        ),
    ]


def test_draw_graph():
    tasks = apv.get_tasks(json.load(open("tests/data/out.json"))["plays"][0]["tasks"])
    apv.draw_graph(tasks)


def test_draw_graph_overlapping():
    tasks = apv.get_tasks(
        json.load(open("tests/data/overlapping.json"))["plays"][0]["tasks"]
    )
    apv.draw_graph(tasks)

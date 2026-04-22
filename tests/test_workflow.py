from __future__ import annotations

from pathlib import Path

from nextgen2026_coding_bootcamp.runtime import RunContext
from nextgen2026_coding_bootcamp.workflow import run_workflow


def test_run_workflow_calls_stages_in_order_and_stores_artifacts(monkeypatch):
    call_order: list[str] = []

    def fake_fetch(cfg, ctx):
        call_order.append("fetch")
        return {"raw_tsv": "fetch.tsv"}

    def fake_prepare(cfg, ctx):
        call_order.append("prepare")
        assert ctx.artifacts["fetch"]["raw_tsv"] == "fetch.tsv"
        return {"prepared_messages_csv": "prepare.csv"}

    def fake_analyze(cfg, ctx):
        call_order.append("analyze")
        assert ctx.artifacts["prepare"]["prepared_messages_csv"] == "prepare.csv"
        return {"message_predictions_csv": "analyze.csv"}

    def fake_report(cfg, ctx):
        call_order.append("report")
        assert ctx.artifacts["analyze"]["message_predictions_csv"] == "analyze.csv"
        return {"report_markdown": "report.md"}

    monkeypatch.setattr("nextgen2026_coding_bootcamp.workflow.run_fetch", fake_fetch)
    monkeypatch.setattr("nextgen2026_coding_bootcamp.workflow.run_prepare", fake_prepare)
    monkeypatch.setattr("nextgen2026_coding_bootcamp.workflow.run_analyze", fake_analyze)
    monkeypatch.setattr("nextgen2026_coding_bootcamp.workflow.run_report", fake_report)

    ctx = RunContext(run_id="workflow-test", run_dir=Path("/tmp/workflow-test"))

    returned_ctx = run_workflow(cfg=object(), ctx=ctx)

    assert returned_ctx is ctx
    assert call_order == ["fetch", "prepare", "analyze", "report"]
    assert ctx.artifacts == {
        "fetch": {"raw_tsv": "fetch.tsv"},
        "prepare": {"prepared_messages_csv": "prepare.csv"},
        "analyze": {"message_predictions_csv": "analyze.csv"},
        "report": {"report_markdown": "report.md"},
    }

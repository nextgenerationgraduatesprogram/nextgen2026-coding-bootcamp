from nextgen2026_coding_bootcamp.steps.analyze import run_analyze
from nextgen2026_coding_bootcamp.steps.fetch import run_fetch
from nextgen2026_coding_bootcamp.steps.prepare import run_prepare
from nextgen2026_coding_bootcamp.steps.report import run_report


def run_workflow(cfg, ctx):
    ctx.artifacts["fetch"] = run_fetch(cfg=cfg, ctx=ctx)
    ctx.artifacts["prepare"] = run_prepare(cfg=cfg, ctx=ctx)
    ctx.artifacts["analyze"] = run_analyze(cfg=cfg, ctx=ctx)
    ctx.artifacts["report"] = run_report(cfg=cfg, ctx=ctx)
    return ctx

import builtins
import importlib
import sys
import types

import pytest

import app.backend.generate_cv_html_to_pdf as pdf_module


def _reload_pdf_module():
    return importlib.reload(pdf_module)


def test_html_to_pdf_raises_actionable_error_when_playwright_missing(monkeypatch, tmp_path):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "playwright.async_api":
            raise ImportError("missing playwright")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    reloaded = _reload_pdf_module()

    with pytest.raises(reloaded.PdfRenderError, match="Playwright is not installed"):
        import asyncio

        asyncio.run(reloaded.html_to_pdf("<html></html>", str(tmp_path / "out.pdf")))


def test_html_to_pdf_wraps_browser_launch_failures(monkeypatch, tmp_path):
    class FakeTimeoutError(Exception):
        pass

    class FakePlaywrightContext:
        async def __aenter__(self):
            return types.SimpleNamespace(
                chromium=types.SimpleNamespace(
                    launch=self._launch,
                )
            )

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def _launch(self):
            raise RuntimeError("Executable doesn't exist at /fake/chromium")

    fake_async_api = types.SimpleNamespace(
        TimeoutError=FakeTimeoutError,
        async_playwright=lambda: FakePlaywrightContext(),
    )
    monkeypatch.setitem(sys.modules, "playwright.async_api", fake_async_api)
    reloaded = _reload_pdf_module()

    with pytest.raises(reloaded.PdfRenderError, match="playwright install chromium"):
        import asyncio

        asyncio.run(reloaded.html_to_pdf("<html></html>", str(tmp_path / "out.pdf")))

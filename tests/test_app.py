import io

import pytest
from rich.console import Console

from sysglance import __version__, app


@pytest.mark.parametrize("pct, word", [
    (0, "Relaxed"), (24, "Relaxed"), (25, "Comfortable"), (60, "Busy"),
    (80, "Working hard"), (100, "Maxed out"),
])
def test_mood_words(pct, word):
    assert app.mood(pct)[0] == word


@pytest.mark.parametrize("n, text", [
    (500 * 2**20, "500 MB"), (2**30, "1.0 GB"), (int(11.1 * 2**30), "11.1 GB"),
])
def test_size(n, text):
    assert app.size(n) == text


@pytest.mark.parametrize("bps, text", [
    (440, "440 B/s"), (2300, "2.3 KB/s"), (5_000_000, "5.0 MB/s"), (2e12, "2000.0 GB/s"),
])
def test_rate(bps, text):
    assert app.rate(bps) == text


@pytest.mark.parametrize("seconds, text", [
    (10, "a moment"), (60, "1 minute"), (180, "3 minutes"), (3660, "1 hour, 1 minute"),
    (6 * 86400 + 6 * 3600 + 120, "6 days, 6 hours"),
])
def test_friendly_duration(seconds, text):
    assert app.friendly_duration(seconds) == text


@pytest.mark.parametrize("proc, user, name", [
    ("brave", "me", "Brave"), ("gnome-shell", "me", "Desktop"), ("MATLABWindow", "me", "MATLAB"),
    ("gsd-power", "me", "Desktop"), ("sshd", "root", "System"), ("kitty-bin", "me", "Kitty"),
])
def test_app_name(proc, user, name):
    assert app.app_name(proc, user) == name


def render(width, height):
    dash = app.Dashboard(1.0)
    dash.update()
    console = Console(file=io.StringIO(), width=width, height=height, force_terminal=False)
    console.print(dash.render(width, height), height=height)
    return console.file.getvalue()


@pytest.mark.parametrize("width, height", [(80, 24), (120, 35), (200, 50)])
def test_dashboard_renders_at_common_sizes(width, height):
    output = render(width, height)
    for title in ("Processor", "Memory", "Graphics", "What's using your computer", "At a glance"):
        assert title in output
    assert f"v{__version__}" in output


def test_memory_line_fits_in_a_standard_terminal():
    cards = "What's using your computer"
    assert "free of" not in render(80, 24).split(cards)[0]
    assert "free of" in render(120, 35).split(cards)[0]


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["sysglance", "--version"])
    with pytest.raises(SystemExit) as exit_info:
        app.main()
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"sysglance {__version__}"


class FakeStdout:
    def __init__(self):
        self.config = None

    def reconfigure(self, **config):
        self.config = config


@pytest.mark.parametrize("is_windows, expected", [
    (True, {"encoding": "utf-8", "errors": "replace"}), (False, None),
])
def test_output_encoding_is_forced_only_on_windows(monkeypatch, is_windows, expected):
    stdout = FakeStdout()
    monkeypatch.setattr(app._compat, "IS_WIN", is_windows)
    monkeypatch.setattr("sys.stdout", stdout)
    app.use_utf8_output()
    assert stdout.config == expected

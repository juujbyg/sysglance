# sysglance

[![CI](https://github.com/juujbyg/sysglance/actions/workflows/ci.yml/badge.svg)](https://github.com/juujbyg/sysglance/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/juujbyg/sysglance)](https://github.com/juujbyg/sysglance/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**See how your computer is doing, in plain language.** A live terminal dashboard for your processor, memory and graphics card, on Linux and Windows.

```
 sysglance   ●  Everything looks good                                                           Friday 20:17
╭─ Processor ──────────────────────╮╭─ Memory ──────────────────────────╮╭─ Graphics ────────────────────────╮
│                                  ││                                   ││                                   │
│   ╻ ╻╺━┓                         ││   ╻ ╻╺━┓                          ││   ┏━┓                             │
│   ┗━┫ ━┫   Comfortable           ││   ┗━┫  ┃   Comfortable            ││   ┃ ┃   Relaxed                   │
│     ╹╺━┛ %                       ││     ╹  ╹ %                        ││   ┗━┛ %                           │
│                                  ││                                   ││                                   │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ││   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ││   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                  ││                                   ││                                   │
│   4 cores  ·  Cool 59°C          ││   5.9 GB free of 11.1 GB          ││   Intel graphics                  │
│   Fan is spinning                ││   Plenty of room                  ││   Estimated from speed            │
│                                  ││                                   ││                                   │
│   ▄  last 1s                     ││   ▄  last 1s                      ││   ▁  last 1s                      │
╰──────────────────────────────────╯╰───────────────────────────────────╯╰───────────────────────────────────╯
```

## What it shows

- A status line in plain words, such as "Everything looks good" or "Memory is running low".
- A card each for Processor, Memory and Graphics, with a big number, a word for how busy it is (Relaxed to Maxed out) and a short history graph.
- **What's using your computer:** processes grouped into apps, such as "Brave ×15". Shared memory is counted only once per app.
- **At a glance:** battery, disk space, internet speed, how long the computer has been on, and tips.

## Install

Single-file downloads need nothing else installed. Get them from the [latest release](https://github.com/juujbyg/sysglance/releases/latest).

**Linux (x64)**
```bash
curl -fsSLo ~/.local/bin/sysglance https://github.com/juujbyg/sysglance/releases/latest/download/sysglance-linux-x64
chmod +x ~/.local/bin/sysglance
```

**Windows (x64):** download `sysglance-windows-x64.exe` and run it from Windows Terminal. It isn't code-signed, so SmartScreen may ask you to confirm.

**From source (Python 3.9+)**
```bash
pipx install git+https://github.com/juujbyg/sysglance
```

## Usage

```bash
sysglance              # live view, press Ctrl+C to close
sysglance -i 2         # update every 2 seconds
sysglance --once       # show one snapshot and exit
sysglance --version
```

## GPU support

| GPU | Linux | Windows |
|---|---|---|
| NVIDIA | `nvidia-smi` | `nvidia-smi` |
| AMD | amdgpu sysfs (busy %, VRAM, temperature, power) | Windows GPU performance counters |
| Intel | per-process DRM fdinfo counters (no root needed) and i915 clock speeds | Windows GPU performance counters |

If no usage counters are readable, sysglance estimates GPU activity from clock speed and says so.

## Development

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'
pytest
```

Pushing a tag such as `v1.0.1` runs the tests, builds both single-file downloads and publishes a release. The tag must match `__version__` in `src/sysglance/__init__.py`.

## License

MIT

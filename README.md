# thaakz

A personal Python utility library for reuse across multiple projects.
Install once into your environment — import anywhere.

---

## Installation

### Local install (development)

Install into a specific environment using that environment's own `pip`:

```bash
C:\SSP\Python\env\Scripts\pip install -e C:\SSP\Python\localpackages\thaakz
```

The `-e` flag installs in **editable mode** — any changes you make to the
source files are reflected immediately without reinstalling.

### PyPI install (future — after upload)

```bash
pip install thaakz
```

---

## Modules

### `thaakz.utils` — General Utilities

#### `TimeReport` — Hierarchical Phase Timer

Measures and reports elapsed time across named phases of a pipeline,
with optional sub-level (hierarchical) breakdown.

**Import:**
```python
from thaakz.utils import TimeReport
from thaakz.utils import time_report_example   # built-in demo
```

**Basic usage — flat phases:**
```python
from thaakz.utils import TimeReport

tr = TimeReport("Load Tokenizer and Model")
tr.StartPhase("Tokenization")
tr.StartPhase("Generation")
tr.StartPhase("Displaying")
tr.FinishedMonitoring()
tr.PrintReport()
```

Output:
```
Load Tokenizer and Model    : 1.172s
Tokenization                : 0.007s
Generation                  : 13.553s
Displaying                  : 0.024s
Total                       : 14.756s
```

**Advanced usage — hierarchical sub-phases:**
```python
from thaakz.utils import TimeReport

tr = TimeReport("Load Tokenizer and Model")
tr.StartPhase("Tokenization")
tr.StartPhase("Generation", startSubPhase=True)  # open sub-level
tr.StartPhase("Resolving Config")
tr.StartPhase("Resolving Trust_Remote_Code")
tr.StartPhase("Internal Generation")
tr.CloseLevel()                                  # close sub-level
tr.StartPhase("Displaying")
tr.FinishedMonitoring()
tr.PrintReport()
```

Output:
```
Load Tokenizer and Model    : 1.172s
Tokenization                : 0.007s
Generation                  :
         Resolving Config : 0.033s
         Resolving Trust_Remote_Code : 0.008s
         Internal Generation : 13.512s
         SubTotal :  13.553s
Displaying                  : 0.024s
Total                       : 14.756s
```

**Run the built-in demo:**
```python
from thaakz.utils import time_report_example
time_report_example()
```

---

#### `TimeReport` API Reference

| Method | Parameters | Description |
|---|---|---|
| `TimeReport(first_phase)` | `first_phase=None` | Create instance; optionally start first phase immediately |
| `StartPhase(name, startSubPhase)` | `name: str`, `startSubPhase=False` | Begin a new phase; `True` opens a sub-level |
| `CloseLevel()` | — | Close current sub-level, return to parent level |
| `FinishedMonitoring()` | — | Signal all phases complete; closes any open levels |
| `PrintReport(indent, col_width)` | `indent='         '`, `col_width=28` | Print and return the formatted timing report |

---

#### Unnamed threshold rule

When `startSubPhase=True` is used, the class watches how quickly the
first named sub-phase arrives:

| Gap before first sub-phase | Behaviour |
|---|---|
| Within 0.5ms | Sub-phase named directly — no extra row |
| Longer than 0.5ms | Gap recorded as `Initialization` automatically |

---

### `thaakz.ai` — AI Utilities *(future)*

```python
from thaakz.ai import ModelViewer    # coming soon
```

---

### `thaakz.hf` — HuggingFace Utilities *(future)*

```python
from thaakz.hf import HuggingFaceGUI as hfgui    # coming soon
```

---

## Verify Installation

```bash
C:\SSP\Python\env\Scripts\pip show thaakz
```

Expected output:
```
Name: thaakz
Version: 0.1.0
Location: C:\SSP\Python\localpackages\thaakz
Editable project location: C:\SSP\Python\localpackages\thaakz
```

---

## Extending the Package

Add new modules inside the relevant sub-package folder:

```
thaakz\utils\
    __init__.py
    time_report.py        ← today
    logger.py             ← add anytime
    rouge_helper.py       ← add anytime
```

Then expose in `thaakz/utils/__init__.py`:

```python
from .time_report  import TimeReport
from .logger       import SSPLogger
from .rouge_helper import compute_rouge_urdu
```

No reinstall needed — editable mode picks up new files automatically.

---

## Environment Management

| Goal | Command |
|---|---|
| Install into `env` | `C:\SSP\Python\env\Scripts\pip install -e C:\SSP\Python\localpackages\thaakz` |
| Install into another env | `C:\SSP\Python\other_env\Scripts\pip install -e C:\SSP\Python\localpackages\thaakz` |
| Verify installation | `C:\SSP\Python\env\Scripts\pip show thaakz` |
| Uninstall | `C:\SSP\Python\env\Scripts\pip uninstall thaakz` |

---

## Version History

| Version | Description |
|---|---|
| 0.1.0 | Initial release — `TimeReport` hierarchical phase timer |

---

## Author

SSP — thaakz personal utility library.

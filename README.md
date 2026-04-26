# elecfreaks-cutebot-pro-v2

A modified MicroPython module for the Elecfreaks Cutebot Pro v2 on the BBC micro:bit v2.

## Overview

This project provides a revised version of the original [`cutebot_pro.py`](https://github.com/elecfreaks/EF_Produce_MicroPython/blob/master/cutebot_pro.py) module from the Elecfreaks [`EF_Produce_MicroPython`](https://github.com/elecfreaks/EF_Produce_MicroPython) repository.

This revision is intended specifically for the **Elecfreaks Cutebot Pro v2** and is designed for use with the **BBC micro:bit v2**.

## Important compatibility note

**This module supports Cutebot Pro v2 only.**

Support for **Cutebot Pro v1** has been removed in this revision. This was done to reduce code size and make room for additional v2-specific functionality.  The additional v2 specific functionality plus client scripts would have been too large for the limited space available on the micro:bit file system.

## Main changes in this revision

- removed Cutebot Pro v1 compatibility
- added `set_neopixels()`
- added `set_neopixels_random()`
- added a new class: `CutebotProLineController`
- renamed many classes, methods, and constants for greater clarity and consistency

## Origin

This project is based on code from the Elecfreaks repository:

- Repository: [`EF_Produce_MicroPython`](https://github.com/elecfreaks/EF_Produce_MicroPython)
- Original file used for this revision: [`cutebot_pro.py`](https://github.com/elecfreaks/EF_Produce_MicroPython/blob/master/cutebot_pro.py)

The Elecfreaks repository is itself a fork of:
- https://github.com/lionyhw/EF_Produce_MicroPython

The upstream repository uses the MIT License. The Elecfreaks fork also includes the MIT License.

## Files

- [`cutebot_pro_v2.py`](cutebot_pro_v2.py) — the main MicroPython module
- [`examples/`](examples/) — example programs
- [`examples/basic_test.py`](examples/basic_test.py) — a simple usage example
- [`docs/changes_from_original.md`](docs/changes_from_original.md) — summary of key changes from the original module
- [`LICENSE`](LICENSE) — license information

## Installation

Copy [`cutebot_pro_v2.py`](cutebot_pro_v2.py) to your BBC micro:bit using your preferred MicroPython file transfer method.

## Compatibility

Tested on actual hardware:

- BBC micro:bit v2
- Elecfreaks Cutebot Pro v2

Not supported:

- Elecfreaks Cutebot Pro v1

## Migration warning for users of the original module

This is **not** a drop-in replacement for the original [`cutebot_pro.py`](https://github.com/elecfreaks/EF_Produce_MicroPython/blob/master/cutebot_pro.py) in all cases.

Because this revision removes v1 support and renames parts of the API, existing code written for the original module will need to be updated.

Changes include:

- class names
- method names
- constant names

See [`docs/changes_from_original.md`](docs/changes_from_original.md) for a summary of major differences.

## Development note

This revised version was developed with AI assistance. Generated code and documentation were reviewed, edited, and tested on actual Elecfreaks Cutebot Pro v2 and BBC micro:bit v2 hardware by the repository author.

## License

This repository contains code derived from an MIT-licensed project. See the [`LICENSE`](LICENSE) file for details.

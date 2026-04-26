docs/changes_from_original.md`

# Changes from the original module

This repository contains a modified version of the original `cutebot_pro.py` module from the Elecfreaks `EF_Produce_MicroPython` repository.

## Summary of major changes

### 1. Removed Cutebot Pro v1 compatibility

Support for Cutebot Pro v1 was removed so that the module could be reduced in size and focused on Cutebot Pro v2 only.

### 2. Added new v2 functionality

The following methods were added to the Cutebot Pro class:

- `set_neopixels()`
- `set_neopixels_random()`

These methods were added to expose control of the robot's neopixels, which was not available through the original module.

### 3. Added a new class

A new class was added:

- `CutebotProLineController`

This class was added to create a PID (Proportional-Integral-Derivative) controller, particularly for purposes of line tracking.  This controller was not available in the original module.

### 4. Renamed parts of the API

Many classes, methods, and constants were renamed for improved clarity and consistency.

Because of these renamings, code written for the original module will need modification before it will work with this revised version.

## Reason for the design changes

The micro:bit file system has limited space for uploading modules and client scripts.  Adding new functionality without removing older compatibility code would have made the module too large for practical use. To make room for the new v2-specific features, support for v1 was removed.

## Compatibility

Supported:

- Elecfreaks Cutebot Pro v2
- BBC micro:bit

Not supported:

- Elecfreaks Cutebot Pro v1

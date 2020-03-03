#!/usr/bin/env python3
"""
    Build script for automated still.
"""
import os

COMMANDS = ("rm -rf still_rc.py ui_still.py __pycache__ CustomQt/__pycache__",
            "pyuic5 -o ui_still.py ui/still.ui",
            "pyrcc5 -o still_rc.py still.qrc")

for command in COMMANDS:
    print(command)
    os.system(command)

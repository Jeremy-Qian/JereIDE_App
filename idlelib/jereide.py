"""
JereIDE - Enhanced Python IDE

This module is deprecated. Please use launch.py as the main entry point.

JereIDE is a fork of Python's IDLE with customizations and enhancements.
For information about changes and new features, see FEATURES.md or the README.
"""

import os.path
import sys
import warnings

# Enable running JereIDE with idlelib in a non-standard location.
# This was once used to run development versions of JereIDE.

idlelib_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if idlelib_dir not in sys.path:
    sys.path.insert(0, idlelib_dir)

# Warn users that this entry point is deprecated
warnings.warn(
    "JereIDE: idlelib.jereide is deprecated. Use launch.py as the main entry point.",
    DeprecationWarning,
    stacklevel=2,
)

from idlelib.pyshell import main  # This is subject to change

main()

import os.path
import sys

# Enable running JereIDE with idlelib in a non-standard location.
# This was once used to run development versions of JereIDE.

idlelib_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if idlelib_dir not in sys.path:
    sys.path.insert(0, idlelib_dir)

from idlelib.pyshell import main  # This is subject to change

main()

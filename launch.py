import os
import sys

# Add the current directory to the very top of Python's search path
# This forces Python to look in './idlelib' BEFORE looking in the system folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import your local idlelib
import idlelib.pyshell

# Start IDLE
idlelib.pyshell.main()

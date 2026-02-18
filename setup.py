import sys

from cx_Freeze import Executable, setup

build_exe_options = {
    "packages": [],
    "excludes": [],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="JereIDE",
    version="v0.0.1",
    description="A Python IDE based on IDLE",
    options={"build_exe": build_exe_options},
    executables=[Executable("launch.py", base=base)],
)

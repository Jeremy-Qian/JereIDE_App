import sys

from cx_Freeze import Executable, setup

# Base configuration for macOS .app bundle
base = "Win32GUI" if sys.platform == "win32" else None

# Executable configuration
executables = [
    Executable(
        script="launch.py",
        base=base,
        target_name="JereIDE",
        icon=None,  # Replace with a .icns file for macOS if available
    )
]

# Setup configuration
setup(
    name="JereIDE",
    version="0.1",
    description="A custom IDE for Jeremy",
    executables=executables,
    options={
        "build_exe": {
            "packages": [],  # Add required packages here
            "excludes": [],  # Exclude unnecessary packages
            "include_files": [],  # Add non-Python files (e.g., assets)
        },
        "bdist_mac": {
            "bundle_name": "JereIDE",  # Name of the .app bundle
            "iconfile": "AppIcon.icns",  # Replace with a .icns file if available
            "custom_info_plist": None,  # Optional: Path to a custom Info.plist
        },
    },
)

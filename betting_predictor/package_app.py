import os
import subprocess
import sys

def build_exe():
    print("📦 Preparing to package SENE Predictor...")
    
    # 1. Install PyInstaller via Python directly
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Create the 'run_app.py' entry point
    with open("run_app.py", "w") as f:
        f.write("""
import streamlit.web.cli as stcli
import os, sys

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, path)

if __name__ == "__main__":
    # Disable email prompt and telemetry
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("streamlit_app.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
        """)

    print("🚀 Building EXE (this may take a few minutes)...")
    
    # 3. Use 'python -m PyInstaller' instead of just 'pyinstaller'
    # This avoids the "system cannot find file" error
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--collect-all", "streamlit",
        "--collect-all", "xgboost",
        "--collect-all", "sklearn",
        "--add-data", f"streamlit_app.py{os.pathsep}.",
        "--add-data", f"analyzer.py{os.pathsep}.",
        "--add-data", f"data_fetcher.py{os.pathsep}.",
        "--add-data", f"config.py{os.pathsep}.",
        "--add-data", f"engine.py{os.pathsep}.",
        "--add-data", f"backtester.py{os.pathsep}.",
        "--add-data", f"kelly.py{os.pathsep}.",
        "--add-data", f"models{os.pathsep}models",
        "--add-data", f"data{os.pathsep}data",
        "run_app.py"
    ]
    
    subprocess.call(cmd)
    print("\n✅ Done! Your app is in the 'dist' folder.")

if __name__ == "__main__":
    build_exe()

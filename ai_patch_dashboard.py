import streamlit as st
import subprocess
import shutil
import pandas as pd
import sys
import platform
import psutil
import io
import json
from datetime import datetime

# Simulated lookup table
lookup_table = pd.DataFrame([
    {"Software Name": "Google Chrome", "Package": "googlechrome"},
    {"Software Name": "Mozilla Firefox", "Package": "firefox"},
    {"Software Name": "Zoom", "Package": "zoom"},
    {"Software Name": "7-Zip", "Package": "7zip"},
])

# Initialize patch log in session state
if "patch_log" not in st.session_state:
    st.session_state.patch_log = []

# Check and install Chocolatey
def check_and_install_chocolatey():
    if shutil.which("choco") is None:
        with st.spinner("Installing Chocolatey..."):
            subprocess.run([
                "powershell",
                "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                "[System.Net.ServicePointManager]::SecurityProtocol = "
                "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
                "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            ], shell=True)
        st.success("Chocolatey installed successfully.")
    else:
        st.success("Chocolatey is ready.")

# Apply patch
def apply_patch(package_name):
    check_and_install_chocolatey()
    with st.spinner(f"Patching {package_name}..."):
        subprocess.run(["choco", "upgrade", package_name, "-y"], shell=True)
    st.session_state.patch_log.append({
        "package": package_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success(f"Patch applied to {package_name}")

# Simulate rollback
def rollback_patch():
    if st.session_state.patch_log:
        last_patch = st.session_state.patch_log.pop()
        st.warning(f"Simulated rollback for {last_patch['package']} — {last_patch['timestamp']}")
    else:
        st.info("No patches to roll back.")

# Generate diagnostics report
def generate_diagnostics_report():
    buffer = io.StringIO()
    buffer.write("System Diagnostics Report\n")
    buffer.write("=========================\n\n")
    buffer.write(f"Python version: {sys.version}\n")
    buffer.write(f"Platform: {platform.platform()}\n")
    buffer.write(f"Executable path: {sys.executable}\n\n")

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    buffer.write(f"CPU Usage: {cpu_usage}%\n")
    buffer.write(f"RAM Usage: {ram.percent}% ({ram.used // (1024 ** 2)} MB used of {ram.total // (1024 ** 2)} MB)\n\n")

    buffer.write("Installed Packages:\n")
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    buffer.write(result.stdout + "\n")

    buffer.write("Patch History:\n")
    if st.session_state.patch_log:
        for i, entry in enumerate(st.session_state.patch_log[::-1], 1):
            buffer.write(f"{i}. {entry['package']} — {entry['timestamp']}\n")
    else:
        buffer.write("No patches applied yet.\n")
    return buffer.getvalue()

# Export patch history
def export_patch_history_csv():
    df = pd.DataFrame(st.session_state.patch_log)
    return df.to_csv(index=False).encode("utf-8")

def export_patch_history_json():
    return json.dumps(st.session_state.patch_log, indent=2).encode("utf-8")

# Version checker
def check_versions():
    result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
    return result.stdout

# Sidebar tab selector
with st.sidebar:
    selected_tab = st.radio("Select a tab", ["Patch Dashboard", "System Diagnostics"])

# Patch Dashboard tab
if selected_tab == "Patch Dashboard":
    st.title("🛠️ AI-Driven Patch Dashboard")
    st.subheader("Select software to patch")

    selected = st.selectbox("Software:", lookup_table["Software Name"])
    package_name = lookup_table[lookup_table["Software Name"] == selected]["Package"].values[0]

    if st.button("Apply Patch"):
        apply_patch(package_name)

    if st.button("Rollback Last Patch"):
        rollback_patch()

    st.subheader("📜 Patch History")
    if st.session_state.patch_log:
        for i, entry in enumerate(st.session_state.patch_log[::-1], 1):
            st.write(f"{i}. {entry['package']} — {entry['timestamp']}")
        st.download_button("📤 Export Patch History (CSV)", export_patch_history_csv(), file_name="patch_history.csv")
        st.download_button("📤 Export Patch History (JSON)", export_patch_history_json(), file_name="patch_history.json")
    else:
        st.info("No patches applied yet.")

# System Diagnostics tab
elif selected_tab == "System Diagnostics":
    st.title("🧪 System Diagnostics")

    st.subheader("🔧 Python Environment")
    st.write("Python version:", sys.version)
    st.write("Platform:", platform.platform())
    st.write("Executable path:", sys.executable)

    st.subheader("📊 CPU and RAM Usage")
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    st.metric("CPU Usage", f"{cpu_usage}%")
    st.metric("RAM Usage", f"{ram.percent}%", help=f"{ram.used // (1024 ** 2)} MB used of {ram.total // (1024 ** 2)} MB")

    st.subheader("📦 Installed Packages")
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    st.text(result.stdout)

    st.subheader("🧪 Outdated Packages")
    outdated = check_versions()
    st.text(outdated if outdated else "All packages are up to date.")

    st.subheader("📜 Patch History")
    if st.session_state.patch_log:
        for i, entry in enumerate(st.session_state.patch_log[::-1], 1):
            st.write(f"{i}. {entry['package']} — {entry['timestamp']}")
    else:
        st.info("No patches applied yet.")

    diagnostics_text = generate_diagnostics_report()
    st.download_button("📥 Download Diagnostics Report", diagnostics_text, file_name="diagnostics_report.txt")
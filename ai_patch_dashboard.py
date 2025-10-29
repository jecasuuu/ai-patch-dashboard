import streamlit as st
import subprocess
import shutil
import pandas as pd

# Simulated lookup table
lookup_table = pd.DataFrame([
    {"Software Name": "Google Chrome", "Package": "googlechrome"},
    {"Software Name": "Mozilla Firefox", "Package": "firefox"},
    {"Software Name": "Zoom", "Package": "zoom"},
    {"Software Name": "7-Zip", "Package": "7zip"},
])

# Patch history log
patch_log = []

# Check and install Chocolatey
def check_and_install_chocolatey():
    if shutil.which("choco") is None:
        st.warning("Chocolatey not found. Installing...")
        subprocess.run([
            "powershell",
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = "
            "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        ], shell=True)
    else:
        st.success("Chocolatey is ready.")

# Apply patch
def apply_patch(package_name):
    check_and_install_chocolatey()
    subprocess.run(["choco", "upgrade", package_name, "-y"], shell=True)
    patch_log.append(package_name)
    st.success(f"Patch applied to {package_name}")

# Simulate rollback
def rollback_patch():
    if patch_log:
        last_patch = patch_log.pop()
        st.warning(f"Simulated rollback for {last_patch}")
    else:
        st.info("No patches to roll back.")

# Streamlit UI
st.title("AI-Driven Patch Dashboard")
st.subheader("Select software to patch")

selected = st.selectbox("Software:", lookup_table["Software Name"])
package_name = lookup_table[lookup_table["Software Name"] == selected]["Package"].values[0]

if st.button("Apply Patch"):
    apply_patch(package_name)

if st.button("Rollback Last Patch"):
    rollback_patch()
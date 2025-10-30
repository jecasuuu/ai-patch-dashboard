# AI Patch Dashboard

[![Build Status](https://github.com/your-username/ai-patch-dashboard/actions/workflows/main.yml/badge.svg)](https://github.com/your-username/ai-patch-dashboard/actions)

A low-cost, AI-driven patch automation system designed for SMEs and barangay-level deployment in Metro Manila. Built with accessibility in mind, this dashboard empowers non-technical users to manage software updates, monitor system health, and export diagnostics — all through a clean Streamlit interface.

---

## 🚀 Features

- 🛠 **Patch Automation**  
  Apply software updates via Chocolatey with one click

- 🔄 **Simulated Rollback**  
  Revert the last patch for testing or recovery scenarios

- 🧠 **System Diagnostics Tab**  
  View Python environment, platform info, and installed packages

- 📊 **Live CPU & RAM Usage Metrics**  
  Monitor system performance in real time

- 🧪 **Version Checker**  
  Detect outdated Python packages using `pip list --outdated`

- 📤 **Export Patch History**  
  Download patch logs in CSV or JSON format

- 📥 **Downloadable Diagnostics Report**  
  Generate a full system report for documentation or support

- 🧩 **Streamlit UI for Non-Technical Users**  
  Simple dropdowns, buttons, and tabs — no command line needed

---

## 📸 Screenshots

> _Add your screenshots to a folder named `/assets` and embed them like this:_

![Dashboard Overview](assets/dashboard-overview.png)  
*Main patching interface with dropdown and history*

![Diagnostics Tab](assets/diagnostics-tab.png)  
*System diagnostics with live metrics and export options*

---

## 🧰 How to Run Locally

```bash
pip install -r requirements.txt
streamlit run ai_patch_dashboard.py
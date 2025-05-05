# PyLynx
PyLynx is a Linux-native Python tool for analyzing logs in real time or from history. It detects anomalies, failed logins, and helps with security monitoring.

# 🐾 PyLynx – Linux Log Analyzer

> Real-time, intelligent, and customizable log analysis tool built with Python 🐍, designed to hunt down anomalies in your Linux system like a Lynx prowling for threats 😼.

PyLynx is a mini-SIEM (Security Information and Event Management) system that monitors logs from Linux services like **FTP** and **Apache**, detects failed login attempts, identifies suspicious behavior, and automates alerting and reporting tasks.

---

## ✅ Key Features

- 📡 **Real-time & historical log parsing**
- 🔍 **Filtering** by date, service, IP, or keyword
- 🔁 **Event correlation** (e.g., brute-force login attempts)
- 🚨 **Anomaly alerting** via terminal or email
- 📊 **Data classification & visualizations**
- 🗓️ **Automated reporting** (daily/weekly/monthly)

---

## 🛠️ Tech Stack

| Component       | Description                                      |
|----------------|--------------------------------------------------|
| Language        | Python 3.10+ 🐍                                  |
| OS              | Linux (openSUSE, Ubuntu, Debian) 🐧             |
| Log sources     | `/var/log/`, `journalctl`, `tail`, `grep`       |
| Dependencies    | See below ⬇                                     |

---

## 📦 Dependencies

Install with:

```bash
pip install -r requirements.txt

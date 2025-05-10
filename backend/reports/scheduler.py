import schedule
import time
from datetime import datetime

from backend.logs.log_loader import load_log_file
from backend.reports.report_generator import generate_report

def analyze_logs_job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔍 Running scheduled log analysis...")

    logs_to_check = {
        "apache": "/var/log/apache2/access.log",
        "ftp": "/var/log/vsftpd.log"
    }

    for log_type, path in logs_to_check.items():
        try:
            result = load_log_file(path)
            print(f"[{log_type.upper()}] ✅ {result['valid_lines']} valid | ❌ {result['invalid_lines']} invalid")
        except FileNotFoundError:
            print(f"[{log_type.upper()}] ❌ File not found: {path}")
        except Exception as e:
            print(f"[{log_type.upper()}] ⚠️ Error: {e}")

def report_job(format="pdf", output_path="reports/scheduled_report.pdf"):
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📝 Generating scheduled report...")
    generate_report(format=format, output_path=output_path)

def start_scheduler(log_frequency_minutes=5, report_frequency="daily", report_format="pdf", output_path="reports/scheduled_report.pdf"):
    """
    Starts both the log analyzer and report generator on their own schedules.
    """
    # Schedule log analysis
    schedule.every(log_frequency_minutes).minutes.do(analyze_logs_job)

    # Schedule report generation
    if report_frequency == "daily":
        schedule.every().day.at("08:00").do(report_job, format=report_format, output_path=output_path)
    elif report_frequency == "weekly":
        schedule.every().monday.at("08:00").do(report_job, format=report_format, output_path=output_path)
    elif report_frequency == "monthly":
        schedule.every(30).days.at("08:00").do(report_job, format=report_format, output_path=output_path)
    else:
        print("❌ Unsupported report frequency.")
        return

    print(f"📅 Scheduler started: Log scan every {log_frequency_minutes}min, Report: {report_frequency} at 08:00")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Optional: run directly
if __name__ == "__main__":
    start_scheduler()

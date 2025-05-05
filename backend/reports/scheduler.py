
from backend.reports.report_generator import generate_report
import schedule
import time


def start_scheduler(frequency="daily", format="pdf", output_path="reports/scheduled_report.pdf"):
    """
    Starts the report scheduler based on the frequency selected.
    Supported: daily, weekly, monthly.
    """
    def job():
        print(f"⏰ Running scheduled report: {frequency}")
        generate_report(format=format, output_path=output_path)

    if frequency == "daily":
        schedule.every().day.at("08:00").do(job)
    elif frequency == "weekly":
        schedule.every().monday.at("08:00").do(job)
    elif frequency == "monthly":
        schedule.every(30).days.at("08:00").do(job)
    else:
        print("❌ Unsupported frequency. Use 'daily', 'weekly', or 'monthly'.")
        return

    print(f"📅 Scheduler running in '{frequency}' mode...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # Manually run this to start the scheduling loop
    start_scheduler(frequency="daily", format="pdf", output_path="reports/scheduled_report.pdf")

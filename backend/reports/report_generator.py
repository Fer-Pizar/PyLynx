# backend/reporting/report_generator.py

import pandas as pd
from fpdf import FPDF
import os
import schedule
import time
from datetime import datetime


def generate_mock_data():
    """Simulates log events for report testing."""
    return pd.DataFrame({
        'ip': ['192.168.1.1', '10.0.0.2', '172.16.0.3', '192.168.1.1', '10.0.0.2', '10.0.0.3'],
        'severity': ['error', 'info', 'warning', 'error', 'info', 'warning'],
        'service': ['apache', 'ftp', 'apache', 'ssh', 'ftp', 'apache']
    })


def group_events(df: pd.DataFrame):
    """Groups logs by service, severity, and IP."""
    return df.groupby(['service', 'severity', 'ip']).size().reset_index(name='count')


def export_markdown(grouped_df, output_path):
    """Exports report as a Markdown (.md) file."""
    with open(output_path, "w") as f:
        f.write(f"# 📊 PyLynx Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("| Service | Severity | IP | Count |\n")
        f.write("|---------|----------|----|-------|\n")
        for _, row in grouped_df.iterrows():
            f.write(f"| {row['service']} | {row['severity']} | {row['ip']} | {row['count']} |\n")
    print(f"✅ Markdown report saved to {output_path}")


def export_pdf(grouped_df, output_path):
    """Exports report as a PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="📊 PyLynx Report", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=datetime.now().strftime('%Y-%m-%d %H:%M'), ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    for _, row in grouped_df.iterrows():
        line = f"Service: {row['service']} | Severity: {row['severity']} | IP: {row['ip']} | Events: {row['count']}"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(output_path)
    print(f"✅ PDF report saved to {output_path}")


def generate_report(format="pdf", output_path="report.pdf"):
    """Main function to generate a report."""
    df = generate_mock_data()  # Replace with real DB call later
    grouped = group_events(df)

    if grouped.empty:
        print("⚠️ No data to report.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if format == "pdf":
        export_pdf(grouped, output_path)
    elif format == "md":
        export_markdown(grouped, output_path)
    else:
        print("❌ Unsupported format. Use 'pdf' or 'md'.")


def schedule_report(frequency="daily", format="pdf", output_path="reports/scheduled_report.pdf"):
    """Schedules the report based on the selected frequency."""
    def job():
        print(f"⏰ Generating scheduled {frequency} report...")
        generate_report(format=format, output_path=output_path)

    if frequency == "daily":
        schedule.every().day.at("08:00").do(job)
    elif frequency == "weekly":
        schedule.every().monday.at("08:00").do(job)
    elif frequency == "monthly":
        schedule.every(30).days.at("08:00").do(job)
    else:
        print("❌ Unsupported schedule. Use 'daily', 'weekly', or 'monthly'.")
        return

    print(f"📅 Report scheduler started: {frequency.upper()} mode...")
    while True:
        schedule.run_pending()
        time.sleep(1)


# Manual test block
if __name__ == "__main__":
    # Uncomment one of the following to test manually:

    # generate_report(format="pdf", output_path="reports/manual_report.pdf")
    # generate_report(format="md", output_path="reports/manual_report.md")
    
    # schedule_report(frequency="daily", format="pdf", output_path="reports/scheduled_report.pdf")
    pass

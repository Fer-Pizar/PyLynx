# frontend/cli/cli_interface.py

import argparse
import pandas as pd
from backend.visuals.plot_generator import plot_grouped_events, generate_mock_data
from backend.reports.report_generator import generate_report
from backend.reports.scheduler import start_scheduler


def main():
    parser = argparse.ArgumentParser(description="🦊 PyLynx CLI – Log Analysis & Reporting")
    subparsers = parser.add_subparsers(dest="command")

    # 📊 Subcommand: charts
    charts_cmd = subparsers.add_parser("charts", help="📊 Generate event visualizations")
    charts_cmd.add_argument("type", choices=["top-ips"], help="Chart type shortcut (currently only top-ips)")
    charts_cmd.add_argument("--group-by", default="ip", choices=["ip", "severity", "service"],
                            help="Column to group events by (default: ip)")
    charts_cmd.add_argument("--chart", default="bar", choices=["bar", "pie"],
                            help="Chart format: bar or pie (default: bar)")
    charts_cmd.add_argument("--format", default="png", choices=["png", "html"],
                            help="Export file format: png or html (default: png)")
    charts_cmd.add_argument("--output", help="File path to save the chart (optional)")

    # 📄 Subcommand: report
    report_cmd = subparsers.add_parser("report", help="📄 Generate or schedule system activity reports")
    report_cmd.add_argument("--now", action="store_true", help="Generate report immediately")
    report_cmd.add_argument("--schedule", choices=["daily", "weekly", "monthly"],
                            help="Schedule reports to run periodically")
    report_cmd.add_argument("--format", choices=["pdf", "md"], default="pdf", help="Report format")
    report_cmd.add_argument("--output", default="reports/report_output", help="Output file path without extension")

    args = parser.parse_args()

    #  Handle: charts
    if args.command == "charts":
        if args.type == "top-ips":
            print("📥 Loading log data...")
            df = generate_mock_data()  # Replace with real DB call soon

            if df.empty:
                print("⚠️ No data found to visualize.")
                return

            interactive = args.format == "html"
            print(f"🛠️ Generating {args.chart} chart grouped by {args.group_by}...")

            try:
                plot_grouped_events(
                    data=df,
                    group_by=args.group_by,
                    chart_type=args.chart,
                    export_path=args.output,
                    interactive=interactive
                )

                if args.output:
                    print(f"✅ Chart saved to: {args.output}")
                else:
                    print("📊 Chart displayed successfully.")
            except Exception as e:
                print(f"❌ Failed to generate chart: {e}")

    # 📄 Handle: report
    elif args.command == "report":
        final_output = f"{args.output}.{args.format}"

        if args.now:
            print("📄 Generating manual report...")
            generate_report(format=args.format, output_path=final_output)
            print(f"✅ Manual report generated at: {final_output}")

        elif args.schedule:
            print(f"📅 Starting {args.schedule} scheduler...")
            start_scheduler(frequency=args.schedule, format=args.format, output_path=final_output)

        else:
            print("❌ Please specify either --now or --schedule.")


if __name__ == "__main__":
    main()

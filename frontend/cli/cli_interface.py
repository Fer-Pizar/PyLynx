# frontend/cli/cli_interface.py

import argparse
import pandas as pd
from backend.visuals.plot_generator import plot_grouped_events, generate_mock_data


def main():
    parser = argparse.ArgumentParser(description="🦊 PyLynx CLI – Data Visualization for Logs")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: charts
    charts_cmd = subparsers.add_parser("charts", help="📊 Generate event visualizations")
    charts_cmd.add_argument("type", choices=["top-ips"], help="Chart type shortcut (currently only top-ips)")
    charts_cmd.add_argument("--group-by", default="ip", choices=["ip", "severity", "service"],
                            help="Column to group events by (default: ip)")
    charts_cmd.add_argument("--chart", default="bar", choices=["bar", "pie"],
                            help="Chart format: bar or pie (default: bar)")
    charts_cmd.add_argument("--format", default="png", choices=["png", "html"],
                            help="Export file format: png or html (default: png)")
    charts_cmd.add_argument("--output", help="File path to save the chart (optional)")

    args = parser.parse_args()

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
        else:
            print("🚫 Unknown chart type requested.")


if __name__ == "__main__":
    main()

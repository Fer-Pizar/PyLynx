import argparse
import json
import os
import pandas as pd
import requests
from getpass import getpass
from tabulate import tabulate

from backend.visuals.plot_generator import plot_grouped_events, generate_mock_data
from backend.reports.report_generator import generate_report
from backend.reports.scheduler import start_scheduler
from backend.security.auth import login
from backend.database.db_connector import create_user, get_user_by_username

SESSION_FILE = "session.json"

# 🔐 Utility: Save & load session
def save_session(user):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": user.username, "role": user.role}, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE) as f:
        return json.load(f)

def require_admin():
    session = load_session()
    if not session or session["role"] != "admin":
        raise PermissionError("❌ Admin privileges required.")


def main():
    parser = argparse.ArgumentParser(description="🦊 PyLynx CLI – Log Analysis & Role-Based Access Control")
    subparsers = parser.add_subparsers(dest="command")

    # 📊 Subcommand: charts
    charts_cmd = subparsers.add_parser("charts", help="📊 Generate visualizations from logs")
    charts_cmd.add_argument("type", choices=["top-ips"], help="Chart type (only 'top-ips' available now)")
    charts_cmd.add_argument("--group-by", default="ip", choices=["ip", "severity", "service"], help="Field to group by")
    charts_cmd.add_argument("--chart", choices=["bar", "pie"], default="bar", help="Chart style")
    charts_cmd.add_argument("--format", choices=["png", "html"], default="png", help="Export format")
    charts_cmd.add_argument("--output", help="Output file path")

    # 📄 Subcommand: report
    report_cmd = subparsers.add_parser("report", help="📄 Generate or schedule reports")
    report_cmd.add_argument("--now", action="store_true", help="Generate report immediately")
    report_cmd.add_argument("--schedule", choices=["daily", "weekly", "monthly"], help="Schedule frequency")
    report_cmd.add_argument("--format", choices=["pdf", "md"], default="pdf", help="Report format")
    report_cmd.add_argument("--output", default="reports/report_output", help="Output file path (no extension)")

    # 🔐 login
    login_cmd = subparsers.add_parser("login", help="🔐 Log in to PyLynx")
    login_cmd.add_argument("--username", required=True)
    login_cmd.add_argument("--password", required=True)

    # ➕ create user
    user_cmd = subparsers.add_parser("user", help="👥 Manage users")
    user_cmd.add_argument("action", choices=["add"])
    user_cmd.add_argument("--username", required=True)
    user_cmd.add_argument("--role", choices=["admin", "viewer"], required=True)

    # 👤 whoami
    subparsers.add_parser("whoami", help="👤 Show current logged-in user")

    # 🚪 logout
    subparsers.add_parser("logout", help="🚪 Log out of session")

    # 🌐 api-test
    api_test_cmd = subparsers.add_parser("api-test", help="🌐 Test the REST API /events")
    api_test_cmd.add_argument("--start", help="Start date (YYYY-MM-DD)")
    api_test_cmd.add_argument("--end", help="End date (YYYY-MM-DD)")
    api_test_cmd.add_argument("--ip", help="Filter by IP address")
    api_test_cmd.add_argument("--service", help="Filter by service")
    api_test_cmd.add_argument("--page", type=int, default=1)
    api_test_cmd.add_argument("--limit", type=int, default=10)

    # 📘 api-doc
    subparsers.add_parser("api-doc", help="📘 Show usage documentation for the API")

    args = parser.parse_args()

    # ======= CHARTS =======
    if args.command == "charts":
        df = generate_mock_data()
        if df.empty:
            print("⚠️ No data found.")
            return
        interactive = args.format == "html"
        plot_grouped_events(df, group_by=args.group_by, chart_type=args.chart,
                            export_path=args.output, interactive=interactive)
        if args.output:
            print(f"✅ Chart saved to: {args.output}")
        else:
            print("📊 Chart displayed successfully.")

    # ======= REPORTS =======
    elif args.command == "report":
        final_path = f"{args.output}.{args.format}"
        if args.now:
            generate_report(format=args.format, output_path=final_path)
            print(f"✅ Report generated at: {final_path}")
        elif args.schedule:
            try:
                require_admin()
                start_scheduler(frequency=args.schedule, format=args.format, output_path=final_path)
            except Exception as e:
                print(f"❌ Failed to start scheduler: {e}")
        else:
            print("❌ Please provide --now or --schedule.")

    # ======= LOGIN =======
    elif args.command == "login":
        try:
            user = login(args.username, args.password)
            save_session(user)
            print(f"✅ Logged in as {user.username} ({user.role})")
        except Exception as e:
            print(f"❌ Login failed: {e}")

    # ======= USER ADD =======
    elif args.command == "user":
        try:
            require_admin()
            password = getpass("Enter password: ")
            create_user(args.username, password, args.role)
        except Exception as e:
            print(f"❌ Cannot add user: {e}")

    # ======= WHOAMI =======
    elif args.command == "whoami":
        session = load_session()
        if session:
            print(f"👤 You are logged in as: {session['username']} (role: {session['role']})")
        else:
            print("⚠️ No active session.")

    # ======= LOGOUT =======
    elif args.command == "logout":
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            print("🚪 Logged out.")
        else:
            print("⚠️ No active session.")

    # ======= API TEST =======
    elif args.command == "api-test":
        params = {
            "start_date": args.start,
            "end_date": args.end,
            "ip": args.ip,
            "service": args.service,
            "page": args.page,
            "limit": args.limit
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        try:
            response = requests.get("http://127.0.0.1:5000/api/events", params=clean_params)
            if response.status_code != 200:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return
            data = response.json()
            print(f"📄 Total: {data['total']} | Page {data['current_page']} of {data['pages']}")
            print(tabulate(data['results'], headers="keys", tablefmt="grid"))
        except Exception as e:
            print(f"❌ Failed to connect: {e}")

    # ======= API DOC =======
    elif args.command == "api-doc":
        print(\"\"\"
📘 API Usage Guide

📍 Endpoint:
  GET /api/events

🔍 Filters:
  --start       Filter from date (e.g. 2025-05-01)
  --end         Filter to date (e.g. 2025-05-04)
  --ip          Filter by IP address
  --service     Filter by service name
  --page        Page number (default: 1)
  --limit       Number of results per page (default: 10)

▶️ Example CLI:
  pylinx api-test --start 2025-05-01 --ip 10.0.0.1 --service apache --page 2 --limit 5
\"\"\")

if __name__ == "__main__":
    main()

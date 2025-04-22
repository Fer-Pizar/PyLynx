import argparse

def main():
    parser = argparse.ArgumentParser(description="🐾 PyLynx - Linux Log Analyzer")
    parser.add_argument("--file", required=True, help="Path to the log file (e.g., /var/log/auth.log)")
    parser.add_argument("--filter", required=False, help="Keyword to search for in the logs")

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as log_file:
            for line in log_file:
                if args.filter:
                    if args.filter.lower() in line.lower():
                        print(line.strip())
                else:
                    print(line.strip())
    except FileNotFoundError:
        print("🚫 Log file not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

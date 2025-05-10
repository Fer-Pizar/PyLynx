from flask import Blueprint, request, jsonify
from backend.logs.log_loader import load_log_file

api = Blueprint('api', __name__)

@api.route("/analyze-log", methods=["GET"])
def analyze_log():
    """
    Reads and analyzes a system log file (Apache or FTP) directly from disk.
    Example: GET /analyze-log?type=apache
    """
    log_type = request.args.get("type")

    if log_type == "apache":
        path = "/var/log/apache2/access.log"
    elif log_type == "ftp":
        path = "/var/log/vsftpd.log"
    else:
        return jsonify({"error": "Invalid log type. Use ?type=apache or ?type=ftp"}), 400

    try:
        result = load_log_file(path)
        return jsonify(result)
    except FileNotFoundError:
        return jsonify({"error": f"Log file not found at {path}"}), 404
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

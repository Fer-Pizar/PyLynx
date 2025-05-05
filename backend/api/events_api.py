from flask import Blueprint, request, jsonify
from backend.database.db_config import Session
from backend.database.models.event_model import Event
from sqlalchemy import and_
from datetime import datetime

events_api = Blueprint('events_api', __name__)

@events_api.route('/events', methods=['GET'])
def get_events():
    session = Session()
    try:
        # Query parameters
        ip = request.args.get('ip')
        service = request.args.get('service')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        filters = []

        if ip:
            filters.append(Event.ip == ip)
        if service:
            filters.append(Event.service == service)
        if start_date:
            filters.append(Event.timestamp >= datetime.fromisoformat(start_date))
        if end_date:
            filters.append(Event.timestamp <= datetime.fromisoformat(end_date))

        query = session.query(Event).filter(and_(*filters)) if filters else session.query(Event)

        total = query.count()
        events = query.order_by(Event.timestamp.desc()).offset(offset).limit(limit).all()

        results = [{
            "timestamp": e.timestamp.isoformat(),
            "ip": e.ip,
            "severity": e.severity,
            "service": e.service,
            "message": e.message
        } for e in events]

        return jsonify({
            "total": total,
            "pages": (total + limit - 1) // limit,
            "current_page": page,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

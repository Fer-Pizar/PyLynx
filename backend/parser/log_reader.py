from fastapi import APIRouter
from backend.parser.log_reader import read_logs

router = APIRouter()

@router.get("/logs")
def get_logs():
    return read_logs("/var/log/auth.log")

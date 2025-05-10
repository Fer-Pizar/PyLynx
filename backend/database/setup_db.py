from backend.database.db_config import engine, Base
from backend.database.models.event_model import Event

# 🔧 Create all tables defined with Base
Base.metadata.create_all(engine)

print("Tables created successfully! Your DB is ready")

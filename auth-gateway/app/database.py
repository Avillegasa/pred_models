"""
Database configuration and session management
"""
import json
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    """Run database migrations for schema changes"""
    inspector = inspect(engine)

    # Check if users table exists
    if 'users' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('users')]

        # Migration: Add permissions column if it doesn't exist
        if 'permissions' not in columns:
            print("Running migration: Adding 'permissions' column to users table...")
            default_permissions = json.dumps({
                "dashboard": True,
                "predictions": False,
                "reports": True,
                "alerts": True
            })
            with engine.connect() as conn:
                conn.execute(text(
                    f"ALTER TABLE users ADD COLUMN permissions TEXT DEFAULT '{default_permissions}'"
                ))
                conn.commit()
            print("Migration completed: 'permissions' column added.")


def init_db():
    """Initialize database tables"""
    from .models import user, file, report, alert, prediction  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Run migrations for existing databases
    run_migrations()

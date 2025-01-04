from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

def initialize_database():
    engine = create_engine("sqlite:///./database/plex_invite.db")
    
    # Check if database exists and has tables
    inspector = inspect(engine)
    tables_exist = inspector.get_table_names()
    
    if not tables_exist:
        print("Initializing database...")
        # Run all migrations
        alembic_cfg = Config("database/migrations/alembic.ini")
        command.upgrade(alembic_cfg, 'head')
        print("Database initialized successfully")

if __name__ == "__main__":
    initialize_database()
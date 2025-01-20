from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add these imports
from app.core.config import settings
from app.models.base import Base
import app.models  # This will import all models

# this is the Alembic Config object
config = context.config

# Update the database URL from your settings
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Update the target_metadata
target_metadata = Base.metadata

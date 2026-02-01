from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so SQLAlchemy registers tables before create_all.
from app.models import (  # noqa: F401,E402
    file_summary,
    repo_documentation,
    repository,
    user,
)

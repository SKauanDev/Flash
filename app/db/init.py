from app.db.models import Base
from app.db.session import engine

# Import models that register their SQLAlchemy metadata before create_all.
from app.tools.tasks import Task  # noqa: F401,E402


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

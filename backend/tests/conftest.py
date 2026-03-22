import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()

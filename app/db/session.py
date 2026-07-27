from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings
database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
    query={"charset": "utf8mb4"},
)
engine = create_engine(
    database_url,
    echo=True, 
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
)
class Base(DeclarativeBase):
    pass

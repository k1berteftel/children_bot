import datetime
from typing import Literal

from sqlalchemy import BigInteger, VARCHAR, ForeignKey, DateTime, Boolean, Column, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(VARCHAR)
    name: Mapped[str] = mapped_column(VARCHAR)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    active: Mapped[int] = mapped_column(Integer, default=1)
    activity: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    entry: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    join: Mapped[str] = mapped_column(VARCHAR, default=None, nullable=True)
    sub: Mapped["UserSubTable"] = relationship('UserSubTable', lazy="selectin", cascade='all, delete', uselist=False)


class UserSubTable(Base):
    __tablename__ = 'user-sub-data'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    rate: Mapped[Literal['child', 'recipe', 'both']] = mapped_column(VARCHAR, nullable=True)
    sub_days: Mapped[int] = mapped_column(Integer)
    days_count: Mapped[int] = mapped_column(Integer, default=1)
    freeze_days: Mapped[int] = mapped_column(Integer, default=10)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class DeeplinksTable(Base):
    __tablename__ = 'deeplinks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(VARCHAR)
    link: Mapped[str] = mapped_column(VARCHAR)
    entry: Mapped[int] = mapped_column(BigInteger, default=0)
    earned: Mapped[int] = mapped_column(Integer, default=0)
    create: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())


class AdminsTable(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)


class OneTimeLinksIdsTable(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)


class StaticTable(Base):
    __tablename__ = 'static'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    sum: Mapped[int] = mapped_column(Integer, default=0)
    buys: Mapped[int] = mapped_column(Integer, default=0)
    child_buys: Mapped[int] = mapped_column(Integer, default=0)
    recipe_buys: Mapped[int] = mapped_column(Integer, default=0)


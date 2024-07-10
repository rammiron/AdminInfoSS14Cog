from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)
    last_seen_user_name = Column(Text, nullable=False)


class Admin(Base):
    __tablename__ = "admin"
    user_id = Column(Text, nullable=False, primary_key=True)
    title = Column(Text)


class ServerBan(Base):
    __tablename__ = "server_ban"
    server_ban_id = Column(Integer, nullable=False, primary_key=True)
    ban_time = Column(Text, nullable=False)
    expiration_time = Column(Text)
    banning_admin = Column(Text)
    player_user_id = Column(Text)
    reason = Column(Text)
    round_id = Column(Integer)


class ServerRoleBan(Base):
    __tablename__ = "server_role_ban"
    server_role_ban_id = Column(Integer, nullable=False, primary_key=True)
    ban_time = Column(Text, nullable=False)
    expiration_time = Column(Text)
    banning_admin = Column(Text)
    player_user_id = Column(Text)
    reason = Column(Text)
    role_id = Column(Text, nullable=False)
    round_id = Column(Integer)

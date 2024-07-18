from sqlalchemy import Column, Integer, Text, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DiscordUser(Base):
    __tablename__ = "discord_user"
    discord_id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Text, nullable=False)
    activated = Column(Boolean, nullable=False, default=True)
    id = Column(Integer, nullable=False, autoincrement=True)


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
    ban_time = Column(DateTime, nullable=False)
    expiration_time = Column(DateTime)
    banning_admin = Column(Text)
    player_user_id = Column(Text)
    reason = Column(Text)
    round_id = Column(Integer)


class ServerRoleBan(Base):
    __tablename__ = "server_role_ban"
    server_role_ban_id = Column(Integer, nullable=False, primary_key=True)
    ban_time = Column(DateTime, nullable=False)
    expiration_time = Column(DateTime)
    banning_admin = Column(Text)
    player_user_id = Column(Text)
    reason = Column(Text)
    role_id = Column(Text, nullable=False)
    round_id = Column(Integer)

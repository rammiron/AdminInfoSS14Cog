from .models import Player, Admin, Server_ban, Server_role_ban
from utils.db_alchemy import get_db


def get_admins_list():
    db = next(get_db())
    return db.query(Player.last_seen_user_name, Admin.title).join(Admin, Player.user_id == Admin.user_id).all()


def get_player_name_by_id(user_id: int):
    db = next(get_db())
    return db.query(Player.last_seen_user_name).filter(Player.user_id == user_id).first()[0]


def get_user_id_by_name(name: str):
    db = next(get_db())
    return db.query(Player.user_id).filter(Player.last_seen_user_name == name).first()[0]


def get_user_bans(user_id: int):
    db = next(get_db())
    return db.query(Server_ban).filter(Server_ban.player_user_id == user_id).all()


def get_user_job_bans(user_id: int):
    db = next(get_db())
    return db.query(Server_role_ban).filter(Server_role_ban.player_user_id == user_id).all()


def get_all_bans():
    db = next(get_db())
    return db.query(Server_ban).all()


def get_all_job_bans():
    db = next(get_db())
    return db.query(Server_role_ban).all()

from sqlalchemy import func

from .models import Player, Admin, ServerBan, ServerRoleBan
from utils.db_alchemy import get_db



def ds_user_was_found_in_db:

def get_user_by_name(name):
    db = next(get_db())
    user = db.query(Player).filter(Player.last_seen_user_name == name)
    if user is not None:
        return user
    else:
        return None


def get_player_name_by_id(user_id: int):
    db = next(get_db())
    return db.query(Player.last_seen_user_name).filter(Player.user_id == user_id).first()[0]


def get_user_id_by_name(name: str):
    db = next(get_db())
    user_id = db.query(Player.user_id).filter(Player.last_seen_user_name == name).first()
    if user_id is None:
        return None
    return user_id[0]


def get_user_bans(start_date, end_date, user_id):
    db = next(get_db())
    return db.query(ServerBan).filter(ServerBan.ban_time > start_date, ServerBan.ban_time < end_date,
                                      ServerBan.player_user_id == user_id).limit(100).all()


def get_user_job_bans(start_date, end_date, user_id):
    db = next(get_db())
    return db.query(ServerRoleBan).filter(ServerRoleBan.ban_time > start_date, ServerRoleBan.ban_time < end_date,
                                          ServerRoleBan.player_user_id == user_id).limit(100).all()


def get_all_bans_count(start_date, end_date):
    db = next(get_db())
    return (db.query(func.count(ServerBan.server_ban_id), ServerBan.banning_admin, Player.last_seen_user_name).
            join(ServerBan, Player.user_id == ServerBan.banning_admin).
            filter(start_date < ServerBan.ban_time, ServerBan.ban_time < end_date).
            group_by(ServerBan.banning_admin, Player.last_seen_user_name).
            order_by(func.count(ServerBan.server_ban_id).desc()).
            limit(10).all())


def get_all_job_bans_count(start_date, end_date):
    db = next(get_db())
    return (
        db.query(func.count(ServerRoleBan.server_role_ban_id), ServerRoleBan.banning_admin, Player.last_seen_user_name).
        join(ServerRoleBan, Player.user_id == ServerRoleBan.banning_admin).
        filter(start_date < ServerRoleBan.ban_time, ServerRoleBan.ban_time < end_date).
        group_by(ServerRoleBan.banning_admin, Player.last_seen_user_name).
        order_by(func.count(ServerRoleBan.server_role_ban_id).desc()).
        limit(10).all())


def get_admin_bans(user_id, start_date, end_date):
    db = next(get_db())
    return (db.query(ServerBan).filter(ServerBan.ban_time > start_date, ServerBan.ban_time < end_date,
                                       ServerBan.banning_admin == user_id).
            limit(100).all())


def get_admin_role_bans(user_id, start_date, end_date):
    db = next(get_db())
    return (db.query(ServerRoleBan).filter(ServerRoleBan.ban_time > start_date, ServerRoleBan.ban_time < end_date,
                                           ServerRoleBan.banning_admin == user_id).
            limit(100).all())

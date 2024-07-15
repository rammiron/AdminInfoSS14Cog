import datetime
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.commands import Option

if "cogs" in __name__:
    from .utils import crud
    from .utils import models
else:
    from utils import crud
    from utils import models


def time_difference_restruct(time_difference: timedelta):
    time_dict = {
        "minute": 60,
        "hour": 3600,
        "day": 86400
    }
    time_to_seconds = time_difference.total_seconds()
    seconds_to_int = int(time_to_seconds)
    if time_dict["minute"] <= seconds_to_int < time_dict["hour"]:
        minutes = int(seconds_to_int / time_dict["minute"])
        return f"{minutes} мин."
    elif time_dict["day"] > seconds_to_int >= time_dict["hour"]:
        hours = seconds_to_int / time_dict["hour"]
        return f"{hours:.1f} ч."
    elif time_dict["day"] <= seconds_to_int:
        days = seconds_to_int / time_dict["day"]
        return f"{days:.0f} д."


class AdminInfoSs14Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # the first function is to get a list of administrators on the server
    @commands.slash_command(name="admins_list",
                            description=
                            "Выводит список администрации сервера"
                            " и наименования отображаемые в"
                            "adminwho.")
    async def get_admins_list(self, ctx: discord.ApplicationContext):
        # region embed
        result_embed = discord.Embed(
            title="Список администрации на данном сервере:",
            colour=discord.Colour.dark_green()
        )
        # endregion

        # this is tuple with all fields from table "admin"
        admins = crud.get_admins_list()
        # this is string with result
        # this is a loop to get the administrator's name by id
        for admin in admins:
            result_embed.add_field(name=f"\n{admin[0].last_seen_user_name} - {admin[1] if admin[1] is not None else 'наименования нет.'}",
                                   value="", inline=False)
        await ctx.respond(embed=result_embed)

    @commands.slash_command(name="user_bans_list",
                            description="Выводит список банов пользователя "
                                        "по имени за определенный промежуток времени.")
    async def get_user_bans(self, ctx: discord.ApplicationContext, username: Option(str, "Сикей игрока."),
                            start_date: Option(str, "Начало временного диапазона для поиска банов. Формат времени:"
                                                    "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                            end_date: Option(str, "Конец временного диапазона для поиска банов. Формат времени:"
                                                  "\"ГГГГ-ММ-ДД\"")
                            = str(datetime.today().date())):

        user = crud.get_user_id_by_name(username)
        if user is None:
            await ctx.respond(f"Пользователь **{username}** не найден. Убедитесь что правильно ввели сикей.")
            return
        await ctx.defer()

        if start_date == '2000-01-01':
            embed_start_date = ""
        else:
            embed_start_date = f"с {start_date} "
        if end_date == str(datetime.today().date()):
            embed_end_date = "до сегодняшнего дня."
        else:
            embed_end_date = f"до {end_date}."
        if start_date == str(datetime.today().date()) and end_date == str(datetime.today().date()):
            embed_start_date = ""
            embed_end_date = "за сегодняшний день."
        elif start_date == end_date:
            embed_start_date = ""
            embed_end_date = f"за {end_date}."

        # region embed
        result_embed = discord.Embed(
            title=f"Первые 100 банов *{username}* " + embed_start_date + embed_end_date,
            color=discord.Colour.red()
        )
        # endregion

        start_date_formatted = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_formatted = datetime.strptime(end_date, "%Y-%m-%d")
        bans = crud.get_user_bans(start_date_formatted, end_date_formatted, crud.get_user_id_by_name(username))
        if len(bans) <= 0 or bans is None:
            await ctx.respond(f"У {username} {embed_start_date}"
                              f"{embed_end_date.split('.')[0]} банов не обнаружено.")
            return
        bans_count = 0
        for ban in bans:

            bans_count += 1
            time_difference = "перманентный"
            if ban.expiration_time is not None:
                date_format = "%Y-%m-%d %H:%M:%S"
                expiration_time = datetime.strptime(str(ban.expiration_time).split('.')[0], date_format)
                ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)
                time_difference = expiration_time - ban_time
                time_difference = time_difference_restruct(time_difference)

            banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)
            result_embed.add_field(name=f"**Бан {bans_count}**", value=f"Раунд: {ban.round_id}."
                                                                       f"\nВремя бана: {time_difference}"
                                                                       f"\nПричина: {ban.reason}."
                                                                       f"\nВремя выдачи:"
                                                                       f" {str(ban.ban_time).split('.')[0]}."
                                                                       f"\nБан выдал: {banning_admin_name}.")
        await ctx.respond(embed=result_embed)

    @commands.slash_command(name="user_job_bans_list")
    async def get_user_jb(self, ctx: discord.ApplicationContext, username: Option(str, "Сикей игрока."),
                          start_date: Option(str, "Начало временного диапазона для поиска банов. Формат времени:"
                                                  "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                          end_date: Option(str, "Конец временного диапазона для поиска банов. Формат времени:"
                                                "\"ГГГГ-ММ-ДД\"")
                          = str(datetime.today().date())):
        user = crud.get_user_id_by_name(username)
        if user is None:
            await ctx.respond(f"Пользователь **{username}** не найден. Убедитесь что правильно ввели сикей.")
            return
        await ctx.defer()

        if start_date == '2000-01-01':
            embed_start_date = ""
        else:
            embed_start_date = f"с {start_date} "
        if end_date == str(datetime.today().date()):
            embed_end_date = "до сегодняшнего дня."
        else:
            embed_end_date = f"до {end_date}."
        if start_date == str(datetime.today().date()) and end_date == str(datetime.today().date()):
            embed_start_date = ""
            embed_end_date = "за сегодняшний день."
        elif start_date == end_date:
            embed_start_date = ""
            embed_end_date = f"за {end_date}."

        # region embed
        result_embed = discord.Embed(
            title=f"Первые 100 банов ролей *{username}* " + embed_start_date + embed_end_date,
            color=discord.Colour.dark_blue()
        )
        # endregion

        start_date_formatted = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_formatted = datetime.strptime(end_date, "%Y-%m-%d")
        bans = crud.get_user_job_bans(start_date_formatted, end_date_formatted, crud.get_user_id_by_name(username))
        if len(bans) <= 0 or bans is None:
            await ctx.respond(f"У {username} {embed_start_date}"
                              f"{embed_end_date.split('.')[0]} банов ролей не обнаружено.")
            return
        bans_count = 0
        for ban in bans:

            bans_count += 1
            time_difference = "перманентный."
            if ban.expiration_time is not None:
                date_format = "%Y-%m-%d %H:%M:%S"
                expiration_time = datetime.strptime(str(ban.expiration_time).split('.')[0], date_format)
                ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)
                time_difference = expiration_time - ban_time
                time_difference = time_difference_restruct(time_difference)

            banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)
            result_embed.add_field(name=f"**Бан {bans_count}**", value=f"Раунд: {ban.round_id}."
                                                                       f"\nВремя бана: {time_difference}"
                                                                       f"\nПричина: {ban.reason}."
                                                                       f"\nРоль: {str(ban.role_id).split(':')[1]}"
                                                                       f"\nВремя выдачи:"
                                                                       f" {str(ban.ban_time).split('.')[0]}."
                                                                       f"\nБан выдал: {banning_admin_name}."
                                   , inline=False)
        await ctx.respond(embed=result_embed)

    # this function displays top admins by ban
    @commands.slash_command(name="top_bans_admin", description="Отображает топ админов по банам.")
    async def get_top_of_bans_between_admins(self, ctx: discord.ApplicationContext,
                                             start_date: Option(str,
                                                                "Начало временного диапазона для поиска банов. Формат "
                                                                "времени:"
                                                                "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                                             end_date: Option(str,
                                                              "Конец временного диапазона для поиска банов. Формат "
                                                              "времени:"
                                                              "\"ГГГГ-ММ-ДД\"") = str(datetime.today().date())):

        if start_date == '2000-01-01':
            embed_start_date = ""
        else:
            embed_start_date = f"с {start_date} "
        if end_date == str(datetime.today().date()):
            embed_end_date = "до сегодняшнего дня."
        else:
            embed_end_date = f"до {end_date}."
        if start_date == str(datetime.today().date()) and end_date == str(datetime.today().date()):
            embed_start_date = ""
            embed_end_date = "за сегодняшний день."
        elif start_date == end_date:
            embed_start_date = ""
            embed_end_date = f"за {end_date}."
        # region embed
        result_embed = discord.Embed(
            title=f"Топ админов по банам {embed_start_date} {embed_end_date}",
            colour=discord.Colour.dark_gold()
        )

        # endregion

        admins_dict = {}

        for admin in crud.get_admins_list():
            bans = crud.get_admin_bans(admin[0].user_id, start_date, end_date)
            if len(bans) <= 0:
                continue
            admins_dict[admin[0].last_seen_user_name] = len(bans)
        if len(admins_dict) <= 0:
            await ctx.respond("Баны не обнаружены.")
            return
        sorted_admin_dict = dict(sorted(admins_dict.items(), key=lambda item: item[1], reverse=True))
        index = 1
        for admin in sorted_admin_dict:
            # formating result string
            result_embed.add_field(name=f"{index}e место:", value=f" **{admin}** выдал банов:"
                                                                  f" {sorted_admin_dict[admin]}", inline=False)
            index += 1

        await ctx.respond(embed=result_embed)

    # this function displays top admins by job ban
    @commands.slash_command(name="top_job_bans_admin", description="Отображает топ админов по банам ролей.")
    async def get_top_of_job_bans_between_admins(self, ctx: discord.ApplicationContext,
                                                 start_date: Option(str,
                                                                    "Начало временного диапазона для поиска"
                                                                    " банов. Формат времени:"
                                                                    "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                                                 end_date: Option(str,
                                                                  "Конец временного диапазона для поиска "
                                                                  "банов. Формат времени:"
                                                                  "\"ГГГГ-ММ-ДД\"") = str(datetime.today().date())):
        if start_date == '2000-01-01':
            embed_start_date = ""
        else:
            embed_start_date = f"с {start_date} "
        if end_date == str(datetime.today().date()):
            embed_end_date = "до сегодняшнего дня."
        else:
            embed_end_date = f"до {end_date}."
        if start_date == str(datetime.today().date()) and end_date == str(datetime.today().date()):
            embed_start_date = ""
            embed_end_date = "за сегодняшний день."
        elif start_date == end_date:
            embed_start_date = ""
            embed_end_date = f"за {end_date}."
        # region embed
        result_embed = discord.Embed(
            title=f"Топ админов по банам ролей {embed_start_date} {embed_end_date}",
            colour=discord.Colour.dark_gold()
        )

        # endregion

        admins_dict = {}

        for admin in crud.get_admins_list():
            bans = crud.get_admin_role_bans(admin[0].user_id, start_date, end_date)
            if len(bans) <= 0:
                continue
            admins_dict[admin[0].last_seen_user_name] = len(bans)
        if len(admins_dict) <= 0:
            await ctx.respond("Баны ролей не обнаружены.")
            return
        sorted_admin_dict = dict(sorted(admins_dict.items(), key=lambda item: item[1], reverse=True))
        index = 1
        for admin in sorted_admin_dict:
            # formating result string
            result_embed.add_field(name=f"{index}e место:", value=f" **{admin}** выдал банов ролей:"
                                                                  f" {sorted_admin_dict[admin]}", inline=False)
            index += 1

        await ctx.respond(embed=result_embed)

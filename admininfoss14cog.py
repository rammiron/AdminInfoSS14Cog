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

    @commands.slash_command(name="user_bans_list",
                            description="Выводит список банов пользователя "
                                        "по имени за определенный промежуток времени.")
    async def get_user_bans(self, ctx: discord.ApplicationContext, username: Option(str, "Сикей игрока."),
                            start_date: Option(str, "Начало временного диапазона для поиска банов. Формат времени:"
                                                    "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                            end_date: Option(str, "Конец временного диапазона для поиска банов. Формат времени:"
                                                  "\"ГГГГ-ММ-ДД\"")
                            = str(datetime.today().date())):

        user_id = crud.get_user_id_by_name(username)

        if user_id is None:
            await ctx.respond(f"Пользователь **{username}** не найден. Убедитесь что правильно ввели сикей.")
            return
        await ctx.defer()
        if not crud.ds_user_was_found_in_db(ctx.author.id):
            await ctx.respond(f"{ctx.author.mention}, "
                              f"похоже ваш дискорд не привязан. Привяжите его написав в лс боту с помощью команды "
                              f"\"/gift\".", ephemeral=True)
            return
        if not crud.ds_user_was_player_owner(ctx.author.id, user_id):
            await ctx.respond(f"{ctx.author.mention}, вы не можете просмотреть чужой список банов.")
            return
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
        user_id = crud.get_user_id_by_name(username)

        await ctx.defer()

        if user_id is None:
            await ctx.respond(f"Пользователь **{username}** не найден. Убедитесь что правильно ввели сикей.")
            return

        if not crud.ds_user_was_found_in_db(ctx.author.id):
            await ctx.respond(f"Похоже ваш дискорд не привязан. Привяжите его написав в лс боту с помощью команды "
                              f"\"/gift\".", ephemeral=True)
            return
        if not crud.ds_user_was_player_owner(ctx.author.id, user_id):
            await ctx.respond(f"Извините, вы не можете просмотреть чужой список банов.", ephemeral=True)
            return

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
                expiration_time = ban.expiration_time.strptime(date_format)
                ban_time = ban.ban_time.striptime(date_format)
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
        index = 1
        top_bans_list = crud.get_all_bans_count(start_date, end_date)
        for ban_count_tuple in top_bans_list:
            # formating result string
            result_embed.add_field(name=f"{index}e место:", value=f" **{ban_count_tuple[2]}** выдал банов:"
                                                                  f" {ban_count_tuple[0]}", inline=False)
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

        index = 1
        top_bans_list = crud.get_all_job_bans_count(start_date, end_date)
        for ban_count_tuple in top_bans_list:
            # formating result string
            result_embed.add_field(name=f"{index}e место:", value=f" **{ban_count_tuple[2]}** выдал банов ролей:"
                                                                  f" {ban_count_tuple[0]}", inline=False)
            index += 1

        await ctx.respond(embed=result_embed)

    @commands.slash_command(name="check_admin_stats", description="Отображает статистику администратора.")
    async def get_admin_stats(self, ctx: discord.ApplicationContext,
                              nickname: Option(str, "Игровое имя администратора."),
                              start_date: Option(str,
                                                 "Начало временного диапазона"
                                                 " для поиска. Формат времени:"
                                                 " \"ГГГГ-ММ-ДД\"") = '2000-01-01',
                              end_date: Option(str, "Конец временного диапазона для поиска. Формат времени:"
                                                    " \"ГГГГ-ММ-ДД\"") = str(datetime.today().date())):
        user_id = crud.get_user_id_by_name(nickname)
        if user_id is None:
            await ctx.respond(f"Пользователь с ником {nickname} не найден.")
            return
        if crud.user_id_belongs_admin(user_id) is False:
            await ctx.respond(f"Пользователь с ником {nickname} не является администратором.")
            return
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
        bans = crud.get_admin_bans_count(user_id, start_date, end_date)
        job_bans = crud.get_admin_job_bans_count(user_id, start_date, end_date)
        admin_notes = crud.get_admin_notes_count(user_id, start_date, end_date)

        result_embed = discord.Embed(
            title=f"Статистика администратора {nickname} {embed_start_date} {embed_end_date}\n"
                  f"Количество банов: {bans}\n"
                  f"Количество джоббанов: {job_bans}\n"
                  f"Количество предупреждений: {admin_notes}",
            colour=discord.Colour.dark_gold()
        )
        await ctx.respond(embed=result_embed)

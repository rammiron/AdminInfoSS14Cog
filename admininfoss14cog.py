import datetime
from datetime import datetime

import discord
from discord.ext import commands
from discord.commands import Option

from utils.db_alchemy import engine

if "cogs" in __name__:
    from .utils import crud
    from .utils.models import Base
else:
    from utils import crud
    from utils.models import Base




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
        # this is tuple with all fields from table "admin"
        admins = crud.get_admins_list()
        # this is string with result
        result = "**Список администрации на данном сервере:** "
        # this is a loop to get the administrator's name by id
        for admin in admins:
            result += f"\n{admin[0]} - {admin[1] if admin[1] is not None else "Наименования нет."}"
        print(admins)
        await ctx.respond(result)


    @commands.Cog.listener()
    async def on_ready(self):
        Base.metadata.create_all(engine)


    # function for displaying a list
    # of user bans by name for a certain period of time
    @commands.slash_command(name="user_bans_list",
                       description="Выводит список банов пользователя "
                                   "по имени за определенный промежуток времени.")
    async def get_user_bans(self, ctx: discord.ApplicationContext, username: Option(str, "Сикей игрока."),
                            start_date: Option(str, "Начало временного диапазона для поиска банов. Формат времени:"
                                                    "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                            end_date: Option(str, "Конец временного диапазона для поиска банов. Формат времени:"
                                                  "\"ГГГГ-ММ-ДД\"")
                            = str(datetime.today().date())):
        # getting the user ID
        user_id = crud.get_user_id_by_name(username)
        # checking the presence of this user in the table
        if user_id is None:
            # this is message responding when user not detected
            await ctx.respond("Пользователь не найден.")
            return
        await ctx.defer()
        # this is string with result
        result = f"**Баны {username}:**\n-----------"
        # this is tuple with all bans in the table
        user_bans = crud.get_user_bans(user_id)
        bans_got = 0
        datetime_end_date = (
            datetime.strptime(end_date, "%Y-%m-%d").date())
        datetime_start_date = (
            datetime.strptime(start_date, "%Y-%m-%d").date())
        # checking the presence values on the tuple
        if len(user_bans) <= 0:
            await ctx.respond(f"У пользователя {username} не обнаружено банов на данном промежутке времени.")
            return
        for ban in user_bans:
            date_format = "%Y-%m-%d %H:%M:%S"
            ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)

            if datetime_end_date >= ban_time.date() > datetime_start_date:
                # see field name :)
                date_format = "%Y-%m-%d %H:%M:%S"
                # also with this
                expiration_time = datetime.strptime(ban.expiration_time.split('.')[0], date_format)
                # calculating the difference between the dates
                time_difference = expiration_time - ban_time

                banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)

                # update result string
                result += (f"\n**Бан раунда #{ban.round_id}.** \n**Причина:** \"{ban.reason}\"."
                           f" \n**Время бана:** {time_difference}\n**Выдан:** {ban_time}s\n**Бан выдал**: "
                           f"{banning_admin_name}"
                           f"\n-----------")
                bans_got += 1
        if bans_got == 0:
            await ctx.respond(f"У пользователя {username} не обнаружено банов на данном промежутке времени.")
            return
        # respond result
        await ctx.respond(result)

    @commands.slash_command(name="user_job_bans_list")
    async def get_user_jb(self, ctx: discord.ApplicationContext, username: Option(str, "Сикей игрока."),
                          start_date: Option(str, "Начало временного диапазона для поиска банов. Формат времени:"
                                                  "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                          end_date: Option(str, "Конец временного диапазона для поиска банов. Формат времени:"
                                                "\"ГГГГ-ММ-ДД\"")
                          = str(datetime.today().date())):
        # getting the user ID
        user_id = crud.get_user_id_by_name(username)
        # checking the presence of this user in the table
        if user_id is None:
            # this is message responding when user not detected
            await ctx.respond("Пользователь не найден.")
            return
        await ctx.defer()
        # this is string with result
        result = f"**Баны {username}:**\n-----------"
        # this is tuple with all bans in the table
        user_bans = crud.get_user_job_bans(user_id)
        bans_got = 0
        datetime_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        datetime_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        # checking the presence values on the tuple
        if len(user_bans) <= 0:
            await ctx.respond(f"У пользователя {username} не обнаружено банов ролей на данном промежутке времени.")
            return
        for ban in user_bans:
            date_format = "%Y-%m-%d %H:%M:%S"
            ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)

            if datetime_end_date >= ban_time.date() > datetime_start_date:
                # see field name :)
                date_format = "%Y-%m-%d %H:%M:%S"
                # also with this
                expiration_time = datetime.strptime(ban.expiration_time.split('.')[0], date_format)
                # calculating the difference between the dates
                time_difference = expiration_time - ban_time

                banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)

                # update result string
                result += (
                    f"\n**Бан раунда #{ban.round_id}.** \n**Роль:** {ban.role_id.split(':')[1]}.\n**Причина:** \"{ban.reason}\"."
                    f" \n**Время бана:** {time_difference}\n**Выдан:** {ban_time}s\n**Бан выдал**: "
                    f"{banning_admin_name} "
                    f"\n-----------")
                bans_got += 1
        if bans_got == 0:
            await ctx.respond(f"У пользователя {username} не обнаружено банов на данном промежутке времени.")
            return
        # respond result
        await ctx.respond(result)

    # this function displays top admins by ban
    @commands.slash_command(name="top_bans_admin", description="Отображает топ админов по банам.")
    async def get_top_of_bans_between_admins(self, ctx: discord.ApplicationContext,
                                             start_date: Option(str,
                                                                "Начало временного диапазона для поиска банов. Формат времени:"
                                                                "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                                             end_date: Option(str,
                                                              "Конец временного диапазона для поиска банов. Формат времени:"
                                                              "\"ГГГГ-ММ-ДД\"") = str(datetime.today().date())):
        # tuple with all bans
        bans = crud.get_all_bans()

        # dictionary with admins who committed bans
        admins_dictionary = {}

        # checking len of bans
        if len(bans) == 0:
            await ctx.respond("Баны не обнаружены.")
            return
        for ban in bans:
            date_format = "%Y-%m-%d %H:%M:%S"
            ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)
            # checking whether the ban falls within the time period
            if datetime.strptime(end_date, "%Y-%m-%d").date() >= ban_time.date() > datetime.strptime(start_date,
                                                                                                     "%Y-%m-%d").date():
                # checking the dictionary for the presence of a key with the value of bans
                banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)
                if banning_admin_name in admins_dictionary:
                    admins_dictionary[banning_admin_name] += 1
                else:
                    admins_dictionary[banning_admin_name] = 1

        # checking the presence admins in admin dictionary
        if len(admins_dictionary) == 0:
            await ctx.respond("Баны не обнаружены.")
            return
        # sorting dictionary of admins
        sorted_admin_dict = dict(sorted(admins_dictionary.items(), key=lambda item: item[1], reverse=True))
        # this is the result string for respond
        result = "**Топ админов по банам:** \n\n"
        # index field for greater clarity
        index = 1
        for admin in sorted_admin_dict:
            # formating result string
            result += f"{index}. {admin} выдал банов: {sorted_admin_dict[admin]}\n"
            index += 1
        # responding the result
        await ctx.respond(result)

    # this function displays top admins by job ban
    @commands.slash_command(name="top_job_bans_admin", description="Отображает топ админов по банам ролей.")
    async def get_top_of_job_bans_between_admins(self, ctx: discord.ApplicationContext,
                                                 start_date: Option(str,
                                                                    "Начало временного диапазона для поиска банов. Формат времени:"
                                                                    "\"ГГГГ-ММ-ДД\"") = '2000-01-01',
                                                 end_date: Option(str,
                                                                  "Конец временного диапазона для поиска банов. Формат времени:"
                                                                  "\"ГГГГ-ММ-ДД\"") = str(datetime.today().date())):
        # tuple with all bans
        bans = crud.get_all_job_bans()

        # dictionary with admins who committed bans
        admins_dictionary = {}

        # checking len of bans
        if len(bans) == 0:
            await ctx.respond("Баны ролей не обнаружены.")
            return
        for ban in bans:
            date_format = "%Y-%m-%d %H:%M:%S"

            ban_time = datetime.strptime(str(ban.ban_time).split('.')[0], date_format)
            # checking whether the ban falls within the time period
            if datetime.strptime(end_date, "%Y-%m-%d").date() >= ban_time.date() > datetime.strptime(start_date,
                                                                                                     "%Y-%m-%d").date():

                banning_admin_name = crud.get_player_name_by_id(ban.banning_admin)
                # checking the dictionary for the presence of a key with the value of bans
                if banning_admin_name in admins_dictionary:
                    admins_dictionary[banning_admin_name] += 1
                else:
                    admins_dictionary[banning_admin_name] = 1
        # checking the presence admins in admin dictionary
        if len(admins_dictionary) == 0:
            await ctx.respond("Баны ролей не обнаружены.")
            return
        # sorting dictionary of admins
        sorted_admin_dict = dict(sorted(admins_dictionary.items(), key=lambda item: item[1], reverse=True))
        # this is the result string for respond
        result = "**Топ админов по банам ролей:** \n\n"
        # index field for greater clarity
        index = 1
        for admin in sorted_admin_dict:
            # formating result string
            result += f"{index}. {admin} выдал банов ролей: {sorted_admin_dict[admin]}\n"
            index += 1
        # responding the result
        await ctx.respond(result)

import telebot
import requests
import config
import datetime
from typing import Optional, Tuple
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.access_token)

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_page(group='K3140', week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page: str, day: str) -> Optional[Tuple[list, list, list, list]]:
    soup = BeautifulSoup(web_page, "html5lib")
    if day in days:
        date = str(days.index(day) + 1) + 'day'

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table")
    if schedule_table == None:
        return "error"

    schedule_table = soup.find("table", attrs={"id": date})
    # Время проведения занятий
    try:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
    except AttributeError:
        return None
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations = [room.span.text for room in locations_list]
    rooms = [room.dd.text for room in locations_list]
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.dd.text for lesson in lessons_list]
    return times_list, locations, rooms, lessons_list


def get_study_day(page: str, day: str, week: str, group: str) -> Optional[Tuple[list, list, list, list]]:
    if days.index(day) >= 6:
        day = 'monday'
        if week == 2:
            week = 1
        else:
            week = 2
        page = get_page(group, week)

    schedule = get_schedule(page, day)
    cur_day = days.index(day) + 1
    i = 0
    while schedule is None and i != 7:
        if cur_day == 6:
            cur_day = 0
            if week == 2:
                week = 1
            else:
                week = 2
            page = get_page(group, week)
        schedule = get_schedule(page, days[cur_day])
        if schedule == "error":
            return "error"
        cur_day += 1
        i += 1

    return schedule


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def get_day(message: telebot.types.Message) -> None:
    try:
        day, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id, '/day <week: 1-even or 2-odd> <groupname>')
        return None
    group = group.upper()
    web_page = get_page(group, week)
    schedule = get_schedule(web_page, day[1:])

    if schedule == "error":
        response = '<b>Неверные данные</b>'
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None
    if schedule is None:
        response = 'Атдыхаем'
    else:
        times_lst, locations_lst, rooms, lessons_lst = schedule
        response = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, rooms, lessons_lst):
            response += 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n\n'.format(time, location, room, lesson)
    bot.send_message(message.chat.id, response, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message: telebot.types.Message) -> None:
    try:
        _, group = message.text.split()
    except:
        bot.send_message(message.chat.id, '/tommorow <groupname>')
        return None
    group = group.upper()
    dt = datetime.datetime.now()
    if dt.weekday() == 6:
        day = 'monday'
        week = int(dt.isocalendar()[1]) % 2
    else:
        day = days[dt.weekday() + 1]
        week = int(dt.isocalendar()[1]) % 2 + 1
    web_page = get_page(group, week)
    schedule = get_schedule(web_page, day)
    if schedule == "error":
        response = '<b>Неверные данные</b>'
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None
    if schedule is None:
        response = 'Ничего'
    else:
        times_lst, locations_lst, rooms, lessons_lst = schedule
        response = ''
        for time, location, room, lesson in zip(times_lst, locations_lst, rooms, lessons_lst):
            response += 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n\n'.format(time, location, room, lesson)
    if dt.weekday() == 5:
        response = "<b>ГУЛЯЕМ</b>"
    bot.send_message(message.chat.id, response, parse_mode='HTML')


@bot.message_handler(commands=['week'])
def get_week(message: telebot.types.Message) -> None:
    try:
        _, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id, '/week <week: 1-even or 2-odd> <groupname>')
        return None
    group = group.upper()
    page = get_page(group, week)
    response = ''
    for day in days:
        schedule = get_schedule(page, day)
        if schedule == "error":
            response = '<b>Неверные данные</b>'
            bot.send_message(message.chat.id, response, parse_mode='HTML')
            return None
        if schedule is not None:
            times_lst, locations_lst, rooms, lessons_lst = schedule
            response += '<b>' + chr(ord(day[0])-32) + day[1:] + ':' + '</b>' + '\n'
            for time, location, room, lesson in zip(times_lst, locations_lst, rooms, lessons_lst):
                response += 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n \n'.format(time, location, room, lesson)
        response += '\n'
    bot.send_message(message.chat.id, response, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near(message: telebot.types.Message) -> None:
    try:
        _, group = message.text.split()
    except:
        bot.send_message(message.chat.id, '/near <groupname>')
        return None

    group = group.upper()
    today = datetime.datetime.now()
    if today.weekday() != 6:
        day = days[today.weekday()]
    else:
        day = 'monday'
        week = int(today.isocalendar()[1]) % 2
        page = get_page(group, week)
        schedule = get_study_day(page, day, week, group)
        if schedule == "error":
            response = '<b>Неверные данные</b>'
            bot.send_message(message.chat.id, response, parse_mode='HTML')
            return None
        if schedule is None:
            bot.send_message(message.chat.id, 'Wrong group number')
            return None
        times_lst, locations_lst, rooms, lessons_lst = schedule
        response = 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n \n'.format(times_lst[0], locations_lst[0], rooms[0], lessons_lst[0])
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None
    week = int(today.isocalendar()[1]) % 2 + 1
    page = get_page(group, week)
    schedule = get_schedule(page, day)
    if schedule == "error":
        response = '<b>Неверные данные</b>'
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None
    if schedule is None:
        schedule = get_study_day(page, day, week, group)
        if schedule == "error":
            response = '<b>Неверные данные</b>'
            bot.send_message(message.chat.id, response, parse_mode='HTML')
            return None
        times_lst, locations_lst, rooms, lessons_lst = schedule
        response = 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n \n'.format(times_lst[0], locations_lst[0], rooms[0], lessons_lst[0])
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None
    else:
        times_lst, locations_lst, rooms, lessons_lst = schedule
        count = 0
        for i in times_lst:
            try:
                t_start, t_end = i.split('-')
            except ValueError:
                break
            t_start = '{} {} {} {}'.format(today.year, today.day, today.month, t_start)
            t_start = datetime.datetime.strptime(t_start, '%Y %d %m %H:%M')
            if today < t_start:
                response = 'В <b>{4}</b> <b>{0}</b> {3} на {1} в <b>{2}</b>\n \n'.format(times_lst[count], locations_lst[count], rooms[count],
                                                                       lessons_lst[count], days[count])
                bot.send_message(message.chat.id, response, parse_mode='HTML')
                return None
            count += 1
        day = days[days.index(day) + 1]
        schedule = get_study_day(page, day, week, group)
        if schedule == "error":
            response = '<b>Неверные данные</b>'
            bot.send_message(message.chat.id, response, parse_mode='HTML')
            return None
        times_lst, locations_lst, rooms, lessons_lst = schedule
        response = 'В <b>{0}</b> {3} на {1} в <b>{2}</b>\n \n'.format(times_lst[0], locations_lst[0], rooms[0], lessons_lst[0])
        bot.send_message(message.chat.id, response, parse_mode='HTML')
        return None


@bot.message_handler(content_types=['text'])
def help(message: telebot.types.Message) -> None:
    response = "Экспекто Патронум, Дементор!"
    bot.send_message(message.chat.id, response, parse_mode='HTML')
    return None


if __name__ == '__main__':
    bot.polling(none_stop=True)
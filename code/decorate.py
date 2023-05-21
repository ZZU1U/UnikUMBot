WEEKDAYS = {
    1: 'Понедельник',
    2: 'Вторник',
    3: 'Среда',
    4: 'Четверг',
    5: 'Пятница',
    6: 'Суббота',
    7: 'Воскресенье'
}

LESSONS_WEEKDAY = {
    1: ('8:30', '10:00'),
    2: ('10:20', '11:50'),
    3: ('12:10', '13:40'),
    4: ('15:20', '16:50'),
    5: ('17:00', '18:30'),
    6: ('18:40', '20:10')
}

LESSONS_WEEKEND = {
    1: ('9:00', '10:30'),
    2: ('10:40', '12:10'),
    3: ('12:30', '14:00'),
    4: ('14:10', '15:40'),
    5: ('16:00', '17:30'),
    6: ('17:40', '19:10')
}

LESSONS_KUZGTU = {
    1: ('9:00', '10:30'),
    2: ('10:50', '12:20'),
    3: ('13:20', '14:50'),
    4: ('15:10', '16:40'),
    5: ('17:00', '18:30'),
    6: ('18:50', '20:20'),
    7: ('20:30', '22:00')
}

def create_beautiful_table(lessons: str, schedule_type:str, org:str) -> str:
    if schedule_type == 'coming':
        lessons_dict = {}

        for id, lesson in lessons[1:]:
            lessons_dict[lesson] = lessons_dict.get(lesson, []) + [id]

        day = lessons[0]
        if org == 'УникУм':
            if day.weekday() < 5:
                lessonsInfo = '\n'.join([f" - {lesson}: **{LESSONS_WEEKDAY[times[0]][0]}-{LESSONS_WEEKDAY[times[-1]][1]}**" for lesson, times in lessons_dict.items()])
            else:
                lessonsInfo = '\n'.join([f" - {lesson}: *{LESSONS_WEEKEND[times[0]][0]}-{LESSONS_WEEKEND[times[-1]][1]}*" for lesson, times in lessons_dict.items()])
        else:
            lessonsInfo = '\n'.join([f" - {lesson}: *{LESSONS_KUZGTU[times[0]][0]}-{LESSONS_KUZGTU[times[-1]][1]}*" for lesson, times in lessons_dict.items()])

        message = f"Ближайший рабочий день будет *{WEEKDAYS[day.weekday()+1]} - {day.strftime('%d.%m.%Y')} 📚*\n{lessonsInfo}"


    if schedule_type == 'tooday':
        lessons_dict = {}

        for id, lesson in lessons[1:]:
            lessons_dict[lesson] = lessons_dict.get(lesson, []) + [id]

        day = lessons[0]

        if org == 'УникУм':
            if day.weekday() < 5:
                lessonsInfo = '\n'.join([f" - {lesson}: *{LESSONS_WEEKDAY[times[0]][0]}-{LESSONS_WEEKDAY[times[-1]][1]}*" for lesson, times in lessons_dict.items()])
            else:
                lessonsInfo = '\n'.join([f" - {lesson}: *{LESSONS_WEEKEND[times[0]][0]}-{LESSONS_WEEKEND[times[-1]][1]}*" for lesson, times in lessons_dict.items()])
        else:
            lessonsInfo = '\n'.join([f" - {lesson}: *{LESSONS_KUZGTU[times[0]][0]}-{LESSONS_KUZGTU[times[-1]][1]}*" for lesson, times in lessons_dict.items()])

        message = f"*{WEEKDAYS[day.weekday()+1]} - {day.strftime('%d.%m.%Y')} 📚*\n{lessonsInfo}"


    if schedule_type == 'week':
        message = ""

        for days_lessons in lessons:
            lessons_dict = {}
            

            for id, days_lesson in days_lessons[1:]:
                lessons_dict[days_lesson] = lessons_dict.get(days_lesson, []) + [id]

            day = days_lessons[0]
            if org == 'УникУм':
                if day.weekday() < 5:
                    lessons_info = '\n'.join([f" - {lesson}: *{LESSONS_WEEKDAY[times[0]][0]}-{LESSONS_WEEKDAY[times[-1]][1]}*" for lesson, times in lessons_dict.items()])
                else:
                    lessons_info = '\n'.join([f" - {lesson}: *{LESSONS_WEEKEND[times[0]][0]}-{LESSONS_WEEKEND[times[-1]][1]}*" for lesson, times in lessons_dict.items()])
            else:
                lessons_info = '\n'.join([f" - {lesson}: *{LESSONS_KUZGTU[times[0]][0]}-{LESSONS_KUZGTU[times[-1]][1]}*" for lesson, times in lessons_dict.items()])

            message += f"*{WEEKDAYS[day.weekday()+1]} - {day.strftime('%d.%m.%Y')} 📚*\n{lessons_info}\n\n"


    return message

def create_beautiful_list(some_list: list, organization: str) -> str:
    message = f"*Вот список групп в {organization}:*\n{'  '.join(some_list)}"
    return message

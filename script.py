import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


HOW_TO_PRAISE = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
    ]



def name_student(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{name}'не найден.")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Вы ничего не ввели или найдено несколько учеников с именем {name}, уточните ФИО.")

def fix_marks(schoolkid):
    child = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    child.update(points=5)


def remove_chastisements(schoolkid):
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement.delete()


def create_commendation(schoolkid, item_name):
    try:
        get_subject = Subject.objects.get(title=item_name, year_of_study=schoolkid.year_of_study)
    except Subject.DoesNotExist:
        print(f"Уточните название предмета {item_name}")
    except Subject.MultipleObjectsReturned:
        print(f"Предмета {item_name} для {schoolkid.year_of_study} класса не существует")


    last_lesson = Lesson.objects.filter(subject__title=item_name, group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study).order_by('-date').first()
    if last_lesson is None:
        print(f"{item_name} данного урока нет.")
    else:
        praise = Commendation.objects.create(text=random.choice(HOW_TO_PRAISE), created=last_lesson.date, schoolkid=schoolkid, subject=last_lesson.subject, teacher=last_lesson.teacher)

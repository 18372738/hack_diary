from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def name_student(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print(f"Ученик с именем '{name}'не найден. Проверьте правильность ввода.")
    except MultipleObjectsReturned:
        if name == "":
            print("Ничего не указали, введите ФИО.")
        else:
            print(f'Найдено несколько школьников с именем "{name}", добавьте фамилию или отчество.')



def fix_marks(schoolkid):
    child = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    child.update(points=5)


def remove_chastisements(schoolkid):
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement.delete()


def create_commendation(schoolkid, item_name):
    how_to_praise = [
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

    try:
        subject = Lesson.objects.get(subject__title=item_name, group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study).first()
    except ObjectDoesNotExist:
        print(f"Уточните название предмета {item_name}")
    except MultipleObjectsReturned:
        last_subject = Lesson.objects.filter(subject__title=item_name, group_letter=schoolkid.group_letter, year_of_study=schoolkid.year_of_study).order_by('date').first()
        praise = Commendation.objects.create(text=random.choice(how_to_praise), created=last_subject.date, schoolkid=schoolkid, subject=last_subject.subject, teacher=last_subject.teacher )
        praise.save()

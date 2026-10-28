"""Задание 2. Выбор следующего вопроса — «лесенка».

Этот модуль ничего не печатает. Названия функций и то, что они принимают,
менять нельзя: их вызывают exam.py и тесты. Меняй тела функций.
Как устроена лесенка и где она ломается — materials/ladder_rus.md.
"""

START_LEVEL = 1


def next_level(level, result):
    """Уровень следующего вопроса.

    level — уровень, на котором был вопрос; result — "верно", "неверно"
    или "нет ответа".

    После "верно" — на единицу выше, после "неверно" — на единицу ниже,
    но не ниже 1 и не выше 5. После "нет ответа" уровень не меняется.

    Пока тело не написано, уровень не меняется никогда.
    """
    if result == "верно" and level < 5:
        return level + 1 
    elif result == "неверно" and level >1:
        return level - 1 
    return level


def pick_question(questions, level, asked):
    """Следующий вопрос.

    questions — список вопросов (сначала вопросы команды, потом выданные);
    level — нужный уровень; asked — список id уже заданных вопросов.

    Возвращает первый по порядку в списке вопрос нужного уровня, которого
    нет в asked. Если на этом уровне вопросов не осталось — ближайший уровень;
    при равном расстоянии — тот, что ниже. Если не осталось совсем — None.

    Пока тело не написано, функция берёт первый незаданный вопрос,
    не глядя на уровень.
    """ 
    for question in questions:
        if question["id"] not in asked and question["level"] == level:
            return question
    for question in questions:
        if question["id"] not in asked and question["level"] == level - 1:
            return question
    for question in questions:
        if question["id"] not in asked and question["level"] == level + 1:
            return question
    return None

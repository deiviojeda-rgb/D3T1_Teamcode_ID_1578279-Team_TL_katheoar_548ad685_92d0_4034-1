"""Задание 3. Экзамен: разговор с человеком и итог.

Запуск из корня репозитория:  python3 src/exam.py

Функция main в конце файла уже соединяет части экзамена: загружает вопросы,
спрашивает имя, задаёт вопросы по лесенке, подводит итог и записывает результат.
Тела остальных функций этого файла пока простейшие — их пишет тот, кто взял
Задание 3. Как должен выглядеть экран — materials/screen_rus.md.

Этот файл — точка входа: печатает только он.
"""

import sys

import answers
import bank
import ladder

TEAM = "datasets/team.csv"
BANK = "datasets/bank.csv"
RESULTS = "results.csv"
MAX_QUESTIONS = 10


def load_questions():
    """Все вопросы экзамена одним списком: сначала из TEAM, потом из BANK.

    Если файла нет, ошибку FileNotFoundError здесь не перехватывай:
    её перехватывает main.

    Пока тело простейшее: только выданные вопросы.
    """
    a, _= bank.load_bank(TEAM)
    b, _= bank.load_bank(BANK)
    questions=a + b
    return questions


def read_line():
    """Прочитать одну строку, которую ввёл человек.

    Возвращает строку без перевода строки в конце. Если ввод закончился
    (Ctrl+D), возвращает None.

    Пока тело простейшее: конец ввода не отличается от пустой строки.
    """
    n =sys.stdin.readline()
    if n=="":
        return None
    else: return n.rstrip("\n")


def show_question(number, question):
    """Показать вопрос с номером number, как в materials/screen_rus.md.

    Пока тело простейшее: только текст и варианты.
    """
    print( f"Вопрос {number} из 10")
    for line in bank.question_lines(question):
        print(line)
    if question["type"] == "несколько":
        print("Введи номера всех верных вариантов через запятую.")
    if question["type"] == "один":
        print("Введи номер варианта.")
    if question["type"] == "короткий":
        print("Напиши ответ.")

def show_result(result):
    """Показать результат ответа: «Верно.», «Неверно.» или «Нет ответа.».

    Пока тело простейшее: результат как есть.
    """
    if result == "верно":
        result = "Верно."
    elif result == "неверно":
        result = "Неверно."
    elif result == "нет ответа":
        result = "Нет ответа."
    print(result)


def final_level(history):
    """Итоговый уровень по правилу последнего правильного ответа.

    history — список пар (уровень вопроса, результат) в порядке экзамена,
    например [(1, "верно"), (2, "неверно"), (1, "верно")].

    Возвращает уровень последнего вопроса с результатом "верно"
    или None, если верных ответов не было.

    Пока тело простейшее: всегда None.
    """
    i = len(history)
    while i>0:
        i-=1
        if history[i][1] == "верно":
            return history[i][0]
        
    return None


def final_lines(level, history):
    """Строки итога: «Итог: …» и «Почему: …», как в materials/screen_rus.md.

    level — итоговый уровень или None.

    Пока тело простейшее: только первая строка.
    """
    if level == None:
        a = "Итог: не определён."
        b = "Почему: ни одного правильного ответа."
        return [a, b]
    else:
        a = f"Итог: уровень {level}."
        b= f"Почему: последний правильный ответ — на уровне {level}."
        return [a, b]



def stable_level(history):
    """Задание 6 (дополнительное). Самый высокий уровень, где у человека
    хотя бы два верных ответа, или None.
    """
    count = {}
    max_level = 0
    for level, answer in history:
        if answer == 'верно':
            count[level] = count.get(level, 0) +1
    for key, value in count.items():
        if value >= 2:
            max_level = max(key, max_level)
    return max_level if max_level else None


def stable_lines(level, history):
    """Задание 6 (дополнительное). Строки итога для устойчивого правила."""
    if level == None:
        return ["Итог: не определён.","Почему: ни одного правильного ответа."]
    count = {}
    for his_lev, answer in history:
        if level == his_lev:
            count[his_lev] = count.get(his_lev, 0) +1
            if answer == 'верно':
                count[str(his_lev) + "верно"] = count.get(str(his_lev) + "верно", 0) +1

        elif level + 1 == his_lev:

            count[his_lev] = count.get(his_lev, 0) +1

            if answer == 'верно':
                count[str(his_lev) + "верно"] = count.get(str(his_lev)+ "верно", 0) +1

    c1 = count[str(level) + "верно"]

    c2 = count.get(str(level+1 )+ "верно", 0)

    c3 = count.get(level + 1, 0)
    c4 = count[level]

    part1 = f"Почему: уровень {level} — самый высокий, где у тебя 2 верных ответа ({c1} из {c4})."
    part2 = f"На уровне {level + 1} верных ответов нет ({c2} из {c3})."
    
    return [f"Итог: уровень {level}.", part1 + part2]


def save_result(name, level, asked, correct):
    """Дописать строку «имя;уровень;задано;верно» в конец файла RESULTS.

    level — число или None; при None в поле уровня пишется «не определён».

    Пока тело простейшее: ничего не записывается.
    """
    if not level:
        write_file =f'{name};не определён;{asked};{correct}\n'
    else:
        write_file =f'{name};{level};{asked};{correct}\n'
    with open(RESULTS, "a", encoding="utf-8") as target:
        target.write(write_file)

def main():
    try:
        questions = load_questions()
    except FileNotFoundError as error:
        print("Файл не найден: %s" % error.filename)
        return 1

    print("Как тебя зовут?")
    name = read_line()
    if name is None:
        print("Экзамен не начат.")
        return 0
    name = name.replace(";", " ").strip() or "без имени"

    stable = "--stable" in sys.argv
    level = ladder.START_LEVEL
    asked = []
    history = []
    while len(asked) < MAX_QUESTIONS:
        question = ladder.pick_question(questions, level, asked)
        if question is None:
            break
        asked.append(question["id"])
        print()
        show_question(len(asked), question)
        raw = read_line()
        result = answers.check_answer(question, raw if raw is not None else "")
        show_result(result)
        history.append((question["level"], result))
        level = ladder.next_level(question["level"], result)
        if raw is None:
            break

    if stable:
        result_level = stable_level(history)
        lines = stable_lines(result_level, history)
    else:
        result_level = final_level(history)
        lines = final_lines(result_level, history)
    print()
    for line in lines:
        print(line)
    correct = 0
    for _, result in history:
        if result == "верно":
            correct += 1
    save_result(name, result_level, len(asked), correct)
    return 0


if __name__ == "__main__":
    sys.exit(main())

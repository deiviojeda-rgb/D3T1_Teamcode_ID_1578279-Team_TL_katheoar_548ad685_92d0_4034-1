# Python для дней 03–04

Все примеры доступны офлайн. Реализация использует стандартную библиотеку.

## Словарь и связи

```python
by_id = {}
by_id[101] = {"id": 101, "level": 3}
answers_by_id = {}
answers_by_id.setdefault(101, []).append({"label": "А", "correct": True})
```

ID не обязан совпадать с индексом списка. Сопоставляйте вопрос и ответы по ID.
Банки для запуска корректны; готовая проверка данных помогает найти опечатки в своих вопросах.

## Множества и сортировка

```python
used = set()
used.add(101)
available = [q for q in questions if q["id"] not in used]
available = sorted(available, key=lambda q: q["id"])
```

Множество не хранит пригодный для воспроизводимости порядок. Для случайного
выбора сначала упорядочьте список. Словарь в современных Python сохраняет
порядок вставки, но разные источники вставки всё равно дают разные порядки.

## Случайность

```python
import random
rng = random.Random(seed)
question = rng.choice(available)
```

Не выбирайте из пустого списка. Один объект rng на сессию. Один seed работает
при одинаковом порядке данных и последовательности обращений к генератору.

## Файлы и исключения

```python
from pathlib import Path
path = Path(folder) / "bank_reference.txt"
text = path.read_text(encoding="utf-8")
for line in text.splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    fields = [part.strip() for part in line.split("|")]
```

У вопроса пять полей, у ответа четыре. Ошибка открытия папки или основного
файла — ошибка запуска: сообщите о ней пользователю. Корректность записей
перед сессией проверяет готовая команда --bank-check.

## CLI

Можно использовать sys.argv или argparse — argparse входит в стандартную библиотеку.
Проверяйте обязательный путь, значение после --seed, конфликт флагов и неизвестные флаги.
`sys.exit(2)` — ненулевой код при неверном запуске.

## Диалог и JSON в логе

```python
import json
import sys
print("> " + question_text)
print("ОТВЕТ:", flush=True)
try:
    answer = input()
except EOFError:
    answer = None
encoded = json.dumps(answer, ensure_ascii=False)
print(log_line, file=sys.stderr, flush=True)
```

input снимает завершающий перевод строки, но не пробелы. None нельзя перепутать
с пустой строкой: это EOF. JSON сохраняет различие между null и "" и экранирует
кавычки/управляющие символы. Поле ответа в log_line берётся из encoded.

## Модули

main.py импортирует bank и engine; bank.check обращается к answers.check. Файлы рядом в src; __init__.py не требуется.
Модули возвращают данные, печатает main.py. Избегайте круговых зависимостей:
банк не должен зависеть от состояния движка. Не всякий круговой import сразу
падает, но такой договор хрупок и усложняет понимание.

Самостоятельный пример разбора аргументов и диалога — cli_example_rus.md.

"""Реализуйте контракт из materials/protocol_rus.md. Модуль не печатает."""
import answers


def load(folder):
    raise NotImplementedError('Реализуйте чтение банка')


def check(question, answer):
    return answers.check(question, answer)

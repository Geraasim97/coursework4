from src.vacancy_class import Vacancy


def user_format(vacancies: list) -> list[Vacancy]:
    """Из листа вакансий формирует наглядный для пользователя перечень экземпляров класса Vacancy"""

    vacancy_cls_list = []
    for vacancy in vacancies:
        vacancy_cls_list.append(Vacancy(vacancy["title"], vacancy["url"], vacancy["salary_from"], vacancy["employer"]))

    return vacancy_cls_list
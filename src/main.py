from src.job_site_api_class import HeadHunterAPI, SuperJobAPI
from src.connector_class import JsonConnector
from src.user_utils import user_format


def main():

    # Очищаем файл от предыдущих запусков программы
    json_vac = JsonConnector()
    json_vac.delete_vacancies()

    # Получаем от пользователя ключевое слово и платформы для сбора вакансий
    keyword = input("Введите ключевое слово для поиска вакансий: ")
    json_vac = JsonConnector()

    platform_hh = input("Вас интересуют вакансии с сайта HeadHunter? y/n ")

    platform_sj = input("Вас интересуют вакансии с сайта SuperJob? y/n ")

    if platform_hh != "y" and platform_sj != "y":
        print("К сожалению, вы не выбрали ни одну платформу")
        exit()

    # Пользователь выбирает необходимую команду
    search_way = input("""Выберите команду:
    sort - выдаст вакансии, содержащие ключевое слово
    top - выдаст лучшие вакансии по зарплате \nsort или top: """)

    if search_way not in ("sort", "top"):
        print("Неверная команда")
        exit()

    # Собираем файл из вакансий на выбранных платформах
    if platform_hh == "y":  # с hh.ru
        hh_api = HeadHunterAPI()
        hh_vacancies = hh_api.get_vacancies(keyword)
        hh_clean_vacancies = hh_api.clean_vacancies(hh_vacancies)
        json_vac.add_vacancies(hh_clean_vacancies)

    if platform_sj == "y":  # с superjob.ru
        sj_api = SuperJobAPI()
        sj_vacancies = sj_api.get_vacancies(keyword)
        sj_clean_vacancies = sj_api.clean_vacancies(sj_vacancies)
        json_vac.add_vacancies(sj_clean_vacancies)

    # Выводим вакансии по команде сортировки
    if search_way == "sort":
        search_word = input("Введите поисковый запрос для фильтрации вакансий: ")
        filtered_vacancies = json_vac.filter_vacancies(search_word)
        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
            for vacancy in user_format(filtered_vacancies):
                print(vacancy)

    # Выводим вакансии по команде top
    elif search_way == "top":
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        top_vacancies = json_vac.top_vacancies(top_n)
        if not top_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
            for vacancy in user_format(top_vacancies):
                print(vacancy)


if __name__ == "__main__":
    main()
# Дипломный проект - автоматизация тестирования
## Запуск приложения
1. Установить Docker Desktop
2. Выполнить в терминале: docker-compose up --build
3. Подождать 1-2 минуты, перейти по адресу: http://localhost:8080

## Данные для тестов

- **APPROVED** карта: `4444 4444 4444 4441`
- **DECLINED** карта: `4444 4444 4444 4442`
- Месяц: `12`, Год: `26`, Владелец: `Ivanov Ivan`, CVC: `123`

## Запуск автотестов
1. Создать виртуальное окружение: 
- python -m venv .venv
- .venv\Scripts\activate (для Windows)
- source .venv/bin/activate (для macOS/Linux)
2. Установить зависимости: pip install -r requirements.txt
3. Проверить работу приложения (http://localhost:8080)
4. Запустить тесты: pytest tests/ --alluredir=allure-results
5. Сгенерировать Allure-отчёт:
- allure generate allure-results -o allure-report --clean
- allure open allure-report

# 🌺 FlowerDelivery Master

**Автор проекта**  
Фролов Иван

## Оглавление
- [Описание проекта](#описание-проекта)
- [Функциональные возможности](#функциональные-возможности)
  - [Веб-сайт](#веб-сайт)
  - [Telegram-бот](#telegram-бот)
- [Установка и запуск](#установка-и-запуск)
  - [Предварительные требования](#предварительные-требования)
  - [Установка](#установка)
  - [Запуск веб-сайта](#запуск-веб-сайта)
  - [Запуск Telegram-бота](#запуск-telegram-бота)
- [Архитектура системы](#архитектура-системы)
  - [Модули и приложения](#модули-и-приложения)
  - [Модель данных](#модель-данных)
- [Тестирование](#тестирование)
- [Используемые технологии](#используемые-технологии)
- [Лицензия](#лицензия)
- [Контакты](#контакты)

## Описание проекта
**FlowerDelivery Master** — это комплексное решение для заказа цветов через веб-сайт с интеграцией Telegram-бота для управления заказами и получения уведомлений. Проект предоставляет удобный и интуитивно понятный интерфейс для пользователей, а также мощные инструменты для администраторов и сотрудников компании.

## Функциональные возможности

- Веб-сайт:
    - Регистрация и авторизация пользователей.
    - Просмотр каталога цветов.
    - Выбор цветов и добавление в корзину.
    - Оформление заказа с указанием данных для доставки.
    - Просмотр истории заказов.
    - Аккаунт администратора для отметки статуса заказа
    - Возможность повторного заказа, той же позиции из каталога.
    - Поддержка отзывов и рейтингов.
    - Аналитика и отчеты по заказам.
- Telegram бот:
    - Получение заказов с информацией о букетах и доставке.
    - Уведомления о статусе заказа.
    - Аналитика и отчеты по заказам (для сотрудников)


## Установка и запуск

### Предварительные требования
- Python 3.8+
- Django 3.2+
- Redis (для работы с Celery)
- Celery (для выполнения фоновых задач)
- Аккаунт Telegram и созданный бот через BotFather

### Установка
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/FIV-F4/ITG02_2.git
    cd ITG02_2/flower_delivery
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
    - Для Linux/MacOS:
      ```bash
      source venv/bin/activate
      ```
    - Для Windows:
      ```bash
      venv\Scripts\activate
      ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

6. Соберите статические файлы:
    ```bash
    python manage.py collectstatic
    ```

### Запуск веб-сайта
```bash
python manage.py runserver
```
Веб-сайт будет доступен по адресу [http://localhost:8000/](http://localhost:8000/).

### Запуск Telegram-бота
1. Настройте переменные окружения:  
   В файле `module_telegram/config.py` укажите токен вашего бота:
    ```python
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    ```

2. Запустите бота:
    ```bash
    python bot_runner.py
    ```

## Архитектура системы

### Модули и приложения
- `module_reg_auth_user` — регистрация и авторизация пользователей.
- `module_catalog` — каталог товаров.
- `module_orders` — оформление и управление заказами.
- `module_reviews` — отзывы и рейтинги.
- `module_analytics` — аналитика и отчеты.
- `module_telegram` — интеграция с Telegram-ботом.

### Модель данных
- `User` — расширенная модель пользователя с дополнительными полями (телефон, адрес, Telegram ID).
- `Products` — товары, доступные для заказа.
- `Order` — информация о заказе, статус, дата.
- `OrderProduct` — связи между заказами и товарами.
- `Delivery` — информация о доставке заказа.
- `Review` — отзывы пользователей о товарах.
- `Report` — индивидуальные отчеты по заказам.
- `AggregateReport` — агрегированные отчеты за периоды.

## Тестирование
- Юнит-тесты для основных модулей и функционала.
- Запуск тестов:
    ```bash
    python manage.py test
    ```

## Используемые технологии
- Язык программирования: Python 3.8+
- Веб-фреймворк: Django 3.2+
- База данных: SQLite (для разработки), поддержка PostgreSQL/MySQL (для продакшена)
- Фронтенд: Bootstrap 4
- Мессенджер-бот: aiogram (для работы с Telegram API)
- Асинхронные задачи: Celery с брокером сообщений Redis
- Прочее:
  - Django ORM для взаимодействия с базой данных
  - Django Templates для рендеринга страниц
  - Docker (опционально, для контейнеризации приложения)

## Лицензия
Этот проект лицензируется под лицензией MIT. Подробнее см. LICENSE.

© 2023 Иван Фролов. Все права защищены.

## Контакты
- **Telegram:** [@Ivan_Frolov](https://t.me/ivan_frolov)

## Структура проекта

```plaintext
flower_delivery/
├── flower_delivery/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── module_analytics/
│   ├── models.py
│   ├── views.py
│   ├── reports.py
│   └── ...
├── module_catalog/
│   ├── models.py
│   ├── views.py
│   └── ...
├── module_orders/
│   ├── models.py
│   ├── views.py
│   └── ...
├── module_reg_auth_user/
│   ├── models.py
│   ├── views.py
│   └── ...
├── module_reviews/
│   ├── models.py
│   ├── views.py
│   └── ...
├── module_telegram/
│   ├── bot.py
│   ├── config.py
│   └── ...
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
├── static/
│   └── css/
│       └── styles.css
├── manage.py
├── requirements.txt
└── README.md
```

## Запуск Celery (опционально)
Для выполнения фоновых задач (например, отправка уведомлений) используется Celery. Убедитесь, что Redis запущен и доступен.

Запуск воркера Celery:
```bash
celery -A flower_delivery worker -l info
```

**Примечание:** Для корректной работы приложения убедитесь, что все зависимости установлены, а настройки соответствуют вашему окружению. В случае возникновения вопросов или проблем с запуском проекта, пожалуйста, создайте новый вопрос в разделе Issues данного репозитория.

## Лицензия

Данный проект распространяется под лицензией MIT. Подробности см. в файле LICENSE.

© 2024 Иван Фролов. Все права защищены.

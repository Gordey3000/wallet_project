# Wallet API

## Описание
Данный проект представляет собой REST API сервис для управления кошельками, позволяя пополнять баланс, снимать средства и получать информацию о текущем балансе.

## Стек технологий
- Python 3
- Django + Django REST Framework
- PostgreSQL
- Docker + Docker Compose

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <репозиторий>
cd <папка_проекта>
```

### 2. Запуск с помощью Docker
```bash
docker-compose up --build
```

### 3. Создание миграций
```bash
docker-compose exec web python manage.py makemigrations
```

### 4. Применение миграций
```bash
docker-compose exec web python manage.py migrate
```


## API Эндпоинты

### Получить баланс кошелька
**GET /api/v1/wallets/{wallet_uuid}/**
- **Ответ (200 OK):**
```json
{
    "uuid": "b0f4e64c-9b77-4ffb-91f8-98e945b3e3f1",
    "balance": 100.00,
    "created_at": "2025-03-18T12:00:00Z"
}
```

### Операция с балансом (пополнение/снятие)
**POST /api/v1/wallets/{wallet_uuid}/operation**
- **Тело запроса:**
```json
{
    "operation_type": "DEPOSIT",  // Или "WITHDRAW"
    "amount": 500.00
}
```
- **Ответ (200 OK):**
```json
{
    "uuid": "b0f4e64c-9b77-4ffb-91f8-98e945b3e3f1",
    "balance": 600.00
}
```
- **Ошибка (400 Bad Request) при недостаточном балансе:**
```json
{
    "error": "Insufficient balance"
}
```

## Запуск тестов
```bash
docker-compose exec web python manage.py test
```

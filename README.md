# alfapilot

Решение для кейса "Разработка copilot-приложения для клиентов микробизнеса" / Альфа-Будущее хакатон

## Запуск

### Локально в терминале

Создать окружение и переменные окружения (также не забыть заполнить `.env`):

```bash
python3 -m venv venv
source venv/bin/activate
cp .env.example .env
```

Запуск:

```bash
python3 -m bot.main
```

### Docker

Локальный билд

```bash
docker build -t alfapilot .
docker run --name alfapilot -e TOKEN=<TELEGRAM_BOT_TOKEN> alfapilot
```

Или пулл из докерхаба

```bash
docker pull muhammaduss/alfapilot:latest
docker run --name alfapilot -e TOKEN=<TELEGRAM_BOT_TOKEN> muhammaduss/alfapilot
```

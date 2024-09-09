from django.http import HttpResponse
from .bot import start_bot

def start_telegram_bot(request):
    start_bot()
    return HttpResponse("Telegram бот запущен.")

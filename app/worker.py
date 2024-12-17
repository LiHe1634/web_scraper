from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "web_scraper",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.tasks.scraper_tasks']
)

# Celery配置
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1小时
    worker_max_tasks_per_child=100,
    broker_connection_retry_on_startup=True
)

# 定时任务配置
celery_app.conf.beat_schedule = {
    'check-proxies-every-5-minutes': {
        'task': 'app.tasks.scraper_tasks.check_proxies',
        'schedule': 300.0,  # 5分钟
    },
    'update-cookies-every-hour': {
        'task': 'app.tasks.scraper_tasks.update_cookies',
        'schedule': 3600.0,  # 1小时
    },
}

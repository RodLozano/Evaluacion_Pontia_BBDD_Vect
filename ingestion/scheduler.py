from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import NEWS_FETCH_INTERVAL_MINUTES, PRICE_FETCH_INTERVAL_SECONDS
from ingestion.pipeline_news import run_news_pipeline
from ingestion.pipeline_prices import run_prices_pipeline
from vectordb.weaviate_client import get_client
from vectordb.operations import archive_old_news

scheduler = BlockingScheduler()


def archive_job() -> None:
    """Job nocturno: archiva noticias antiguas."""
    client = get_client()
    count = archive_old_news(client)
    print(f"🗄️  {count} noticias archivadas")


def main() -> None:
    print("🚀 Arrancando scheduler de ingesta...")

    # Pipeline A — Noticias cada 15 minutos
    scheduler.add_job(
        run_news_pipeline,
        trigger=IntervalTrigger(minutes=NEWS_FETCH_INTERVAL_MINUTES),
        id="news_pipeline",
        next_run_time=__import__("datetime").datetime.now(),  # Ejecutar al arrancar
    )

    # Pipeline B — Precios cada 60 segundos
    scheduler.add_job(
        run_prices_pipeline,
        trigger=IntervalTrigger(seconds=PRICE_FETCH_INTERVAL_SECONDS),
        id="prices_pipeline",
        next_run_time=__import__("datetime").datetime.now(),
    )

    # Job nocturno — Archivado a las 02:00
    scheduler.add_job(
        archive_job,
        trigger="cron",
        hour=2,
        minute=0,
        id="archive_job",
    )

    print(f"   📰 Noticias: cada {NEWS_FETCH_INTERVAL_MINUTES} minutos")
    print(f"   📈 Precios: cada {PRICE_FETCH_INTERVAL_SECONDS} segundos")
    print(f"   🗄️  Archivado: cada noche a las 02:00")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n⛔ Scheduler detenido")


if __name__ == "__main__":
    main()
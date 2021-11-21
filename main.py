import uvicorn
import logging
from api.settings import get_app_settings
from api import create_app


logger = logging.getLogger("app.main")
app = create_app(testing=False)


def main():
    settings = get_app_settings()
    logger.info(f"Starting , listening on " f"{settings.listen_host}:{settings.listen_port}")
    uvicorn.run(
        "services.app:app",
        host=settings.listen_host,
        port=settings.listen_port,
        reload=settings.debug,
        debug=settings.debug,
    )


if __name__ == "__main__":
    main()

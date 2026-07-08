from fastapi.middleware.gzip import GZipMiddleware

def register_gzip(app):
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )
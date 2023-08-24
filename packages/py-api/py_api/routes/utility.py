class UtilityRoutes:
    @staticmethod
    def bind(app):
        @app.get('/health')
        async def health():
            return {"status": "healthy"}

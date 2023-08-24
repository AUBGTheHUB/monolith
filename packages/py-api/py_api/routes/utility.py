class UtilityRoutes:
    def __init__(self, app):
        @app.get('/health')
        async def health(): 
            return {"status": "healthy"}
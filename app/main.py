from fastapi import FastAPI

def create_app():
    return FastAPI(
        title="Fuzzy Search",
        docs_url="/api/docs",
        description="API app for Fuzzy Search",
        debug=True,
    )
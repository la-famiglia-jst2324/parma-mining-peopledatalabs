"""Main entrypoint for the API routes in of parma-analytics."""

from fastapi import FastAPI

app = FastAPI()


# root endpoint
@app.get("/", status_code=200)
def root():
    """Root endpoint for the API."""
    return {"welcome": "at parma-mining-peopledatalabs"}

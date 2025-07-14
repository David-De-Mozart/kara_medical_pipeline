from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import List
from . import crud, schemas

app = FastAPI()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing_page():
    html_content = """
    <html>
        <head>
            <title>Welcome to the API</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>Welcome to Kara Medical Pipeline API</h1>
            <p>Please choose your documentation interface:</p>
            <a href="/docs" style="font-size: 18px; margin-right: 20px;">Swagger UI</a>
            <a href="/redoc" style="font-size: 18px;">ReDoc</a>
        </body>
    </html>
    """
    return html_content

@app.get("/api/reports/top-products", response_model=List[schemas.ProductCount])
def top_products(limit: int = 10):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=List[schemas.MessageResult])
def search_messages(query: str):
    return crud.search_messages(query)

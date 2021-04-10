from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from name_processor import make_name_response
app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8080/search",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def index_page():
    """
    """
    with open('html/index.html', 'rt') as index_file:
        index_page=index_file.read()
    return index_page

@app.get("/search/")
async def search_name(q: str):
    result = make_name_response(q)
    return result

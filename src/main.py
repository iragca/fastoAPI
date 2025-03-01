import pandas as pd

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.models import character

DATA_PATH = Path() / "data"

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/characters")


@app.get("/characters")
async def get_characters():
    data = pd.read_csv(DATA_PATH / "characters.csv")

    return data["Character Name"].to_dict()


@app.get("/characters/{name}")
async def get_characters_by_name(name):
    data = pd.read_csv(DATA_PATH / "characters.csv")
    name = name.replace("-", " ")
    filtered_data = data[data["Character Name"] == name]

    return {
        "Character Name": filtered_data["Character Name"].values[0],
        "Quote": filtered_data["Quote"].values[0],
    }


@app.post("/create_character")
async def create_character(body: character.Character):
    try:
        data = pd.read_csv(DATA_PATH / "characters.csv")
        name = body.character_name
        quote = body.quote
    except Exception as e:
        return {
            "message": "Something went wrong with the data"
        }

    try:
        data = pd.concat(
            [data, pd.DataFrame({"Character Name": [name], "Quote": [quote]})],
            ignore_index=True,
        )

        data.to_csv(DATA_PATH / "characters.csv", index=False)
    except Exception as e:
        return {
        "message": "Something went wrong",
    }

    return {
        "message": "Character created successfully",
    }


@app.get("/quotes")
async def get_quotes():
    # Get a random quote
    data = pd.read_csv(DATA_PATH / "characters.csv")

    return data["Quote"].sample().to_dict()

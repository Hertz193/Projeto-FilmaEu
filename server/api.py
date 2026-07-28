from fastapi import FastAPI

app = FastAPI()

videos = {
    1: {"title": "volei", "description": "Descrição do Video de volei"},
    2: {"title": "basquete", "description": "Descrição do Video de basquete"},
    3: {"title": "futsal", "description": "Descrição do Video de futsal"},
    4: {"title": "futebol", "description": "Descrição do Video de futebol"}
}

@app.get("/")
def home():
    return {"message": "Minha primeira API com FastAPI"}

@app.get("/replays/{videoID}")
def get_replays(videoID: int):
    if videoID in videos:
        return videos.get(videoID)
    else:
        return {"message": "Video não encontrado"}
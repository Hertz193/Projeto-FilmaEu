from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, video.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {
        "message": "Ok",
        "filename": video.filename,
    }

@app.get("/videos")
async def list_videos():
    videos = [
        file 
        for file in os.listdir(UPLOAD_FOLDER) 
        if file.endswith(".mp4")
    ]
    return {"videos": videos}

@app.get("/video/{filename}")
async def get_video(filename: str):

    filename = Path(filename).name
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
            raise HTTPException(404, "Vídeo não encontrado")

    if not filename.endswith(".mp4"):
        raise HTTPException(400, "Formato inválido")
    
    return FileResponse(
        os.path.join(UPLOAD_FOLDER, filename),
        media_type="video/mp4"
    )

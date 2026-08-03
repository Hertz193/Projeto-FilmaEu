from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from fastapi.responses import StreamingResponse, FileResponse
from pathlib import Path
from typing import BinaryIO
import os
import shutil
import ffmpeg
from pathlib import Path
from datetime import datetime, timedelta


# Back-end API para upload e reprodução de vídeos, utilizando FastAPI e FFmpeg para conversão de formatos.

app = FastAPI()

UPLOAD_FOLDER = "videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CAMINHO_FFMPEG = r"C:\ffmpeg\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"

def limpar_videos_antigos():
    limite = datetime.now() - timedelta(hours=48)

    for arquivo in Path(UPLOAD_FOLDER).glob("*.mp4"):
        data_modificacao = datetime.fromtimestamp(
            arquivo.stat().st_mtime
        )

        if data_modificacao < limite:
            arquivo.unlink()
            print(f"{arquivo.name} removido")

def ler_arquivo_em_blocos(file_obj: BinaryIO, start: int, chunk_size: int, file_size: int):
    file_obj.seek(start)
    bytes_restantes = file_size - start
    while bytes_restantes > 0:
        tamanho_leitura = min(chunk_size, bytes_restantes)
        data = file_obj.read(tamanho_leitura)
        if not data:
            break
        bytes_restantes -= len(data)
        yield data

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    print(">>> ENTROU EM /upload")

    limpar_videos_antigos()

    nome_original = video.filename
    pasta_temporaria = "temp_uploads"
    os.makedirs(pasta_temporaria, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    caminho_temporario = os.path.join(pasta_temporaria, nome_original)
    caminho_final = os.path.join(UPLOAD_FOLDER, nome_original)

    # salva o arquivo bruto vindo da câmera
    try:
        with open(caminho_temporario, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo temporário: {str(e)}")

    print("Cheguei antes do FFmpeg")
    print(CAMINHO_FFMPEG)
    print(os.path.exists(CAMINHO_FFMPEG))

    # executa a conversão com FFmpeg
    try:
        # verifica se o executável do FFmpeg realmente existe no caminho informado
        if not os.path.exists(CAMINHO_FFMPEG):
            raise FileNotFoundError(f"O executável do FFmpeg não foi encontrado em: {CAMINHO_FFMPEG}")

        (
            ffmpeg
            .input(caminho_temporario)
            .output(caminho_final, vcodec='libx264', acodec='aac', movflags='faststart')
            .overwrite_output()
            .run(cmd=CAMINHO_FFMPEG, capture_stdout=True, capture_stderr=True)
        )
        
        # remove o arquivo temporário se a conversão deu certo
        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)
            
    except ffmpeg.Error as e:
        erro_ffmpeg = e.stderr.decode('utf-8') if e.stderr else str(e)
        print(f"Erro crítico no FFmpeg: {erro_ffmpeg}")
        
        shutil.move(caminho_temporario, caminho_final)
        return {
            "message": "Ok (Aviso: salvo sem conversão devido a erro no codec)",
            "filename": nome_original,
            "error_log": erro_ffmpeg[:200] 
        }
    except Exception as e:
        print(f"Erro geral no upload: {str(e)}")
        shutil.move(caminho_temporario, caminho_final)
        return {
            "message": "Ok (Salvo original)",
            "filename": nome_original,
            "error_log": str(e)
        }

    return {
        "message": "Ok",
        "filename": nome_original,
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
async def get_video(filename: str, range: str = Header(None)):
    print(">>> ENTROU EM /video")

    filename = Path(filename).name
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(404, "Vídeo não encontrado")

    if not filename.endswith(".mp4"):
        raise HTTPException(400, "Formato inválido")

    file_size = os.path.getsize(file_path)
    
    start = 0
    end = file_size - 1
    status_code = 200
    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "video/mp4"
    }

    if range:
        try:
            range_bytes = range.replace("bytes=", "").split("-")
            if range_bytes[0]:
                start = int(range_bytes[0])
            if len(range_bytes) > 1 and range_bytes[1]:
                end = int(range_bytes[1])
        except ValueError:
            raise HTTPException(400, "Range inválido")
        
        status_code = 206
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"

    conteudo_comprimento = end - start + 1
    headers["Content-Length"] = str(conteudo_comprimento)

    file_obj = open(file_path, "rb")
    
    def ler_arquivo_em_blocos():
        try:
            file_obj.seek(start)
            bytes_restantes = conteudo_comprimento
            chunk_size = 512 * 1024  # 512KB por bloco
            
            while bytes_restantes > 0:
                tamanho_leitura = min(chunk_size, bytes_restantes)
                data = file_obj.read(tamanho_leitura)
                if not data:
                    break
                bytes_restantes -= len(data)
                yield data
        finally:
            file_obj.close()  

    return StreamingResponse(
        ler_arquivo_em_blocos(),
        status_code=status_code,
        headers=headers
    )

@app.get("/videos/search")
async def search_videos(date: str):
    videos = []

    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".mp4") and date in file:
            videos.append(file)

    videos.sort(reverse=True)

    return {"videos": videos}

@app.get("/download/{filename}")
async def download_video(filename: str):
    print(">>> ENTROU EM /download")

    filename = Path(filename).name
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        raise HTTPException(404, "Vídeo não encontrado")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4"
    )
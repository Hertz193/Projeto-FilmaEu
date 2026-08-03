# Replays IFF

Sistema de replay para quadras poliesportivas desenvolvido para o Instituto Federal Fluminense (IFF).

O projeto utiliza câmeras IP conectadas a Raspberry Pis para gravar continuamente as partidas. Os últimos segundos ficam armazenados em um buffer circular e, quando um botão é acionado, o replay é salvo e enviado automaticamente para um servidor, onde pode ser reproduzido e baixado através de uma interface web.

---

## Funcionalidades

- Captura contínua de vídeo.
- Buffer circular para armazenar os últimos segundos.
- Salvamento do replay sob demanda.
- Upload automático para o servidor.
- Conversão automática dos vídeos para MP4 (FFmpeg).
- Reprodução via navegador.
- Download dos replays.
- Busca de replays por data.
- Remoção automática de vídeos antigos (planejado).

---

## Arquitetura

```
                Raspberry Pi
            (Captura da câmera)
                     │
                     │ Upload HTTP
                     ▼
              FastAPI (Servidor)
          ┌───────────────────────┐
          │ Recebe os vídeos      │
          │ Converte com FFmpeg   │
          │ Gerencia os arquivos  │
          └──────────┬────────────┘
                     │
                     ▼
          Interface Web (Streamlit)
                     │
           Reprodução e download
```

---

## Tecnologias

- Python 3
- OpenCV
- FastAPI
- Streamlit
- FFmpeg
- SQLite *(planejado)*
- Raspberry Pi 5

---

## Estrutura do projeto

```text
ReplaySystem/
│
├── camera/
│   ├── __init__.py
│   ├── main.py
│   ├── master_cam.py
│   ├── cam_capture.py
│   ├── replay_buffer.py
│   ├── uploader.py
│   └── video_recorder.py
│
├── server/
│   ├── __init__.py
│   ├── api.py
│   ├── database.py
│   ├── main.py
│   └── data/
│       └── filmaeu.db
│
├── ui/
│   └── interface.py
│
├── videos/
├── temp_uploads/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositório>
```

Entre na pasta:

```bash
cd ReplaySystem
```

Crie um ambiente virtual.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando

## 1. Coloque as devidas URLs e os IPs certos nos campos necessários

### 2. Inicie a API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

### 3. Inicie a interface

```bash
streamlit run app.py --server.address 0.0.0.0
```

---

### 4. Inicie o Raspberry Pi

```bash
python camera/main.py
```

---

## Fluxo de funcionamento

1. A câmera captura vídeo continuamente.
2. Os frames ficam armazenados em um buffer circular.
3. O botão de replay é pressionado.
4. O replay é salvo.
5. O Raspberry envia o vídeo para o servidor.
6. O servidor converte o vídeo para MP4 utilizando FFmpeg.
7. O vídeo fica disponível na interface web para reprodução e download.

---

## Organização dos vídeos

Os replays são armazenados utilizando o padrão:

```text
replay-AAAA-MM-DD-HH-MM-SS.mp4
```

Exemplo:

```text
replay-2026-07-31-15-42-18.mp4
```

Esse padrão permite localizar rapidamente os vídeos pela data através da interface.

---

## Status do projeto

### Implementado

- Captura de vídeo
- Buffer circular
- Salvamento do replay
- Upload automático
- API REST (FastAPI)
- Conversão utilizando FFmpeg
- Interface Web (Streamlit)
- Reprodução de vídeos
- Busca por data
- Download de replays
- Remoção automática de vídeos antigos

### Em desenvolvimento

- Integração completa com Raspberry Pi
- Banco de dados SQLite
- Suporte a múltiplas câmeras
- Sistema de configuração

---

## Possíveis aplicações

O projeto foi desenvolvido inicialmente para a quadra poliesportiva do IFF Macaé, podendo ser adaptado para:

- Quadras esportivas escolares;
- Competições estudantis;
- Treinamentos esportivos;
- Eventos esportivos internos;
- Outros campi do Instituto Federal Fluminense.

---

## Licença

Projeto acadêmico desenvolvido no Instituto Federal Fluminense (IFF).

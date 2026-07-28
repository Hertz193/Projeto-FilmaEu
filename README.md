# Replay System

Sistema de replay para a quadra poliesportiva do IFF Macaé.

O projeto utiliza uma câmera IP conectada a um Raspberry Pi para manter um buffer dos últimos segundos de vídeo. Quando um botão é acionado, o replay é salvo e enviado para um servidor, onde pode ser acessado por uma interface web.

---

## Objetivos

- Capturar vídeo continuamente.
- Manter um buffer circular dos últimos segundos.
- Salvar replays sob demanda.
- Enviar automaticamente os vídeos para um servidor.
- Disponibilizar os replays por uma interface web.

---

## Tecnologias

- Python 3
- OpenCV
- FastAPI *(em desenvolvimento)*
- SQLite *(planejado)*
- Raspberry Pi 5 *(hardware do projeto)*

---

## Estrutura do projeto

```
ReplaySystem/
|
camera/
│
├── __init__.py
├── main.py
├── master_cam.py
├── cam_capture.py
├── replay_buffer.py
└── video_recorder.py
|
server/
|
├── __init__.py
├── api.py
├── database.py
├── main.py
└── data/
|    └── filmaeu.db
|
ui/
|
.gitignore
requirements.txt
README.md
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

Crie um ambiente virtual:

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

```bash
python main.py
```

---

## Status do projeto

Em desenvolvimento.

### Implementado

- Captura da câmera
- Buffer circular
- Gravação dos últimos segundos

### Planejado

- Integração com Raspberry Pi
- Upload automático
- FastAPI
- Banco de dados
- Interface Web

---

## Licença

Projeto acadêmico desenvolvido para o Instituto Federal Fluminense (IFF).

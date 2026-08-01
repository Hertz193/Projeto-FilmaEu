import streamlit as st
import requests

API_URL = "http://192.168.0.7:8000" # Colocar a URL do servidor aqui

st.set_page_config(page_title="Streaming de Vídeos", layout="wide")
st.title("Replays IFF")

st.header("Encontre seu Replay")

# busca por data
data_busca = st.date_input("Selecione o dia do jogo:")

st.subheader("Os replays disponíveis foram gravados nos seguintes horários:")

resposta = requests.get(
    f"{API_URL}/videos/search",
    params={"date": data_busca.strftime("%Y-%m-%d")}
)

videos = resposta.json()["videos"]

if videos:
    videos_dict = {
        video[18:-4].replace("-", ":"): video
        for video in videos
    }

    video_select = st.selectbox(
        "Selecione o horário do replay:",
        list(videos_dict.keys())
    )

    file = videos_dict[video_select]

    url_download = f"{API_URL}/download/{file}"
    url_video = f"{API_URL}/video/{file}"

    resposta = requests.get(url_download)

    st.link_button(
       "Baixar Replay",
       f"{API_URL}/download/{file}"
    )

    st.video(url_video)
else:
    st.info("Nenhum replay encontrado para a data selecionada.")

st.header("O que é o Replay IFF?")

st.write("O Replay IFF é uma plataforma dedicada a fornecer acesso a replays de jogos que ocorreram nas quadras poliesporticas do IFF (Instituto Federal Fluminense). Nosso objetivo é permitir que jogadores, treinadores e entusiastas do esporte possam rever partidas, analisar desempenhos e compartilhar momentos marcantes. Através de uma interface simples e intuitiva, os usuários podem buscar replays por data, assistir aos vídeos diretamente na plataforma e explorar o histórico de jogos realizados no IFF. Com o Replay IFF, a experiência esportiva se torna mais acessível e interativa para todos os envolvidos.")

st.header("Como funciona o Replay IFF?")

st.write("Uma vez que um jogo é realizado nas quadras do IFF, a partida é gravada e assim que o botão de salvar replay é pressionado, o vídeo é armazenado em nosso servidor. Os vídeos são então processados e disponibilizados na plataforma Replay IFF. Os usuários podem acessar a plataforma, selecionar a data do jogo desejado e escolher entre os replays disponíveis para assistir. A plataforma pode ser acessada pelo QR Code fornecido no local do jogo ou através do link compartilhado no perfil do Instagram sportsIFFmacaé.")

st.subheader("Créditos e Agradecimentos")
st.write("Hugo Rafael de Medeiros - Desenvolvedor do sistema")
st.write("Nikolas Gomes do Nascimento - Suporte técnico e manutenção do sistema")
st.write("Lab IF Maker - Infraestrutura")
st.write("Receita Federal - Fornecimento de equipamentos")


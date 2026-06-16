import streamlit as st
import pandas as pd

# Configuração da página para ficar bonita no celular e computador
st.set_page_config(
    page_title="Bolão Feltrim Correa - Copa 2026",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização personalizada com CSS (Cores azul e cinza da Feltrim)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    h1 {
        color: #1155cc;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 4px;
        padding: 8px 16px;
        color: #1e293b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1155cc !important;
        color: white !important;
    }
    .leaderboard-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 5px solid #1155cc;
    }
    .podium-1 { border-left: 5px solid #ffd700; background-color: #fffbeb; }
    .podium-2 { border-left: 5px solid #c0c0c0; background-color: #f8fafc; }
    .podium-3 { border-left: 5px solid #cd7f32; background-color: #fff7ed; }
    </style>
""", unsafe_allow_html=True)

# Link público de exportação CSV da planilha do Google Sheets
# Nota: A planilha precisa estar configurada como "Qualquer pessoa com o link pode ler"
SHEET_ID = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"
URL_RESPOSTAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Respostas_Formulario"
URL_RESULTADOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=🎯%20Resultados%20Oficiais"

@st.cache_data(ttl=60)  # Atualiza os dados a cada 60 segundos
def carregar_dados():
    try:
        df_resp = pd.read_csv(URL_RESPOSTAS)
        df_res = pd.read_csv(URL_RESULTADOS)
        return df_resp, df_res
    except Exception as e:
        st.error("Erro ao conectar com a planilha. Certifique-se de que ela está compartilhada no modo 'Leitor para qualquer pessoa com o link'.")
        return None, None

# Carregar os dados
df_respostas, df_resultados = carregar_dados()

st.title("🏆 Bolão Feltrim Correa")
st.write("<p style='text-align: center; color: #64748b;'>Acompanhe a classificação e palpites da Copa 2026 em tempo real!</p>", unsafe_allow_html=True)

if df_respostas is not None and df_resultados is not None:
    # Tratamento de dados de segurança e nomes de colunas
    # Procura a coluna de e-mail e pontos de forma flexível
    col_email = [col for col in df_respostas.columns if 'E-mail' in col or 'Email' in col or 'Usuário' in col or 'Username' in col][0]
    col_pontos = [col for col in df_respostas.columns if 'Pontos Ganhos' in col or 'Pontos' in col][0]
    
    # Abas do aplicativo web
    tab_ranking, tab_palpites, tab_jogos = st.tabs(["📊 Classificação", "🎯 Palpites Individuais", "⚽ Jogos da Rodada"])

    # --- ABA 1: RANKING GERAL ---
    with tab_ranking:
        st.subheader("Leaderboard Geral")
        
        # Agrupar pontos por usuário e ordenar
        ranking = df_respostas.groupby(col_email)[col_pontos].sum().reset_index()
        ranking = ranking.sort_values(by=col_pontos, ascending=False).reset_index(drop=True)
        
        # Renderizar o ranking estilizado
        for idx, row in ranking.iterrows():
            posicao = idx + 1
            usuario = row[col_email].split('@')[0] # exibe apenas a primeira parte do e-mail corporativo
            pontos = int(row[col_pontos]) if pd.notnull(row[col_pontos]) else 0
            
            # Estilos especiais para o pódio
            card_class = "leaderboard-card"
            emoji = "👤"
            if posicao == 1:
                card_class += " podium-1"
                emoji = "🥇"
            elif posicao == 2:
                card_class += " podium-2"
                emoji = "🥈"
            elif posicao == 3:
                card_class += " podium-3"
                emoji = "🥉"
                
            st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 1.2rem; font-weight: bold; width: 30px;">#{posicao}</span>
                        <span style="font-size: 1.2rem;">{emoji}</span>
                        <span style="font-weight: 500; font-size: 1.1rem; color: #1e293b;">{usuario}</span>
                    </div>
                    <span style="font-size: 1.2rem; font-weight: bold; color: #1155cc;">{pontos} pts</span>
                </div>
            """, unsafe_allow_html=True)

    # --- ABA 2: PALPITES INDIVIDUAIS ---
    with tab_palpites:
        st.subheader("Ver Palpites por Participante")
        usuarios_disponiveis = ranking[col_email].unique()
        usuario_selecionado = st.selectbox("Selecione um participante:", usuarios_disponiveis)
        
        if usuario_selecionado:
            palpites_user = df_respostas[df_respostas[col_email] == usuario_selecionado]
            for _, palpite in palpites_user.iterrows():
                # Tenta localizar o nome do jogo
                col_jogo = [col for col in df_respostas.columns if 'ID_Jogo' in col or 'Jogo' in col][0]
                jogo = palpite[col_jogo]
                
                # Procura palpites
                col_m = [col for col in df_respostas.columns if 'Mandante' in col or 'Placar' in col and '1' in col][0]
                col_v = [col for col in df_respostas.columns if 'Visitante' in col or 'Placar' in col and '2' in col][0]
                
                palpite_m = palpite[col_m]
                palpite_v = palpite[col_v]
                pts_ganhos = int(palpite[col_pontos]) if pd.notnull(palpite[col_pontos]) else 0
                
                # Card de palpite individual
                st.info(f"**{jogo}**  \nPalpite: **{palpite_m} x {palpite_v}**  \nPontos obtidos: **{pts_ganhos} pts**")

    # --- ABA 3: RESULTADOS OFICIAIS ---
    with tab_jogos:
        st.subheader("Placar Oficial dos Jogos")
        for _, jogo in df_resultados.iterrows():
            nome_jogo = jogo['Jogo']
            p_m = jogo['Placar Real Mandante']
            p_v = jogo['Placar Real Visitante']
            status = jogo['Status']
            
            placar_texto = f"{int(p_m)} x {int(p_v)}" if pd.notnull(p_m) and pd.notnull(p_v) else "vs"
            badge_status = f"🟢 {status}" if status == "Encerrado" else f"🕒 {status}"
            
            st.markdown(f"""
                <div style="background-color: white; padding: 12px; border-radius: 8px; margin-bottom: 8px; text-align: center; border: 1px solid #e2e8f0;">
                    <p style="font-size: 0.9rem; color: #64748b; margin: 0;">{badge_status}</p>
                    <h4 style="margin: 5px 0;">{nome_jogo}</h4>
                    <p style="font-size: 1.3rem; font-weight: bold; color: #1155cc; margin: 0;">{placar_texto}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Aguardando carregamento da base de dados...")

import streamlit as st
import pandas as pd
import urllib.parse
import requests
import json
import re

st.set_page_config(
    page_title="Bolão Feltrim Correa - Copa 2026",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', Arial, sans-serif;
    }
    
    .main {
        background-color: #f4f7f5;
    }
    
    /* Cabeçalho Temático Brasil Premium */
    .header-title {
        color: #004b23;
        text-align: center;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 2px;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        text-align: center;
        color: #003566;
        font-size: 1.05rem;
        margin-bottom: 25px;
        font-weight: 600;
    }

    /* Tabs Estilizadas em Verde e Amarelo */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
        background-color: #e8efe9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #c2d6c5;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 8px 14px;
        color: #004b23;
        font-weight: 600;
        transition: all 0.25s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #004b23 !important;
        color: #ffbd00 !important;
        box-shadow: 0 4px 10px rgba(0, 75, 35, 0.25);
    }

    /* Alertas Personalizados */
    .custom-warning {
        background-color: #fffdf0;
        border-left: 4px solid #ffbd00;
        color: #856404;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }

    .custom-info {
        background-color: #f0f7f4;
        border-left: 4px solid #004b23;
        color: #004b23;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }

    /* Grid de Estatísticas */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 25px;
    }
    
    .metric-box {
        background-color: white;
        padding: 14px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.04);
        border: 1px solid #e8efe9;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #004b23;
    }
    
    .metric-label {
        font-size: 0.72rem;
        color: #003566;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Pódio Verde e Amarelo Tridimensional */
    .podium-row {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 12px;
        margin-bottom: 30px;
        padding-top: 15px;
    }
    
    .podium-card {
        background: white;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 75, 35, 0.05);
        border: 1px solid #e8efe9;
        flex: 1;
        transition: transform 0.3s;
    }
    
    .podium-card:hover {
        transform: translateY(-5px);
    }
    
    .podium-1 {
        order: 2;
        border-top: 5px solid #ffbd00; /* Amarelo Ouro */
        background: linear-gradient(180deg, #fffdf0 0%, #ffffff 100%);
        min-height: 170px;
    }
    
    .podium-2 {
        order: 1;
        border-top: 5px solid #003566; /* Azul do Globo */
        background: linear-gradient(180deg, #f0f4f8 0%, #ffffff 100%);
        min-height: 145px;
    }
    
    .podium-3 {
        order: 3;
        border-top: 5px solid #004b23; /* Verde Bandeira */
        background: linear-gradient(180deg, #f4faf6 0%, #ffffff 100%);
        min-height: 130px;
    }
    
    .podium-badge {
        font-size: 2rem;
        margin-bottom: 5px;
    }
    
    .podium-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: #1e293b;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .podium-pts {
        font-weight: 800;
        color: #004b23;
        font-size: 1.15rem;
        margin-top: 4px;
    }

    /* Lista do Leaderboard */
    .ranking-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .ranking-item {
        background-color: white;
        padding: 14px 18px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0, 75, 35, 0.02);
        border: 1px solid #e8efe9;
        transition: transform 0.2s ease;
    }
    
    .ranking-item:hover {
        transform: translateX(4px);
    }
    
    .ranking-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .ranking-pos {
        font-size: 0.85rem;
        font-weight: 800;
        color: #003566;
        width: 24px;
    }
    
    .ranking-avatar {
        background-color: #e8efe9;
        color: #004b23;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #c2d6c5;
    }
    
    .ranking-name {
        font-weight: 600;
        color: #334155;
        font-size: 0.95rem;
    }
    
    .ranking-score {
        font-weight: 800;
        color: #004b23;
        font-size: 1.05rem;
    }

    /* Cards de Jogos Estilo FIFA */
    .match-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 14px;
        border: 1px solid #e8efe9;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.03);
    }
    
    .match-header {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .badge-status {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-agendado { background-color: #f1f5f9; color: #475569; }
    .status-andamento { background-color: #fffbeb; color: #b45309; border: 1px solid #fef3c7; }
    .status-encerrado { background-color: #f0f7f4; color: #004b23; border: 1px solid #c2d6c5; }
    
    .match-body {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 700;
        gap: 10px;
    }
    
    .team-container {
        display: flex;
        align-items: center;
        gap: 8px;
        width: 38%;
    }

    .team-left { justify-content: flex-end; text-align: right; }
    .team-right { justify-content: flex-start; text-align: left; }
    
    .team-name {
        font-size: 0.95rem;
        color: #1e293b;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .team-color-circle {
        font-size: 1.2rem;
        line-height: 1;
    }
    
    .match-score-box {
        font-size: 1.6rem;
        font-weight: 800;
        color: #003566;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background-color: #f4f7f5;
        padding: 6px 16px;
        border-radius: 12px;
        border: 1px solid #c2d6c5;
        min-width: 90px;
    }

    /* Formulários e Botões customizados do Brasil */
    .form-container {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e8efe9;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.04);
    }

    /* Sobrescrever estilo dos botões padrões do Streamlit */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #004b23 !important;
        color: #ffffff !important;
        border: 2px solid #ffbd00 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #ffbd00 !important;
        color: #004b23 !important;
        box-shadow: 0 4px 12px rgba(255, 189, 0, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

MAPA_CORES_CIRCULOS = {
    "brasil": "🟢", "brazil": "🟢",
    "argentina": "🔵", "frança": "🔵", "franca": "🔵", "france": "🔵",
    "alemanha": "⚪", "germany": "⚪", "espanha": "🔴", "spain": "🔴",
    "itália": "🔵", "italia": "🔵", "italy": "🔵", "inglaterra": "⚪", "england": "⚪",
    "portugal": "🔴", "holanda": "🟠", "países baixos": "🟠", "netherlands": "🟠",
    "bélgica": "🔴", "belgica": "🔴", "belgium": "🔴", "croácia": "🔴", "croacia": "🔴",
    "uruguai": "🔵", "colômbia": "🟡", "chile": "🔴", "equador": "🟡", "marrocos": "🔴",
    "japão": "🔵", "japan": "🔵", "coreia": "🔴", "korea": "🔴", "senegal": "🟢",
    "eua": "⚪", "usa": "⚪", "estados unidos": "⚪", "méxico": "🟢", "canadá": "🔴",
    "haiti": "🔵", "paraguai": "🔴", "peru": "🔴", "venezuela": "🟣", "bolívia": "🟢",
    "república tcheca": "🔴", "republica tcheca": "🔴", "áfrica do sul": "🟢", "africa do sul": "🟢",
    "suíça": "🔴", "bósnia": "🔵", "catar": "🟣", "escócia": "🔵", "turquia": "🔴",
    "austrália": "🟡", "costa do marfim": "🟠", "curaçau": "🔵", "suécia": "🟡", "tunísia": "🔴",
    "irã": "⚪", "nova zelândia": "⚫", "egito": "🔴", "arábia saudita": "🟢", "cabo verde": "🔵",
    "iraque": "🟢", "noruega": "🔴", "algéria": "🟢", "áustria": "🔴", "jordânia": "🔴",
    "rd do congo": "🔵", "uzbequistão": "🔵", "gana": "🟡", "panamá": "🔴"
}

def obter_circulo_cor(nome_time):
    if not nome_time or pd.isna(nome_time):
        return "⚪"
    nome_clean = str(nome_time).strip().lower()
    nome_sem_emoji = re.sub(r'[^\w\s]', '', nome_clean).strip()
    
    for pais, cor in MAPA_CORES_CIRCULOS.items():
        if pais in nome_sem_emoji:
            return cor
    return "⚪"

def formatar_nome_time(nome_time):
    if not nome_time or pd.isna(nome_time):
        return ""
    nome_limpo = re.sub(r'^[^\w\s]+', '', str(nome_time)).strip()
    return nome_limpo

def embelezar_jogo(nome_jogo):
    if not nome_jogo or pd.isna(nome_jogo) or 'vs' not in str(nome_jogo).lower():
        return str(nome_jogo)
    
    separador = 'vs' if 'vs' in str(nome_jogo).lower() else 'VS'
    partes = str(nome_jogo).split(separador)
    
    time1 = formatar_nome_time(partes[0])
    time2 = formatar_nome_time(partes[1]) if len(partes) > 1 else ""
    
    cor1 = obter_circulo_cor(time1)
    cor2 = obter_circulo_cor(time2)
    
    return f"{cor1} {time1} vs {time2} {cor2}"

SHEET_ID = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"

if "web_app_url" not in st.session_state:
    st.session_state["web_app_url"] = ""

@st.cache_data(ttl=5)
def carregar_dados_seguro():
    df_resp = None
    df_res = None
    erro_resp = None
    erro_res = None
    
    # 1. Tentar ler as respostas de palpites (Procura Inteligente pelas abas de Resposta)
    abas_palpites = ["Form Responses 2", "Respostas_Formulario", "Form Responses 1", "Respostas do formulário 1"]
    for aba in abas_palpites:
        try:
            aba_encoded = urllib.parse.quote(aba)
            url_respostas = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={aba_encoded}"
            df_temp = pd.read_csv(url_respostas)
            if df_temp is not None and not df_temp.empty and len(df_temp.columns) >= 2:
                df_resp = df_temp
                break
        except Exception as e:
            erro_resp = str(e)

    # 2. Tentar carregar a aba de resultados oficiais
    abas_resultados = ["🎯 Resultados Oficiais", "Resultados Oficiais", "Resultados", "Jogos", "Placares"]
    for aba_nome in abas_resultados:
        try:
            aba_encoded = urllib.parse.quote(aba_nome)
            url_tentativa = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={aba_encoded}"
            df_temp = pd.read_csv(url_tentativa)
            if df_temp is not None and not df_temp.empty and any(col in df_temp.columns for col in ['Jogo', 'partida', 'jogo', 'JOGO']):
                df_res = df_temp
                break
        except Exception as ex:
            erro_res = str(ex)
        
    return df_resp, df_res, erro_resp, erro_res

# Carregamento dos dados
df_respostas_raw, df_resultados_raw, erro_resp, erro_res = carregar_dados_seguro()

df_respostas = None
df_resultados = None

if df_respostas_raw is not None and not df_respostas_raw.empty:
    df_respostas = df_respostas_raw.dropna(how='all')
    
    # Identificação de email
    col_email_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['email', 'e-mail', 'usuário', 'username', 'quem', 'participante', 'address'])]
    col_email = col_email_list[0] if col_email_list else df_respostas.columns[1]
    df_respostas = df_respostas.dropna(subset=[col_email])

    # Identificação do Nome Completo
    col_nome_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['nome', 'name', 'completo', 'participante', '👤'])]
    col_nome = col_nome_list[0] if col_nome_list else col_email

if df_resultados_raw is not None and not df_resultados_raw.empty:
    df_resultados = df_resultados_raw.dropna(subset=['Jogo'], how='any')
    df_resultados = df_resultados[df_resultados['Jogo'].astype(str).str.strip() != ""]
    df_resultados['Jogo'] = df_resultados['Jogo'].astype(str).str.strip()
    df_resultados['Status'] = df_resultados['Status'].fillna('Agendado').astype(str).str.strip()

# Renderização do cabeçalho temático do Brasil
st.write('<h1 class="header-title">🏆 Bolão Feltrim Correa</h1>', unsafe_allow_html=True)
st.write('<p class="header-subtitle">🇧🇷 Rumo ao Hexa - Classificação em Tempo Real!</p>', unsafe_allow_html=True)

if df_respostas is not None and not df_respostas.empty:

    # Mapeando os nomes completos dos competidores a partir de seus emails para exibição no ranking
    mapa_nomes = df_respostas.groupby(col_email)[col_nome].first().to_dict()

    def obter_nome_exibicao(email_val):
        nome_completo = mapa_nomes.get(email_val, email_val)
        if nome_completo == email_val and "@" in str(email_val):
            return str(email_val).split('@')[0].capitalize()
        return str(nome_completo).title()

    def calcular_pontos_participante(row):
        """Calcula dinamicamente a pontuação de cada palpite baseado em tendência."""
        if df_resultados is None or df_resultados.empty:
            return 0
        
        pontos_totais = 0
        
        # Mapeia colunas de jogos nas respostas do formulário
        for col_name in df_respostas.columns:
            if "vs" in col_name.lower() or "⚽" in col_name:
                palpite_usuario = str(row[col_name]).strip()
                if not palpite_usuario or pd.isna(row[col_name]) or palpite_usuario.lower() == 'nan':
                    continue
                
                # Encontrar o jogo correspondente nos Resultados Oficiais
                jogo_limpo_respostas = formatar_nome_time(col_name).lower()
                jogo_oficial = df_resultados[df_resultados['Jogo'].apply(formatar_nome_time).str.lower() == jogo_limpo_respostas]
                
                if jogo_oficial.empty:
                    # Tenta busca parcial caso o nome da coluna de perguntas tenha data ex: "(18/06)"
                    jogo_oficial = df_resultados[df_resultados['Jogo'].apply(lambda x: formatar_nome_time(x).lower() in jogo_limpo_respostas)]
                
                if not jogo_oficial.empty:
                    real_m = jogo_oficial.iloc[0]['Placar Real Mandante']
                    real_v = jogo_oficial.iloc[0]['Placar Real Visitante']
                    status = jogo_oficial.iloc[0]['Status']
                    
                    if pd.isna(real_m) or pd.isna(real_v) or status != "Encerrado":
                        continue
                        
                    try:
                        val_r_m = int(float(real_m))
                        val_r_v = int(float(real_v))
                    except Exception:
                        continue
                    
                    # Determinar o resultado oficial real
                    times_split = str(jogo_oficial.iloc[0]['Jogo']).split('vs') if 'vs' in str(jogo_oficial.iloc[0]['Jogo']).lower() else str(jogo_oficial.iloc[0]['Jogo']).split('VS')
                    time_m = formatar_nome_time(times_split[0])
                    time_v = formatar_nome_time(times_split[1]) if len(times_split) > 1 else ""
                    
                    if val_r_m > val_r_v:
                        resultado_real = f"vitoria do {time_m.lower()}"
                    elif val_r_v > val_r_m:
                        resultado_real = f"vitoria do {time_v.lower()}"
                    else:
                        resultado_real = "empate"
                    
                    # Comparar palpite com o resultado real
                    palpite_clean = palpite_usuario.lower()
                    
                    # Verificação inteligente (ex: "vitoria do brasil" ou "empate")
                    if resultado_real == "empate" and "empate" in palpite_clean:
                        pontos_totais += 10 # Acertou o empate
                    elif "vitoria" in resultado_real:
                        time_vencedor = resultado_real.replace("vitoria do ", "").strip()
                        if time_vencedor in palpite_clean:
                            pontos_totais += 10 # Acertou o time vencedor!
                            
        return pontos_totais

    # Criando o ranking aplicando a pontuação inteligente
    df_respostas['Pontos_Calculados'] = df_respostas.apply(calcular_pontos_participante, axis=1)

    # Abas principais do aplicativo do Bolão
    tab_ranking, tab_enviar, tab_palpites, tab_jogos = st.tabs([
        "📊 Classificação", 
        "📝 Dar Palpite", 
        "🎯 Ver Palpites", 
        "⚽ Resultados Reais"
    ])

    with tab_ranking:
        ranking = df_respostas.groupby(col_email)['Pontos_Calculados'].sum().reset_index()
        ranking = ranking.sort_values(by='Pontos_Calculados', ascending=False).reset_index(drop=True)
        
        total_participantes = len(ranking)
        lider_atual = obter_nome_exibicao(ranking.iloc[0][col_email]) if total_participantes > 0 else "-"
        media_pontos = int(ranking['Pontos_Calculados'].mean()) if total_participantes > 0 else 0
        
        st.markdown(f"""
            <div class="metrics-container">
                <div class="metric-box">
                    <div class="metric-value">{total_participantes}</div>
                    <div class="metric-label">Competidores</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">🥇 {lider_atual.split()[0]}</div>
                    <div class="metric-label">Líder Atual</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{media_pontos} pts</div>
                    <div class="metric-label">Média Geral</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Pódio premium tridimensional baseado nas 3 primeiras posições
        p1_nome, p1_pts = "Aguardando", "0 pts"
        p2_nome, p2_pts = "Aguardando", "0 pts"
        p3_nome, p3_pts = "Aguardando", "0 pts"
        
        if len(ranking) > 0:
            p1_nome = obter_nome_exibicao(ranking.iloc[0][col_email])
            p1_pts = f"{int(ranking.iloc[0]['Pontos_Calculados'])} pts"
        if len(ranking) > 1:
            p2_nome = obter_nome_exibicao(ranking.iloc[1][col_email])
            p2_pts = f"{int(ranking.iloc[1]['Pontos_Calculados'])} pts"
        if len(ranking) > 2:
            p3_nome = obter_nome_exibicao(ranking.iloc[2][col_email])
            p3_pts = f"{int(ranking.iloc[2]['Pontos_Calculados'])} pts"
            
        st.markdown(f"""
            <div class="podium-row">
                <div class="podium-card podium-2">
                    <div class="podium-badge">🥈</div>
                    <div class="podium-name" title="{p2_nome}">{p2_nome}</div>
                    <div class="podium-pts">{p2_pts}</div>
                </div>
                <div class="podium-card podium-1">
                    <div class="podium-badge">🥇</div>
                    <div class="podium-name" title="{p1_nome}">{p1_nome}</div>
                    <div class="podium-pts">{p1_pts}</div>
                </div>
                <div class="podium-card podium-3">
                    <div class="podium-badge">🥉</div>
                    <div class="podium-name" title="{p3_nome}">{p3_nome}</div>
                    <div class="podium-pts">{p3_pts}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="ranking-list">', unsafe_allow_html=True)
        for idx, row in ranking.iterrows():
            posicao = idx + 1
            if posicao <= 3:
                continue
                
            usuario = obter_nome_exibicao(row[col_email])
            pontos = int(row['Pontos_Calculados'])
            inicial = usuario[0]
            
            st.markdown(f"""
                <div class="ranking-item">
                    <div class="ranking-left">
                        <span class="ranking-pos">#{posicao}</span>
                        <div class="ranking-avatar">{inicial}</div>
                        <span class="ranking-name">{usuario}</span>
                    </div>
                    <span class="ranking-score">{pontos} pts</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_enviar:
        st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Registre seu Palpite Oficial</h3>", unsafe_allow_html=True)
        
        if not st.session_state["web_app_url"]:
            st.markdown("""
                <div class="custom-info">
                    <div>
                        <strong>ℹ️ Integração com a Planilha:</strong> Configure sua URL de automação do Google Apps Script uma única vez abaixo para ativar a gravação em tempo real.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            url_input = st.text_input("Cole aqui a URL do seu Apps Script (Web App):", placeholder="https://script.google.com/macros/s/.../exec")
            if url_input:
                st.session_state["web_app_url"] = url_input
                st.success("Automação do formulário ativada com sucesso!")
                st.rerun()
        else:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            with st.form("form_palpite", clear_on_submit=True):
                email_user = st.text_input("Seu E-mail Corporativo:", placeholder="exemplo@feltrim.com.br").strip().lower()
                nome_user = st.text_input("Seu Nome Completo:", placeholder="Digite seu nome completo").strip()
                
                # Coleta dinâmica de jogos sem "nan"
                lista_jogos_display = ["Selecione uma partida..."]
                lista_jogos_valores = ["Selecione uma partida..."]
                
                if df_resultados is not None and not df_resultados.empty:
                    jogos_ativos = df_resultados[df_resultados['Status'] != 'Encerrado']
                    origem_lista = jogos_ativos if not jogos_ativos.empty else df_resultados
                    for _, r in origem_lista.iterrows():
                        jogo_limpo = str(r['Jogo']).strip()
                        if jogo_limpo and jogo_limpo.lower() != 'nan':
                            lista_jogos_display.append(embelezar_jogo(jogo_limpo))
                            lista_jogos_valores.append(jogo_limpo)
                
                jogo_index = st.selectbox("Qual partida você quer palpitar?", range(len(lista_jogos_display)), format_func=lambda x: lista_jogos_display[x])
                jogo_selecionado = lista_jogos_valores[jogo_index]
                
                # Mapeando os palpites de tendência (Vitória Time 1, Empate, Vitória Time 2)
                opcoes_palpite = ["Selecione seu palpite..."]
                if jogo_selecionado != "Selecione uma partida...":
                    times_split = jogo_selecionado.split('vs') if 'vs' in jogo_selecionado.lower() else jogo_selecionado.split('VS')
                    t1 = formatar_nome_time(times_split[0])
                    t2 = formatar_nome_time(times_split[1]) if len(times_split) > 1 else ""
                    opcoes_palpite = [
                        f"Vitória do {t1}",
                        "Empate",
                        f"Vitória do {t2}"
                    ]
                
                palpite_selecionado = st.selectbox("Seu Palpite de Resultado:", opcoes_palpite)
                
                enviar = st.form_submit_button("🔥 Gravar meu Palpite!")
                
                if enviar:
                    if not email_user or "@" not in email_user:
                        st.error("❌ Digite um e-mail corporativo válido.")
                    elif not nome_user:
                        st.error("❌ Digite o seu nome completo.")
                    elif jogo_selecionado == "Selecione uma partida...":
                        st.error("❌ Por favor, selecione uma partida da lista.")
                    elif palpite_selecionado == "Selecione seu palpite...":
                        st.error("❌ Por favor, selecione o seu palpite de vencedor/empate.")
                    else:
                        with st.spinner("Gravando direto na planilha..."):
                            payload = {
                                "email": email_user,
                                "nome": nome_user,
                                "id_jogo": jogo_selecionado,
                                "palpite": palpite_selecionado
                            }
                            
                            try:
                                response = requests.post(
                                    st.session_state["web_app_url"], 
                                    data=json.dumps(payload),
                                    headers={"Content-Type": "application/json"}
                                )
                                
                                if response.status_code == 200:
                                    st.success(f"🎉 Palpite registrado com sucesso!")
                                    st.balloons()
                                    st.cache_data.clear()
                                else:
                                    st.error(f"Erro no servidor Google: {response.text}")
                            except Exception as ex:
                                st.error(f"Erro de envio. Detalhes: {ex}")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_palpites:
        st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Consulta de Participante</h3>", unsafe_allow_html=True)
        
        # Mapeando emails únicos para nomes na caixa de seleção
        usuarios_nomes_map = {email: obter_nome_exibicao(email) for email in df_respostas[col_email].unique()}
        usuarios_ordenados = sorted(usuarios_nomes_map.items(), key=lambda item: item[1])
        
        usuario_email_selecionado = st.selectbox(
            "Selecione um participante para ver todos os palpites:", 
            options=[item[0] for item in usuarios_ordenados], 
            format_func=lambda x: usuarios_nomes_map[x]
        )
        
        if usuario_email_selecionado:
            palpites_user = df_respostas[df_respostas[col_email] == usuario_email_selecionado].iloc[0]
            
            for col_name in df_respostas.columns:
                if "vs" in col_name.lower() or "⚽" in col_name:
                    palpite_val = palpites_user[col_name]
                    if pd.isna(palpite_val) or str(palpite_val).strip().lower() == 'nan':
                        continue
                    
                    jogo_embelezado = embelezar_jogo(col_name)
                    st.markdown(f"""
                        <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #e8efe9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,75,35,0.01);">
                            <div>
                                <p style="font-weight: 700; color: #1e293b; margin: 0; font-size: 0.95rem;">{jogo_embelezado}</p>
                                <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #003566; font-weight:600;">Palpite: <strong style="color: #004b23;">{palpite_val}</strong></p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_jogos:
        st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Placares Reais dos Jogos</h3>", unsafe_allow_html=True)
        
        if df_resultados is not None and not df_resultados.empty:
            for _, jogo in df_resultados.iterrows():
                nome_jogo = jogo['Jogo']
                p_m = jogo['Placar Real Mandante']
                p_v = jogo['Placar Real Visitante']
                status = jogo['Status']
                
                p_m_display = str(int(float(p_m))) if pd.notna(p_m) else ""
                p_v_display = str(int(float(p_v))) if pd.notna(p_v) else ""
                
                if status == "Encerrado":
                    badge_class = "badge-status status-encerrado"
                    badge_label = "🟢 Encerrado"
                elif status == "Em Andamento":
                    badge_class = "badge-status status-andamento"
                    badge_label = "🟡 Ao Vivo"
                else:
                    badge_class = "badge-status status-agendado"
                    badge_label = "🕒 Agendado"
                
                tem_placar = p_m_display != "" and p_v_display != ""
                placar_html = f'<div class="match-score-box"><span>{p_m_display}</span><span>-</span><span>{p_v_display}</span></div>' if tem_placar else '<div class="match-score-box" style="font-size: 1.1rem; color: #003566; font-weight: 600;">VS</div>'
                
                times = str(nome_jogo).split('vs') if 'vs' in str(nome_jogo) else str(nome_jogo).split('VS')
                time1 = formatar_nome_time(times[0].strip()) if len(times) > 0 else "Mandante"
                time2 = formatar_nome_time(times[1].strip()) if len(times) > 1 else "Visitante"
                
                cor1 = obter_circulo_cor(time1)
                cor2 = obter_circulo_cor(time2)
                
                st.markdown(f"""
                    <div class="match-card">
                        <div class="match-header">
                            <span class="{badge_class}">{badge_label}</span>
                        </div>
                        <div class="match-body">
                            <div class="team-container team-left">
                                <span class="team-name">{time1}</span>
                                <span class="team-color-circle">{cor1}</span>
                            </div>
                            {placar_html}
                            <div class="team-container team-right">
                                <span class="team-color-circle">{cor2}</span>
                                <span class="team-name">{time2}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="custom-warning">
                    <p style="font-weight: 700; margin: 0 0 10px 0; font-size: 1.05rem;">📍 Aba "🎯 Resultados Oficiais" não encontrada!</p>
                    <p style="margin: 0; font-size: 0.85rem;">Certifique-se de ter criado a aba com o nome correto na sua planilha do Google.</p>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="custom-info" style="text-align: center; padding: 30px;">
            <p style="font-size: 2.5rem; margin: 0 0 15px 0;">🏆</p>
            <p style="font-weight: 700; font-size: 1.2rem; margin: 0 0 10px 0; color: #004b23;">Bem-vindo ao Bolão Feltrim Correa!</p>
            <p style="margin: 0; color: #003566;">Nenhum palpite foi cadastrado ainda na aba <strong>Form Responses 2</strong>. Vá na aba <strong>📝 Dar Palpite</strong> para registrar a primeira jogada!</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
with st.expander("🛠️ Painel de Diagnóstico do Administrador (Clique para expandir)"):
    st.subheader("Configurações do Banco de Dados")
    st.write(f"**ID da Planilha Configurado:** `{SHEET_ID}`")
    
    col_diag1, col_diag2 = st.columns(2)
    
    with col_diag1:
        st.write("**Aba 'Form Responses 2' (Palpites):**")
        if df_respostas_raw is not None:
            st.success(f"Encontrada com sucesso! ({len(df_respostas_raw)} linhas)")
            st.write(f"**Colunas Identificadas:** {list(df_respostas_raw.columns)[:5]}...")
        else:
            st.error("Aba não encontrada! Verifique o nome 'Form Responses 2'.")
                
    with col_diag2:
        st.write("**Aba 'Resultados Oficiais':**")
        if df_resultados_raw is not None:
            st.success("Encontrada com sucesso!")
        else:
            st.warning("Não encontrada.")

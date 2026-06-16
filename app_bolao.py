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

# Estilização CSS Premium customizada para evitar componentes padrão "feios"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', Arial, sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    /* Cabeçalho Premium */
    .header-title {
        color: #1e3a8a;
        text-align: center;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 2px;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 30px;
        font-weight: 500;
    }

    /* Tabs Estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 8px 16px;
        color: #64748b;
        font-weight: 600;
        transition: all 0.25s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.25);
    }

    /* Alertas customizados bonitos (evitando st.warning feio) */
    .custom-warning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #b45309;
        padding: 16px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .custom-info {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        color: #1d4ed8;
        padding: 16px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
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
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01), 0 2px 4px -1px rgba(0,0,0,0.01);
        border: 1px solid #f1f5f9;
    }
    
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1e3a8a;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Pódio Tridimensional */
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
        box-shadow: 0 10px 20px rgba(0,0,0,0.03);
        border: 1px solid #f1f5f9;
        flex: 1;
        transition: transform 0.3s;
    }
    
    .podium-card:hover {
        transform: translateY(-5px);
    }
    
    .podium-1 {
        order: 2;
        border-top: 5px solid #fbbf24;
        background: linear-gradient(180deg, #fefdf0 0%, #ffffff 100%);
        min-height: 170px;
    }
    
    .podium-2 {
        order: 1;
        border-top: 5px solid #94a3b8;
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        min-height: 145px;
    }
    
    .podium-3 {
        order: 3;
        border-top: 5px solid #d97706;
        background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);
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
        color: #1e3a8a;
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
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        border: 1px solid #f1f5f9;
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
        color: #94a3b8;
        width: 24px;
    }
    
    .ranking-avatar {
        background-color: #eff6ff;
        color: #2563eb;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .ranking-name {
        font-weight: 600;
        color: #334155;
        font-size: 0.95rem;
    }
    
    .ranking-score {
        font-weight: 800;
        color: #1e3a8a;
        font-size: 1.05rem;
    }

    /* Visual dos Jogos Estilo FIFA (Match Cards) */
    .match-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
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
    .status-andamento { background-color: #fef3c7; color: #d97706; }
    .status-encerrado { background-color: #dcfce7; color: #166534; }
    
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

    .team-flag {
        font-size: 1.5rem;
        line-height: 1;
    }
    
    .match-score-box {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background-color: #f8fafc;
        padding: 6px 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        min-width: 90px;
    }

    /* Caixas de Formulário */
    .form-container {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# Dicionário robusto de mapeamento de seleções e bandeiras correspondentes
MAPA_BANDEIRAS = {
    "brasil": "🇧🇷", "brazil": "🇧🇷",
    "argentina": "🇦🇷",
    "frança": "🇫🇷", "franca": "🇫🇷", "france": "🇫🇷",
    "alemanha": "🇩🇪", "germany": "🇩🇪",
    "espanha": "🇪🇸", "spain": "🇪🇸",
    "itália": "🇮🇹", "italia": "🇮🇹", "italy": "🇮🇹",
    "inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "portugal": "🇵🇹",
    "holanda": "🇳🇱", "países baixos": "🇳🇱", "netherlands": "🇳🇱",
    "bélgica": "🇧🇪", "belgica": "🇧🇪", "belgium": "🇧🇪",
    "croácia": "🇭🇷", "croacia": "🇭🇷", "croatia": "🇭🇷",
    "uruguai": "🇺🇾", "uruguay": "🇺🇾",
    "colômbia": "🇨🇴", "colombia": "🇨🇴",
    "chile": "🇨🇱",
    "equador": "🇪🇨", "ecuador": "🇪🇨",
    "marrocos": "🇲🇦", "morocco": "🇲🇦",
    "japão": "🇯🇵", "japao": "🇯🇵", "japan": "🇯🇵",
    "coreia": "🇰🇷", "korea": "🇰🇷",
    "senegal": "🇸🇳",
    "eua": "🇺🇸", "usa": "🇺🇸", "estados unidos": "🇺🇸",
    "méxico": "🇲🇽", "mexico": "🇲🇽",
    "canadá": "🇨🇦", "canada": "🇨🇦",
    "haiti": "🇭🇹", "paraguai": "🇵🇾", "peru": "🇵🇪",
    "venezuela": "🇻🇪", "bolívia": "🇧🇴", "bolivia": "🇧🇴"
}

def obter_bandeira(nome_time):
    """Retorna a bandeira correspondente ao país ou uma padrão."""
    if not nome_time:
        return "🏳️"
    nome_clean = str(nome_time).strip().lower()
    
    # Remove emojis existentes do nome do time para tratamento limpo
    nome_sem_emoji = re.sub(r'[^\w\s]', '', nome_clean).strip()
    
    for pais, bandeira in MAPA_BANDEIRAS.items():
        if pais in nome_sem_emoji:
            return bandeira
    return "🏳️"

def formatar_nome_time(nome_time):
    """Limpa o nome do time de qualquer emoji pré-existente para evitar duplicação feia."""
    if not nome_time:
        return ""
    # Remove caracteres especiais/emojis no início
    nome_limpo = re.sub(r'^[^\w\s]+', '', str(nome_time)).strip()
    return nome_limpo

def embelezar_jogo(nome_jogo):
    """Divide o jogo 'Mandante vs Visitante' e reconstrói com bandeiras lindas."""
    if not nome_jogo or 'vs' not in str(nome_jogo).lower():
        return str(nome_jogo)
    
    separador = 'vs' if 'vs' in str(nome_jogo).lower() else 'VS'
    partes = str(nome_jogo).split(separador)
    
    time1 = formatar_nome_time(partes[0])
    time2 = formatar_nome_time(partes[1]) if len(partes) > 1 else ""
    
    bandeira1 = obter_bandeira(time1)
    bandeira2 = obter_bandeira(time2)
    
    return f"{bandeira1} {time1} vs {time2} {bandeira2}"

SHEET_ID = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"

# Codificação das abas para importação direta via CSV do Google Sheets
sheet_res_encoded = urllib.parse.quote("Form Responses 2")

URL_RESPOSTAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_res_encoded}"

if "web_app_url" not in st.session_state:
    st.session_state["web_app_url"] = ""

@st.cache_data(ttl=5)
def carregar_dados_seguro():
    df_resp = None
    df_res = None
    erro_resp = None
    erro_res = None
    
    # Tentativa de carregar respostas
    try:
        df_resp = pd.read_csv(URL_RESPOSTAS)
    except Exception as e:
        erro_resp = str(e)

    # Tentativa inteligente e sequencial de carregar a aba de resultados oficiais (com e sem emoji)
    tentativas_abas = ["🎯 Resultados Oficiais", "Resultados Oficiais", "Resultados", "Jogos"]
    for aba_nome in tentativas_abas:
        try:
            aba_encoded = urllib.parse.quote(aba_nome)
            url_tentativa = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={aba_encoded}"
            df_temp = pd.read_csv(url_tentativa)
            # Verifica se possui as colunas necessárias para ser a aba correta
            if df_temp is not None and not df_temp.empty and 'Jogo' in df_temp.columns:
                df_res = df_temp
                break
        except Exception as ex:
            erro_res = str(ex)
        
    return df_resp, df_res, erro_resp, erro_res

df_respostas_raw, df_resultados_raw, erro_resp, erro_res = carregar_dados_seguro()

df_respostas = None
df_resultados = None

# Higienização e estruturação inteligente da aba de respostas do formulário
if df_respostas_raw is not None and not df_respostas_raw.empty:
    df_respostas = df_respostas_raw.dropna(how='all')
    
    col_email_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['email', 'e-mail', 'usuário', 'username', 'quem'])]
    col_email = col_email_list[0] if col_email_list else df_respostas.columns[1]
    df_respostas = df_respostas.dropna(subset=[col_email])
    
    col_jogo_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['jogo', 'partida', 'id_jogo', 'qual partida'])]
    col_jogo = col_jogo_list[0] if col_jogo_list else df_respostas.columns[2]
    df_respostas = df_respostas.dropna(subset=[col_jogo])
    
    col_p_m_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['mandante', 'gols 1', 'placar 1', 'gols mandante'])]
    col_p_v_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['visitante', 'gols 2', 'placar 2', 'gols visitante'])]
    col_p_m = col_p_m_list[0] if col_p_m_list else df_respostas.columns[3]
    col_p_v = col_p_v_list[0] if col_p_v_list else df_respostas.columns[4]

# Higienização da aba de resultados (removendo linhas vazias indesejadas que geram "nan")
if df_resultados_raw is not None and not df_resultados_raw.empty:
    df_resultados = df_resultados_raw.dropna(subset=['Jogo'], how='any')
    df_resultados = df_resultados[df_resultados['Jogo'].astype(str).str.strip() != ""]
    df_resultados['Jogo'] = df_resultados['Jogo'].astype(str).str.strip()
    df_resultados['Status'] = df_resultados['Status'].fillna('Agendado').astype(str).str.strip()

st.write('<h1 class="header-title">🏆 Bolão Feltrim Correa</h1>', unsafe_allow_html=True)
st.write('<p class="header-subtitle">Central de palpites e classificação em tempo real!</p>', unsafe_allow_html=True)

if df_respostas is not None and not df_respostas.empty:

    # Cálculo dinâmico e seguro de pontos feito diretamente em Python
    def calcular_pontos(row):
        if df_resultados is None or df_resultados.empty:
            return 0
        
        jogo_palpitado = formatar_nome_time(row[col_jogo]).lower()
        
        # Encontra o jogo correspondente independentemente de caixa ou formatação de emojis
        jogo_oficial = df_resultados[df_resultados['Jogo'].apply(formatar_nome_time).str.lower() == jogo_palpitado]
        
        if jogo_oficial.empty:
            return 0
            
        real_m = jogo_oficial.iloc[0]['Placar Real Mandante']
        real_v = jogo_oficial.iloc[0]['Placar Real Visitante']
        status = jogo_oficial.iloc[0]['Status']
        
        if pd.isna(real_m) or pd.isna(real_v) or status != "Encerrado":
            return 0
            
        try:
            val_p_m = int(row[col_p_m])
            val_p_v = int(row[col_p_v])
            val_r_m = int(real_m)
            val_r_v = int(real_v)
        except Exception:
            return 0
            
        if val_p_m == val_r_m and val_p_v == val_r_v:
            return 10
            
        signo_palpite = (val_p_m > val_p_v) - (val_p_m < val_p_v)
        signo_real = (val_r_m > val_r_v) - (val_r_m < val_r_v)
        
        if signo_palpite == signo_real:
            return 5
            
        return 0

    df_respostas['Pontos_Calculados'] = df_respostas.apply(calcular_pontos, axis=1)

    tab_ranking, tab_enviar, tab_palpites, tab_jogos = st.tabs([
        "📊 Classificação", 
        "📝 Dar Palpite", 
        "🎯 Ver Palpites", 
        "⚽ Resultados Reais"
    ])

    # --- ABA 1: RANKING GERAL (LEADERBOARD) ---
    with tab_ranking:
        
        ranking = df_respostas.groupby(col_email)['Pontos_Calculados'].sum().reset_index()
        ranking = ranking.sort_values(by='Pontos_Calculados', ascending=False).reset_index(drop=True)
        
        total_participantes = len(ranking)
        lider_atual = ranking.iloc[0][col_email].split('@')[0].capitalize() if total_participantes > 0 else "-"
        media_pontos = int(ranking['Pontos_Calculados'].mean()) if total_participantes > 0 else 0
        
        st.markdown(f"""
            <div class="metrics-container">
                <div class="metric-box">
                    <div class="metric-value">{total_participantes}</div>
                    <div class="metric-label">Competidores</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">🥇 {lider_atual}</div>
                    <div class="metric-label">Líder Atual</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{media_pontos} pts</div>
                    <div class="metric-label">Média Geral</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        podium_1st_name = "Aguardando"
        podium_1st_pts = "0"
        podium_2nd_name = "Aguardando"
        podium_2nd_pts = "0"
        podium_3rd_name = "Aguardando"
        podium_3rd_pts = "0"
        
        if len(ranking) > 0:
            podium_1st_name = str(ranking.iloc[0][col_email]).split('@')[0].capitalize()
            podium_1st_pts = f"{int(ranking.iloc[0]['Pontos_Calculados'])} pts"
        if len(ranking) > 1:
            podium_2nd_name = str(ranking.iloc[1][col_email]).split('@')[0].capitalize()
            podium_2nd_pts = f"{int(ranking.iloc[1]['Pontos_Calculados'])} pts"
        if len(ranking) > 2:
            podium_3rd_name = str(ranking.iloc[2][col_email]).split('@')[0].capitalize()
            podium_3rd_pts = f"{int(ranking.iloc[2]['Pontos_Calculados'])} pts"
            
        st.markdown(f"""
            <div class="podium-row">
                <div class="podium-card podium-2">
                    <div class="podium-badge">🥈</div>
                    <div class="podium-name">{podium_2nd_name}</div>
                    <div class="podium-pts">{podium_2nd_pts}</div>
                </div>
                <div class="podium-card podium-1">
                    <div class="podium-badge">🥇</div>
                    <div class="podium-name">{podium_1st_name}</div>
                    <div class="podium-pts">{podium_1st_pts}</div>
                </div>
                <div class="podium-card podium-3">
                    <div class="podium-badge">🥉</div>
                    <div class="podium-name">{podium_3rd_name}</div>
                    <div class="podium-pts">{podium_3rd_pts}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="ranking-list">', unsafe_allow_html=True)
        for idx, row in ranking.iterrows():
            posicao = idx + 1
            if posicao <= 3:
                continue  # Pula o top 3 do pódio
                
            usuario = str(row[col_email]).split('@')[0].capitalize()
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

    # --- ABA 2: ENVIAR PALPITE DIRETAMENTE ---
    with tab_enviar:
        st.write("<h3 style='font-weight: 700; color: #1e3a8a; margin-top: 10px;'>Registre seu Palpite Oficial</h3>", unsafe_allow_html=True)
        
        if not st.session_state["web_app_url"]:
            st.markdown("""
                <div class="custom-info">
                    <span>ℹ️</span>
                    <div>
                        <strong>Integração com a Planilha:</strong> Configure sua URL de automação do Google Apps Script uma única vez abaixo para ativar a gravação em tempo real.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            url_input = st.text_input("Cole aqui a URL de implantação do Apps Script (Web App):", placeholder="https://script.google.com/macros/s/.../exec")
            if url_input:
                st.session_state["web_app_url"] = url_input
                st.success("Automação configurada com sucesso!")
                st.rerun()
        else:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            with st.form("form_palpite", clear_on_submit=True):
                email_user = st.text_input("Seu E-mail Corporativo:", placeholder="exemplo@feltrim.com.br").strip().lower()
                
                lista_jogos_display = ["Selecione uma partida..."]
                lista_jogos_valores = ["Selecione uma partida..."]
                
                if df_resultados is not None and not df_resultados.empty:
                    jogos_ativos = df_resultados[df_resultados['Status'] != 'Encerrado']
                    if not jogos_ativos.empty:
                        for _, r in jogos_ativos.iterrows():
                            lista_jogos_display.append(embelezar_jogo(r['Jogo']))
                            lista_jogos_valores.append(r['Jogo'])
                    else:
                        for _, r in df_resultados.iterrows():
                            lista_jogos_display.append(embelezar_jogo(r['Jogo']))
                            lista_jogos_valores.append(r['Jogo'])
                
                jogo_index = st.selectbox("Qual partida você quer palpitar?", range(len(lista_jogos_display)), format_func=lambda x: lista_jogos_display[x])
                jogo_selecionado = lista_jogos_valores[jogo_index]
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    palpite_m = st.number_input("Gols Mandante:", min_value=0, max_value=20, value=0, step=1)
                with col_g2:
                    palpite_v = st.number_input("Gols Visitante:", min_value=0, max_value=20, value=0, step=1)
                
                enviar = st.form_submit_button("🔥 Gravar meu Palpite!")
                
                if enviar:
                    if not email_user or "@" not in email_user:
                        st.error("❌ Digite um e-mail corporativo válido.")
                    elif jogo_selecionado == "Selecione uma partida...":
                        st.error("❌ Por favor, selecione uma partida válida da lista.")
                    else:
                        with st.spinner("Gravando direto na planilha..."):
                            payload = {
                                "email": email_user,
                                "id_jogo": jogo_selecionado,
                                "palpite_m": int(palpite_m),
                                "palpite_v": int(palpite_v)
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
                                st.error(f"Não foi possível enviar. Verifique a URL do script. Detalhe: {ex}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Resetar link de automação", help="Apaga a URL de webhook salva no navegador."):
                st.session_state["web_app_url"] = ""
                st.rerun()

    # --- ABA 3: PALPITES INDIVIDUAIS ---
    with tab_palpites:
        st.write("<h3 style='font-weight: 700; color: #1e3a8a; margin-top: 10px;'>Consulta de Participante</h3>", unsafe_allow_html=True)
        usuarios_disponiveis = sorted(ranking[col_email].unique())
        usuario_selecionado = st.selectbox("Selecione um participante:", usuarios_disponiveis)
        
        if usuario_selecionado:
            palpites_user = df_respostas[df_respostas[col_email] == usuario_selecionado]
            for _, palpite in palpites_user.iterrows():
                jogo_raw = palpite[col_jogo]
                p_m_val = palpite[col_p_m]
                p_v_val = palpite[col_p_v]
                pts_ganhos = int(palpite['Pontos_Calculados'])
                
                jogo_embelezado = embelezar_jogo(jogo_raw)
                
                try:
                    p_m_display = str(int(float(p_m_val))) if pd.notna(p_m_val) else "-"
                    p_v_display = str(int(float(p_v_val))) if pd.notna(p_v_val) else "-"
                except Exception:
                    p_m_display = "-"
                    p_v_display = "-"
                
                ponto_cor = "#16a34a" if pts_ganhos == 10 else ("#2563eb" if pts_ganhos == 5 else "#94a3b8")
                
                st.markdown(f"""
                    <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #f1f5f9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.01);">
                        <div>
                            <p style="font-weight: 700; color: #1e293b; margin: 0; font-size: 0.95rem;">{jogo_embelezado}</p>
                            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">Palpite: <strong style="color: #0f172a;">{p_m_display} x {p_v_display}</strong></p>
                        </div>
                        <span style="background-color: {ponto_cor}10; color: {ponto_cor}; padding: 6px 12px; border-radius: 20px; font-weight: 800; font-size: 0.85rem;">+{pts_ganhos} PTS</span>
                    </div>
                """, unsafe_allow_html=True)

    # --- ABA 4: RESULTADOS OFICIAIS ---
    with tab_jogos:
        st.write("<h3 style='font-weight: 700; color: #1e3a8a; margin-top: 10px;'>Placares Reais dos Jogos</h3>", unsafe_allow_html=True)
        
        if df_resultados is not None and not df_resultados.empty:
            for _, jogo in df_resultados.iterrows():
                nome_jogo = jogo['Jogo']
                p_m = jogo['Placar Real Mandante']
                p_v = jogo['Placar Real Visitante']
                status = jogo['Status']
                
                try:
                    p_m_display = str(int(float(p_m))) if pd.notna(p_m) else ""
                    p_v_display = str(int(float(p_v))) if pd.notna(p_v) else ""
                except Exception:
                    p_m_display = ""
                    p_v_display = ""
                
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
                placar_html = f'<div class="match-score-box"><span>{p_m_display}</span><span>-</span><span>{p_v_display}</span></div>' if tem_placar else '<div class="match-score-box" style="font-size: 1.1rem; color: #94a3b8; font-weight: 600;">VS</div>'
                
                # Divide o nome do time para renderizar com bandeiras gigantes separadas lateralmente
                times = nome_jogo.split('vs') if 'vs' in nome_jogo else nome_jogo.split('VS')
                time1 = formatar_nome_time(times[0].strip()) if len(times) > 0 else "Mandante"
                time2 = formatar_nome_time(times[1].strip()) if len(times) > 1 else "Visitante"
                
                bandeira1 = obter_bandeira(time1)
                bandeira2 = obter_bandeira(time2)
                
                st.markdown(f"""
                    <div class="match-card">
                        <div class="match-header">
                            <span class="{badge_class}">{badge_label}</span>
                        </div>
                        <div class="match-body">
                            <div class="team-container team-left">
                                <span class="team-name">{time1}</span>
                                <span class="team-flag">{bandeira1}</span>
                            </div>
                            {placar_html}
                            <div class="team-container team-right">
                                <span class="team-flag">{bandeira2}</span>
                                <span class="team-name">{time2}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="custom-warning">
                    <span>⚠️</span>
                    <div>
                        <strong>Aba de Jogos não encontrada!</strong><br>
                        Verifique se você criou a aba <strong>🎯 Resultados Oficiais</strong> no seu Google Sheets e adicionou as partidas.
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="custom-info">
            <span>🏆</span>
            <div>
                <strong>Bem-vindo ao Bolão Feltrim Correa!</strong><br>
                Nenhum palpite foi cadastrado ainda. Vá na aba <strong>📝 Dar Palpite</strong> para registrar a primeira partida!
            </div>
        </div>
    """, unsafe_allow_html=True)

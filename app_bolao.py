import streamlit as st
import pandas as pd
import requests
import json
import re
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="Feltrim Correa - Bolão Copa 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Chaves de Integração Consolidadas e Definitivas
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"
DEFAULT_SPREADSHEET_ID = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');
    
    /* Configuração de Fonte Global */
    html, body, [class*="st-"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Fundo de Tela Moderno Soft */
    .stApp {
        background: linear-gradient(135deg, #f8faf9 0%, #f0f4f1 100%);
    }
    
    /* Banner Corporativo Premium */
    .banner-container {
        background: linear-gradient(135deg, #004b23 0%, #002e14 100%);
        color: #ffffff;
        padding: 35px 25px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0, 75, 35, 0.12);
        border-bottom: 4px solid #d4af37;
        position: relative;
        overflow: hidden;
    }
    
    .banner-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -1px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.25);
    }
    
    .banner-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* customizando a barra de abas nativa do Streamlit para harmonia visual */
    div[data-testid="stTabBar"] {
        background-color: #ffffff;
        padding: 6px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }

    div[data-testid="stTabBar"] button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #555 !important;
        padding: 8px 16px !important;
        transition: all 0.25s ease !important;
    }

    /* Destaque Elegante para a Guia "Dar Palpite" (3ª Aba - index 2) */
    div[data-testid="stTabBar"] button:nth-of-type(3) {
        background-color: #eef7f2 !important;
        color: #004b23 !important;
        font-weight: 700 !important;
        border: 1px solid rgba(0, 75, 35, 0.2) !important;
    }

    div[data-testid="stTabBar"] button:nth-of-type(3)[aria-selected="true"] {
        background: linear-gradient(135deg, #004b23 0%, #007736 100%) !important;
        color: #ffffff !important;
        border: 1px solid #d4af37 !important;
    }

    /* Cards de Métricas Premium Unificados */
    .metrics-wrapper {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }

    .metric-card-premium {
        flex: 1;
        min-width: 240px;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #004b23;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        transition: transform 0.2s ease;
    }

    .metric-card-premium:hover {
        transform: translateY(-2px);
    }
    
    .metric-val-premium {
        font-size: 1.8rem;
        font-weight: 800;
        color: #004b23;
        line-height: 1.2;
    }
    
    .metric-lbl-premium {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-top: 6px;
    }
    
    /* Pódio Sleek 3D */
    .podium-wrapper {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 15px;
        margin: 25px 0;
        flex-wrap: wrap;
    }
    
    .podium-box {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0, 75, 35, 0.04);
        flex: 1;
        min-width: 240px;
        transition: transform 0.2s ease;
    }
    
    .podium-box:hover {
        transform: translateY(-4px);
    }
    
    .podium-1 {
        border-top: 5px solid #d4af37;
        background: linear-gradient(180deg, #fffef6 0%, #ffffff 100%);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
        order: 2;
    }
    
    .podium-2 {
        border-top: 5px solid #b5c2b7;
        order: 1;
    }
    
    .podium-3 {
        border-top: 5px solid #ca9063;
        order: 3;
    }
    
    .podium-rank-badge {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 10px auto;
        font-weight: 800;
        font-size: 1.1rem;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
    }
    
    .badge-p1 { background: linear-gradient(135deg, #ffd700, #ffa500); color: white; }
    .badge-p2 { background: linear-gradient(135deg, #e0e0e0, #9e9e9e); color: white; }
    .badge-p3 { background: linear-gradient(135deg, #d7ccc8, #8d6e63); color: white; }
    
    .podium-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #004b23;
        margin-top: 4px;
        word-wrap: break-word;
    }
    
    .podium-points {
        font-size: 1.6rem;
        font-weight: 800;
        color: #004b23;
        margin: 6px 0;
    }

    /* Tabela de Classificação Premium */
    .table-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.04);
        margin-top: 15px;
    }
    
    .premium-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }
    
    .premium-table th {
        background-color: #004b23;
        color: white;
        padding: 14px 18px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .premium-table td {
        padding: 12px 18px;
        border-bottom: 1px solid #f2f2f2;
        font-size: 0.9rem;
        color: #333;
    }
    
    .premium-table tr:last-child td {
        border-bottom: none;
    }
    
    .premium-table tr:hover {
        background-color: #f9fbf9;
    }

    /* Cards de Jogos / Feed de Partidas */
    .match-card {
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 14px; 
        margin-bottom: 14px; 
        border: 1px solid rgba(0,0,0,0.04); 
        box-shadow: 0 3px 10px rgba(0,0,0,0.015);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .match-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
    }

    .badge-open {
        background-color: rgba(0, 75, 35, 0.06);
        color: #004b23;
        border: 1px solid rgba(0, 75, 35, 0.1);
    }
    
    .badge-closed {
        background-color: rgba(217, 4, 41, 0.05);
        color: #d90429;
        border: 1px solid rgba(217, 4, 41, 0.08);
    }

    /* Tickets dos Palpites Lançados (Meus Palpites) */
    .ticket-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.015);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease;
        border: 1px solid rgba(0,0,0,0.04);
    }

    .ticket-card:hover {
        transform: translateY(-2px);
    }

    .ticket-pending { border-left: 5px solid #8d99ae; }
    .ticket-correct { border-left: 5px solid #2b9348; background: linear-gradient(90deg, #f5fbf7 0%, #ffffff 100%); }
    .ticket-wrong { border-left: 5px solid #d90429; background: linear-gradient(90deg, #fff6f6 0%, #ffffff 100%); }

    .ticket-game-title {
        font-weight: 700;
        font-size: 1rem;
        color: #1a1a1a;
        margin-bottom: 6px;
    }

    .ticket-info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 4px;
    }

    .ticket-badge {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        text-transform: uppercase;
    }

    .badge-pending { background-color: #eedfdf00; border: 1px solid #ccc; color: #555; }
    .badge-correct { background-color: #d8f3dc; color: #1b4332; }
    .badge-wrong { background-color: #fcd5ce; color: #641212; }

    /* Customização de Botões Premium Estilo Pill-Shape */
    div.stButton > button {
        background: linear-gradient(135deg, #004b23 0%, #007736 100%) !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        border: 2px solid #d4af37 !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 15px rgba(0, 75, 35, 0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0.85rem !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
        border-color: #ffd700 !important;
        color: #ffffff !important;
    }

    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Estilo Especial para Botão Secundário de Recarregar */
    div[data-testid="stHeader"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

def safe_to_int(val):
    """Converte valores com segurança prevenindo falhas de dados nulos ou strings inválidas."""
    try:
        if pd.isna(val) or val is None or str(val).strip() == "":
            return ""
        return int(float(val))
    except Exception:
        return ""

def obter_datetime_jogo(nome_jogo, horario_str):
    """Gera o objeto datetime completo combinando o dia e hora oficial do jogo."""
    try:
        match_data = re.search(r'(\d{2})/(\d{2})', str(nome_jogo))
        if not match_data:
            return None
        dia, mes = int(match_data.group(1)), int(match_data.group(2))
        
        horario_limpo = "15:00"
        if pd.notna(horario_str) and str(horario_str).strip() != "":
            val = str(horario_str).lower().strip().replace('h', ':')
            match_hora = re.search(r'(\d{1,2}):(\d{2})', val)
            if match_hora:
                horario_limpo = f"{int(match_hora.group(1)):02d}:{int(match_hora.group(2)):02d}"
            else:
                match_hora_sola = re.search(r'(\d{1,2})', val)
                if match_hora_sola:
                    horario_limpo = f"{int(match_hora_sola.group(1)):02d}:00"
                    
        hora, minuto = map(int, horario_limpo.split(':'))
        return datetime(2026, mes, dia, hora, minuto)
    except Exception:
        return None

def chave_ordenacao_jogo(text):
    """Gera chave cronológica para ordenação do DataFrame baseado no dia e mês."""
    match = re.search(r'(\d{2})/(\d{2})', str(text))
    if match:
        dia, mes = int(match.group(1)), int(match.group(2))
        return (mes, dia)
    return (12, 31)

def formatar_time_slug(nome_completo_jogo, time_tipo="mandante"):
    """Separa de forma limpa e formata os nomes dos dois times envolvidos."""
    limpo = str(nome_completo_jogo).replace("⚽", "").strip()
    partes = re.split(r'\s+vs\s+', limpo, flags=re.IGNORECASE)
    if len(partes) >= 2:
        if time_tipo == "mandante":
            return re.sub(r'\s*\(\d{2}/\d{2}\)', '', partes[0]).strip()
        else:
            return re.sub(r'\s*\(\d{2}/\d{2}\)', '', partes[1]).strip()
    return limpo

@st.cache_data(ttl=5)
def fetch_spreadsheet_data(sheet_id, sheet_name):
    """Consome e valida a leitura dos dados do Google Sheets de forma resiliente."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        if df.empty or (df.columns.size > 0 and str(df.columns[0]).startswith("<!DOCTYPE")):
            return None
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None

if 'spreadsheet_id' not in st.session_state:
    st.session_state['spreadsheet_id'] = DEFAULT_SPREADSHEET_ID

sheet_id = st.session_state['spreadsheet_id']

# Leitura e mapeamento de redundância das planilhas
df_palpites = fetch_spreadsheet_data(sheet_id, "Palpites")
if df_palpites is None or df_palpites.empty:
    df_palpites = fetch_spreadsheet_data(sheet_id, "Respostas_Formulario")

df_resultados = fetch_spreadsheet_data(sheet_id, "Resultados")
if df_resultados is None or df_resultados.empty:
    df_resultados = fetch_spreadsheet_data(sheet_id, "Resultados Oficiais")

df_classificacao = fetch_spreadsheet_data(sheet_id, "Classificacao")
if df_classificacao is None or df_classificacao.empty:
    df_classificacao = fetch_spreadsheet_data(sheet_id, "Classificação")

# Caso de erro de conexão ou permissão
if df_resultados is None:
    st.warning("⚠️ **Acesso à Planilha Não Configurado ou Privado**")
    st.info("""
    Garanta que a planilha esteja configurada em modo público para leitura ("Qualquer pessoa com o link pode ler").
    """)
    st.stop()

# Garantia de colunas essenciais
if df_resultados.empty or 'Jogo' not in df_resultados.columns:
    df_resultados_sorted = pd.DataFrame(columns=['Jogo', 'Status', 'Placar Real Mandante', 'Placar Real Visitante', 'Horário'])
else:
    df_resultados_sorted = df_resultados.copy()
    df_resultados_sorted = df_resultados_sorted.dropna(subset=['Jogo'])
    df_resultados_sorted['Jogo'] = df_resultados_sorted['Jogo'].astype(str)
    df_resultados_sorted = df_resultados_sorted[df_resultados_sorted['Jogo'].str.strip() != ""]
    
    if 'Status' not in df_resultados_sorted.columns:
        df_resultados_sorted['Status'] = "🕒 Agendado"
    if 'Horário' not in df_resultados_sorted.columns:
        df_resultados_sorted['Horário'] = "15:00"
        
    df_resultados_sorted['Data_Ordenacao'] = df_resultados_sorted['Jogo'].apply(chave_ordenacao_jogo)
    df_resultados_sorted = df_resultados_sorted.sort_values(by='Data_Ordenacao').drop(columns=['Data_Ordenacao'])

# Fuso horário oficial do Estado de São Paulo (UTC-3)
agora_brasil = datetime.now(timezone.utc) - timedelta(hours=3)

# Exibição da barra flutuante de horário
st.markdown(f"""
<div style="text-align: right; font-size: 0.8rem; color: #555; font-weight: 700; margin-bottom: 12px; letter-spacing: 0.5px;">
    🕒 HORA DE BRASÍLIA (UTC-3): {agora_brasil.strftime('%d/%m/%Y %H:%M:%S')}
</div>
""", unsafe_allow_html=True)

# Banner de Identidade Visual
st.markdown("""
<div class="banner-container">
    <div class="banner-title">🏆 BOLÃO CORPORATIVO FELTRIM CORREA</div>
    <div class="banner-subtitle">Consulte o ranking, lance novos palpites e gerencie suas apostas em tempo real!</div>
</div>
""", unsafe_allow_html=True)

# Lista de abas
abas_nomes = [
    "📊 Classificação Geral", 
    "📅 Jogos & Resultados",
    "📝 Dar Palpite", 
    "🎯 Meus Palpites",
    "⚙️ Painel Admin"
]

abas_selecionadas = st.tabs(abas_nomes)

# --- ABA 0: CLASSIFICAÇÃO GERAL ---
with abas_selecionadas[0]:
    st.markdown("<h2 style='text-align: center; color: #004b23; font-weight: 800; margin-bottom: 25px;'>Placar de Líderes</h2>", unsafe_allow_html=True)

    num_competidores = 0
    lider_nome = "-"
    media_pontos = 0.0

    if df_classificacao is not None and not df_classificacao.empty:
        col_nome_ref = next((c for c in df_classificacao.columns if "participante" in str(c).lower() or "nome" in str(c).lower()), None)
        col_pts_ref = next((c for c in df_classificacao.columns if "pontos" in str(c).lower() or "acumulados" in str(c).lower()), None)
        
        if col_nome_ref and col_pts_ref:
            df_classificacao_clean = df_classificacao[
                df_classificacao[col_nome_ref].astype(str).str.contains("vs|⚽|Timestamp|E-mail", case=False) == False
            ]
            
            num_competidores = len(df_classificacao_clean)
            if num_competidores > 0:
                df_class_sorted = df_classificacao_clean.sort_values(by=col_pts_ref, ascending=False)
                lider_nome = str(df_class_sorted.iloc[0][col_nome_ref]).split("@")[0].title()
                media_pontos = float(df_class_sorted[col_pts_ref].dropna().mean())

    st.markdown(f"""
    <div class="metrics-wrapper">
        <div class="metric-card-premium">
            <div class="metric-val-premium">{num_competidores}</div>
            <div class="metric-lbl-premium">Participantes</div>
        </div>
        <div class="metric-card-premium" style="border-left-color: #d4af37;">
            <div class="metric-val-premium">👑 {lider_nome}</div>
            <div class="metric-lbl-premium">Líder do Ranking</div>
        </div>
        <div class="metric-card-premium" style="border-left-color: #0077b6;">
            <div class="metric-val-premium">{media_pontos:.1f} pts</div>
            <div class="metric-lbl-premium">Média Geral</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_rec, _ = st.columns([1.5, 4])
    with col_rec:
        if st.button("🔄 Recarregar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown("<br><h3 style='text-align: center; color: #004b23; font-weight: 700; margin-bottom: 10px;'>🏆 Top 3 Competidores</h3>", unsafe_allow_html=True)
    
    p1_nome, p1_pts = "Aguardando", "0 pts"
    p2_nome, p2_pts = "Aguardando", "0 pts"
    p3_nome, p3_pts = "Aguardando", "0 pts"

    if df_classificacao is not None and num_competidores > 0:
        if num_competidores >= 1:
            p1_nome = str(df_class_sorted.iloc[0][col_nome_ref]).title()
            p1_pts = f"{safe_to_int(df_class_sorted.iloc[0][col_pts_ref])} pts"
        if num_competidores >= 2:
            p2_nome = str(df_class_sorted.iloc[1][col_nome_ref]).title()
            p2_pts = f"{safe_to_int(df_class_sorted.iloc[1][col_pts_ref])} pts"
        if num_competidores >= 3:
            p3_nome = str(df_class_sorted.iloc[2][col_nome_ref]).title()
            p3_pts = f"{safe_to_int(df_class_sorted.iloc[2][col_pts_ref])} pts"

    st.markdown(f"""
    <div class="podium-wrapper">
        <div class="podium-box podium-2">
            <div class="podium-rank-badge badge-p2">2º</div>
            <div class="podium-name">{p2_nome}</div>
            <div class="podium-points">{p2_pts}</div>
        </div>
        <div class="podium-box podium-1">
            <div class="podium-rank-badge badge-p1">1º</div>
            <div class="podium-name" style="font-size: 1.25rem; font-weight: 800;">{p1_nome}</div>
            <div class="podium-points" style="font-size: 2rem; color: #004b23; font-weight: 900;">{p1_pts}</div>
        </div>
        <div class="podium-box podium-3">
            <div class="podium-rank-badge badge-p3">3º</div>
            <div class="podium-name">{p3_nome}</div>
            <div class="podium-points">{p3_pts}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='color: #004b23; font-weight: 700; margin-bottom: 20px;'>Lista Geral de Classificação</h3>", unsafe_allow_html=True)
    
    if df_classificacao is not None and num_competidores > 0:
        df_exibir = df_class_sorted.copy()
        if 'Posição' in df_exibir.columns:
            df_exibir = df_exibir.drop(columns=['Posição'])
            
        posicoes = [f"{x}º" for x in range(1, len(df_exibir) + 1)]
        participantes = df_exibir[col_nome_ref].tolist()
        pontos = [f"{safe_to_int(p)} pts" for p in df_exibir[col_pts_ref].tolist()]
        
        linhas_html = ""
        for i in range(len(posicoes)):
            bg_destaque = "style='background-color: #fffef2; font-weight: bold;'" if i == 0 else ""
            linhas_html += f"<tr {bg_destaque}><td style='font-weight: 700; width: 100px;'>{posicoes[i]}</td><td>{participantes[i]}</td><td style='font-weight: 700; color: #004b23; text-align: right; width: 150px;'>{pontos[i]}</td></tr>"
            
        st.html(f"""
        <div class="table-container">
            <table class="premium-table">
                <thead>
                    <tr><th>Posição</th><th>Competidor</th><th style="text-align: right;">Pontuação</th></tr>
                </thead>
                <tbody>{linhas_html}</tbody>
            </table>
        </div>
        """)
    else:
        st.info("Nenhum participante pontuou ainda. Os pontos serão exibidos assim que os primeiros jogos forem finalizados!")

# --- ABA 1: JOGOS & RESULTADOS ---
with abas_selecionadas[1]:
    st.markdown("<h2 style='color: #004b23; font-weight: 800; margin-bottom: 8px;'>📅 Tabela de Jogos & Resultados</h2>", unsafe_allow_html=True)
    st.write("Acompanhe a classificação cronológica dos jogos, placares cadastrados e limites de bloqueios.")
    
    if df_resultados_sorted.empty:
        st.info("Nenhum jogo localizado.")
    else:
        for idx, row in df_resultados_sorted.iterrows():
            nome_jogo = str(row['Jogo'])
            status_oficial = str(row.get('Status', '🕒 Agendado'))
            horario_col = row.get('Horário', '15:00')
            p_m = row.get('Placar Real Mandante', '')
            p_v = row.get('Placar Real Visitante', '')
            
            team_m = formatar_time_slug(nome_jogo, "mandante")
            team_v = formatar_time_slug(nome_jogo, "visitante")
            dt_jogo = obter_datetime_jogo(nome_jogo, horario_col)
            
            if dt_jogo:
                limite_palpite = dt_jogo - timedelta(hours=1)
                if agora_brasil >= limite_palpite or "encerrado" in status_oficial.lower() or "vivo" in status_oficial.lower() or "andamento" in status_oficial.lower():
                    status_palpites = "🔒 Palpites Encerrados"
                    classe_badge = "badge-closed"
                else:
                    status_palpites = f"🔓 Palpites Abertos (Até às {limite_palpite.strftime('%H:%M')} de {limite_palpite.strftime('%d/%m')})"
                    classe_badge = "badge-open"
                data_exibicao = dt_jogo.strftime("%d/%m às %H:%M")
            else:
                status_palpites = "🕒 Agendado"
                classe_badge = "badge-closed"
                data_exibicao = "A definir"

            st.markdown(f"""
            <div class="match-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-size: 0.85rem; font-weight: bold; color: #555;">📅 {data_exibicao}</span>
                    <span class="{classe_badge}" style="font-size: 0.78rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">{status_palpites}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                    <div style="flex: 1; text-align: right; font-weight: 700; font-size: 1.1rem; color: #333;">{team_m}</div>
                    <div style="padding: 0 15px; font-size: 1.5rem; font-weight: 900; color: #004b23; min-width: 110px; text-align: center; letter-spacing: 2px;">
                        {f"{safe_to_int(p_m)} - {safe_to_int(p_v)}" if pd.notna(p_m) and pd.notna(p_v) and str(p_m).strip() != "" and str(p_v).strip() != "" else "VS"}
                    </div>
                    <div style="flex: 1; text-align: left; font-weight: 700; font-size: 1.1rem; color: #333;">{team_v}</div>
                </div>
                <div style="text-align: center; margin-top: 10px; border-top: 1px solid #f5f5f5; padding-top: 8px;">
                    <span style="font-size: 0.75rem; color: #777; font-weight: 600; text-transform: uppercase;">Estado: {status_oficial}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ABA 2: ENVIAR PALPITE ---
with abas_selecionadas[2]:
    st.markdown("<h2 style='color: #004b23; font-weight: 800; margin-bottom: 20px;'>Enviar Meu Palpite</h2>", unsafe_allow_html=True)
    
    email_user = st.text_input("Seu E-mail Corporativo Feltrim Correa:", value="", placeholder="exemplo@feltrim.com.br")
    nome_user = st.text_input("Seu Nome Completo:", value="")

    jogos_disponiveis = []

    for idx, row in df_resultados_sorted.iterrows():
        status_raw = row.get('Status')
        status_jogo = "🕒 Agendado" if pd.isna(status_raw) or str(status_raw).strip() == "" else str(status_raw)
        nome_jogo = str(row['Jogo'])
        horario_col = row.get('Horário', '15:00')
        dt_jogo = obter_datetime_jogo(nome_jogo, horario_col)
        
        jogo_bloqueado = False
        if dt_jogo:
            limite_palpite = dt_jogo - timedelta(hours=1)
            if agora_brasil >= limite_palpite:
                jogo_bloqueado = True

        if "agendado" in status_jogo.lower() and not jogo_bloqueado:
            jogos_disponiveis.append(nome_jogo)

    if not jogos_disponiveis:
        st.info("Nenhum jogo aberto para palpites no momento! Todos os confrontos de hoje estão trancados.")
    else:
        jogo_selecionado = st.selectbox("Selecione a partida que deseja votar:", jogos_disponiveis)
        
        if jogo_selecionado:
            team_m = formatar_time_slug(jogo_selecionado, "mandante")
            team_v = formatar_time_slug(jogo_selecionado, "visitante")
            
            ja_votou = False
            voto_anterior = ""
            
            if email_user.strip() != "" and df_palpites is not None and not df_palpites.empty:
                email_limpo = email_user.strip().lower()
                col_email_ref = next((c for c in df_palpites.columns if "email" in str(c).lower() or "e-mail" in str(c).lower()), None)
                if col_email_ref and jogo_selecionado in df_palpites.columns:
                    registros_user = df_palpites[df_palpites[col_email_ref].astype(str).str.strip().str.lower() == email_limpo]
                    if not registros_user.empty:
                        v_val = registros_user.iloc[0][jogo_selecionado]
                        if pd.notna(v_val) and str(v_val).strip() != "":
                            ja_votou = True
                            voto_anterior = str(v_val).strip()

            st.markdown(f"### Quem vencerá a partida: **{team_m}** vs **{team_v}**?")
            
            if ja_votou:
                st.warning(f"⚠️ **Palpite já registrado!** Você já enviou seu palpite para este jogo: **'{voto_anterior}'**. Não é permitida a alteração de palpites pós-envio.")
            else:
                voto_opcao = st.radio(
                    "Escolha o seu palpite oficial:",
                    [f"🟢 Vitória do {team_m}", "🤝 Empate", f"🟢 Vitória do {team_v}"],
                    index=0
                )
                
                if st.button("Confirmar e Enviar Palpite 🚀", use_container_width=True):
                    if not email_user or "@" not in email_user:
                        st.error("Por favor, informe um e-mail corporativo válido.")
                    elif len(nome_user) < 3:
                        st.error("Por favor, insira o seu nome completo.")
                    else:
                        palpite_post = ""
                        if "Empate" in voto_opcao:
                            palpite_post = "Empate"
                        elif team_m in voto_opcao:
                            palpite_post = f"Vitoria do {team_m}"
                        else:
                            palpite_post = f"Vitoria do {team_v}"

                        payload = {
                            "action": "fazerPalpite",
                            "email": email_user.strip().lower(),
                            "nome": nome_user.strip(),
                            "id_jogo": jogo_selecionado,
                            "palpite": palpite_post
                        }
                        
                        with st.spinner("Registrando o palpite na planilha..."):
                            try:
                                response = requests.post(URL_APPS_SCRIPT, json=payload, timeout=10)
                                if response.status_code == 200:
                                    res_json = response.json()
                                    if res_json.get("status") == "success":
                                        st.success(f"Excelente, {nome_user}! Palpite para '{jogo_selecionado}' registrado!")
                                        st.cache_data.clear()
                                        st.rerun()
                                    else:
                                        st.error(f"Erro: {res_json.get('message')}")
                                else:
                                    st.error("Erro técnico na comunicação do servidor.")
                            except Exception as e:
                                st.error(f"Erro de conexão: {str(e)}")

# --- ABA 3: MEUS PALPITES ---
with abas_selecionadas[3]:
    st.markdown("<h2 style='color: #004b23; font-weight: 800;'>Meus Palpites Lançados</h2>", unsafe_allow_html=True)
    email_filtro = st.text_input("Digite o seu e-mail corporativo cadastrado:", value="", key="filtro_votos_email")
    
    if email_filtro:
        email_limpo = email_filtro.strip().lower()
        
        if df_palpites is not None and not df_palpites.empty:
            col_email_ref = next((c for c in df_palpites.columns if "email" in str(c).lower() or "e-mail" in str(c).lower()), None)
            
            if col_email_ref:
                registros_usuario = df_palpites[df_palpites[col_email_ref].astype(str).str.strip().str.lower() == email_limpo]
                
                if registros_usuario.empty:
                    st.info(f"Nenhum palpite foi localizado para o e-mail: **{email_limpo}**.")
                else:
                    st.markdown(f"### Palpites de: **{registros_usuario.iloc[0].get('Nome Completo', email_limpo)}**")
                    
                    for col in df_palpites.columns:
                        if "vs" in col or "⚽" in col:
                            voto_valor = registros_usuario.iloc[0][col]
                            if pd.notna(voto_valor) and str(voto_valor).strip() != "":
                                status_oficial = "🕒 Agendado"
                                placar_text = "Resultado: Aguardando Partida"
                                ticket_class = "ticket-pending"
                                badge_class = "badge-pending"
                                badge_lbl = "Aguardando"
                                
                                match_resultado = df_resultados_sorted[df_resultados_sorted['Jogo'] == col]
                                if not match_resultado.empty:
                                    status_oficial = match_resultado.iloc[0].get('Status', '🕒 Agendado')
                                    p_m_real = match_resultado.iloc[0].get('Placar Real Mandante', '')
                                    p_v_real = match_resultado.iloc[0].get('Placar Real Visitante', '')
                                    
                                    # Valida o acerto da aposta
                                    if pd.notna(p_m_real) and pd.notna(p_v_real) and str(p_m_real).strip() != "" and str(p_v_real).strip() != "":
                                        gols_m, gols_v = int(float(p_m_real)), int(float(p_v_real))
                                        placar_text = f"Resultado Real: {gols_m} x {gols_v}"
                                        
                                        vencedor_real = "Empate"
                                        if gols_m > gols_v:
                                            vencedor_real = f"Vitoria do {formatar_time_slug(col, 'mandante')}"
                                        elif gols_v > gols_m:
                                            vencedor_real = f"Vitoria do {formatar_time_slug(col, 'visitante')}"
                                        
                                        voto_norm = str(voto_valor).strip().lower().replace("vitória", "vitoria")
                                        real_norm = vencedor_real.strip().lower().replace("vitória", "vitoria")
                                        
                                        if voto_norm == real_norm:
                                            ticket_class = "ticket-correct"
                                            badge_class = "badge-correct"
                                            badge_lbl = "Acertou! +5 pts"
                                        else:
                                            ticket_class = "ticket-wrong"
                                            badge_class = "badge-wrong"
                                            badge_lbl = "Errou"
                                
                                st.markdown(f"""
                                <div class="ticket-card {ticket_class}">
                                    <div class="ticket-game-title">⚽ {col}</div>
                                    <div class="ticket-info-row">
                                        <div style="font-size: 0.95rem; color: #444;">Seu Palpite: <strong>{voto_valor}</strong></div>
                                        <div style="font-size: 0.9rem; font-weight: 600; color: #555;">{placar_text}</div>
                                        <span class="ticket-badge {badge_class}">{badge_lbl}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
            else:
                st.error("Coluna de e-mail de palpites não localizada.")

# --- ABA 4: PAINEL ADMIN (Protegida por Cofre Digital contra Bugs) ---
with abas_selecionadas[4]:
    st.markdown("<h2 style='color: #004b23; font-weight: 800;'>🔐 Painel de Controle Administrativo</h2>", unsafe_allow_html=True)
    
    # Verifica autenticação na própria aba para não quebrar o ecossistema de abas do Streamlit
    if not st.session_state.get('admin_autenticado', False):
        st.info("Esta área é reservada para coordenadores do bolão. Insira a senha mestra para desbloquear:")
        senha_digitada = st.text_input("Senha de Acesso do Administrador:", type="password", key="senha_admin_tab_direta")
        
        if senha_digitada == "feltrim2026":
            st.session_state['admin_autenticado'] = True
            st.success("🔑 Acesso administrativo concedido com sucesso!")
            st.rerun()
        elif senha_digitada != "":
            st.error("❌ Senha incorreta! Tente novamente.")
    else:
        # Área administrativa desbloqueada
        st.markdown("### 🏆 Cadastro de Resultados Oficiais")
        lista_atualizacao = list(df_resultados_sorted['Jogo'].unique()) if not df_resultados_sorted.empty else []
        
        if not lista_atualizacao:
            st.warning("⚠️ Nenhum jogo carregado na base para atualizar placares.")
        else:
            jogo_escolhido = st.selectbox("Selecione o Jogo para Cadastrar Placar:", lista_atualizacao)
            
            if jogo_escolhido:
                team_m = formatar_time_slug(jogo_escolhido, "mandante")
                team_v = formatar_time_slug(jogo_escolhido, "visitante")
                
                st.markdown(f"#### Partida: **{team_m}** vs **{team_v}**")
                
                placar_m_padrao = ""
                placar_v_padrao = ""
                status_padrao = "🕒 Agendado"
                
                match_row = df_resultados[df_resultados['Jogo'] == jogo_escolhido]
                if not match_row.empty:
                    placar_m_padrao = str(match_row.iloc[0].get('Placar Real Mandante', ''))
                    placar_v_padrao = str(match_row.iloc[0].get('Placar Real Visitante', ''))
                    status_padrao = str(match_row.iloc[0].get('Status', '🕒 Agendado'))
                
                col_pl1, col_pl2 = st.columns(2)
                with col_pl1:
                    novo_placar_m = st.text_input(f"Gols de {team_m}:", value=placar_m_padrao)
                with col_pl2:
                    novo_placar_v = st.text_input(f"Gols de {team_v}:", value=placar_v_padrao)
                    
                novo_status = st.selectbox(
                    "Status Atual do Jogo:",
                    ["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"],
                    index=["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"].index(status_padrao) if status_padrao in ["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"] else 0
                )
                
                if st.button("Salvar Placar Oficial 💾", use_container_width=True):
                    payload_admin = {
                        "action": "atualizarPlacar",
                        "senha": "feltrim2026",
                        "jogo": jogo_escolhido,
                        "placar_m": novo_placar_m,
                        "placar_v": novo_placar_v,
                        "status": novo_status
                    }
                    
                    with st.spinner("Gravando placar..."):
                        try:
                            response = requests.post(URL_APPS_SCRIPT, json=payload_admin, timeout=10)
                            if response.status_code == 200:
                                res_json = response.json()
                                if res_json.get("status") == "success":
                                    st.success("Placar atualizado com sucesso!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {res_json.get('message')}")
                            else:
                                st.error("Erro de conexão com o script.")
                        except Exception as e:
                            st.error(f"Erro técnico: {str(e)}")
                            
        st.write("---")
        st.markdown("### ✨ Inicialização Rápida de Partidas")
        st.write("Deseja restaurar ou popular a lista de 56 jogos originais com dias e horários de São Paulo (GMT-3)?")
        
        if st.button("✨ Inicializar Todos os 56 Jogos na Planilha", use_container_width=True):
            payload_init = {
                "action": "inicializarNovoBolao",
                "senha": "feltrim2026"
            }
            with st.spinner("Gerando dados..."):
                try:
                    response = requests.post(URL_APPS_SCRIPT, json=payload_init, timeout=25)
                    if response.status_code == 200:
                        res_json = response.json()
                        if res_json.get("status") == "success":
                            st.success("Planilha configurada com sucesso!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Erro: {res_json.get('message')}")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

        st.write("---")
        st_id_input = st.text_input("ID da Planilha Google Ativa:", value=sheet_id)
        if st.button("Gravar Alteração de Planilha"):
            st.session_state['spreadsheet_id'] = st_id_input
            st.cache_data.clear()
            st.success("Planilha alterada com sucesso!")
            st.rerun()
            
        if st.button("Sair do Painel Admin 🔒", use_container_width=True):
            st.session_state['admin_autenticado'] = False
            st.rerun()

# Rodapé minimalista
st.markdown("<br><hr><p style='text-align: center; color: #888; font-size: 0.85rem;'>🏆 Feltrim Correa - Todos os direitos reservados. Desenvolvimento de TI Integrado Copa 2026.</p>", unsafe_allow_html=True)

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta
import urllib.parse


st.set_page_config(
    page_title="Feltrim Correa - Bolão Copa 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constantes de Configuração Geral
SPREADSHEET_ID = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"

# Fuso Horário de Brasília (UTC-3)
agora_brasil = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=3)

# 56 Jogos da Copa do Mundo em Ordem Cronológica Real
JOGOS_ESTATICOS = [
    {"ID_Jogo": "JOGO_01", "Jogo": "⚽ Estados Unidos vs Austrália (11/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_02", "Jogo": "⚽ México vs África do Sul (11/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_03", "Jogo": "⚽ Canadá vs Nova Zelândia (12/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_04", "Jogo": "⚽ Uruguai vs Japão (12/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_05", "Jogo": "⚽ Itália vs Camarões (13/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_06", "Jogo": "⚽ Colômbia vs Coreia do Sul (13/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_07", "Jogo": "⚽ Portugal vs Irã (13/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_08", "Jogo": "⚽ Espanha vs Costa Rica (13/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_09", "Jogo": "⚽ Inglaterra vs Tunísia (14/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_10", "Jogo": "⚽ Alemanha vs Equador (14/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_11", "Jogo": "⚽ Croácia vs Jamaica (14/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_12", "Jogo": "⚽ Holanda vs Arábia Saudita (14/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_13", "Jogo": "⚽ Argentina vs Nigéria (15/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_14", "Jogo": "⚽ Bélgica vs Honduras (15/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_15", "Jogo": "⚽ Suécia vs Marrocos (15/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_16", "Jogo": "⚽ Suíça vs Panamá (15/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_17", "Jogo": "⚽ França vs Senegal (16/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_18", "Jogo": "⚽ Chile vs Romênia (16/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_19", "Jogo": "⚽ Ucrânia vs Gana (16/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_20", "Jogo": "⚽ Dinamarca vs Peru (16/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_21", "Jogo": "⚽ Brasil vs Haiti (17/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_22", "Jogo": "⚽ Polônia vs Egito (17/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_23", "Jogo": "⚽ Áustria vs Iraque (17/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_24", "Jogo": "⚽ Noruega vs Catar (17/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_25", "Jogo": "⚽ Estados Unidos vs Jamaica (18/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_26", "Jogo": "⚽ México vs Tunísia (18/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_27", "Jogo": "⚽ Itália vs Coreia do Sul (18/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_28", "Jogo": "⚽ Colômbia vs Camarões (18/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_29", "Jogo": "⚽ Canadá vs Equador (19/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_30", "Jogo": "⚽ Uruguai vs Nigéria (19/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_31", "Jogo": "⚽ Alemanha vs Costa Rica (19/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_32", "Jogo": "⚽ Espanha vs Nova Zelândia (19/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_33", "Jogo": "⚽ Portugal vs Romênia (20/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_34", "Jogo": "⚽ Inglaterra vs Austrália (20/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_35", "Jogo": "⚽ Holanda vs Gana (20/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_36", "Jogo": "⚽ Croácia vs África do Sul (20/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_37", "Jogo": "⚽ Argentina vs Senegal (21/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_38", "Jogo": "⚽ Bélgica vs Panamá (21/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_39", "Jogo": "⚽ Ucrânia vs Arábia Saudita (21/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_40", "Jogo": "⚽ Suíça vs Honduras (21/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_41", "Jogo": "⚽ França vs Nigéria (22/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_42", "Jogo": "⚽ Chile vs Marrocos (22/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_43", "Jogo": "⚽ Dinamarca vs Iraque (22/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_44", "Jogo": "⚽ Suécia vs Romênia (22/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_45", "Jogo": "⚽ Brasil vs Egito (23/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_46", "Jogo": "⚽ Polônia vs Haiti (23/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_47", "Jogo": "⚽ Áustria vs Catar (23/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_48", "Jogo": "⚽ Noruega vs Romênia (23/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_49", "Jogo": "⚽ Estados Unidos vs Camarões (24/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_50", "Jogo": "⚽ México vs Equador (24/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_51", "Jogo": "⚽ Canadá vs Costa Rica (24/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_52", "Jogo": "⚽ Uruguai vs Coreia do Sul (24/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_53", "Jogo": "⚽ Itália vs Nigéria (25/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_54", "Jogo": "⚽ Colômbia vs Marrocos (25/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_55", "Jogo": "⚽ Portugal vs Senegal (25/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_56", "Jogo": "⚽ Espanha vs Haiti (25/06)", "Horário": "21:30"}
]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Cabeçalho Premium */
    .header-container {
        background: linear-gradient(135deg, #004b23 0%, #007200 100%);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0, 75, 35, 0.2);
        border: 2px solid #d4af37;
    }
    
    .header-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .header-subtitle {
        font-size: 1rem;
        margin-top: 10px;
        color: #f1f1f1;
        font-weight: 300;
    }
    
    /* Fuso Horário */
    .timezone-bar {
        background-color: #f8f9fa;
        border-left: 5px solid #004b23;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
        color: #333;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    /* Destacar Especialmente a Guia de Palpite */
    button[data-baseweb="tab"]:nth-child(3) {
        background: linear-gradient(135deg, #004b23 0%, #007200 100%) !important;
        color: white !important;
        border: 1.8px solid #d4af37 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 10px rgba(0, 114, 0, 0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    button[data-baseweb="tab"]:nth-child(3):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4) !important;
    }

    /* Botões Pill-Shape Premium */
    .stButton > button {
        background: linear-gradient(135deg, #004b23 0%, #007200 100%) !important;
        color: white !important;
        border: 1.5px solid #d4af37 !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        padding: 8px 24px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(212, 175, 55, 0.3) !important;
        border-color: #ffffff !important;
    }

    /* Cards de Jogos */
    .game-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e1e8e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .game-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0, 75, 35, 0.08);
        border-color: #d4af37;
    }

    /* Badges de Status do Jogo */
    .badge-status {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-agendado { background-color: #e9ecef; color: #495057; }
    .badge-andamento { background-color: #fff3cd; color: #856404; animation: blinker 1.5s infinite; }
    .badge-encerrado { background-color: #d4edda; color: #155724; }

    @keyframes blinker {
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">🏆 Bolão Corporativo Feltrim Correa</div>
    <div class="header-subtitle">Consulte a classificação oficial, envie seus palpites e acompanhe os placares em tempo real!</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="timezone-bar">
    <span>🕒</span>
    <span><b>HORA OFICIAL DE BRASÍLIA (UTC-3):</b> {agora_brasil.strftime('%d/%m/%Y %H:%M:%S')}</span>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=15)
def puxar_planilha_segura(sheet_name):
    """
    Carrega o CSV de uma aba específica da planilha Google com tratamento de erros robusto.
    """
    try:
        sheet_encoded = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_encoded}"
        df = pd.read_csv(url)
        df = df.dropna(how='all', axis=1)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

# Carregamento seguro de dados
df_resultados_raw = puxar_planilha_segura("Resultados Oficiais")
df_palpites_raw = puxar_planilha_segura("Palpites")

# Configuração de Fallback se a planilha estiver inacessível ou vazia
if df_resultados_raw.empty or 'Jogo' not in df_resultados_raw.columns:
    df_resultados = pd.DataFrame(JOGOS_ESTATICOS)
    df_resultados['Placar Real Mandante'] = ""
    df_resultados['Placar Real Visitante'] = ""
    df_resultados['Status'] = "🕒 Agendado"
    planilha_precisa_inicializar = True
else:
    df_resultados = df_resultados_raw.copy()
    planilha_precisa_inicializar = False

def obter_datetime_jogo(jogo_nome, horario_str):
    """
    Analisa a data e o horário e retorna um datetime naive para evitar erros de comparação de fuso.
    """
    try:
        if "(" in jogo_nome and "/" in jogo_nome:
            parte_data = jogo_nome.split("(")[-1].split(")")[0]
            dia, mes = map(int, parte_data.split("/"))
            horario_str = str(horario_str).strip()
            if ":" in horario_str:
                hora, minuto = map(int, horario_str.split(":"))
            else:
                hora, minuto = 15, 0
            return datetime(2026, mes, dia, hora, minuto)
    except Exception:
        pass
    return datetime(2026, 6, 25, 23, 59)

# Ordenação Cronológica de Jogos
df_resultados['Data_Ordenacao'] = df_resultados.apply(
    lambda r: obter_datetime_jogo(r['Jogo'], r['Horário']), axis=1
)
df_resultados_sorted = df_resultados.sort_values(by='Data_Ordenacao').copy()

def calcular_pontos_palpite(palpite, placar_m, placar_v):
    """
    Cálculo de pontos oficial:
    10 pontos: Acerto exato do placar.
    5 pontos: Acerto do vencedor/empate com placar errado.
    0 pontos: Palpite errado.
    """
    try:
        if pd.isna(placar_m) or pd.isna(placar_v) or str(placar_m).strip() == "" or str(placar_v).strip() == "":
            return None
        
        real_m = int(float(placar_m))
        real_v = int(float(placar_v))
        
        palpite_limpo = str(palpite).lower().replace(" ", "").replace("-", "x")
        if "x" not in palpite_limpo:
            return 0
            
        partes = palpite_limpo.split("x")
        palp_m = int(float(partes[0]))
        palp_v = int(float(partes[1]))
        
        if palp_m == real_m and palp_v == real_v:
            return 10
            
        status_real = 1 if real_m > real_v else (-1 if real_m < real_v else 0)
        status_palpite = 1 if palp_m > palp_v else (-1 if palp_m < palp_v else 0)
        
        if status_real == status_palpite:
            return 5
            
        return 0
    except Exception:
        return 0

tabela_ranking = {}

if not df_palpites_raw.empty and len(df_palpites_raw.columns) > 3:
    col_email = ""
    col_nome = ""
    for col in df_palpites_raw.columns:
        if "email" in col.lower() or "e-mail" in col.lower() or "usuário" in col.lower():
            col_email = col
        if "nome" in col.lower():
            col_nome = col
            
    if col_email and col_nome:
        for idx, row in df_palpites_raw.iterrows():
            email = str(row[col_email]).strip().lower()
            nome = str(row[col_nome]).strip()
            
            if not email or "@" not in email:
                continue
                
            if email not in tabela_ranking:
                tabela_ranking[email] = {"Nome": nome, "Pontos": 0, "Acertos_Exatos": 0, "Acertos_Simples": 0, "Palpites_Feitos": 0}
                
            for j_idx, j_row in df_resultados_sorted.iterrows():
                jogo_nome = j_row['Jogo']
                if jogo_nome in df_palpites_raw.columns:
                    palpite_usuario = row[jogo_nome]
                    if pd.notna(palpite_usuario) and str(palpite_usuario).strip() != "":
                        pts = calcular_pontos_palpite(
                            palpite_usuario, 
                            j_row['Placar Real Mandante'], 
                            j_row['Placar Real Visitante']
                        )
                        if pts is not None:
                            tabela_ranking[email]["Pontos"] += pts
                            tabela_ranking[email]["Palpites_Feitos"] += 1
                            if pts == 10:
                                tabela_ranking[email]["Acertos_Exatos"] += 1
                            elif pts == 5:
                                tabela_ranking[email]["Acertos_Simples"] += 1

df_ranking = pd.DataFrame.from_dict(tabela_ranking, orient='index')
if not df_ranking.empty:
    df_ranking = df_ranking.sort_values(by=["Pontos", "Acertos_Exatos", "Nome"], ascending=[False, False, True])
    df_ranking.reset_index(drop=True, inplace=True)
    if 'Posição' not in df_ranking.columns:
        df_ranking.insert(0, 'Posição', range(1, len(df_ranking) + 1))
else:
    df_ranking = pd.DataFrame(columns=['Posição', 'Nome', 'Pontos', 'Acertos_Exatos', 'Palpites_Feitos'])

# Estrutura de Abas do Aplicativo
tabs = st.tabs([
    "🏆 Classificação Geral", 
    "📅 Jogos & Resultados", 
    "📝 Dar Palpite", 
    "🎟️ Meus Palpites", 
    "🔑 Portal Admin"
])

# ==================== ABA 1: CLASSIFICAÇÃO GERAL ====================
with tabs[0]:
    st.markdown("### 🏆 Placar de Líderes")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-left: 5px solid #004b23; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.04);">
            <div style="font-size: 0.9rem; color: #666; text-transform: uppercase;">Participantes</div>
            <div style="font-size: 2rem; font-weight: 700; color: #004b23; margin-top: 5px;">{len(df_ranking)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        top_name = df_ranking.iloc[0]['Nome'] if not df_ranking.empty else "Nenhum"
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-left: 5px solid #d4af37; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.04);">
            <div style="font-size: 0.9rem; color: #666; text-transform: uppercase;">Líder Atual 👑</div>
            <div style="font-size: 1.4rem; font-weight: 700; color: #b8860b; margin-top: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{top_name}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        media_pts = round(df_ranking['Pontos'].mean(), 1) if not df_ranking.empty else 0.0
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-left: 5px solid #007200; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.04);">
            <div style="font-size: 0.9rem; color: #666; text-transform: uppercase;">Média de Pontuação</div>
            <div style="font-size: 2rem; font-weight: 700; color: #007200; margin-top: 5px;">{media_pts} pts</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Exibir pódio com medalhas circulares elegantes
    if not df_ranking.empty:
        st.markdown("#### 🥇 Top 3 Competidores")
        cols_podio = st.columns(3)
        
        # 1º Lugar
        with cols_podio[0]:
            if len(df_ranking) >= 1:
                p1 = df_ranking.iloc[0]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fffaf0 0%, #fff0d4 100%); border: 2px solid #d4af37; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 6px 15px rgba(212,175,55,0.15);">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">🥇</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: #856404;">{p1['Nome']}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #004b23; margin-top: 5px;">{p1['Pontos']} pts</div>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">{p1['Acertos_Exatos']} placares exatos</div>
                </div>
                """, unsafe_allow_html=True)
        # 2º Lugar
        with cols_podio[1]:
            if len(df_ranking) >= 2:
                p2 = df_ranking.iloc[1]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 1.5px solid #adb5bd; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">🥈</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #495057;">{p2['Nome']}</div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: #004b23; margin-top: 5px;">{p2['Pontos']} pts</div>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">{p2['Acertos_Exatos']} placares exatos</div>
                </div>
                """, unsafe_allow_html=True)
        # 3º Lugar
        with cols_podio[2]:
            if len(df_ranking) >= 3:
                p3 = df_ranking.iloc[2]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fdf6f0 0%, #f5e6d3 100%); border: 1.5px solid #cd7f32; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">🥉</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #8a4f1c;">{p3['Nome']}</div>
                    <div style="font-size: 1.4rem; font-weight: 700; color: #004b23; margin-top: 5px;">{p3['Pontos']} pts</div>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">{p3['Acertos_Exatos']} placares exatos</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("#### 📋 Classificação Completa")
        
        tabela_html = "<div style='overflow-x: auto; margin-top: 15px;'><table style='width:100%; border-collapse: collapse; border-radius: 10px; overflow: hidden; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.03);'>"
        tabela_html += "<thead style='background-color: #004b23; color: white; text-align: left;'><tr><th style='padding: 12px; font-weight: 600;'>Posição</th><th style='padding: 12px; font-weight: 600;'>Competidor</th><th style='padding: 12px; font-weight: 600;'>Pontos</th><th style='padding: 12px; font-weight: 600; text-align: center;'>Acertos Exatos</th></tr></thead><tbody>"
        
        for idx, row in df_ranking.iterrows():
            bg_cor = "#ffffff" if idx % 2 == 0 else "#f8f9fa"
            if idx == 0:
                bg_cor = "#fffbeb"
            tabela_html += f"<tr style='background-color: {bg_cor}; border-bottom: 1px solid #eef2ee;'>"
            tabela_html += f"<td style='padding: 12px; font-weight: 700; color: #004b23;'>{row['Posição']}º</td>"
            tabela_html += f"<td style='padding: 12px; font-weight: 500; color: #333;'>{row['Nome']}</td>"
            tabela_html += f"<td style='padding: 12px; font-weight: 700; color: #007200;'>{row['Pontos']} pts</td>"
            tabela_html += f"<td style='padding: 12px; text-align: center;'>🎯 {row['Acertos_Exatos']}</td>"
            tabela_html += "</tr>"
            
        tabela_html += "</tbody></table></div>"
        st.html(tabela_html)
    else:
        st.info("💡 Nenhum palpite registrado na classificação ainda.")
        
    st.write("")
    if st.button("🔄 Recarregar Dados", key="btn_reload"):
        st.cache_data.clear()
        st.rerun()

# ==================== ABA 2: JOGOS & RESULTADOS ====================
with tabs[1]:
    st.markdown("### 📅 Agenda de Jogos e Resultados")
    
    for idx, row in df_resultados_sorted.iterrows():
        id_jogo = row['ID_Jogo']
        jogo = row['Jogo']
        horario = row['Horário']
        status = row['Status']
        real_m = row['Placar Real Mandante']
        real_v = row['Placar Real Visitante']
        
        data_jogo = obter_datetime_jogo(jogo, horario)
        limite_palpite = data_jogo - timedelta(hours=1)
        palpites_abertos = agora_brasil < limite_palpite
        
        if "encerrado" in str(status).lower():
            status_badge = '<span class="badge-status badge-encerrado">🟢 Finalizado</span>'
            placar_exibicao = f"<span style='font-size: 1.6rem; font-weight: 700; color: #004b23;'>{int(float(real_m))} - {int(float(real_v))}</span>"
        elif "andamento" in str(status).lower() or "vivo" in str(status).lower():
            status_badge = '<span class="badge-status badge-andamento">🟡 Ao Vivo</span>'
            placar_exibicao = f"<span style='font-size: 1.6rem; font-weight: 700; color: #b8860b;'>{int(float(real_m))} - {int(float(real_v))}</span>"
        else:
            status_badge = '<span class="badge-status badge-agendado">🕒 Agendado</span>'
            placar_exibicao = "<span style='font-size: 1.1rem; color: #666; font-style: italic;'>vs</span>"
            
        aberto_badge = '<span style="background-color: #d1e7dd; color: #0f5132; font-size: 0.75rem; font-weight: bold; padding: 4px 10px; border-radius: 50px; margin-left: 10px;">📝 Palpites Livres</span>' if palpites_abertos else '<span style="background-color: #f8d7da; color: #842029; font-size: 0.75rem; font-weight: bold; padding: 4px 10px; border-radius: 50px; margin-left: 10px;">🔒 Palpites Trancados</span>'

        st.markdown(f"""
        <div class="game-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    {status_badge}
                    {aberto_badge}
                    <div style="font-size: 0.8rem; color: #888; margin-top: 5px;">📅 Partida: <b>{data_jogo.strftime('%d/%m')} às {horario}</b> (Horário de Brasília)</div>
                    <div style="font-size: 0.8rem; color: #888;">⏱️ Limite para apostas: {limite_palpite.strftime('%d/%m às %H:%M')}</div>
                </div>
                <div style="text-align: center; margin-top: 10px; min-width: 150px; background: #fafafa; padding: 10px; border-radius: 8px; border: 1px solid #eee;">
                    <div style="font-size: 0.95rem; font-weight: 600; color: #333; margin-bottom: 5px;">{jogo}</div>
                    <div>{placar_exibicao}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== ABA 3: DAR PALPITE ====================
with tabs[2]:
    st.markdown("### 📝 Registrar seu Palpite")
    
    if planilha_precisa_inicializar:
        st.error("⚠️ Para conseguir enviar novos palpites, a planilha precisa primeiro ser inicializada no Portal Administrativo.")
    else:
        st.write("Digite o seu e-mail corporativo cadastrado para filtrar e selecionar as partidas disponíveis.")
        
        user_email = st.text_input("📧 E-mail Corporativo do Colaborador:", key="user_email_input").strip().lower()
        user_nome = st.text_input("👤 Nome Completo:", key="user_nome_input").strip()
        
        if user_email and "@" in user_email and len(user_nome) >= 3:
            # Identificar e carregar palpites já efetuados por este e-mail
            col_email = ""
            palpites_feitos_usuario = []
            for c in df_palpites_raw.columns:
                if "email" in c.lower() or "e-mail" in c.lower() or "usuário" in c.lower():
                    col_email = c
                    break
            
            if col_email and not df_palpites_raw.empty:
                usuario_existente = df_palpites_raw[df_palpites_raw[col_email].astype(str).str.strip().str.lower() == user_email]
                if not usuario_existente.empty:
                    linha_user = usuario_existente.iloc[0]
                    for col in df_palpites_raw.columns:
                        if col not in ["Carimbo de data/hora", "E-mail do Usuário", "Nome Completo", "email", "e-mail", col_email]:
                            voto_realizado = str(linha_user[col]).strip()
                            if voto_realizado and voto_realizado != "nan" and voto_realizado != "":
                                palpites_feitos_usuario.append(col)

            # Filtrar e remover jogos que o colaborador já palpitou ou que estão fechados/trancados
            jogos_disponiveis = []
            for j_idx, j_row in df_resultados_sorted.iterrows():
                jogo_nome = j_row['Jogo']
                limite = j_row['Data_Ordenacao'] - timedelta(hours=1)
                
                # Regra: antes do tempo limite, não encerrado E ainda não palpitado
                if agora_brasil < limite and "encerrado" not in str(j_row['Status']).lower():
                    if jogo_nome not in palpites_feitos_usuario:
                        jogos_disponiveis.append(jogo_nome)
            
            if len(jogos_disponiveis) == 0:
                st.success("🎉 Você já deu palpite em todos os jogos cronologicamente disponíveis no momento!")
            else:
                with st.form("form_palpite_novo"):
                    jogo_selecionado = st.selectbox("⚽ Selecione o Jogo que deseja apostar:", jogos_disponiveis)
                    
                    st.markdown(f"##### 🎯 Palpite de Placar para {jogo_selecionado}")
                    col_m, col_v = st.columns(2)
                    with col_m:
                        gols_m = st.number_input("Gols do Mandante (Equipe 1):", min_value=0, max_value=25, value=0, step=1)
                    with col_v:
                        gols_v = st.number_input("Gols do Visitante (Equipe 2):", min_value=0, max_value=25, value=0, step=1)
                        
                    st.write("")
                    btn_envio = st.form_submit_button("Confirmar e Registrar Palpite")
                    
                    if btn_envio:
                        palpite_texto = f"{gols_m} x {gols_v}"
                        dados_envio = {
                            "action": "fazerPalpite",
                            "email": user_email,
                            "nome": user_nome,
                            "id_jogo": jogo_selecionado,
                            "palpite": palpite_texto
                        }
                        
                        try:
                            resposta = requests.post(WEB_APP_URL, json=dados_envio, timeout=35)
                            try:
                                res_json = resposta.json()
                                if res_json.get("status") == "success":
                                    st.success(f"🎉 Palpite registrado com sucesso para o jogo: {jogo_selecionado}!")
                                    st.balloons()
                                    st.cache_data.clear()
                                else:
                                    st.error(f"Erro ao registrar: {res_json.get('message')}")
                            except ValueError:
                                st.error("⚠️ Erro de Resposta: O Google Apps Script não pôde processar o envio. Verifique as configurações de acesso.")
                                with st.expander("🔍 Ver detalhes técnicos"):
                                    st.code(resposta.text[:1000], language="html")
                        except Exception as e:
                            st.error(f"Falha de conexão com a API do Google Sheets. Detalhes: {e}")
        else:
            st.info("💡 Digite o seu e-mail corporativo completo e seu nome para listar os palpites em aberto.")

# ==================== ABA 4: MEUS PALPITES ====================
with tabs[3]:
    st.markdown("### 🎟️ Meus Tickets de Apostas")
    st.write("Digite o seu e-mail corporativo cadastrado para visualizar todo o seu histórico de palpites.")
    
    email_busca = st.text_input("📧 Pesquisar Histórico pelo seu E-mail:", "", key="email_busca_input").strip().lower()
    
    if email_busca:
        if df_palpites_raw.empty:
            st.info("Nenhum palpite registrado no banco de dados ainda.")
        else:
            col_email = ""
            for c in df_palpites_raw.columns:
                if "email" in c.lower() or "e-mail" in c.lower() or "usuário" in c.lower():
                    col_email = c
                    break
                    
            if col_email:
                usuario_palpites = df_palpites_raw[df_palpites_raw[col_email].astype(str).str.strip().str.lower() == email_busca]
                
                if usuario_palpites.empty:
                    st.warning("Nenhum registro de palpites foi localizado para este e-mail.")
                else:
                    linha_user = usuario_palpites.iloc[0]
                    st.success(f"👤 Histórico localizado para o colaborador: **{linha_user.get('Nome Completo', 'Sem nome')}**")
                    
                    algum_palpite = False
                    for j_idx, j_row in df_resultados_sorted.iterrows():
                        jogo_c = j_row['Jogo']
                        if jogo_c in df_palpites_raw.columns:
                            voto_cadastrado = str(linha_user[jogo_c]).strip()
                            if voto_cadastrado and voto_cadastrado != "nan" and voto_cadastrado != "":
                                algum_palpite = True
                                pts_obtidos = calcular_pontos_palpite(
                                    voto_cadastrado, 
                                    j_row['Placar Real Mandante'], 
                                    j_row['Placar Real Visitante']
                                )
                                
                                if pts_obtidos == 10:
                                    cor_feedback = "border-left: 6px solid #198754; background: #eafbf1;"
                                    msg_pts = f"🎯 <b>10 Pontos obtidos</b> (Acertou o Placar Exato!)"
                                elif pts_obtidos == 5:
                                    cor_feedback = "border-left: 6px solid #ffc107; background: #fffdf5;"
                                    msg_pts = f"⚽ <b>5 Pontos obtidos</b> (Acertou o Vencedor/Empate)"
                                elif pts_obtidos == 0:
                                    cor_feedback = "border-left: 6px solid #dc3545; background: #fff5f5;"
                                    msg_pts = f"❌ <b>0 Pontos</b> (Errou o resultado oficial)"
                                else:
                                    cor_feedback = "border-left: 6px solid #6c757d; background: #fdfdfd;"
                                    msg_pts = "🕒 <i>Jogo ainda não realizado. Aguardando resultado oficial...</i>"
                                    
                                placar_real_str = f"({int(float(j_row['Placar Real Mandante']))}x{int(float(j_row['Placar Real Visitante']))})" if pts_obtidos is not None else ""
                                
                                st.markdown(f"""
                                <div style="border-radius: 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); {cor_feedback}">
                                    <div style="font-weight: 700; color: #333; font-size: 0.95rem;">{jogo_c}</div>
                                    <div style="font-size: 0.85rem; color: #555; margin-top: 4px;">Seu palpite: <b>{voto_cadastrado}</b> {placar_real_str}</div>
                                    <div style="font-size: 0.85rem; color: #444; margin-top: 4px;">{msg_pts}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    if not algum_palpite:
                        st.info("Nenhum palpite preenchido até o momento por este usuário.")

# ==================== ABA 5: PORTAL ADMIN ====================
with tabs[4]:
    st.markdown("### 🔑 Controle de Acesso Administrativo")
    st.write("Digite a sua credencial administrativa do bolão para desbloquear as opções de controle e configuração:")
    
    admin_pass = st.text_input("🔑 Senha de Administrador:", type="password", key="senha_admin_field").strip()
    
    if admin_pass == "feltrim2026":
        st.success("✅ Acesso administrativo liberado!")
        st.divider()
        
        # Gerenciamento de inicialização em massa (Batch Optimization)
        st.markdown("#### ✨ Inicialização em Lote de Partidas")
        st.write("Use o botão abaixo para criar todas as abas e os 56 confrontos na sua planilha do Google Sheets de uma só vez (otimizado para evitar lentidões):")
        
        if st.button("🚀 Inicializar Todos os 56 Jogos na Planilha", key="btn_init_planilha"):
            with st.spinner("Conectando ao banco de dados e enviando jogos em lote..."):
                try:
                    res_init = requests.post(
                        WEB_APP_URL, 
                        json={"action": "inicializarNovoBolao", "senha": "feltrim2026"}, 
                        timeout=35
                    )
                    try:
                        r_json = res_init.json()
                        if r_json.get("status") == "success":
                            st.success("🎉 Todas as tabelas e os 56 jogos foram criados com gravação em massa super-rápida!")
                            st.cache_data.clear()
                        else:
                            st.error(f"Erro na criação: {r_json.get('message')}")
                    except ValueError:
                        st.error("⚠️ O Google Apps Script não pôde inicializar. Verifique o link de implantação.")
                        with st.expander("🔍 Detalhes técnicos"):
                            st.code(res_init.text[:1000], language="html")
                except Exception as ex:
                    st.error(f"Erro ao se conectar ao Google Apps Script: {ex}")
                    
        st.divider()
        
        # Cadastro de Resultados Oficiais
        st.markdown("#### 🏆 Cadastro de Resultados Oficiais")
        st.write("Insira e atualize o placar oficial real de cada partida:")
        
        with st.form("form_resultado_oficial"):
            jogo_placar_sel = st.selectbox("Selecione a partida que deseja lançar placar:", df_resultados_sorted['Jogo'].unique())
            
            col_rm, col_rv = st.columns(2)
            with col_rm:
                placar_real_m = st.number_input("Placar Real Mandante:", min_value=0, max_value=25, value=0, step=1)
            with col_rv:
                placar_real_v = st.number_input("Placar Real Visitante:", min_value=0, max_value=25, value=0, step=1)
                
            status_oficial = st.selectbox("Status Oficial da Partida:", ["🟢 Encerrado", "🟡 Em Andamento", "🕒 Agendado"])
            
            btn_oficial = st.form_submit_button("Salvar Resultado Oficial")
            
            if btn_oficial:
                payload_oficial = {
                    "action": "atualizarPlacar",
                    "senha": "feltrim2026",
                    "jogo": jogo_placar_sel,
                    "placar_m": int(placar_real_m),
                    "placar_v": int(placar_real_v),
                    "status": status_oficial
                }
                
                with st.spinner("Salvando placar e recalculando notas..."):
                    try:
                        res_p = requests.post(WEB_APP_URL, json=payload_oficial, timeout=35)
                        try:
                            p_json = res_p.json()
                            if p_json.get("status") == "success":
                                st.success(f"🎉 Placar de '{jogo_placar_sel}' atualizado com sucesso!")
                                st.cache_data.clear()
                            else:
                                st.error(f"Erro: {p_json.get('message')}")
                        except ValueError:
                            st.error("⚠️ Erro de Resposta: O placar não pôde ser salvo.")
                    except Exception as ex:
                        st.error(f"Falha de comunicação: {ex}")
    else:
        if admin_pass != "":
            st.error("🔑 Senha incorreta. Acesso negado.")
        else:
            st.info("Painel restrito. Digite a senha administrativa para obter acesso.")

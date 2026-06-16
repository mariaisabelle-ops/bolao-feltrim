import streamlit as st
import pandas as pd
import urllib.parse
import requests
import json
import re
import textwrap
import unicodedata

# =========================================================================
# ⚙️ CONFIGURAÇÃO DE INTEGRAÇÃO DEFINITIVA (APPS SCRIPT ATUALIZADO)
# =========================================================================
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"
# =========================================================================

st.set_page_config(
    page_title="Bolão Feltrim Correa - Copa 2026",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS institucional (Verde, Amarelo e Azul-Marinho) totalmente integrada
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', Arial, sans-serif; }
    .main { background-color: #f4f7f5; }
    
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

    /* Abas personalizadas */
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
        color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(0, 75, 35, 0.25);
    }

    .custom-error-box {
        background-color: #fdf2f2;
        border-left: 4px solid #ef4444;
        color: #9b1c1c;
        padding: 18px;
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

    /* Cards e Métricas */
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

    /* Pódio de Classificação */
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
    }
    
    .podium-1 {
        order: 2;
        border-top: 5px solid #ffbd00;
        background: linear-gradient(180deg, #fffdf0 0%, #ffffff 100%);
        min-height: 160px;
    }
    
    .podium-2 {
        order: 1;
        border-top: 5px solid #003566;
        background: linear-gradient(180deg, #f0f4f8 0%, #ffffff 100%);
        min-height: 135px;
    }
    
    .podium-3 {
        order: 3;
        border-top: 5px solid #004b23;
        background: linear-gradient(180deg, #f4faf6 0%, #ffffff 100%);
        min-height: 120px;
    }
    
    .podium-badge { font-size: 1.8rem; margin-bottom: 5px; }
    
    .podium-name {
        font-weight: 700;
        font-size: 0.9rem;
        color: #1e293b;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .podium-pts {
        font-weight: 800;
        color: #004b23;
        font-size: 1.1rem;
        margin-top: 4px;
    }

    /* Lista de Classificação */
    .ranking-list { display: flex; flex-direction: column; gap: 8px; }
    
    .ranking-item {
        background-color: white;
        padding: 12px 16px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0, 75, 35, 0.02);
        border: 1px solid #e8efe9;
    }
    
    .ranking-left { display: flex; align-items: center; gap: 12px; }
    .ranking-pos { font-size: 0.85rem; font-weight: 800; color: #003566; width: 24px; }
    
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
    
    .ranking-name { font-weight: 600; color: #334155; font-size: 0.95rem; }
    .ranking-score { font-weight: 800; color: #004b23; font-size: 1.05rem; }

    /* Enquetes de Palpites */
    .poll-card {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 16px;
        border: 1px solid #e8efe9;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.03);
    }
    
    .poll-header {
        text-align: center;
        font-weight: 700;
        color: #003566;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 14px;
    }
    
    .poll-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .poll-team-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 40%;
        text-align: center;
    }
    
    .poll-team-name { font-weight: 700; color: #1e293b; font-size: 0.95rem; line-height: 1.2; }
    
    .poll-vs {
        font-weight: 800;
        font-size: 0.95rem;
        color: #004b23;
        background-color: #e8efe9;
        padding: 4px 10px;
        border-radius: 20px;
    }

    /* Barras de Progresso Limpas (Sem Código Streamlit Aparente) */
    .poll-bar-container { margin-bottom: 8px; }
    
    .poll-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 3px;
    }
    
    .poll-bar-outer { background-color: #f1f5f9; border-radius: 8px; height: 10px; overflow: hidden; position: relative; }
    .poll-bar-inner { height: 100%; border-radius: 8px; transition: width 0.6s ease; }
    
    .bar-color-m { background-color: #004b23; }
    .bar-color-draw { background-color: #ffbd00; }
    .bar-color-v { background-color: #003566; }

    /* Botões de Ação Personalizados */
    div.stButton > button {
        background-color: #004b23 !important;
        color: #ffffff !important;
        border: 2px solid #ffbd00 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        transition: all 0.25s ease !important;
        padding: 8px 16px !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #ffbd00 !important;
        color: #004b23 !important;
        box-shadow: 0 4px 12px rgba(255, 189, 0, 0.35) !important;
    }
    </style>
""", unsafe_allow_html=True)

def remover_acentos(texto):
    if not texto: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn').lower()

def safe_to_int(val):
    if pd.isna(val):
        return 0
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0

def formatar_nome_time(nome_time):
    if not nome_time or pd.isna(nome_time): return ""
    nome_limpo = str(nome_time).strip()
    nome_limpo = re.sub(r'\(.*?\)', '', nome_limpo)
    nome_limpo = re.sub(r'[^\w\s\-\.]', '', nome_limpo)
    return nome_limpo.strip()

def extrair_data_jogo(col_name):
    match = re.search(r'\((\d{2})/(\d{2})\)', str(col_name))
    if match: return int(match.group(1)), int(match.group(2))
    return 31, 12

def chave_ordenacao_jogo(col_name):
    dia, mes = extrair_data_jogo(col_name)
    return (mes, dia)

# ID padrão da nova planilha limpa
if "sheet_id" not in st.session_state:
    st.session_state["sheet_id"] = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"

@st.cache_data(ttl=2)
def carregar_dados_seguro(sheet_id):
    df_resp = None
    df_res = None
    df_class = None
    is_private = False
    
    # 1. Carrega Palpites
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet=Palpites"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            if response.text.strip().startswith("<html") or "<!DOCTYPE" in response.text:
                is_private = True
            else:
                df_resp = pd.read_csv(url)
    except Exception:
        pass

    # 2. Carrega Resultados
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet=Resultados"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and not (response.text.strip().startswith("<html") or "<!DOCTYPE" in response.text):
            df_res = pd.read_csv(url)
    except Exception:
        pass

    # 3. Carrega Classificacao
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet=Classificacao"
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and not (response.text.strip().startswith("<html") or "<!DOCTYPE" in response.text):
            df_class = pd.read_csv(url)
    except Exception:
        pass

    return df_resp, df_res, df_class, is_private

df_respostas, df_resultados, df_classificacao, is_private = carregar_dados_seguro(st.session_state["sheet_id"])

# Mensagem se a planilha for privada
if is_private:
    st.markdown(textwrap.dedent("""
        <div class="custom-error-box">
            <h4 style="margin:0 0 8px 0; font-weight:700;">🔒 Planilha Privada ou ID Incorreto</h4>
            <p style="margin:0;">Mude o compartilhamento da planilha para <strong>"Qualquer pessoa com o link pode ler"</strong> ou altere o ID no Painel Admin abaixo!</p>
        </div>
    """), unsafe_allow_html=True)

lista_jogos_formulario = []
col_email = "E-mail Corporativo"
col_nome = "Nome Completo"

if df_respostas is not None and not df_respostas.empty:
    df_respostas.columns = df_respostas.columns.str.strip()
    col_email_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['email', 'e-mail'])]
    if col_email_list: col_email = col_email_list[0]
    col_nome_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['nome', 'completo'])]
    if col_nome_list: col_nome = col_nome_list[0]
    
    for col in df_respostas.columns:
        if "vs" in col.lower() or "⚽" in col:
            lista_jogos_formulario.append(col.strip())
            
lista_jogos_formulario.sort(key=chave_ordenacao_jogo)

# Abas principais do app
tab_ranking, tab_enviar, tab_palpites, tab_jogos = st.tabs([
    "📊 Classificação", "📝 Dar Palpite", "🎯 Ver Palpites", "⚽ Resultados Reais"
])

with tab_ranking:
    st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 5px; text-align: center;'>Classificação Geral</h3>", unsafe_allow_html=True)
    
    col_vazia, col_btn_sync = st.columns([4, 1])
    with col_btn_sync:
        if st.button("🔄 Recarregar", key="sync_ranking"):
            st.cache_data.clear()
            st.rerun()

    if df_classificacao is not None and not df_classificacao.empty:
        df_classificacao.columns = df_classificacao.columns.str.strip()
        ranking = df_classificacao.reset_index(drop=True)
        
        col_part_ref = "Participante"
        for c in ranking.columns:
            if any(x in str(c).lower() for x in ["participante", "nome", "competidor"]):
                col_part_ref = c
                break
                
        col_pts_ref = "Pontos Acumulados"
        for c in ranking.columns:
            if any(x in str(c).lower() for x in ["pontos", "ponto", "acumulado", "score"]):
                col_pts_ref = c
                break
        
        total_participantes = len(ranking)
        lider_atual = str(ranking.iloc[0][col_part_ref]).title() if total_participantes > 0 and col_part_ref in ranking.columns else "-"
        
        try:
            media_pontos = int(ranking[col_pts_ref].dropna().mean()) if total_participantes > 0 and col_pts_ref in ranking.columns else 0
        except Exception:
            media_pontos = 0
        
        st.markdown(textwrap.dedent(f"""
            <div class="metrics-container">
                <div class="metric-box">
                    <div class="metric-value">{total_participantes}</div>
                    <div class="metric-label">Competidores</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">🏆 {lider_atual.split()[0]}</div>
                    <div class="metric-label">Líder</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{media_pontos} pts</div>
                    <div class="metric-label">Média Geral</div>
                </div>
            </div>
        """), unsafe_allow_html=True)
        
        p1_nome, p1_pts = "Aguardando", "0 pts"
        p2_nome, p2_pts = "Aguardando", "0 pts"
        p3_nome, p3_pts = "Aguardando", "0 pts"
        
        if len(ranking) > 0 and col_part_ref in ranking.columns and col_pts_ref in ranking.columns:
            p1_nome = str(ranking.iloc[0][col_part_ref]).title()
            p1_pts = f"{safe_to_int(ranking.iloc[0][col_pts_ref])} pts"
        if len(ranking) > 1 and col_part_ref in ranking.columns and col_pts_ref in ranking.columns:
            p2_nome = str(ranking.iloc[1][col_part_ref]).title()
            p2_pts = f"{safe_to_int(ranking.iloc[1][col_pts_ref])} pts"
        if len(ranking) > 2 and col_part_ref in ranking.columns and col_pts_ref in ranking.columns:
            p3_nome = str(ranking.iloc[2][col_part_ref]).title()
            p3_pts = f"{safe_to_int(ranking.iloc[2][col_pts_ref])} pts"
            
        st.markdown(textwrap.dedent(f"""
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
        """), unsafe_allow_html=True)
        
        st.markdown('<div class="ranking-list">', unsafe_allow_html=True)
        for idx, row in ranking.iterrows():
            posicao = idx + 1
            if posicao <= 3: continue
            usuario = str(row[col_part_ref]).title()
            pontos = safe_to_int(row[col_pts_ref])
            inicial = usuario[0] if len(usuario) > 0 else "?"
            st.markdown(textwrap.dedent(f"""
                <div class="ranking-item">
                    <div class="ranking-left">
                        <span class="ranking-pos">#{posicao}</span>
                        <div class="ranking-avatar">{inicial}</div>
                        <span class="ranking-name">{usuario}</span>
                    </div>
                    <span class="ranking-score">{pontos} pts</span>
                </div>
            """), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Aguardando inserção de palpites para carregar a classificação geral!")

with tab_enviar:
    st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Palpites da Equipe</h3>", unsafe_allow_html=True)
    
    email_user = st.text_input("E-mail Corporativo:", placeholder="exemplo@feltrim.com.br", key="env_email").strip().lower()
    nome_user = st.text_input("Nome Completo:", placeholder="Seu nome completo", key="env_nome").strip()
    
    if not email_user or "@" not in email_user or not nome_user:
        st.info("💡 Insira seu Nome e E-mail Corporativo para abrir as votações de palpites!")
    else:
        jogos_ativos = []
        for col_jogo in lista_jogos_formulario:
            # Regra estrita: remover os jogos que ocorrem na data de hoje (16/06)
            dia, mes = extrair_data_jogo(col_jogo)
            if dia == 16 and mes == 6:
                continue
                
            status_jogo = "🕒 Agendado"
            if df_resultados is not None and not df_resultados.empty:
                df_resultados.columns = df_resultados.columns.str.strip()
                match_status = df_resultados[df_resultados['Jogo'].astype(str).str.strip() == col_jogo]
                if not match_status.empty:
                    status_jogo = str(match_status.iloc[0]['Status']).strip()
            
            # Só exibe para palpite se estiver com status de agendado
            if "agendado" in status_jogo.lower():
                jogos_ativos.append(col_jogo)
                
        for col_jogo in jogos_ativos:
            dia, mes = extrair_data_jogo(col_jogo)
            partes = col_jogo.split('vs') if 'vs' in col_jogo.lower() else col_jogo.split('VS')
            t1 = formatar_nome_time(partes[0])
            t2 = formatar_nome_time(partes[1]) if len(partes) > 1 else "Visitante"
            
            total_votos_jogo = 0
            votos_t1 = 0
            votos_draw = 0
            votos_t2 = 0
            
            if df_respostas is not None and not df_respostas.empty:
                validos = df_respostas[df_respostas[col_jogo].notna() & (df_respostas[col_jogo].astype(str).str.strip() != '')]
                total_votos_jogo = len(validos)
                votos_t1 = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains(t1.lower())]) if t1 else 0
                votos_draw = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains('empate')])
                votos_t2 = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains(t2.lower())]) if t2 else 0
            
            pct_t1 = int((votos_t1 / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
            pct_draw = int((votos_draw / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
            pct_t2 = int((votos_t2 / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
            
            st.markdown(textwrap.dedent(f"""
                <div class="poll-card">
                    <div class="poll-header">🎯 Escolha quem vai Vencer - {dia:02d}/{mes:02d}</div>
                    <div class="poll-teams">
                        <div class="poll-team-box">
                            <span class="poll-team-name">{t1}</span>
                        </div>
                        <span class="poll-vs">VS</span>
                        <div class="poll-team-box">
                            <span class="poll-team-name">{t2}</span>
                        </div>
                    </div>
                    
                    <div class="poll-bar-container">
                        <div class="poll-bar-label"><span>{t1} Vence ({pct_t1}%)</span><span>{votos_t1} palpites</span></div>
                        <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-m" style="width: {pct_t1}%;"></div></div>
                    </div>
                    <div class="poll-bar-container">
                        <div class="poll-bar-label"><span>Empate ({pct_draw}%)</span><span>{votos_draw} palpites</span></div>
                        <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-draw" style="width: {pct_draw}%;"></div></div>
                    </div>
                    <div class="poll-bar-container" style="margin-bottom: 20px;">
                        <div class="poll-bar-label"><span>{t2} Vence ({pct_t2}%)</span><span>{votos_t2} palpites</span></div>
                        <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-v" style="width: {pct_t2}%;"></div></div>
                    </div>
                </div>
            """), unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                palpite_m_formatado = f"Vitória do {t1}".strip()
                if st.button(f"Vitória {t1}", key=f"v_t1_{col_jogo}"):
                    payload = {"action": "fazerPalpite", "email": email_user, "nome": nome_user, "id_jogo": col_jogo, "palpite": palpite_m_formatado}
                    try:
                        r = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                        if r.status_code == 200:
                            st.success("Palpite salvo!")
                            st.balloons()
                            st.cache_data.clear()
                            st.rerun()
                    except:
                        st.error("Erro ao registrar voto.")
                            
            with col_btn2:
                if st.button("🤝 Empate", key=f"v_draw_{col_jogo}"):
                    payload = {"action": "fazerPalpite", "email": email_user, "nome": nome_user, "id_jogo": col_jogo, "palpite": "🤝 Empate"}
                    try:
                        r = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                        if r.status_code == 200:
                            st.success("Palpite salvo!")
                            st.balloons()
                            st.cache_data.clear()
                            st.rerun()
                    except:
                        st.error("Erro ao registrar voto.")
                            
            with col_btn3:
                palpite_v_formatado = f"Vitória do {t2}".strip()
                if st.button(f"Vitória {t2}", key=f"v_t2_{col_jogo}"):
                    payload = {"action": "fazerPalpite", "email": email_user, "nome": nome_user, "id_jogo": col_jogo, "palpite": palpite_v_formatado}
                    try:
                        r = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                        if r.status_code == 200:
                            st.success("Palpite salvo!")
                            st.balloons()
                            st.cache_data.clear()
                            st.rerun()
                    except:
                        st.error("Erro ao registrar voto.")
            st.markdown("<br>", unsafe_allow_html=True)
            
        if len(jogos_ativos) == 0:
            st.info("🕒 Nenhuma partida agendada aberta no momento. Aguarde liberação do administrador!")

with tab_palpites:
    st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Consulta de Palpites por Participante</h3>", unsafe_allow_html=True)
    
    if df_respostas is not None and not df_respostas.empty:
        df_respostas.columns = df_respostas.columns.str.strip()
        df_respostas_filtradas = df_respostas[
            (df_respostas[col_email].astype(str).str.contains("@", na=True))
        ]
        
        mapa_nomes = df_respostas_filtradas.groupby(col_email)[col_nome].first().to_dict()
        
        def obter_nome_exibicao(email_val):
            nome_completo = mapa_nomes.get(email_val, email_val)
            if nome_completo == email_val and "@" in str(email_val):
                return str(email_val).split('@')[0].capitalize()
            return str(nome_completo).title()
            
        usuarios_nomes_map = {email: obter_nome_exibicao(email) for email in df_respostas_filtradas[col_email].unique()}
        usuarios_ordenados = sorted(usuarios_nomes_map.items(), key=lambda item: item[1])
        
        usuario_email_selecionado = st.selectbox(
            "Selecione o Participante:", 
            options=[item[0] for item in usuarios_ordenados], 
            format_func=lambda x: usuarios_nomes_map[x],
            key="consulta_email"
        )
        
        if usuario_email_selecionado:
            palpites_user = df_respostas_filtradas[df_respostas_filtradas[col_email] == usuario_email_selecionado].iloc[-1]
            for col_name in lista_jogos_formulario:
                palpite_val = palpites_user[col_name]
                if pd.isna(palpite_val) or str(palpite_val).strip().lower() in ['nan', 'none', '']:
                    continue
                
                partes = col_name.split('vs') if 'vs' in col_name.lower() else col_name.split('VS')
                t1 = formatar_nome_time(partes[0])
                t2 = formatar_nome_time(partes[1]) if len(partes) > 1 else ""
                dia, mes = extrair_data_jogo(col_name)
                
                st.markdown(textwrap.dedent(f"""
                    <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #e8efe9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="font-weight: 700; color: #1e293b; margin: 0; font-size: 0.95rem;">{t1} vs {t2} - {dia:02d}/{mes:02d}</p>
                            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #003566; font-weight:600;">Palpite: <strong style="color: #004b23;">{palpite_val}</strong></p>
                        </div>
                    </div>
                """), unsafe_allow_html=True)
    else:
        st.info("Nenhum palpite enviado ainda!")

with tab_jogos:
    st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Placares Reais dos Jogos</h3>", unsafe_allow_html=True)
    if df_resultados is not None and not df_resultados.empty:
        df_resultados.columns = df_resultados.columns.str.strip()
        df_resultados_sorted = df_resultados.copy()
        df_resultados_sorted['Data_Ordenacao'] = df_resultados_sorted['Jogo'].apply(chave_ordenacao_jogo)
        df_resultados_sorted = df_resultados_sorted.sort_values(by='Data_Ordenacao').reset_index(drop=True)
        
        for _, jogo in df_resultados_sorted.iterrows():
            nome_jogo = jogo['Jogo']
            p_m = jogo['Placar Real Mandante']
            p_v = jogo['Placar Real Visitante']
            status = jogo['Status']
            
            p_m_display = str(int(float(p_m))) if pd.notna(p_m) and str(p_m).strip() != "" else ""
            p_v_display = str(int(float(p_v))) if pd.notna(p_v) and str(p_v).strip() != "" else ""
            
            status_clean = str(status).strip().lower()
            if "encerrado" in status_clean:
                badge_label = "🟢 Encerrado"
            elif "andamento" in status_clean or "vivo" in status_clean:
                badge_label = "🟡 Ao Vivo"
            else:
                badge_label = "🕒 Agendado"
            
            tem_placar = p_m_display != "" and p_v_display != ""
            
            times = str(nome_jogo).split('vs') if 'vs' in str(nome_jogo) else str(nome_jogo).split('VS')
            time1 = formatar_nome_time(times[0].strip()) if len(times) > 0 else "Mandante"
            time2 = formatar_nome_time(times[1].strip()) if len(times) > 1 else "Visitante"
            dia, mes = extrair_data_jogo(nome_jogo)
            
            st.markdown(textwrap.dedent(f"""
                <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #e8efe9; margin-bottom: 12px; display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: bold; color: #475569;">
                        <span>🏆 Copa 2026 - {dia:02d}/{mes:02d}</span>
                        <span>{badge_label}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0;">
                        <div style="display: flex; align-items: center; gap: 8px; width: 35%;">
                            <span style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">{time1}</span>
                        </div>
                        <div style="font-size: 1.2rem; font-weight: 800; color: #004b23; width: 30%; text-align: center;">
                            {p_m_display if tem_placar else " - "} VS {p_v_display if tem_placar else " - "}
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px; width: 35%; justify-content: flex-end; text-align: right;">
                            <span style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">{time2}</span>
                        </div>
                    </div>
                </div>
            """), unsafe_allow_html=True)
    else:
        st.info("Planilha de resultados vazia ou não carregada!")

st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🛠️ Painel de Controle do Administrador"):
    senha_admin = st.text_input("Senha do Administrador:", type="password", key="senha_admin")
    if senha_admin == "feltrim2026":
        st.success("Acesso Autorizado!")
        
        st.write("### ⚽ Gravar/Alterar Placar Oficial")
        if lista_jogos_formulario:
            jogo_selecionado = st.selectbox("Selecione o Jogo para atualizar:", options=lista_jogos_formulario)
            
            partes_jogo = jogo_selecionado.split('vs') if 'vs' in jogo_selecionado.lower() else jogo_selecionado.split('VS')
            nome_m = formatar_nome_time(partes_jogo[0])
            nome_v = formatar_nome_time(partes_jogo[1]) if len(partes_jogo) > 1 else "Visitante"
            
            col_gols_m, col_gols_v = st.columns(2)
            with col_gols_m:
                gols_m = st.number_input(f"Gols {nome_m}:", min_value=0, max_value=20, value=0, step=1, key="gols_m_admin")
            with col_gols_v:
                gols_v = st.number_input(f"Gols {nome_v}:", min_value=0, max_value=20, value=0, step=1, key="gols_v_admin")
                
            status_jogo = st.selectbox("Status:", options=["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"])
            
            if st.button("🚀 Salvar Placar e Recalcular"):
                payload = {
                    "action": "atualizarPlacar", "senha": "feltrim2026", "jogo": jogo_selecionado,
                    "placar_m": int(gols_m), "placar_v": int(gols_v), "status": status_jogo
                }
                try:
                    response = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                    res_json = response.json()
                    if response.status_code == 200 and res_json.get("status") == "success":
                        st.success("Placar salvo e pontos recalculados!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Erro: {res_json.get('message')}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
                        
        st.write("---")
        novo_sheet_id = st.text_input("ID do Google Sheets:", value=st.session_state["sheet_id"])
        if novo_sheet_id != st.session_state["sheet_id"]:
            st.session_state["sheet_id"] = novo_sheet_id
            st.cache_data.clear()
            st.rerun()
    elif senha_admin:
        st.error("Senha incorreta!")

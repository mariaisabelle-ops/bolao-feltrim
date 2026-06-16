import streamlit as st
import pandas as pd
import requests
import json
import re
from datetime import datetime, timedelta

# Configurações globais da página
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
    
    /* Fundo de Tela Moderno */
    .stApp {
        background: linear-gradient(135deg, #f5f8f6 0%, #eef3ef 100%);
    }
    
    /* Banner Corporativo Premium */
    .banner-container {
        background: linear-gradient(135deg, #004b23 0%, #002e14 100%);
        color: #ffffff;
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 75, 35, 0.18);
        border-bottom: 5px solid #d4af37;
        position: relative;
        overflow: hidden;
    }
    
    .banner-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 80%);
        pointer-events: none;
    }
    
    .banner-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -1.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .banner-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    .card-metric {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 16px;
        border-left: 6px solid #004b23;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
        text-align: center;
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card-metric:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    
    .card-val {
        font-size: 2.1rem;
        font-weight: 800;
        color: #004b23;
        line-height: 1.1;
    }
    
    .card-lbl {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* Pódio Sleek 3D */
    .podium-wrapper {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 15px;
        margin: 30px 0;
        flex-wrap: wrap;
    }
    
    .podium-box {
        background-color: #ffffff;
        border-radius: 18px;
        padding: 25px 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(0, 75, 35, 0.05);
        flex: 1;
        min-width: 250px;
        transition: transform 0.2s ease;
    }
    
    .podium-box:hover {
        transform: translateY(-5px);
    }
    
    .podium-1 {
        border-top: 6px solid #d4af37;
        background: linear-gradient(180deg, #fffef5 0%, #ffffff 100%);
        box-shadow: 0 12px 35px rgba(212, 175, 55, 0.15);
        order: 2;
    }
    
    .podium-2 {
        border-top: 6px solid #b5c2b7;
        order: 1;
    }
    
    .podium-3 {
        border-top: 6px solid #ca9063;
        order: 3;
    }
    
    .podium-rank-badge {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 12px auto;
        font-weight: 800;
        font-size: 1.2rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .badge-p1 { background: linear-gradient(135deg, #ffd700, #ffa500); color: white; }
    .badge-p2 { background: linear-gradient(135deg, #e0e0e0, #9e9e9e); color: white; }
    .badge-p3 { background: linear-gradient(135deg, #d7ccc8, #8d6e63); color: white; }
    
    .podium-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #004b23;
        margin-top: 5px;
        word-wrap: break-word;
    }
    
    .podium-points {
        font-size: 1.8rem;
        font-weight: 800;
        color: #004b23;
        margin: 8px 0;
    }

    .table-container {
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.03);
        overflow: hidden;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .premium-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }
    
    .premium-table th {
        background-color: #004b23;
        color: white;
        padding: 16px 20px;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .premium-table td {
        padding: 14px 20px;
        border-bottom: 1px solid #f0f0f0;
        font-size: 0.95rem;
        color: #333;
    }
    
    .premium-table tr:last-child td {
        border-bottom: none;
    }
    
    .premium-table tr:hover {
        background-color: #f8faf8;
    }

    /* Cards de Jogos */
    .match-card {
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 16px; 
        margin-bottom: 16px; 
        border: 1px solid rgba(0,0,0,0.06); 
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .match-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    }

    .badge-open {
        background-color: rgba(0, 75, 35, 0.1);
        color: #004b23;
        border: 1px solid rgba(0, 75, 35, 0.2);
    }
    
    .badge-closed {
        background-color: rgba(217, 4, 41, 0.08);
        color: #d90429;
        border: 1px solid rgba(217, 4, 41, 0.15);
    }
</style>
""", unsafe_allow_html=True)

def safe_to_int(val):
    """Converte com segurança valores para inteiros, prevenindo erros de float ou NaNs."""
    try:
        if pd.isna(val) or val is None or str(val).strip() == "":
            return ""
        return int(float(val))
    except Exception:
        return ""

def obter_datetime_jogo(nome_jogo, horario_str):
    """Gera um objeto datetime combinando a data descrita no nome do jogo com o horário de início."""
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
    """Gera tupla de ordenação cronológica a partir do nome do jogo para ordenar o DataFrame."""
    match = re.search(r'(\d{2})/(\d{2})', str(text))
    if match:
        dia, mes = int(match.group(1)), int(match.group(2))
        return (mes, dia)
    return (12, 31)

def formatar_time_slug(nome_completo_jogo, time_tipo="mandante"):
    """Isola os nomes limpos de mandantes e visitantes tirando marcações adicionais."""
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
    """Puxa dados das abas do Google Sheets com tratamento de erros integrado."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        if df.empty or (df.columns.size > 0 and str(df.columns[0]).startswith("<!DOCTYPE")):
            return None
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return None

# Recupera ID ativo do Bolão
if 'spreadsheet_id' not in st.session_state:
    st.session_state['spreadsheet_id'] = DEFAULT_SPREADSHEET_ID

sheet_id = st.session_state['spreadsheet_id']

# Leitura e Fallback de Abas
df_palpites = fetch_spreadsheet_data(sheet_id, "Palpites")
if df_palpites is None or df_palpites.empty:
    df_palpites = fetch_spreadsheet_data(sheet_id, "Respostas_Formulario")

df_resultados = fetch_spreadsheet_data(sheet_id, "Resultados")
if df_resultados is None or df_resultados.empty:
    df_resultados = fetch_spreadsheet_data(sheet_id, "Resultados Oficiais")

df_classificacao = fetch_spreadsheet_data(sheet_id, "Classificacao")
if df_classificacao is None or df_classificacao.empty:
    df_classificacao = fetch_spreadsheet_data(sheet_id, "Classificação")

if df_resultados is None:
    st.warning("⚠️ **Acesso à Planilha Não Configurado ou Privado**")
    st.info("""
    Para que o sistema exiba os dados, certifique-se de que:
    1. Compartilhou a sua planilha no modo **"Qualquer pessoa com o link pode ler"** (Leitor).
    2. Registrou o ID correto da planilha no painel administrativo abaixo.
    """)
    
    with st.expander("🔑 Painel de Configuração Inicial"):
        novo_id = st.text_input("ID da Planilha Google (Cole o ID ou o link completo):", value=sheet_id)
        if st.button("Gravar Nova Planilha"):
            id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', novo_id)
            final_id = id_match.group(1) if id_match else novo_id
            st.session_state['spreadsheet_id'] = final_id
            st.cache_data.clear()
            st.rerun()
    st.stop()

if df_resultados.empty:
    # Cria estrutura de fallback segura para evitar quebras do Pandas
    df_resultados = pd.DataFrame(columns=['Jogo', 'Status', 'Placar Real Mandante', 'Placar Real Visitante', 'Horário'])
else:
    if 'Jogo' not in df_resultados.columns:
        df_resultados = pd.DataFrame(columns=['Jogo', 'Status', 'Placar Real Mandante', 'Placar Real Visitante', 'Horário'])
    if 'Status' not in df_resultados.columns:
        df_resultados['Status'] = "🕒 Agendado"
    if 'Horário' not in df_resultados.columns:
        df_resultados['Horário'] = "15:00"

# Ordenação Cronológica de Segurança
if not df_resultados.empty:
    df_resultados_sorted = df_resultados.copy()
    df_resultados_sorted = df_resultados_sorted.dropna(subset=['Jogo'])
    df_resultados_sorted['Jogo'] = df_resultados_sorted['Jogo'].astype(str)
    df_resultados_sorted = df_resultados_sorted[df_resultados_sorted['Jogo'].str.strip() != ""]
    
    df_resultados_sorted['Data_Ordenacao'] = df_resultados_sorted['Jogo'].apply(chave_ordenacao_jogo)
    df_resultados_sorted = df_resultados_sorted.sort_values(by='Data_Ordenacao').drop(columns=['Data_Ordenacao'])
else:
    df_resultados_sorted = df_resultados.copy()

# Renderiza banner principal corporativo
st.markdown("""
<div class="banner-container">
    <div class="banner-title">🏆 BOLÃO CORPORATIVO FELTRIM CORREA</div>
    <div class="banner-subtitle">Acompanhe seus pontos, lance palpites e dispute o topo do ranking em tempo real!</div>
</div>
""", unsafe_allow_html=True)

# Tabs Principais do Aplicativo
tab_ranking, tab_jogos, tab_palpites, tab_meus_votos, tab_admin = st.tabs([
    "📊 Classificação Geral", 
    "📅 Jogos & Resultados",
    "📝 Dar Palpite", 
    "🎯 Meus Palpites", 
    "⚙️ Painel Admin"
])

with tab_ranking:
    st.markdown("<h2 style='text-align: center; color: #004b23; font-weight: 800; margin-bottom: 25px;'>Placar de Líderes</h2>", unsafe_allow_html=True)
    
    col_rec, col_vazio = st.columns([1, 4])
    with col_rec:
        if st.button("🔄 Recarregar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

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

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-val">{num_competidores}</div>
            <div class="card-lbl">Participantes Ativos</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card-metric" style="border-left-color: #d4af37;">
            <div class="card-val">👑 {lider_nome}</div>
            <div class="card-lbl">Líder do Ranking</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card-metric" style="border-left-color: #0077b6;">
            <div class="card-val">{media_pontos:.1f} pts</div>
            <div class="card-lbl">Média de Pontos</div>
        </div>
        """, unsafe_allow_html=True)

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
            <div class="podium-name" style="font-size: 1.35rem; font-weight: 800;">{p1_nome}</div>
            <div class="podium-points" style="font-size: 2.2rem; color: #004b23; font-weight: 900;">{p1_pts}</div>
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
        
        # Monta a tabela elegante em formato HTML linear (evita o bug de espaçamento do markdown)
        linhas_html = ""
        for i in range(len(posicoes)):
            bg_destaque = "style='background-color: #fffef2; font-weight: bold;'" if i == 0 else ""
            linhas_html += (
                f"<tr {bg_destaque}>"
                f"<td style='font-weight: 700; width: 100px;'>{posicoes[i]}</td>"
                f"<td>{participantes[i]}</td>"
                f"<td style='font-weight: 700; color: #004b23; text-align: right; width: 150px;'>{pontos[i]}</td>"
                f"</tr>"
            )
            
        tabela_completa_html = (
            f"<div class='table-container'>"
            f"<table class='premium-table'>"
            f"<thead>"
            f"<tr>"
            f"<th>Posição</th>"
            f"<th>Competidor</th>"
            f"<th style='text-align: right;'>Pontuação</th>"
            f"</tr>"
            f"</thead>"
            f"<tbody>"
            f"{linhas_html}"
            f"</tbody>"
            f"</table>"
            f"</div>"
        )
        st.html(tabela_completa_html)
    else:
        st.info("Nenhum participante pontuou ainda. Os pontos serão calculados à medida que as partidas forem concluídas!")

with tab_jogos:
    st.markdown("<h2 style='color: #004b23; font-weight: 800; margin-bottom: 8px;'>📅 Tabela de Jogos & Resultados</h2>", unsafe_allow_html=True)
    st.write("Acompanhe os confrontos na ordem cronológica de acontecimento e visualize os placares oficiais cadastrados.")
    
    # Fuso Horário de Brasília de forma automatizada (UTC-3)
    try:
        agora_brasil = datetime.utcnow() - timedelta(hours=3)
    except Exception:
        agora_brasil = datetime.now()

    if df_resultados_sorted.empty:
        st.info("Nenhum jogo cadastrado na tabela de resultados oficiais.")
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
            
            # Bloqueio automático de 1h antes com base no horário de Brasília
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
                    <div style="flex: 1; text-align: right; font-weight: 700; font-size: 1.15rem; color: #333;">{team_m}</div>
                    <div style="padding: 0 15px; font-size: 1.6rem; font-weight: 900; color: #004b23; min-width: 120px; text-align: center; letter-spacing: 2px;">
                        {f"{safe_to_int(p_m)} - {safe_to_int(p_v)}" if pd.notna(p_m) and pd.notna(p_v) and str(p_m).strip() != "" and str(p_v).strip() != "" else "VS"}
                    </div>
                    <div style="flex: 1; text-align: left; font-weight: 700; font-size: 1.15rem; color: #333;">{team_v}</div>
                </div>
                <div style="text-align: center; margin-top: 10px; border-top: 1px solid #f5f5f5; padding-top: 8px;">
                    <span style="font-size: 0.78rem; color: #777; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Estado: {status_oficial}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab_palpites:
    st.markdown("<h2 style='color: #004b23; font-weight: 800; margin-bottom: 20px;'>Enviar Meu Palpite</h2>", unsafe_allow_html=True)
    
    email_user = st.text_input("Seu E-mail Corporativo Feltrim Correa:", value="", placeholder="exemplo@feltrim.com.br")
    nome_user = st.text_input("Seu Nome Completo:", value="")

    # Fuso Horário de Brasília
    try:
        agora_brasil = datetime.utcnow() - timedelta(hours=3)
    except Exception:
        agora_brasil = datetime.now()

    jogos_disponiveis = []

    for idx, row in df_resultados_sorted.iterrows():
        status_raw = row.get('Status')
        status_jogo = "🕒 Agendado" if pd.isna(status_raw) or str(status_raw).strip() == "" else str(status_raw)
        nome_jogo = str(row['Jogo'])
        horario_col = row.get('Horário', '15:00')
        
        # Bloqueio automático de 1 hora antes de cada jogo
        dt_jogo = obter_datetime_jogo(nome_jogo, horario_col)
        jogo_bloqueado = False
        
        if dt_jogo:
            limite_palpite = dt_jogo - timedelta(hours=1)
            if agora_brasil >= limite_palpite:
                jogo_bloqueado = True
        else:
            match_data = re.search(r'(\d{2})/(\d{2})', nome_jogo)
            if match_data:
                try:
                    dia_j, mes_j = int(match_data.group(1)), int(match_data.group(2))
                    data_limite_jogo = datetime(2026, mes_j, dia_j).date()
                    if data_limite_jogo <= agora_brasil.date():
                        jogo_bloqueado = True
                except Exception:
                    pass

        if "agendado" in status_jogo.lower() and not jogo_bloqueado:
            jogos_disponiveis.append(nome_jogo)

    if not jogos_disponiveis:
        st.info("Não existem novas partidas abertas para palpites no momento! Todos os confrontos ativos já foram trancados.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("---")
        
        jogo_selecionado = st.selectbox("Selecione a partida que deseja votar:", jogos_disponiveis)
        
        if jogo_selecionado:
            team_m = formatar_time_slug(jogo_selecionado, "mandante")
            team_v = formatar_time_slug(jogo_selecionado, "visitante")
            
            # Verificação em tempo real de duplicidade de palpites
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
                st.warning(f"⚠️ **Palpite já registrado!** Você já enviou seu palpite para este jogo: **'{voto_anterior}'**. Para manter a integridade do bolão, alterações de palpites não são permitidas após o envio.")
            else:
                voto_opcao = st.radio(
                    "Escolha o seu palpite oficial:",
                    [
                        f"🟢 Vitória do {team_m}",
                        "🤝 Empate",
                        f"🟢 Vitória do {team_v}"
                    ],
                    index=0
                )
                
                if st.button("Confirmar e Enviar Palpite 🚀", use_container_width=True):
                    if not email_user or "@" not in email_user:
                        st.error("Por favor, informe um e-mail corporativo válido para registrar o palpite.")
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
                                        st.success(f"Excelente, {nome_user}! Palpite para '{jogo_selecionado}' registrado com sucesso!")
                                        st.cache_data.clear()
                                        st.rerun()
                                    else:
                                        st.error(f"Erro no registro: {res_json.get('message')}")
                                else:
                                    st.error("Erro na resposta do servidor. Tente novamente em instantes.")
                            except Exception as e:
                                st.error(f"Erro técnico de rede: {str(e)}")

with tab_meus_votos:
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
                    
                    historico_lista = []
                    
                    for col in df_palpites.columns:
                        if "vs" in col or "⚽" in col:
                            voto_valor = registros_usuario.iloc[0][col]
                            if pd.notna(voto_valor) and str(voto_valor).strip() != "":
                                status_oficial = "🕒 Agendado"
                                placar_text = "Sem placar cadastrado"
                                
                                match_resultado = df_resultados[df_resultados['Jogo'] == col]
                                if not match_resultado.empty:
                                    status_oficial = match_resultado.iloc[0].get('Status', '🕒 Agendado')
                                    p_m = match_resultado.iloc[0].get('Placar Real Mandante', '')
                                    p_v = match_resultado.iloc[0].get('Placar Real Visitante', '')
                                    if pd.notna(p_m) and pd.notna(p_v) and str(p_m) != "" and str(p_v) != "":
                                        placar_text = f"Resultado Real: {safe_to_int(p_m)} x {safe_to_int(p_v)}"
                                
                                historico_lista.append({
                                    "Partida": col,
                                    "Seu Voto": voto_valor,
                                    "Status": status_oficial,
                                    "Placar Oficial": placar_text
                                })
                    
                    if historico_lista:
                        st.table(pd.DataFrame(historico_lista))
                    else:
                        st.info("Nenhum palpite individual registrado nas colunas da planilha.")
            else:
                st.error("Estrutura da aba 'Palpites' incorreta. Coluna de e-mail não encontrada.")
        else:
            st.info("Ainda não existem palpites registrados por competidores na planilha.")

with tab_admin:
    st.markdown("<h2 style='color: #004b23; font-weight: 800;'>🔐 Painel de Controle Administrativo</h2>", unsafe_allow_html=True)
    
    senha_admin = st.text_input("Senha do Administrador:", type="password")
    
    if senha_admin == "feltrim2026":
        st.success("Acesso administrativo autenticado com sucesso!")
        st.write("---")
        
        st.markdown("### 🏆 Cadastro de Resultados Oficiais")
        
        lista_atualizacao = list(df_resultados_sorted['Jogo'].unique())
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
                
                with st.spinner("Atualizando resultados e recalculando posições do ranking..."):
                    try:
                        response = requests.post(URL_APPS_SCRIPT, json=payload_admin, timeout=10)
                        if response.status_code == 200:
                            res_json = response.json()
                            if res_json.get("status") == "success":
                                st.success(f"Placar gravado! {team_m} {novo_placar_m} x {novo_placar_v} {team_v} ({novo_status})")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Falha de resposta no servidor: {res_json.get('message')}")
                        else:
                            st.error("Erro técnico de comunicação no servidor do Apps Script.")
                    except Exception as e:
                        st.error(f"Erro técnico de rede: {str(e)}")
                        
        st.write("---")
        st.markdown("### ✨ Inicialização Rápida de Partidas")
        st.write("Se a sua nova planilha está vazia e você precisa carregar todos os 56 jogos oficiais da Copa em ordem cronológica de uma só vez, utilize o botão abaixo:")
        
        if st.button("✨ Inicializar Todos os 56 Jogos na Planilha", use_container_width=True):
            payload_init = {
                "action": "inicializarNovoBolao",
                "senha": "feltrim2026"
            }
            with st.spinner("Criando as abas e cadastrando os 56 confrontos na planilha Google..."):
                try:
                    response = requests.post(URL_APPS_SCRIPT, json=payload_init, timeout=25)
                    if response.status_code == 200:
                        res_json = response.json()
                        if res_json.get("status") == "success":
                            st.success("Tabelas configuradas com sucesso! Todos os 56 jogos já estão criados.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Erro na criação: {res_json.get('message')}")
                    else:
                        st.error("Erro de comunicação com o servidor.")
                except Exception as e:
                    st.error(f"Erro técnico de comunicação: {str(e)}")

        st.write("---")
        st.markdown("### ⚙️ Troca de Planilha Ativa")
        st_id_input = st.text_input("ID da Planilha Google em Uso:", value=sheet_id)
        if st.button("Gravar Alteração de Planilha"):
            st.session_state['spreadsheet_id'] = st_id_input
            st.cache_data.clear()
            st.success("Planilha atualizada com sucesso nesta sessão do app!")
            st.rerun()
    elif senha_admin != "":
        st.error("Senha de Administrador incorreta!")

st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 0.85rem;'>🏆 Feltrim Correa - Todos os direitos reservados. Desenvolvimento de TI Integrado Copa 2026.</p>", unsafe_allow_html=True)

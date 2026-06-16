import streamlit as st
import pandas as pd
import urllib.parse
import requests
import json
import re
import textwrap
import unicodedata

# =========================================================================
# ⚙️ CONFIGURAÇÃO DE INTEGRAÇÃO (COLE SEU LINK DO APPS SCRIPT AQUI)
# =========================================================================
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbz_your_actual_script_id_here/exec"
# =========================================================================

st.set_page_config(
    page_title="Bolão Feltrim Correa - Copa 2026",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom css for brazil theme branding
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

    /* Alertas Personalizados Estilo Premium */
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

    /* Pódio Verde e Amarelo */
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
    
    .podium-badge {
        font-size: 1.8rem;
        margin-bottom: 5px;
    }
    
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

    /* Lista do Leaderboard */
    .ranking-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
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
    
    .ranking-left {
        display: flex;
        align-items: center;
        gap: 12px;
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

    /* Estilo de Cartões de Jogos em Grade de Enquete */
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
    
    .poll-team-flag {
        font-size: 1.8rem;
        margin-bottom: 6px;
    }
    
    .poll-team-name {
        font-weight: 700;
        color: #1e293b;
        font-size: 0.95rem;
        line-height: 1.2;
    }
    
    .poll-vs {
        font-weight: 800;
        font-size: 0.95rem;
        color: #004b23;
        background-color: #e8efe9;
        padding: 4px 10px;
        border-radius: 20px;
    }

    /* Barras de Estatística de Palpites */
    .poll-bar-container {
        margin-bottom: 8px;
    }
    
    .poll-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 3px;
    }
    
    .poll-bar-outer {
        background-color: #f1f5f9;
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .poll-bar-inner {
        height: 100%;
        border-radius: 8px;
        transition: width 0.6s ease;
    }
    
    .bar-color-m { background-color: #004b23; }
    .bar-color-draw { background-color: #ffbd00; }
    .bar-color-v { background-color: #003566; }

    /* Personalização de botões nativos */
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

MAPA_EMOJIS_PAIS = {
    "brasil": "🇧🇷💚💛", "brazil": "🇧🇷💚💛",
    "argentina": "🇦🇷💙🤍", "frança": "🇫🇷💙❤️", "franca": "🇫🇷💙❤️", "france": "🇫🇷💙❤️",
    "alemanha": "🇩🇪🖤❤️", "germany": "🇩🇪🖤❤️", "espanha": "🇪🇸❤️💛", "spain": "🇪🇸❤️💛",
    "itália": "🇮🇹💚❤️", "italia": "🇮🇹💚❤️", "italy": "🇮🇹💚❤️", "inglaterra": "🇬🇧❤️🤍", "england": "🇬🇧❤️🤍",
    "portugal": "🇵🇹❤️💚", "holanda": "🇳🇱🧡🤍", "países baixos": "🇳🇱🧡🤍", "netherlands": "🇳🇱🧡🤍",
    "bélgica": "🇧🇪🖤❤️", "belgica": "🇧🇪🖤❤️", "belgium": "🇧🇪🖤❤️", "croácia": "🇭🇷❤️🤍", "croacia": "🇭🇷❤️🤍",
    "uruguai": "🇺🇾💙🤍", "colômbia": "🇨🇴💛💙", "chile": "🇨🇱❤️💙", "equador": "🇪🇨💛💙", "marrocos": "🇲🇦❤️💚",
    "japão": "🇯🇵❤️🤍", "japan": "🇯🇵❤️🤍", "coreia": "🇰🇷❤️💙", "korea": "🇰🇷❤️💙", "senegal": "🇸🇳💚❤️",
    "eua": "🇺🇸💙❤️", "usa": "🇺🇸💙❤️", "estados unidos": "🇺🇸💙❤️", "méxico": "🇲🇽💚❤️", "canadá": "🇨🇦❤️🤍",
    "haiti": "🇭🇹💙❤️", "paraguai": "🇵🇾❤️💙", "peru": "🇵🇪❤️🤍", "venezuela": "🇻🇪💛💙", "bolívia": "🇧🇴❤️💚",
    "república tcheca": "🇨🇿💙❤️", "republica tcheca": "🇨🇿💙❤️", "áfrica do sul": "🇿🇦💚💛", "africa do sul": "🇿🇦💚💛",
    "suíça": "🇨🇭❤️🤍", "bósnia": "🇧🇦💙💛", "catar": "🇶🇦💜🤍", "escócia": "🇬🇧💙🤍", "turquia": "🇹🇷❤️🤍",
    "austrália": "🇦🇺💙❤️", "costa do marfim": "🇨🇮🧡💚", "curaçau": "🇨🇼💙💛", "suécia": "🇸🇪💙💛", "tunísia": "🇹🇳❤️🤍",
    "irã": "🇮🇷💚❤️", "nova zelândia": "🇳🇿💙❤️", "egito": "🇪🇬❤️🖤", "arábia saudita": "🇸🇦💚🤍", "cabo verde": "🇨🇻💙❤️",
    "iraque": "🇮🇶❤️💚", "noruega": "🇳🇴❤️💙", "algéria": "🇩🇿💚❤️", "áustria": "🇦🇹❤️🤍", "jordânia": "🇯🇴❤️💚",
    "rd do congo": "🇨🇩💙❤️", "uzbequistão": "🇺🇿💙💚", "gana": "🇬🇭❤️💛", "panamá": "🇵🇦💙❤️"
}

def remover_acentos(texto):
    if not texto:
        return ""
    return "".join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    ).lower()

def obter_emojis_pais(nome_time):
    if not nome_time or pd.isna(nome_time):
        return "🏳️⚽"
    nome_clean = str(nome_time).strip().lower()
    nome_sem_emoji = re.sub(r'[^\w\s]', '', nome_clean).strip()
    for pais, emojis in MAPA_EMOJIS_PAIS.items():
        if pais in nome_sem_emoji:
            return emojis
    return "🏳️⚽"

def formatar_nome_time(nome_time):
    if not nome_time or pd.isna(nome_time):
        return ""
    nome_limpo = str(nome_time).strip()
    nome_limpo = re.sub(r'\(\d{2}/\d{2}\)', '', nome_limpo)
    nome_limpo = re.sub(r'[^\w\s\-\.]', '', nome_limpo)
    return nome_limpo.strip()

def normalizar_nome_jogo(nome):
    if not nome or pd.isna(nome):
        return ""
    s = str(nome).lower()
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'[^\w\s]', '', s)
    parts = s.split('vs')
    if len(parts) == 2:
        return f"{parts[0].strip()} vs {parts[1].strip()}"
    return s.strip()

# Inicialização de estado seguro para o ID da planilha
if "sheet_id" not in st.session_state:
    st.session_state["sheet_id"] = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"

@st.cache_data(ttl=5)
def carregar_dados_seguro(sheet_id):
    df_resp = None
    df_res = None
    is_private = False
    
    # Lista de abas que podem conter palpites
    abas_palpites = ["Form Responses 2", "Respostas_Formulario", "Form Responses 1"]
    for aba in abas_palpites:
        try:
            aba_encoded = urllib.parse.quote(aba)
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={aba_encoded}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                if response.text.strip().startswith("<html") or "<!DOCTYPE" in response.text:
                    is_private = True
                    break
                df_temp = pd.read_csv(url)
                if df_temp is not None and not df_temp.empty:
                    df_temp.columns = df_temp.columns.str.strip()
                    df_resp = df_temp
                    break
        except Exception:
            pass

    # Lista de abas que podem conter resultados oficiais
    abas_resultados = ["🎯 Resultados Oficiais", "Resultados Oficiais", "Resultados"]
    for aba in abas_resultados:
        try:
            aba_encoded = urllib.parse.quote(aba)
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet={aba_encoded}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and not (response.text.strip().startswith("<html") or "<!DOCTYPE" in response.text):
                df_temp = pd.read_csv(url)
                if df_temp is not None and not df_temp.empty:
                    df_temp.columns = df_temp.columns.str.strip()
                    df_res = df_temp
                    break
        except Exception:
            pass

    return df_resp, df_res, is_private

df_respostas_raw, df_resultados_raw, is_private = carregar_dados_seguro(st.session_state["sheet_id"])

# Títulos Principais
st.write('<h1 class="header-title">🏆 Bolão Feltrim Correa</h1>', unsafe_allow_html=True)
st.write('<p class="header-subtitle">🇧🇷 Rumo ao Hexa - Classificação em Tempo Real!</p>', unsafe_allow_html=True)

if is_private:
    st.markdown(textwrap.dedent("""
        <div class="custom-error-box" style="padding: 18px; border-radius: 12px; margin-bottom: 20px;">
            <h4 style="margin:0 0 8px 0; font-weight:700;">🔒 Acesso Geral da Planilha está Privado</h4>
            <p style="margin:0 0 12px 0; font-size:0.9rem;">O sistema não consegue ler os dados da planilha. Ajuste as permissões no Drive:</p>
            <ol style="margin:0; padding-left:20px; font-size:0.88rem;">
                <li>Abra sua planilha do Google Drive.</li>
                <li>No canto superior direito, clique em <strong>Compartilhar</strong>.</li>
                <li>Em 'Acesso Geral', mude para <strong>'Qualquer pessoa com o link'</strong>.</li>
                <li>Garanta que a permissão ao lado está como <strong>'Leitor'</strong> e salve.</li>
            </ol>
            <p style="margin-top:10px; font-size:0.85rem;"><strong>Nota:</strong> Se você estiver usando uma cópia própria da planilha, insira o ID correto dela no Painel Admin abaixo!</p>
        </div>
    """), unsafe_allow_html=True)

df_respostas = None
df_resultados = None

if df_respostas_raw is not None and not df_respostas_raw.empty:
    df_respostas = df_respostas_raw.dropna(how='all')
    
    col_email_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['email', 'e-mail', 'usuário', 'address'])]
    col_email = col_email_list[0] if col_email_list else df_respostas.columns[1]
    df_respostas = df_respostas.dropna(subset=[col_email])

    col_nome_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['nome', 'completo', 'participante', '👤'])]
    col_nome = col_nome_list[0] if col_nome_list else col_email

lista_jogos_formulario = []
if df_respostas is not None:
    for col in df_respostas.columns:
        if "vs" in col.lower() or "⚽" in col:
            lista_jogos_formulario.append(col.strip())

if df_resultados_raw is not None and not df_resultados_raw.empty:
    df_resultados_raw.columns = df_resultados_raw.columns.str.strip()
    
    # Normalização robusta contra mudanças de maiúsculas/minúsculas nas colunas
    mapeamento_colunas = {}
    for col in df_resultados_raw.columns:
        col_lower = col.lower()
        if 'jogo' in col_lower and 'id' not in col_lower:
            mapeamento_colunas[col] = 'Jogo'
        elif 'mandante' in col_lower:
            mapeamento_colunas[col] = 'Placar Real Mandante'
        elif 'visitante' in col_lower:
            mapeamento_colunas[col] = 'Placar Real Visitante'
        elif 'status' in col_lower:
            mapeamento_colunas[col] = 'Status'
            
    df_resultados_raw = df_resultados_raw.rename(columns=mapeamento_colunas)
    
    if 'Jogo' in df_resultados_raw.columns:
        df_resultados = df_resultados_raw.dropna(subset=['Jogo'], how='any')
        df_resultados['Jogo'] = df_resultados['Jogo'].astype(str).str.strip()
        
        # Garante que colunas de placar e status existem mesmo que não criadas
        for col_nec in ['Placar Real Mandante', 'Placar Real Visitante', 'Status']:
            if col_nec not in df_resultados.columns:
                df_resultados[col_nec] = None
        df_resultados['Status'] = df_resultados['Status'].fillna('Agendado').astype(str).str.strip()
    else:
        # Fallback de segurança se coluna "Jogo" não for localizada
        df_resultados = pd.DataFrame(columns=['Jogo', 'Placar Real Mandante', 'Placar Real Visitante', 'Status'])
else:
    # Cria estrutura de backup para os jogos baseados nos palpites coletados
    jogos_ficticios = []
    for jogo_nome in lista_jogos_formulario:
        jogos_ficticios.append({
            'Jogo': jogo_nome,
            'Placar Real Mandante': None,
            'Placar Real Visitante': None,
            'Status': 'Agendado'
        })
    df_resultados = pd.DataFrame(jogos_ficticios)

if df_respostas is not None and not df_respostas.empty:
    mapa_nomes = df_respostas.groupby(col_email)[col_nome].first().to_dict()

    def obter_nome_exibicao(email_val):
        nome_completo = mapa_nomes.get(email_val, email_val)
        if nome_completo == email_val and "@" in str(email_val):
            return str(email_val).split('@')[0].capitalize()
        return str(nome_completo).title()

    def calcular_pontos_participante(row):
        if df_resultados is None or df_resultados.empty:
            return 0
        pontos = 0
        for col_name in df_respostas.columns:
            if "vs" in col_name.lower() or "⚽" in col_name:
                palpite_usuario = str(row[col_name]).strip()
                if not palpite_usuario or pd.isna(row[col_name]) or palpite_usuario.lower() in ['nan', 'none', '']:
                    continue
                
                # Procura correspondente nos resultados oficiais
                jogo_norm = normalizar_nome_jogo(col_name)
                jogo_oficial = df_resultados[df_resultados['Jogo'].apply(normalizar_nome_jogo) == jogo_norm]
                
                if not jogo_oficial.empty:
                    real_m = jogo_oficial.iloc[0]['Placar Real Mandante']
                    real_v = jogo_oficial.iloc[0]['Placar Real Visitante']
                    status = jogo_oficial.iloc[0]['Status']
                    
                    status_clean = str(status).strip().lower()
                    if pd.isna(real_m) or pd.isna(real_v) or "encerrado" not in status_clean:
                        continue
                    
                    try:
                        val_m = int(float(real_m))
                        val_v = int(float(real_v))
                    except:
                        continue
                    
                    # Identificar o time mandante e visitante para validar acerto de tendência
                    times_split = col_name.split('vs') if 'vs' in col_name.lower() else col_name.split('VS')
                    time_m = formatar_nome_time(times_split[0])
                    time_v = formatar_nome_time(times_split[1]) if len(times_split) > 1 else ""
                    
                    # Unicode cleanup para comparação segura de texto
                    time_m_clean = remover_acentos(time_m)
                    time_v_clean = remover_acentos(time_v)
                    palpite_clean = remover_acentos(palpite_usuario)
                    
                    if val_m > val_v:
                        resultado_real = "mandante"
                    elif val_v > val_m:
                        resultado_real = "visitante"
                    else:
                        resultado_real = "empate"
                        
                    # Se acertou a tendência ganha 10 pontos
                    if resultado_real == "empate" and "empate" in palpite_clean:
                        pontos += 10
                    elif resultado_real == "mandante" and time_m_clean in palpite_clean:
                        pontos += 10
                    elif resultado_real == "visitante" and time_v_clean in palpite_clean:
                        pontos += 10
        return pontos

    # Consolidar palpites pegando o último registro enviado por participante
    def obter_ultimo_nao_nulo(series):
        validos = series.dropna()
        validos = validos[validos.astype(str).str.strip().str.lower() != 'nan']
        validos = validos[validos != '']
        return validos.iloc[-1] if not validos.empty else None

    agg_dict = {col_nome: obter_ultimo_nao_nulo}
    for col in lista_jogos_formulario:
        agg_dict[col] = obter_ultimo_nao_nulo
        
    col_timestamp_list = [col for col in df_respostas.columns if any(x in str(col).lower() for x in ['timestamp', 'carimbo', 'data', 'hora'])]
    col_timestamp = col_timestamp_list[0] if col_timestamp_list else df_respostas.columns[0]
    
    df_respostas[col_timestamp] = pd.to_datetime(df_respostas[col_timestamp], errors='coerce')
    df_respostas_consolidadas = df_respostas.sort_values(col_timestamp).groupby(col_email).agg(agg_dict).reset_index()
    df_respostas_consolidadas['Pontos_Calculados'] = df_respostas_consolidadas.apply(calcular_pontos_participante, axis=1)

    tab_ranking, tab_enviar, tab_palpites, tab_jogos = st.tabs([
        "📊 Classificação", 
        "📝 Dar Palpite", 
        "🎯 Ver Palpites", 
        "⚽ Resultados Reais"
    ])

    with tab_ranking:
        ranking = df_respostas_consolidadas.sort_values(by='Pontos_Calculados', ascending=False).reset_index(drop=True)
        total_participantes = len(ranking)
        lider_atual = obter_nome_exibicao(ranking.iloc[0][col_email]) if total_participantes > 0 else "-"
        media_pontos = int(ranking['Pontos_Calculados'].mean()) if total_participantes > 0 else 0
        
        st.markdown(textwrap.dedent(f"""
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
        """), unsafe_allow_html=True)
        
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
            if posicao <= 3:
                continue
            usuario = obter_nome_exibicao(row[col_email])
            pontos = int(row['Pontos_Calculados'])
            inicial = usuario[0]
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

    with tab_enviar:
        st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Enquete de Palpites em Tempo Real</h3>", unsafe_allow_html=True)
        
        email_user = st.text_input("Insira seu E-mail Corporativo:", placeholder="exemplo@feltrim.com.br", key="env_email").strip().lower()
        nome_user = st.text_input("Insira seu Nome Completo:", placeholder="Seu nome completo aqui", key="env_nome").strip()
        
        gravacao_bloqueada = "your_actual_script_id_here" in URL_APPS_SCRIPT or URL_APPS_SCRIPT == ""
        
        if not email_user or "@" not in email_user or not nome_user:
            st.info("💡 Digite seu Nome e E-mail corporativo acima para liberar o painel de enquetes!")
        else:
            if gravacao_bloqueada:
                st.markdown(textwrap.dedent("""
                    <div class="custom-info" style="border-left-color: #ffbd00; color: #003566; background-color: #fffdf0; margin-bottom: 25px;">
                        ⚠️ <strong>Modo de Demonstração Ativo:</strong> As enquetes abaixo estão liberadas para teste! Para gravar de verdade na planilha, configure a URL real do seu Apps Script no topo do código do app.
                    </div>
                """), unsafe_allow_html=True)
            
            st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
            
            for col_jogo in lista_jogos_formulario:
                partes = col_jogo.split('vs') if 'vs' in col_jogo.lower() else col_jogo.split('VS')
                t1 = formatar_nome_time(partes[0])
                t2 = formatar_nome_time(partes[1]) if len(partes) > 1 else "Visitante"
                
                emojis_t1 = obter_emojis_pais(t1)
                emojis_t2 = obter_emojis_pais(t2)
                
                # Computando estatísticas de palpites enviadas
                total_votos_jogo = len(df_respostas[df_respostas[col_jogo].notna() & (df_respostas[col_jogo] != '')])
                votos_t1 = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains(t1.lower())]) if t1 else 0
                votos_draw = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains('empate')])
                votos_t2 = len(df_respostas[df_respostas[col_jogo].astype(str).str.lower().str.contains(t2.lower())]) if t2 else 0
                
                pct_t1 = int((votos_t1 / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
                pct_draw = int((votos_draw / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
                pct_t2 = int((votos_t2 / total_votos_jogo) * 100) if total_votos_jogo > 0 else 0
                
                st.markdown(textwrap.dedent(f"""
                    <div class="poll-card">
                        <div class="poll-header">🎯 Enquete de Opinião</div>
                        <div class="poll-teams">
                            <div class="poll-team-box">
                                <span class="poll-team-flag">{emojis_t1}</span>
                                <span class="poll-team-name">{t1}</span>
                            </div>
                            <span class="poll-vs">VS</span>
                            <div class="poll-team-box">
                                <span class="poll-team-flag">{emojis_t2}</span>
                                <span class="poll-team-name">{t2}</span>
                            </div>
                        </div>
                        
                        <div class="poll-bar-container">
                            <div class="poll-bar-label"><span>{t1} Vence ({pct_t1}%)</span><span>{votos_t1} votos</span></div>
                            <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-m" style="width: {pct_t1}%;"></div></div>
                        </div>
                        <div class="poll-bar-container">
                            <div class="poll-bar-label"><span>Empate ({pct_draw}%)</span><span>{votos_draw} votos</span></div>
                            <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-draw" style="width: {pct_draw}%;"></div></div>
                        </div>
                        <div class="poll-bar-container" style="margin-bottom: 20px;">
                            <div class="poll-bar-label"><span>{t2} Vence ({pct_t2}%)</span><span>{votos_t2} votos</span></div>
                            <div class="poll-bar-outer"><div class="poll-bar-inner bar-color-v" style="width: {pct_t2}%;"></div></div>
                        </div>
                    </div>
                """), unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button(f"Vitória do {t1}", key=f"v_t1_{col_jogo}"):
                        if gravacao_bloqueada:
                            st.success(f"🎉 Voto simulado para o {t1}! (Ative o Apps Script para gravar real)")
                            st.balloons()
                        else:
                            payload = {
                                "email": email_user,
                                "nome": nome_user,
                                "id_jogo": col_jogo,
                                "palpite": f"Vitória do {t1}"
                            }
                            try:
                                response = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                if response.status_code == 200:
                                    st.success(f"Voto computado!")
                                    st.balloons()
                                    st.cache_data.clear()
                                    st.rerun()
                            except Exception:
                                st.error("Erro de conexão.")
                                
                with col_btn2:
                    if st.button("🤝 Empate", key=f"v_draw_{col_jogo}"):
                        if gravacao_bloqueada:
                            st.success("🤝 Empate simulado! (Ative o Apps Script para gravar real)")
                            st.balloons()
                        else:
                            payload = {
                                "email": email_user,
                                "nome": nome_user,
                                "id_jogo": col_jogo,
                                "palpite": "🤝 Empate"
                            }
                            try:
                                response = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                if response.status_code == 200:
                                    st.success("Voto para Empate computado!")
                                    st.balloons()
                                    st.cache_data.clear()
                                    st.rerun()
                            except Exception:
                                st.error("Erro de conexão.")
                                
                with col_btn3:
                    if st.button(f"Vitória do {t2}", key=f"v_t2_{col_jogo}"):
                        if gravacao_bloqueada:
                            st.success(f"🎉 Voto simulado para o {t2}! (Ative o Apps Script para gravar real)")
                            st.balloons()
                        else:
                            payload = {
                                "email": email_user,
                                "nome": nome_user,
                                "id_jogo": col_jogo,
                                "palpite": f"Vitória do {t2}"
                            }
                            try:
                                response = requests.post(URL_APPS_SCRIPT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                                if response.status_code == 200:
                                    st.success(f"Voto computado!")
                                    st.balloons()
                                    st.cache_data.clear()
                                    st.rerun()
                            except Exception:
                                st.error("Erro de conexão.")
                st.markdown("<br>", unsafe_allow_html=True)

    with tab_palpites:
        st.write("<h3 style='font-weight: 700; color: #004b23; margin-top: 10px;'>Consulta de Participante</h3>", unsafe_allow_html=True)
        usuarios_nomes_map = {email: obter_nome_exibicao(email) for email in df_respostas_consolidadas[col_email].unique()}
        usuarios_ordenados = sorted(usuarios_nomes_map.items(), key=lambda item: item[1])
        
        usuario_email_selecionado = st.selectbox(
            "Selecione um participante:", 
            options=[item[0] for item in usuarios_ordenados], 
            format_func=lambda x: usuarios_nomes_map[x],
            key="consulta_email"
        )
        
        if usuario_email_selecionado:
            palpites_user = df_respostas_consolidadas[df_respostas_consolidadas[col_email] == usuario_email_selecionado].iloc[0]
            for col_name in df_respostas.columns:
                if "vs" in col_name.lower() or "⚽" in col_name:
                    palpite_val = palpites_user[col_name]
                    if pd.isna(palpite_val) or str(palpite_val).strip().lower() in ['nan', 'none', '']:
                        continue
                    
                    partes = col_name.split('vs') if 'vs' in col_name.lower() else col_name.split('VS')
                    t1 = formatar_nome_time(partes[0])
                    t2 = formatar_nome_time(partes[1]) if len(partes) > 1 else ""
                    emojis_t1 = obter_emojis_pais(t1)
                    emojis_t2 = obter_emojis_pais(t2)
                    
                    st.markdown(textwrap.dedent(f"""
                        <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #e8efe9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <p style="font-weight: 700; color: #1e293b; margin: 0; font-size: 0.95rem;">{emojis_t1} {t1} vs {t2} {emojis_t2}</p>
                                <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #003566; font-weight:600;">Palpite: <strong style="color: #004b23;">{palpite_val}</strong></p>
                            </div>
                        </div>
                    """), unsafe_allow_html=True)

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
                
                emojis1 = obter_emojis_pais(time1)
                emojis2 = obter_emojis_pais(time2)
                
                st.markdown(textwrap.dedent(f"""
                    <div style="background-color: white; padding: 18px; border-radius: 14px; border: 1px solid #e8efe9; margin-bottom: 12px; display: flex; flex-direction: column; gap: 8px;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: bold; color: #475569;">
                            <span>⚽ Copa 2026</span>
                            <span>{badge_label}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0;">
                            <div style="display: flex; align-items: center; gap: 8px; width: 35%;">
                                <span>{emojis1}</span>
                                <span style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">{time1}</span>
                            </div>
                            <div style="font-size: 1.2rem; font-weight: 800; color: #004b23; width: 30%; text-align: center;">
                                {p_m_display if tem_placar else ""} VS {p_v_display if tem_placar else ""}
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px; width: 35%; justify-content: flex-end; text-align: right;">
                                <span style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">{time2}</span>
                                <span>{emojis2}</span>
                            </div>
                        </div>
                    </div>
                """), unsafe_allow_html=True)
else:
    st.markdown(textwrap.dedent("""
        <div class="custom-info" style="text-align: center; padding: 30px;">
            <p style="font-size: 2.5rem; margin: 0 0 15px 0;">🏆</p>
            <p style="font-weight: 700; font-size: 1.2rem; margin: 0 0 10px 0; color: #004b23;">Bem-vindo ao Bolão Feltrim Correa!</p>
            <p style="margin: 0; color: #003566;">Por favor, insira o ID correto da sua planilha no Painel Admin abaixo para sincronizar as respostas de palpites e placares reais!</p>
        </div>
    """), unsafe_allow_html=True)

st.markdown("---")
with st.expander("🛠️ Painel de Controle do Administrador"):
    senha_admin = st.text_input("Insira a senha do Administrador:", type="password", key="senha_admin")
    if senha_admin == "feltrim2026":
        st.success("Acesso de Administrador Autorizado!")
        
        novo_sheet_id = st.text_input(
            "ID da Planilha do Google Sheets:", 
            value=st.session_state["sheet_id"],
            help="O ID é a sequência de letras e números que fica na URL da sua planilha."
        )
        
        if novo_sheet_id != st.session_state["sheet_id"]:
            st.session_state["sheet_id"] = novo_sheet_id
            st.cache_data.clear()
            st.rerun()
            
        st.write("### Status de Configuração")
        st.write(f"**URL do Apps Script Cadastrada:** `{'Configurada' if not gravacao_bloqueada else 'Pendente (Edite o código em app_bolao.py)'}`")
        st.write(f"**Aba Palpites (Form Responses 2) encontrada:** `{'Sim' if df_respostas is not None else 'Não'}`")
        st.write(f"**Aba Resultados Oficiais encontrada:** `{'Sim' if df_resultados_raw is not None else 'Usando Fallback'}`")
    elif senha_admin:
        st.error("Senha incorreta!")

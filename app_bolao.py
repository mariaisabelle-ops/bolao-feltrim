import streamlit as st
import pandas as pd
import requests
import json
import re

# LISTA OFICIAL CRONOLÓGICA DE 72 JOGOS DA COPA DO MUNDO FIFA 2026 (FASE DE GRUPOS)
# Todos os horários e datas estão baseados estritamente no fuso de Brasília (UTC-3).
JOGOS_CADASTRADOS = [
    # --- 11/06 ---
    {"ID_Jogo": "JOGO_01", "Jogo": "⚽ México vs África do Sul (11/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_02", "Jogo": "⚽ Coreia do Sul vs Tchéquia (11/06)", "Horário": "22:00"},

    # --- 12/06 ---
    {"ID_Jogo": "JOGO_03", "Jogo": "⚽ Canadá vs Bósnia e Herzegovina (12/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_04", "Jogo": "⚽ Estados Unidos vs Paraguai (12/06)", "Horário": "21:00"},

    # --- 13/06 ---
    {"ID_Jogo": "JOGO_05", "Jogo": "⚽ Catar vs Suíça (13/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_06", "Jogo": "⚽ Brasil vs Marrocos (13/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_07", "Jogo": "⚽ Haiti vs Escócia (13/06)", "Horário": "21:00"},

    # --- 14/06 ---
    {"ID_Jogo": "JOGO_08", "Jogo": "⚽ Austrália vs Turquia (14/06)", "Horário": "00:00"},
    {"ID_Jogo": "JOGO_09", "Jogo": "⚽ Alemanha vs Curaçao (14/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_10", "Jogo": "⚽ Holanda vs Japão (14/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_11", "Jogo": "⚽ Costa do Marfim vs Equador (14/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_12", "Jogo": "⚽ Suécia vs Tunísia (14/06)", "Horário": "22:00"},

    # --- 15/06 ---
    {"ID_Jogo": "JOGO_13", "Jogo": "⚽ Espanha vs Cabo Verde (15/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_14", "Jogo": "⚽ Bélgica vs Egito (15/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_15", "Jogo": "⚽ Arábia Saudita vs Uruguai (15/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_16", "Jogo": "⚽ Irã vs Nova Zelândia (15/06)", "Horário": "21:00"},

    # --- 16/06 ---
    {"ID_Jogo": "JOGO_17", "Jogo": "⚽ França vs Senegal (16/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_18", "Jogo": "⚽ Iraque vs Noruega (16/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_19", "Jogo": "⚽ Argentina vs Argélia (16/06)", "Horário": "21:00"},

    # --- 17/06 ---
    {"ID_Jogo": "JOGO_20", "Jogo": "⚽ Áustria vs Jordânia (17/06)", "Horário": "00:00"},
    {"ID_Jogo": "JOGO_21", "Jogo": "⚽ Portugal vs RD Congo (17/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_22", "Jogo": "⚽ Inglaterra vs Croácia (17/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_23", "Jogo": "⚽ Gana vs Panamá (17/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_24", "Jogo": "⚽ Uzbequistão vs Colômbia (17/06)", "Horário": "22:00"},

    # --- 18/06 ---
    {"ID_Jogo": "JOGO_25", "Jogo": "⚽ Tchéquia vs África do Sul (18/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_26", "Jogo": "⚽ Suíça vs Bósnia e Herzegovina (18/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_27", "Jogo": "⚽ Canadá vs Catar (18/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_28", "Jogo": "⚽ México vs Coreia do Sul (18/06)", "Horário": "21:00"},

    # --- 19/06 ---
    {"ID_Jogo": "JOGO_29", "Jogo": "⚽ Estados Unidos vs Austrália (19/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_30", "Jogo": "⚽ Escócia vs Marrocos (19/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_31", "Jogo": "⚽ Brasil vs Haiti (19/06)", "Horário": "21:30"},
    {"ID_Jogo": "JOGO_32", "Jogo": "⚽ Turquia vs Paraguai (19/06)", "Horário": "23:00"},

    # --- 20/06 ---
    {"ID_Jogo": "JOGO_33", "Jogo": "⚽ Holanda vs Suécia (20/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_34", "Jogo": "⚽ Alemanha vs Costa do Marfim (20/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_35", "Jogo": "⚽ Equador vs Curaçao (20/06)", "Horário": "20:00"},

    # --- 21/06 ---
    {"ID_Jogo": "JOGO_36", "Jogo": "⚽ Tunísia vs Japão (21/06)", "Horário": "00:00"},
    {"ID_Jogo": "JOGO_37", "Jogo": "⚽ Espanha vs Arábia Saudita (21/06)", "Horário": "12:00"},
    {"ID_Jogo": "JOGO_38", "Jogo": "⚽ Bélgica vs Irã (21/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_39", "Jogo": "⚽ Uruguai vs Cabo Verde (21/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_40", "Jogo": "⚽ Nova Zelândia vs Egito (21/06)", "Horário": "21:00"},

    # --- 22/06 ---
    {"ID_Jogo": "JOGO_41", "Jogo": "⚽ Argentina vs Áustria (22/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_42", "Jogo": "⚽ França vs Iraque (22/06)", "Horário": "17:00"},
    {"ID_Jogo": "JOGO_43", "Jogo": "⚽ Noruega vs Senegal (22/06)", "Horário": "20:00"},
    {"ID_Jogo": "JOGO_44", "Jogo": "⚽ Jordânia vs Argélia (22/06)", "Horário": "23:00"},

    # --- 23/06 ---
    {"ID_Jogo": "JOGO_45", "Jogo": "⚽ Portugal vs Uzbequistão (23/06)", "Horário": "13:00"},
    {"ID_Jogo": "JOGO_46", "Jogo": "⚽ Inglaterra vs Gana (23/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_47", "Jogo": "⚽ Panamá vs Croácia (23/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_48", "Jogo": "⚽ Colômbia vs RD Congo (23/06)", "Horário": "22:00"},

    # --- 24/06 ---
    {"ID_Jogo": "JOGO_49", "Jogo": "⚽ Suíça vs Canadá (24/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_50", "Jogo": "⚽ Bósnia e Herzegovina vs Catar (24/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_51", "Jogo": "⚽ Escócia vs Brasil (24/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_52", "Jogo": "⚽ Marrocos vs Haiti (24/06)", "Horário": "18:00"},
    {"ID_Jogo": "JOGO_53", "Jogo": "⚽ Tchéquia vs México (24/06)", "Horário": "21:00"},
    {"ID_Jogo": "JOGO_54", "Jogo": "⚽ África do Sul vs Coreia do Sul (24/06)", "Horário": "21:00"},

    # --- 25/06 ---
    {"ID_Jogo": "JOGO_55", "Jogo": "⚽ Equador vs Alemanha (25/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_56", "Jogo": "⚽ Curaçao vs Costa do Marfim (25/06)", "Horário": "16:00"},
    {"ID_Jogo": "JOGO_57", "Jogo": "⚽ Tunísia vs Holanda (25/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_58", "Jogo": "⚽ Japão vs Suécia (25/06)", "Horário": "19:00"},
    {"ID_Jogo": "JOGO_59", "Jogo": "⚽ Turquia vs Estados Unidos (25/06)", "Horário": "22:00"},
    {"ID_Jogo": "JOGO_60", "Jogo": "⚽ Paraguai vs Austrália (25/06)", "Horário": "22:00"},

    # --- 26/06 ---
    {"ID_Jogo": "JOGO_61", "Jogo": "⚽ Noruega vs França (26/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_62", "Jogo": "⚽ Senegal vs Iraque (26/06)", "Horário": "15:00"},
    {"ID_Jogo": "JOGO_63", "Jogo": "⚽ Uruguai vs Espanha (26/06)", "Horário": "20:00"},
    {"ID_Jogo": "JOGO_64", "Jogo": "⚽ Cabo Verde vs Arábia Saudita (26/06)", "Horário": "20:00"},
    {"ID_Jogo": "JOGO_65", "Jogo": "⚽ Nova Zelândia vs Bélgica (26/06)", "Horário": "23:00"},
    {"ID_Jogo": "JOGO_66", "Jogo": "⚽ Egito vs Irã (26/06)", "Horário": "23:00"},

    # --- 27/06 ---
    {"ID_Jogo": "JOGO_67", "Jogo": "⚽ Panamá vs Inglaterra (27/06)", "Horário": "17:00"},
    {"ID_Jogo": "JOGO_68", "Jogo": "⚽ Croácia vs Gana (27/06)", "Horário": "17:00"},
    {"ID_Jogo": "JOGO_69", "Jogo": "⚽ Colômbia vs Portugal (27/06)", "Horário": "19:30"},
    {"ID_Jogo": "JOGO_70", "Jogo": "⚽ RD Congo vs Uzbequistão (27/06)", "Horário": "19:30"},
    {"ID_Jogo": "JOGO_71", "Jogo": "⚽ Jordânia vs Argentina (27/06)", "Horário": "22:00"},
    {"ID_Jogo": "JOGO_72", "Jogo": "⚽ Argélia vs Áustria (27/06)", "Horário": "22:00"}
]

st.set_page_config(
    page_title="Feltrim Correa - Bolão Copa 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de estados globais de conexão
if "spreadsheet_id" not in st.session_state:
    st.session_state.spreadsheet_id = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"
if "web_app_url" not in st.session_state:
    st.session_state.web_app_url = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"

# Estilos CSS unificados para um layout corporativo limpo e premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebar"] {
        font-family: 'Montserrat', sans-serif;
    }
    .main-title {
        font-weight: 700;
        font-size: 2.3rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        text-align: center;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.8rem;
    }
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
    }
    .podium-1 {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #111;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    .podium-2 {
        background: linear-gradient(135deg, #C0C0C0 0%, #A9A9A9 100%);
        color: #111;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(192, 192, 192, 0.3);
    }
    .podium-3 {
        background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(205, 127, 50, 0.3);
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/120/cup.png", width=65)
    st.markdown("### 🏆 Feltrim Correa")
    st.markdown("Bolão Corporativo Oficial")
    st.markdown("---")
    
    aba_selecionada = st.radio(
        "Menu de Opções",
        ["📊 Tabela de Classificação", "📝 Fazer Palpite", "🔧 Portal Admin"]
    )
    
    st.markdown("---")
    st.markdown("<small>Versão Premium V2.5</small>", unsafe_allow_html=True)

def carregar_dados_planilha(sheet_id):
    try:
        url_palpites = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Palpites"
        df_palpites = pd.read_csv(url_palpites)
        
        url_resultados = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Resultados+Oficiais"
        df_resultados = pd.read_csv(url_resultados)
        
        return df_palpites, df_resultados
    except Exception:
        return None, None

def calcular_ranking_real(df_palpites, df_resultados):
    if df_palpites is None or df_resultados is None or df_palpites.empty or df_resultados.empty:
        return pd.DataFrame()
        
    resultado_map = {}
    for _, row in df_resultados.iterrows():
        jogo_id = str(row["ID_Jogo"]).strip()
        try:
            m = int(row["Placar Real Mandante"])
            v = int(row["Placar Real Visitante"])
            status = str(row["Status"]).strip()
            resultado_map[jogo_id] = {"m": m, "v": v, "status": status}
        except Exception:
            continue
            
    pontuacao = {}
    cols = list(df_palpites.columns)
    email_col = None
    nome_col = None
    
    for c in cols:
        lc = c.lower().strip()
        if "email" in lc or "e-mail" in lc or "usuário" in lc:
            email_col = c
        if "nome" in lc:
            nome_col = c
            
    if not email_col:
        return pd.DataFrame()
        
    for _, row in df_palpites.iterrows():
        email = str(row[email_col]).strip()
        nome = str(row[nome_col]).strip() if nome_col else email
        
        if not email or email == "nan":
            continue
            
        if email not in pontuacao:
            pontuacao[email] = {"Nome": nome, "Pontos": 0, "Acertos Exatos": 0, "Acertos Vencedor": 0, "Palpites Feitos": 0}
            
        for jogo in JOGOS_CADASTRADOS:
            nome_jogo = jogo["Jogo"]
            jogo_id = jogo["ID_Jogo"]
            
            if nome_jogo in df_palpites.columns:
                palpite = str(row[nome_jogo]).strip()
                if palpite and palpite != "nan" and "-" in palpite:
                    pontuacao[email]["Palpites Feitos"] += 1
                    
                    if jogo_id in resultado_map and "Encerrado" in resultado_map[jogo_id]["status"]:
                        res_real = resultado_map[jogo_id]
                        try:
                            parts = palpite.split("-")
                            pm = int(parts[0].strip())
                            pv = int(parts[1].strip())
                            rm = res_real["m"]
                            rv = res_real["v"]
                            
                            if pm == rm and pv == rv:
                                pontuacao[email]["Pontos"] += 10
                                pontuacao[email]["Acertos Exatos"] += 1
                            elif (pm > pv and rm > rv) or (pm < pv and rm < rv) or (pm == pv and rm == rv):
                                pontuacao[email]["Pontos"] += 5
                                pontuacao[email]["Acertos Vencedor"] += 1
                        except Exception:
                            pass
                            
    ranking_df = pd.DataFrame(pontuacao.values())
    if not ranking_df.empty:
        ranking_df = ranking_df.sort_values(by=["Pontos", "Acertos Exatos", "Nome"], ascending=[False, False, True])
        ranking_df.insert(0, "Posição", range(1, len(ranking_df) + 1))
        
    return ranking_df

# Carregamento prévio dos dados
df_p, df_r = carregar_dados_planilha(st.session_state.spreadsheet_id)

if aba_selecionada == "📊 Tabela de Classificação":
    st.markdown('<div class="main-title">🏆 Feltrim Correa - Classificação</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Acompanhe a sua pontuação e pódio do Bolão em tempo real</div>', unsafe_allow_html=True)
    
    if df_p is not None and df_r is not None:
        rank = calcular_ranking_real(df_p, df_r)
        
        if not rank.empty:
            st.markdown("### 🥇 Os Três Líderes do Pódio")
            col1, col2, col3 = st.columns(3)
            
            if len(rank) >= 1:
                with col1:
                    st.markdown(f"""
                    <div class="podium-1">
                        <div style="font-size: 2.0rem;">🥇 1º Lugar</div>
                        <div style="font-size: 1.25rem; margin-top:0.4rem;">{rank.iloc[0]['Nome']}</div>
                        <div style="font-size: 1.7rem; margin-top:0.3rem;">{rank.iloc[0]['Pontos']} Pts</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            if len(rank) >= 2:
                with col2:
                    st.markdown(f"""
                    <div class="podium-2">
                        <div style="font-size: 1.8rem;">🥈 2º Lugar</div>
                        <div style="font-size: 1.15rem; margin-top:0.4rem;">{rank.iloc[1]['Nome']}</div>
                        <div style="font-size: 1.5rem; margin-top:0.3rem;">{rank.iloc[1]['Pontos']} Pts</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with col2:
                    st.markdown('<div class="card" style="text-align:center;">Vago</div>', unsafe_allow_html=True)
                    
            if len(rank) >= 3:
                with col3:
                    st.markdown(f"""
                    <div class="podium-3">
                        <div style="font-size: 1.6rem;">🥉 3º Lugar</div>
                        <div style="font-size: 1.05rem; margin-top:0.4rem;">{rank.iloc[2]['Nome']}</div>
                        <div style="font-size: 1.35rem; margin-top:0.3rem;">{rank.iloc[2]['Pontos']} Pts</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                with col3:
                    st.markdown('<div class="card" style="text-align:center;">Vago</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📊 Classificação Completa")
            st.dataframe(rank, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum palpite cadastrado ainda! Comece enviando os palpites na aba ao lado.")
    else:
        st.warning("""
        ### Planilha Desconectada ou em Branco!
        Mensagem Técnica: Planilha vazia ou com abas não configuradas.
        
        Como resolver de forma instantânea em 2 passos:
        1. Confirme se as abas estão devidamente criadas no seu Google Sheets.
        2. Vá na aba **Portal Admin** usando a sua senha de acesso administrativo para salvar as configurações!
        """)

elif aba_selecionada == "📝 Fazer Palpite":
    st.markdown('<div class="main-title">📝 Enviar Meus Palpites</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Registre os seus resultados para a fase de grupos do torneio</div>', unsafe_allow_html=True)
    
    with st.form("form_palpites"):
        st.markdown("#### 👤 Seus Dados de Identificação")
        c1, c2 = st.columns(2)
        with c1:
            nome_user = st.text_input("Nome Completo", placeholder="Ex: João Silva")
        with c2:
            email_user = st.text_input("E-mail Corporativo", placeholder="Ex: joao.silva@feltrim.com")
            
        st.markdown("---")
        st.markdown("#### ⚽ Seu Palpite Real")
        
        jogo_selecionado = st.selectbox(
            "Selecione a partida que deseja palpitar:",
            options=[j["Jogo"] for j in JOGOS_CADASTRADOS]
        )
        
        col_m, col_div, col_v = st.columns([2, 1, 2])
        with col_m:
            gols_m = st.number_input("Mandante", min_value=0, max_value=25, value=0, step=1)
        with col_div:
            st.markdown("<h3 style='text-align: center; margin-top: 1.5rem;'>x</h3>", unsafe_allow_html=True)
        with col_v:
            gols_v = st.number_input("Visitante", min_value=0, max_value=25, value=0, step=1)
            
        st.markdown("<br>", unsafe_allow_html=True)
        submetido = st.form_submit_button("🚀 Enviar Meu Voto")
        
        if submetido:
            if not nome_user or not email_user:
                st.error("Por favor, preencha o seu nome e e-mail para validar o seu palpite!")
            elif "@" not in email_user or "." not in email_user:
                st.error("E-mail num formato inválido! Verifique a digitação.")
            else:
                match = next((item for item in JOGOS_CADASTRADOS if item["Jogo"] == jogo_selecionado), None)
                if match:
                    payload = {
                        "action": "fazerPalpite",
                        "spreadsheet_id": st.session_state.spreadsheet_id,
                        "email": email_user.strip(),
                        "nome": nome_user.strip(),
                        "id_jogo": match["ID_Jogo"],
                        "palpite": f"{gols_m}-{gols_v}"
                    }
                    try:
                        resp = requests.post(
                            st.session_state.web_app_url,
                            data=json.dumps(payload),
                            headers={"Content-Type": "application/json"}
                        )
                        dados_api = resp.json()
                        if dados_api.get("status") == "success":
                            st.success(f"Excelente! Palpite de {gols_m} x {gols_v} para o jogo '{jogo_selecionado}' enviado com sucesso!")
                        else:
                            st.error(f"Erro ao gravar na planilha: {dados_api.get('message')}")
                    except Exception as ex:
                        st.error(f"Erro ao conectar com a API: {str(ex)}")

elif aba_selecionada == "🔧 Portal Admin":
    st.markdown('<div class="main-title">🔧 Portal do Administrador</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Configurações globais e cadastro de resultados oficiais</div>', unsafe_allow_html=True)
    
    senha_digitada = st.text_input("Senha de Acesso Administrativo", type="password")
    
    if senha_digitada == "feltrim2026":
        st.success("Acesso administrativo autenticado com sucesso!")
        
        st.markdown("### 🔗 Configurações de Conexão com o Google Sheets")
        with st.expander("Alterar ID da Planilha ou URL da API do Apps Script"):
            novo_id = st.text_input("ID do Google Sheets", value=st.session_state.spreadsheet_id)
            nova_url = st.text_input("URL do App da Web (Apps Script)", value=st.session_state.web_app_url)
            
            if st.button("💾 Salvar Configurações de Conexão"):
                st.session_state.spreadsheet_id = novo_id
                st.session_state.web_app_url = nova_url
                st.success("Configurações atualizadas localmente!")
                st.rerun()

        st.markdown("### 🧪 Diagnóstico de Conexão")
        if st.button("Executar Testes de Conexão"):
            with st.spinner("Testando conexão..."):
                try:
                    payload = {"action": "testPing", "spreadsheet_id": st.session_state.spreadsheet_id}
                    r = requests.post(
                        st.session_state.web_app_url,
                        data=json.dumps(payload),
                        headers={"Content-Type": "application/json"}
                    )
                    if r.status_code == 200:
                        st.json(r.json())
                        st.success("Conexão bem-sucedida com a API do Google!")
                    else:
                        st.error(f"Falha de Comunicação. Código do Servidor: {r.status_code}")
                except Exception as ex:
                    st.error(f"Erro na requisição: {str(ex)}")

        st.markdown("---")
        st.markdown("### ⚽ Lançar Resultados Reais e Alterar Status")
        
        with st.form("form_admin_placar"):
            jogo_adm = st.selectbox("Selecione a partida para atualizar:", options=[j["Jogo"] for j in JOGOS_CADASTRADOS])
            status_adm = st.selectbox("Novo Status do Jogo", ["🕒 Agendado", "🟡 Em Andamento", "🟢 Encerrado"])
            
            c1, c2 = st.columns(2)
            with c1:
                g_m = st.number_input("Gols do Mandante Oficial", min_value=0, max_value=25, value=0, step=1)
            with c2:
                g_v = st.number_input("Gols do Visitante Oficial", min_value=0, max_value=25, value=0, step=1)
                
            bt_placar = st.form_submit_button("💾 Salvar Placar Oficial")
            
            if bt_placar:
                placar_payload = {
                    "action": "atualizarPlacar",
                    "spreadsheet_id": st.session_state.spreadsheet_id,
                    "senha": "feltrim2026",
                    "jogo": jogo_adm,
                    "placar_m": int(g_m),
                    "placar_v": int(g_v),
                    "status": status_adm
                }
                try:
                    r = requests.post(
                        st.session_state.web_app_url,
                        data=json.dumps(placar_payload),
                        headers={"Content-Type": "application/json"}
                    )
                    ret_api = r.json()
                    if ret_api.get("status") == "success":
                        st.success("Placar e status atualizados com sucesso na planilha!")
                    else:
                        st.error(f"Erro na gravação: {ret_api.get('message')}")
                except Exception as ex:
                    st.error(f"Erro de conexão com o script Google: {str(ex)}")
                    
        st.markdown("---")
        st.markdown("### ⚠️ Zona de Risco")
        
        if st.button("🚀 Inicializar Todos os 72 Jogos na Planilha"):
            with st.spinner("Gerando planilhas e limpando dados antigos..."):
                init_payload = {
                    "action": "inicializarNovoBolao",
                    "spreadsheet_id": st.session_state.spreadsheet_id,
                    "senha": "feltrim2026"
                }
                try:
                    r = requests.post(
                        st.session_state.web_app_url,
                        data=json.dumps(init_payload),
                        headers={"Content-Type": "application/json"}
                    )
                    res_init = r.json()
                    if res_init.get("status") == "success":
                        st.success("Planilha configurada com sucesso com todos os 72 jogos oficiais!")
                    else:
                        st.error(f"Erro ao inicializar: {res_init.get('message')}")
                except Exception as ex:
                    st.error(f"Erro ao inicializar a planilha: {str(ex)}")
    elif senha_digitada:
        st.error("Senha incorreta! Acesso restrito apenas ao administrador do bolão.")
```
eof

### 🏆 Conclusão & Próximos Passos:
O código do **`app_bolao.py`** foi totalmente saneado e está livre de qualquer bug de indentação ou caractere incorreto!

1. Substitua o código no seu repositório do **GitHub**.
2. O Streamlit Cloud irá detectar o commit e reiniciar a aplicação instantaneamente.
3. Se o site avisar que a planilha não está carregada, use a senha `feltrim2026` na aba **Portal Admin**, cole a sua URL do Apps Script e clique no botão **"🚀 Inicializar Todos os 72 Jogos na Planilha"** para recriar as tabelas oficiais de forma limpa e com as datas reais de transmissão!

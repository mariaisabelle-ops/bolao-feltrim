import streamlit as st
import pandas as pd
import requests
import io
import re

st.set_page_config(
    page_title="Feltrim Correa - Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constantes globais
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"

# Design System Premium (Verde Corporativo Feltrim & Destaques Ouro)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #fcfdfe;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #004b23;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #556b2f;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Menu de Navegação Horizontal Customizado */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 2rem;
        padding: 8px;
        background-color: #f1f7f3;
        border-radius: 50px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
    }
    
    .nav-btn {
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #38b000;
        background: transparent;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    /* Cards de Estatísticas */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e1e7e3;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,75,35,0.02);
    }
    
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #004b23;
        margin-bottom: 5px;
    }
    
    .metric-lbl {
        font-size: 0.85rem;
        color: #708090;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Layout do Pódio de Líderes */
    .podium-container {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 20px;
        margin: 3rem 0;
        padding-top: 20px;
    }
    
    .podium-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 180px;
    }
    
    .podium-card {
        width: 100%;
        background: #ffffff;
        border-radius: 16px 16px 8px 8px;
        text-align: center;
        padding: 20px 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .p-1st { height: 160px; border-top: 6px solid #ffd700; background: linear-gradient(180deg, #fffdf2 0%, #ffffff 100%); }
    .p-2nd { height: 130px; border-top: 6px solid #c0c0c0; background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%); }
    .p-3rd { height: 110px; border-top: 6px solid #cd7f32; background: linear-gradient(180deg, #fffbf7 0%, #ffffff 100%); }
    
    .avatar-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #004b23;
        color: white;
        font-size: 1.4rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,75,35,0.15);
    }
    
    /* Enquete Interativa de Voto */
    .match-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.01);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .match-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,75,35,0.04);
    }
</style>
""", unsafe_allowed_html=True)

if "spreadsheet_id" not in st.session_state:
    st.session_state.spreadsheet_id = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg" # Conectado à sua planilha nova

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "🏆 Classificação"

# Funções de Leitura Segura anti-Crash e Limpeza de Lixo
def safe_to_int(val):
    try:
        if pd.isna(val) or str(val).strip() == "" or str(val).lower() == "nan":
            return 0
        return int(float(val))
    except:
        return 0

def eh_nome_valido(nome):
    if not nome or not isinstance(nome, str):
        return False
    n_limpo = nome.strip().lower()
    if "vs" in n_limpo or "⚽" in n_limpo or "timestamp" in n_limpo or "@" in n_limpo:
        return False
    if len(nome.strip()) < 2:
        return False
    return True

def ler_aba_sheets(sheet_name):
    s_id = st.session_state.spreadsheet_id.strip()
    if not s_id:
        return pd.DataFrame()
    
    url = f"https://docs.google.com/spreadsheets/d/{s_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return pd.DataFrame()
        
        # Se Google Sheets retornou redirecionamento para login de privacidade
        if "<html" in response.text.lower() or "<!doctype" in response.text.lower():
            return "PRIVADO"
            
        df = pd.read_csv(io.StringIO(response.text))
        # Limpa espaços extras nos nomes de colunas
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

st.markdown('<h1 class="main-title">🏆 BOLÃO FELTRIM CORREA</h1>', unsafe_allowed_html=True)
st.markdown('<p class="subtitle">Acompanhe a classificação, registre seus palpites e dispute a liderança!</p>', unsafe_allowed_html=True)

# Menu de Abas Premium
tabs = ["🏆 Classificação", "📝 Dar Palpite", "🎯 Ver Palpites", "⚙️ Painel Admin"]
col_t1, col_t2, col_t3, col_t4 = st.columns(4)

with col_t1:
    if st.button("🏆 CLASSIFICAÇÃO", use_container_width=True, type="primary" if st.session_state.current_tab == "🏆 Classificação" else "secondary"):
        st.session_state.current_tab = "🏆 Classificação"
        st.rerun()
with col_t2:
    if st.button("📝 DAR PALPITE", use_container_width=True, type="primary" if st.session_state.current_tab == "📝 Dar Palpite" else "secondary"):
        st.session_state.current_tab = "📝 Dar Palpite"
        st.rerun()
with col_t3:
    if st.button("🎯 VER PALPITES", use_container_width=True, type="primary" if st.session_state.current_tab == "🎯 Ver Palpites" else "secondary"):
        st.session_state.current_tab = "🎯 Ver Palpites"
        st.rerun()
with col_t4:
    if st.button("⚙️ ADMINISTRADOR", use_container_width=True, type="primary" if st.session_state.current_tab == "⚙️ Painel Admin" else "secondary"):
        st.session_state.current_tab = "⚙️ Painel Admin"
        st.rerun()

st.markdown("<hr style='margin-top:0.5rem; margin-bottom:2rem; border-color:#e1e7e3;'>", unsafe_allowed_html=True)

# Carregamento seguro dos dados globais
df_classificacao = ler_aba_sheets("Classificacao")
df_resultados = ler_aba_sheets("Resultados")

if isinstance(df_classificacao, str) and df_classificacao == "PRIVADO":
    st.warning("⚠️ **Conexão com a Planilha Bloqueada!**")
    st.info("""
    Para que o site consiga puxar os dados, a sua nova planilha do Google precisa ser aberta para leitura na internet:
    
    1. Abra a sua planilha do Google Sheets.
    2. Clique no botão azul **Compartilhar** no canto superior direito.
    3. Em **Acesso Geral**, altere de **Restrito** para **"Qualquer pessoa com o link"**.
    4. Mantenha a permissão como **Leitor**.
    5. Volte aqui e clique no botão **🔄 Sincronizar Sistema** no Painel Admin ou atualize o navegador.
    """)
    st.stop()

# Se estiver vazia ou com falha genérica de carregamento
if df_classificacao is None or df_classificacao.empty:
    df_classificacao = pd.DataFrame(columns=["Posição", "Participante", "E-mail Corporativo", "Pontos Acumulados"])

if df_resultados is None or df_resultados.empty:
    df_resultados = pd.DataFrame(columns=["ID_Jogo", "Jogo", "Placar Real Mandante", "Placar Real Visitante", "Status"])

# Normalizações preventivas de dados
if "Pontos Acumulados" in df_classificacao.columns:
    df_classificacao["Pontos Acumulados"] = df_classificacao["Pontos Acumulados"].apply(safe_to_int)

# Filtro de Competidores Válidos na Classificação (Remove Jogos, Cabeçalhos e Lixo vazados no formulário)
if "Participante" in df_classificacao.columns:
    df_classificacao = df_classificacao[df_classificacao["Participante"].apply(eh_nome_valido)]

if st.session_state.current_tab == "🏆 Classificação":
    
    st.markdown("### 📊 Pódio e Classificação Geral")
    
    # KPIs Rápidos
    total_participantes = len(df_classificacao)
    lider_atual = "-"
    pontos_lider = 0
    media_pontos = 0
    
    if total_participantes > 0:
        df_classificacao_sorted = df_classificacao.sort_values(by="Pontos Acumulados", ascending=False)
        lider_atual = df_classificacao_sorted.iloc[0]["Participante"]
        pontos_lider = df_classificacao_sorted.iloc[0]["Pontos Acumulados"]
        media_pontos = round(df_classificacao_sorted["Pontos Acumulados"].mean(), 1)
        
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{total_participantes}</div><div class="metric-lbl">Participantes</div></div>', unsafe_allowed_html=True)
    with col_k2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">👑 {str(lider_atual)[:15]}</div><div class="metric-lbl">Líder ({pontos_lider} pts)</div></div>', unsafe_allowed_html=True)
    with col_k3:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{media_pontos} pts</div><div class="metric-lbl">Média Geral</div></div>', unsafe_allowed_html=True)
        
    # PÓDIO PREMIUM
    st.markdown("<br>", unsafe_allowed_html=True)
    
    p1_nome, p1_pts = "Aguardando", "0 pts"
    p2_nome, p2_pts = "Aguardando", "0 pts"
    p3_nome, p3_pts = "Aguardando", "0 pts"
    
    if total_participantes > 0:
        p1_nome = df_classificacao_sorted.iloc[0]["Participante"]
        p1_pts = f"{df_classificacao_sorted.iloc[0]['Pontos Acumulados']} pts"
    if total_participantes > 1:
        p2_nome = df_classificacao_sorted.iloc[1]["Participante"]
        p2_pts = f"{df_classificacao_sorted.iloc[1]['Pontos Acumulados']} pts"
    if total_participantes > 2:
        p3_nome = df_classificacao_sorted.iloc[2]["Participante"]
        p3_pts = f"{df_classificacao_sorted.iloc[2]['Pontos Acumulados']} pts"
        
    # Estrutura HTML do Pódio
    st.markdown(f"""
    <div class="podium-container">
        <div class="podium-col">
            <div style="font-size:1.8rem; margin-bottom:8px;">🥈</div>
            <div class="podium-card p-2nd">
                <div class="avatar-circle" style="background-color:#9ca3af;">{str(p2_nome)[0].upper()}</div>
                <div style="font-weight:600; font-size:0.95rem; color:#4b5563;">{str(p2_nome)[:20]}</div>
                <div style="font-weight:800; font-size:1.1rem; color:#1f2937; margin-top:5px;">{p2_pts}</div>
            </div>
        </div>
        <div class="podium-col">
            <div style="font-size:2.2rem; margin-bottom:8px;">👑</div>
            <div class="podium-card p-1st">
                <div class="avatar-circle" style="background-color:#d97706; width:60px; height:60px; font-size:1.6rem;">{str(p1_nome)[0].upper()}</div>
                <div style="font-weight:800; font-size:1.05rem; color:#1e1b4b;">{str(p1_nome)[:20]}</div>
                <div style="font-weight:800; font-size:1.3rem; color:#b45309; margin-top:5px;">{p1_pts}</div>
            </div>
        </div>
        <div class="podium-col">
            <div style="font-size:1.7rem; margin-bottom:8px;">🥉</div>
            <div class="podium-card p-3rd">
                <div class="avatar-circle" style="background-color:#b45309;">{str(p3_nome)[0].upper()}</div>
                <div style="font-weight:600; font-size:0.95rem; color:#78350f;">{str(p3_nome)[:20]}</div>
                <div style="font-weight:800; font-size:1.1rem; color:#451a03; margin-top:5px;">{p3_pts}</div>
            </div>
        </div>
    </div>
    """, unsafe_allowed_html=True)
    
    # Tabela Completa de Classificação
    if total_participantes > 0:
        st.markdown("#### Lista de Classificação Geral")
        st.dataframe(
            df_classificacao_sorted[["Participante", "E-mail Corporativo", "Pontos Acumulados"]].reset_index(drop=True),
            use_container_width=True,
            column_config={
                "Participante": st.column_config.TextColumn("Participante"),
                "E-mail Corporativo": st.column_config.TextColumn("E-mail Corporativo"),
                "Pontos Acumulados": st.column_config.NumberColumn("Pontuação Total", format="%d pts")
            }
        )
    else:
        st.info("Nenhum palpite foi processado até o momento. Aguardando finalização dos jogos!")

elif st.session_state.current_tab == "📝 Dar Palpite":
    st.markdown("### 📝 Dar Palpite na Partida")
    
    # Filtra jogos que estão marcados estritamente como "🕒 Agendado"
    if not df_resultados.empty and "Status" in df_resultados.columns:
        jogos_voto = df_resultados[df_resultados["Status"].str.contains("Agendado", na=False)]
    else:
        jogos_voto = pd.DataFrame()
        
    if jogos_voto.empty:
        st.success("🎉 Todos os jogos cadastrados já começaram, foram encerrados ou estão indisponíveis para palpites!")
    else:
        st.markdown("Selecione abaixo o seu nome, e-mail corporativo e registre o seu palpite para cada partida agendada:")
        
        # Form de Dados do Participante
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            nome_user = st.text_input("Qual o seu nome completo?", key="voto_nome").strip()
        with col_f2:
            email_user = st.text_input("Qual o seu e-mail corporativo?", key="voto_email").strip()
            
        st.markdown("<br>", unsafe_allowed_html=True)
        
        # Listagem de Enquetes Ativas
        for idx, row in jogos_voto.iterrows():
            jogo_id = row["ID_Jogo"]
            jogo_nome = row["Jogo"]
            
            # Limpa o nome do jogo tirando o emoji
            jogo_exibir = re.sub(r'⚽\s*', '', str(jogo_nome))
            
            # Divide os times mandante e visitante
            partes_times = jogo_exibir.split("vs")
            time_m = partes_times[0].strip() if len(partes_times) > 0 else "Mandante"
            time_v = partes_times[1].strip() if len(partes_times) > 1 else "Visitante"
            
            st.markdown(f"""
            <div class="match-box">
                <div style="font-weight:800; font-size:1.15rem; color:#004b23; margin-bottom:15px; text-align:center;">{jogo_exibir}</div>
            </div>
            """, unsafe_allowed_html=True)
            
            voto_selecionado = st.radio(
                "Quem vencerá esta partida?",
                options=[f"Vitória do {time_m}", "Empate", f"Vitória do {time_v}"],
                key=f"voto_radio_{jogo_id}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            # Botão individual de Envio
            if st.button(f"Enviar Palpite: {time_m} vs {time_v}", key=f"btn_voto_{jogo_id}"):
                if not nome_user or not email_user or "@" not in email_user:
                    st.error("⚠️ Preencha seu nome e um e-mail corporativo válido antes de palpitar!")
                elif not eh_nome_valido(nome_user):
                    st.error("⚠️ Digite um nome de participante real e válido!")
                else:
                    with st.spinner("Registrando palpite na planilha..."):
                        payload = {
                            "action": "fazerPalpite",
                            "nome": nome_user,
                            "email": email_user,
                            "id_jogo": jogo_nome,
                            "palpite": voto_selecionado
                        }
                        try:
                            res = requests.post(URL_APPS_SCRIPT, json=payload, timeout=15)
                            if res.status_code == 200:
                                st.success(f"⚽ Palpite enviado com sucesso para: {jogo_exibir}!")
                            else:
                                st.error("Erro ao enviar palpite. Tente novamente.")
                        except Exception as e:
                            st.error(f"Erro de conexão com o banco de dados: {e}")

elif st.session_state.current_tab == "🎯 Ver Palpites":
    st.markdown("### 🎯 Consultar Palpites Registrados")
    
    df_todos_palpites = ler_aba_sheets("Palpites")
    
    if df_todos_palpites is None or df_todos_palpites.empty:
        st.info("Nenhum palpite foi cadastrado na planilha ainda.")
    else:
        # Filtra palpites tirando registros com nomes de teste ou inválidos
        if "Nome Completo" in df_todos_palpites.columns:
            df_todos_palpites = df_todos_palpites[df_todos_palpites["Nome Completo"].apply(eh_nome_valido)]
            
        st.markdown("Pesquise e confira os palpites de cada participante do bolão:")
        
        lista_emails = df_todos_palpites["E-mail Corporativo"].unique().tolist()
        email_selecionado = st.selectbox("Selecione o participante pelo E-mail Corporativo:", options=lista_emails)
        
        if email_selecionado:
            votos_user = df_todos_palpites[df_todos_palpites["E-mail Corporativo"] == email_selecionado].iloc[0]
            st.markdown(f"#### Palpites de: **{votos_user['Nome Completo']}**")
            
            col_esq, col_dir = st.columns(2)
            metade = len(votos_user.index) // 2
            
            for i, col_name in enumerate(votos_user.index):
                if col_name in ["Timestamp", "E-mail Corporativo", "Nome Completo", "Pontos Acumulados"]:
                    continue
                palpite_val = votos_user[col_name]
                if pd.isna(palpite_val) or str(palpite_val).strip() == "":
                    palpite_val = "Não palpitou"
                    
                target_col = col_esq if i <= metade else col_dir
                with target_col:
                    st.markdown(f"**{col_name}**  \n👉 Palpite: *{palpite_val}*  \n<hr style='margin:5px 0; border-color:#e1e7e3;'>", unsafe_allowed_html=True)

elif st.session_state.current_tab == "⚙️ Painel Admin":
    st.markdown("### ⚙️ Painel Administrativo de Resultados")
    
    st.markdown("Use esta área para cadastrar os placares reais e controlar os jogos oficiais:")
    
    senha_admin = st.text_input("Senha de Administrador do Bolão:", type="password")
    
    if senha_admin == "feltrim2026":
        st.success("Acesso administrativo autenticado!")
        
        if df_resultados.empty:
            st.info("Nenhuma partida carregada no banco de dados.")
        else:
            st.markdown("#### Registrar Placar e Atualizar Status do Jogo")
            
            lista_jogos = df_resultados["Jogo"].tolist()
            jogo_para_atualizar = st.selectbox("Selecione a partida:", options=lista_jogos)
            
            if jogo_para_atualizar:
                partida_linha = df_resultados[df_resultados["Jogo"] == jogo_para_atualizar].iloc[0]
                
                col_ad1, col_ad2, col_ad3 = st.columns(3)
                with col_ad1:
                    novo_placar_m = st.number_input("Gols Mandante:", min_value=0, max_value=20, value=safe_to_int(partida_linha["Placar Real Mandante"]))
                with col_ad2:
                    novo_placar_v = st.number_input("Gols Visitante:", min_value=0, max_value=20, value=safe_to_int(partida_linha["Placar Real Visitante"]))
                with col_ad3:
                    novo_status = st.selectbox("Status da Partida:", options=["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"], index=0)
                    
                if st.button("Salvar Resultado Oficial e Sincronizar", use_container_width=True):
                    with st.spinner("Atualizando resultados e recalculando pontuações..."):
                        payload = {
                            "action": "atualizarPlacar",
                            "senha": senha_admin,
                            "jogo": jogo_para_atualizar,
                            "placar_m": int(novo_placar_m),
                            "placar_v": int(novo_placar_v),
                            "status": novo_status
                        }
                        try:
                            res = requests.post(URL_APPS_SCRIPT, json=payload, timeout=20)
                            if res.status_code == 200:
                                st.success("Placar atualizado e pontos recalculados na planilha!")
                                st.rerun()
                            else:
                                st.error("Falha ao salvar. Verifique o Apps Script.")
                        except Exception as e:
                            st.error(f"Erro de conexão: {e}")

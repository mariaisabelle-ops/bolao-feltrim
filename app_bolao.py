import streamlit as st
import pandas as pd
import urllib.parse
import requests
import json

st.set_page_config(
    page_title="Bolão Feltrim Correa - Copa 2026",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1 {
        color: #1155cc;
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 10px 20px;
        color: #475569;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1155cc !important;
        color: white !important;
        box-shadow: 0 4px 6px -1px rgba(17, 85, 204, 0.2);
    }
    .leaderboard-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 5px solid #1155cc;
        transition: transform 0.2s;
    }
    .leaderboard-card:hover {
        transform: translateY(-2px);
    }
    .podium-1 { border-left: 5px solid #eab308; background-color: #fef9c3; }
    .podium-2 { border-left: 5px solid #cbd5e1; background-color: #f8fafc; }
    .podium-3 { border-left: 5px solid #ca8a04; background-color: #ffedd5; }
    
    .form-box {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_ID = "1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg"

# Codificação segura de abas com espaços e caracteres especiais
sheet_res_encoded = urllib.parse.quote("Form Responses 2")
sheet_oficiais_encoded = urllib.parse.quote("🎯 Resultados Oficiais")

URL_RESPOSTAS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_res_encoded}"
URL_RESULTADOS = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_oficiais_encoded}"

# Inicializando estado para a URL do Web App (Apps Script) para envio direto de palpites
if "web_app_url" not in st.session_state:
    st.session_state["web_app_url"] = ""

@st.cache_data(ttl=10)  # Atualização rápida a cada 10 segundos
def carregar_dados():
    df_resp = None
    df_res = None
    erro_resp = None
    erro_res = None
    
    try:
        df_resp = pd.read_csv(URL_RESPOSTAS)
    except Exception as e:
        erro_resp = f"Falha ao ler a aba de palpites (Form Responses 2): {e}"

    try:
        df_res = pd.read_csv(URL_RESULTADOS)
    except Exception as e:
        erro_res = f"Aba de Resultados Oficiais não encontrada ou inacessível: {e}"
        
    return df_resp, df_res, erro_resp, erro_res

df_respostas, df_resultados, erro_resp, erro_res = carregar_dados()

# Título Principal do App
st.write("<h1>🏆 Bolão Feltrim Correa</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #64748b; margin-bottom: 25px;'>Sua central de palpites e classificação da Copa 2026!</p>", unsafe_allow_html=True)

if df_respostas is not None:
    # Identificar coluna de e-mail de forma inteligente
    col_email_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['email', 'e-mail', 'usuário', 'username', 'quem'])]
    col_email = col_email_list[0] if col_email_list else df_respostas.columns[1]
    
    # Identificar coluna de jogo de forma inteligente
    col_jogo_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['jogo', 'partida', 'id_jogo', 'qual partida'])]
    col_jogo = col_jogo_list[0] if col_jogo_list else df_respostas.columns[2]
    
    # Identificar colunas de placares de palpites de forma inteligente
    col_p_m_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['mandante', 'gols 1', 'placar 1', 'gols mandante'])]
    col_p_v_list = [col for col in df_respostas.columns if any(x in col.lower() for x in ['visitante', 'gols 2', 'placar 2', 'gols visitante'])]
    
    col_p_m = col_p_m_list[0] if col_p_m_list else df_respostas.columns[3]
    col_p_v = col_p_v_list[0] if col_p_v_list else df_respostas.columns[4]

    def calcular_pontos(row):
        if df_resultados is None or df_resultados.empty:
            return 0
        
        jogo_palpitado = row[col_jogo]
        # Filtrar o jogo correspondente nos resultados oficiais
        jogo_oficial = df_resultados[df_resultados['Jogo'] == jogo_palpitado]
        
        if jogo_oficial.empty:
            return 0
            
        real_m = jogo_oficial.iloc[0]['Placar Real Mandante']
        real_v = jogo_oficial.iloc[0]['Placar Real Visitante']
        status = jogo_oficial.iloc[0]['Status']
        
        # Se o jogo ainda não aconteceu ou não tem placar lançado, não pontua
        if pd.isna(real_m) or pd.isna(real_v) or status != "Encerrado":
            return 0
            
        try:
            val_p_m = int(row[col_p_m])
            val_p_v = int(row[col_p_v])
            val_r_m = int(real_m)
            val_r_v = int(real_v)
        except Exception:
            return 0 # Erro de conversão de dados
            
        # 1. Acerto em cheio (10 pontos)
        if val_p_m == val_r_m and val_p_v == val_r_v:
            return 10
            
        # 2. Acerto de tendência (Vencedor ou Empate) (5 pontos)
        signo_palpite = (val_p_m > val_p_v) - (val_p_m < val_p_v)
        signo_real = (val_r_m > val_r_v) - (val_r_m < val_r_v)
        
        if signo_palpite == signo_real:
            return 5
            
        return 0

    # Criando coluna de cálculo dinâmico de pontuação
    df_respostas['Pontos_Calculados'] = df_respostas.apply(calcular_pontos, axis=1)

    tab_ranking, tab_enviar, tab_palpites, tab_jogos = st.tabs([
        "📊 Classificação", 
        "📝 Dar Palpite", 
        "🎯 Ver Palpites", 
        "⚽ Resultados Reais"
    ])

    # --- ABA 1: RANKING GERAL (LEADERBOARD) ---
    with tab_ranking:
        st.subheader("Leaderboard Geral (40 Participantes)")
        
        # Agrupamento e soma de pontos por usuário
        ranking = df_respostas.groupby(col_email)['Pontos_Calculados'].sum().reset_index()
        ranking = ranking.sort_values(by='Pontos_Calculados', ascending=False).reset_index(drop=True)
        
        for idx, row in ranking.iterrows():
            posicao = idx + 1
            usuario = str(row[col_email]).split('@')[0].capitalize()
            pontos = int(row['Pontos_Calculados'])
            
            # Estilização visual condicional para pódio
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
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.2rem; font-weight: 800; width: 30px; color: #475569;">#{posicao}</span>
                        <span style="font-size: 1.4rem;">{emoji}</span>
                        <span style="font-weight: 600; font-size: 1.1rem; color: #1e293b;">{usuario}</span>
                    </div>
                    <span style="font-size: 1.2rem; font-weight: bold; color: #1155cc;">{pontos} pts</span>
                </div>
            """, unsafe_allow_html=True)

    # --- ABA 2: ENVIAR PALPITE DIRETAMENTE ---
    with tab_enviar:
        st.subheader("Envie seu palpite direto para a planilha!")
        
        if not st.session_state["web_app_url"]:
            st.info("ℹ️ Para ativar o envio de palpites em tempo real, configure sua URL de automação uma única vez abaixo.")
            url_input = st.text_input("Cole aqui a URL de implantação do Apps Script (Web App):", placeholder="https://script.google.com/macros/s/.../exec")
            if url_input:
                st.session_state["web_app_url"] = url_input
                st.success("Automação configurada com sucesso!")
                st.rerun()
        else:
            st.markdown('<div class="form-box">', unsafe_allow_html=True)
            with st.form("form_palpite", clear_on_submit=True):
                email_user = st.text_input("Seu E-mail Corporativo:", placeholder="exemplo@feltrim.com.br").strip().lower()
                
                # Coletar jogos da aba de Resultados Oficiais
                lista_jogos = ["Selecione uma partida..."]
                if df_resultados is not None and not df_resultados.empty:
                    jogos_ativos = df_resultados[df_resultados['Status'] != 'Encerrado']
                    if not jogos_ativos.empty:
                        lista_jogos.extend(jogos_ativos['Jogo'].tolist())
                    else:
                        lista_jogos.extend(df_resultados['Jogo'].tolist())
                else:
                    lista_jogos.extend(["⚽ Brasil vs Haiti", "⚽ Argentina vs França"])
                
                jogo_selecionado = st.selectbox("Qual partida você quer palpitar?", lista_jogos)
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    palpite_m = st.number_input("Gols Mandante:", min_value=0, max_value=20, value=0, step=1)
                with col_g2:
                    palpite_v = st.number_input("Gols Visitante:", min_value=0, max_value=20, value=0, step=1)
                
                enviar = st.form_submit_button("🔥 Registrar Palpite Oficial")
                
                if enviar:
                    if not email_user or "@" not in email_user:
                        st.error("❌ Digite um e-mail corporativo válido.")
                    elif jogo_selecionado == "Selecione uma partida...":
                        st.error("❌ Por favor, selecione uma partida válida da lista.")
                    else:
                        with st.spinner("Conectando e salvando na planilha do Google..."):
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
                                    st.success(f"🎉 Palpite registrado com sucesso para {email_user}!")
                                    st.balloons()
                                    st.cache_data.clear() # Limpa cache para exibição imediata
                                else:
                                    st.error(f"Erro no servidor Google Apps Script: {response.text}")
                            except Exception as ex:
                                st.error(f"Não foi possível enviar o palpite. Verifique sua conexão e a URL configurada. Erro: {ex}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Resetar link de automação"):
                st.session_state["web_app_url"] = ""
                st.rerun()

    # --- ABA 3: PALPITES INDIVIDUAIS ---
    with tab_palpites:
        st.subheader("Ver Palpites por Participante")
        usuarios_disponiveis = ranking[col_email].unique()
        usuario_selecionado = st.selectbox("Selecione um participante:", usuarios_disponiveis)
        
        if usuario_selecionado:
            palpites_user = df_respostas[df_respostas[col_email] == usuario_selecionado]
            for _, palpite in palpites_user.iterrows():
                jogo = palpite[col_jogo]
                p_m_val = palpite[col_p_m]
                p_v_val = palpite[col_p_v]
                pts_ganhos = int(palpite['Pontos_Calculados'])
                
                # Tratamento robusto para impedir o erro 'ValueError: cannot convert float NaN to integer'
                try:
                    p_m_display = str(int(float(p_m_val))) if pd.notna(p_m_val) else "-"
                    p_v_display = str(int(float(p_v_val))) if pd.notna(p_v_val) else "-"
                except Exception:
                    p_m_display = "-"
                    p_v_display = "-"
                
                st.info(f"**{jogo}**  \nPalpite enviado: **{p_m_display} x {p_v_display}**  \nPontuação obtida: **{pts_ganhos} pts**")

    # --- ABA 4: RESULTADOS OFICIAIS ---
    with tab_jogos:
        st.subheader("Tabela de Jogos & Resultados Oficiais")
        if df_resultados is not None and not df_resultados.empty:
            for _, jogo in df_resultados.iterrows():
                nome_jogo = jogo['Jogo']
                p_m = jogo['Placar Real Mandante']
                p_v = jogo['Placar Real Visitante']
                status = jogo['Status']
                
                try:
                    p_m_display = str(int(float(p_m))) if pd.notna(p_m) else None
                    p_v_display = str(int(float(p_v))) if pd.notna(p_v) else None
                except Exception:
                    p_m_display = None
                    p_v_display = None
                
                placar_texto = f"{p_m_display} x {p_v_display}" if p_m_display is not None and p_v_display is not None else "vs"
                badge_status = f"🟢 {status}" if status == "Encerrado" else f"🕒 {status}"
                
                st.markdown(f"""
                    <div style="background-color: white; padding: 16px; border-radius: 12px; margin-bottom: 12px; text-align: center; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                        <p style="font-size: 0.85rem; font-weight: bold; color: #1155cc; margin: 0; text-transform: uppercase; letter-spacing: 0.05em;">{badge_status}</p>
                        <h4 style="margin: 8px 0; font-size: 1.15rem; color: #1e293b;">{nome_jogo}</h4>
                        <p style="font-size: 1.5rem; font-weight: 800; color: #1e293b; margin: 0;">{placar_texto}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Crie a aba '🎯 Resultados Oficiais' no Google Sheets para exibir e pontuar os jogos reais.")

else:
    st.error("🔴 Erro de Conexão com o Google Sheets.")
    st.info("Por favor, verifique se o compartilhamento da planilha com ID **1fmM9ocjt8cF3xw9zfNv4ysjlSCpNVCgTEefwbuZ_gwg** está ativado no modo 'Leitor para qualquer pessoa com o link'.")
    with st.expander("Ver detalhes técnicos do erro para diagnóstico"):
        st.write(f"Erro ao carregar respostas: {erro_resp}")
        st.write(f"Erro ao carregar resultados oficiais: {erro_res}")

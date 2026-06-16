import streamlit as st
import pandas as pd
import requests
import json
import re
from datetime import datetime

st.set_page_config(
    page_title="Feltrim Correa - Bolão Copa 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constantes Globais de Integração
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"
DEFAULT_SPREADSHEET_ID = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc" # ID Padrão Seguro


# Estilização CSS Customizada para visual elegante e corporativo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');
    
    /* Configurações Globais de Tipografia */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Cores Institucionais e Fundos */
    .stApp {
        background: linear-gradient(135deg, #f4f7f5 0%, #e9efe8 100%);
    }
    
    /* Banner de Boas-vindas */
    .banner-container {
        background: linear-gradient(135deg, #004b23 0%, #003b1c 100%);
        color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 24px rgba(0, 75, 35, 0.15);
        border: 2px solid #ffb703;
    }
    
    .banner-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }
    
    .banner-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Abas de Navegação Personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(0, 75, 35, 0.05);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 8px;
        color: #004b23;
        font-weight: 600;
        border: 1px solid rgba(0, 75, 35, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #ffb703;
        color: #000000;
        border-color: #ffb703;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #004b23 !important;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(0, 75, 35, 0.2);
    }
    
    /* Cards de Informação e Métricas */
    .card-metric {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border-left: 5px solid #004b23;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .card-metric:hover {
        transform: translateY(-3px);
    }
    
    .card-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #004b23;
    }
    
    .card-lbl {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Pódios e Listas */
    .podium-box {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
        border: 1px solid rgba(0, 75, 35, 0.08);
    }
    
    .podium-1 {
        border-top: 6px solid #ffb703;
        background: linear-gradient(180deg, #fffdf0 0%, #ffffff 100%);
    }
    
    .podium-2 {
        border-top: 6px solid #b5c2b7;
    }
    
    .podium-3 {
        border-top: 6px solid #ca9063;
    }
    
    .podium-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #004b23;
        margin-top: 10px;
    }
    
    .podium-points {
        font-size: 1.8rem;
        font-weight: 800;
        color: #004b23;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

def safe_to_int(val):
    """Converte qualquer tipo de dado de forma segura para inteiro, tratando NaNs."""
    try:
        if pd.isna(val) or val is None:
            return 0
        return int(float(val))
    except:
        return 0

def extract_date_key(text):
    """Extrai chave de ordenação de data (Mês, Dia) do título de uma partida."""
    match = re.search(r'(\d{2})/(\d{2})', str(text))
    if match:
        day, month = int(match.group(1)), int(match.group(2))
        return (month, day)
    return (12, 31)

def formatar_time_slug(nome_completo_jogo, time_tipo="mandante"):
    """Extrai o nome limpo do time mandante ou visitante."""
    limpo = str(nome_completo_jogo).replace("⚽", "").strip()
    partes = re.split(r'\s+vs\s+', limpo, flags=re.IGNORECASE)
    if len(partes) >= 2:
        if time_tipo == "mandante":
            return re.sub(r'\s*\(\d{2}/\d{2}\)', '', partes[0]).strip()
        else:
            return re.sub(r'\s*\(\d{2}/\d{2}\)', '', partes[1]).strip()
    return limpo

@st.cache_data(ttl=15)
def fetch_spreadsheet_data(sheet_id, sheet_name):
    """Busca dados de uma aba específica garantindo tolerância contra planilhas privadas."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        # Se o retorno parecer HTML (página de login do Google), a planilha está privada
        if df.empty or (df.columns.size > 0 and str(df.columns[0]).startswith("<!DOCTYPE")):
            return None
        # Limpar cabeçalhos removendo espaços em branco extras
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return None

# Controle de Sessão para Armazenar ID da Planilha Ativa
if 'spreadsheet_id' not in st.session_state:
    st.session_state['spreadsheet_id'] = DEFAULT_SPREADSHEET_ID

sheet_id = st.session_state['spreadsheet_id']

# Carregamento de Tabelas Cruciais do Banco de Dados
df_palpites = fetch_spreadsheet_data(sheet_id, "Palpites")
df_resultados = fetch_spreadsheet_data(sheet_id, "Resultados")
df_classificacao = fetch_spreadsheet_data(sheet_id, "Classificacao")

# Exibe aviso de configuração se a planilha estiver inacessível
if df_resultados is None:
    st.warning("⚠️ **Acesso à Planilha Não Configurado**")
    st.info("""
    Para que o sistema exiba os dados, certifique-se de que:
    1. Você criou uma planilha do Google a partir do nosso guia de setup.
    2. Compartilhou a sua planilha no modo **"Qualquer pessoa com o link pode ler"** (Leitor).
    3. Registrou o ID correto da planilha no painel do administrador abaixo.
    """)
    
    with st.expander("🔑 Painel de Configuração Inicial"):
        novo_id = st.text_input("ID da Planilha Google (Cole o link ou ID):", value=sheet_id)
        if st.button("Gravar Nova Planilha"):
            # Extrai ID do link caso o usuário cole a URL completa
            id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', novo_id)
            final_id = id_match.group(1) if id_match else novo_id
            st.session_state['spreadsheet_id'] = final_id
            st.rerun()
    st.stop()

# Garantia de colunas válidas na tabela de resultados
if 'Jogo' not in df_resultados.columns:
    df_resultados['Jogo'] = []
if 'Status' not in df_resultados.columns:
    df_resultados['Status'] = "🕒 Agendado"

# Ordenação Cronológica de Partidas
df_resultados['Data_Ordenacao'] = df_resultados['Jogo'].apply(extract_date_key)
df_resultados_sorted = df_resultados.sort_values(by='Data_Ordenacao').drop(columns=['Data_Ordenacao'])

# Renderização do Banner de Boas-vindas
st.markdown("""
<div class="banner-container">
    <div class="banner-title">🏆 BOLÃO CORPORATIVO FELTRIM CORREA</div>
    <div class="banner-subtitle">Acompanhe seus pontos, lance palpites e dispute a liderança em tempo real!</div>
</div>
""", unsafe_allow_html=True)

# Abas Principais de Navegação do App
tab_ranking, tab_palpites, tab_meus_votos, tab_admin = st.tabs([
    "📊 Classificação Geral", 
    "📝 Dar Palpite", 
    "🎯 Meus Palpites", 
    "⚙️ Painel Admin"
])

with tab_ranking:
    # Cabeçalho da classificação
    st.markdown("<h2 style='text-align: center; color: #004b23;'>Placar de Líderes</h2>", unsafe_allow_html=True)
    
    col_rec, col_vazio = st.columns([1, 4])
    with col_rec:
        if st.button("🔄 Recarregar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Métricas Globais do Bolão
    num_competidores = 0
    lider_nome = "-"
    media_pontos = 0.0

    # Validação do DataFrame de Classificação
    if df_classificacao is not None and not df_classificacao.empty:
        colunas_class = [str(c).lower() for c in df_classificacao.columns]
        col_nome_ref = next((c for c in df_classificacao.columns if "participante" in str(c).lower() or "nome" in str(c).lower()), None)
        col_pts_ref = next((c for c in df_classificacao.columns if "pontos" in str(c).lower() or "acumulados" in str(c).lower()), None)
        
        if col_nome_ref and col_pts_ref:
            # Filtrar nomes indesejados (cabeçalhos vazados ou jogos salvos por erro)
            df_classificacao_clean = df_classificacao[
                df_classificacao[col_nome_ref].astype(str).str.contains("vs|⚽|Timestamp|E-mail", case=False) == False
            ]
            
            num_competidores = len(df_classificacao_clean)
            if num_competidores > 0:
                # Ordenar por pontuação
                df_class_sorted = df_classificacao_clean.sort_values(by=col_pts_ref, ascending=False)
                lider_nome = str(df_class_sorted.iloc[0][col_nome_ref]).split("@")[0].title()
                media_pontos = float(df_class_sorted[col_pts_ref].dropna().mean())

    # Exibição dos Painéis de Métricas
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
        <div class="card-metric">
            <div class="card-val">👑 {lider_nome}</div>
            <div class="card-lbl">Líder do Ranking</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card-metric">
            <div class="card-val">{media_pontos:.1f} pts</div>
            <div class="card-lbl">Média de Pontos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Construção Visual do Pódio Premium
    st.markdown("<h3 style='text-align: center; color: #004b23; margin-bottom: 20px;'>🏆 Top 3 Competidores</h3>", unsafe_allow_html=True)
    
    col_p2, col_p1, col_p3 = st.columns([1, 1.2, 1])
    
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

    with col_p2:
        st.markdown(f"""
        <div class="podium-box podium-2">
            <div style="font-size: 2.5rem;">🥈</div>
            <div class="podium-name">{p2_nome}</div>
            <div class="podium-points">{p2_pts}</div>
            <div style="font-weight: bold; color: #666;">2º Lugar</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p1:
        st.markdown(f"""
        <div class="podium-box podium-1">
            <div style="font-size: 3.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));">👑</div>
            <div class="podium-name" style="font-size: 1.3rem;">{p1_nome}</div>
            <div class="podium-points" style="font-size: 2.2rem; color: #004b23;">{p1_pts}</div>
            <div style="font-weight: bold; color: #ffb703; font-size: 1.1rem;">Líder</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p3:
        st.markdown(f"""
        <div class="podium-box podium-3">
            <div style="font-size: 2.5rem;">🥉</div>
            <div class="podium-name">{p3_nome}</div>
            <div class="podium-points">{p3_pts}</div>
            <div style="font-weight: bold; color: #666;">3º Lugar</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #004b23;'>Lista Geral de Classificação</h3>", unsafe_allow_html=True)
    if df_classificacao is not None and num_competidores > 0:
        df_exibir = df_class_sorted.copy()
        
        # Blindagem: Se a coluna Posição já existir no DataFrame importado da planilha, removemos antes de reconstruir
        if 'Posição' in df_exibir.columns:
            df_exibir = df_exibir.drop(columns=['Posição'])
            
        df_exibir.insert(0, 'Posição', range(1, len(df_exibir) + 1))
        df_exibir['Posição'] = df_exibir['Posição'].apply(lambda x: f"{x}º")
        
        # Renomeia colunas para o usuário final
        df_exibir = df_exibir.rename(columns={
            col_nome_ref: "Participante",
            col_pts_ref: "Pontos Acumulados"
        })
        
        st.dataframe(
            df_exibir[['Posição', 'Participante', 'Pontos Acumulados']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum participante pontuou ainda. Os pontos aparecerão assim que os jogos terminarem!")

with tab_palpites:
    st.markdown("<h2 style='color: #004b23;'>Enviar Meu Palpite</h2>", unsafe_allow_html=True)
    
    # Campo de cadastro do Participante
    email_user = st.text_input("Seu E-mail Corporativo Feltrim Correa:", value="", placeholder="exemplo@feltrim.com.br")
    nome_user = st.text_input("Seu Nome Completo:", value="")

    # Filtrar partidas disponíveis (Apenas "Agendadas" e que NÃO acontecem hoje)
    jogos_disponiveis = []
    
    # Data de corte: Hoje é dia 16/06/2026
    data_hoje_str = "16/06"

    for idx, row in df_resultados_sorted.iterrows():
        status_jogo = str(row.get('Status', '🕒 Agendado'))
        nome_jogo = str(row['Jogo'])
        
        # Só permite votação em jogos marcados como Agendado
        if "agendado" in status_jogo.lower():
            # Impede votação em partidas agendadas para o dia de hoje
            if data_hoje_str not in nome_jogo:
                jogos_disponiveis.append(nome_jogo)

    if not jogos_disponiveis:
        st.info("Não há novos jogos abertos para palpites no momento! Todos os jogos de hoje já foram trancados.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("---")
        
        # Seleção de Jogo para Palpite
        jogo_selecionado = st.selectbox("Selecione a partida que deseja votar:", jogos_disponiveis)
        
        if jogo_selecionado:
            team_m = formatar_time_slug(jogo_selecionado, "mandante")
            team_v = formatar_time_slug(jogo_selecionado, "visitante")
            
            st.markdown(f"### Quem vencerá a partida: **{team_m}** vs **{team_v}**?")
            
            # Opções de Voto focadas em Vencedor
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
                    st.error("Por favor, insira um e-mail corporativo válido para registrar o seu palpite.")
                elif len(nome_user) < 3:
                    st.error("Por favor, preencha o seu nome completo.")
                else:
                    # Mapeamento do palpite final
                    palpite_post = ""
                    if "Empate" in voto_opcao:
                        palpite_post = "Empate"
                    elif team_m in voto_opcao:
                        palpite_post = f"Vitoria do {team_m}"
                    else:
                        palpite_post = f"Vitoria do {team_v}"

                    # Montagem da Requisição ao Apps Script
                    payload = {
                        "action": "fazerPalpite",
                        "email": email_user.strip().lower(),
                        "nome": nome_user.strip(),
                        "id_jogo": jogo_selecionado,
                        "palpite": palpite_post
                    }
                    
                    with st.spinner("Registrando seu palpite na planilha..."):
                        try:
                            response = requests.post(URL_APPS_SCRIPT, json=payload, timeout=10)
                            if response.status_code == 200:
                                res_json = response.json()
                                if res_json.get("status") == "success":
                                    st.success(f"Excelente, {nome_user}! Seu palpite para '{jogo_selecionado}' foi gravado com sucesso!")
                                    st.cache_data.clear()
                                else:
                                    st.error(f"Erro no registro: {res_json.get('message')}")
                            else:
                                st.error("Erro de comunicação com o servidor. Tente novamente em instantes.")
                        except Exception as e:
                            st.error(f"Falha na rede: {str(e)}")

with tab_meus_votos:
    st.markdown("<h2 style='color: #004b23;'>Meus Palpites Lançados</h2>", unsafe_allow_html=True)
    email_filtro = st.text_input("Digite o seu e-mail corporativo cadastrado:", value="", key="filtro_votos_email")
    
    if email_filtro:
        email_limpo = email_filtro.strip().lower()
        
        # Varredura resiliente na base de palpites
        if df_palpites is not None and not df_palpites.empty:
            colunas_palpite = [str(c).lower() for c in df_palpites.columns]
            col_email_ref = next((c for c in df_palpites.columns if "email" in str(c).lower() or "e-mail" in str(c).lower()), None)
            
            if col_email_ref:
                registros_usuario = df_palpites[df_palpites[col_email_ref].astype(str).str.strip().str.lower() == email_limpo]
                
                if registros_usuario.empty:
                    st.info(f"Nenhum palpite foi localizado para o e-mail: **{email_limpo}**.")
                else:
                    st.markdown(f"### Palpites de: **{registros_usuario.iloc[0].get('Nome Completo', email_limpo)}**")
                    
                    historico_lista = []
                    
                    for col in df_palpites.columns:
                        # Identifica colunas que pertencem a partidas
                        if "vs" in col or "⚽" in col:
                            voto_valor = registros_usuario.iloc[0][col]
                            if pd.notna(voto_valor) and str(voto_valor).strip() != "":
                                # Busca status oficial do jogo
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
                st.error("Estrutura da aba 'Palpites' incorreta. Coluna de E-mail não localizada.")
        else:
            st.info("Ainda não existem palpites de competidores salvos na planilha.")

with tab_admin:
    st.markdown("<h2 style='color: #004b23;'>🔐 Painel de Controle Administrativo</h2>", unsafe_allow_html=True)
    
    senha_admin = st.text_input("Senha do Administrador:", type="password")
    
    if senha_admin == "feltrim2026":
        st.success("Acesso administrativo autenticado com sucesso!")
        st.write("---")
        
        st.markdown("### 🏆 Cadastro de Resultados Oficiais")
        
        # Seleção de jogo para atualizar placares
        lista_atualizacao = list(df_resultados_sorted['Jogo'].unique())
        jogo_escolhido = st.selectbox("Selecione o Jogo para Cadastrar Placar:", lista_atualizacao)
        
        if jogo_escolhido:
            team_m = formatar_time_slug(jogo_escolhido, "mandante")
            team_v = formatar_time_slug(jogo_escolhido, "visitante")
            
            st.markdown(f"#### Partida: **{team_m}** vs **{team_v}**")
            
            # Recupera valores atuais salvos
            placar_m_padrao = ""
            placar_v_padrao = ""
            status_padrao = "🕒 Agendado"
            
            match_row = df_resultados[df_resultados['Jogo'] == jogo_escolhido]
            if not match_row.empty:
                placar_m_padrao = str(match_row.iloc[0].get('Placar Real Mandante', ''))
                placar_v_padrao = str(match_row.iloc[0].get('Placar Real Visitante', ''))
                status_padrao = str(match_row.iloc[0].get('Status', '🕒 Agendado'))
            
            # Inputs de placar e status
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
                # Monta payload de envio para o Google Sheets
                payload_admin = {
                    "action": "atualizarPlacar",
                    "senha": "feltrim2026",
                    "jogo": jogo_escolhido,
                    "placar_m": novo_placar_m,
                    "placar_v": novo_placar_v,
                    "status": novo_status
                }
                
                with st.spinner("Atualizando planilha e recalculando ranking..."):
                    try:
                        response = requests.post(URL_APPS_SCRIPT, json=payload_admin, timeout=10)
                        if response.status_code == 200:
                            res_json = response.json()
                            if res_json.get("status") == "success":
                                st.success(f"Placar oficial gravado! {team_m} {novo_placar_m} x {novo_placar_v} {team_v} ({novo_status})")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Erro no Apps Script: {res_json.get('message')}")
                        else:
                            st.error("Erro técnico ao conectar no Apps Script da Planilha.")
                    except Exception as e:
                        st.error(f"Erro de conexão: {str(e)}")
                        
        st.write("---")
        st.markdown("### ⚙️ Troca de Planilha Ativa")
        st_id_input = st.text_input("ID da Planilha Google em Uso:", value=sheet_id)
        if st.button("Gravar Alteração de Planilha"):
            st.session_state['spreadsheet_id'] = st_id_input
            st.cache_data.clear()
            st.success("Planilha updated com sucesso na sessão!")
            st.rerun()
    elif senha_admin != "":
        st.error("Senha de Administrador incorreta!")

st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 0.85rem;'>🏆 Feltrim Correa - Todos os direitos reservados. Desenvolvimento de TI Integrado Copa 2026.</p>", unsafe_allow_html=True)

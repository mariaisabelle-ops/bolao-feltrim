import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
import urllib.parse

st.set_page_config(
    page_title="🏆 Bolão Corporativo Feltrim Correa",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constantes globais
SHEET_ID = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"
SENHA_ADMIN = "feltrim2026"

# Fuso horário oficial do Estado de São Paulo (UTC-3) sem timezone-awareness para evitar quebras de comparação
agora_brasil = (datetime.now(timezone.utc) - timedelta(hours=3)).replace(tzinfo=None)

st.markdown(f"""
<style>
    /* Estilos Globais e Fundo */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, #f4f7f6 0%, #e9eff1 100%);
        font-family: 'Montserrat', sans-serif;
        color: #2b2d42;
    }}
    
    /* Banner Principal Elegante */
    .banner-premium {{
        background: linear-gradient(135deg, #004b23 0%, #007200 100%);
        padding: 40px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 75, 35, 0.2);
        margin-bottom: 25px;
        border: 2px solid #D4AF37;
    }}
    
    .banner-premium h1 {{
        color: #ffffff;
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .banner-premium p {{
        color: #e0f2f1;
        font-size: 1.1rem;
        margin-top: 10px;
        margin-bottom: 0;
        font-weight: 300;
    }}

    /* Barra Flutuante de Horário */
    .relogio-container {{
        background-color: #ffffff;
        padding: 10px 20px;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: inline-block;
        margin-bottom: 20px;
        border-left: 5px solid #004b23;
    }}

    /* Estilização Customizada de Botões via Classes Especiais */
    div.stButton > button {{
        background: linear-gradient(135deg, #004b23 0%, #007200 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        padding: 12px 35px !important;
        border: 2px solid #D4AF37 !important;
        box-shadow: 0 6px 15px rgba(0, 75, 35, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        width: auto !important;
        margin: 10px auto !important;
        display: block !important;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.4) !important;
        border-color: #ffffff !important;
        background: linear-gradient(135deg, #007200 0%, #38b000 100%) !important;
    }}
    
    div.stButton > button:active {{
        transform: translateY(-1px) !important;
    }}

    /* Botão Secundário de Recarregar */
    .recarregar-btn div.stButton > button {{
        background: #ffffff !important;
        color: #004b23 !important;
        border: 2px solid #004b23 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
    }}

    .recarregar-btn div.stButton > button:hover {{
        background: #004b23 !important;
        color: white !important;
        border-color: #D4AF37 !important;
    }}

    /* Destaque Inteligente e Atração da Aba "Dar Palpite" */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background-color: transparent;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
        color: #666;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: #004b23 !important;
        color: #ffffff !important;
        border-color: #D4AF37 !important;
        box-shadow: 0 5px 15px rgba(0, 75, 35, 0.15) !important;
    }}

    /* Visual Call-to-Action Exclusivo para o Botão/Aba Dar Palpite */
    .stTabs [data-baseweb="tab"]:nth-child(3) {{
        background: linear-gradient(135deg, #004b23 0%, #007200 100%) !important;
        color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
    }}

    .stTabs [data-baseweb="tab"]:nth-child(3):hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4);
    }}

    /* Cards Estilo Ticket de Jogos */
    .ticket-jogo {{
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border-left: 8px solid #004b23;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }}

    .ticket-jogo:hover {{
        transform: translateY(-2px);
    }}

    .ticket-jogo.fechado {{
        border-left-color: #d90429;
    }}

    .ticket-jogo.aberto {{
        border-left-color: #38b000;
    }}

    /* Pódio 3D Flat Minimalista */
    .podio-container {{
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 20px;
        margin: 40px 0;
        padding: 10px;
    }}

    .podio-col {{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 160px;
    }}

    .podio-card {{
        background: #ffffff;
        border-radius: 16px 16px 8px 8px;
        width: 100%;
        padding: 15px 10px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        border: 1px solid #eef2f5;
    }}

    .podio-avatar {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #f0f4f8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: -15px;
        z-index: 2;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 3px solid #fff;
    }}

    .podio-avatar.ouro {{ border-color: #D4AF37; background: #fffdf0; }}
    .podio-avatar.prata {{ border-color: #C0C0C0; background: #f5f5f5; }}
    .podio-avatar.bronze {{ border-color: #CD7F32; background: #faf3ee; }}

    .podio-rank {{
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 15px;
    }}
    .ouro-txt {{ color: #D4AF37; }}
    .prata-txt {{ color: #708090; }}
    .bronze-txt {{ color: #cd7f32; }}

    /* Cards Informativos de Métricas Unificadas */
    .metric-grid {{
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
    }}

    .metric-box {{
        flex: 1;
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border: 1px solid #eef2f5;
        border-top: 4px solid #004b23;
    }}

    .metric-box h3 {{
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 10px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .metric-box p {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #004b23;
        margin: 0;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="banner-premium">
    <h1>🏆 BOLÃO CORPORATIVO FELTRIM CORREA</h1>
    <p>Consulte a classificação, envie palpites de jogos e acompanhe os placares oficiais em tempo real!</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="relogio-container">
    <span style="font-size: 0.9rem; font-weight: 700; color: #004b23;">🕒 HORA OFICIAL DE BRASÍLIA (UTC-3):</span>
    <span style="font-size: 0.9rem; font-weight: 800; color: #2b2d42; margin-left: 5px;">
        {agora_brasil.strftime('%d/%m/%Y %H:%M:%S')}
    </span>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=15)
def carregar_dados_planilha(sheet_name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"
        df = pd.read_csv(url)
        # Limpeza de colunas vazias geradas pelo Google Sheets
        df = df.dropna(how='all', axis=1)
        df = df.dropna(how='all', axis=0)
        return df
    except Exception as e:
        st.error(f"Erro ao ler aba '{sheet_name}' na Planilha: {e}")
        return pd.DataFrame()

df_resultados = carregar_dados_planilha("Resultados Oficiais")
df_palpites = carregar_dados_planilha("Palpites")
df_classificacao = carregar_dados_planilha("Classificação")

def obter_datetime_jogo(jogo_nome, horario_str):
    try:
        if not horario_str or pd.isna(horario_str):
            horario_str = "12:00"
            
        horario_str = str(horario_str).strip().replace("h", ":")
        jogo_clean = str(jogo_nome).replace("⚽", "").strip()
        
        # Procura por padrão de data (DD/MM) no nome do jogo
        # Exemplo: "Estados Unidos vs Austrália (11/06)" -> "11/06"
        if "(" in jogo_clean:
            data_str = jogo_clean.split("(")[-1].replace(")", "").strip()
        else:
            data_str = "16/06" # Fallback de segurança para o dia de hoje
            
        dia, mes = map(int, data_str.split("/"))
        hora, minuto = map(int, horario_str.split(":"))
        return datetime(2026, mes, dia, hora, minuto)
    except Exception:
        # Retorno de fallback sem fuso horário
        return datetime(2026, 6, 16, 12, 0)

tab_ranking, tab_jogos, tab_votar, tab_meus_votos, tab_admin = st.tabs([
    "📊 Classificação Geral", 
    "📅 Jogos & Resultados", 
    "📝 Dar Palpite", 
    "👤 Meus Palpites",
    "⚙️ Painel Admin"
])

with tab_ranking:
    st.markdown("<h2 style='color:#004b23; font-weight:800; margin-bottom:20px;'>🏆 Tabela de Classificação</h2>", unsafe_allow_html=True)
    
    # Exibição das métricas corporativas
    total_participantes = len(df_classificacao) if not df_classificacao.empty else 0
    primeiro_lugar = df_classificacao.iloc[0]['Nome Completo'] if total_participantes > 0 else "Ninguém cadastrado"
    media_pontos = round(df_classificacao['Pontos Acumulados'].mean(), 1) if total_participantes > 0 else 0.0

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-box">
            <h3>Participantes</h3>
            <p>{total_participantes}</p>
        </div>
        <div class="metric-box">
            <h3>Líder Atual</h3>
            <p style="font-size: 1.4rem; padding-top: 5px;">👑 {primeiro_lugar}</p>
        </div>
        <div class="metric-box">
            <h3>Média Geral</h3>
            <p>{media_pontos} pts</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Construção do Pódio 3D
    if total_participantes > 0:
        p1 = df_classificacao.iloc[0]['Nome Completo'] if total_participantes > 0 else "-"
        pts1 = df_classificacao.iloc[0]['Pontos Acumulados'] if total_participantes > 0 else 0
        
        p2 = df_classificacao.iloc[1]['Nome Completo'] if total_participantes > 1 else "-"
        pts2 = df_classificacao.iloc[1]['Pontos Acumulados'] if total_participantes > 1 else 0
        
        p3 = df_classificacao.iloc[2]['Nome Completo'] if total_participantes > 2 else "-"
        pts3 = df_classificacao.iloc[2]['Pontos Acumulados'] if total_participantes > 2 else 0

        st.markdown(f"""
        <div class="podio-container">
            <!-- 2º LUGAR -->
            <div class="podio-col">
                <div class="podio-avatar prata">🥈</div>
                <div class="podio-card" style="height: 110px;">
                    <div style="font-weight: 700; font-size: 0.9rem; color:#444;">{p2}</div>
                    <div class="podio-rank prata-txt">{pts2} pts</div>
                </div>
            </div>
            <!-- 1º LUGAR -->
            <div class="podio-col">
                <div class="podio-avatar ouro">👑</div>
                <div class="podio-card" style="height: 140px; border-color: #D4AF37;">
                    <div style="font-weight: 800; font-size: 1rem; color:#004b23;">{p1}</div>
                    <div class="podio-rank ouro-txt" style="font-size: 1.7rem;">{pts1} pts</div>
                </div>
            </div>
            <!-- 3º LUGAR -->
            <div class="podio-col">
                <div class="podio-avatar bronze">🥉</div>
                <div class="podio-card" style="height: 90px;">
                    <div style="font-weight: 700; font-size: 0.85rem; color:#444;">{p3}</div>
                    <div class="podio-rank bronze-txt">{pts3} pts</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tabela Completa de Classificação Estilizada em HTML5
    if not df_classificacao.empty:
        # Prevenção contra clonagem de colunas de posição
        df_exibir = df_classificacao.copy()
        if 'Posição' in df_exibir.columns:
            df_exibir = df_exibir.drop(columns=['Posição'])
            
        linhas_html = ""
        for index, row in df_exibir.iterrows():
            pos = index + 1
            nome = row['Nome Completo']
            pontos = row['Pontos Acumulados']
            
            # Formatação especial para o Top 3
            bg_style = ""
            badge = f"{pos}º"
            if pos == 1:
                bg_style = "background-color: #fffdf0; font-weight: bold; border-left: 5px solid #D4AF37;"
                badge = "👑 1º"
            elif pos == 2:
                bg_style = "background-color: #f8fafc; font-weight: bold; border-left: 5px solid #708090;"
                badge = "🥈 2º"
            elif pos == 3:
                bg_style = "background-color: #fdfbf7; font-weight: bold; border-left: 5px solid #cd7f32;"
                badge = "🥉 3º"
                
            linhas_html += f"""
            <tr style='{bg_style} border-bottom: 1px solid #eef2f5;'>
                <td style='padding: 14px; font-weight: 700; width: 100px;'>{badge}</td>
                <td style='padding: 14px;'>{nome}</td>
                <td style='padding: 14px; font-weight: 700; color: #004b23; text-align: right; width: 150px;'>{pontos} pts</td>
            </tr>
            """
            
        tabela_completa_html = f"""
        <div style="overflow-x: auto; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); border: 1px solid #eef2f5; background: white;">
            <table style="width: 100%; border-collapse: collapse; font-family: 'Montserrat', sans-serif; text-align: left;">
                <thead>
                    <tr style="background-color: #004b23; color: white;">
                        <th style="padding: 16px; font-weight: 700; border-top-left-radius: 16px;">POSIÇÃO</th>
                        <th style="padding: 16px; font-weight: 700;">COMPETIDOR</th>
                        <th style="padding: 16px; font-weight: 700; text-align: right; border-top-right-radius: 16px;">PONTUAÇÃO</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_html}
                </tbody>
            </table>
        </div>
        """
        st.html(tabela_completa_html)
    else:
        st.info("Nenhum competidor pontuou ou foi localizado na classificação.")

    # Botão de recarregamento forçado com estilo secundário
    st.markdown('<div class="recarregar-btn">', unsafe_allow_html=True)
    if st.button("🔄 Recarregar Dados da Classificação", key="recarregar_dados"):
        st.cache_data.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab_jogos:
    st.markdown("<h2 style='color:#004b23; font-weight:800; margin-bottom:20px;'>📅 Cronograma de Jogos</h2>", unsafe_allow_html=True)
    
    if not df_resultados.empty:
        df_resultados_sorted = df_resultados.copy()
        
        # Criação de chave de ordenação cronológica de forma segura
        def chave_ordenacao_jogo(row):
            return obter_datetime_jogo(row['Jogo'], row['Horário'])
            
        df_resultados_sorted['Data_Ordenacao'] = df_resultados_sorted.apply(chave_ordenacao_jogo, axis=1)
        df_resultados_sorted = df_resultados_sorted.sort_values(by='Data_Ordenacao')
        
        for idx, row in df_resultados_sorted.iterrows():
            id_jogo = row['ID_Jogo']
            jogo_nome = row['Jogo']
            placar_m = row['Placar Real Mandante']
            placar_v = row['Placar Real Visitante']
            status_oficial = str(row['Status']).strip()
            horario = row['Horário']
            
            limite_palpite = obter_datetime_jogo(jogo_nome, horario) - timedelta(hours=1)
            esta_aberto = agora_brasil < limite_palpite and "encerrado" not in status_oficial.lower() and "andamento" not in status_oficial.lower() and "vivo" not in status_oficial.lower()
            
            status_cor = "#38b000" if esta_aberto else "#d90429"
            status_txt = f"📝 Palpites Abertos (Até {limite_palpite.strftime('%H:%M')})" if esta_aberto else "🔒 Palpites Encerrados"
            
            # Exibição de placar se já houver resultados cadastrados
            tem_placar = not pd.isna(placar_m) and not pd.isna(placar_v) and str(placar_m).strip() != ""
            placar_exibido = f"<span style='font-size: 1.8rem; font-weight:800; color:#004b23; margin: 0 15px;'>{int(float(placar_m))} x {int(float(placar_v))}</span>" if tem_placar else "<span style='font-size: 1.2rem; color:#888; font-weight:600;'>VS</span>"
            
            st.markdown(f"""
            <div class="ticket-jogo {'aberto' if esta_aberto else 'fechado'}">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="background-color: #f0f4f8; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight:700; color:#555;">
                            {id_jogo}
                        </span>
                        <span style="margin-left: 10px; font-weight:700; font-size: 1.1rem; color:#1a1d20;">{jogo_nome}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 0.85rem; color: {status_cor};">
                        {status_txt}
                    </div>
                </div>
                <div style="margin-top: 15px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 0.95rem; font-weight: 600; color:#666; margin-right: 15px;">🕒 Início: {horario}</span>
                    {placar_exibido}
                    <span style="font-size: 0.95rem; font-weight: 700; color: #444; margin-left: 15px; border-left: 2px solid #ccc; padding-left: 15px;">
                        Estado: {status_oficial}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Nenhuma partida agendada foi encontrada na planilha.")

with tab_votar:
    st.markdown("<h2 style='color:#004b23; font-weight:800; margin-bottom:10px;'>📝 Enviar Novo Palpite</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666; margin-bottom:25px;'>Informe seu e-mail corporativo para validar, selecione a partida e envie seu voto de forma exclusiva.</p>", unsafe_allow_html=True)
    
    # Validador de URL Web App do Google Apps Script
    web_app_url = "https://script.google.com/macros/s/AKfycbxj3Lg88oM6A7gMOnr1F18A3e70E8-Nn0IeYdYQpXwS9f9gWwX5o9Y_G9_X9Y_G9_X9/exec"
    
    email_usuario = st.text_input("📧 Seu E-mail Corporativo:", placeholder="exemplo@feltrim.com.br").strip().lower()
    nome_usuario = st.text_input("👤 Seu Nome Completo (Apenas no primeiro voto):", placeholder="João Silva").strip()
    
    if email_usuario:
        if not df_resultados.empty:
            jogos_disponiveis = []
            jogos_nomes_dict = {}
            
            for idx, row in df_resultados.iterrows():
                jogo_nome = row['Jogo']
                id_jogo = row['ID_Jogo']
                status_oficial = str(row['Status']).strip()
                horario = row['Horário']
                
                limite_palpite = obter_datetime_jogo(jogo_nome, horario) - timedelta(hours=1)
                
                # Regra de corte para votação de palpites
                if agora_brasil < limite_palpite and "encerrado" not in status_oficial.lower() and "andamento" not in status_oficial.lower() and "vivo" not in status_oficial.lower():
                    jogos_disponiveis.append(jogo_nome)
                    jogos_nomes_dict[jogo_nome] = id_jogo
            
            if jogos_disponiveis:
                jogo_selecionado = st.selectbox("⚽ Selecione a Partida:", options=jogos_disponiveis)
                id_jogo_sel = jogos_nomes_dict[jogo_selecionado]
                
                # Verificação inteligente de duplicidade em tempo real
                voto_ja_registrado = False
                voto_anterior = ""
                
                if not df_palpites.empty and 'E-mail do Usuário' in df_palpites.columns:
                    filtro_usuario = df_palpites[df_palpites['E-mail do Usuário'].str.strip().str.lower() == email_usuario]
                    if not filtro_usuario.empty and jogo_selecionado in filtro_usuario.columns:
                        voto_existente = filtro_usuario.iloc[0][jogo_selecionado]
                        if not pd.isna(voto_existente) and str(voto_existente).strip() != "":
                            voto_ja_registrado = True
                            voto_anterior = str(voto_existente).strip()
                
                if voto_ja_registrado:
                    st.markdown(f"""
                    <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 8px; margin-top: 15px;">
                        <span style="font-weight: 700; color: #856404;">⚠️ PALPITE JÁ REGISTRADO!</span><br>
                        <span style="color: #856404;">Você já apostou <strong>'{voto_anterior}'</strong> para este jogo. O envio de um novo palpite atualizará seu palpite anterior na planilha automaticamente!</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                palpite_opcao = st.radio(
                    "🎯 Escolha o seu Palpite Oficial:",
                    options=["Vitória do Mandante", "Empate", "Vitória do Visitante"],
                    index=0
                )
                
                # Botão de confirmação de palpite corporativo
                if st.button("🚀 Confirmar e Enviar Palpite", key="btn_confirmar_voto"):
                    if not email_usuario or "@" not in email_usuario:
                        st.error("Por favor, informe um e-mail válido.")
                    elif not nome_usuario and not voto_ja_registrado:
                        st.error("Por favor, preencha o seu nome completo para concluir seu primeiro registro.")
                    else:
                        payload = {
                            "action": "fazerPalpite",
                            "email": email_usuario,
                            "nome": nome_usuario if nome_usuario else "Participante Sincronizado",
                            "id_jogo": jogo_selecionado,
                            "palpite": palpite_opcao
                        }
                        
                        try:
                            with st.spinner("Enviando seu voto para o sistema corporativo..."):
                                res = requests.post(web_app_url, json=payload, timeout=10)
                                response_json = res.json()
                                
                                if response_json.get("status") == "success":
                                    st.success(f"🎉 Maravilha! Seu palpite de '{palpite_opcao}' para o jogo '{jogo_selecionado}' foi registrado!")
                                    st.cache_data.clear()
                                else:
                                    st.error(f"Erro no servidor: {response_json.get('message')}")
                        except Exception as error:
                            st.error(f"Não foi possível conectar à API de voto do Sheets: {error}. Certifique-se de implantar a versão correta do Web App.")
            else:
                st.info("No momento, não há nenhum jogo aberto para palpites.")
        else:
            st.error("Não foi possível verificar a lista de jogos ativos.")

with tab_meus_votos:
    st.markdown("<h2 style='color:#004b23; font-weight:800; margin-bottom:20px;'>👤 Seus Palpites Registrados</h2>", unsafe_allow_html=True)
    
    email_busca = st.text_input("📧 Digite seu E-mail de Competidor para Buscar:", key="email_busca_votos", placeholder="seuemail@feltrim.com.br").strip().lower()
    
    if email_busca:
        if not df_palpites.empty and 'E-mail do Usuário' in df_palpites.columns:
            usuario_palpites = df_palpites[df_palpites['E-mail do Usuário'].str.strip().str.lower() == email_busca]
            
            if not usuario_palpites.empty:
                st.markdown(f"<p style='font-size: 1.1rem; color: #444;'>Palpites cadastrados para o colaborador: <strong>{usuario_palpites.iloc[0].get('Nome Completo', email_busca)}</strong></p>", unsafe_allow_html=True)
                
                confrontos_encontrados = False
                for col_name in df_palpites.columns:
                    if col_name not in ["Carimbo de data/hora", "E-mail do Usuário", "Nome Completo"] and not pd.isna(usuario_palpites.iloc[0][col_name]):
                        voto_val = str(usuario_palpites.iloc[0][col_name]).strip()
                        if voto_val != "":
                            confrontos_encontrados = True
                            
                            # Busca informações do placar oficial correspondente
                            placar_real_txt = "Resultado oficial não lançado"
                            resultado_oficial = "Agendado"
                            status_ticket = "neutro"
                            
                            if not df_resultados.empty:
                                correspondente = df_resultados[df_resultados['Jogo'].str.strip() == col_name.strip()]
                                if not correspondente.empty:
                                    placar_m = correspondente.iloc[0]['Placar Real Mandante']
                                    placar_v = correspondente.iloc[0]['Placar Real Visitante']
                                    resultado_oficial = str(correspondente.iloc[0]['Status']).strip()
                                    
                                    if not pd.isna(placar_m) and not pd.isna(placar_v) and str(placar_m).strip() != "":
                                        placar_real_txt = f"{int(float(placar_m))} x {int(float(placar_v))}"
                                        
                                        # Avaliação se acertou ou errou o palpite
                                        vencedor_real = "Empate"
                                        if int(float(placar_m)) > int(float(placar_v)):
                                            vencedor_real = "Vitória do Mandante"
                                        elif int(float(placar_m)) < int(float(placar_v)):
                                            vencedor_real = "Vitória do Visitante"
                                            
                                        if voto_val == vencedor_real:
                                            status_ticket = "acertou"
                                        else:
                                            status_ticket = "errou"
                                            
                            cor_borda = "#004b23"
                            sub_msg = f"⚽ Jogo: {resultado_oficial}"
                            
                            if status_ticket == "acertou":
                                cor_borda = "#38b000"
                                sub_msg = f"🟢 ACERTOU! Placar Oficial: {placar_real_txt}"
                            elif status_ticket == "errou":
                                cor_borda = "#d90429"
                                sub_msg = f"🔴 ERROU! Placar Oficial: {placar_real_txt}"
                                
                            st.markdown(f"""
                            <div class="ticket-jogo" style="border-left-color: {cor_borda};">
                                <div style="font-weight: 700; font-size: 1.1rem; color: #1a1d20;">{col_name}</div>
                                <div style="margin-top: 8px; font-weight: 600; color: #555;">Seu Voto: <span style="color:{cor_borda}; font-weight:700;">{voto_val}</span></div>
                                <div style="margin-top: 5px; font-size: 0.9rem; color: #666; font-weight:700;">{sub_msg}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                if not confrontos_encontrados:
                    st.info("Você ainda não registrou nenhum palpite neste bolão.")
            else:
                st.warning("Nenhum registro de palpites localizado para este endereço de e-mail.")
        else:
            st.error("Erro ao carregar o banco de dados de palpites para consulta.")

with tab_admin:
    st.markdown("<h2 style='color:#004b23; font-weight:800; margin-bottom:20px;'>🔒 Área de Controle Administrador</h2>", unsafe_allow_html=True)
    
    senha_digitada = st.text_input("🔑 Chave de Acesso Administrativa:", type="password", key="senha_admin_tab").strip()
    
    if senha_digitada == SENHA_ADMIN:
        st.success("🔓 Acesso Administrador Concedido!")
        
        web_app_url_admin = st.text_input(
            "⚙️ URL do Web App do Google Apps Script:",
            value="https://script.google.com/macros/s/AKfycbxj3Lg88oM6A7gMOnr1F18A3e70E8-Nn0IeYdYQpXwS9f9gWwX5o9Y_G9_X9Y_G9_X9/exec",
            help="Coloque aqui a URL que o Google Apps Script gerou após implantar como Aplicativo da Web."
        )
        
        # Seção 1: Lançar Resultados Reais de Jogos
        st.markdown("<hr style='border-color:#ccc;'>", unsafe_allow_html=True)
        st.markdown("### 🏆 Lançamento de Resultados Oficiais")
        
        if not df_resultados.empty:
            jogo_lista_lancador = df_resultados['Jogo'].tolist()
            jogo_para_salvar = st.selectbox("⚽ Selecione o Jogo que Terminou:", options=jogo_lista_lancador, key="jogo_salvar_admin")
            
            col_m, col_v = st.columns(2)
            with col_m:
                placar_m_input = st.number_input("Mandante Placar:", min_value=0, max_value=20, step=1, key="pl_m_admin")
            with col_v:
                placar_v_input = st.number_input("Visitante Placar:", min_value=0, max_value=20, step=1, key="pl_v_admin")
                
            status_partida = st.selectbox("🏁 Status da Partida:", options=["🕒 Agendado", "🟡 Ao Vivo", "🟢 Encerrado"])
            
            if st.button("💾 Salvar Placar Oficial na Planilha", key="btn_salvar_placar_admin"):
                payload = {
                    "action": "atualizarPlacar",
                    "senha": SENHA_ADMIN,
                    "jogo": jogo_para_salvar,
                    "placar_m": int(placar_m_input),
                    "placar_v": int(placar_v_input),
                    "status": status_partida
                }
                
                try:
                    with st.spinner("Enviando dados do placar para o Google Sheets..."):
                        res = requests.post(web_app_url_admin, json=payload, timeout=10)
                        res_json = res.json()
                        if res_json.get("status") == "success":
                            st.success(f"🏆 Placar de '{jogo_para_salvar}' atualizado com sucesso para {placar_m_input}x{placar_v_input} ({status_partida})!")
                            st.cache_data.clear()
                        else:
                            st.error(f"Erro: {res_json.get('message')}")
                except Exception as ex:
                    st.error(f"Erro ao salvar: {ex}")
        else:
            st.warning("Não há partidas cadastradas para lançar placares.")
            
        # Seção 2: Inicialização de Bolão de 56 Jogos
        st.markdown("<hr style='border-color:#ccc;'>", unsafe_allow_html=True)
        st.markdown("### ✨ Inicialização Rápida de Partidas")
        st.info("Caso queira zerar todas as abas e re-inserir os 56 confrontos da Copa em ordem cronológica de Brasília (UTC-3), utilize o recurso abaixo:")
        
        if st.button("⚙️ Inicializar Todos os 56 Jogos na Planilha", key="btn_inicializar_bolao_admin"):
            payload = {
                "action": "inicializarNovoBolao",
                "senha": SENHA_ADMIN
            }
            try:
                with st.spinner("Limpando planilha e reconstruindo partidas..."):
                    res = requests.post(web_app_url_admin, json=payload, timeout=20)
                    res_json = res.json()
                    if res_json.get("status") == "success":
                        st.success("🎉 Sensacional! Todos os 56 jogos da Copa foram cadastrados na planilha Google em perfeita ordem cronológica de fuso horário!")
                        st.cache_data.clear()
                    else:
                        st.error(f"Falha na ação: {res_json.get('message')}")
            except Exception as ex:
                st.error(f"Erro ao inicializar planilha: {ex}")
                
    elif senha_digitada != "":
        st.error("🔑 Senha incorreta! O acesso ao Painel Admin permanece bloqueado.")
    else:
        st.info("Digite a senha administrativa 'feltrim2026' para liberar os controles do bolão.")

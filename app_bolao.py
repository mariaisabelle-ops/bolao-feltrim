import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timezone, timedelta

# Configuração de Página Premium do Streamlit
st.set_page_config(
    page_title="Feltrim Correa - Bolão Corporativo",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🏆 LISTA OFICIAL DE 72 JOGOS DA FASE DE GRUPOS
# ==========================================
JOGOS_CADASTRADOS = [
    # --- 11/06 ---
    {"ID_Jogo": "JOGO_01", "Jogo": "⚽ México vs África do Sul (11/06)", "Horário": "15:00", "Data": "11/06 (Quinta)", "Time_M": "México", "ISO_M": "mx", "Time_V": "África do Sul", "ISO_V": "za"},
    {"ID_Jogo": "JOGO_02", "Jogo": "⚽ Coreia do Sul vs Tchéquia (11/06)", "Horário": "22:00", "Data": "11/06 (Quinta)", "Time_M": "Coreia do Sul", "ISO_M": "kr", "Time_V": "Tchéquia", "ISO_V": "cz"},
    # --- 12/06 ---
    {"ID_Jogo": "JOGO_03", "Jogo": "⚽ Canadá vs Bósnia e Herzegovina (12/06)", "Horário": "15:00", "Data": "12/06 (Sexta)", "Time_M": "Canadá", "ISO_M": "ca", "Time_V": "Bósnia e Herzegovina", "ISO_V": "ba"},
    {"ID_Jogo": "JOGO_04", "Jogo": "⚽ Estados Unidos vs Paraguai (12/06)", "Horário": "21:00", "Data": "12/06 (Sexta)", "Time_M": "Estados Unidos", "ISO_M": "us", "Time_V": "Paraguai", "ISO_V": "py"},
    # --- 13/06 ---
    {"ID_Jogo": "JOGO_05", "Jogo": "⚽ Catar vs Suíça (13/06)", "Horário": "15:00", "Data": "13/06 (Sábado)", "Time_M": "Catar", "ISO_M": "qa", "Time_V": "Suíça", "ISO_V": "ch"},
    {"ID_Jogo": "JOGO_06", "Jogo": "⚽ Brasil vs Marrocos (13/06)", "Horário": "18:00", "Data": "13/06 (Sábado)", "Time_M": "Brasil", "ISO_M": "br", "Time_V": "Marrocos", "ISO_V": "ma"},
    {"ID_Jogo": "JOGO_07", "Jogo": "⚽ Haiti vs Escócia (13/06)", "Horário": "21:00", "Data": "13/06 (Sábado)", "Time_M": "Haiti", "ISO_M": "ht", "Time_V": "Escócia", "ISO_V": "gb-sct"},
    # --- 14/06 ---
    {"ID_Jogo": "JOGO_08", "Jogo": "⚽ Austrália vs Turquia (14/06)", "Horário": "00:00", "Data": "14/06 (Domingo)", "Time_M": "Austrália", "ISO_M": "au", "Time_V": "Turquia", "ISO_V": "tr"},
    {"ID_Jogo": "JOGO_09", "Jogo": "⚽ Alemanha vs Curaçao (14/06)", "Horário": "13:00", "Data": "14/06 (Domingo)", "Time_M": "Alemanha", "ISO_M": "de", "Time_V": "Curaçao", "ISO_V": "cw"},
    {"ID_Jogo": "JOGO_10", "Jogo": "⚽ Holanda vs Japão (14/06)", "Horário": "16:00", "Data": "14/06 (Domingo)", "Time_M": "Holanda", "ISO_M": "nl", "Time_V": "Japão", "ISO_V": "jp"},
    {"ID_Jogo": "JOGO_11", "Jogo": "⚽ Costa do Marfim vs Equador (14/06)", "Horário": "19:00", "Data": "14/06 (Domingo)", "Time_M": "Costa do Marfim", "ISO_M": "ci", "Time_V": "Equador", "ISO_V": "ec"},
    {"ID_Jogo": "JOGO_12", "Jogo": "⚽ Suécia vs Tunísia (14/06)", "Horário": "22:00", "Data": "14/06 (Domingo)", "Time_M": "Suécia", "ISO_M": "se", "Time_V": "Tunísia", "ISO_V": "tn"},
    # --- 15/06 ---
    {"ID_Jogo": "JOGO_13", "Jogo": "⚽ Espanha vs Cabo Verde (15/06)", "Horário": "12:00", "Data": "15/06 (Segunda)", "Time_M": "Espanha", "ISO_M": "es", "Time_V": "Cabo Verde", "ISO_V": "cv"},
    {"ID_Jogo": "JOGO_14", "Jogo": "⚽ Bélgica vs Egito (15/06)", "Horário": "15:00", "Data": "15/06 (Segunda)", "Time_M": "Bélgica", "ISO_M": "be", "Time_V": "Egito", "ISO_V": "eg"},
    {"ID_Jogo": "JOGO_15", "Jogo": "⚽ Arábia Saudita vs Uruguai (15/06)", "Horário": "18:00", "Data": "15/06 (Segunda)", "Time_M": "Arábia Saudita", "ISO_M": "sa", "Time_V": "Uruguai", "ISO_V": "uy"},
    {"ID_Jogo": "JOGO_16", "Jogo": "⚽ Irã vs Nova Zelândia (15/06)", "Horário": "21:00", "Data": "15/06 (Segunda)", "Time_M": "Irã", "ISO_M": "ir", "Time_V": "Nova Zelândia", "ISO_V": "nz"},
    # --- 16/06 ---
    {"ID_Jogo": "JOGO_17", "Jogo": "⚽ França vs Senegal (16/06)", "Horário": "15:00", "Data": "16/06 (Terça)", "Time_M": "França", "ISO_M": "fr", "Time_V": "Senegal", "ISO_V": "sn"},
    {"ID_Jogo": "JOGO_18", "Jogo": "⚽ Iraque vs Noruega (16/06)", "Horário": "18:00", "Data": "16/06 (Terça)", "Time_M": "Iraque", "ISO_M": "iq", "Time_V": "Noruega", "ISO_V": "no"},
    {"ID_Jogo": "JOGO_19", "Jogo": "⚽ Argentina vs Argélia (16/06)", "Horário": "21:00", "Data": "16/06 (Terça)", "Time_M": "Argentina", "ISO_M": "ar", "Time_V": "Argélia", "ISO_V": "dz"},
    # --- 17/06 ---
    {"ID_Jogo": "JOGO_20", "Jogo": "⚽ Áustria vs Jordânia (17/06)", "Horário": "00:00", "Data": "17/06 (Quarta)", "Time_M": "Áustria", "ISO_M": "at", "Time_V": "Jordânia", "ISO_V": "jo"},
    {"ID_Jogo": "JOGO_21", "Jogo": "⚽ Portugal vs RD Congo (17/06)", "Horário": "13:00", "Data": "17/06 (Quarta)", "Time_M": "Portugal", "ISO_M": "pt", "Time_V": "RD Congo", "ISO_V": "cd"},
    {"ID_Jogo": "JOGO_22", "Jogo": "⚽ Inglaterra vs Croácia (17/06)", "Horário": "16:00", "Data": "17/06 (Quarta)", "Time_M": "Inglaterra", "ISO_M": "gb-eng", "Time_V": "Croácia", "ISO_V": "hr"},
    {"ID_Jogo": "JOGO_23", "Jogo": "⚽ Gana vs Panamá (17/06)", "Horário": "19:00", "Data": "17/06 (Quarta)", "Time_M": "Gana", "ISO_M": "gh", "Time_V": "Panamá", "ISO_V": "pa"},
    {"ID_Jogo": "JOGO_24", "Jogo": "⚽ Uzbequistão vs Colômbia (17/06)", "Horário": "22:00", "Data": "17/06 (Quarta)", "Time_M": "Uzbequistão", "ISO_M": "uz", "Time_V": "Colômbia", "ISO_V": "co"},
    # --- 18/06 ---
    {"ID_Jogo": "JOGO_25", "Jogo": "⚽ Tchéquia vs África do Sul (18/06)", "Horário": "12:00", "Data": "18/06 (Quinta)", "Time_M": "Tchéquia", "ISO_M": "cz", "Time_V": "África do Sul", "ISO_V": "za"},
    {"ID_Jogo": "JOGO_26", "Jogo": "⚽ Suíça vs Bósnia e Herzegovina (18/06)", "Horário": "15:00", "Data": "18/06 (Quinta)", "Time_M": "Suíça", "ISO_M": "ch", "Time_V": "Bósnia e Herzegovina", "ISO_V": "ba"},
    {"ID_Jogo": "JOGO_27", "Jogo": "⚽ Canadá vs Catar (18/06)", "Horário": "18:00", "Data": "18/06 (Quinta)", "Time_M": "Canadá", "ISO_M": "ca", "Time_V": "Catar", "ISO_V": "qa"},
    {"ID_Jogo": "JOGO_28", "Jogo": "⚽ México vs Coreia do Sul (18/06)", "Horário": "21:00", "Data": "18/06 (Quinta)", "Time_M": "México", "ISO_M": "mx", "Time_V": "Coreia do Sul", "ISO_V": "kr"},
    # --- 19/06 ---
    {"ID_Jogo": "JOGO_29", "Jogo": "⚽ Estados Unidos vs Austrália (19/06)", "Horário": "15:00", "Data": "19/06 (Sexta)", "Time_M": "Estados Unidos", "ISO_M": "us", "Time_V": "Austrália", "ISO_V": "au"},
    {"ID_Jogo": "JOGO_30", "Jogo": "⚽ Escócia vs Marrocos (19/06)", "Horário": "18:00", "Data": "19/06 (Sexta)", "Time_M": "Escócia", "ISO_M": "gb-sct", "Time_V": "Marrocos", "ISO_V": "ma"},
    {"ID_Jogo": "JOGO_31", "Jogo": "⚽ Brasil vs Haiti (19/06)", "Horário": "21:30", "Data": "19/06 (Sexta)", "Time_M": "Brasil", "ISO_M": "br", "Time_V": "Haiti", "ISO_V": "ht"},
    {"ID_Jogo": "JOGO_32", "Jogo": "⚽ Turquia vs Paraguai (19/06)", "Horário": "23:00", "Data": "19/06 (Sexta)", "Time_M": "Turquia", "ISO_M": "tr", "Time_V": "Paraguai", "ISO_V": "py"},
    # --- 20/06 ---
    {"ID_Jogo": "JOGO_33", "Jogo": "⚽ Holanda vs Suécia (20/06)", "Horário": "13:00", "Data": "20/06 (Sábado)", "Time_M": "Holanda", "ISO_M": "nl", "Time_V": "Suécia", "ISO_V": "se"},
    {"ID_Jogo": "JOGO_34", "Jogo": "⚽ Alemanha vs Costa do Marfim (20/06)", "Horário": "16:00", "Data": "20/06 (Sábado)", "Time_M": "Alemanha", "ISO_M": "de", "Time_V": "Costa do Marfim", "ISO_V": "ci"},
    {"ID_Jogo": "JOGO_35", "Jogo": "⚽ Equador vs Curaçao (20/06)", "Horário": "20:00", "Data": "20/06 (Sábado)", "Time_M": "Equador", "ISO_M": "ec", "Time_V": "Curaçao", "ISO_V": "cw"},
    # --- 21/06 ---
    {"ID_Jogo": "JOGO_36", "Jogo": "⚽ Tunísia vs Japão (21/06)", "Horário": "00:00", "Data": "21/06 (Domingo)", "Time_M": "Tunísia", "ISO_M": "tn", "Time_V": "Japão", "ISO_V": "jp"},
    {"ID_Jogo": "JOGO_37", "Jogo": "⚽ Espanha vs Arábia Saudita (21/06)", "Horário": "12:00", "Data": "21/06 (Domingo)", "Time_M": "Espanha", "ISO_M": "es", "Time_V": "Arábia Saudita", "ISO_V": "sa"},
    {"ID_Jogo": "JOGO_38", "Jogo": "⚽ Bélgica vs Irã (21/06)", "Horário": "15:00", "Data": "21/06 (Domingo)", "Time_M": "Bélgica", "ISO_M": "be", "Time_V": "Irã", "ISO_V": "ir"},
    {"ID_Jogo": "JOGO_39", "Jogo": "⚽ Uruguay vs Cabo Verde (21/06)", "Horário": "18:00", "Data": "21/06 (Domingo)", "Time_M": "Uruguai", "ISO_M": "uy", "Time_V": "Cabo Verde", "ISO_V": "cv"},
    {"ID_Jogo": "JOGO_40", "Jogo": "⚽ Nova Zelândia vs Egito (21/06)", "Horário": "21:00", "Data": "21/06 (Domingo)", "Time_M": "Nova Zelândia", "ISO_M": "nz", "Time_V": "Egito", "ISO_V": "eg"},
    # --- 22/06 ---
    {"ID_Jogo": "JOGO_41", "Jogo": "⚽ Argentina vs Áustria (22/06)", "Horário": "13:00", "Data": "22/06 (Segunda)", "Time_M": "Argentina", "ISO_M": "ar", "Time_V": "Áustria", "ISO_V": "at"},
    {"ID_Jogo": "JOGO_42", "Jogo": "⚽ França vs Iraque (22/06)", "Horário": "17:00", "Data": "22/06 (Segunda)", "Time_M": "França", "ISO_M": "fr", "Time_V": "Iraque", "ISO_V": "iq"},
    {"ID_Jogo": "JOGO_43", "Jogo": "⚽ Noruega vs Senegal (22/06)", "Horário": "20:00", "Data": "22/06 (Segunda)", "Time_M": "Noruega", "ISO_M": "no", "Time_V": "Senegal", "ISO_V": "sn"},
    {"ID_Jogo": "JOGO_44", "Jogo": "⚽ Jordânia vs Argélia (22/06)", "Horário": "23:00", "Data": "22/06 (Segunda)", "Time_M": "Jordânia", "ISO_M": "jo", "Time_V": "Argélia", "ISO_V": "dz"},
    # --- 23/06 ---
    {"ID_Jogo": "JOGO_45", "Jogo": "⚽ Portugal vs Uzbequistão (23/06)", "Horário": "13:00", "Data": "23/06 (Terça)", "Time_M": "Portugal", "ISO_M": "pt", "Time_V": "Uzbequistão", "ISO_V": "uz"},
    {"ID_Jogo": "JOGO_46", "Jogo": "⚽ Inglaterra vs Gana (23/06)", "Horário": "16:00", "Data": "23/06 (Terça)", "Time_M": "Inglaterra", "ISO_M": "gb-eng", "Time_V": "Gana", "ISO_V": "gh"},
    {"ID_Jogo": "JOGO_47", "Jogo": "⚽ Panamá vs Croácia (23/06)", "Horário": "19:00", "Data": "23/06 (Terça)", "Time_M": "Panamá", "ISO_M": "pa", "Time_V": "Croácia", "ISO_V": "hr"},
    {"ID_Jogo": "JOGO_48", "Jogo": "⚽ Colômbia vs RD Congo (23/06)", "Horário": "22:00", "Data": "23/06 (Terça)", "Time_M": "Colômbia", "ISO_M": "co", "Time_V": "RD Congo", "ISO_V": "cd"},
    # --- 24/06 ---
    {"ID_Jogo": "JOGO_49", "Jogo": "⚽ Suíça vs Canadá (24/06)", "Horário": "15:00", "Data": "24/06 (Quarta)", "Time_M": "Suíça", "ISO_M": "ch", "Time_V": "Canadá", "ISO_V": "ca"},
    {"ID_Jogo": "JOGO_50", "Jogo": "⚽ Bósnia e Herzegovina vs Catar (24/06)", "Horário": "15:00", "Data": "24/06 (Quarta)", "Time_M": "Bósnia e Herzegovina", "ISO_M": "ba", "Time_V": "Catar", "ISO_V": "qa"},
    {"ID_Jogo": "JOGO_51", "Jogo": "⚽ Escócia vs Brasil (24/06)", "Horário": "18:00", "Data": "24/06 (Quarta)", "Time_M": "Escócia", "ISO_M": "gb-sct", "Time_V": "Brasil", "ISO_V": "br"},
    {"ID_Jogo": "JOGO_52", "Jogo": "⚽ Marrocos vs Haiti (24/06)", "Horário": "18:00", "Data": "24/06 (Quarta)", "Time_M": "Marrocos", "ISO_M": "ma", "Time_V": "Haiti", "ISO_V": "ht"},
    {"ID_Jogo": "JOGO_53", "Jogo": "⚽ Tchéquia vs México (24/06)", "Horário": "21:00", "Data": "24/06 (Quarta)", "Time_M": "Tchéquia", "ISO_M": "cz", "Time_V": "México", "ISO_V": "mx"},
    {"ID_Jogo": "JOGO_54", "Jogo": "⚽ África do Sul vs Coreia do Sul (24/06)", "Horário": "21:00", "Data": "24/06 (Quarta)", "Time_M": "África do Sul", "ISO_M": "za", "Time_V": "Coreia do Sul", "ISO_V": "kr"},
    # --- 25/06 ---
    {"ID_Jogo": "JOGO_55", "Jogo": "⚽ Equador vs Alemanha (25/06)", "Horário": "16:00", "Data": "25/06 (Quinta)", "Time_M": "Equador", "ISO_M": "ec", "Time_V": "Alemanha", "ISO_V": "de"},
    {"ID_Jogo": "JOGO_56", "Jogo": "⚽ Curaçao vs Costa do Marfim (25/06)", "Horário": "16:00", "Data": "25/06 (Quinta)", "Time_M": "Curaçao", "ISO_M": "cw", "Time_V": "Costa do Marfim", "ISO_V": "ci"},
    {"ID_Jogo": "JOGO_57", "Jogo": "⚽ Tunísia vs Holanda (25/06)", "Horário": "19:00", "Data": "25/06 (Quinta)", "Time_M": "Tunísia", "ISO_M": "tn", "Time_V": "Holanda", "ISO_V": "nl"},
    {"ID_Jogo": "JOGO_58", "Jogo": "⚽ Japão vs Suécia (25/06)", "Horário": "19:00", "Data": "25/06 (Quinta)", "Time_M": "Japão", "ISO_M": "jp", "Time_V": "Suécia", "ISO_V": "se"},
    {"ID_Jogo": "JOGO_59", "Jogo": "⚽ Turquia vs Estados Unidos (25/06)", "Horário": "22:00", "Data": "25/06 (Quinta)", "Time_M": "Turquia", "ISO_M": "tr", "Time_V": "Estados Unidos", "ISO_V": "us"},
    {"ID_Jogo": "JOGO_60", "Jogo": "⚽ Paraguai vs Austrália (25/06)", "Horário": "22:00", "Data": "25/06 (Quinta)", "Time_M": "Paraguai", "ISO_M": "py", "Time_V": "Austrália", "ISO_V": "au"},
    # --- 26/06 ---
    {"ID_Jogo": "JOGO_61", "Jogo": "⚽ Noruega vs França (26/06)", "Horário": "15:00", "Data": "26/06 (Sexta)", "Time_M": "Noruega", "ISO_M": "no", "Time_V": "França", "ISO_V": "fr"},
    {"ID_Jogo": "JOGO_62", "Jogo": "⚽ Senegal vs Iraque (26/06)", "Horário": "15:00", "Data": "26/06 (Sexta)", "Time_M": "Senegal", "ISO_M": "sn", "Time_V": "Iraque", "ISO_V": "iq"},
    {"ID_Jogo": "JOGO_63", "Jogo": "⚽ Uruguai vs Espanha (26/06)", "Horário": "20:00", "Data": "26/06 (Sexta)", "Time_M": "Uruguai", "ISO_M": "uy", "Time_V": "Espanha", "ISO_V": "es"},
    {"ID_Jogo": "JOGO_64", "Jogo": "⚽ Cabo Verde vs Arábia Saudita (26/06)", "Horário": "20:00", "Data": "26/06 (Sexta)", "Time_M": "Cabo Verde", "ISO_M": "cv", "Time_V": "Arábia Saudita", "ISO_V": "sa"},
    {"ID_Jogo": "JOGO_65", "Jogo": "⚽ Nova Zelândia vs Bélgica (26/06)", "Horário": "23:00", "Data": "26/06 (Sexta)", "Time_M": "Nova Zelândia", "ISO_M": "nz", "Time_V": "Bélgica", "ISO_V": "be"},
    {"ID_Jogo": "JOGO_66", "Jogo": "⚽ Egito vs Irã (26/06)", "Horário": "23:00", "Data": "26/06 (Sexta)", "Time_M": "Egito", "ISO_M": "eg", "Time_V": "Irã", "ISO_V": "ir"},
    # --- 27/06 ---
    {"ID_Jogo": "JOGO_67", "Jogo": "⚽ Panamá vs Inglaterra (27/06)", "Horário": "17:00", "Data": "27/06 (Sábado)", "Time_M": "Panamá", "ISO_M": "pa", "Time_V": "Inglaterra", "ISO_V": "gb-eng"},
    {"ID_Jogo": "JOGO_68", "Jogo": "⚽ Croácia vs Gana (27/06)", "Horário": "17:00", "Data": "27/06 (Sábado)", "Time_M": "Croácia", "ISO_M": "hr", "Time_V": "Gana", "ISO_V": "gh"},
    {"ID_Jogo": "JOGO_69", "Jogo": "⚽ Colômbia vs Portugal (27/06)", "Horário": "19:30", "Data": "27/06 (Sábado)", "Time_M": "Colômbia", "ISO_M": "co", "Time_V": "Portugal", "ISO_V": "pt"},
    {"ID_Jogo": "JOGO_70", "Jogo": "⚽ RD Congo vs Uzbequistão (27/06)", "Horário": "19:30", "Data": "27/06 (Sábado)", "Time_M": "RD Congo", "ISO_M": "cd", "Time_V": "Uzbequistão", "ISO_V": "uz"},
    {"ID_Jogo": "JOGO_71", "Jogo": "⚽ Jordânia vs Argentina (27/06)", "Horário": "22:00", "Data": "27/06 (Sábado)", "Time_M": "Jordânia", "ISO_M": "jo", "Time_V": "Argentina", "ISO_V": "ar"},
    {"ID_Jogo": "JOGO_72", "Jogo": "⚽ Argélia vs Áustria (27/06)", "Horário": "22:00", "Data": "27/06 (Sábado)", "Time_M": "Argélia", "ISO_M": "dz", "Time_V": "Áustria", "ISO_V": "at"}
]

# Configurações dinâmicas padrão
if "spreadsheet_id" not in st.session_state:
    st.session_state.spreadsheet_id = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"
if "web_app_url" not in st.session_state:
    st.session_state.web_app_url = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"

# Armazenamento de credenciais locais
if "saved_email" not in st.session_state:
    st.session_state.saved_email = ""
if "saved_name" not in st.session_state:
    st.session_state.saved_name = ""

# ==========================================
# 🎯 FUNÇÃO DE VALIDAÇÃO TEMPORAL EM TEMPO REAL (FUSO HORÁRIO BRASÍLIA)
# ==========================================
def jogo_ja_passou(data_str, horario_str):
    """
    Verifica se o jogo já passou/começou baseado no horário de Brasília (UTC-3).
    data_str format: "11/06 (Quinta)"
    horario_str format: "15:00"
    """
    try:
        # Extrai dia e mês da string "11/06 (Quinta)"
        dia_mes = data_str.split(" ")[0]
        dia, mes = dia_mes.split("/")
        hora, minuto = horario_str.split(":")
        
        # O ano é 2026
        ano = 2026
        
        # Cria fuso horário UTC-3 (Brasília)
        br_tz = timezone(timedelta(hours=-3))
        
        # Constrói o datetime do jogo localizado em BRT
        match_dt = datetime(ano, int(mes), int(dia), int(hora), int(minuto), tzinfo=br_tz)
        
        # Obtém o tempo atual localizado em BRT
        now_br = datetime.now(timezone(timedelta(hours=-3)))
        
        return now_br >= match_dt
    except Exception:
        return False

# ==========================================
# 🎨 ESTILIZAÇÃO VISUAL PREMIUM E DE ALTO RELEVO (LARANJA, ROSA, VERDE E BEGE)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #FAF6F0 !important; /* Alabastro/Bege Macio Premium */
        color: #3C332E !important; /* Grafite-Terra para conforto visual máximo */
    }
    
    /* Centralização Absoluta do Bloco Principal no Streamlit (Corrige o "tá torto/esquerda") */
    .block-container, [data-testid="stAppViewBlockContainer"] {
        max-width: 1050px !important;
        margin: 0 auto !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }
    
    /* Configuração da Barra Lateral (Sidebar) Macia e Elegante */
    [data-testid="stSidebar"] {
        background-color: #FFFDF9 !important;
        border-right: 1.5px solid rgba(224, 83, 21, 0.1) !important;
    }
    
    /* Cabeçalho de Título com Grife Feltrim Correa */
    .hero-title {
        font-weight: 850;
        font-size: 2.8rem;
        color: #E05315 !important; /* Laranja Terracota Sólido - Sem gradiente */
        text-align: center;
        margin-bottom: 0.1rem;
        letter-spacing: -0.04em;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #E05315; /* Laranja Terracota */
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    
    /* Cápsula de Conexão do Colaborador */
    .profile-banner {
        background: #FFFFFF;
        color: #3C332E;
        padding: 1.25rem;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(217, 114, 205, 0.2); /* Rosa Dusty */
        box-shadow: 0 8px 30px rgba(61, 51, 46, 0.02);
    }
    
    /* Reset outer stTabs container so it doesn't restrict content width or add weird borders */
    div[data-testid="stTabs"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Redesenho Total das Abas Nativas (Floating Pills Premium) - Sem gradiente e Centralizadas */
    div[data-testid="stTabs"] [role="tablist"] {
        background: #FFFFFF !important;
        padding: 6px !important;
        border-radius: 40px !important;
        border: 1px solid rgba(224, 83, 21, 0.12) !important;
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto 2rem auto !important;
        max-width: max-content !important;
        box-shadow: 0 4px 15px rgba(224, 83, 21, 0.03) !important;
        border-bottom: none !important;
    }
    
    div[data-testid="stTabs"] button[role="tab"] {
        color: #3C332E !important;
        background-color: transparent !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 8px 20px !important;
        border-radius: 20px !important;
        margin-right: 4px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stTabs"] button[role="tab"]:hover {
        color: #D972CD !important; /* Rosa Dusty */
        background-color: rgba(217, 114, 205, 0.04) !important;
    }
    
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background-color: #E05315 !important; /* Solid Laranja Terracota */
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(224, 83, 21, 0.18) !important;
    }
    
    /* Evitar "abas duplas pesadas" ao customizar as sub-abas aninhadas e centralizá-las */
    div[data-testid="stTabs"] div[data-testid="stTabs"] [role="tablist"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 auto 1.5rem auto !important;
        display: flex !important;
        justify-content: center !important;
        max-width: max-content !important;
    }
    
    div[data-testid="stTabs"] div[data-testid="stTabs"] button[role="tab"] {
        font-size: 0.9rem !important;
        padding: 6px 16px !important;
        border-radius: 8px !important;
        border: 1px solid rgba(224, 83, 21, 0.15) !important;
        background-color: #FFFFFF !important;
    }
    
    div[data-testid="stTabs"] div[data-testid="stTabs"] button[role="tab"]:hover {
        background-color: rgba(224, 83, 21, 0.03) !important;
    }
    
    div[data-testid="stTabs"] div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: #FAF6F0 !important;
        color: #E05315 !important;
        border: 1.5px solid #E05315 !important;
        box-shadow: none !important;
    }
    
    /* ELIMINAÇÃO TOTAL E COMPLETA DE BARRAS DE HIGHLIGHT E BORDAS DO STREAMLIT QUE CORTAM AS ABAS */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight-bar"],
    [data-baseweb="tab-highlight-bar"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"],
    [data-baseweb="tab-border"] {
        display: none !important;
        background-color: transparent !important;
        height: 0px !important;
        border: none !important;
    }
    
    /* Botões em Cápsula do Escritório - Totalmente Sólidos (Sem Gradientes) */
    .stButton > button {
        background-color: #E05315 !important; /* Cor Sólida Laranja Terracota */
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 30px !important; /* Formato Pílula */
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(224, 83, 21, 0.15) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(217, 114, 205, 0.35) !important;
        background-color: #D972CD !important; /* Cor Sólida Rosa Dusty */
        color: #FFFFFF !important;
    }
    
    /* Card de Container Premium (Efeito Hover Inteligente) */
    div[data-testid="stVerticalBlockBorder"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(224, 83, 21, 0.08) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(61, 51, 46, 0.015) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    div[data-testid="stVerticalBlockBorder"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(224, 83, 21, 0.045) !important;
        border-color: rgba(224, 83, 21, 0.15) !important;
    }
    
    /* Customização de Inputs do Formulário */
    input[type="number"] {
        border-radius: 12px !important;
        border: 1.5px solid rgba(224, 83, 21, 0.12) !important;
        background-color: #FFFDF8 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        color: #3C332E !important;
        transition: border-color 0.2s ease !important;
    }
    
    input[type="number"]:focus {
        border-color: #D972CD !important;
        background-color: #FFFFFF !important;
    }
    
    /* Pódio Corporativo Minimalista e Harmonizado (Sem sobreposições) */
    .podium-section {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 1.5rem;
        margin: 2.5rem auto 1.5rem auto;
        max-width: 800px;
        padding: 0 1rem;
    }
    
    .podium-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .podium-box {
        width: 100%;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(61, 51, 46, 0.02);
        border: 1px solid rgba(224, 83, 21, 0.12);
        background-color: #FFFFFF;
        box-sizing: border-box;
    }
    
    /* Cores Nobres do Pódio nas Bordas */
    .gold-box {
        border-top: 6px solid #E05315 !important; /* Laranja no 1º */
        height: 240px;
        z-index: 3;
    }
    
    .silver-box {
        border-top: 6px solid #D972CD !important; /* Rosa no 2º */
        height: 200px;
        z-index: 2;
    }
    
    .bronze-box {
        border-top: 6px solid #7CA613 !important; /* Verde no 3º */
        height: 180px;
        z-index: 1;
    }
    
    .avatar-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #FAF6F0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 10px rgba(61, 51, 46, 0.04);
        border: 1.5px solid rgba(224, 83, 21, 0.15);
    }
    
    .podium-name {
        font-size: 1rem;
        font-weight: 700;
        color: #3C332E;
        margin-bottom: 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }
    
    .podium-score {
        font-size: 1.15rem;
        font-weight: 850;
        color: #E05315;
    }
    
    /* Crachás do lugar agora posicionados de forma limpa e estática dentro da caixa */
    .badge-rank {
        padding: 0.25rem 0.85rem;
        border-radius: 30px;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        background-color: #FAF6F0;
        border: 1px solid;
    }
    
    /* Tabelas Corporativas Elegantes - Sem gradiente */
    .premium-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 6px;
        margin-top: 1rem;
    }
    
    .premium-table th {
        background-color: #E05315 !important; /* Sólido Laranja Terracota */
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 1.1rem 1.2rem !important;
        text-align: left !important;
        border-bottom: 2px solid rgba(224, 83, 21, 0.15) !important;
    }
    
    .premium-row {
        background: #FFFFFF;
        box-shadow: 0 2px 6px rgba(61, 51, 46, 0.01);
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .premium-row:hover {
        transform: scale(1.004);
        box-shadow: 0 4px 15px rgba(224, 83, 21, 0.035) !important;
    }
    
    .premium-row td {
        padding: 1.1rem 1.2rem;
        border-top: 1px solid rgba(61, 51, 46, 0.015);
        border-bottom: 1px solid rgba(61, 51, 46, 0.015);
        font-size: 0.95rem;
        color: #3C332E;
    }
    
    .premium-row td:first-child {
        border-left: 4px solid #E05315;
        border-radius: 12px 0 0 12px;
        font-weight: 700;
    }
    
    .premium-row td:last-child {
        border-right: 1px solid rgba(61, 51, 46, 0.015);
        border-radius: 0 12px 12px 0;
    }
    
    .rank-indicator {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 0.8rem;
        color: white;
    }
    
    .rank-1 { background-color: #E05315; color: #FFFFFF; }
    .rank-2 { background-color: #D972CD; color: #FFFFFF; }
    .rank-3 { background-color: #7CA613; color: #FFFFFF; }
    .rank-other { background-color: #FFFDF6; color: #3C332E; border: 1px solid rgba(224,83,21,0.12); }
    
    /* Configuração de Containers Nativos do Streamlit */
    div[data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(224, 83, 21, 0.12) !important;
        border-radius: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/120/trophy.png", width=55)
    st.markdown("<h3 style='color:#3C332E; margin-bottom: 0;'>🏆 Feltrim Correa</h3>", unsafe_allow_html=True)
    st.markdown("<small style='color:#E05315; font-weight:700;'>Copa do Mundo FIFA 2026</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Identificação do usuário logado na barra lateral
    if st.session_state.saved_email and st.session_state.saved_name:
        st.markdown(f"""
        <div style='background-color:#FFFFFF; padding:12px; border-radius:12px; border-left:4px solid #D972CD; margin-bottom:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.02); border-right:1px solid rgba(224,83,21,0.05); border-top:1px solid rgba(224,83,21,0.05); border-bottom:1px solid rgba(224,83,21,0.05);'>
            <span style='font-size:0.75rem; text-transform:uppercase; color:#E05315; font-weight:700;'>Identificado</span>
            <div style='font-weight:800; color:#3C332E;'>⚽ {st.session_state.saved_name}</div>
            <span style='font-size:0.75rem; color:#3C332E; opacity:0.8;'>{st.session_state.saved_email}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Alternar Utilizador"):
            st.session_state.saved_email = ""
            st.session_state.saved_name = ""
            st.rerun()
    else:
        st.markdown("<small style='color:#3C332E; opacity:0.7;'>Identifique-se na aba de palpites para começar.</small>", unsafe_allow_html=True)
        
    st.markdown("---")
    if st.button("🔄 Sincronizar Agora", use_container_width=True):
        st.cache_data.clear()
        st.success("Sincronização efetuada!")
        st.rerun()

@st.cache_data(ttl=60)
def carregar_dados_planilha(sheet_id):
    try:
        url_palpites = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Palpites"
        df_palpites = pd.read_csv(url_palpites)
        
        url_resultados = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Resultados+Oficiais"
        df_resultados = pd.read_csv(url_resultados)
        
        return df_palpites, df_resultados
    except Exception:
        return None, None

df_p, df_r = carregar_dados_planilha(st.session_state.spreadsheet_id)

def obter_resultado_map(df_resultados):
    if df_resultados is None or df_resultados.empty:
        return {}
    res_map = {}
    for _, row in df_resultados.iterrows():
        j_id = str(row["ID_Jogo"]).strip()
        try:
            m = int(row["Placar Real Mandante"])
            v = int(row["Placar Real Visitante"])
            status = str(row["Status"]).strip()
            res_map[j_id] = {"m": m, "v": v, "status": status}
        except Exception:
            res_map[j_id] = {"m": None, "v": None, "status": str(row.get("Status", "Agendado")).strip()}
    return res_map

def calcular_pontos_palpite(palpite_str, real_m, real_v):
    if not palpite_str or "-" not in palpite_str or real_m is None or real_v is None:
        return 0, "Sem Palpite"
    try:
        parts = palpite_str.split("-")
        pm, pv = int(parts[0].strip()), int(parts[1].strip())
        
        if pm == real_m and pv == real_v:
            return 10, "Exato"
        elif (pm > pv and real_m > real_v) or (pm < pv and real_m < real_v) or (pm == pv and real_m == real_v):
            return 5, "Vencedor"
        return 0, "Errou"
    except Exception:
        return 0, "Erro"

def calcular_ranking_real(df_palpites, df_resultados):
    if df_palpites is None or df_resultados is None or df_palpites.empty or df_resultados.empty:
        return pd.DataFrame()
        
    resultado_map = obter_resultado_map(df_resultados)
    pontuacao = {}
    
    cols = list(df_palpites.columns)
    email_col, nome_col = None, None
    for c in cols:
        lc = c.lower().strip()
        if "email" in lc or "e-mail" in lc or "usuário" in lc:
            email_col = c
        if "nome" in lc:
            nome_col = c
            
    if not email_col:
        return pd.DataFrame()
        
    for _, row in df_palpites.iterrows():
        email = str(row[email_col]).strip().lower()
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
                    
                    if juego_info := resultado_map.get(jogo_id):
                        if "Encerrado" in juego_info["status"] or "Ao Vivo" in juego_info["status"]:
                            pts, tipo = calcular_pontos_palpite(palpite, juego_info["m"], juego_info["v"])
                            pontuacao[email]["Pontos"] += pts
                            if tipo == "Exato":
                                pontuacao[email]["Acertos Exatos"] += 1
                            elif tipo == "Vencedor":
                                pontuacao[email]["Acertos Vencedor"] += 1
                                
    ranking_df = pd.DataFrame(pontuacao.values())
    if not ranking_df.empty:
        ranking_df = ranking_df.sort_values(by=["Pontos", "Acertos Exatos", "Nome"], ascending=[False, False, True])
        ranking_df.insert(0, "Posição", range(1, len(ranking_df) + 1))
        
    return ranking_df

# ==========================================
# 📊 DESIGN SYSTEM DE ABAS SUPERIORES (TOP TABS - FLOATING PILLS)
# ==========================================
tab_ranking, tab_palpites, tab_admin = st.tabs([
    "📊 Resultados & Classificação Geral", 
    "📝 Registrar Meus Palpites", 
    "🔧 Portal de Administração"
])

# --- ABA 1: RANKING E RESULTADOS ---
with tab_ranking:
    st.markdown('<div class="hero-title">Feltrim Correa</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Bolão Corporativo Oficial da Fase de Grupos</div>', unsafe_allow_html=True)
    
    sub_tab_rank, sub_tab_jogos = st.tabs(["📊 Classificação dos Colaboradores", "📅 Tabela de Jogos e Resultados Oficiais"])
    
    with sub_tab_rank:
        if df_p is not None and df_r is not None:
            rank = calcular_ranking_real(df_p, df_r)
            
            if not rank.empty:
                p1_nome = rank.iloc[0]['Nome'] if len(rank) >= 1 else "Vago"
                p1_pontos = rank.iloc[0]['Pontos'] if len(rank) >= 1 else 0
                
                p2_nome = rank.iloc[1]['Nome'] if len(rank) >= 2 else "Vago"
                p2_pontos = rank.iloc[1]['Pontos'] if len(rank) >= 2 else 0
                
                p3_nome = rank.iloc[2]['Nome'] if len(rank) >= 3 else "Vago"
                p3_pontos = rank.iloc[2]['Pontos'] if len(rank) >= 3 else 0
                
                # Montagem do Pódio perfeitamente simétrica e contida dentro dos cards
                podium_html = (
                    '<div class="podium-section">'
                      '<div class="podium-col">'
                        '<div class="podium-box silver-box">'
                          '<span class="badge-rank" style="border-color:#D972CD; color:#D972CD;">2º Lugar</span>'
                          '<div class="avatar-circle">🥈</div>'
                          '<div class="podium-name">' + p2_nome + '</div>'
                          '<div class="podium-score" style="color:#D972CD;">' + str(p2_pontos) + ' pts</div>'
                        '</div>'
                      '</div>'
                      '<div class="podium-col">'
                        '<div class="podium-box gold-box">'
                          '<span class="badge-rank" style="border-color:#E05315; color:#E05315; font-weight:800;">Líder 👑</span>'
                          '<div class="avatar-circle" style="border-color:#E05315;">👑</div>'
                          '<div class="podium-box gold-box">'
                            '<div class="podium-name" style="font-size:1.1rem; font-weight:800; color:#3C332E;">' + p1_nome + '</div>'
                            '<div class="podium-score" style="font-size:1.45rem; color:#E05315;">' + str(p1_pontos) + ' pts</div>'
                          '</div>'
                        '</div>'
                      '</div>'
                      '<div class="podium-col">'
                        '<div class="podium-box bronze-box">'
                          '<span class="badge-rank" style="border-color:#7CA613; color:#7CA613;">3º Lugar</span>'
                          '<div class="avatar-circle">🥉</div>'
                          '<div class="podium-name">' + p3_nome + '</div>'
                          '<div class="podium-score" style="color:#7CA613;">' + str(p3_pontos) + ' pts</div>'
                        '</div>'
                      '</div>'
                    '</div>'
                )
                st.markdown(podium_html, unsafe_allow_html=True)
                
                st.markdown("<h4 style='color:#3C332E; font-weight:800; margin-top:2.5rem;'>📊 Classificação Geral</h4>", unsafe_allow_html=True)
                
                table_html = """<table class="premium-table">
<thead>
<tr>
<th style="width: 80px; text-align: center;">Posição</th>
<th>Colaborador</th>
<th style="text-align: center;">Palpites Feitos</th>
<th style="text-align: center;">Placar Exato (10 Pts)</th>
<th style="text-align: center;">Vencedor/Empate (5 Pts)</th>
<th style="text-align: right; padding-right: 1.5rem;">Pontuação Geral</th>
</tr>
</thead>
<tbody>"""
                
                for _, row in rank.iterrows():
                    pos = row["Posição"]
                    if pos == 1:
                        rank_class = "rank-1"
                        badge = "🥇"
                    elif pos == 2:
                        rank_class = "rank-2"
                        badge = "🥈"
                    elif pos == 3:
                        rank_class = "rank-3"
                        badge = "🥉"
                    else:
                        rank_class = "rank-other"
                        badge = str(pos)
                        
                    table_html += f"""<tr class="premium-row">
<td style="text-align: center;"><span class="rank-indicator {rank_class}">{badge}</span></td>
<td style="font-weight: 700; color: #3C332E;">{row['Nome']}</td>
<td style="text-align: center; font-weight: 600;">{row['Palpites Feitos']}</td>
<td style="text-align: center; color: #E05315; font-weight: 700;">{row['Acertos Exatos']}</td>
<td style="text-align: center; color: #D972CD; font-weight: 700;">{row['Acertos Vencedor']}</td>
<td style="text-align: right; font-weight: 800; font-size: 1.15rem; color: #3C332E; padding-right: 1.5rem;">{row['Pontos']} pts</td>
</tr>"""
                    
                table_html += "</tbody></table>"
                st.markdown(table_html, unsafe_allow_html=True)
                
            else:
                st.info("Nenhum palpite foi cadastrado ainda! Registre os seus palpites na aba superior.")
        else:
            st.error("⚠️ Planilha Desconectada ou em Branco!")
            st.info("Para sincronizar o sistema do bolão, configure o ID e a API do seu Sheets no Portal de Controle.")
            
    with sub_tab_jogos:
        if df_r is not None and not df_r.empty:
            res_map = obter_resultado_map(df_r)
            
            # Mapear os palpites do usuário conectado para mostrar nos cards
            user_bets = {}
            if st.session_state.saved_email and df_p is not None and not df_p.empty:
                email_col_name = None
                for c in df_p.columns:
                    if "email" in c.lower() or "e-mail" in c.lower() or "usuário" in c.lower():
                        email_col_name = c
                        break
                if email_col_name:
                    u_row = df_p[df_p[email_col_name].astype(str).str.strip().str.lower() == st.session_state.saved_email]
                    if not u_row.empty:
                        for j in JOGOS_CADASTRADOS:
                            nome_j = j["Jogo"]
                            if nome_j in df_p.columns:
                                val = str(u_row[nome_j].values[0]).strip()
                                if val and val != "nan" and "-" in val:
                                    user_bets[j["ID_Jogo"]] = val

            st.markdown("<h4 style='color:#3C332E; font-weight:800;'>🏟️ Tabela de Jogos e Resultados em Tempo Real</h4>", unsafe_allow_html=True)
            filtro_dia = st.selectbox("📅 Filtrar Jogos por Data", sorted(list(set([j["Data"] for j in JOGOS_CADASTRADOS])), key=lambda x: x[:5]), key="filtro_jogos_dia")
            
            jogos_filtrados = [j for j in JOGOS_CADASTRADOS if j["Data"] == filtro_dia]
            
            for j in jogos_filtrados:
                jogo_id = j["ID_Jogo"]
                info_real = res_map.get(jogo_id, {"m": None, "v": None, "status": "Agendado"})
                status_real = info_real["status"]
                
                status_badge = "🕒 Agendado"
                if "Encerrado" in status_real:
                    status_badge = "🟢 Encerrado"
                elif "Ao Vivo" in status_real or "Andamento" in status_real:
                    status_badge = "🔴 Ao Vivo"
                
                with st.container(border=True):
                    # Topo do Card
                    col_t1, col_t2 = st.columns([3, 1])
                    with col_t1:
                        st.markdown(f"**🏆 Fase de Grupos** • {j['Data']}")
                    with col_t2:
                        st.markdown(f"<p style='text-align:right; margin:0; font-weight:800; color:#E05315;'>{status_badge}</p>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    col_team_m, col_score, col_team_v = st.columns([3, 2, 3])
                    
                    with col_team_m:
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 100px;">
                                <img src="https://flagcdn.com/w160/{j['ISO_M']}.png" style="width:65px; border-radius:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.1);">
                                <div style="color:#3C332E; font-size:1.1rem; font-weight:800; margin-top:8px;">{j['Time_M']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_score:
                        if "Encerrado" in status_real or "Ao Vivo" in status_real:
                            st.markdown(f"""
                                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100px;">
                                    <h1 style='text-align:center; margin:0; color:#3C332E; font-weight:800; font-size:2.4rem;'>{info_real['m']} - {info_real['v']}</h1>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100px;">
                                    <div style='text-align:center; padding:8px 12px; background:#FFFAE6; border:1.5px solid #E05315; border-radius:30px; font-weight:800; color:#3C332E; font-size:0.9rem;'>🕒 {j['Horário']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with col_team_v:
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 100px;">
                                <img src="https://flagcdn.com/w160/{j['ISO_V']}.png" style="width:65px; border-radius:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.1);">
                                <div style="color:#3C332E; font-size:1.1rem; font-weight:800; margin-top:8px;">{j['Time_V']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    if jogo_id in user_bets:
                        palpite_u = user_bets[jogo_id]
                        if "Encerrado" in status_real:
                            pts, tipo_acerto = calcular_pontos_palpite(palpite_u, info_real["m"], info_real["v"])
                            if tipo_acerto == "Exato":
                                badge_pontos = f"<span style='background-color:#7CA613; color:#FFFFFF; padding:0.35rem 0.85rem; border-radius:30px; font-weight:800; font-size:0.8rem;'>⭐ +10 pts (Placar Exato)</span>"
                            elif tipo_acerto == "Vencedor":
                                badge_pontos = f"<span style='background-color:#D972CD; color:#FFFFFF; padding:0.35rem 0.85rem; border-radius:30px; font-weight:800; font-size:0.8rem;'>⭐ +5 pts (Vencedor)</span>"
                            else:
                                badge_pontos = f"<span style='background-color:#FFFDF5; border:1px solid #E05315; color:#E05315; padding:0.35rem 0.85rem; border-radius:30px; font-weight:800; font-size:0.8rem;'>❌ 0 pts (Errou)</span>"
                            
                            st.markdown(f"<div style='margin-top:1.25rem; text-align:center; font-size:0.9rem;'>Seu palpite: <strong>{palpite_u}</strong> • {badge_pontos}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='margin-top:1.25rem; text-align:center; font-size:0.9rem; color:#3C332E;'>Seu palpite salvo: <strong style='color:#E05315; background:#FFFFFF; border:1px solid #E05315; padding:0.2rem 0.6rem; border-radius:30px;'>{palpite_u}</strong></div>", unsafe_allow_html=True)
                    elif st.session_state.saved_email:
                        st.markdown("<div style='margin-top:1.25rem; text-align:center; font-size:0.9rem; color:#E05315; font-weight:700;'>⚠️ Você ainda não palpitou nesta partida!</div>", unsafe_allow_html=True)

# --- CONTEÚDO DA ABA 2: REGISTRAR PALPITES ---
with tab_palpites:
    st.markdown('<div class="hero-title">📝 Registrar Meus Palpites</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Insira o seu perfil para liberar e palpitar de forma dinâmica e reativa</div>', unsafe_allow_html=True)
    
    # Perfil e Login do Colaborador
    if not st.session_state.saved_email or not st.session_state.saved_name:
        with st.container(border=True):
            st.markdown("<h4 style='color:#3C332E; font-weight:800;'>👤 1. Identificação de Acesso</h4>", unsafe_allow_html=True)
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                email_input = st.text_input("E-mail Corporativo", placeholder="Ex: joao.silva@feltrim.com", key="login_email").strip().lower()
            with col_p2:
                nome_input = st.text_input("Nome Completo", placeholder="Ex: João Silva", key="login_nome").strip()
                
            if st.button("🔓 Desbloquear Painel de Palpites", use_container_width=True, key="login_btn"):
                if email_input and "@" in email_input and "." in email_input and nome_input:
                    st.session_state.saved_email = email_input
                    st.session_state.saved_name = nome_input
                    st.success("Painel de palpites desbloqueado!")
                    st.rerun()
                else:
                    st.error("Por favor, digite um e-mail corporativo válido e o seu nome completo.")
    else:
        # Card Elegante de Identificação do Colaborador Ativo
        st.markdown(f"""
        <div class="profile-banner">
            <div>
                <span style="font-size:0.85rem; text-transform:uppercase; font-weight:800; opacity:0.8; color:#E05315;">Colaborador Conectado</span>
                <div style="font-size:1.4rem; font-weight:800; margin-top:2px;">⚽ {st.session_state.saved_name}</div>
                <span style="font-size:0.85rem; opacity:0.9;">{st.session_state.saved_email}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Cruzamento de palpites já feitos para evitar repetições na lista de pendentes
        lista_jogos_betted = set()
        if df_p is not None and not df_p.empty:
            email_col_name = None
            for c in df_p.columns:
                if "email" in c.lower() or "e-mail" in c.lower() or "usuário" in c.lower():
                    email_col_name = c
                    break
            
            if email_col_name:
                user_row = df_p[df_p[email_col_name].astype(str).str.strip().str.lower() == st.session_state.saved_email]
                if not user_row.empty:
                    for jogo_item in JOGOS_CADASTRADOS:
                        nome_jogo = jogo_item["Jogo"]
                        if nome_jogo in df_p.columns:
                            val = str(user_row[nome_jogo].values[0]).strip()
                            if val and val != "nan" and "-" in val:
                                lista_jogos_betted.add(nome_jogo)

        # Filtragem de partidas disponíveis para o usuário (FILTRAGEM DE SEGURANÇA AVANÇADA)
        jogos_disponiveis = []
        res_map = obter_resultado_map(df_r)

        for j in JOGOS_CADASTRADOS:
            nome_jogo = j["Jogo"]
            jogo_id = j["ID_Jogo"]
            
            # 1. Se o colaborador já deu palpite neste jogo, pula.
            if nome_jogo in lista_jogos_betted:
                continue
                
            # 2. Se a hora do jogo já passou no fuso horário BRT, pula.
            if jogo_ja_passou(j["Data"], j["Horário"]):
                continue
                
            # 3. Se o administrador já fechou o jogo (Status na planilha), pula.
            info_real = res_map.get(jogo_id, {"status": "Agendado"})
            status_real = info_real.get("status", "Agendado")
            if "Encerrado" in status_real or "Ao Vivo" in status_real or "Andamento" in status_real:
                continue
                
            jogos_disponiveis.append(j)
        
        st.markdown("---")
        st.markdown(f"<h4 style='color:#3C332E; font-weight:800;'>🏟️ Seus Palpites Disponíveis ({len(jogos_disponiveis)} jogos restantes)</h4>", unsafe_allow_html=True)
        
        if len(jogos_disponiveis) == 0:
            st.success("🏆 Espetacular! Não há nenhum palpite elegível pendente de envio para o seu perfil!")
        else:
            # Seletor de Data para organizar a tela
            datas_disponiveis = sorted(list(set([j["Data"] for j in jogos_disponiveis])), key=lambda x: x[:5])
            
            dia_selecionado = st.selectbox(
                "📅 Escolha uma Data da Copa para Visualizar as Partidas do Dia",
                options=datas_disponiveis,
                key="filtro_palpites_dia"
            )
            
            jogos_do_dia = [j for j in jogos_disponiveis if j["Data"] == dia_selecionado]
            
            for jogo in jogos_do_dia:
                with st.container(border=True):
                    # Cabeçalho Interno do Card
                    col_h1, col_h2 = st.columns([2, 1])
                    with col_h1:
                        st.markdown("**🏆 Rodada de Grupos**")
                    with col_h2:
                        st.markdown(f"<p style='text-align:right; margin:0; font-weight:700; color:#E05315;'>🕒 {jogo['Horário']}</p>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    col_m, col_vs, col_v = st.columns([3, 1, 3])
                    
                    with col_m:
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 120px;">
                                <img src="https://flagcdn.com/w160/{jogo['ISO_M']}.png" style="width:65px; border-radius:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.1);">
                                <div style="color:#3C332E; font-size:1.1rem; font-weight:800; margin-top:8px; margin-bottom: 4px;">{jogo['Time_M']}</div>
                                <div style="font-size:0.85rem; color:#E05315; font-weight:700;">Gols Mandante</div>
                            </div>
                        """, unsafe_allow_html=True)
                        gols_m = st.number_input("Gols Mandante", min_value=0, max_value=20, value=0, key=f"m_{jogo['ID_Jogo']}", step=1, label_visibility="collapsed")
                        
                    with col_vs:
                        st.markdown("<div style='display: flex; flex-direction: column; justify-content: center; align-items: center; height: 165px; font-size: 1.8rem; font-weight: 800; color:#3C332E;'>x</div>", unsafe_allow_html=True)
                        
                    with col_v:
                        st.markdown(f"""
                            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 120px;">
                                <img src="https://flagcdn.com/w160/{jogo['ISO_V']}.png" style="width:65px; border-radius:8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.1);">
                                <div style="color:#3C332E; font-size:1.1rem; font-weight:800; margin-top:8px; margin-bottom: 4px;">{jogo['Time_V']}</div>
                                <div style="font-size:0.85rem; color:#D972CD; font-weight:700;">Gols Visitante</div>
                            </div>
                        """, unsafe_allow_html=True)
                        gols_v = st.number_input("Gols Visitante", min_value=0, max_value=20, value=0, key=f"v_{jogo['ID_Jogo']}", step=1, label_visibility="collapsed")
                    
                    # Botão de envio integrado no rodapé de cada card de forma super elegante
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"🚀 Confirmar Palpite: {jogo['Time_M']} x {jogo['Time_V']}", key=f"btn_{jogo['ID_Jogo']}", use_container_width=True):
                        payload = {
                            "action": "fazerPalpite",
                            "spreadsheet_id": st.session_state.spreadsheet_id,
                            "email": st.session_state.saved_email,
                            "nome": st.session_state.saved_name,
                            "id_jogo": jogo["ID_Jogo"],
                            "palpite": f"{gols_m}-{gols_v}"
                        }
                        with st.spinner("Gravando palpite na planilha..."):
                            try:
                                r = requests.post(
                                    st.session_state.web_app_url,
                                    data=json.dumps(payload),
                                    headers={"Content-Type": "application/json"}
                                )
                                resp_json = r.json()
                                if resp_json.get("status") == "success":
                                    st.success("Palpite registrado com sucesso!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Erro na gravação: {resp_json.get('message')}")
                            except Exception as e:
                                st.error(f"Inconsistência de comunicação: {str(e)}")

# --- CONTEÚDO DA ABA 3: ADMINISTRAÇÃO ---
with tab_admin:
    st.markdown('<div class="hero-title">🔧 Portal de Controle</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Configurações globais e banco de dados reservado ao Administrador</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        senha_digitada = st.text_input("Senha Administrativa", type="password", key="admin_senha")
        
        if senha_digitada == "feltrim2026":
            st.success("Acesso administrativo desbloqueado com sucesso!")
            
            st.markdown("<h4 style='color:#3C332E; font-weight:800;'>🔗 Endereçamento e Conexões com Planilhas Google</h4>", unsafe_allow_html=True)
            novo_id = st.text_input("ID do Google Sheets", value=st.session_state.spreadsheet_id, key="sheets_id_input")
            nova_url = st.text_input("URL do App da Web (Google Apps Script)", value=st.session_state.web_app_url, key="web_app_url_input")
            
            if st.button("💾 Salvar Novas Configurações de Conexão", use_container_width=True, key="save_conn_btn"):
                st.session_state.spreadsheet_id = novo_id
                st.session_state.web_app_url = nova_url
                st.success("Chaves de conexão atualizadas localmente!")
                st.cache_data.clear()
                st.rerun()
                
            st.markdown("---")
            st.markdown("<h4 style='color:#3C332E; font-weight:800;'>🧪 Painel de Diagnóstico em Tempo Real</h4>", unsafe_allow_html=True)
            if st.button("Executar Testes de Comunicação", use_container_width=True, key="ping_test_btn"):
                with st.spinner("Verificando integridade da API..."):
                    try:
                        payload = {"action": "testPing", "spreadsheet_id": st.session_state.spreadsheet_id}
                        r = requests.post(
                            st.session_state.web_app_url,
                            data=json.dumps(payload),
                            headers={"Content-Type": "application/json"}
                        )
                        if r.status_code == 200:
                            st.json(r.json())
                            st.success("A ponte de comunicação e a planilha estão ativas e sincronizadas de forma perfeita!")
                        else:
                            st.error(f"Erro de conexão. Código de erro HTTP: {r.status_code}")
                    except Exception as ex:
                        st.error(f"Não foi possível conectar: {str(ex)}")
                        
            st.markdown("---")
            st.markdown("<h4 style='color:#3C332E; font-weight:800;'>🚀 Ações Globais e em Lote</h4>", unsafe_allow_html=True)
            if st.button("⚡ Inicializar Todos os 72 Jogos na Planilha", use_container_width=True, key="batch_init_btn"):
                with st.spinner("Apagando registros obsoletos e recriando tabela oficial..."):
                    payload = {
                        "action": "inicializarNovoBolao",
                        "spreadsheet_id": st.session_state.spreadsheet_id,
                        "senha": "feltrim2026"
                    }
                    try:
                        r = requests.post(
                            st.session_state.web_app_url,
                            data=json.dumps(payload),
                            headers={"Content-Type": "application/json"}
                        )
                        st.json(r.json())
                        st.cache_data.clear()
                        st.success("Comando enviado! Verifique as abas criadas na sua planilha do Google.")
                    except Exception as e:
                        st.error(f"Falha de lote: {str(e)}")

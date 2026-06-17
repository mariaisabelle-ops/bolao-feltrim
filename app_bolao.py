import streamlit as st
import pandas as pd
import requests
import json

# ==========================================
# 🏆 1. LISTA OFICIAL CRONOLÓGICA DE 72 JOGOS
# ==========================================
JOGOS_CADASTRADOS = [
    # --- 11/06 ---
    {"ID_Jogo": "JOGO_01", "Jogo": "⚽ México vs África do Sul (11/06)", "Horário": "15:00", "Data": "11/06 (Quinta)", "Time_M": "México", "Emoji_M": "🇲🇽", "Time_V": "África do Sul", "Emoji_V": "🇿🇦"},
    {"ID_Jogo": "JOGO_02", "Jogo": "⚽ Coreia do Sul vs Tchéquia (11/06)", "Horário": "22:00", "Data": "11/06 (Quinta)", "Time_M": "Coreia do Sul", "Emoji_M": "🇰🇷", "Time_V": "Tchéquia", "Emoji_V": "🇨🇿"},

    # --- 12/06 ---
    {"ID_Jogo": "JOGO_03", "Jogo": "⚽ Canadá vs Bósnia e Herzegovina (12/06)", "Horário": "15:00", "Data": "12/06 (Sexta)", "Time_M": "Canadá", "Emoji_M": "🇨🇦", "Time_V": "Bósnia e Herzegovina", "Emoji_V": "🇧🇦"},
    {"ID_Jogo": "JOGO_04", "Jogo": "⚽ Estados Unidos vs Paraguai (12/06)", "Horário": "21:00", "Data": "12/06 (Sexta)", "Time_M": "Estados Unidos", "Emoji_M": "🇺🇸", "Time_V": "Paraguai", "Emoji_V": "🇵🇾"},

    # --- 13/06 ---
    {"ID_Jogo": "JOGO_05", "Jogo": "⚽ Catar vs Suíça (13/06)", "Horário": "15:00", "Data": "13/06 (Sábado)", "Time_M": "Catar", "Emoji_M": "🇶🇦", "Time_V": "Suíça", "Emoji_V": "🇨🇭"},
    {"ID_Jogo": "JOGO_06", "Jogo": "⚽ Brasil vs Marrocos (13/06)", "Horário": "18:00", "Data": "13/06 (Sábado)", "Time_M": "Brasil", "Emoji_M": "🇧🇷", "Time_V": "Marrocos", "Emoji_V": "🇲🇦"},
    {"ID_Jogo": "JOGO_07", "Jogo": "⚽ Haiti vs Escócia (13/06)", "Horário": "21:00", "Data": "13/06 (Sábado)", "Time_M": "Haiti", "Emoji_M": "🇭🇹", "Time_V": "Escócia", "Emoji_V": "⚽"},

    # --- 14/06 ---
    {"ID_Jogo": "JOGO_08", "Jogo": "⚽ Austrália vs Turquia (14/06)", "Horário": "00:00", "Data": "14/06 (Domingo)", "Time_M": "Austrália", "Emoji_M": "🇦🇺", "Time_V": "Turquia", "Emoji_V": "🇹🇷"},
    {"ID_Jogo": "JOGO_09", "Jogo": "⚽ Alemanha vs Curaçao (14/06)", "Horário": "13:00", "Data": "14/06 (Domingo)", "Time_M": "Alemanha", "Emoji_M": "🇩🇪", "Time_V": "Curaçao", "Emoji_V": "🇨🇼"},
    {"ID_Jogo": "JOGO_10", "Jogo": "⚽ Holanda vs Japão (14/06)", "Horário": "16:00", "Data": "14/06 (Domingo)", "Time_M": "Holanda", "Emoji_M": "🇳🇱", "Time_V": "Japão", "Emoji_V": "🇯🇵"},
    {"ID_Jogo": "JOGO_11", "Jogo": "⚽ Costa do Marfim vs Equador (14/06)", "Horário": "19:00", "Data": "14/06 (Domingo)", "Time_M": "Costa do Marfim", "Emoji_M": "🇨🇮", "Time_V": "Equador", "Emoji_V": "🇪🇨"},
    {"ID_Jogo": "JOGO_12", "Jogo": "⚽ Suécia vs Tunísia (14/06)", "Horário": "22:00", "Data": "14/06 (Domingo)", "Time_M": "Suécia", "Emoji_M": "🇸🇪", "Time_V": "Tunísia", "Emoji_V": "🇹🇳"},

    # --- 15/06 ---
    {"ID_Jogo": "JOGO_13", "Jogo": "⚽ Espanha vs Cabo Verde (15/06)", "Horário": "12:00", "Data": "15/06 (Segunda)", "Time_M": "Espanha", "Emoji_M": "🇪🇸", "Time_V": "Cabo Verde", "Emoji_V": "🇨🇻"},
    {"ID_Jogo": "JOGO_14", "Jogo": "⚽ Bélgica vs Egito (15/06)", "Horário": "15:00", "Data": "15/06 (Segunda)", "Time_M": "Bélgica", "Emoji_M": "🇧🇪", "Time_V": "Egito", "Emoji_V": "🇪🇬"},
    {"ID_Jogo": "JOGO_15", "Jogo": "⚽ Arábia Saudita vs Uruguai (15/06)", "Horário": "18:00", "Data": "15/06 (Segunda)", "Time_M": "Arábia Saudita", "Emoji_M": "🇸🇦", "Time_V": "Uruguai", "Emoji_V": "🇺🇾"},
    {"ID_Jogo": "JOGO_16", "Jogo": "⚽ Irã vs Nova Zelândia (15/06)", "Horário": "21:00", "Data": "15/06 (Segunda)", "Time_M": "Irã", "Emoji_M": "🇮🇷", "Time_V": "Nova Zelândia", "Emoji_V": "🇳🇿"},

    # --- 16/06 ---
    {"ID_Jogo": "JOGO_17", "Jogo": "⚽ França vs Senegal (16/06)", "Horário": "15:00", "Data": "16/06 (Terça)", "Time_M": "França", "Emoji_M": "🇫🇷", "Time_V": "Senegal", "Emoji_V": "🇸🇳"},
    {"ID_Jogo": "JOGO_18", "Jogo": "⚽ Iraque vs Noruega (16/06)", "Horário": "18:00", "Data": "16/06 (Terça)", "Time_M": "Iraque", "Emoji_M": "🇮🇶", "Time_V": "Noruega", "Emoji_V": "🇳🇴"},
    {"ID_Jogo": "JOGO_19", "Jogo": "⚽ Argentina vs Argélia (16/06)", "Horário": "21:00", "Data": "16/06 (Terça)", "Time_M": "Argentina", "Emoji_M": "🇦🇷", "Time_V": "Argélia", "Emoji_V": "🇩🇿"},

    # --- 17/06 ---
    {"ID_Jogo": "JOGO_20", "Jogo": "⚽ Áustria vs Jordânia (17/06)", "Horário": "00:00", "Data": "17/06 (Quarta)", "Time_M": "Áustria", "Emoji_M": "🇦🇹", "Time_V": "Jordânia", "Emoji_V": "🇯🇴"},
    {"ID_Jogo": "JOGO_21", "Jogo": "⚽ Portugal vs RD Congo (17/06)", "Horário": "13:00", "Data": "17/06 (Quarta)", "Time_M": "Portugal", "Emoji_M": "🇵🇹", "Time_V": "RD Congo", "Emoji_V": "🇨🇩"},
    {"ID_Jogo": "JOGO_22", "Jogo": "⚽ Inglaterra vs Croácia (17/06)", "Horário": "16:00", "Data": "17/06 (Quarta)", "Time_M": "Inglaterra", "Emoji_M": "⚽", "Time_V": "Croácia", "Emoji_V": "🇭🇷"},
    {"ID_Jogo": "JOGO_23", "Jogo": "⚽ Gana vs Panamá (17/06)", "Horário": "19:00", "Data": "17/06 (Quarta)", "Time_M": "Gana", "Emoji_M": "🇬🇭", "Time_V": "Panamá", "Emoji_V": "🇵🇦"},
    {"ID_Jogo": "JOGO_24", "Jogo": "⚽ Uzbequistão vs Colômbia (17/06)", "Horário": "22:00", "Data": "17/06 (Quarta)", "Time_M": "Uzbequistão", "Emoji_M": "🇺🇿", "Time_V": "Colômbia", "Emoji_V": "🇨🇴"},

    # --- 18/06 ---
    {"ID_Jogo": "JOGO_25", "Jogo": "⚽ Tchéquia vs África do Sul (18/06)", "Horário": "12:00", "Data": "18/06 (Quinta)", "Time_M": "Tchéquia", "Emoji_M": "🇨🇿", "Time_V": "África do Sul", "Emoji_V": "🇿🇦"},
    {"ID_Jogo": "JOGO_26", "Jogo": "⚽ Suíça vs Bósnia e Herzegovina (18/06)", "Horário": "15:00", "Data": "18/06 (Quinta)", "Time_M": "Suíça", "Emoji_M": "🇨🇭", "Time_V": "Bósnia e Herzegovina", "Emoji_V": "🇧🇦"},
    {"ID_Jogo": "JOGO_27", "Jogo": "⚽ Canadá vs Catar (18/06)", "Horário": "18:00", "Data": "18/06 (Quinta)", "Time_M": "Canadá", "Emoji_M": "🇨🇦", "Time_V": "Catar", "Emoji_V": "🇶🇦"},
    {"ID_Jogo": "JOGO_28", "Jogo": "⚽ México vs Coreia do Sul (18/06)", "Horário": "21:00", "Data": "18/06 (Quinta)", "Time_M": "México", "Emoji_M": "🇲🇽", "Time_V": "Coreia do Sul", "Emoji_V": "🇰🇷"},

    # --- 19/06 ---
    {"ID_Jogo": "JOGO_29", "Jogo": "⚽ Estados Unidos vs Austrália (19/06)", "Horário": "15:00", "Data": "19/06 (Sexta)", "Time_M": "Estados Unidos", "Emoji_M": "🇺🇸", "Time_V": "Austrália", "Emoji_V": "🇦🇺"},
    {"ID_Jogo": "JOGO_30", "Jogo": "⚽ Escócia vs Marrocos (19/06)", "Horário": "18:00", "Data": "19/06 (Sexta)", "Time_M": "Escócia", "Emoji_M": "⚽", "Time_V": "Marrocos", "Emoji_V": "🇲🇦"},
    {"ID_Jogo": "JOGO_31", "Jogo": "⚽ Brasil vs Haiti (19/06)", "Horário": "21:30", "Data": "19/06 (Sexta)", "Time_M": "Brasil", "Emoji_M": "🇧🇷", "Time_V": "Haiti", "Emoji_V": "🇭🇹"},
    {"ID_Jogo": "JOGO_32", "Jogo": "⚽ Turquia vs Paraguai (19/06)", "Horário": "23:00", "Data": "19/06 (Sexta)", "Time_M": "Turquia", "Emoji_M": "🇹🇷", "Time_V": "Paraguai", "Emoji_V": "🇵🇾"},

    # --- 20/06 ---
    {"ID_Jogo": "JOGO_33", "Jogo": "⚽ Holanda vs Suécia (20/06)", "Horário": "13:00", "Data": "20/06 (Sábado)", "Time_M": "Holanda", "Emoji_M": "🇳🇱", "Time_V": "Suécia", "Emoji_V": "🇸🇪"},
    {"ID_Jogo": "JOGO_34", "Jogo": "⚽ Alemanha vs Costa do Marfim (20/06)", "Horário": "16:00", "Data": "20/06 (Sábado)", "Time_M": "Alemanha", "Emoji_M": "🇩🇪", "Time_V": "Costa do Marfim", "Emoji_V": "🇨🇮"},
    {"ID_Jogo": "JOGO_35", "Jogo": "⚽ Equador vs Curaçao (20/06)", "Horário": "20:00", "Data": "20/06 (Sábado)", "Time_M": "Equador", "Emoji_M": "🇪🇨", "Time_V": "Curaçao", "Emoji_V": "🇨🇼"},

    # --- 21/06 ---
    {"ID_Jogo": "JOGO_36", "Jogo": "⚽ Tunísia vs Japão (21/06)", "Horário": "00:00", "Data": "21/06 (Domingo)", "Time_M": "Tunísia", "Emoji_M": "🇹🇳", "Time_V": "Japão", "Emoji_V": "🇯🇵"},
    {"ID_Jogo": "JOGO_37", "Jogo": "⚽ Espanha vs Arábia Saudita (21/06)", "Horário": "12:00", "Data": "21/06 (Domingo)", "Time_M": "Espanha", "Emoji_M": "🇪🇸", "Time_V": "Arábia Saudita", "Emoji_V": "🇸🇦"},
    {"ID_Jogo": "JOGO_38", "Jogo": "⚽ Bélgica vs Irã (21/06)", "Horário": "15:00", "Data": "21/06 (Domingo)", "Time_M": "Bélgica", "Emoji_M": "🇧🇪", "Time_V": "Irã", "Emoji_V": "🇮🇷"},
    {"ID_Jogo": "JOGO_39", "Jogo": "⚽ Uruguai vs Cabo Verde (21/06)", "Horário": "18:00", "Data": "21/06 (Domingo)", "Time_M": "Uruguai", "Emoji_M": "🇺🇾", "Time_V": "Cabo Verde", "Emoji_V": "🇨🇻"},
    {"ID_Jogo": "JOGO_40", "Jogo": "⚽ Nova Zelândia vs Egito (21/06)", "Horário": "21:00", "Data": "21/06 (Domingo)", "Time_M": "Nova Zelândia", "Emoji_M": "🇳🇿", "Time_V": "Egito", "Emoji_V": "🇪🇬"},

    # --- 22/06 ---
    {"ID_Jogo": "JOGO_41", "Jogo": "⚽ Argentina vs Áustria (22/06)", "Horário": "13:00", "Data": "22/06 (Segunda)", "Time_M": "Argentina", "Emoji_M": "🇦🇷", "Time_V": "Áustria", "Emoji_V": "🇦🇹"},
    {"ID_Jogo": "JOGO_42", "Jogo": "⚽ França vs Iraque (22/06)", "Horário": "17:00", "Data": "22/06 (Segunda)", "Time_M": "França", "Emoji_M": "🇫🇷", "Time_V": "Iraque", "Emoji_V": "🇮🇶"},
    {"ID_Jogo": "JOGO_43", "Jogo": "⚽ Noruega vs Senegal (22/06)", "Horário": "20:00", "Data": "22/06 (Segunda)", "Time_M": "Noruega", "Emoji_M": "🇳🇴", "Time_V": "Senegal", "Emoji_V": "🇸🇳"},
    {"ID_Jogo": "JOGO_44", "Jogo": "⚽ Jordânia vs Argélia (22/06)", "Horário": "23:00", "Data": "22/06 (Segunda)", "Time_M": "Jordânia", "Emoji_M": "🇯🇴", "Time_V": "Argélia", "Emoji_V": "🇩🇿"},

    # --- 23/06 ---
    {"ID_Jogo": "JOGO_45", "Jogo": "⚽ Portugal vs Uzbequistão (23/06)", "Horário": "13:00", "Data": "23/06 (Terça)", "Time_M": "Portugal", "Emoji_M": "🇵🇹", "Time_V": "Uzbequistão", "Emoji_V": "🇺🇿"},
    {"ID_Jogo": "JOGO_46", "Jogo": "⚽ Inglaterra vs Gana (23/06)", "Horário": "16:00", "Data": "23/06 (Terça)", "Time_M": "Inglaterra", "Emoji_M": "⚽", "Time_V": "Gana", "Emoji_V": "🇬🇭"},
    {"ID_Jogo": "JOGO_47", "Jogo": "⚽ Panamá vs Croácia (23/06)", "Horário": "19:00", "Data": "23/06 (Terça)", "Time_M": "Panamá", "Emoji_M": "🇵🇦", "Time_V": "Croácia", "Emoji_V": "🇭🇷"},
    {"ID_Jogo": "JOGO_48", "Jogo": "⚽ Colômbia vs RD Congo (23/06)", "Horário": "22:00", "Data": "23/06 (Terça)", "Time_M": "Colômbia", "Emoji_M": "🇨🇴", "Time_V": "RD Congo", "Emoji_V": "🇨🇩"},

    # --- 24/06 ---
    {"ID_Jogo": "JOGO_49", "Jogo": "⚽ Suíça vs Canadá (24/06)", "Horário": "15:00", "Data": "24/06 (Quarta)", "Time_M": "Suíça", "Emoji_M": "🇨🇭", "Time_V": "Canadá", "Emoji_V": "🇨🇦"},
    {"ID_Jogo": "JOGO_50", "Jogo": "⚽ Bósnia e Herzegovina vs Catar (24/06)", "Horário": "15:00", "Data": "24/06 (Quarta)", "Time_M": "Bósnia e Herzegovina", "Emoji_M": "🇧🇦", "Time_V": "Catar", "Emoji_V": "🇶🇦"},
    {"ID_Jogo": "JOGO_51", "Jogo": "⚽ Escócia vs Brasil (24/06)", "Horário": "18:00", "Data": "24/06 (Quarta)", "Time_M": "Escócia", "Emoji_M": "⚽", "Time_V": "Brasil", "Emoji_V": "🇧🇷"},
    {"ID_Jogo": "JOGO_52", "Jogo": "⚽ Marrocos vs Haiti (24/06)", "Horário": "18:00", "Data": "24/06 (Quarta)", "Time_M": "Marrocos", "Emoji_M": "🇲🇦", "Time_V": "Haiti", "Emoji_V": "🇭🇹"},
    {"ID_Jogo": "JOGO_53", "Jogo": "⚽ Tchéquia vs México (24/06)", "Horário": "21:00", "Data": "24/06 (Quarta)", "Time_M": "Tchéquia", "Emoji_M": "🇨🇿", "Time_V": "México", "Emoji_V": "🇲🇽"},
    {"ID_Jogo": "JOGO_54", "Jogo": "⚽ África do Sul vs Coreia do Sul (24/06)", "Horário": "21:00", "Data": "24/06 (Quarta)", "Time_M": "África do Sul", "Emoji_M": "🇿🇦", "Time_V": "Coreia do Sul", "Emoji_V": "🇰🇷"},

    # --- 25/06 ---
    {"ID_Jogo": "JOGO_55", "Jogo": "⚽ Equador vs Alemanha (25/06)", "Horário": "16:00", "Data": "25/06 (Quinta)", "Time_M": "Equador", "Emoji_M": "🇪🇨", "Time_V": "Alemanha", "Emoji_V": "🇩🇪"},
    {"ID_Jogo": "JOGO_56", "Jogo": "⚽ Curaçao vs Costa do Marfim (25/06)", "Horário": "16:00", "Data": "25/06 (Quinta)", "Time_M": "Curaçao", "Emoji_M": "🇨🇼", "Time_V": "Costa do Marfim", "Emoji_V": "🇨🇮"},
    {"ID_Jogo": "JOGO_57", "Jogo": "⚽ Tunísia vs Holanda (25/06)", "Horário": "19:00", "Data": "25/06 (Quinta)", "Time_M": "Tunísia", "Emoji_M": "🇹🇳", "Time_V": "Holanda", "Emoji_V": "🇳🇱"},
    {"ID_Jogo": "JOGO_58", "Jogo": "⚽ Japão vs Suécia (25/06)", "Horário": "19:00", "Data": "25/06 (Quinta)", "Time_M": "Japão", "Emoji_M": "🇯🇵", "Time_V": "Suécia", "Emoji_V": "🇸🇪"},
    {"ID_Jogo": "JOGO_59", "Jogo": "⚽ Turquia vs Estados Unidos (25/06)", "Horário": "22:00", "Data": "25/06 (Quinta)", "Time_M": "Turquia", "Emoji_M": "🇹🇷", "Time_V": "Estados Unidos", "Emoji_V": "🇺🇸"},
    {"ID_Jogo": "JOGO_60", "Jogo": "⚽ Paraguai vs Austrália (25/06)", "Horário": "22:00", "Data": "25/06 (Quinta)", "Time_M": "Paraguai", "Emoji_M": "🇵🇾", "Time_V": "Austrália", "Emoji_V": "🇦🇺"},

    # --- 26/06 ---
    {"ID_Jogo": "JOGO_61", "Jogo": "⚽ Noruega vs França (26/06)", "Horário": "15:00", "Data": "26/06 (Sexta)", "Time_M": "Noruega", "Emoji_M": "🇳🇴", "Time_V": "França", "Emoji_V": "🇫🇷"},
    {"ID_Jogo": "JOGO_62", "Jogo": "⚽ Senegal vs Iraque (26/06)", "Horário": "15:00", "Data": "26/06 (Sexta)", "Time_M": "Senegal", "Emoji_M": "🇸🇳", "Time_V": "Iraque", "Emoji_V": "🇮🇶"},
    {"ID_Jogo": "JOGO_63", "Jogo": "⚽ Uruguai vs Espanha (26/06)", "Horário": "20:00", "Data": "26/06 (Sexta)", "Time_M": "Uruguai", "Emoji_M": "🇺🇾", "Time_V": "Espanha", "Emoji_V": "🇪🇸"},
    {"ID_Jogo": "JOGO_64", "Jogo": "⚽ Cabo Verde vs Arábia Saudita (26/06)", "Horário": "20:00", "Data": "26/06 (Sexta)", "Time_M": "Cabo Verde", "Emoji_M": "🇨🇻", "Time_V": "Arábia Saudita", "Emoji_V": "🇸🇦"},
    {"ID_Jogo": "JOGO_65", "Jogo": "⚽ Nova Zelândia vs Bélgica (26/06)", "Horário": "23:00", "Data": "26/06 (Sexta)", "Time_M": "Nova Zelândia", "Emoji_M": "🇳🇿", "Time_V": "Bélgica", "Emoji_V": "🇧🇪"},
    {"ID_Jogo": "JOGO_66", "Jogo": "⚽ Egito vs Irã (26/06)", "Horário": "23:00", "Data": "26/06 (Sexta)", "Time_M": "Egito", "Emoji_M": "🇪🇬", "Time_V": "Irã", "Emoji_V": "🇮🇷"},

    # --- 27/06 ---
    {"ID_Jogo": "JOGO_67", "Jogo": "⚽ Panamá vs Inglaterra (27/06)", "Horário": "17:00", "Data": "27/06 (Sábado)", "Time_M": "Panamá", "Emoji_M": "🇵🇦", "Time_V": "Inglaterra", "Emoji_V": "⚽"},
    {"ID_Jogo": "JOGO_68", "Jogo": "⚽ Croácia vs Gana (27/06)", "Horário": "17:00", "Data": "27/06 (Sábado)", "Time_M": "Croácia", "Emoji_M": "🇭🇷", "Time_V": "Gana", "Emoji_V": "🇬🇭"},
    {"ID_Jogo": "JOGO_69", "Jogo": "⚽ Colômbia vs Portugal (27/06)", "Horário": "19:30", "Data": "27/06 (Sábado)", "Time_M": "Colômbia", "Emoji_M": "🇨🇴", "Time_V": "Portugal", "Emoji_V": "🇵🇹"},
    {"ID_Jogo": "JOGO_70", "Jogo": "⚽ RD Congo vs Uzbequistão (27/06)", "Horário": "19:30", "Data": "27/06 (Sábado)", "Time_M": "RD Congo", "Emoji_M": "🇨🇩", "Time_V": "Uzbequistão", "Emoji_V": "🇺🇿"},
    {"ID_Jogo": "JOGO_71", "Jogo": "⚽ Jordânia vs Argentina (27/06)", "Horário": "22:00", "Data": "27/06 (Sábado)", "Time_M": "Jordânia", "Emoji_M": "🇯🇴", "Time_V": "Argentina", "Emoji_V": "🇦🇷"},
    {"ID_Jogo": "JOGO_72", "Jogo": "⚽ Argélia vs Áustria (27/06)", "Horário": "22:00", "Data": "27/06 (Sábado)", "Time_M": "Argélia", "Emoji_M": "🇩🇿", "Time_V": "Áustria", "Emoji_V": "🇦🇹"}
]

# Configuração da página Streamlit
st.set_page_config(
    page_title="Feltrim Correa - Bolão Corporativo",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização de estados globais de conexão (salvamento dinâmico via Portal Admin)
if "spreadsheet_id" not in st.session_state:
    st.session_state.spreadsheet_id = "1QEDWCDuV0DRkVq86QQwC9Dr5x_KU209Eypu_hmFsdAc"
if "web_app_url" not in st.session_state:
    st.session_state.web_app_url = "https://script.google.com/macros/s/AKfycby4zNkmzBsq-vT1J4RQ7wf8qLN1vX0SFgEqjDCqOueoGR5GRuYW3RtmzEOBph4Pn_7Z/exec"

# Preservar dados de identificação do usuário
if "saved_email" not in st.session_state:
    st.session_state.saved_email = ""
if "saved_name" not in st.session_state:
    st.session_state.saved_name = ""

# Injeção de Estilos CSS customizados para UI Premium e Responsiva
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    
    /* Título Principal */
    .hero-title {
        font-weight: 800;
        font-size: 2.6rem;
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.1rem;
        letter-spacing: -0.05em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    
    /* Cards Gerais */
    .custom-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 30px rgba(15, 23, 42, 0.04);
        border: 1px solid #f1f5f9;
        margin-bottom: 1.5rem;
    }
    
    /* Perfil Conectado */
    .profile-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        border: 1px solid #334155;
    }
    
    /* Pódio de Classificação */
    .podium-section {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 1.5rem;
        margin: 2rem auto;
        max-width: 900px;
        padding: 1rem;
    }
    
    .podium-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }
    
    .podium-box {
        width: 100%;
        border-radius: 20px 20px 12px 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }
    
    .podium-box:hover {
        transform: translateY(-5px);
    }
    
    .gold-box {
        background: linear-gradient(135deg, #fef08a 0%, #eab308 100%);
        border: 2px solid #fde047;
        height: 240px;
        z-index: 3;
    }
    
    .silver-box {
        background: linear-gradient(135deg, #f1f5f9 0%, #cbd5e1 100%);
        border: 2px solid #e2e8f0;
        height: 190px;
        z-index: 2;
    }
    
    .bronze-box {
        background: linear-gradient(135deg, #ffedd5 0%, #ca8a04 100%);
        border: 2px solid #fed7aa;
        height: 160px;
        z-index: 1;
    }
    
    .avatar-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        color: #1e293b;
    }
    
    .podium-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    
    .podium-score {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
    }
    
    .badge-rank {
        position: absolute;
        top: -15px;
        padding: 0.25rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    
    /* Cards de Jogos Interativos */
    .match-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        border-color: #cbd5e1;
    }
    
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px dashed #e2e8f0;
    }
    
    .match-badge {
        background: #eff6ff;
        color: #2563eb;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        border: 1px solid #dbeafe;
    }
    
    .match-time {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .team-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .team-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
        width: 140px;
        text-align: center;
    }
    
    .team-flag {
        font-size: 2.2rem;
    }
    
    /* Estilização da Tabela de Classificação Premium */
    .premium-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 8px;
        margin-top: 1.5rem;
    }
    
    .premium-table th {
        background: #f1f5f9;
        color: #475569;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        padding: 1rem;
        border: none;
        text-align: left;
    }
    
    .premium-table th:first-child { border-radius: 8px 0 0 8px; }
    .premium-table th:last-child { border-radius: 0 8px 8px 0; }
    
    .premium-row {
        background: #ffffff;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(15,23,42,0.02);
    }
    
    .premium-row:hover {
        background: #f8fafc;
        transform: scale(1.005);
    }
    
    .premium-row td {
        padding: 1.2rem 1rem;
        border-top: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.95rem;
        color: #334155;
    }
    
    .premium-row td:first-child {
        border-left: 1px solid #f1f5f9;
        border-radius: 12px 0 0 12px;
        font-weight: 700;
    }
    
    .premium-row td:last-child {
        border-right: 1px solid #f1f5f9;
        border-radius: 0 12px 12px 0;
    }
    
    .rank-indicator {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    .rank-1 { background: #fef08a; color: #854d0e; }
    .rank-2 { background: #e2e8f0; color: #475569; }
    .rank-3 { background: #ffedd5; color: #9a3412; }
    .rank-other { background: #f1f5f9; color: #64748b; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/120/cup.png", width=60)
    st.markdown("### 🏆 Feltrim Correa")
    st.markdown("<small style='color:#64748b; font-weight:500;'>Copa do Mundo FIFA 2026</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    aba_selecionada = st.radio(
        "Menu de Navegação",
        ["📊 Classificação Geral", "📝 Registrar Palpites", "🔧 Portal de Controle"],
        key="menu_navegacao"
    )
    st.markdown("---")
    st.markdown("<small style='color:#94a3b8;'>Plataforma Premium V3.0</small>", unsafe_allow_html=True)

@st.cache_data(ttl=10)
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
                    
                    if jogo_id in resultado_map and "Encerrado" in resultado_map[jogo_id]["status"]:
                        res_real = resultado_map[jogo_id]
                        try:
                            parts = palpite.split("-")
                            pm, pv = int(parts[0].strip()), int(parts[1].strip())
                            rm, rv = res_real["m"], res_real["v"]
                            
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

# Carregamento automático dos dados da planilha conectada
df_p, df_r = carregar_dados_planilha(st.session_state.spreadsheet_id)

# ==========================================
# 📊 ABA 1: CLASSIFICAÇÃO GERAL
# ==========================================
if aba_selecionada == "📊 Classificação Geral":
    st.markdown('<div class="hero-title">🏆 Feltrim Correa</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Bolão Oficial da Copa do Mundo FIFA 2026</div>', unsafe_allow_html=True)
    
    if df_p is not None and df_r is not None:
        rank = calcular_ranking_real(df_p, df_r)
        
        if not rank.empty:
            # Renderização de Pódio HTML Volumétrico Premium
            p1_nome = rank.iloc[0]['Nome'] if len(rank) >= 1 else "Vago"
            p1_pontos = rank.iloc[0]['Pontos'] if len(rank) >= 1 else 0
            
            p2_nome = rank.iloc[1]['Nome'] if len(rank) >= 2 else "Vago"
            p2_pontos = rank.iloc[1]['Pontos'] if len(rank) >= 2 else 0
            
            p3_nome = rank.iloc[2]['Nome'] if len(rank) >= 3 else "Vago"
            p3_pontos = rank.iloc[2]['Pontos'] if len(rank) >= 3 else 0
            
            st.markdown(f"""<div class="podium-section">
<div class="podium-col">
<span class="badge-rank" style="background:#94a3b8;">2º Lugar</span>
<div class="avatar-circle">🥈</div>
<div class="podium-box silver-box">
<div class="podium-name">{p2_nome}</div>
<div class="podium-score">{p2_pontos} pts</div>
</div>
</div>
<div class="podium-col">
<span class="badge-rank" style="background:#eab308;">Líder do Pódio</span>
<div class="avatar-circle">👑</div>
<div class="podium-box gold-box">
<div class="podium-name" style="font-size:1.35rem; font-weight:800;">{p1_nome}</div>
<div class="podium-score" style="font-size:1.8rem;">{p1_pontos} pts</div>
</div>
</div>
<div class="podium-col">
<span class="badge-rank" style="background:#ea580c;">3º Lugar</span>
<div class="avatar-circle">🥉</div>
<div class="podium-box bronze-box">
<div class="podium-name">{p3_nome}</div>
<div class="podium-score">{p3_pontos} pts</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📊 Resultado Geral da Classificação")
            
            # Construindo Tabela HTML Customizada de Altíssima Performance e Visual Premium
            table_html = """
            <table class="premium-table">
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
                <tbody>
            """
            
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
                    
                table_html += f"""
                <tr class="premium-row">
                    <td style="text-align: center;">
                        <span class="rank-indicator {rank_class}">{badge}</span>
                    </td>
                    <td style="font-weight: 600; color: #0f172a;">{row['Nome']}</td>
                    <td style="text-align: center; font-weight: 500;">{row['Palpites Feitos']}</td>
                    <td style="text-align: center; color: #16a34a; font-weight: 600;">{row['Acertos Exatos']}</td>
                    <td style="text-align: center; color: #2563eb; font-weight: 600;">{row['Acertos Vencedor']}</td>
                    <td style="text-align: right; font-weight: 800; font-size: 1.1rem; color: #0f172a; padding-right: 1.5rem;">{row['Pontos']} pts</td>
                </tr>
                """
                
            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)
            
        else:
            st.info("Nenhum palpite foi cadastrado ainda! Registre os seus palpites na aba ao lado.")
    else:
        st.warning("""
        **Planilha Desconectada ou em Configuração!**  
        Seja bem-vindo ao Bolão Feltrim Correa. O administrador configurará o painel usando as diretrizes de acesso do Google.
        """)

# ==========================================
# 📝 ABA 2: REGISTRAR PALPITES (UX TOTALMENTE OTIMIZADA)
# ==========================================
elif aba_selecionada == "📝 Registrar Palpites":
    st.markdown('<div class="hero-title">📝 Enviar Meus Palpites</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Insira o seu perfil para desbloquear e palpitar de forma reativa</div>', unsafe_allow_html=True)
    
    # Seção 1: Controle de Identificação Premium
    if not st.session_state.saved_email or not st.session_state.saved_name:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 1. Identificação Inicial")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            email_input = st.text_input("E-mail Corporativo", placeholder="Ex: joao.silva@feltrim.com").strip().lower()
        with col_p2:
            nome_input = st.text_input("Nome Completo", placeholder="Ex: João Silva").strip()
            
        if st.button("🔓 Desbloquear Painel de Palpites", use_container_width=True):
            if email_input and "@" in email_input and "." in email_input and nome_input:
                st.session_state.saved_email = email_input
                st.session_state.saved_name = nome_input
                st.success("Painel de jogos desbloqueado com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, digite um e-mail corporativo válido e o seu nome completo.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Card de Perfil Ativo (Substitui os campos de texto para melhorar a UX)
        st.markdown(f"""
        <div class="profile-banner">
            <div>
                <span style="font-size:0.9rem; text-transform:uppercase; font-weight:700; opacity:0.8;">Perfil Ativo</span>
                <div style="font-size:1.4rem; font-weight:800; margin-top:2px;">⚽ {st.session_state.saved_name}</div>
                <span style="font-size:0.85rem; opacity:0.9;">{st.session_state.saved_email}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Alterar Colaborador conectado", type="secondary"):
            st.session_state.saved_email = ""
            st.session_state.saved_name = ""
            st.rerun()
            
        # Cruzamento de palpites já feitos para evitar repetições
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

        # Filtragem de partidas disponíveis para o usuário
        jogos_disponiveis = [j for j in JOGOS_CADASTRADOS if j["Jogo"] not in lista_jogos_betted]
        
        st.markdown("---")
        st.markdown(f"### 🏟️ Seus Palpites Disponíveis ({len(jogos_disponiveis)} jogos restantes)")
        
        if len(jogos_disponiveis) == 0:
            st.success("🏆 Espetacular! Você já registrou palpites para todas as 72 partidas da Fase de Grupos!")
        else:
            # UX REVOLUCIONÁRIA: Agrupar por Datas para navegação rápida
            datas_disponiveis = sorted(list(set([j["Data"] for j in jogos_disponiveis])), key=lambda x: x[:5])
            
            dia_selecionado = st.selectbox(
                "📅 Escolha uma Data para Visualizar as Partidas",
                options=datas_disponiveis
            )
            
            jogos_do_dia = [j for j in jogos_disponiveis if j["Data"] == dia_selecionado]
            
            for jogo in jogos_do_dia:
                # Layout moderno de Card Interativo para cada partida
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-header">
                        <span class="match-badge">🏆 Rodada de Grupos</span>
                        <span class="match-time">🕒 {jogo['Horário']} - Fuso Brasília</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Renderização das bandeiras e controle numérico do placar
                col_m, col_vs, col_v = st.columns([3, 1, 3])
                
                with col_m:
                    st.markdown(f"<div style='text-align:center; font-size:2.5rem;'>{jogo['Emoji_M']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-weight:700; color:#0f172a; font-size:1.1rem;'>{jogo['Time_M']}</div>", unsafe_allow_html=True)
                    gols_m = st.number_input("Gols Mandante", min_value=0, max_value=20, value=0, key=f"m_{jogo['ID_Jogo']}", step=1)
                    
                with col_vs:
                    st.markdown("<h2 style='text-align: center; margin-top: 1.5rem; color:#94a3b8;'>x</h2>", unsafe_allow_html=True)
                    
                with col_v:
                    st.markdown(f"<div style='text-align:center; font-size:2.5rem;'>{jogo['Emoji_V']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center; font-weight:700; color:#0f172a; font-size:1.1rem;'>{jogo['Time_V']}</div>", unsafe_allow_html=True)
                    gols_v = st.number_input("Gols Visitante", min_value=0, max_value=20, value=0, key=f"v_{jogo['ID_Jogo']}", step=1)
                
                # Botão de envio reativo integrado diretamente no card do confronto
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
                                st.success("Palpite salvo e registrado com sucesso!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error(f"Erro na gravação: {resp_json.get('message')}")
                        except Exception as e:
                            st.error(f"Inconsistência de comunicação: {str(e)}")
                
                st.markdown("<hr style='border: 1px solid #f1f5f9; margin: 2rem 0;' />", unsafe_allow_html=True)

# ==========================================
# 🔧 PORTAL DO ADMINISTRADOR
# ==========================================
elif aba_selecionada == "🔧 Portal de Controle":
    st.markdown('<div class="hero-title">🔧 Portal de Controle</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Configurações globais e banco de dados reservado ao Administrador</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    senha_digitada = st.text_input("Senha Administrativa", type="password")
    
    if senha_digitada == "feltrim2026":
        st.success("Acesso administrativo desbloqueado com sucesso!")
        
        st.markdown("### 🔗 Endereçamento e Conexões com Planilhas Google")
        novo_id = st.text_input("ID do Google Sheets", value=st.session_state.spreadsheet_id)
        nova_url = st.text_input("URL do App da Web (Google Apps Script)", value=st.session_state.web_app_url)
        
        if st.button("💾 Salvar Novas Configurações de Conexão", use_container_width=True):
            st.session_state.spreadsheet_id = novo_id
            st.session_state.web_app_url = nova_url
            st.success("Chaves de conexão atualizadas localmente!")
            st.cache_data.clear()
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 🧪 Painel de Diagnóstico em Tempo Real")
        if st.button("Executar Testes de Comunicação", use_container_width=True):
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
        st.markdown("### 🚀 Ações Globais e em Lote")
        if st.button("⚡ Inicializar Todos os 72 Jogos na Planilha", use_container_width=True):
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
    st.markdown('</div>', unsafe_allow_html=True)

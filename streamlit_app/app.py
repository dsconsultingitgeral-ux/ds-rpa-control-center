import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import datetime

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Robot Virtual — Painel de Controlo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# 2. SISTEMA DE LOGIN SIMPLES (Fase de Testes)
# -------------------------------------------------------------------------
def check_password():
    """Retorna True se o utilizador estiver autenticado com sucesso."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Ecrã de Login estilo Apple (Clean e Centrado)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔐 Robot Virtual")
        st.markdown("### Painel de Controlo — Autenticação")
        
        # Credenciais predefinidas para testes
        username_input = st.text_input("Utilizador", value="admin")
        password_input = st.text_input("Palavra-passe", type="password", value="dsrobot")
        
        if st.button("Entrar no Sistema", use_container_width=True):
            # Ler credenciais seguras de st.secrets (com fallback para os valores de teste)
            expected_user = st.secrets.get("auth", {}).get("username", "admin")
            expected_pass = st.secrets.get("auth", {}).get("password", "dsrobot")
            
            if username_input == expected_user and password_input == expected_pass:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Utilizador ou palavra-passe incorretos.")
    return False

if not check_password():
    st.stop()

# -------------------------------------------------------------------------
# 3. LIGAÇÃO AO SUPABASE
# -------------------------------------------------------------------------
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error(f"Erro ao ligar ao Supabase: {e}")
    st.stop()

# -------------------------------------------------------------------------
# 4. BUSCAR E TRATAR DADOS
# -------------------------------------------------------------------------
@st.cache_data(ttl=10)
def fetch_data():
    response = supabase.table("rpa_execucoes").select("*").order("id", desc=False).execute()
    return pd.DataFrame(response.data)

df_raw = fetch_data()

if df_raw.empty:
    st.warning("⚠️ A tabela `rpa_execucoes` está vazia.")
    st.info("Executa o script SQL de teste no Supabase para popular a tabela.")
    st.stop()

# Criar coluna em minutos para análise de duração
df_raw['duration_minutes'] = df_raw['duration_seconds'] / 60.0

# -------------------------------------------------------------------------
# 5. BARRA LATERAL (FILTROS)
# -------------------------------------------------------------------------
st.sidebar.title("🤖 Robot Virtual")
st.sidebar.markdown("### Painel de Controlo")
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros")

ambientes = ["Todos"] + list(df_raw['environment'].unique())
ambiente_escolhido = st.sidebar.selectbox("Ambiente", ambientes)

robos = ["Todos"] + list(df_raw['robot_name'].unique())
robo_escolhido = st.sidebar.selectbox("Robot Virtual", robos)

status_opcoes = ["Todos", "OK", "KO"]
status_escolhido = st.sidebar.selectbox("Estado", status_opcoes)

termo_pesquisa = st.sidebar.text_input("Pesquisa nos Logs", "")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Terminar Sessão", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

# Aplicar filtros ao dataframe
df_filtrado = df_raw.copy()
if ambiente_escolhido != "Todos":
    df_filtrado = df_filtrado[df_filtrado['environment'] == ambiente_escolhido]
if robo_escolhido != "Todos":
    df_filtrado = df_filtrado[df_filtrado['robot_name'] == robo_escolhido]
if status_escolhido != "Todos":
    df_filtrado = df_filtrado[df_filtrado['status'] == status_escolhido]
if termo_pesquisa:
    df_filtrado = df_filtrado[df_filtrado['logs'].str.contains(termo_pesquisa, case=False, na=False)]

# -------------------------------------------------------------------------
# 6. TÍTULO PRINCIPAL E KPIS
# -------------------------------------------------------------------------
st.title("🤖 Robot Virtual — Painel de Controlo")
st.markdown("Monitorização em tempo real do parque de robôs, auditoria de execuções e análise de desempenho.")

total_execucoes = len(df_filtrado)
sucessos = len(df_filtrado[df_filtrado['status'] == 'OK'])
total_kos = len(df_filtrado[df_filtrado['status'] == 'KO'])
taxa_sucesso = (sucessos / total_execucoes * 100) if total_execucoes > 0 else 0
tempo_medio = df_filtrado['duration_minutes'].mean() if total_execucoes > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total de Execuções", total_execucoes)
col2.metric("✅ Taxa de Sucesso", f"{taxa_sucesso:.1f}%")
col3.metric("❌ Total de Erros (KO)", total_kos)
col4.metric("⏱️ Duração Média", f"{tempo_medio:.2f} min")

st.markdown("---")

# -------------------------------------------------------------------------
# 7. SISTEMA DE ALERTAS INTELIGENTES (5 REGRAS PARAMETRIZADAS)
# -------------------------------------------------------------------------
if total_execucoes > 0:
    # Verificar erros nas últimas 24h (assumindo a data atual ou a data máxima da tabela para testes)
    data_recente = df_filtrado['start_time_date'].max()
    erros_recentes = len(df_filtrado[(df_filtrado['status'] == 'KO') & (df_filtrado['start_time_date'] == data_recente)])
    
    # Verificar falhas consecutivas nas últimas pin-points do df filtrado
    ultimas_duas_ko = False
    if len(df_filtrado) >= 2:
        ultimos_status = df_filtrado.sort_values(by='id', ascending=False)['status'].head(2).tolist()
        if all(s == 'KO' for s in ultimos_status):
            ultimas_duas_ko = True

    # Avaliação das Regras de Alerta
    if taxa_sucesso < 50.0:
        st.error(f"🚨 **Alerta Crítico:** A taxa de sucesso atual é de apenas **{taxa_sucesso:.1f}%** (abaixo do limiar de 50%). Intervenção prioritária recomendada.")
    elif ultimas_duas_ko:
        st.error("🔴 **Falha Recorrente:** O robot falhou nas últimas 2 execuções consecutivas. Causa provável: alteração no portal de destino ou credenciais expiradas.")
    elif erros_recentes > 0:
        st.warning(f"⚠️ **Atenção:** Foram detetadas **{erros_recentes} falhas recentes** no filtro selecionado. Verifique a secção de auditoria abaixo para mais detalhes.")
    elif taxa_sucesso >= 90.0:
        st.success("✅ **Operação Saudável:** Todos os sistemas e robôs estão a funcionar dentro dos parâmetros ideais de desempenho.")
    else:
        st.info("ℹ️ **Estado Regular:** Sistema operacional com pequenos avisos menores registados.")

st.markdown("---")

# -------------------------------------------------------------------------
# 8. GRÁFICOS DE ANÁLISE KPI
# -------------------------------------------------------------------------
st.subheader("Análise KPI")

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("##### 📈 Evolução da Duração (Min)")
    if not df_filtrado.empty:
        fig_linha = px.line(
            df_filtrado, x="id", y="duration_minutes", color="robot_name",
            markers=True, labels={"id": "ID", "duration_minutes": "Min", "robot_name": "Robot"}
        )
        fig_linha.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig_linha, use_container_width=True)
    else:
        st.info("Sem dados.")

with col_g2:
    st.markdown("##### 🍩 Taxa de Sucesso (OK / KO)")
    if total_execucoes > 0:
        df_status_counts = df_filtrado['status'].value_counts().reset_index()
        df_status_counts.columns = ['status', 'count']
        fig_donut = px.pie(
            df_status_counts, names='status', values='count', hole=0.5,
            color='status', color_discrete_map={'OK': '#2ECC71', 'KO': '#E74C3C'}
        )
        fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Sem dados.")

with col_g3:
    st.markdown("##### 📊 Categorias de Erro")
    df_kos = df_filtrado[df_filtrado['status'] == 'KO']
    if not df_kos.empty and df_kos['error_category'].notna().any():
        fig_bar = px.bar(
            df_kos['error_category'].value_counts().reset_index(),
            x='count', y='error_category', orientation='h',
            labels={'count': 'Total', 'error_category': 'Erro'}
        )
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sem erros registados.")

st.markdown("---")

# -------------------------------------------------------------------------
# 9. HISTÓRICO E INSPETOR DE LOGS
# -------------------------------------------------------------------------
st.subheader("Histórico")

if not df_filtrado.empty:
    colunas_tabela = [
        'id', 'id_robot', 'robot_name', 'environment', 
        'start_time_date', 'start_time_hour', 'duration_seconds', 'status'
    ]
    st.dataframe(df_filtrado[colunas_tabela], use_container_width=True, hide_index=True)

    st.markdown("### Auditoria de Logs")
    ids_disponiveis = df_filtrado['id'].tolist()
    
    if ids_disponiveis:
        id_selecionado = st.selectbox("Selecione o ID da Execução para auditar:", ids_disponiveis)
        registo = df_filtrado[df_filtrado['id'] == id_selecionado].iloc[0]
        
        info1, info2, info3 = st.columns(3)
        info1.markdown(f"**Robot:** {registo['robot_name']} (`ID: {registo['id_robot']}`)")
        info2.markdown(f"**Data/Hora:** {registo['start_time_date']} às {registo['start_time_hour']}")
        info3.markdown(f"**Estado Final:** `{registo['status']}`")

        log_conteudo = registo['logs'] if pd.notna(registo['logs']) else "Sem logs registados."
        st.code(log_conteudo, language="text")
else:
    st.warning("Nenhum registo encontrado com os filtros atuais.")

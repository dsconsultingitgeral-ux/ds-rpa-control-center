import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import datetime

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA (Estilo Apple / Clean Minimalista)
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Robot Virtual — Painel de Controlo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# 2. SISTEMA DE AUTENTICAÇÃO SEGURO
# -------------------------------------------------------------------------
def check_password():
    """Valida se o utilizador está autenticado com base nos segredos do Streamlit."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return True

    # Layout centralizado e limpo para o Login
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🔐 Robot Virtual")
        st.markdown("### Painel de Controlo — Autenticação Segura")
        
        # Campo de utilizador agora VAZIO por predefinição (sem mostrar "admin")
        username_input = st.text_input("Utilizador", value="")
        password_input = st.text_input("Palavra-passe", type="password")
        
        if st.button("Entrar no Sistema", use_container_width=True):
            expected_user = st.secrets.get("ADMIN_USER", "admin")
            expected_pass = st.secrets.get("ADMIN_PASS", "digitalsolutions")
            
            if username_input == expected_user and password_input == expected_pass:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Utilizador ou palavra-passe incorretos. Tente novamente.")
    return False

if not check_password():
    st.stop()

# -------------------------------------------------------------------------
# 3. LIGAÇÃO SEGURA AO SUPABASE
# -------------------------------------------------------------------------
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error(f"Erro crítico ao ligar ao Supabase: {e}")
    st.stop()

# -------------------------------------------------------------------------
# 4. AQUISIÇÃO E TRATAMENTO DOS DADOS
# -------------------------------------------------------------------------
@st.cache_data(ttl=10)
def fetch_data():
    response = supabase.table("rpa_execucoes").select("*").order("id", desc=False).execute()
    return pd.DataFrame(response.data)

df_raw = fetch_data()

if df_raw.empty:
    st.warning("⚠️ A tabela `rpa_execucoes` está vazia ou inacessível.")
    st.stop()

df_raw['duration_minutes'] = df_raw['duration_seconds'] / 60.0

# -------------------------------------------------------------------------
# 5. BARRA LATERAL (FILTROS INTELIGENTES)
# -------------------------------------------------------------------------
st.sidebar.title("🤖 Robot Virtual")
st.sidebar.markdown("### Painel de Controlo")
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros de Auditoria")

ambientes = ["Todos"] + list(df_raw['environment'].unique())
ambiente_escolhido = st.sidebar.selectbox("Ambiente", ambientes)

robos = ["Todos"] + list(df_raw['robot_name'].unique())
robo_escolhido = st.sidebar.selectbox("Robot Virtual", robos)

status_opcoes = ["Todos", "OK", "KO"]
status_escolhido = st.sidebar.selectbox("Estado da Execução", status_opcoes)

termo_pesquisa = st.sidebar.text_input("Pesquisa textual nos Logs", "")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Terminar Sessão", use_container_width=True):
    st.session_state["authenticated"] = False
    st.rerun()

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
st.markdown("Monitorização centralizada e em tempo real do parque de robôs, auditoria de execuções e análise proativa de falhas.")

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
    data_recente = df_filtrado['start_time_date'].max()
    erros_recentes = len(df_filtrado[(df_filtrado['status'] == 'KO') & (df_filtrado['start_time_date'] == data_recente)])
    
    ultimas_duas_ko = False
    if len(df_filtrado) >= 2:
        ultimos_status = df_filtrado.sort_values(by='id', ascending=False)['status'].head(2).tolist()
        if all(s == 'KO' for s in ultimos_status):
            ultimas_duas_ko = True

    if taxa_sucesso < 50.0:
        st.error(f"🚨 **Alerta Crítico:** A taxa de sucesso atual é de apenas **{taxa_sucesso:.1f}%** (abaixo do limiar de 50%). Requer intervenção prioritária.")
    elif ultimas_duas_ko:
        st.error("🔴 **Falha Recorrente:** O robô falhou nas últimas 2 execuções consecutivas. Possível alteração no portal de destino ou credenciais expiradas.")
    elif erros_recentes > 0:
        st.warning(f"⚠️ **Atenção:** Foram detetadas **{erros_recentes} falhas críticas** no período recente selecionado. Consulte a auditoria abaixo.")
    elif taxa_sucesso >= 90.0:
        st.success("✅ **Operação Saudável:** Todos os sistemas e robôs estão a operar dentro dos parâmetros ideais de desempenho.")
    else:
        st.info("ℹ️ **Estado Regular:** Sistema operacional com pequenos avisos registados.")

st.markdown("---")

# -------------------------------------------------------------------------
# 8. GRÁFICOS DE ANÁLISE KPI (Linha, Rosca e Barras Horizontais)
# -------------------------------------------------------------------------
st.subheader("Análise KPI e Desempenho Visual")

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("##### 📈 Evolução da Duração (Min)")
    if not df_filtrado.empty:
        fig_linha = px.line(
            df_filtrado, x="id", y="duration_minutes", color="robot_name",
            markers=True, labels={"id": "ID Execução", "duration_minutes": "Duração (Min)", "robot_name": "Robô"}
        )
        fig_linha.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig_linha, use_container_width=True)
    else:
        st.info("Sem dados para exibir.")

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
        st.info("Sem dados para exibir.")

with col_g3:
    st.markdown("##### 📊 Categorias de Erro")
    df_kos = df_filtrado[df_filtrado['status'] == 'KO']
    if not df_kos.empty and df_kos['error_category'].notna().any():
        fig_bar = px.bar(
            df_kos['error_category'].value_counts().reset_index(),
            x='count', y='error_category', orientation='h',
            labels={'count': 'Total de Erros', 'error_category': 'Categoria'}
        )
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sem erros registados nos filtros atuais.")

st.markdown("---")

# -------------------------------------------------------------------------
# 9. HISTÓRICO GERAL E INSPETOR DE LOGS LINHA A LINHA
# -------------------------------------------------------------------------
st.subheader("Auditoria e Registo de Logs")

if not df_filtrado.empty:
    colunas_tabela = [
        'id', 'id_robot', 'robot_name', 'environment', 
        'start_time_date', 'start_time_hour', 'duration_seconds', 'status'
    ]
    st.dataframe(df_filtrado[colunas_tabela], use_container_width=True, hide_index=True)

    st.markdown("### Inspetor de Consola (Logs Detalhados)")
    ids_disponiveis = df_filtrado['id'].tolist()
    
    if ids_disponiveis:
        id_selecionado = st.selectbox("Selecione o ID da Execução para inspecionar os logs:", ids_disponiveis)
        registo = df_filtrado[df_filtrado['id'] == id_selecionado].iloc[0]
        
        info1, info2, info3 = st.columns(3)
        info1.markdown(f"**Robô:** {registo['robot_name']} (`ID: {registo['id_robot']}`)")
        info2.markdown(f"**Data/Hora:** {registo['start_time_date']} às {registo['start_time_hour']}")
        info3.markdown(f"**Estado Final:** `{registo['status']}`")

        log_conteudo = registo['logs'] if pd.notna(registo['logs']) else "Sem logs registados para esta execução."
        st.code(log_conteudo, language="text")
else:
    st.warning("Nenhum registo encontrado com os filtros aplicados.")

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime
from services.agents import BloggerAgent, SocialAgent, SeoAgent, UrlSeoAnalyzerAgent, TranslatorAgent

# ========== CONFIGURAÇÃO DO BANCO DE DADOS DE TAREFAS ==========
def init_db():
    conn = sqlite3.connect(os.getenv("TASKS_DB_PATH", "./data/tasks.db"))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  agent_type TEXT,
                  prompt TEXT,
                  result TEXT,
                  image_path TEXT,
                  latency_ms INTEGER,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

def save_task(agent_type, prompt, result, image_path, latency_ms):
    conn = sqlite3.connect(os.getenv("TASKS_DB_PATH", "./data/tasks.db"))
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (agent_type, prompt, result, image_path, latency_ms, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (agent_type, prompt, result, image_path, latency_ms, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(os.getenv("TASKS_DB_PATH", "./data/tasks.db"))
    df = pd.read_sql_query("SELECT * FROM tasks ORDER BY created_at DESC", conn)
    conn.close()
    return df

# ========== STREAMLIT APP ==========
st.set_page_config(page_title="Squad IA Local", layout="wide")
st.title("🤖 Squad de IA Local – Agentes de Conteúdo")

# Inicializa banco de tarefas e pastas
os.makedirs("./data", exist_ok=True)
os.makedirs("./media", exist_ok=True)
init_db()

# Cria instâncias dos agentes (usamos session_state para manter)
if 'blogger' not in st.session_state:
    st.session_state.blogger = BloggerAgent()
if 'social' not in st.session_state:
    st.session_state.social = SocialAgent()
if 'seo' not in st.session_state:          # antes era 'designer'
    st.session_state.seo = SeoAgent()
if 'url_analyzer' not in st.session_state:
    st.session_state.url_analyzer = UrlSeoAnalyzerAgent()
if 'translator' not in st.session_state:
    st.session_state.translator = TranslatorAgent()

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📝 Redator Blog", "📱 Social Media", "🔍 Especialista SEO", "🌐 Analisador de URL", "🚀 Tradutor", "📊 Monitor", "📄 Formatador ABNT"])

# ========== TAB 1: BLOGGER ==========
with tab1:
    st.header("Redator de Blog")
    with st.expander("📁 Adicionar Documento à Memória", expanded=False):
        uploaded_file = st.file_uploader("Escolha um arquivo (PDF, DOCX, TXT, imagem)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], key="blogger_file")
        if uploaded_file:
            if uploaded_file.type.startswith('image'):
                description = st.text_input("Descrição da imagem (opcional):", key="blogger_img_desc")
            else:
                description = ""
            if st.button("Adicionar à Memória", key="blogger_add_doc"):
                with st.spinner("Processando arquivo..."):
                    result = st.session_state.blogger.remember_document(uploaded_file, description)
                st.success(result)

    with st.expander("🧠 Memória do Agente", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            remember_text = st.text_area("Digite algo para o agente lembrar:", key="blogger_remember")
            if st.button("Lembrar", key="blogger_remember_btn"):
                if remember_text:
                    result = st.session_state.blogger.remember(remember_text)
                    st.success(result)
        with col2:
            recall_query = st.text_input("Pesquisar na memória:", key="blogger_recall")
            if st.button("Buscar", key="blogger_recall_btn"):
                if recall_query:
                    memories = st.session_state.blogger.recall(recall_query)
                    st.text_area("Memórias encontradas:", memories, height=150)

    prompt = st.text_area("Tema do post:", height=100, key="blogger_prompt")
    if st.button("Gerar Post", key="blogger_generate"):
        if prompt:
            with st.spinner("Gerando conteúdo..."):
                result, latency = st.session_state.blogger.process(prompt)
                st.subheader("Post gerado:")
                st.write(result)
                save_task("blogger", prompt, result, "", latency)
                st.info(f"Tempo de resposta: {latency:.0f} ms")

# ========== TAB 2: SOCIAL MEDIA ==========
with tab2:
    st.header("Agente de Social Media")
    with st.expander("📁 Adicionar Documento à Memória", expanded=False):
        uploaded_file = st.file_uploader("Escolha um arquivo (PDF, DOCX, TXT, imagem)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], key="social_file")
        if uploaded_file:
            if uploaded_file.type.startswith('image'):
                description = st.text_input("Descrição da imagem (opcional):", key="social_img_desc")
            else:
                description = ""
            if st.button("Adicionar à Memória", key="social_add_doc"):
                with st.spinner("Processando arquivo..."):
                    result = st.session_state.social.remember_document(uploaded_file, description)
                st.success(result)

    with st.expander("🧠 Memória do Agente", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            remember_text = st.text_area("Digite algo para o agente lembrar:", key="social_remember")
            if st.button("Lembrar", key="social_remember_btn"):
                if remember_text:
                    result = st.session_state.social.remember(remember_text)
                    st.success(result)
        with col2:
            recall_query = st.text_input("Pesquisar na memória:", key="social_recall")
            if st.button("Buscar", key="social_recall_btn"):
                if recall_query:
                    memories = st.session_state.social.recall(recall_query)
                    st.text_area("Memórias encontradas:", memories, height=150)

    prompt = st.text_area("Tema para o post social:", height=100, key="social_prompt")
    if st.button("Gerar Post Social", key="social_generate"):
        if prompt:
            with st.spinner("Gerando conteúdo..."):
                result, latency = st.session_state.social.process(prompt)
                st.subheader("Post gerado:")
                st.write(result)
                save_task("social", prompt, result, "", latency)
                st.info(f"Tempo de resposta: {latency:.0f} ms")

# ========== TAB 3: Especialista SEO ==========
with tab3:
    st.header("Especialista em SEO")
    with st.expander("📁 Adicionar Documento à Memória", expanded=False):
        uploaded_file = st.file_uploader("Escolha um arquivo (PDF, DOCX, TXT, imagem)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], key="seo_file")
        if uploaded_file:
            if uploaded_file.type.startswith('image'):
                description = st.text_input("Descrição da imagem (opcional):", key="seo_img_desc")
            else:
                description = ""
            if st.button("Adicionar à Memória", key="seo_add_doc"):
                with st.spinner("Processando arquivo..."):
                    result = st.session_state.seo.remember_document(uploaded_file, description)
                st.success(result)

    with st.expander("🧠 Memória do Agente", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            remember_text = st.text_area("Digite algo para o agente lembrar:", key="seo_remember")
            if st.button("Lembrar", key="seo_remember_btn"):
                if remember_text:
                    result = st.session_state.seo.remember(remember_text)
                    st.success(result)
        with col2:
            recall_query = st.text_input("Pesquisar na memória:", key="seo_recall")
            if st.button("Buscar", key="seo_recall_btn"):
                if recall_query:
                    memories = st.session_state.seo.recall(recall_query)
                    st.text_area("Memórias encontradas:", memories, height=150)

    original_text = st.text_area("Texto original a ser otimizado:", height=200, key="seo_text")
    keywords = st.text_input("Palavras-chave (separadas por vírgula):", key="seo_keywords")
    if st.button("Otimizar para SEO", key="seo_generate"):
        if original_text and keywords:
            with st.spinner("Otimizando texto..."):
                result, latency = st.session_state.seo.process(original_text, keywords)
                st.subheader("Texto otimizado:")
                st.write(result)
                save_task("seo", f"Texto: {original_text[:50]}... | Palavras-chave: {keywords}", result, "", latency)
                st.info(f"Tempo de resposta: {latency:.0f} ms")
        else:
            st.warning("Preencha o texto e as palavras-chave.")

# ========== TAB 4: Analisador de URL (SEO) ==========
with tab4:
    st.header("Analisador de URL (SEO)")
    with st.expander("🧠 Memória do Agente (opcional)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            remember_text = st.text_area("Digite algo para o agente lembrar:", key="url_remember")
            if st.button("Lembrar", key="url_remember_btn"):
                if remember_text:
                    result = st.session_state.url_analyzer.remember(remember_text)
                    st.success(result)
        with col2:
            recall_query = st.text_input("Pesquisar na memória:", key="url_recall")
            if st.button("Buscar", key="url_recall_btn"):
                if recall_query:
                    memories = st.session_state.url_analyzer.recall(recall_query)
                    st.text_area("Memórias encontradas:", memories, height=150)

    url_input = st.text_input("Digite a URL para análise:", placeholder="https://exemplo.com/artigo")
    if st.button("Analisar URL", key="url_analyze"):
        if url_input:
            with st.spinner("Acessando e analisando a página..."):
                result, latency = st.session_state.url_analyzer.process(url_input)
                st.subheader("🔍 Relatório SEO")
                st.write(result)
                save_task("url_analyzer", f"URL: {url_input}", result, "", latency)
                st.info(f"Tempo de resposta: {latency:.0f} ms")
        else:
            st.warning("Insira uma URL válida.")

# ========== TAB 5: Tradutor Inteligente ==========
with tab5:
    st.header("Tradutor Inteligente (Hermes 3)")

    # Memória (opcional, mas útil)
    with st.expander("🧠 Memória do Agente", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            remember_text = st.text_area("Digite algo para o agente lembrar:", key="translator_remember")
            if st.button("Lembrar", key="translator_remember_btn"):
                if remember_text:
                    result = st.session_state.translator.remember(remember_text)
                    st.success(result)
        with col2:
            recall_query = st.text_input("Pesquisar na memória:", key="translator_recall")
            if st.button("Buscar", key="translator_recall_btn"):
                if recall_query:
                    memories = st.session_state.translator.recall(recall_query)
                    st.text_area("Memórias encontradas:", memories, height=150)

    # Entrada de dados
    input_type = st.radio("Fonte:", ["Texto", "Arquivo"], key="translator_input_type")

    if input_type == "Texto":
        text_input = st.text_area("Texto a traduzir:", height=150, key="translator_text")
    else:
        uploaded_file = st.file_uploader("Escolha um arquivo (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], key="translator_file")
        if uploaded_file:
            text_input = None  # será tratado depois
        else:
            text_input = None

    # Idiomas
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.text_input("Idioma de origem (opcional, deixe em branco para detecção automática):", key="source_lang")
    with col2:
        target_lang = st.selectbox("Idioma de destino:", ["português", "inglês", "espanhol", "francês", "alemão", "italiano"], key="target_lang")

    if st.button("Traduzir", key="translator_generate"):
        # Inicializa agente se não existir
        if 'translator' not in st.session_state:
            st.session_state.translator = TranslatorAgent()

        if input_type == "Texto":
            if text_input:
                with st.spinner("Traduzindo..."):
                    result, latency = st.session_state.translator.process(
                        text_input, target_lang, source_lang if source_lang else None
                    )
                    st.subheader("Texto traduzido:")
                    st.write(result)
                    save_task("translator", f"Tradução para {target_lang}", result, "", latency)
                    st.info(f"Tempo de resposta: {latency:.0f} ms")
            else:
                st.warning("Digite o texto a traduzir.")
        else:
            if uploaded_file:
                with st.spinner("Processando arquivo e traduzindo..."):
                    result, latency = st.session_state.translator.process_file(
                        uploaded_file, target_lang, source_lang if source_lang else None
                    )
                    st.subheader("Texto traduzido:")
                    st.write(result)
                    save_task("translator", f"Arquivo {uploaded_file.name} → {target_lang}", result, "", latency)
                    st.info(f"Tempo de resposta: {latency:.0f} ms")
            else:
                st.warning("Envie um arquivo.")

# ========== TAB 6: MONITOR ==========
with tab6:
    st.header("Monitor de Tarefas")
    tasks_df = get_tasks()

    if not tasks_df.empty:
        # Converte created_at para datetime e ordena
        tasks_df['created_at'] = pd.to_datetime(tasks_df['created_at'])
        tasks_df = tasks_df.sort_values('created_at')

        # Filtro de data (sidebar ou dentro da aba)
        st.sidebar.subheader("Filtro de datas")
        min_date = tasks_df['created_at'].min().date()
        max_date = tasks_df['created_at'].max().date()
        start_date = st.sidebar.date_input("Data inicial", value=max_date - pd.Timedelta(days=1), min_value=min_date, max_value=max_date)
        end_date = st.sidebar.date_input("Data final", value=max_date, min_value=min_date, max_value=max_date)

        # Aplica filtro
        mask = (tasks_df['created_at'].dt.date >= start_date) & (tasks_df['created_at'].dt.date <= end_date)
        filtered_df = tasks_df[mask]

        if filtered_df.empty:
            st.info("Nenhuma tarefa no período selecionado.")
        else:
            # Gráfico de linha: latência por agente ao longo do tempo
            fig = px.line(
                filtered_df,
                x='created_at',
                y='latency_ms',
                color='agent_type',
                title='Latência ao longo do tempo',
                labels={'created_at': 'Data/Hora', 'latency_ms': 'Latência (ms)', 'agent_type': 'Agente'},
                line_shape='linear'  # garante linha reta entre pontos
            )
            st.plotly_chart(fig, use_container_width=True)

            # Contagem por agente (barras)
            count = filtered_df['agent_type'].value_counts().reset_index()
            count.columns = ['Agente', 'Quantidade']
            fig2 = px.bar(count, x='Agente', y='Quantidade', title='Uso por agente')
            st.plotly_chart(fig2, use_container_width=True)

            # Tabela detalhada (opcional)
            with st.expander("Ver detalhes das tarefas"):
                st.dataframe(filtered_df[['id', 'agent_type', 'prompt', 'latency_ms', 'created_at']], use_container_width=True)
    else:
        st.info("Nenhuma tarefa registrada ainda.")

# ========== TAB 7: MONITOR ==========
with tab7:
    st.header("Formatador ABNT para Documentos Word")
    st.markdown("Envie um arquivo **.docx** e ele será formatado conforme as normas ABNT (margens, fontes, títulos, espaçamento, tabelas).")

    uploaded_file = st.file_uploader("Escolha um arquivo Word (.docx)", type=["docx"], key="abnt_file")
    if uploaded_file:
        if st.button("Formatar conforme ABNT", key="abnt_format"):
            with st.spinner("Formatando documento... Isso pode levar alguns segundos."):
                if 'abnt_formatter' not in st.session_state:
                    from services.agents import AbntFormatterAgent
                    st.session_state.abnt_formatter = AbntFormatterAgent()
                result, latency = st.session_state.abnt_formatter.process(uploaded_file)
                if result.startswith("Erro"):
                    st.error(result)
                else:
                    st.success(f"Documento formatado com sucesso! Tempo: {latency:.0f} ms")
                    with open(result, "rb") as f:
                        st.download_button(
                            label="Baixar documento formatado",
                            data=f,
                            file_name=os.path.basename(result),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
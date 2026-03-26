# 🧠 Squad IA Local – Agentes de Conteúdo

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LM Studio](https://img.shields.io/badge/LM_Studio-0A0A0A?style=flat-square)](https://lmstudio.ai)
[![Hermes 3](https://img.shields.io/badge/Hermes_3-FFD700?style=flat-square)](https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-00A67E?style=flat-square)](https://www.trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

> **Sistema local, offline e privado** para geração e otimização de conteúdo, com agentes especializados, memória persistente e monitoramento integrado. Tudo rodando com modelos locais (Hermes 3 e Nomic Embed) via LM Studio, banco vetorial ChromaDB e interface Streamlit.

---

## 📌 Sobre o Projeto

Este sistema reúne um conjunto de **agentes de IA locais** que operam completamente offline, sem dependência de nuvem. Cada agente executa uma tarefa específica:

- **Redator de Blog** Gera posts longos a partir de prompts e memórias.
- **Social Media** Cria posts curtos otimizados para redes sociais.
- **Especialista SEO** Reescreve textos para melhorar ranqueamento, utilizando palavras‑chave fornecidas.
- **Analisador de URL** Extrai dados de uma página web (título, meta descrição, links) e gera um relatório SEO estruturado.
- **Tradutor** Traduz textos ou arquivos para qualquer idioma, com detecção automática de origem.
- **Formatador ABNT** Recebe um documento Word (.docx) e aplica formatação conforme as normas da ABNT (margens, fontes, títulos, tabelas).
- **Monitor** Exibe histórico de tarefas, latência e gráficos de uso, utilizando SQLite.

Todos os agentes compartilham uma **memória persistente** (ChromaDB + embeddings Nomic via LM Studio), permitindo que o contexto seja armazenado e recuperado conforme necessário.

---

## 🛠️ Stack Tecnológica

| **Categoria** | **Tecnologias e Bibliotecas** |
|---------------|-------------------------------|
| **Linguagem** | Python 3.10+ |
| **Interface** | Streamlit |
| **IA Local** | LM Studio, Hermes 3 (LLM), Nomic Embed (embeddings) |
| **Memória** | ChromaDB (banco vetorial) |
| **Banco de Dados** | SQLite (histórico de tarefas) |
| **Processamento de Documentos** | PyPDF2, python-docx, Pillow, BeautifulSoup |
| **Visualização** | Plotly, Matplotlib, pandas |
| **Utilitários** | requests, python-dotenv, langdetect |
| **Segurança** | Guardrails com regex (detecção de prompt injection) |

---

## 📊 Arquitetura do Sistema

```plaintext
┌─────────────────────────────────────────────────────────────────────────┐
│                         🖥️  INTERFACE STREAMLIT                         │
│  (Upload de arquivos, prompts, visualização de resultados, monitor)    │
└─────────────────────────────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│   AGENTES DE      │    │   AGENTES DE      │    │   AGENTES DE      │
│   CONTEÚDO        │    │   ANÁLISE         │    │   UTILITÁRIOS     │
├───────────────────┤    ├───────────────────┤    ├───────────────────┤
│ • Redator Blog    │    │ • URL SEO        │    │ • Tradutor        │
│ • Social Media    │    │                  │    │ • Formatador ABNT │
│ • Especialista SEO│    │                  │    │                   │
└───────────────────┘    └───────────────────┘    └───────────────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 ▼
                 ┌───────────────────────────────┐
                 │      SERVIÇOS CENTRAIS        │
                 ├───────────────────────────────┤
                 │  • LLM Service (Hermes 3)     │
                 │  • Memory Service (ChromaDB)  │
                 │  • File Processor             │
                 │  • Guardrails (validação)     │
                 └───────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│   BANCO DE        │  │   BANCO VETORIAL  │  │   ARQUIVOS        │
│   DADOS (SQLite)  │  │   (ChromaDB)      │  │   (Media / Temp)  │
├───────────────────┤  ├───────────────────┤  ├───────────────────┤
│ • Histórico de    │  │ • Memórias por    │  │ • Uploads         │
│   tarefas         │  │   agente          │  │ • Imagens geradas │
│ • Latência        │  │ • Embeddings      │  │ • Documentos      │
│ • Logs            │  │   (Nomic via LM)  │  │   processados     │
└───────────────────┘  └───────────────────┘  └───────────────────┘
                                 │
                                 ▼
                 ┌───────────────────────────────┐
                 │      MODELOS LOCAIS           │
                 ├───────────────────────────────┤
                 │  • Hermes 3 (LLM)             │
                 │  • Nomic Embed (embedding)    │
                 │  • (via LM Studio)            │
                 └───────────────────────────────┘


# 🚀 Como Executar

## Pré‑requisitos
- Python 3.9+
- **LM Studio** com os modelos carregados:
  - `hermes-3-llama-3.2-3b` (GGUF)
  - `nomic-embed-text-v1.5` (GGUF)
- `ffmpeg` (opcional, necessário para processamento de áudio/vídeo)

## Passo a passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Gussnogue/system-content-agents-ai-local.git
   cd system-content-agents-ai-local
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   Configure o arquivo .env (crie na raiz do projeto)
   ```
4. **Execute a aplicação Streamlit**

   ```bash
   streamlit run app.py
   ```

# 🧠 Como Usar os Agentes

Cada agente possui sua própria aba no Streamlit. A maioria oferece:

- Memória: use “Lembrar” para inserir contexto manualmente, ou “Adicionar Documento” para carregar PDF, DOCX, TXT ou imagem.

- Pesquisa: “Buscar” recupera memórias relevantes para o prompt atual.

- Geração: após fornecer os dados necessários, clique no botão de ação (ex: “Gerar Post”, “Traduzir”, “Formatar”).

O Monitor exibe o histórico de tarefas com gráficos de latência e contagem de uso.

# 🔒 Guardrails e Segurança

O sistema implementa validação de entrada e saída no BaseAgent, detectando tentativas de prompt injection em 
português, inglês, espanhol, francês, alemão e italiano. Padrões suspeitos são bloqueados e a resposta é substituída por uma mensagem de segurança.

# 📂 Estrutura do Projeto

```bash
system-content-agents-ai-local/
│
├── app.py                     # Aplicação Streamlit
├── services/                  # Módulos dos agentes e serviços
│   ├── agents.py              # Classes dos agentes (Blog, Social, SEO, URL, Tradutor, ABNT)
│   ├── llm_service.py         # Cliente Hermes 3 (LM Studio)
│   ├── memory_service.py      # ChromaDB + embeddings
│   ├── file_processor.py      # Extração de texto de PDF/DOCX/imagens
│   └── document_editor.py     # Formatação ABNT com python-docx
├── data/                      # (criado automaticamente) SQLite e ChromaDB
├── media/                     # (criado automaticamente) imagens, documentos editados
├── requirements.txt
├── .env (exemplo)
└── README.md
```

# Modelos Locais:

*Hermes 3 – Nous Research*

*Nomic Embed Text v1.5 – Nomic AI*

Frameworks e Bibliotecas: Streamlit, ChromaDB, python-docx, PyPDF2, BeautifulSoup, Plotly, pandas, langdetect, etc.

# 📄 Licença

MIT License – sinta‑se à vontade para usar, modificar e distribuir.

🔗 Repositório: Gussnogue/system-content-agents-ai-local

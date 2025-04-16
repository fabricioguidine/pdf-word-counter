# 📄 PDF Word Counter with Frequency Weighting (Silent Mode)

Este projeto é um script em Python que processa arquivos `.pdf` em uma pasta, extrai palavras compostas e relevantes com análise gramatical via spaCy, calcula frequências, atribui pesos e **salva os resultados em um arquivo `output.txt`** — sem exibir nada no terminal.

---

## 🚀 Como usar

### 1. Clone o repositório ou baixe os arquivos
```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

### 2. (Opcional) Crie um ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

> Para textos em português, use `pt_core_news_sm`

### 4. Coloque seus arquivos PDF
Adicione os PDFs na pasta:
```
sample_pdfs/
```

### 5. Execute o script
```bash
python count_pdf_words.py
```

---

## 📁 O que será gerado?

Um arquivo `output.txt` com:
- Total de palavras úteis extraídas
- Palavras compostas detectadas (ex: `software testing`)
- Frequência de ocorrência
- Peso relativo baseado na palavra mais repetida
- Top 10% palavras mais frequentes

---

## 📂 Estrutura do projeto

```
pdf-word-counter/
├── count_pdf_words.py         # Script principal
├── sample_pdfs/               # PDFs de entrada
├── requirements.txt           # Dependências
├── output.txt                 # Resultado gerado automaticamente
└── README.md                  # Este arquivo
```

---

## 🧠 Tecnologias usadas

- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [spaCy](https://spacy.io/)
- Modelo: `en_core_web_sm` (ou `pt_core_news_sm`)

---

## 📝 Licença

Este projeto é livre para uso educacional ou pessoal. Adicione uma licença oficial se necessário.

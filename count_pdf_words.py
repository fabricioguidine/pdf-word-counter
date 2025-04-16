import os
import re
import spacy
from collections import Counter
from PyPDF2 import PdfReader

# Carrega o modelo spaCy (ajuste para pt_core_news_sm se o texto for em português)
nlp = spacy.load("en_core_web_sm")

# 🔍 Extrai compostos (ex: software testing)
def extract_compound_terms(doc):
    return [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]

# 📥 Extrai palavras úteis e compostas
def extract_words_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        doc = nlp(text.lower())

        single_words = [
            token.text for token in doc 
            if token.pos_ in ("NOUN", "PROPN", "VERB") and len(token.text) > 2
        ]
        compound_terms = extract_compound_terms(doc)

        return single_words + compound_terms

    except Exception as e:
        return [f"❌ Erro ao ler {pdf_path}: {e}"]

# 📊 Contagem, pesos e salvamento
def count_words_with_weights(folder_path):
    total_words = []
    output_lines = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            path = os.path.join(folder_path, file)
            words = extract_words_from_pdf(path)

            if len(words) == 1 and words[0].startswith("❌"):
                output_lines.append(words[0])
                continue

            output_lines.append(f"{file}: {len(words)} palavras úteis")
            total_words.extend(words)

    word_counts = Counter(total_words)

    if not word_counts:
        output_lines.append("⚠️ Nenhuma palavra útil encontrada nos PDFs.")
        return write_output(output_lines)

    total_unique = len(word_counts)
    max_freq = word_counts.most_common(1)[0][1]

    weighted = [(word, count, round(count / max_freq, 4)) for word, count in word_counts.items()]
    weighted.sort(key=lambda x: x[1], reverse=True)

    top_n = max(1, int(total_unique * 0.10))
    top_words = weighted[:top_n]

    output_lines.append(f"\n🔢 Palavras únicas úteis: {total_unique}")
    output_lines.append(f"\n🏆 Top {top_n} palavras mais frequentes (com pesos):\n")

    for i, (word, count, weight) in enumerate(top_words, start=1):
        line = f"{i:02d}. {word:<25} → {count:>4}x | peso: {weight:.2f}"
        output_lines.append(line)

    write_output(output_lines)

# 💾 Salva apenas no arquivo
def write_output(lines):
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# 🚀 Execução
if __name__ == "__main__":
    folder = os.path.join(os.path.dirname(__file__), "sample_pdfs")
    count_words_with_weights(folder)

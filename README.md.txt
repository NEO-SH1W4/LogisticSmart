
# 📦 LogisticSmart

**LogisticSmart** é uma ferramenta web inteligente para análise e geração de relatórios de entregas. Desenvolvido com **Streamlit**, permite que usuários façam upload de planilhas `.xlsx`, apliquem filtros dinâmicos, visualizem entregas por entregador e exportem relatórios em múltiplos formatos.

---

## 🚀 Funcionalidades

- Upload de arquivos `.xlsx` com dados de entrega
- Filtros inteligentes por colunas detectadas automaticamente (como cidade, entregador, status, tipo de produto etc.)
- Agrupamento por entregador
- Exportação para:
  - 📄 Excel
  - 📝 Word (.docx)
  - 📑 PDF
- Interface intuitiva e responsiva com ícones visuais e modo escuro
- Separação por **entregas pendentes** e **entregues**

---

## 🛠️ Tecnologias

- Python 3.10+
- Streamlit
- Pandas
- OpenPyXL
- python-docx
- pdfkit + wkhtmltopdf

---

## 🧩 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/LogisticSmart.git
cd LogisticSmart
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se de que o `wkhtmltopdf` esteja instalado e disponível no PATH (para gerar PDF).

---

## ▶️ Executando

```bash
streamlit run LogisticSmart_v1.py
```

> Use `start_LogisticSmart.bat` no Windows para facilitar a inicialização.

---

## 📂 Estrutura esperada do Excel

O sistema detecta automaticamente colunas como:

- `Data prevista de entrega`
- `Entregador`
- `Cidade`
- `Tipo de produto`
- `Status`
- `Destino`
- `Tipo problemático`

> Os nomes das colunas devem estar na primeira linha do Excel.

---

## 🧠 Inteligência Adaptativa

- Todos os filtros são gerados com base nas **colunas detectadas** no arquivo.
- O app se adapta a diferentes estruturas de planilhas sem necessidade de configuração manual.

---

## 📅 Última atualização

22/03/2025

---

## 📜 Licença

Este projeto é open-source, sob a licença MIT.

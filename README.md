
# 📦 LogisticSmart v2.0

**LogisticSmart** é um sistema inteligente para análise e geração de relatórios de entregas, desenvolvido com foco em usabilidade, segurança e performance.

![LogisticSmart](https://img.shields.io/badge/LogisticSmart-v2.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Funcionalidades Principais

- ✅ **Autenticação Segura** com diferentes níveis de acesso (Admin, Usuário, Visitante)
- 📊 **Processamento Inteligente** de dados Excel/CSV com detecção automática de colunas
- 🎛️ **Filtros Adaptativos** baseados na estrutura dos dados carregados
- 📈 **Dashboard Interativo** com visualizações modernas usando Plotly
- 📥 **Exportação Múltipla** (Excel, CSV, PDF, Word)
- 🔍 **Análise de Qualidade** dos dados com recomendações
- ⚡ **Cache Inteligente** para melhor performance
- 🎨 **Interface Moderna** com tema escuro personalizável

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit, Plotly, HTML/CSS
- **Backend**: Python, Pandas, NumPy
- **Segurança**: bcrypt para hash de senhas
- **Exportação**: openpyxl, python-docx, pdfkit
- **Visualização**: Plotly Express, Altair

## 📋 Estrutura de Dados Suportada

O sistema detecta automaticamente colunas como:

### Obrigatórias:
- `Data prevista de entrega` (ou variações)

### Opcionais:
- `Entregador` / `Responsável` / `Motorista`
- `Cidade` / `Local` / `Destino` / `Município`
- `Status` / `Situação` / `Estado`
- `Tipo de produto` / `Item` / `Mercadoria`
- `Cliente` / `Destinatário` / `Receptor`

## 🧩 Instalação

### 1. Clone o repositório:
```bash
git clone https://github.com/NEO-SH1W4/LogisticSmart.git
cd LogisticSmart
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Para geração de PDF (opcional):
- **Windows**: Baixe [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) e adicione ao PATH
- **Linux**: `sudo apt-get install wkhtmltopdf`
- **macOS**: `brew install wkhtmltopdf`

## ▶️ Executando

```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 👥 Perfis de Usuário

### 👑 Admin
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Permissões**: Acesso completo a todas as funcionalidades

### 👤 Usuário Neo
- **Usuário**: `neo`
- **Senha**: `matrix`
- **Permissões**: Acesso completo a todas as funcionalidades

### 👁️ Visitante
- **Usuário**: `visitante`
- **Senha**: `fasebeta`
- **Permissões**: Apenas visualização de relatórios

## 🎛️ Funcionalidades por Perfil

| Funcionalidade | Admin | Neo | Visitante |
|----------------|-------|-----|-----------|
| Upload de arquivos | ✅ | ✅ | ❌ |
| Visualizar relatórios | ✅ | ✅ | ✅ |
| Exportar dados | ✅ | ✅ | ❌ |
| Filtros avançados | ✅ | ✅ | ❌ |
| Análise de qualidade | ✅ | ✅ | ❌ |
| Gerenciar usuários | ✅ | ✅ | ❌ |

## 📊 Exemplo de Uso

1. **Login**: Acesse com suas credenciais
2. **Upload**: Carregue arquivo Excel/CSV com dados de entregas
3. **Análise**: Use filtros para análise específica (pendentes, entregues, etc.)
4. **Visualização**: Veja dashboard com gráficos interativos
5. **Exportação**: Baixe relatórios em diferentes formatos

## 📁 Estrutura do Projeto

```
LogisticSmart/
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências
├── README.md                   # Documentação
├── .streamlit/
│   └── config.toml            # Configuração do Streamlit
├── src/
│   ├── __init__.py
│   ├── config/
│   │   └── settings.py        # Configurações centralizadas
│   ├── auth/
│   │   └── authentication.py  # Sistema de autenticação
│   ├── utils/
│   │   ├── data_processor.py  # Processamento de dados
│   │   └── export_utils.py    # Utilitários de exportação
│   └── components/
│       └── ui_components.py   # Componentes de UI
├── tests/                     # Testes automatizados
├── docs/                      # Documentação adicional
└── logs/                      # Logs da aplicação
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=200
CACHE_TTL=3600
THEME_MODE=dark
```

### Customização de Tema

Edite `.streamlit/config.toml` para personalizar cores e aparência.

## 🧪 Testes

```bash
# Executar testes
pytest tests/

# Cobertura de testes
pytest --cov=src tests/
```

## 📈 Performance

- **Cache inteligente** para arquivos carregados
- **Processamento otimizado** com Pandas
- **Lazy loading** de componentes pesados
- **Compressão automática** de dados exportados

## 🔒 Segurança

- Hash seguro de senhas com bcrypt
- Validação de arquivos carregados
- Sanitização de dados de entrada
- Controle de acesso baseado em perfis

## 🐛 Solução de Problemas

### Erro de importação pandas/streamlit
```bash
pip install --upgrade pandas streamlit
```

### Erro na geração de PDF
```bash
# Verificar se wkhtmltopdf está instalado
wkhtmltopdf --version

# Instalar se necessário (Windows com Chocolatey)
choco install wkhtmltopdf
```

### Arquivo muito grande
- Máximo permitido: 200MB
- Para arquivos maiores, considere dividir em partes menores

## 🔗 Links Úteis

- **GitHub**: [NEO-SH1W4/LogisticSmart](https://github.com/NEO-SH1W4/LogisticSmart)
- **Demo Online**: [LogisticSmart Demo](https://logisticsmartx33beta.streamlit.app/)
- **Documentação Streamlit**: [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Docs**: [plotly.com/python](https://plotly.com/python/)

## 📝 Changelog

### v2.0.0 (2025-01-07)
- 🆕 Reescrita completa da aplicação
- ✅ Sistema de autenticação seguro
- 📊 Dashboard interativo com Plotly
- 🎛️ Filtros adaptativos inteligentes
- 📥 Exportação em múltiplos formatos
- 🔍 Análise de qualidade dos dados
- ⚡ Cache e otimizações de performance
- 🎨 Interface moderna e responsiva

### v1.0.0 (2025-03-22)
- 🎉 Primeira versão funcional
- 📊 Análise básica de entregas
- 📄 Exportação para Excel

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**NEO-SH1W4**
- GitHub: [@NEO-SH1W4](https://github.com/NEO-SH1W4)

---

⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!

**Desenvolvido com ❤️ e ☕ por NEO-SH1W4**

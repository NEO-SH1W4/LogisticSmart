# Contribuindo para o LogisticSmart 🚀

Obrigado pelo interesse em contribuir para o LogisticSmart! Este documento fornece diretrizes para contribuir com o projeto.

## 🌟 Como Contribuir

### 1. Preparando o Ambiente

1. Faça um fork do repositório
2. Clone seu fork: `git clone https://github.com/seu-usuario/LogisticSmart.git`
3. Adicione o upstream: `git remote add upstream https://github.com/NEO-SH1W4/LogisticSmart.git`
4. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```
5. Instale as dependências de desenvolvimento: `pip install -e ".[dev]"`

### 2. Fluxo de Trabalho

1. Sincronize seu fork: `git fetch upstream && git merge upstream/main`
2. Crie um branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   # ou para correções
   git checkout -b fix/nome-do-bug
   ```
3. Faça suas alterações seguindo as convenções de código
4. Teste suas alterações: `pytest`
5. Verifique a formatação do código:
   ```bash
   black .
   isort .
   flake8 .
   ```
6. Commit suas alterações seguindo as [Conventional Commits](https://www.conventionalcommits.org/)
7. Push para seu fork: `git push origin feature/nome-da-feature`
8. Abra um Pull Request

### 3. Padrões de Código

Este projeto segue os seguintes padrões:

- **Python**: PEP 8 com formatação Black (88 caracteres por linha)
- **Docstrings**: Google Style
- **Imports**: Agrupados por builtin → externos → internos (usando isort)
- **Testes**: pytest para todos os novos recursos
- **Type Hints**: Sempre usar type hints para novas funções

## 📋 Tipos de Contribuições

### Funcionalidades

Para novas funcionalidades, primeiro abra uma issue para discutir o escopo e a implementação.

### Bugs

Para correções de bugs, verifique se há uma issue existente. Se não, crie uma nova com:
- Passos para reproduzir
- Comportamento esperado
- Comportamento atual
- Ambiente (OS, Python version, etc.)

### Documentação

A documentação é crucial! Melhorias são sempre bem-vindas:
- Exemplos de uso
- Melhorias no README
- Docstrings em funções e classes
- Documentação mais detalhada em arquivos `.md`

## 🧪 Testes

Todos os Pull Requests devem incluir testes para novas funcionalidades ou correções de bugs:

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Apenas testes específicos
pytest tests/test_specific_module.py
```

## 📈 CI/CD

O projeto utiliza GitHub Actions para:
- Lint e verificação de formatação
- Testes automáticos
- Build do pacote
- Deploy para demo (em branches principais)

Todos os checks devem passar para que um PR seja aceito.

## 📝 Changelog

O CHANGELOG.md é mantido automaticamente. Use Conventional Commits para que suas alterações sejam refletidas corretamente:

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, sem mudança no código
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes
- `chore`: Alterações em build, CI, etc.

## 🎯 Ciclo de Releases

- **Versões Minor**: Mensalmente (novas funcionalidades)
- **Versões Patch**: Conforme necessário (correções)
- **Versões Major**: Planejadas (breaking changes)

## 🙏 Código de Conduta

- Seja respeitoso com outros contribuidores
- Forneça feedback construtivo
- Foque na qualidade do código e nas melhores práticas
- Ajude outros contribuidores quando possível

## ❓ Dúvidas?

Abra uma issue ou participe das discussões no GitHub.

---

⭐ Seu esforço é valorizado! Obrigado por contribuir para o LogisticSmart!


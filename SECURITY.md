# Política de Segurança

## Versões Suportadas

As seguintes versões do LogisticSmart recebem atualizações de segurança:

| Versão | Suportada          |
| ------ | ------------------ |
| 2.0.x  | :white_check_mark: |
| 1.x.x  | :x:                |

## Relatando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança no LogisticSmart, pedimos que nos informe de forma responsável.

### Como Relatar

1. **NÃO** abra uma issue pública no GitHub
2. Envie um email para: [criar um email específico para segurança]
3. Inclua uma descrição detalhada da vulnerabilidade
4. Inclua passos para reproduzir o problema
5. Se possível, inclua uma correção sugerida

### O que Esperar

- **Confirmação**: Responderemos em até 48 horas
- **Avaliação**: Avaliaremos a vulnerabilidade em até 7 dias
- **Correção**: Trabalharemos para corrigir vulnerabilidades críticas em até 30 dias
- **Disclosure**: Coordenaremos a divulgação pública após a correção

### Escopo

As seguintes áreas estão no escopo de segurança:

- Sistema de autenticação e autorização
- Upload e processamento de arquivos
- Exportação de dados
- Validação de entrada de dados
- Armazenamento de credenciais
- Configurações de acesso

### Fora do Escopo

- Ataques de engenharia social
- Vulnerabilidades em dependências de terceiros (reporte aos mantenedores)
- Problemas que requerem acesso físico ao sistema

## Práticas de Segurança

### Para Desenvolvedores

- Use sempre type hints em Python
- Valide todas as entradas de usuário
- Use bibliotecas de hash seguras (bcrypt)
- Mantenha dependências atualizadas
- Execute testes de segurança regularmente

### Para Usuários

- Use senhas fortes e únicas
- Mantenha o software atualizado
- Não compartilhe credenciais
- Verifique a origem dos arquivos antes do upload
- Use HTTPS sempre que disponível

## Dependências de Segurança

O projeto utiliza as seguintes bibliotecas com foco em segurança:

- `bcrypt` para hash de senhas
- `python-dotenv` para variáveis de ambiente
- Validação rigorosa de tipos de arquivo
- Sanitização de dados de entrada

## Atualizações de Segurança

As atualizações de segurança são distribuídas através de:

- Releases no GitHub
- Notificações no README
- Issues de segurança (quando apropriado)

## Conformidade

Este projeto segue as melhores práticas de segurança para:

- OWASP Top 10
- Princípios de segurança por design
- Validação de entrada rigorosa
- Controle de acesso baseado em funções

---

**Nota**: Esta política de segurança é específica para o LogisticSmart. Para questões de segurança relacionadas ao Streamlit ou outras dependências, consulte suas respectivas políticas de segurança.


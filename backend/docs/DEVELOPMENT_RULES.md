# DEVELOPMENT_RULES.md

# Regras de Desenvolvimento

Este documento define as regras obrigatórias para qualquer desenvolvedor ou IA que realize alterações neste projeto.

O objetivo é preservar a arquitetura, facilitar a manutenção e evitar regressões.

---

# Princípios

Todo desenvolvimento deve priorizar:

* Simplicidade.
* Clareza.
* Organização.
* Baixo acoplamento.
* Alta coesão.
* Facilidade de manutenção.
* Compatibilidade com o restante do sistema.

Sempre prefira soluções simples antes de soluções complexas.

---

# Leitura obrigatória

Antes de realizar qualquer alteração, leia obrigatoriamente:

1. `docs/README.md`
2. `docs/architecture.md`
3. `docs/modules.md`
4. `docs/api.md`
5. `docs/developer-guide.md`
6. Este arquivo (`DEVELOPMENT_RULES.md`)

Nenhuma implementação deve ser iniciada sem compreender a arquitetura atual.

---

# Nunca faça

Nunca:

* Reescreva módulos inteiros sem necessidade.
* Faça refatorações não solicitadas.
* Altere comportamento de funcionalidades existentes sem autorização.
* Crie novos padrões arquiteturais sem justificativa.
* Duplique código.
* Ignore padrões já existentes.
* Renomeie arquivos ou diretórios sem necessidade.
* Adicione dependências externas sem necessidade real.
* Remova funcionalidades existentes sem autorização explícita.
* Atualize diversas partes do sistema quando apenas um módulo precisa ser alterado.

---

# Sempre faça

Sempre:

* Entenda o fluxo antes de modificar.
* Identifique exatamente quais arquivos serão alterados.
* Faça a menor alteração possível.
* Reutilize código existente.
* Mantenha compatibilidade com o restante do projeto.
* Preserve APIs públicas existentes.
* Atualize a documentação ao final.
* Explique o impacto da alteração.

---

# Escopo das alterações

Cada tarefa deve alterar somente os arquivos necessários.

Evite modificações em arquivos não relacionados.

Quanto menor o impacto, melhor.

---

# Antes de implementar

Sempre identifique:

* Qual problema será resolvido.
* Quais módulos são afetados.
* Quais arquivos precisam ser modificados.
* Quais riscos existem.
* Como garantir compatibilidade.

---

# Após implementar

Sempre verificar:

* O projeto continua funcionando.
* Não existem erros de sintaxe.
* Não existem imports quebrados.
* Não existem referências inválidas.
* Não existem funções órfãs.
* A documentação continua correta.

---

# Documentação

Toda alteração deve manter a pasta `docs` sincronizada.

Sempre atualizar quando houver mudanças em:

* arquitetura
* rotas
* módulos
* fluxos
* configuração
* instalação
* comportamento do sistema

Nunca deixe documentação desatualizada.

---

# Criação de novos módulos

Ao criar um módulo:

* siga a organização existente;
* mantenha o mesmo padrão de nomenclatura;
* documente sua responsabilidade;
* documente suas dependências;
* documente sua integração.

Todo novo módulo deve possuir responsabilidade única.

---

# Alterações em APIs

Toda alteração de rota deve atualizar:

* api.md
* flow.md (quando necessário)
* architecture.md (caso a arquitetura seja afetada)

Sempre informar:

* endpoint
* método HTTP
* parâmetros
* resposta
* fluxo interno

---

# Refatoração

Refatorações devem:

* manter o comportamento externo;
* melhorar organização;
* reduzir complexidade;
* reduzir duplicação;
* preservar compatibilidade.

Nunca misture refatoração com implementação de novas funcionalidades.

---

# Tratamento de erros

Sempre:

* tratar erros esperados;
* registrar mensagens úteis;
* evitar exceções silenciosas;
* retornar informações claras ao usuário.

---

# Logging

Logs devem:

* ser objetivos;
* facilitar depuração;
* evitar excesso de informações;
* conter contexto suficiente para identificar problemas.

---

# Organização do código

Priorizar:

* funções pequenas;
* responsabilidades únicas;
* nomes claros;
* baixo acoplamento;
* alta reutilização.

Evite funções extremamente longas.

---

# Performance

Antes de otimizar:

* identifique gargalos reais;
* não faça otimizações prematuras;
* preserve legibilidade.

---

# Dependências

Antes de instalar qualquer biblioteca:

* verificar se o projeto já possui solução equivalente;
* justificar sua necessidade;
* preferir bibliotecas maduras e amplamente utilizadas.

---

# Compatibilidade

Toda alteração deve preservar:

* APIs existentes;
* arquivos de configuração;
* estrutura do projeto;
* comportamento esperado.

Mudanças incompatíveis devem ser explicitamente autorizadas.

---

# Convenções

Seguir sempre:

* padrão de nomenclatura existente;
* estrutura de diretórios existente;
* estilo de código existente;
* arquitetura existente.

---

# Fluxo obrigatório para qualquer tarefa

1. Ler a documentação.
2. Compreender a arquitetura.
3. Identificar os arquivos afetados.
4. Explicar o plano de implementação.
5. Implementar somente o necessário.
6. Verificar impactos.
7. Atualizar documentação.
8. Informar exatamente quais arquivos foram alterados.

---

# Em caso de dúvida

Nunca assumir comportamento.

Quando houver ambiguidade:

* interrompa a implementação;
* explique a dúvida;
* solicite esclarecimentos.

---

# Objetivo final

Toda alteração deve deixar o projeto:

* mais organizado;
* mais simples;
* mais consistente;
* melhor documentado;
* fácil de manter;
* sem regressões.

A documentação deve sempre refletir fielmente o código-fonte, e o código-fonte deve permanecer coerente com a arquitetura definida. Ambos são considerados fontes oficiais do projeto.

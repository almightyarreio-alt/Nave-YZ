# 📜 Leis dos Observadores

> Os Observadores são os sentinelas do planeta.
>
> Eles permanecem atentos ao ambiente, percebendo mudanças, sinais e acontecimentos.
>
> Um Observador nunca executa o trabalho do planeta.
>
> Sua missão é perceber, registrar quando necessário e despertar o Habitante correto.

---

# 👁️ Observadores

## Representam

Os mecanismos responsáveis por detectar acontecimentos no planeta.

Equivalente técnico:

```text
Watchers
Listeners
Hooks
Event Handlers
Subscribers
Monitores
Triggers
```

No Arreiowork, todos são conhecidos como:

```text
Observadores
```

---

# Propósito

Observar continuamente o planeta e informar quando algo relevante acontece.

Os Observadores não tomam decisões.

Eles apenas dizem:

> "Algo aconteceu."

---

# Responsabilidades

* Observar eventos.
* Detectar mudanças.
* Escutar sinais.
* Notificar Habitantes.
* Registrar acontecimentos importantes nas Crônicas.
* Permanecer atentos durante a existência do planeta.

---

# Pode

* Monitorar diretórios.
* Escutar WebSockets.
* Escutar filas.
* Escutar eventos do sistema.
* Monitorar arquivos.
* Monitorar processos.
* Detectar mudanças na Memória.
* Despertar Habitantes.
* Consultar Cifras para compreender eventos.

---

# Não Pode

* Executar regras de negócio.
* Resolver problemas.
* Manipular a Memória.
* Expor Portais.
* Construir interfaces.
* Tomar decisões.

---

# Exemplo Narrativo

```text
O Observador vigia a floresta.

Uma árvore cai.

Ele não tenta levantá-la.

Ele apenas informa:

"Habitante Florestal,
uma árvore acabou de cair."

O Habitante decide o que fazer.
```

---

# O Ciclo da Observação

```text
Mudança
      │
      ▼
👁️ Observador
      │
      ▼
📖 Crônicas (quando relevante)
      │
      ▼
👤 Habitante
      │
      ▼
Ação executada
```

O Observador nunca realiza a ação.

Ele apenas desperta quem deve agir.

---

# Estrutura Recomendada

Os Observadores devem ser organizados conforme aquilo que observam.

```text
observadores/
│
├── diretorios.py
├── navegador.py
├── memoria.py
├── filas.py
├── websocket.py
├── sistema.py
├── processos.py
└── arquivos.py
```

Nunca:

```text
observadores/
│
└── eventos.py
```

Cada Observador deve possuir um campo de vigilância bem definido.

---

# Especialização

Cada Observador observa apenas um tipo de acontecimento.

Exemplos:

```text
Observador de Diretórios

Detecta criação,
alteração e remoção de arquivos.

--------------------------------

Observador de Navegador

Detecta abertura,
fechamento e falhas.

--------------------------------

Observador de WebSocket

Detecta conexões,
desconexões e mensagens.

--------------------------------

Observador do Sistema

Detecta inicialização,
encerramento e mudanças do ambiente.
```

---

# Cooperação

Os Observadores nunca trabalham sozinhos.

Eles sempre notificam algum Habitante.

```text
Arquivo alterado
        │
        ▼
👁️ Observador Diretório
        │
        ▼
👤 Habitante Arquivos
        │
        ▼
📖 Crônicas
```

---

# O que pertence aos Observadores

✅ Watchers.

✅ Hooks.

✅ Listeners.

✅ Subscribers.

✅ Monitoramento.

✅ Escuta de eventos.

✅ Detecção de alterações.

---

# O que NÃO pertence aos Observadores

❌ Processamento.

❌ Automações.

❌ Regras de negócio.

❌ APIs.

❌ Interface.

❌ Persistência.

❌ Decisões.

---

# 📜 Leis Gerais dos Observadores

### I. Um Observador apenas observa.

Se ele começa a executar tarefas, deixou de ser um Observador e passou a agir como um Habitante.

---

### II. Todo acontecimento importante pode possuir um Observador.

Mas nem todo acontecimento precisa de um.

Criar Observadores apenas quando houver necessidade de vigilância contínua.

---

### III. Observadores despertam Habitantes.

Nunca executam o trabalho por conta própria.

---

### IV. Um Observador deve permanecer imparcial.

Ele registra o que aconteceu.

Jamais interpreta intenções ou aplica regras.

---

### V. Cada Observador possui um único campo de vigilância.

Misturar diferentes tipos de eventos no mesmo Observador dificulta sua manutenção.

---

### VI. Observadores devem ser silenciosos.

Quando nada acontece, eles apenas permanecem atentos.

Não devem consumir recursos desnecessários nem produzir registros constantes sem motivo.

---

### VII. Observadores não conhecem o resultado da missão.

Depois de despertar um Habitante, sua responsabilidade termina.

O sucesso ou a falha da execução pertence ao Habitante.

---

### VIII. Um mesmo acontecimento pode despertar vários Habitantes.

Quando necessário, um Observador pode notificar mais de um especialista.

Exemplo:

```text
Arquivo criado
      │
      ▼
👁️ Observador Diretório
      │
      ├────────► 👤 Habitante Indexador
      │
      ├────────► 👤 Habitante Auditor
      │
      └────────► 👤 Habitante Notificador
```

O Observador continua apenas observando.

---

### IX. Observadores não criam acontecimentos.

Eles apenas reagem aos acontecimentos existentes.

---

### X. A vigilância deve ser contínua e confiável.

Enquanto o planeta estiver desperto, os Observadores responsáveis devem permanecer atentos ao seu domínio.

---

# Sinais de Violação

Um Observador está incorreto quando:

❌ Executa Playwright.

❌ Altera bancos de dados.

❌ Move arquivos.

❌ Faz chamadas HTTP de negócio.

❌ Contém regras complexas.

❌ Decide o que deve acontecer.

❌ Assume responsabilidades de um Habitante.

---

# Sinais de Saúde

Um bom Observador:

✅ É especializado.

✅ É leve.

✅ Detecta rapidamente mudanças.

✅ Desperta o Habitante correto.

✅ Não executa processamento pesado.

✅ Registra apenas eventos relevantes.

✅ Pode ser substituído sem alterar o restante do planeta.

---

# Princípio Fundamental

> **Os Observadores são os olhos e os ouvidos do planeta.**
>
> **Eles não trabalham, não decidem e não constroem.**
>
> **Sua missão é permanecer atentos, perceber as mudanças do mundo ao seu redor e despertar os Habitantes certos no momento certo.**
>
> **Sem Observadores, o planeta continua existindo, mas deixa de perceber quando o universo muda ao seu redor.** 👁️

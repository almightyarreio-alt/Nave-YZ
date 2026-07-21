# 📜 Leis dos Habitantes

> Os Habitantes são aqueles que dão vida ao planeta.
>
> Toda ação, toda missão e todo trabalho realizado dentro do planeta acontece através de um Habitante.
>
> Eles são os trabalhadores, exploradores, construtores e especialistas que mantêm o planeta funcionando.
>
> Nenhum Habitante existe sem um propósito.

---

# 👤 Habitantes

## Representam

Os agentes responsáveis por executar as tarefas do planeta.

Equivalente técnico:

```text
Services
Classes de domínio
Workers
Casos de uso
Processadores
Executores
```

No Arreiowork, todos são conhecidos como:

```text
Habitantes
```

---

# Propósito

Transformar intenções em ações.

Enquanto os Portais recebem pedidos, os Habitantes realizam o trabalho necessário para atendê-los.

---

# Responsabilidades

* Executar tarefas.
* Resolver problemas.
* Coordenar missões.
* Consultar as Leis.
* Utilizar a Memória.
* Registrar Crônicas.
* Colaborar com outros Habitantes quando necessário.

---

# Pode

* Consultar as Leis.
* Ler e atualizar a Memória.
* Registrar Crônicas.
* Utilizar Cifras.
* Ser chamado por Portais.
* Ser despertado por Observadores.
* Trabalhar em conjunto com outros Habitantes especializados.

---

# Não Pode

* Expor APIs.
* Receber diretamente visitantes.
* Monitorar acontecimentos continuamente.
* Definir regras do planeta.
* Alterar contratos das Cifras.
* Construir interfaces da Civilização.

---

# Exemplo Narrativo

```text
Um visitante solicita a criação de um novo perfil.

O Portal recebe o pedido.

O Habitante responsável pela administração de perfis é chamado.

Ele consulta as Leis.

Verifica a Memória.

Realiza a criação.

Registra a ação nas Crônicas.

Retorna o resultado ao Portal.
```

---

# O Ciclo de Trabalho

```text
Visitante
      │
      ▼
🚪 Portal
      │
      ▼
👤 Habitante
      │
      ├────────► 📜 Leis
      │
      ├────────► 🧠 Memória
      │
      ├────────► 📜 Cifras
      │
      └────────► 📖 Crônicas
      │
      ▼
🚪 Portal
      │
      ▼
Resposta
```

O Habitante é o centro da execução.

---

# Estrutura Recomendada

Os Habitantes devem ser organizados conforme sua especialidade.

```text
habitantes/
│
├── navegador.py
├── perfis.py
├── fluxos.py
├── variaveis.py
├── autenticacao.py
├── notificacoes.py
├── arquivos.py
└── observabilidade.py
```

Cada Habitante possui uma missão clara.

Nunca:

```text
habitantes/
│
└── utils.py
```

Um Habitante sem missão definida enfraquece a organização do planeta.

---

# Especialização

Cada Habitante deve possuir apenas uma profissão.

Exemplos:

```text
Habitante Navegador

Especialista em controlar navegadores.

--------------------------------

Habitante Fluxo

Especialista em executar fluxos.

--------------------------------

Habitante Perfil

Especialista em administrar identidades.

--------------------------------

Habitante Arquivos

Especialista em manipular arquivos.

--------------------------------

Habitante Notificador

Especialista em enviar notificações.
```

Nenhum Habitante deve tentar dominar todas as profissões.

---

# Cooperação

Os Habitantes podem trabalhar juntos.

Exemplo:

```text
Habitante Fluxo

        │

        ├────────► Habitante Navegador

        │

        ├────────► Habitante Arquivos

        │

        └────────► Habitante Notificador
```

Cada um realiza apenas sua especialidade.

---

# O que pertence aos Habitantes

✅ Automações.

✅ Processamentos.

✅ Casos de uso.

✅ Integrações.

✅ Manipulação de arquivos.

✅ Chamadas externas.

✅ Execução de Playwright.

✅ Comunicação entre especialistas.

---

# O que NÃO pertence aos Habitantes

❌ Interfaces.

❌ Layouts.

❌ Endpoints.

❌ Configurações.

❌ Contratos.

❌ Logs como responsabilidade principal.

❌ Observação contínua de eventos.

---

# 📜 Leis Gerais dos Habitantes

### I. Todo Habitante possui uma profissão.

Se sua responsabilidade não puder ser resumida em uma frase, provavelmente ele está fazendo mais do que deveria.

---

### II. Todo trabalho do planeta pertence a algum Habitante.

Se ninguém é responsável por uma tarefa, o planeta está incompleto.

---

### III. Habitantes consultam as Leis antes de agir.

Eles executam.

As Leis decidem.

---

### IV. Habitantes preservam a história.

Toda ação importante deve gerar uma Crônica.

---

### V. Habitantes compartilham conhecimento através da Memória.

Eles não armazenam estado permanente em si mesmos quando esse estado pertence ao planeta.

---

### VI. Habitantes colaboram, mas não assumem profissões alheias.

Quando uma missão exige conhecimentos diferentes, cada Habitante executa sua parte.

---

### VII. Um Habitante nunca conversa diretamente com um visitante.

Toda comunicação com o exterior acontece através dos Portais.

---

### VIII. Um Habitante deve ser substituível.

Outro Habitante com a mesma profissão deve conseguir assumir sua função sem exigir mudanças em todo o planeta.

---

### IX. Todo Habitante deve deixar rastros.

Suas ações importantes devem ser registradas nas Crônicas, permitindo que a história do planeta seja compreendida.

---

### X. Um Habitante existe para servir ao planeta.

Ele não busca controlar outros elementos; sua função é executar sua missão com excelência.

---

# Sinais de Violação

Um Habitante está incorreto quando:

❌ Responde requisições HTTP.

❌ Constrói telas.

❌ Contém centenas de responsabilidades.

❌ Define regras estruturais das Cifras.

❌ Monitora eventos continuamente (isso pertence aos Observadores).

❌ Decide políticas do planeta (isso pertence às Leis).

❌ Faz tudo sozinho quando existem Habitantes especializados.

---

# Sinais de Saúde

Um bom Habitante:

✅ Possui uma missão clara.

✅ Resolve um tipo específico de problema.

✅ Consulta as Leis.

✅ Utiliza a Memória corretamente.

✅ Registra Crônicas.

✅ Coopera com outros Habitantes.

✅ Pode ser compreendido rapidamente por qualquer Explorador.

---

# Princípio Fundamental

> **Os Habitantes são a força de trabalho do planeta.**
>
> **Enquanto os Portais recebem pedidos, as Leis orientam, a Memória preserva, as Cifras organizam e as Crônicas registram, são os Habitantes que transformam intenções em realidade.**
>
> **Sem Habitantes, um planeta pode existir... mas jamais poderá agir.** 👤

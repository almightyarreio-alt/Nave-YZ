# 📜 Leis da Memória

> A Memória é onde o planeta preserva seu conhecimento.
>
> Tudo aquilo que precisa sobreviver ao tempo deve ser confiado à Memória.
>
> Os Habitantes podem consultar e atualizar a Memória, mas ela não toma decisões, não executa tarefas e não interpreta informações.
>
> A Memória apenas guarda aquilo que lhe é confiado.

---

# 🧠 Memória

## Representa

Todos os mecanismos de persistência e armazenamento do planeta.

Equivalente técnico:

```text
Banco de Dados

Arquivos

JSON

SQLite

PostgreSQL

MySQL

Redis

Cache

Estado Persistente

Armazenamento Local

Blob Storage
```

No Arreiowork, todos pertencem à:

```text
Memória
```

---

# Propósito

Preservar o conhecimento do planeta.

Quando um Habitante precisa lembrar de algo amanhã, daqui a um mês ou após reiniciar o planeta, essa informação pertence à Memória.

---

# Responsabilidades

* Armazenar informações.
* Recuperar informações.
* Atualizar informações.
* Remover informações quando autorizado.
* Preservar o estado do planeta.
* Garantir a integridade dos dados.

---

# Pode

* Salvar dados.
* Ler dados.
* Atualizar registros.
* Excluir registros.
* Organizar coleções.
* Manter cache.
* Versionar informações quando necessário.

---

# Não Pode

* Executar lógica de negócio.
* Decidir regras.
* Expor APIs.
* Monitorar eventos.
* Construir interfaces.
* Registrar Crônicas por iniciativa própria.

---

# Exemplo Narrativo

```text
Um Habitante encontra um novo conhecimento.

Ele pergunta:

"Isso precisa ser lembrado no futuro?"

Se a resposta for sim,
ele entrega esse conhecimento à Memória.

A Memória o preserva.

Anos depois,
outro Habitante poderá consultá-lo.
```

---

# O Ciclo da Memória

```text
👤 Habitante
      │
      ▼
🧠 Memória
      │
      ▼
Conhecimento preservado
      │
      ▼
👤 Outro Habitante
```

A Memória nunca inicia uma conversa.

Ela apenas responde quando consultada.

---

# Estrutura Recomendada

A Memória deve ser organizada conforme o tipo de conhecimento armazenado.

```text
memoria/
│
├── perfis/
├── fluxos/
├── configuracoes/
├── variaveis/
├── cache/
├── arquivos/
├── banco/
└── temporarios/
```

---

# Tipos de Memória

## Memória Permanente

Informações que sobrevivem ao reinício do planeta.

Exemplos

```text
Perfis

Fluxos

Configurações

Usuários

Histórico persistente
```

---

## Memória Temporária

Existe apenas durante a execução.

Exemplos

```text
Cache

Sessões

Estados transitórios

Resultados temporários
```

---

## Memória Compartilhada

Conhecimento acessado por diversos Habitantes.

Exemplos

```text
Banco de Dados

Redis

Arquivos Compartilhados
```

---

# O que pertence à Memória

✅ Banco de dados.

✅ Arquivos JSON.

✅ SQLite.

✅ PostgreSQL.

✅ Cache.

✅ Sessões.

✅ Configurações persistentes.

✅ Estados persistentes.

✅ Arquivos de armazenamento.

---

# O que NÃO pertence à Memória

❌ Regras de negócio.

❌ Processamentos.

❌ Interfaces.

❌ APIs.

❌ Eventos.

❌ Logs.

❌ Validações.

❌ Automações.

---

# 📜 Leis Gerais da Memória

### I. A Memória apenas preserva.

Ela nunca interpreta o significado daquilo que armazena.

---

### II. Apenas Habitantes alteram a Memória.

Nenhum Portal, Observador ou elemento da Civilização deve modificar diretamente o conhecimento do planeta.

---

### III. A Memória responde.

Ela nunca inicia ações por conta própria.

Sempre aguarda que um Habitante solicite uma leitura ou alteração.

---

### IV. O conhecimento possui um único lar.

Cada informação deve possuir um local oficial dentro da Memória.

Duplicações desnecessárias enfraquecem a consistência do planeta.

---

### V. A Memória deve ser independente.

O planeta pode trocar JSON por SQLite, PostgreSQL ou outro mecanismo sem alterar o comportamento dos Habitantes.

Os Habitantes conhecem **o conhecimento**, não a tecnologia utilizada para armazená-lo.

---

### VI. A Memória deve preservar a integridade.

Nenhuma alteração deve deixar o planeta em um estado inconsistente.

Se uma operação falhar, a Memória deve permanecer íntegra.

---

### VII. O conhecimento permanente deve sobreviver ao despertar.

Após a Superfície reiniciar o planeta, a Memória deve continuar lembrando daquilo que lhe foi confiado.

---

### VIII. O conhecimento temporário deve desaparecer quando sua missão terminar.

Nem toda informação merece ser lembrada para sempre.

O que é transitório deve permanecer apenas enquanto for útil.

---

### IX. A Memória não substitui as Crônicas.

A Memória representa **o presente**.

As Crônicas representam **o passado**.

Exemplo:

```text
Memória

Perfil:
Nome = Otto

------------------------

Crônicas

08:31
Perfil criado.

08:42
Nome alterado de Arreio para Otto.

09:10
Perfil atualizado.
```

A Memória mostra como o planeta está.

As Crônicas mostram como ele chegou até esse estado.

---

### X. A Memória pertence ao planeta.

Nenhum Habitante é dono das informações.

Os Habitantes apenas cuidam delas durante suas missões.

---

# Sinais de Violação

A Memória está incorreta quando:

❌ Contém regras de negócio.

❌ Executa cálculos.

❌ Faz chamadas HTTP.

❌ Dispara eventos por iniciativa própria.

❌ Decide o comportamento do planeta.

❌ Conhece detalhes da Civilização.

❌ Depende diretamente de Portais.

---

# Sinais de Saúde

Uma boa Memória:

✅ É organizada.

✅ É consistente.

✅ É confiável.

✅ Pode ser substituída sem afetar os Habitantes.

✅ Preserva o conhecimento do planeta.

✅ É simples de consultar.

---

# Princípio Fundamental

> **A Memória não pensa, não decide e não executa.**
>
> **Ela existe para preservar o conhecimento do planeta através do tempo.**
>
> **Enquanto os Habitantes realizam missões, os Portais recebem visitantes, os Observadores vigiam e as Crônicas contam a história, é a Memória que garante que o planeta jamais esqueça aquilo que realmente importa.** 🧠

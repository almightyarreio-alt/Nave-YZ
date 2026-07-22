# 01. Fundamentos (Por quê?)

Os Fundamentos não explicam **como** construir software.

Eles explicam **por que** o ArreioWork existe.

É a camada mais abstrata do framework e serve como referência para todas as demais. Nenhuma decisão arquitetural deve contrariar seus princípios.

```text
Fundamentos/
│
├── 00_prefacio.md
├── 01_manifesto.md
├── 02_proposito.md
├── 03_filosofia.md
├── 04_principios.md
├── 05_axiomas.md
├── 06_glossario_fundamental.md
├── 07_modelo_mental.md
└── 08_constituicao.md
```

---

# 00_prefacio.md

## Objetivo

Apresentar o ArreioWork.

Não fala de código.

Não fala de arquitetura.

Não fala de tecnologia.

Responde apenas:

> O que é o ArreioWork?

Conteúdo:

* O problema que motivou sua criação.
* O motivo da linguagem inspirada na astronomia.
* O público-alvo.
* O que o framework pretende resolver.
* O que ele não pretende resolver.

---

# 01_manifesto.md

O Manifesto representa a identidade do framework.

É um documento filosófico.

Exemplo de tópicos:

* Software é conhecimento organizado.
* Arquitetura é comunicação.
* Pessoas entendem histórias antes de estruturas.
* Todo sistema deve possuir identidade.
* Clareza supera complexidade.
* A documentação faz parte do software.
* O software deve explicar a si mesmo.

Este documento muda muito pouco ao longo do tempo.

---

# 02_proposito.md

Este documento responde apenas uma pergunta.

> Por que o ArreioWork existe?

Estrutura:

## Problema

Como o software costuma ser desenvolvido hoje.

## Consequências

Dificuldade de manutenção.

Curva de aprendizado.

Dependência de pessoas.

Documentação inconsistente.

## Objetivo

Criar uma linguagem universal para organização de sistemas.

## Resultado esperado

Projetos compreensíveis.

Arquitetura consistente.

Documentação integrada.

Comunicação entre equipes.

---

# 03_filosofia.md

Aqui nasce a visão do universo.

Conceitos:

Software é um organismo.

Arquitetura é geografia.

Componentes possuem funções sociais.

A informação possui memória.

Toda ação gera história.

Toda comunicação ocorre por contratos.

O software é tratado como um ecossistema vivo.

---

# 04_principios.md

São princípios que orientam decisões.

Não são regras.

Exemplos:

## Clareza

Um sistema deve ser compreendido antes de ser otimizado.

---

## Responsabilidade

Cada elemento possui uma função principal.

---

## Evolução

Todo sistema deve permitir evolução sem destruir sua identidade.

---

## Observabilidade

Tudo que importa deve poder ser observado.

---

## Persistência

Conhecimento importante não deve desaparecer.

---

## Comunicação

A comunicação deve ocorrer através de contratos explícitos.

---

## Independência

Componentes devem possuir baixo acoplamento.

---

## Simplicidade

A solução mais simples que resolve corretamente o problema possui prioridade.

---

# 05_axiomas.md

Aqui entram verdades consideradas universais.

Não precisam ser justificadas.

Exemplos.

Axioma 1

Todo software existe para resolver um problema.

---

Axioma 2

Nenhum componente existe sem responsabilidade.

---

Axioma 3

Toda informação possui origem.

---

Axioma 4

Todo comportamento produz consequências.

---

Axioma 5

Toda decisão possui contexto.

---

Axioma 6

Toda comunicação depende de um contrato.

---

Axioma 7

Nenhum sistema permanece imutável.

---

Axioma 8

Toda arquitetura representa uma forma de organização.

---

Os axiomas dão base lógica para todas as leis futuras.

---

# 06_glossario_fundamental.md

Antes de existir lore...

Existem conceitos.

Cada termo possui exatamente cinco campos.

```
Nome

Definição

Objetivo

Características

Exemplos
```

Exemplo.

---

Conhecimento

Definição

Informação organizada que possui significado.

Objetivo

Permitir tomada de decisão.

Características

Persistente.

Consultável.

Compartilhável.

Exemplos

Banco.

Documento.

Arquivo.

---

Depois vêm termos como:

* Organização
* Sistema
* Componente
* Comunicação
* Estado
* Evento
* Identidade
* Memória
* Responsabilidade

Sem ainda citar "Planeta" ou "Habitante". Primeiro definimos os conceitos universais; a lore vem depois para representá-los.

---

# 07_modelo_mental.md

Este documento ensina como pensar usando o ArreioWork.

Fluxo:

```
Problema

↓

Objetivo

↓

Sistema

↓

Organização

↓

Componentes

↓

Comunicação

↓

Persistência

↓

Observação

↓

Evolução
```

Só depois, nas próximas camadas, esses conceitos recebem nomes como Universo, Planeta, Habitante e Portal.

---

# 08_constituicao.md

Este é o documento normativo.

Não explica.

Determina.

Formato sugerido:

```
Título

Capítulo

Artigo

Parágrafo

Inciso
```

Exemplo.

---

Título I

Da Existência

Art. 1º

Todo software organizado sob o ArreioWork é considerado um Sistema pertencente ao Universo ArreioWork.

Art. 2º

Todo Sistema deverá possuir identidade própria.

Art. 3º

Todo Sistema deverá possuir propósito claramente definido.

Art. 4º

Nenhum componente poderá existir sem responsabilidade principal.

Art. 5º

Todo comportamento relevante deverá ser observável.

---

# O diferencial que eu acrescentaria

Antes mesmo dos Fundamentos, criaria um documento chamado **"Metamodelo"**. Ele não descreve o universo do ArreioWork; descreve **como o próprio ArreioWork organiza conhecimento**.

Em vez de ser apenas um framework de software, ele passa a ser um **framework de modelagem**.

Esse metamodelo define três níveis bem distintos:

* **Conceitos**: ideias universais, como sistema, comunicação, estado, evento e responsabilidade.
* **Representações**: a linguagem da lore, que transforma esses conceitos em Universo, Planeta, Habitante, Portal, Livro e outros elementos fáceis de visualizar.
* **Implementações**: as tecnologias concretas que materializam essas representações, como FastAPI, React, PostgreSQL, Kafka, Docker ou qualquer outra.

Essa separação impede que o framework fique preso a uma linguagem ou tecnologia específica e faz do ArreioWork um modelo conceitual duradouro, capaz de orientar projetos independentemente da stack utilizada.

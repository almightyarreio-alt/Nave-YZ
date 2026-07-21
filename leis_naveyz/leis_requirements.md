# 📜 Leis das Dependências

> Nenhum planeta nasce sozinho.
>
> Todo planeta depende de recursos externos para existir e cumprir sua missão.
>
> As Dependências representam tudo aquilo que o planeta recebe do universo para ampliar suas capacidades.
>
> Elas não fazem parte da identidade do planeta.
>
> São ferramentas que ele utiliza durante sua existência.

---

# 📦 Dependências

## Representam

Todos os recursos externos necessários para o funcionamento do planeta.

Equivalente técnico:

```text
requirements.txt

pyproject.toml

package.json

Cargo.toml

go.mod

Bibliotecas

Frameworks

SDKs

Drivers
```

No Arreiowork, todas são conhecidas como:

```text
Dependências
```

---

# Propósito

Fornecer habilidades que o planeta ainda não possui.

As Dependências expandem as capacidades do planeta, permitindo que seus Habitantes realizem missões mais complexas.

---

# Responsabilidades

* Disponibilizar funcionalidades externas.
* Fornecer tecnologias reutilizáveis.
* Reduzir trabalho repetitivo.
* Integrar o planeta com o ecossistema tecnológico.
* Permitir evolução sem reinventar soluções.

---

# Pode

* Fornecer bibliotecas.
* Fornecer frameworks.
* Fornecer drivers.
* Fornecer clientes de APIs.
* Fornecer ferramentas de desenvolvimento.
* Ser utilizada pelos Habitantes, Portais, Observadores e pela Civilização.

---

# Não Pode

* Definir as Leis do planeta.
* Alterar a identidade do planeta.
* Conter regras de negócio.
* Organizar a arquitetura do planeta.
* Substituir Habitantes.

---

# Exemplo Narrativo

```text
Um Habitante precisa atravessar um oceano.

Ele não constrói um navio do zero.

O planeta já possui uma embarcação fornecida pelo universo.

O Habitante aprende a utilizá-la.

A missão continua.

O navio pertence ao universo.

A missão pertence ao planeta.
```

---

# O Ciclo das Dependências

```text
Universo
      │
      ▼
📦 Dependências
      │
      ▼
Planeta
      │
      ▼
👤 Habitantes
```

As Dependências fornecem capacidades.

Quem realiza o trabalho continua sendo o planeta.

---

# Estrutura Recomendada

Python

```text
requirements.txt
```

ou

```text
pyproject.toml
```

Node

```text
package.json
```

Rust

```text
Cargo.toml
```

Go

```text
go.mod
```

Independentemente da tecnologia, todos representam as Dependências do planeta.

---

# Exemplos

```text
FastAPI

Playwright

SQLAlchemy

Pydantic

Watchfiles

Requests

PySide6

OpenCV
```

Nenhuma dessas bibliotecas define como o planeta funciona.

Elas apenas oferecem novas capacidades.

---

# O que pertence às Dependências

✅ Frameworks.

✅ Bibliotecas.

✅ SDKs.

✅ Drivers.

✅ Ferramentas de desenvolvimento.

✅ Pacotes de terceiros.

---

# O que NÃO pertence às Dependências

❌ Código do planeta.

❌ Habitantes.

❌ Leis.

❌ Portais.

❌ Memória.

❌ Crônicas.

❌ Cifras.

❌ Identidades.

---

# 📜 Leis Gerais das Dependências

### I. Toda Dependência deve possuir um propósito.

Nenhuma biblioteca deve existir apenas porque "pode ser útil um dia".

---

### II. O planeta nunca depende de uma ferramenta quando pode depender de uma capacidade.

Os Habitantes devem conhecer **o que precisam fazer**, não **qual biblioteca realiza o trabalho**.

Exemplo:

O Habitante sabe que precisa controlar um navegador.

Ele não precisa conhecer Playwright.

---

### III. Quanto menos Dependências, mais saudável o planeta.

Cada nova Dependência aumenta a complexidade, o tempo de manutenção e os riscos de incompatibilidade.

---

### IV. Toda Dependência deve ser substituível.

Se amanhã uma biblioteca deixar de existir, o planeta deve conseguir sobreviver com outra equivalente, realizando apenas adaptações localizadas.

---

### V. As Dependências pertencem ao universo, não ao planeta.

Elas são ferramentas externas.

A identidade do planeta jamais deve depender exclusivamente de uma tecnologia específica.

---

### VI. As Dependências devem evoluir com responsabilidade.

Atualizações devem ser planejadas e testadas.

Uma nova versão pode trazer melhorias, mas também alterar comportamentos esperados.

---

### VII. Dependências nunca definem as Leis.

Frameworks não determinam a arquitetura.

Bibliotecas não determinam o comportamento.

O planeta continua governado por suas próprias Leis.

---

### VIII. Todo recurso externo deve ser conhecido.

O planeta deve saber:

* por que utiliza essa Dependência;
* quem a utiliza;
* qual problema ela resolve.

Dependências sem propósito tornam o planeta mais difícil de compreender.

---

### IX. O planeta deve proteger-se contra o desaparecimento das Dependências.

Sempre que possível, os Habitantes devem depender de abstrações próprias do planeta, reduzindo o impacto da troca de tecnologias.

---

### X. Uma Dependência é uma ferramenta, nunca um habitante.

Ela não possui responsabilidades dentro da arquitetura.

Ela apenas oferece recursos para que os verdadeiros Habitantes cumpram suas missões.

---

# Sinais de Violação

As Dependências estão incorretas quando:

❌ O planeta depende diretamente da lógica de um framework.

❌ Regras de negócio estão espalhadas por bibliotecas externas.

❌ Existem bibliotecas duplicando funcionalidades.

❌ Há Dependências não utilizadas.

❌ Trocar uma biblioteca exige reescrever todo o planeta.

---

# Sinais de Saúde

Boas Dependências:

✅ Possuem propósito claro.

✅ São poucas e bem escolhidas.

✅ São atualizadas com responsabilidade.

✅ Podem ser substituídas.

✅ Ampliam as capacidades do planeta sem controlar sua arquitetura.

---

# Princípio Fundamental

> **As Dependências não fazem parte do planeta.**
>
> **Elas são presentes vindos do universo.**
>
> **O planeta utiliza essas ferramentas para expandir suas capacidades, mas sua essência permanece em seus Habitantes, suas Leis, sua Memória, seus Portais e sua Civilização.**
>
> **Se todas as Dependências fossem substituídas por equivalentes, o planeta continuaria sendo o mesmo planeta.** 📦

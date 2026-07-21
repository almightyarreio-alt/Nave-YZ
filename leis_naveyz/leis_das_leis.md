# 📜 Leis das Leis

> As Leis representam a sabedoria do planeta.
>
> Elas definem o que é permitido, proibido e obrigatório.
>
> Nenhum Habitante cria suas próprias regras.
>
> Todos consultam as Leis antes de agir.
>
> Enquanto os Habitantes executam, as Leis determinam como essa execução deve acontecer.

---

# 📚 Leis

## Representam

As regras de negócio do planeta.

Equivalente técnico:

```text
Business Rules

Policies

Validators

Domain Rules

Use Case Rules

Permission Rules

Business Constraints
```

No Arreiowork, todas pertencem às:

```text
leis/
```

Ou, quando específicas do planeta:

```text
leis_naveyz/
```

---

# Propósito

Governar o comportamento do planeta.

As Leis garantem que todos os Habitantes tomem decisões de forma consistente, independentemente de quem esteja executando a missão.

---

# Responsabilidades

* Definir regras de negócio.
* Definir permissões.
* Definir restrições.
* Validar decisões.
* Garantir consistência.
* Proteger a integridade do planeta.

---

# Pode

* Validar informações.
* Autorizar ações.
* Negar ações.
* Definir limites.
* Definir comportamentos.
* Ser consultada por Habitantes.
* Utilizar Cifras para compreender estruturas.

---

# Não Pode

* Executar tarefas.
* Alterar Memórias.
* Abrir Portais.
* Construir interfaces.
* Monitorar eventos.
* Registrar Crônicas por conta própria.

---

# Exemplo Narrativo

```text
Um Habitante deseja apagar um Perfil.

Antes de agir,
ele consulta as Leis.

As Leis respondem:

"Perfis em utilização não podem ser removidos."

O Habitante respeita a decisão.

A missão termina.
```

As Leis não apagam o Perfil.

Elas apenas determinam se isso é permitido.

---

# O Ciclo das Leis

```text
Solicitação
      │
      ▼
👤 Habitante
      │
      ▼
📚 Leis
      │
      ▼
Permitido?
      │
 ┌────┴────┐
 │         │
 ▼         ▼
Sim       Não
 │         │
 ▼         ▼
Executa   Encerra
```

Toda decisão importante deve passar pelas Leis.

---

# Estrutura Recomendada

As Leis devem ser organizadas conforme o domínio do planeta.

```text
leis/
│
├── autenticacao.py
├── navegadores.py
├── perfis.py
├── fluxos.py
├── variaveis.py
├── seguranca.py
├── notificacoes.py
└── arquivos.py
```

Cada conjunto de Leis governa um aspecto específico do planeta.

---

# Exemplos

## Lei de Navegação

```text
Um navegador só pode ser iniciado
caso exista uma Identidade válida.
```

---

## Lei de Perfis

```text
Dois perfis
não podem possuir o mesmo nome.
```

---

## Lei de Fluxos

```text
Um fluxo não pode iniciar
caso outro fluxo exclusivo já esteja em execução.
```

---

## Lei de Segurança

```text
Somente administradores
podem remover Identidades.
```

---

# O que pertence às Leis

✅ Regras de negócio.

✅ Restrições.

✅ Permissões.

✅ Validações de domínio.

✅ Políticas.

✅ Limites.

✅ Critérios de decisão.

---

# O que NÃO pertence às Leis

❌ Interfaces.

❌ APIs.

❌ Persistência.

❌ Logs.

❌ Monitoramento.

❌ Configurações.

❌ Execução de tarefas.

---

# 📜 Leis Gerais das Leis

### I. Toda decisão pertence às Leis.

Se uma resposta depende de "pode ou não pode", essa resposta deve estar nas Leis.

---

### II. Os Habitantes executam.

As Leis decidem.

Misturar essas responsabilidades torna o planeta inconsistente.

---

### III. As Leis são imparciais.

Elas não conhecem quem está executando a missão.

Elas apenas avaliam os fatos apresentados.

---

### IV. Uma Lei deve representar uma única regra.

Se uma Lei responde muitas perguntas diferentes, ela provavelmente deve ser dividida.

---

### V. As Leis devem ser reutilizáveis.

Vários Habitantes podem consultar a mesma Lei.

Uma regra nunca deve ser duplicada em diferentes Habitantes.

---

### VI. As Leis devem ser previsíveis.

Para as mesmas condições, a decisão deve ser sempre a mesma.

---

### VII. Nenhum Habitante pode ignorar uma Lei.

Se uma missão exige uma decisão de negócio, ela deve consultar as Leis antes de agir.

---

### VIII. As Leis evoluem com o planeta.

Quando o negócio muda, as Leis mudam.

Os Habitantes continuam trabalhando, apenas seguindo as novas normas.

---

### IX. As Leis não conhecem tecnologia.

Uma Lei continua válida independentemente de o planeta utilizar FastAPI, Flask, SQLite, PostgreSQL, Playwright ou qualquer outra ferramenta.

As Leis descrevem o comportamento do planeta, não sua implementação.

---

### X. As Leis pertencem ao planeta.

Elas representam sua cultura, seus princípios e sua forma de existir.

Enquanto a tecnologia pode mudar, as Leis preservam a identidade do planeta.

---

# Sinais de Violação

As Leis estão incorretas quando:

❌ Fazem chamadas HTTP.

❌ Consultam bancos diretamente.

❌ Executam Playwright.

❌ Criam interfaces.

❌ Registram Crônicas.

❌ Contêm código de infraestrutura.

❌ Dependem de Portais ou da Civilização.

---

# Sinais de Saúde

Boas Leis:

✅ São claras.

✅ São pequenas.

✅ São reutilizáveis.

✅ São independentes da tecnologia.

✅ São consultadas por diversos Habitantes.

✅ Representam fielmente as regras do planeta.

---

# Princípio Fundamental

> **As Leis são a consciência do planeta.**
>
> **Elas não trabalham, não observam e não se comunicam com o universo.**
>
> **Sua missão é estabelecer os princípios que todos os Habitantes devem respeitar.**
>
> **Quando um Habitante pergunta "o que devo fazer?", as Leis respondem "o que é correto fazer".** 📚

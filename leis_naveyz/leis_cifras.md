# 📜 Leis das Cifras

> As Cifras representam o conhecimento estruturado do planeta.
>
> Elas definem como o planeta fala, quais regras de comunicação existem e como seus elementos devem ser configurados.
>
> As Cifras não executam ações.
> Elas apenas descrevem como as ações devem acontecer.

---

# 📜 Cifras

## Representam

Os contratos, configurações e definições do planeta.

Equivalente técnico:

```text
Configurações
Schemas
Modelos
DTOs
Contratos
Enums
Constantes
Arquivos .json
Arquivos .yaml
Arquivos .toml
Arquivos .env (quando apropriado)
```

No Arreiowork, todos pertencem às:

```text
Cifras
```

---

# Propósito

Garantir que todos os habitantes falam a mesma linguagem.

As Cifras eliminam ambiguidades.

Elas definem:

* quais informações existem;
* como elas devem ser escritas;
* quais valores são aceitos;
* quais configurações governam o planeta.

---

# Responsabilidades

* Definir contratos.
* Definir formatos.
* Definir configurações.
* Definir padrões.
* Definir valores padrão.
* Definir constantes.
* Organizar o conhecimento estrutural.

---

# Pode

* Definir Schemas.
* Definir modelos.
* Definir configurações.
* Definir tipos.
* Definir validações estruturais.
* Definir contratos entre Portais e Habitantes.
* Ser utilizada por qualquer elemento do planeta.

---

# Não Pode

* Executar lógica.
* Fazer cálculos.
* Ler banco.
* Escrever arquivos.
* Monitorar eventos.
* Chamar Habitantes.
* Abrir Portais.
* Registrar Crônicas.

---

# Exemplo Narrativo

```text
Um Portal recebe uma mensagem.

Antes de permitir sua entrada,
ele consulta as Cifras.

As Cifras respondem:

"Essa mensagem possui o formato correto."

O Portal então permite que ela siga para o Habitante.
```

---

# O Ciclo das Cifras

```text
Solicitação
      │
      ▼
🚪 Portal
      │
      ▼
📜 Cifras
      │
      ▼
✔ Estrutura válida?
      │
      ▼
👤 Habitante
```

As Cifras nunca participam da execução.

Elas apenas orientam.

---

# Estrutura Recomendada

```text
cifras/
│
├── configuracoes/
│
├── contratos/
│
├── modelos/
│
├── constantes/
│
├── enumeracoes/
│
├── validacoes/
│
└── idiomas/
```

---

# Exemplos

## Configuração

```python
class ConfiguracaoServidor:

    host = "127.0.0.1"

    porta = 8000
```

---

## Contrato

```python
class CriarPerfil:

    nome: str

    navegador: str
```

---

## Enumeração

```python
class EstadoFluxo(Enum):

    PARADO

    EXECUTANDO

    FINALIZADO
```

---

## Constante

```python
MAXIMO_DE_TENTATIVAS = 5
```

Nenhum desses objetos executa trabalho.

Eles apenas definem conhecimento.

---

# O que pertence às Cifras

✅ Configurações.

✅ Schemas.

✅ DTOs.

✅ Tipos.

✅ Constantes.

✅ Enums.

✅ Modelos de dados.

✅ Contratos da API.

✅ Regras estruturais.

---

# O que NÃO pertence às Cifras

❌ Regras de negócio.

❌ Consultas ao banco.

❌ Processamento.

❌ Automações.

❌ Eventos.

❌ Logs.

❌ Chamadas HTTP.

❌ Manipulação de arquivos.

---

# 📜 Leis Gerais das Cifras

### I. As Cifras descrevem.

Jamais executam.

---

### II. Todo elemento do planeta pode consultar uma Cifra.

Mas nenhuma Cifra depende de um Habitante.

---

### III. As Cifras representam a linguagem oficial do planeta.

Se dois elementos precisam trocar informações, ambos devem seguir as mesmas Cifras.

---

### IV. Configurações pertencem às Cifras.

Valores fixos não devem ficar espalhados pelo planeta.

---

### V. Um contrato deve ser único.

Nunca existirão duas Cifras descrevendo a mesma informação de maneiras diferentes.

---

### VI. Alterar uma Cifra altera a linguagem do planeta.

Mudanças em contratos devem ser cuidadosas e compatíveis com os Portais e Habitantes que as utilizam.

---

### VII. As Cifras são imutáveis durante uma conversa.

Depois que um Portal aceita uma Cifra para interpretar uma mensagem, ela não deve mudar durante aquele processamento.

---

### VIII. Toda comunicação do planeta deve possuir uma Cifra.

Nada entra ou sai do planeta sem um contrato claramente definido.

---

# Sinais de Violação

As Cifras estão incorretas quando:

❌ Executam funções.

❌ Fazem chamadas HTTP.

❌ Consultam bancos.

❌ Criam objetos complexos.

❌ Escrevem arquivos.

❌ Possuem regras de negócio.

❌ Dependem de Habitantes.

---

# Sinais de Saúde

Boas Cifras:

✅ São simples.

✅ São reutilizáveis.

✅ São independentes.

✅ São previsíveis.

✅ São compartilhadas por todo o planeta.

✅ Tornam a comunicação consistente.

---

# Princípio Fundamental

> **As Cifras não dizem ao planeta o que fazer.**
>
> **Elas dizem ao planeta como compreender o que está sendo dito.**
>
> **Enquanto os Habitantes executam e os Portais comunicam, as Cifras garantem que todos falem a mesma linguagem.** 📜

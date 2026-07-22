# 📜 Constituição dos Acontecimentos

## **Lei Fundamental do Domínio de Eventos da Nave YZ**

**Documento:** Constituição dos Acontecimentos
**Domínio:** `acontecimentos/`
**Função:** Estabelecer as leis que governam o nascimento, existência, classificação, registro e preservação de todos os acontecimentos dentro da Nave YZ.

---

# Artigo I — Da Natureza dos Acontecimentos

Todo acontecimento é uma manifestação registrada de uma mudança relevante no estado da Nave YZ.

Um acontecimento não é apenas uma mensagem ou um log.

Um acontecimento é:

> "Uma prova histórica de que algo ocorreu dentro do universo da Nave YZ."

Todo acontecimento deve responder:

* **O que aconteceu?**
* **Quando aconteceu?**
* **Onde aconteceu?**
* **Quem provocou?**
* **Qual foi o impacto?**
* **Qual estado foi alterado?**

---

# Artigo II — Da Existência Oficial

Nenhum acontecimento poderá existir sem passar pelo processo de nascimento oficial.

O ciclo de vida obrigatório é:

```
Intenção
   ↓
Catálogo
   ↓
Fábrica
   ↓
Acontecimento
   ↓
Crônica
   ↓
Memória permanente
```

Nenhum habitante da Nave YZ poderá criar acontecimentos diretamente.

Proibido:

```python
Acontecimento(
    nome="qualquer_coisa",
    dados={}
)
```

Permitido:

```python
fabrica.criar(
    Evento.USUARIO_CADASTRADO,
    dados={}
)
```

---

# Artigo III — Do Catálogo Universal

Arquivo:

```
catalogo.py
```

O catálogo é a autoridade máxima sobre quais acontecimentos existem.

Ele define:

* Nome oficial.
* Código identificador.
* Categoria.
* Severidade padrão.
* Contrato de dados esperado.
* Descrição.

Exemplo:

```python
USUARIO_CRIADO = DefinicaoAcontecimento(
    codigo="USR_001",
    nome="USUARIO_CRIADO",
    categoria=Categoria.USUARIO,
    severidade=Severidade.INFO
)
```

## Lei:

> Nenhum acontecimento nasce sem possuir uma definição no catálogo.

---

# Artigo IV — Da Classificação dos Acontecimentos

Arquivo:

```
categorias.py
```

Todo acontecimento pertence obrigatoriamente a uma categoria.

Categorias representam os territórios onde os acontecimentos ocorrem.

Exemplo:

```
CATEGORIAS

├── SISTEMA
├── SEGURANCA
├── USUARIO
├── AUTOMACAO
├── NAVEGADOR
├── API
├── FLUXO
├── COMPUTADOR
└── NEGOCIO
```

A categoria permite:

* Organização histórica.
* Filtragem.
* Relatórios.
* Métricas.
* Observabilidade.

---

# Artigo V — Da Escala de Impacto

Arquivo:

```
severidades.py
```

Todo acontecimento possui um peso.

A severidade determina sua importância.

Hierarquia:

```
DEBUG
 |
INFO
 |
WARNING
 |
ERROR
 |
CRITICAL
```

Interpretação:

| Nível    | Significado             |
| -------- | ----------------------- |
| DEBUG    | Informação técnica      |
| INFO     | Operação normal         |
| WARNING  | Atenção necessária      |
| ERROR    | Falha recuperável       |
| CRITICAL | Ameaça ao funcionamento |

---

# Artigo VI — Do Nascimento Controlado

Arquivo:

```
fabrica.py
```

A fábrica é o órgão responsável pelo nascimento.

Ela deve garantir:

* Evento existente.
* Dados válidos.
* Origem conhecida.
* Contexto registrado.
* Identidade gerada.

Responsabilidades:

```python
FabricaAcontecimentos

+ validar()
+ criar()
+ enriquecer()
+ registrar()
```

Nenhuma entidade externa possui autoridade para gerar acontecimentos.

---

# Artigo VII — Da Entidade Acontecimento

Arquivo:

```
acontecimento.py
```

O acontecimento é a unidade fundamental da história.

Todo acontecimento deve possuir:

```python
Acontecimento:

id
codigo
nome
categoria
severidade
timestamp
origem
ator
contexto
payload
```

Exemplo:

```json
{
 "id":"evt-001",
 "nome":"FLUXO_EXECUTADO",
 "categoria":"AUTOMACAO",
 "severidade":"INFO",
 "origem":"HabitanteNavegador",
 "timestamp":"2026-07-22T15:00:00",
 "payload":{
    "fluxo":"login_cliente"
 }
}
```

---

# Artigo VIII — Da Origem dos Acontecimentos

Todo acontecimento deve declarar sua origem.

A origem pode ser:

```
Habitante
Observador
Portal
Sistema
Usuário
Processo
Integração
```

Um acontecimento sem origem é considerado inválido.

---

# Artigo IX — Da Memória Histórica

Arquivo:

```
cronica.py
```

A Crônica é responsável por preservar a história.

Ela pode utilizar:

* Arquivo JSON.
* Banco SQL.
* Banco NoSQL.
* Fila de mensagens.
* Sistema externo.

A Crônica nunca altera um acontecimento.

Ela apenas preserva.

Lei:

> "O passado da Nave YZ é imutável."

---

# Artigo X — Da Imutabilidade

Após registrado:

```
Acontecimento Criado
        ↓
       NÃO
        ↓
Alteração
```

Um acontecimento não é corrigido.

Caso algo novo aconteça:

Cria-se outro acontecimento.

Exemplo:

Errado:

```
USUARIO_CRIADO
alterado para
USUARIO_REMOVIDO
```

Correto:

```
USUARIO_CRIADO

↓

USUARIO_REMOVIDO
```

---

# Artigo XI — Da Observação

Todo acontecimento pode ser observado.

Observadores podem:

* Monitorar.
* Alertar.
* Criar métricas.
* Acionar respostas.

Exemplo:

```
Acontecimento:
PAGAMENTO_FALHOU

↓

Observador Financeiro

↓

Alerta enviado
```

---

# Artigo XII — Da Comunicação Entre Mundos

Acontecimentos podem atravessar os portais da Nave YZ.

Fluxo:

```
Habitante
   ↓
Acontecimento
   ↓
Crônica
   ↓
Portal
   ↓
Outro Sistema
```

Exemplo:

```
FLUXO_FINALIZADO

↓

Webhook

↓

Planeta Notify
```

---

# Artigo XIII — Da Evolução

O catálogo de acontecimentos é vivo.

Novos acontecimentos podem surgir quando:

* Uma nova capacidade nasce.
* Um novo habitante é criado.
* Um novo domínio aparece.

Porém:

Toda evolução deve preservar:

* Compatibilidade.
* Histórico.
* Clareza.
* Rastreamento.

---

# Juramento dos Acontecimentos

> "Eu não sou apenas uma mensagem.
> Eu sou uma marca deixada no tempo.
>
> Eu nasço sob uma lei.
> Vivo dentro de um contexto.
> Carrego uma origem.
> E minha existência será lembrada pela história da Nave YZ."

---

## Estrutura final:

```
acontecimentos/

├── __init__.py

├── catalogo.py
│   └── O que pode existir

├── categorias.py
│   └── Onde pertence

├── severidades.py
│   └── Qual impacto possui

├── fabrica.py
│   └── Como nasce

├── acontecimento.py
│   └── O que é

└── cronica.py
    └── Onde permanece
```

**Estado da Constituição: VIGENTE**
**Autoridade: Núcleo da Nave YZ**
**Versão: 1.0 — Lei Fundamental dos Eventos**

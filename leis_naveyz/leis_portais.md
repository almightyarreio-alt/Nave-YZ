# 📜 Leis dos Portais

> Os Portais são os pontos de comunicação do planeta.
>
> Todo visitante, habitante de outro planeta ou sistema externo deve atravessar um Portal para interagir com o planeta.
>
> Um Portal nunca realiza o trabalho do planeta. Ele apenas recebe, organiza e encaminha as solicitações.

---

# 🚪 Portais

## Representam

Os canais oficiais de comunicação do planeta.

Equivalente técnico:

```text
FastAPI
Flask
REST API
GraphQL
WebSocket
CLI
Webhook
RPC
```

No Arreiowork, todos são conhecidos como:

```text
Portais
```

---

## Propósito

Permitir que o planeta se comunique com o universo.

Os Portais recebem mensagens, verificam sua integridade e as encaminham aos Habitantes responsáveis.

---

## Responsabilidades

* Receber solicitações.
* Validar os dados recebidos.
* Encaminhar solicitações aos Habitantes.
* Receber respostas dos Habitantes.
* Traduzir respostas para o visitante.
* Controlar autenticação e autorização quando necessário.
* Registrar a comunicação nas Crônicas.

---

## Pode

* Receber requisições HTTP.
* Receber WebSockets.
* Receber Webhooks.
* Receber comandos internos.
* Validar formatos de entrada.
* Consultar as Cifras para contratos.
* Chamar Habitantes.
* Retornar respostas.
* Informar erros de comunicação.

---

## Não Pode

* Executar regras de negócio.
* Manipular Memórias diretamente.
* Monitorar eventos.
* Tomar decisões das Leis.
* Executar automações.
* Substituir Habitantes.

---

# Exemplo Narrativo

```text
Um visitante chega ao planeta.

O Portal o recebe.

Verifica se a mensagem é compreensível.

Encaminha a solicitação ao Habitante correto.

O Habitante realiza o trabalho.

O Portal recebe a resposta.

O Portal devolve a resposta ao visitante.
```

---

# O Ciclo da Comunicação

Toda comunicação segue o mesmo caminho.

```text
Visitante
     │
     ▼
🚪 Portal
     │
     ▼
📜 Cifras (validação)
     │
     ▼
👤 Habitante
     │
     ▼
🧠 Memória (quando necessário)
     │
     ▼
📖 Crônicas
     │
     ▼
🚪 Portal
     │
     ▼
Visitante
```

O Portal nunca pula etapas.

---

# Estrutura Recomendada

Cada Portal representa um assunto do planeta.

Exemplo:

```text
portais/
│
├── navegadores.py
├── fluxos.py
├── perfis.py
├── variaveis.py
├── notificacoes.py
└── saude.py
```

Nunca:

```text
api.py
rotas.py
tudo.py
```

Os Portais devem ser organizados por domínio, não por quantidade de código.

---

# Como um Portal deve agir

Um Portal ideal faz apenas quatro coisas:

1. Recebe a mensagem.
2. Verifica se ela está correta.
3. Entrega ao Habitante responsável.
4. Devolve a resposta.

Nada além disso.

---

# O que pertence ao Portal

✅ Receber parâmetros.

✅ Validar formatos.

✅ Verificar autenticação.

✅ Converter respostas.

✅ Definir códigos HTTP.

✅ Organizar documentação.

---

# O que NÃO pertence ao Portal

❌ Automatizar navegador.

❌ Consultar banco diretamente.

❌ Manipular arquivos.

❌ Fazer cálculos de negócio.

❌ Decidir regras.

❌ Monitorar diretórios.

❌ Escrever lógica complexa.

Se o Portal começa a "trabalhar", ele está assumindo a função de um Habitante.

---

# 📜 Leis Gerais dos Portais

### I. Todo visitante entra pelo Portal.

Nenhuma comunicação externa acontece fora dele.

---

### II. Todo Portal conhece apenas o caminho da comunicação.

Ele não conhece como o trabalho é realizado.

---

### III. Todo trabalho pertence aos Habitantes.

O Portal apenas encaminha.

---

### IV. Todo dado recebido deve ser validado.

Mensagens inválidas jamais atravessam um Portal.

---

### V. Todo Portal deve falar a linguagem do visitante.

Pode ser HTTP, WebSocket, CLI, Webhook ou qualquer outro meio.

Internamente, todos falam a linguagem do planeta.

---

### VI. Um Portal nunca conversa diretamente com outro Portal.

Se um Portal precisa de algo, ele solicita a um Habitante, que coordena a ação necessária.

---

### VII. Um Portal deve ser previsível.

A mesma mensagem deve produzir o mesmo comportamento esperado.

---

### VIII. Os Portais são a diplomacia do planeta.

Eles representam o planeta perante o universo.

Por isso, devem ser claros, documentados e seguros.

---

# Sinais de Violação

Um Portal está incorreto quando:

❌ Possui centenas de linhas de lógica.

❌ Consulta bancos diretamente.

❌ Manipula arquivos.

❌ Executa Playwright.

❌ Possui regras de negócio.

❌ Monitora eventos.

❌ Faz cálculos complexos.

---

# Sinais de Saúde

Um bom Portal:

✅ É pequeno.

✅ É fácil de ler.

✅ É bem documentado.

✅ Possui contratos claros.

✅ Encaminha rapidamente aos Habitantes.

✅ Responde de forma consistente.

---

# Princípio Fundamental

> **Os Portais não existem para resolver problemas.**
>
> **Eles existem para conectar o planeta ao universo.**
>
> **Quem transforma solicitações em ações são os Habitantes.** 🚪

# 📜 Leis das Identidades

> As Identidades representam quem pode existir dentro ou interagir com o planeta.
>
> Uma Identidade não executa tarefas, não toma decisões e não trabalha.
>
> Ela apenas representa uma existência reconhecida pelo planeta.
>
> Sem uma Identidade, o planeta não sabe quem está realizando uma ação.

---

# 🪪 Identidades

## Representam

As identidades utilizadas pelo planeta para reconhecer pessoas, navegadores, sistemas ou qualquer entidade que participe de suas atividades.

Equivalente técnico:

```text
Perfis

Credenciais

Usuários

Sessões

Contas

Tokens

Cookies

Perfis do Navegador

Certificados

Chaves de Acesso
```

No Arreiowork, todas pertencem às:

```text
Identidades
```

---

# Propósito

Representar quem é o agente de uma ação.

Toda missão realizada pelo planeta pode estar associada a uma ou mais Identidades.

---

# Responsabilidades

* Representar indivíduos.
* Armazenar credenciais.
* Representar sessões.
* Representar perfis.
* Organizar permissões.
* Identificar a origem das ações.

---

# Pode

* Armazenar credenciais.
* Armazenar cookies.
* Armazenar tokens.
* Armazenar certificados.
* Representar perfis persistentes.
* Representar sessões autenticadas.

---

# Não Pode

* Executar tarefas.
* Tomar decisões.
* Realizar autenticação por conta própria.
* Expor Portais.
* Executar automações.
* Registrar Crônicas espontaneamente.

---

# Exemplo Narrativo

```text
Um Habitante precisa acessar outro planeta.

Antes da viagem,
ele procura uma Identidade.

A Identidade entrega suas credenciais.

O Habitante realiza sua missão utilizando aquela identidade.

Ao terminar,
a Identidade permanece preservada para futuras missões.
```

---

# O Ciclo das Identidades

```text
👤 Habitante
      │
      ▼
🪪 Identidade
      │
      ▼
Credenciais disponíveis
      │
      ▼
Missão executada
```

A Identidade nunca realiza a missão.

Ela apenas representa quem a está realizando.

---

# Estrutura Recomendada

As Identidades devem ser organizadas conforme sua finalidade.

```text
identidades/
│
├── navegadores/
├── usuarios/
├── sistemas/
├── clientes/
├── sessoes/
├── certificados/
├── tokens/
└── credenciais/
```

---

# Tipos de Identidade

## Identidade de Navegação

Representa um navegador persistente.

Exemplos

```text
Perfil Chrome

Perfil Edge

Perfil Firefox

Playwright Profile
```

---

## Identidade de Usuário

Representa uma pessoa.

Exemplos

```text
Administrador

Operador

Convidado
```

---

## Identidade de Sistema

Representa outro planeta.

Exemplos

```text
API do WhatsApp

GitHub

Google Drive

Servidor FTP
```

---

## Identidade Temporária

Existe apenas durante uma missão.

Exemplos

```text
Sessão

Token temporário

Cookie temporário
```

---

# O que pertence às Identidades

✅ Perfis.

✅ Cookies.

✅ Tokens.

✅ Credenciais.

✅ Certificados.

✅ Chaves.

✅ Sessões.

✅ Perfis persistentes.

---

# O que NÃO pertence às Identidades

❌ Regras de negócio.

❌ Processamento.

❌ Interface.

❌ APIs.

❌ Observadores.

❌ Logs.

❌ Banco de dados como responsabilidade.

❌ Automações.

---

# 📜 Leis Gerais das Identidades

### I. Toda Identidade representa alguém ou algo.

Nunca existe uma Identidade sem representar um agente real do universo.

---

### II. Identidades não trabalham.

Quem executa as missões são os Habitantes.

As Identidades apenas emprestam sua existência para que essas missões possam ocorrer.

---

### III. Uma Identidade pode participar de muitas missões.

Mas cada missão deve saber exatamente qual Identidade está utilizando.

---

### IV. As Identidades pertencem ao planeta.

Nenhum Habitante é dono de uma Identidade.

Ele apenas a utiliza durante sua missão.

---

### V. Credenciais fazem parte da Identidade.

Senhas, cookies, tokens, certificados e demais formas de autenticação devem permanecer associados à Identidade correspondente.

---

### VI. Uma Identidade pode evoluir.

Novas credenciais, permissões ou informações podem ser adicionadas sem alterar quem ela representa.

Sua essência permanece a mesma.

---

### VII. Identidades podem adormecer.

Uma sessão pode expirar.

Um perfil pode ser desativado.

Uma credencial pode ser revogada.

Mesmo assim, a Identidade continua existindo enquanto o planeta decidir preservá-la.

---

### VIII. Uma missão nunca deve depender de uma Identidade específica.

Se uma missão só funciona com uma única Identidade, o planeta torna-se frágil.

Habitantes devem conseguir trabalhar com qualquer Identidade compatível.

---

### IX. O planeta deve proteger suas Identidades.

Credenciais são patrimônio do planeta.

Nunca devem ser expostas em Crônicas, Portais ou na Civilização.

Toda informação sensível deve permanecer protegida e acessível apenas aos Habitantes autorizados.

---

### X. Toda ação importante pode ser atribuída a uma Identidade.

Isso permite compreender não apenas o que aconteceu, mas também quem realizou a ação, fortalecendo a rastreabilidade e a auditoria do planeta.

---

# Sinais de Violação

Uma Identidade está incorreta quando:

❌ Contém lógica de negócio.

❌ Executa automações.

❌ Faz chamadas HTTP.

❌ Conhece detalhes da Civilização.

❌ Decide permissões sozinha.

❌ Armazena informações que não representam um agente.

❌ Expõe credenciais para outros elementos do planeta.

---

# Sinais de Saúde

Uma boa Identidade:

✅ Representa claramente um agente.

✅ Possui credenciais organizadas.

✅ Pode ser reutilizada por diferentes Habitantes.

✅ É independente da tecnologia utilizada.

✅ É protegida adequadamente.

✅ Permite rastrear quem participou de cada missão.

---

# Princípio Fundamental

> **As Identidades não existem para agir.**
>
> **Elas existem para representar.**
>
> **Enquanto os Habitantes executam as missões, as Identidades emprestam sua existência, permitindo que o planeta saiba quem está interagindo com o universo e garantindo que cada ação possa ser realizada de forma segura, consistente e rastreável.** 🪪

# 📜 Leis da Civilização

A Civilização representa tudo aquilo que um visitante consegue ver, tocar ou utilizar em um planeta.

Ela nunca executa a lógica do planeta. Apenas apresenta informações e conversa com os Portais.

---

# 🏙️ Civilização

## Propósito

Representar visualmente o planeta para seus visitantes.

Toda interação entre um visitante e o planeta acontece através da Civilização.

---

## Responsabilidades

* Exibir informações.
* Receber ações do visitante.
* Organizar a experiência de uso.
* Solicitar informações aos Portais.
* Atualizar a interface conforme as respostas.

---

## Pode

* Utilizar Construções.
* Utilizar Distritos.
* Utilizar Praças.
* Utilizar Arquiteturas.
* Utilizar Recursos.
* Utilizar Sinalizações.
* Utilizar Decorações.
* Utilizar Costumes.

---

## Não Pode

* Executar regras de negócio.
* Acessar bancos diretamente.
* Alterar Memórias.
* Executar Habitantes.
* Tomar decisões que pertencem às Leis.

Toda comunicação acontece pelos Portais.

---

# 🏘️ Distritos

## Representam

As regiões da Civilização.

Cada Distrito possui um propósito específico.

Exemplos

```text
Painel

Perfis

Fluxos

Configurações

Variáveis

Relatórios
```

---

## Responsabilidades

Um Distrito organiza uma experiência completa.

Ele reúne Construções, Praças e Costumes.

---

## Pode

* Possuir várias Construções.
* Possuir várias Praças.
* Consumir Portais.
* Organizar a navegação.

---

## Não Pode

* Ser reutilizado em outro Distrito.
* Possuir lógica de negócio.
* Conhecer detalhes internos dos Habitantes.

---

## Quando criar um novo Distrito

Sempre que existir uma nova área funcional do planeta.

Nunca criar Distritos apenas por questões visuais.

---

# 🏛️ Construções

## Representam

Os edifícios da Civilização.

São componentes reutilizáveis.

---

## Exemplos

```text
Botão

Tabela

Modal

Card

Input

Sidebar

Navbar

Gráfico

Lista

Avatar
```

---

## Responsabilidades

Resolver apenas um pequeno problema visual.

---

## Pode

* Receber propriedades.
* Emitir eventos.
* Possuir pequenos Costumes.

---

## Não Pode

* Conhecer Portais.
* Possuir regras de negócio.
* Conhecer outros Distritos.

---

## Quando criar uma nova Construção

Sempre que algo puder ser reutilizado.

---

# 🌳 Praças

## Representam

Espaços compartilhados da Civilização.

São estruturas que unem diversas Construções.

---

## Exemplos

```text
Layout Principal

Layout Administrativo

Layout Público

Cabeçalho

Rodapé

Área Central
```

---

## Responsabilidades

Organizar a disposição da cidade.

---

## Pode

* Receber Distritos.
* Organizar Construções.

---

## Não Pode

* Executar lógica.
* Consumir Portais.

---

# 🏗️ Arquiteturas

## Representam

Os modelos de construção da Civilização.

Definem padrões.

---

## Exemplos

```text
Template Dashboard

Template Login

Template Configuração
```

---

## Responsabilidades

Padronizar construções.

---

## Pode

* Definir regiões.
* Definir estrutura visual.

---

## Não Pode

* Possuir dados.
* Executar lógica.

---

# 🪧 Sinalizações

## Representam

Toda comunicação visual da cidade.

---

## Exemplos

```text
Ícones

Alertas

Badges

Breadcrumbs

Toast

Tooltip

Mensagens

Status

Indicadores
```

---

## Responsabilidades

Informar o visitante.

---

## Pode

* Exibir estados.
* Exibir mensagens.
* Orientar navegação.

---

## Não Pode

* Alterar comportamento.
* Executar ações.

---

# 🎨 Decorações

## Representam

A identidade visual da Civilização.

---

## Exemplos

```text
Tailwind

CSS

Temas

Animações

Tipografia

Espaçamentos

Sombras

Cores
```

---

## Responsabilidades

Definir aparência.

---

## Pode

* Alterar aparência.
* Alterar animações.
* Alterar responsividade.

---

## Não Pode

* Alterar lógica.
* Alterar dados.

---

# 📜 Costumes

## Representam

Os comportamentos da Civilização.

Toda interação visual acontece através dos Costumes.

---

## Exemplos

```text
Abrir Modal

Fechar Modal

Trocar Aba

Ordenar Lista

Filtrar

Pesquisar

Animações

Eventos do Usuário
```

---

## Responsabilidades

Dar vida à Civilização.

Controlar apenas o comportamento da interface.

---

## Pode

* Consumir Portais.
* Atualizar Construções.
* Manipular estados locais.
* Reagir a eventos.

---

## Não Pode

* Implementar regras de negócio.
* Alterar Memória diretamente.
* Executar Habitantes.
* Ignorar as Leis do planeta.

---

## Quando criar um novo Costume

Sempre que surgir um novo comportamento da interface.

Nunca criar Costumes para resolver regras do planeta.

---

# 📦 Recursos

## Representam

Tudo aquilo que auxilia visualmente a Civilização.

---

## Exemplos

```text
Imagens

SVG

Ícones

Vídeos

Áudios

Fontes

JSON estáticos

Arquivos de idioma
```

---

## Responsabilidades

Fornecer materiais utilizados pela Civilização.

---

## Pode

Ser utilizado por qualquer elemento da Civilização.

---

## Não Pode

Executar lógica.

---

# 📜 Leis Gerais da Civilização

### I. A Civilização nunca toma decisões pelo planeta.

Ela apenas apresenta e encaminha solicitações.

---

### II. Todo pedido para o planeta deve atravessar um Portal.

Nunca acessar Habitantes diretamente.

---

### III. Construções devem ser reutilizáveis.

Se uma Construção depende exclusivamente de um Distrito, ela provavelmente pertence ao próprio Distrito.

---

### IV. Um Costume nunca implementa regras de negócio.

Se uma decisão depende das regras do planeta, ela pertence às Leis ou aos Habitantes.

---

### V. Decorações jamais alteram comportamento.

Aparência e comportamento são responsabilidades distintas.

---

### VI. Distritos representam funcionalidades, nunca apenas organização visual.

Cada Distrito deve corresponder a uma área de uso claramente identificável.

---

### VII. A Civilização existe para servir ao visitante.

Ela não conhece o funcionamento interno do planeta; conhece apenas os Portais pelos quais se comunica.

---

Esse formato tem uma vantagem importante: ele pode ser interpretado por qualquer desenvolvedor e também por qualquer IA. Em vez de explicar "como organizar um projeto React, Vue ou HTML", você está definindo **leis universais** da Civilização. A implementação pode mudar de tecnologia, mas as responsabilidades permanecem as mesmas. Isso torna a lore um contrato arquitetural, não apenas uma convenção de nomes.

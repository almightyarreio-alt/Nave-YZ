📜 Acontecimentos (O Domínio de Eventos / Logs)
Esta é a pasta principal dedicada a capturar tudo de notável que ocorre no sistema. O fluxo de vida de um evento é mapeado em subdiretórios específicos:

1. Vocabulário (catalogo.py)
O que é: O dicionário oficial do que é reconhecido pelo sistema.

Papel Técnico: É o Registro de Eventos (Event Registry/Schema). Como vimos no arquivo da fábrica, ele contém a DefinicaoAcontecimento. Impede que desenvolvedores criem eventos "inventados da cabeça", obrigando o uso de nomes e contratos pré-aprovados (ex: USUARIO_CADASTRADO, FALHA_PAGAMENTO).

2. Classificação (categorias.py)
O que é: A taxonomia dos acontecimentos.

Papel Técnico: Define o agrupamento lógico (ex: SEGURANCA, SISTEMA, NEGOCIOS). Ajuda muito na hora de filtrar relatórios ou direcionar métricas específicas.

3. Impacto (severidades.py)
O que é: O peso de cada acontecimento na balança do sistema.

Papel Técnico: É o Enum de Níveis (Log Levels) que analisamos antes (DEBUG, INFO, ERRO, etc.). Define a urgência de tratamento e quem deve ser notificado.

4. Nascimento (fabrica.py)
O que é: Onde os acontecimentos ganham vida de forma oficial e controlada.

Papel Técnico: O Factory Pattern. Como vimos, é responsável por instanciar os objetos, validar origens e garantir que todos os dados obrigatórios estejam presentes antes de liberar o evento para o resto do sistema.

5. Existência (acontecimento.py)
O que é: O acontecimento em si, vivendo no espaço e no tempo.

Papel Técnico: É a Entidade Principal (Entity/Model). A classe Acontecimento que guarda o estado real da ocorrência: a data/hora exata (timestamp), os dados do payload, o contexto da requisição e de onde ela veio.

6. História (cronica.py)
O que é: Onde os acontecimentos são eternizados.

Papel Técnico: O Repositório, Dispatcher ou Message Broker. É o código responsável por pegar a instância de Acontecimento criada e gravá-la no banco de dados, enviá-la para uma fila (como RabbitMQ ou Kafka), ou escrevê-la em um arquivo de log estruturado.
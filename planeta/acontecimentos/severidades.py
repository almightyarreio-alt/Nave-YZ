"""
🚨 Severidades dos Acontecimentos

Representam o impacto de um acontecimento para o funcionamento do
Planeta.

A severidade auxilia auditorias, monitoramento, observabilidade
e priorização de incidentes.

O enum `Severidade` define os **níveis oficiais de gravidade (ou prioridade)** para o registro de eventos, logs ou ocorrências dentro do sistema **ArreioWork**.

Como herda de `str` e `Enum` (Python), cada membro possui um valor textual correspondente (`"debug"`, `"info"`, etc.), facilitando a serialização, persistência em banco de dados e exibição em interfaces.

---

### Descrição e Quando Utilizar Cada Nível

* **`DEBUG`**
* **O que é:** Informações altamente detalhadas, geralmente de interesse apenas durante o desenvolvimento, testes ou investigação profunda de falhas.
* **Quando utilizar:** Para registrar variáveis, fluxo de execução interno, consultas SQL detalhadas ou estados de objetos que ajudem a rastrear o comportamento exato do código em ambiente de desenvolvimento.


* **`INFO`**
* **O que é:** Mensagens informativas que destacam o progresso normal, o andamento de rotinas ou eventos esperados do sistema.
* **Quando utilizar:** Para registrar marcos importantes, como "Job iniciado com sucesso", "Usuário X realizou login" ou "Conexão com a API externa estabelecida".


* **`AVISO`** (ou *Warning*)
* **O que é:** Um indicativo de que algo inesperado aconteceu, ou que uma situação potenzialmente problemática pode causar problemas no futuro (ex: depreciação de recursos), mas o sistema **ainda continua funcionando normalmente**.
* **Quando utilizar:** Quando uma operação é concluída, mas com ressalvas — por exemplo, quando um arquivo de configuração opcional não é encontrado e o sistema recorre ao padrão, ou quando o uso de memória atinge um limite de alerta.


* **`ERRO`**
* **O que é:** Uma falha mais grave que impediu a conclusão de uma operação específica ou de uma transação, embora o aplicativo como um todo continue rodando.
* **When utilizar:** Quando uma exceção não tratada ocorre em uma tarefa, uma requisição a um serviço essencial falha, ou um registro não pôde ser salvo no banco de dados devido a uma restrição.


* **`CRITICO`** (ou *Critical/Fatal*)
* **O que é:** O nível mais alto de severidade. Indica uma falha catastrófica que compromete a estabilidade geral da aplicação ou de um componente crítico, exigindo intervenção imediata.
* **Quando utilizar:** Quando ow sistema perde a conexão com o banco de dados principal, há uma pane completa em um microsserviço essencial, ou ocorre um erro que causa a queda (crash) do processo principal do ArreioWork.

"""

from enum import Enum


class Severidade(str, Enum):
    """
    Níveis oficiais de severidade do ArreioWork.
    """

    DEBUG = "debug"

    INFO = "info"

    AVISO = "aviso"

    ERRO = "erro"

    CRITICO = "critico"
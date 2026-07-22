
📜 Lei I — Todo planeta possui um propósito único
Um planeta nasce para resolver um domínio específico.
Exemplos:
•	Nave YZ → Automação de navegadores.
•	Window Eye → Observabilidade de diretórios.
•	Notify → Comunicação e notificações.
Um planeta pode crescer, mas nunca perder sua identidade.
________________________________________
📜 Lei II — Todo planeta possui uma superfície
A superfície é a porta de entrada da aplicação.
Ela inicializa o planeta, desperta seus habitantes e abre seus portais.
Exemplo:
superficie.py
________________________________________
📜 Lei III — Todo planeta se comunica apenas pelos Portais
Nenhum planeta invade diretamente outro.
Toda comunicação ocorre pelos Portais (APIs).
Portais
│
├── abrir_perfil
├── observar
├── registrar
└── notificar
Isso permite independência entre os mundos.
________________________________________
📜 Lei IV — Todo acontecimento deve poder virar uma Crônica
Se algo importante aconteceu...
...o planeta deve ser capaz de registrar.
As Crônicas são seu histórico.
Cronista

Evento
Descrição
Data
Origem
Nada relevante deve desaparecer sem deixar vestígios.
________________________________________
📜 Lei V — Todo planeta possui Habitantes
Habitantes executam ações.
Exemplo no Nave YZ:
•	Habitante Navegador
•	Habitante Perfil
•	Habitante Executor
No Window Eye:
•	Habitante Observador
•	Habitante Vigia
________________________________________
📜 Lei VI — Toda decisão é governada pelas Leis
A lógica nunca fica espalhada.
Ela pertence às Leis.
leis/

lei_perfis.py
lei_fluxos.py
lei_execucao.py
Assim os habitantes apenas executam.
________________________________________
📜 Lei VII — Toda memória pertence aos Livros
Habitantes não guardam conhecimento permanente.
Quem guarda são os Livros.
Podem ser:
•	JSON
•	SQLite
•	PostgreSQL
•	Redis
•	arquivos
Na lore, continuam sendo simplesmente Livros.
________________________________________
📜 Lei VIII — Todo planeta observa a si mesmo
Um planeta deve conhecer seu próprio estado.
Por exemplo:
•	erros
•	desempenho
•	eventos
•	consumo de memória
•	tempo de execução
A observabilidade é parte da existência.
________________________________________
📜 Lei IX — Nenhum habitante é eterno
Habitantes podem nascer e desaparecer.
O planeta permanece.
Isso facilita reinicializações, troca de implementações e escalabilidade.
________________________________________
📜 Lei X — O código é a verdade; a lore é sua linguagem
A lore organiza a arquitetura e facilita a compreensão, mas não substitui a implementação.
A documentação deve refletir o código, e o código deve materializar as leis do planeta.
________________________________________
Essas leis formam uma boa base para o ArreioWork. Elas criam uma arquitetura coerente onde cada planeta compartilha a mesma "física", independentemente da tecnologia usada. Um desenvolvedor que aprender essas dez leis conseguirá navegar por qualquer planeta da constelação sem precisar reaprender sua organização.


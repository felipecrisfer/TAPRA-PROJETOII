# TAPRA-PROJETOII

TAPRA-2026
Aplicação desenvolvida para a disciplina de TAPRA, utilizando a plataforma Azure Functions em conjunto com a linguagem Python.

Participantes
Robertha Rezende
Felipe Cristian Fernandes
Vinicius Arthur Quandt
Funções implementadas
O projeto é composto por três funções principais:

1. Função com gatilho de tempo
Essa função é executada automaticamente a cada minuto. A cada execução, uma mensagem é registrada no sistema de logs, permitindo acompanhar seu funcionamento.

2. Função com gatilho HTTP
Essa função recebe o parâmetro name por meio de uma requisição HTTP do tipo GET e utiliza o valor informado para gerar uma resposta personalizada.

Exemplo de requisição:

http://localhost:7071/api/http_trigger_Aula_1?name=Robertha
3. Função temporizada com requisição HTTP
Essa função é acionada automaticamente a cada minuto. Durante sua execução, ela realiza uma chamada HTTP para a função http_trigger_Aula_1 e, posteriormente, registra no log a resposta obtida.

Tecnologias utilizadas
Python
Azure Functions
Azure Functions Core Tools
Azurite
Requests
Finalidade
O projeto foi desenvolvido com o objetivo de praticar a criação e utilização de funções serverless, explorando diferentes tipos de gatilhos disponíveis no Azure Functions, além da comunicação entre funções por meio de requisições HTTP.

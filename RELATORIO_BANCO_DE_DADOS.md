# Relatório do Banco de Dados

## Projeto

AMEI, NOTA ZERO

## Objetivo

O objetivo do banco de dados foi registrar informações importantes sobre o funcionamento do sistema.

A ideia principal foi criar um banco que pudesse guardar logs, tempo de resposta, erros e dados sobre os arquivos enviados. Com isso, fica mais fácil analisar o sistema e pensar em melhorias futuras.

Esse banco não foi feito para guardar dados pessoais dos usuários, mas sim informações técnicas sobre o funcionamento da aplicação.

---

## Banco utilizado

Foi utilizado o SQLite.

Escolhemos o SQLite porque ele é simples de usar, não precisa de servidor e funciona bem para projetos pequenos ou acadêmicos.

O banco criado ficou salvo na pasta:
database/

O arquivo principal do banco é:
amei_nota_zero.db

## Arquivos criados
Dentro da pasta database, foram criados alguns arquivos para organizar o banco:

- schema.sql
- inicializar_banco.py
- monitoramento.py
- consultar_banco.py
- relatorio_monitoramento.py
- limpar_dados_teste.py

schema.sql
Esse arquivo contém a estrutura das tabelas do banco.

inicializar_banco.py
Esse arquivo foi usado para criar o banco de dados.

monitoramento.py
Esse arquivo tem as funções que salvam informações no banco, como logs, erros, uploads e tempo de resposta.

consultar_banco.py
Esse arquivo serve para consultar os dados que foram salvos no banco.

relatorio_monitoramento.py
Esse arquivo mostra um resumo das informações registradas no banco.

limpar_dados_teste.py
Esse arquivo foi usado para apagar dados de teste.

## Tabelas criadas
Foram criadas algumas tabelas no banco de dados.
As principais são:

- uploads
- logs_sistema
- metricas_performance
- erros_sistema
- analises

## Tabela uploads
Essa tabela salva informações sobre os arquivos enviados para o sistema.
Ela guarda:

- nome do arquivo
- tipo do arquivo
- tamanho do arquivo
- data do envio

Essa tabela ajuda a saber quais arquivos foram enviados e qual tipo de arquivo está sendo mais usado.

## Tabela logs_sistema
Essa tabela salva os logs do sistema.
Os logs são registros de coisas que aconteceram durante o uso da aplicação.

Exemplo:
Arquivo recebido
Arquivo carregado com sucesso

Isso ajuda a acompanhar o que o sistema está fazendo.

## Tabela metricas_performance
Essa tabela salva o tempo de resposta das funcionalidades.
No nosso caso, ela foi usada para medir o tempo de carregamento do arquivo enviado.
Com isso, é possível saber se uma parte do sistema está demorando muito para responder.


## Tabela erros_sistema
Essa tabela salva os erros que podem acontecer no sistema.
Ela guarda informações como:

- módulo onde aconteceu o erro
- tipo do erro
- mensagem do erro
- data do erro
Isso ajuda na hora de corrigir problemas no sistema.

## Tabela analises
Essa tabela foi criada pensando em uma possível melhoria futura do projeto.
Ela pode ser usada depois para guardar informações sobre análises feitas pelo sistema.

## Funcionalidade monitorada
A funcionalidade que foi monitorada foi o envio de arquivos.
Quando um arquivo é enviado no sistema, o banco registra:

- nome do arquivo
- tipo do arquivo
- tamanho do arquivo
- log de arquivo recebido
- log de arquivo carregado com sucesso
- tempo de carregamento
- possíveis erros

Essa parte foi integrada no arquivo:
funcionalidades/carregamento.py

RESULTADO OBTIDO
Depois dos testes, foi gerado um relatório com os dados registrados no banco.
O resultado foi:

===== RELATÓRIO DE MONITORAMENTO DO SISTEMA =====

Total de uploads registrados: 1

Uploads por tipo de arquivo:
- json: 1

Tempo médio por funcionalidade:
- Carregamento de arquivo: 63.08 ms em 2 execução(ões)

Erros por módulo:
- Nenhum erro registrado.

Logs por módulo:
- UPLOAD: 4 log(s)

Esse resultado mostra que o banco conseguiu salvar as informações do upload e também registrou o tempo de resposta da funcionalidade.

## Consultas criadas
Também foi criado um arquivo para gerar um resumo das informações do banco.
Com ele é possível ver:

- quantos uploads foram feitos
- quais tipos de arquivos foram enviados
- qual foi o tempo médio de carregamento
- se aconteceu algum erro
- quantos logs foram registrados

Importância do banco
Esse banco é importante porque ajuda a entender melhor o funcionamento do sistema.
Com ele, podemos verificar se alguma parte está lenta, se algum erro aconteceu ou se o upload dos arquivos está funcionando corretamente.
Essas informações podem ajudar o grupo a melhorar o projeto no futuro.

Conclusão
O banco de dados criado ajudou a registrar informações técnicas importantes do sistema.
Ele salva logs, tempo de resposta, erros e informações sobre uploads.
Com isso, o projeto passa a ter uma forma simples de monitoramento, que pode ajudar na manutenção e em melhorias futuras.
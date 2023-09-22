# Todo

## Comandos

| Funcionalidade                        |  Comando                            |  |
|---------------------------------------|-------------------------------------|--|
| Conectar à sala                       |  hi, meu nome eh <nome_do_usuario>  | OK |
| Sair da sala                          |  bye                                | OK |
| Exibir lista de usuários do chat      |  list                               | OK |
| Exibir lista de amigos                |  mylist                             | OK |
| Adicionar usuário à lista de amigos   |  addtomylist <nome_do_usuario>      | OK |
| Remover usuário da lista de amigos    |  rmvfrommylist <nome_do_usuario>    | OK |
| Banir usuário da sala                 |  ban <nome_do_usuario>              |  |

## Outros

1. OK - Formato da mensagem:
   1. OK <IP>:<PORTA>/~<nome_usuario>: <mensagem> <hora-data>
2. OK - Mensagem de alerta quando um usuário se conecta
   1. OK <nome_usuario> entrou na sala
3. OK - Dois usuarios nao podem se conectar com o mesmo nome
4. OK - Usuarios amigos ganham uma tag \[amigo\]
5. Banir usuario:
   1. Servidor abre uma contagem
   2. Caso atinga mais da metade de usuarios conectados, usuario e banido
   3. Todos recebem uma mensagem: <nome_usuario> ban x/y
      1. x é o numero de votos
      2. y é o numero de votos necessarios (metade + 1)
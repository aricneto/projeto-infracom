# Primeira etapa: Envio de arquivos via UDP

## Inicializando o código

Inicialize o cliente

    python ./cliente.py

Em outra janela, inicialize o servidor

    python ./servidor.py

## Cliente

O cliente possui uma interface de comandos para facilitar a interação

### Envio de arquivos

1. Digite `arquivo` ou `arq` para enviar um arquivo ao servidor
2. Insira o caminho do arquivo relativo à pasta em que o cliente está presente
   1. Por exemplo, para enviar um dos arquivos de teste, digite `../test_files/cheems.png`
3. O arquivo será enviado ao servidor junto com um *header* que irá conter as seguintes informações
   1. Uma mensagem especificando o inicio do header
   2. O nome do arquivo e sua extensão
   3. O tamanho, em *bytes* do arquivo
   4. *(opcional)* Uma mensagem extra, se for necessário debugar algo
4. O arquivo será enviado em pacotes de tamanho `buffer_size`, definido em `common.py` como `1024 bytes`
5. O servidor irá receber, primeiramente, o *header*, que lhe informará a quantidade de bytes que ele estará esperando receber
6. A medida que o servidor recebe pacotes do cliente, ele irá os salvando em um arquivo com a mesma extensão
7. Quando a transferência é completada, o arquivo é enviado de volta ao cliente, repetindo as etapas a partir do passo 3
8. Os arquivos do recebidos no cliente e servidor podem ser encontrados em `files_client/` e `files_server/` (ou nos caminhos especificados em `CLIENT_DIR` e `SERVER_DIR`)


### Nome dos arquivos

Para explicitar o funcionamento do código, o arquivo, quando recebido pelo servidor, terá o codigo `s_` adicionado ao inicio do nome descrito no header.
   1. Quando este é recebido pelo cliente, ele terá o código `c_` adicionado ao inicio do nome descrito no header.
   2. Desta forma, sendo o arquivo original `nome.txt`, o servidor irá o salvar (e enviar ao cliente) como `s_nome.txt`, e o cliente irá o salvar como `c_s_nome.txt`

### Funções debug

    exit | ext  : fechar o cliente
    sdw         : desligar o servidor
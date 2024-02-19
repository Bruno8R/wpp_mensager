# Enviador de Mensagens WhatsApp

Este script  automatiza o processo de envio de mensagens personalizadas para vários contatos via WhatsApp usando a biblioteca `pywhatkit`. Ele foi projetado para simplificar o envio de mensagens personalizadas, lendo informações de contato de um arquivo CSV ou TXT e enviando mensagens modificadas com base em um modelo.

## Recursos

- **Compatibilidade com Arquivos de Contatos:** Suporta formatos CSV e TXT para armazenar informações de contato.
- **Customização de Mensagens:** Permite a personalização do conteúdo da mensagem substituindo ocorrências de 'nome' pelos nomes reais dos contatos.
- **Manuseio de Números de Telefone Nacionais e Internacionais:** Converte números de telefone para um formato padronizado, lidando com formatos de número de telefone internacionais e nacionais.
- **Opção de Abortar:** Fornece uma janela de 1 segundo para o usuário pressionar 'q' e abortar o processo de envio de mensagens para cada contato.

## Pré-requisitos

- Python 3.x
- Pacotes necessários: `pywhatkit`, `keyboard`

## Uso

- **contatos.csv (ou .txt):** Arquivo contendo informações de contato (nome, número de telefone).
- **mensagem.txt:** Arquivo contendo o modelo de mensagem, onde as ocorrências de 'nome' serão substituídas pelos nomes dos contatos.

## Exceções Personalizadas

- `ContatosFileError`: Levantada quando o arquivo de contatos não é encontrado.
- `MensagemFileError`: Levantada quando o arquivo de mensagem não é encontrado.
- `CommandLineArgumentsError`: Levantada quando um número incorreto de argumentos da linha de comando é fornecido.
- `ErrorProcessingFile`: Levantada durante erros no processamento de linhas e validação de números de telefone.

## Exemplo

```bash
python wpp.py contatos.csv mensagem.txt

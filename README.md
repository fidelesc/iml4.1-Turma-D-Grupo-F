# Construção de Mecanismos de Captação de Dados

## Introdução

Este projeto tem como objetivo criar um mecanismo de extração de dados que obtém informações da seção de Inteligência Artificial do Arxiv (“https://arxiv.org/list/cs.AI/recent”) e armazena os dados em um arquivo CSV. 

## Requisitos

Antes de executar o projeto, verifique se sua máquina possui os seguintes requisitos:

- **Docker** instalado e em execução.
- **Git Bash** no Windows, ou terminal no Linux/macOS.
- Permissões de execução para os scripts (“chmod +x”).

## Passos para Execução

### 1. Configurar o Ambiente

Primeiro, configure o ambiente do Docker executando o script `setup-docker.sh`:

#### Linux/macOS
Abra o terminal e execute os comandos:
```bash
chmod +x setup-docker.sh
./setup-docker.sh
```

#### Windows
No Windows, utilize o Git Bash:
```bash
chmod +x setup-docker.sh
./setup-docker.sh
```

O script:
- Cria a imagem Docker necessária.
- Configura o container para executar o código.

### 2. Executar o Código

Após configurar o ambiente, execute o script `run-code.sh` para iniciar o mecanismo de extração de dados:

#### Linux/macOS
```bash
chmod +x run-code.sh
./run-code.sh
```

#### Windows
No Git Bash:
```bash
chmod +x run-code.sh
./run-code.sh
```

O script executará o container Docker e gerará o arquivo `arxiv_papers.csv` dentro da pasta `data` no diretório raiz do projeto.

## Resultado Final

Ao final da execução, o arquivo `arxiv_papers.csv` conterá informações sobre os artigos extraídos do Arxiv, incluindo:
- Título.
- Autores.
- Link para o artigo.
- Informações adicionais (exemplo: número de páginas).

Certifique-se de verificar a pasta `data` para encontrar o arquivo gerado.

---

Se encontrar algum problema ou tiver dúvidas, entre em contato com o time de desenvolvimento.

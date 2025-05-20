# Conversor HTML para Markdown - Interface Web

Esta é uma interface web simples para o conversor HTML para Markdown, desenvolvida com Streamlit.

## Funcionalidades

- Interface amigável para usuários leigos
- Upload de arquivos HTML (até 50 MB)
- Prévia do resultado em Markdown
- Download do arquivo Markdown convertido

## Requisitos

- Python 3.6+
- Streamlit
- BeautifulSoup4
- html2text

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Execute o aplicativo com o comando:

```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente no seu navegador padrão.

## Como usar

1. Clique no botão "Escolha um arquivo HTML" para fazer upload do seu arquivo HTML
2. Após o upload, o arquivo será convertido automaticamente
3. Visualize a prévia do Markdown gerado
4. Clique em "Baixar arquivo Markdown" para salvar o resultado
# HTML para Markdown Converter

Este projeto fornece um conversor de HTML para Markdown com uma interface web.

## Funcionalidades

- Conversão de HTML para Markdown
- Interface web amigável
- Suporte para entrada direta de texto HTML
- Suporte para upload de arquivos HTML
- Formatação de cabeçalhos (h1 -> #, h2 -> ##, h3-h6 -> ###)
- Inserção de marcadores de página para elementos com classe `p-Pagina`
- Remoção de elementos de mídia (imagens, vídeos, áudios)
- Substituição de links por seu texto

## Instalação

1. Clone o repositório
2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Interface Web

Execute o aplicativo Streamlit:

```bash
# Método 1: Usando o script de execução
./run_converter.py

# Método 2: Usando o Streamlit diretamente
streamlit run simple_app.py
```

A interface oferece duas opções:
1. **Entrada de Texto**: Cole o código HTML diretamente
2. **Upload de Arquivo**: Faça upload de um arquivo HTML

Após a conversão, você pode visualizar o Markdown gerado e baixá-lo como arquivo.

### Como Biblioteca

Para usar o conversor em seu próprio código:

```python
from simple_app import convert_html_to_markdown

html = "<h1>Título</h1><p>Texto com <img src='imagem.jpg'> e <a href='link.html'>link</a>.</p>"
markdown = convert_html_to_markdown(html)
print(markdown)
```

### Exemplo

**HTML de entrada:**
```html
<h1>Título Principal</h1>
<p>Este é um exemplo de arquivo HTML para testar o conversor.</p>
<h2>Subtítulo</h2>
<p>Aqui temos um parágrafo com <a href="https://exemplo.com">link</a>.</p>
<span class="p-Pagina">42</span>
```

**Markdown de saída:**
```markdown
# Título Principal

Este é um exemplo de arquivo HTML para testar o conversor.

## Subtítulo

Aqui temos um parágrafo com link.

<!-- Página 42 -->42
```

Veja exemplos completos na pasta `examples/`.

## Publicação no GitHub

Para publicar este projeto no GitHub:

```bash
# Execute o script de configuração do Git
./setup_github.py
```

Siga as instruções exibidas pelo script para completar a publicação.

## Licença

Este projeto está licenciado sob a licença MIT.
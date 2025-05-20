#!/usr/bin/env python3
"""
HTML to Markdown Converter
Este script converte HTML para o formato Markdown com as seguintes regras:

Cabeçalhos:
- <h1> -> #
- <h2> -> ##
- <h3> até <h6> -> ###

Mídia e Links:
- Remove todas as tags <img>, <video> e <audio>
- Remove links <a> mantendo apenas o texto

Delimitação de Páginas:
- Insere comentários <!-- Página X --> para elementos com class="p-Pagina"
- Usa o conteúdo do elemento como número da página (ex: "12 e 13")
- Remove os elementos <span> após inserir os comentários
"""

import re
import sys
import os

def mark_page_breaks(html_content):
    """
    Detecta elementos com a classe p-Pagina e insere marcadores de página.
    Extrai o número da página do conteúdo do elemento quando disponível.
    
    Args:
        html_content (str): Conteúdo HTML a ser processado
        
    Returns:
        str: Conteúdo com marcadores de página inseridos
    """
    # Encontra todos os elementos com a classe p-Pagina junto com seu conteúdo
    pattern = r'(<[^>]*class=["\'](?:[^"\']*\s)?p-Pagina(?:\s[^"\']*)?["\'][^>]*>)(.*?)(</\w+>)'
    
    # Função para substituir cada ocorrência
    def page_marker(match):
        opening_tag = match.group(1)
        content = match.group(2).strip()
        closing_tag = match.group(3)
        
        # Usa o conteúdo do elemento como número da página
        return f'<!-- Página {content} -->\n{opening_tag}{content}{closing_tag}'
    
    # Substitui todas as ocorrências
    html_content = re.sub(pattern, page_marker, html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content

def remove_media_and_links(html_content):
    """
    Remove tags de mídia (<img>, <video>, <audio>) e links (<a>) do conteúdo HTML.
    
    Args:
        html_content (str): Conteúdo HTML a ser processado
        
    Returns:
        str: Conteúdo sem as tags de mídia e links
    """
    # Remover tags <img> completamente
    html_content = re.sub(r'<img[^>]*>', '', html_content, flags=re.IGNORECASE)
    
    # Remover tags <video> e seu conteúdo
    html_content = re.sub(r'<video[^>]*>.*?</video>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remover tags <audio> e seu conteúdo
    html_content = re.sub(r'<audio[^>]*>.*?</audio>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Substituir tags <a> por seu conteúdo (mantendo o texto do link)
    html_content = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content

def convert_headers(html_content):
    """
    Converte cabeçalhos HTML para formato Markdown.
    
    Args:
        html_content (str): Conteúdo HTML a ser convertido
        
    Returns:
        str: Conteúdo com cabeçalhos convertidos para Markdown
    """
    # Converter <h1> para # (com espaço após #)
    html_content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Converter <h2> para ## (com espaço após ##)
    html_content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Converter <h3>, <h4>, <h5>, <h6> para ### (com espaço após ###)
    for i in range(3, 7):
        html_content = re.sub(r'<h' + str(i) + r'[^>]*>(.*?)</h' + str(i) + r'>', r'### \1', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content

def remove_page_number_spans(html_content):
    """
    Remove os elementos <span> que contêm a classe p-Pagina após inserir os marcadores.
    
    Args:
        html_content (str): Conteúdo HTML com marcadores de página
        
    Returns:
        str: Conteúdo sem os elementos <span> de número de página
    """
    # Remove os spans com classe p-Pagina (mantém os comentários de página)
    pattern = r'<span[^>]*class=["\'](?:[^"\']*\s)?p-Pagina(?:\s[^"\']*)?["\'][^>]*>.*?</span>'
    html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content

def process_file(input_file, output_file=None):
    """
    Processa um arquivo HTML e converte para Markdown.
    
    Args:
        input_file (str): Caminho para o arquivo HTML de entrada
        output_file (str, optional): Caminho para o arquivo Markdown de saída.
            Se não for fornecido, será usado o mesmo nome do arquivo de entrada com extensão .md
    """
    # Definir arquivo de saída se não fornecido
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.md"
    
    try:
        # Ler o arquivo HTML
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inserir marcadores de página
        html_content = mark_page_breaks(html_content)
        
        # Remover mídia e links
        html_content = remove_media_and_links(html_content)
        
        # Remover os spans de número de página (mantendo os comentários)
        html_content = remove_page_number_spans(html_content)
        
        # Converter cabeçalhos
        md_content = convert_headers(html_content)
        
        # Escrever o resultado no arquivo de saída
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"Conversão concluída: {input_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"Erro ao processar o arquivo {input_file}: {str(e)}")
        return False

def main():
    """Função principal que processa os argumentos da linha de comando."""
    if len(sys.argv) < 2:
        print("Uso: python html_to_md_converter.py arquivo.html [arquivo_saida.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Erro: O arquivo {input_file} não existe.")
        sys.exit(1)
    
    success = process_file(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
HTML to Markdown Converter Module

Este módulo fornece uma função para converter HTML em Markdown,
aplicando transformações como limpeza, formatação de cabeçalhos
e marcação de páginas.
"""

import re
from bs4 import BeautifulSoup
import html2text

def convert(html: str) -> str:
    """
    Converte HTML para Markdown aplicando transformações necessárias.
    
    Args:
        html (str): Conteúdo HTML a ser convertido
        
    Returns:
        str: Conteúdo convertido para Markdown
    """
    # Passo 1: Parsear o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Passo 2: Aplicar transformações
    
    # 2.1: Inserir marcadores de página
    _mark_page_breaks(soup)
    
    # 2.2: Remover mídia (imagens, vídeos, áudios)
    _remove_media(soup)
    
    # 2.3: Substituir links por seu texto
    _process_links(soup)
    
    # 2.4: Processar cabeçalhos diretamente no HTML
    _process_headers(soup)
    
    # Passo 3: Converter para Markdown usando html2text
    h = html2text.HTML2Text()
    h.ignore_links = True  # Já processamos os links
    h.body_width = 0  # Não quebrar linhas
    h.ignore_images = True
    h.unicode_snob = True  # Preservar caracteres Unicode
    
    # Obter o HTML modificado e converter para Markdown
    modified_html = str(soup)
    markdown = h.handle(modified_html)
    
    # Passo 4: Limpeza final do Markdown
    markdown = _clean_markdown(markdown)
    
    return markdown

def _mark_page_breaks(soup):
    """
    Detecta elementos com a classe p-Pagina e insere marcadores de página.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
    """
    page_elements = soup.find_all(class_=lambda c: c and 'p-Pagina' in c.split())
    
    for element in page_elements:
        page_number = element.get_text().strip()
        # Inserir comentário de página antes do elemento
        comment = soup.new_string(f'<!-- Página {page_number} -->')
        element.insert_before(comment)

def _remove_media(soup):
    """
    Remove tags de mídia (img, video, audio) do documento.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
    """
    # Remover imagens
    for img in soup.find_all('img'):
        img.decompose()
    
    # Remover vídeos
    for video in soup.find_all('video'):
        video.decompose()
    
    # Remover áudios
    for audio in soup.find_all('audio'):
        audio.decompose()

def _process_links(soup):
    """
    Substitui links por seu texto.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
    """
    for link in soup.find_all('a'):
        link.replace_with(link.get_text())

def _process_headers(soup):
    """
    Processa cabeçalhos diretamente no HTML para garantir formatação correta no Markdown.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
    """
    # Substituir h1 por texto simples com prefixo Markdown
    for h1 in soup.find_all('h1'):
        text = h1.get_text().strip()
        new_tag = soup.new_tag('p')
        new_tag.string = f"# {text}"
        h1.replace_with(new_tag)
    
    # Substituir h2 por texto simples com prefixo Markdown
    for h2 in soup.find_all('h2'):
        text = h2.get_text().strip()
        new_tag = soup.new_tag('p')
        new_tag.string = f"## {text}"
        h2.replace_with(new_tag)
    
    # Substituir h3-h6 por texto simples com prefixo Markdown
    for i in range(3, 7):
        for h in soup.find_all(f'h{i}'):
            text = h.get_text().strip()
            new_tag = soup.new_tag('p')
            new_tag.string = f"### {text}"
            h.replace_with(new_tag)

def _clean_markdown(markdown):
    """
    Realiza limpeza final no Markdown gerado.
    
    Args:
        markdown (str): Conteúdo Markdown a ser limpo
        
    Returns:
        str: Conteúdo Markdown limpo
    """
    # Remover linhas em branco extras
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    # Remover spans de número de página (mantendo os comentários)
    markdown = re.sub(r'`?<span[^>]*class=["\'](?:[^"\']*\s)?p-Pagina(?:\s[^"\']*)?["\'][^>]*>.*?</span>`?', '', markdown)
    
    return markdown.strip()
"""
Conversor para Markdown

Este módulo contém funções para converter HTML parseado para Markdown.
"""

import re
import html2text
from bs4 import BeautifulSoup
from typing import Union

def convert_to_markdown(soup: Union[BeautifulSoup, str]) -> str:
    """
    Converte HTML parseado para Markdown.
    
    Args:
        soup (Union[BeautifulSoup, str]): Objeto BeautifulSoup ou string HTML
        
    Returns:
        str: Conteúdo convertido para Markdown
    """
    # Se for uma string, parsear como HTML
    if isinstance(soup, str):
        from htmltomd.parser import parse_html
        soup = parse_html(soup)
    
    # Configurar o conversor html2text
    h = html2text.HTML2Text()
    h.ignore_links = True  # Já processamos os links
    h.body_width = 0  # Não quebrar linhas
    h.ignore_images = True
    h.unicode_snob = True  # Preservar caracteres Unicode
    
    # Converter para Markdown
    markdown = h.handle(str(soup))
    
    # Limpar o Markdown gerado
    return clean_markdown(markdown)

def clean_markdown(markdown: str) -> str:
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
"""
Parser HTML

Este módulo contém funções para parsear HTML e aplicar transformações iniciais.
"""

from bs4 import BeautifulSoup
from typing import Union

def parse_html(html: str) -> BeautifulSoup:
    """
    Parseia o conteúdo HTML e retorna um objeto BeautifulSoup.
    
    Args:
        html (str): Conteúdo HTML a ser parseado
        
    Returns:
        BeautifulSoup: Objeto BeautifulSoup do documento HTML
    """
    return BeautifulSoup(html, 'html.parser')

def mark_page_breaks(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Detecta elementos com a classe p-Pagina e insere marcadores de página.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
        
    Returns:
        BeautifulSoup: Objeto BeautifulSoup modificado
    """
    page_elements = soup.find_all(class_=lambda c: c and 'p-Pagina' in c.split())
    
    for element in page_elements:
        page_number = element.get_text().strip()
        # Inserir comentário de página antes do elemento
        comment = soup.new_string(f'<!-- Página {page_number} -->')
        element.insert_before(comment)
    
    return soup

def remove_media(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Remove tags de mídia (img, video, audio) do documento.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
        
    Returns:
        BeautifulSoup: Objeto BeautifulSoup modificado
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
    
    return soup

def process_links(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Substitui links por seu texto.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
        
    Returns:
        BeautifulSoup: Objeto BeautifulSoup modificado
    """
    for link in soup.find_all('a'):
        link.replace_with(link.get_text())
    
    return soup

def process_headers(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Processa cabeçalhos diretamente no HTML para garantir formatação correta no Markdown.
    
    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup do documento HTML
        
    Returns:
        BeautifulSoup: Objeto BeautifulSoup modificado
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
    
    return soup
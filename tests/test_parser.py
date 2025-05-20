"""
Testes para o módulo parser
"""

import unittest
from htmltomd.parser import parse_html, mark_page_breaks, remove_media, process_links
from htmltomd.parser.html_parser import process_headers
from bs4 import BeautifulSoup

class TestParser(unittest.TestCase):
    """Testes para o módulo parser"""
    
    def test_parse_html(self):
        """Testa o parsing de HTML"""
        html = "<h1>Título</h1>"
        soup = parse_html(html)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.h1.string, "Título")
    
    def test_mark_page_breaks(self):
        """Testa a inserção de marcadores de página"""
        # Teste para elementos com class="p-Pagina"
        soup = parse_html('<span class="p-Pagina">12 e 13</span>')
        soup = mark_page_breaks(soup)
        
        # Verificar se o comentário foi inserido
        comments = list(soup.find_all(string=lambda text: isinstance(text, str) and '<!-- Página' in text))
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0], '<!-- Página 12 e 13 -->')
    
    def test_remove_media(self):
        """Testa a remoção de tags de mídia"""
        # Teste para remover imagens
        soup = parse_html('<p>Texto com <img src="imagem.jpg" alt="Imagem"> imagem.</p>')
        soup = remove_media(soup)
        self.assertIsNone(soup.find('img'))
        self.assertEqual(soup.p.get_text(), "Texto com  imagem.")
        
        # Teste para remover vídeos
        soup = parse_html('<p>Texto com <video controls><source src="video.mp4">Texto alternativo</video> vídeo.</p>')
        soup = remove_media(soup)
        self.assertIsNone(soup.find('video'))
        self.assertEqual(soup.p.get_text(), "Texto com  vídeo.")
    
    def test_process_links(self):
        """Testa o processamento de links"""
        # Teste para manter texto de links
        soup = parse_html('<p>Visite nosso <a href="https://exemplo.com">site</a> para mais informações.</p>')
        soup = process_links(soup)
        self.assertIsNone(soup.find('a'))
        self.assertEqual(soup.p.get_text(), "Visite nosso site para mais informações.")
    
    def test_process_headers(self):
        """Testa o processamento de cabeçalhos"""
        # Teste para h1
        soup = parse_html("<h1>Título Principal</h1>")
        soup = process_headers(soup)
        self.assertIsNone(soup.find('h1'))
        self.assertEqual(soup.p.string, "# Título Principal")
        
        # Teste para h2
        soup = parse_html("<h2>Subtítulo</h2>")
        soup = process_headers(soup)
        self.assertIsNone(soup.find('h2'))
        self.assertEqual(soup.p.string, "## Subtítulo")
        
        # Teste para h3
        soup = parse_html("<h3>Seção</h3>")
        soup = process_headers(soup)
        self.assertIsNone(soup.find('h3'))
        self.assertEqual(soup.p.string, "### Seção")

if __name__ == "__main__":
    unittest.main()
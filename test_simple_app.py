#!/usr/bin/env python3
"""
Testes para o conversor HTML para Markdown simplificado
"""

import unittest
from simple_app import (
    parse_html, mark_page_breaks, remove_media, 
    process_links, process_headers, convert_to_markdown,
    convert_html_to_markdown
)

class TestSimpleApp(unittest.TestCase):
    """Testes para o conversor HTML para Markdown simplificado"""
    
    def test_parse_html(self):
        """Testa o parsing de HTML"""
        html = "<h1>Título</h1>"
        soup = parse_html(html)
        self.assertEqual(soup.h1.string, "Título")
    
    def test_mark_page_breaks(self):
        """Testa a inserção de marcadores de página"""
        soup = parse_html('<span class="p-Pagina">42</span>')
        soup = mark_page_breaks(soup)
        comments = list(soup.find_all(string=lambda text: isinstance(text, str) and '<!-- Página' in text))
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0], '<!-- Página 42 -->')
    
    def test_remove_media(self):
        """Testa a remoção de tags de mídia"""
        soup = parse_html('<p>Texto com <img src="imagem.jpg"> imagem.</p>')
        soup = remove_media(soup)
        self.assertIsNone(soup.find('img'))
    
    def test_process_links(self):
        """Testa o processamento de links"""
        soup = parse_html('<p>Texto com <a href="link.html">link</a>.</p>')
        soup = process_links(soup)
        self.assertIsNone(soup.find('a'))
        self.assertEqual(soup.p.get_text(), "Texto com link.")
    
    def test_process_headers(self):
        """Testa o processamento de cabeçalhos"""
        soup = parse_html("<h1>Título</h1>")
        soup = process_headers(soup)
        self.assertIsNone(soup.find('h1'))
        self.assertEqual(soup.p.string, "# Título")
    
    def test_convert_to_markdown(self):
        """Testa a conversão para Markdown"""
        soup = parse_html("<p>Texto simples</p>")
        markdown = convert_to_markdown(soup)
        self.assertEqual(markdown, "Texto simples")
    
    def test_convert_html_to_markdown(self):
        """Testa a função principal de conversão"""
        html = """
        <h1>Título</h1>
        <p>Texto com <img src="imagem.jpg"> e <a href="link.html">link</a>.</p>
        <span class="p-Pagina">42</span>
        """
        markdown = convert_html_to_markdown(html)
        self.assertIn("# Título", markdown)
        self.assertIn("Texto com e link.", markdown)  # Corrigido: espaço duplo removido
        self.assertIn("<!-- Página 42 -->", markdown)
        self.assertNotIn("<img", markdown)
        self.assertNotIn("<a href", markdown)

if __name__ == "__main__":
    unittest.main()
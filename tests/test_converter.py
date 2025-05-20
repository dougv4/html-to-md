"""
Testes para o módulo converter
"""

import unittest
from htmltomd.parser import parse_html
from htmltomd.converter import convert_to_markdown, clean_markdown

class TestConverter(unittest.TestCase):
    """Testes para o módulo converter"""
    
    def test_convert_to_markdown(self):
        """Testa a conversão de HTML para Markdown"""
        # Teste com string HTML
        html = "<p>Texto simples</p>"
        markdown = convert_to_markdown(html)
        self.assertEqual(markdown, "Texto simples")
        
        # Teste com objeto BeautifulSoup
        soup = parse_html("<p>Texto com BeautifulSoup</p>")
        markdown = convert_to_markdown(soup)
        self.assertEqual(markdown, "Texto com BeautifulSoup")
    
    def test_clean_markdown(self):
        """Testa a limpeza do Markdown"""
        # Teste para remover linhas em branco extras
        markdown = "Linha 1\n\n\n\nLinha 2"
        cleaned = clean_markdown(markdown)
        self.assertEqual(cleaned, "Linha 1\n\nLinha 2")
        
        # Teste para remover spans de número de página
        markdown = "Texto\n<span class=\"p-Pagina\">42</span>\nMais texto"
        cleaned = clean_markdown(markdown)
        self.assertEqual(cleaned, "Texto\n\nMais texto")
    
    def test_combined_conversion(self):
        """Testa a conversão completa com todas as transformações"""
        html = """
        <h1>Título Principal</h1>
        <p>Texto com <img src="imagem.jpg"> e <a href="link.html">link</a>.</p>
        <span class="p-Pagina">42</span>
        <h2>Subtítulo</h2>
        <video controls><source src="video.mp4"></video>
        <p>Mais <a href="outro.html">outro link</a> aqui.</p>
        <h3>Seção</h3>
        """
        
        # Parsear o HTML
        soup = parse_html(html)
        
        # Aplicar transformações (simulando o fluxo completo)
        from htmltomd.parser.html_parser import mark_page_breaks, remove_media, process_links, process_headers
        
        soup = mark_page_breaks(soup)
        soup = remove_media(soup)
        soup = process_links(soup)
        soup = process_headers(soup)
        
        # Converter para Markdown
        markdown = convert_to_markdown(soup)
        
        # Verificar se contém os elementos esperados
        self.assertIn('# Título Principal', markdown)
        self.assertIn('## Subtítulo', markdown)
        self.assertIn('### Seção', markdown)
        self.assertIn('<!-- Página 42 -->', markdown)
        self.assertIn('Texto com e link.', markdown)
        self.assertIn('Mais outro link aqui.', markdown)
        
        # Verificar se não contém elementos removidos
        self.assertNotIn('<img', markdown)
        self.assertNotIn('<video', markdown)
        self.assertNotIn('<a href', markdown)

if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python3
"""
Testes para o módulo converter.py
"""

import unittest
from converter import convert

class TestConverter(unittest.TestCase):
    """Testes para a função convert do módulo converter.py"""
    
    def test_convert_headers(self):
        """Testa a conversão de cabeçalhos HTML para Markdown"""
        # Teste para h1
        html = "<h1>Título Principal</h1>"
        expected = "# Título Principal"
        self.assertEqual(convert(html).strip(), expected)
        
        # Teste para h2
        html = "<h2>Subtítulo</h2>"
        expected = "## Subtítulo"
        self.assertEqual(convert(html).strip(), expected)
        
        # Teste para h3 até h6
        for i in range(3, 7):
            html = f"<h{i}>Título nível {i}</h{i}>"
            expected = f"### Título nível {i}"
            self.assertEqual(convert(html).strip(), expected)
    
    def test_mark_page_breaks(self):
        """Testa a inserção de marcadores de página"""
        # Teste para elementos com class="p-Pagina"
        html = '<span class="p-Pagina">12 e 13</span>'
        result = convert(html)
        self.assertIn('<!-- Página 12 e 13 -->', result)
        
        # Teste para classe com outros atributos
        html = '<span class="_20-asap-bold numero_text p-Pagina">14 e 15</span>'
        result = convert(html)
        self.assertIn('<!-- Página 14 e 15 -->', result)
    
    def test_remove_media(self):
        """Testa a remoção de tags de mídia"""
        # Teste para remover imagens
        html = '<p>Texto com <img src="imagem.jpg" alt="Imagem"> imagem.</p>'
        expected = 'Texto com imagem.'
        self.assertEqual(convert(html).strip(), expected)
        
        # Teste para remover vídeos
        html = '<p>Texto com <video controls><source src="video.mp4">Texto alternativo</video> vídeo.</p>'
        expected = 'Texto com vídeo.'
        self.assertEqual(convert(html).strip(), expected)
        
        # Teste para remover áudio
        html = '<p>Texto com <audio controls><source src="audio.mp3">Texto alternativo</audio> áudio.</p>'
        expected = 'Texto com áudio.'
        self.assertEqual(convert(html).strip(), expected)
    
    def test_process_links(self):
        """Testa o processamento de links"""
        # Teste para manter texto de links
        html = '<p>Visite nosso <a href="https://exemplo.com">site</a> para mais informações.</p>'
        expected = 'Visite nosso site para mais informações.'
        self.assertEqual(convert(html).strip(), expected)
    
    def test_combined_transformations(self):
        """Testa todas as transformações combinadas"""
        html = """
        <h1>Título Principal</h1>
        <p>Texto com <img src="imagem.jpg"> e <a href="link.html">link</a>.</p>
        <span class="p-Pagina">42</span>
        <h2>Subtítulo</h2>
        <video controls><source src="video.mp4"></video>
        <p>Mais <a href="outro.html">outro link</a> aqui.</p>
        <h3>Seção</h3>
        """
        result = convert(html)
        
        # Verificar se contém os elementos esperados
        self.assertIn('# Título Principal', result)
        self.assertIn('## Subtítulo', result)
        self.assertIn('### Seção', result)
        self.assertIn('<!-- Página 42 -->', result)
        self.assertIn('Texto com e link.', result)
        self.assertIn('Mais outro link aqui.', result)
        
        # Verificar se não contém elementos removidos
        self.assertNotIn('<img', result)
        self.assertNotIn('<video', result)
        self.assertNotIn('<a href', result)

if __name__ == "__main__":
    unittest.main()
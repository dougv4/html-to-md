#!/usr/bin/env python3
"""
Testes para o conversor de HTML para Markdown
"""

import unittest
import tempfile
import os
from html_to_md_converter import convert_headers, remove_media_and_links, mark_page_breaks, remove_page_number_spans, process_file

class TestHTMLToMarkdownConverter(unittest.TestCase):
    """Testes para o conversor de HTML para Markdown"""
    
    def test_convert_headers(self):
        """Testa a conversão de cabeçalhos HTML para Markdown"""
        # Teste para h1
        html = "<h1>Título Principal</h1>"
        expected = "# Título Principal"
        self.assertEqual(convert_headers(html), expected)
        
        # Teste para h2
        html = "<h2>Subtítulo</h2>"
        expected = "## Subtítulo"
        self.assertEqual(convert_headers(html), expected)
        
        # Teste para h3 até h6
        for i in range(3, 7):
            html = f"<h{i}>Título nível {i}</h{i}>"
            expected = f"### Título nível {i}"
            self.assertEqual(convert_headers(html), expected)
        
        # Teste com atributos nos cabeçalhos
        html = '<h1 class="titulo">Título com classe</h1>'
        expected = "# Título com classe"
        self.assertEqual(convert_headers(html), expected)
        
        # Teste com múltiplos cabeçalhos
        html = """
        <h1>Título Principal</h1>
        <p>Algum texto</p>
        <h2>Subtítulo</h2>
        <h3>Seção</h3>
        <h4>Subseção</h4>
        """
        expected = """
        # Título Principal
        <p>Algum texto</p>
        ## Subtítulo
        ### Seção
        ### Subseção
        """
        self.assertEqual(convert_headers(html), expected)
    
    def test_mark_page_breaks(self):
        """Testa a inserção de marcadores de página"""
        # Teste para elementos com class="p-Pagina"
        html = '<span class="p-Pagina">12 e 13</span>'
        expected = '<!-- Página 12 e 13 -->\n<span class="p-Pagina">12 e 13</span>'
        self.assertEqual(mark_page_breaks(html), expected)
        
        # Teste para classe com outros atributos
        html = '<span class="_20-asap-bold numero_text p-Pagina">14 e 15</span>'
        expected = '<!-- Página 14 e 15 -->\n<span class="_20-asap-bold numero_text p-Pagina">14 e 15</span>'
        self.assertEqual(mark_page_breaks(html), expected)
        
    def test_remove_page_number_spans(self):
        """Testa a remoção de spans de número de página"""
        # Teste para remover spans com classe p-Pagina
        html = '<!-- Página 12 e 13 -->\n<span class="p-Pagina">12 e 13</span>'
        expected = '<!-- Página 12 e 13 -->\n'
        self.assertEqual(remove_page_number_spans(html), expected)
        
        # Teste para remover spans com múltiplas classes
        html = '<!-- Página 14 e 15 -->\n<span class="_20-asap-bold numero_text p-Pagina">14 e 15</span>'
        expected = '<!-- Página 14 e 15 -->\n'
        self.assertEqual(remove_page_number_spans(html), expected)
    
    def test_remove_media_and_links(self):
        """Testa a remoção de tags de mídia e links"""
        # Teste para remover imagens
        html = '<p>Texto com <img src="imagem.jpg" alt="Imagem"> imagem.</p>'
        expected = '<p>Texto com  imagem.</p>'
        self.assertEqual(remove_media_and_links(html), expected)
        
        # Teste para remover vídeos
        html = '<p>Texto com <video controls><source src="video.mp4">Texto alternativo</video> vídeo.</p>'
        expected = '<p>Texto com  vídeo.</p>'
        self.assertEqual(remove_media_and_links(html), expected)
        
        # Teste para remover áudio
        html = '<p>Texto com <audio controls><source src="audio.mp3">Texto alternativo</audio> áudio.</p>'
        expected = '<p>Texto com  áudio.</p>'
        self.assertEqual(remove_media_and_links(html), expected)
        
        # Teste para manter texto de links
        html = '<p>Visite nosso <a href="https://exemplo.com">site</a> para mais informações.</p>'
        expected = '<p>Visite nosso site para mais informações.</p>'
        self.assertEqual(remove_media_and_links(html), expected)
        
        # Teste combinado
        html = """
        <p>Texto com <img src="imagem.jpg"> e <a href="link.html">link</a>.</p>
        <video controls><source src="video.mp4"></video>
        <p>Mais <a href="outro.html">outro link</a> aqui.</p>
        """
        expected = """
        <p>Texto com  e link.</p>
        
        <p>Mais outro link aqui.</p>
        """
        self.assertEqual(remove_media_and_links(html), expected)
    
    def test_process_file(self):
        """Testa o processamento de arquivo"""
        # Criar arquivo temporário para teste
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
            temp_html.write(b"<h1>Teste</h1><img src='img.jpg'><h2>Subteste</h2><a href='link.html'>Link</a><h3>Detalhe</h3>")
            temp_html_path = temp_html.name
        
        # Nome do arquivo de saída
        temp_md_path = temp_html_path.replace('.html', '.md')
        
        try:
            # Processar o arquivo
            result = process_file(temp_html_path)
            self.assertTrue(result)
            
            # Verificar se o arquivo de saída foi criado
            self.assertTrue(os.path.exists(temp_md_path))
            
            # Verificar o conteúdo do arquivo de saída
            with open(temp_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertEqual(content, "# Teste## SubtesteLink### Detalhe")
        
        finally:
            # Limpar arquivos temporários
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
            if os.path.exists(temp_md_path):
                os.unlink(temp_md_path)

if __name__ == "__main__":
    unittest.main()
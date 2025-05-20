"""
Aplicativo Streamlit simplificado para converter HTML para Markdown
"""

import streamlit as st
from bs4 import BeautifulSoup
import html2text
import re
import base64
import tempfile
import os

def parse_html(html):
    """Parseia o HTML com BeautifulSoup"""
    return BeautifulSoup(html, 'html.parser')

def mark_page_breaks(soup):
    """Insere marcadores de página"""
    page_elements = soup.find_all(class_=lambda c: c and 'p-Pagina' in c.split())
    
    for element in page_elements:
        page_number = element.get_text().strip()
        comment = soup.new_string(f'<!-- Página {page_number} -->')
        element.insert_before(comment)
    
    return soup

def remove_media(soup):
    """Remove tags de mídia"""
    for tag in soup.find_all(['img', 'video', 'audio']):
        tag.decompose()
    return soup

def process_links(soup):
    """Substitui links por seu texto"""
    for link in soup.find_all('a'):
        link.replace_with(link.get_text())
    return soup

def process_headers(soup):
    """Processa cabeçalhos"""
    for h1 in soup.find_all('h1'):
        text = h1.get_text().strip()
        new_tag = soup.new_tag('p')
        new_tag.string = f"# {text}"
        h1.replace_with(new_tag)
    
    for h2 in soup.find_all('h2'):
        text = h2.get_text().strip()
        new_tag = soup.new_tag('p')
        new_tag.string = f"## {text}"
        h2.replace_with(new_tag)
    
    for i in range(3, 7):
        for h in soup.find_all(f'h{i}'):
            text = h.get_text().strip()
            new_tag = soup.new_tag('p')
            new_tag.string = f"### {text}"
            h.replace_with(new_tag)
    
    return soup

def convert_to_markdown(soup):
    """Converte para Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.body_width = 0
    h.ignore_images = True
    h.unicode_snob = True
    
    markdown = h.handle(str(soup))
    
    # Limpeza final
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    markdown = re.sub(r'`?<span[^>]*class=["\'](?:[^"\']*\s)?p-Pagina(?:\s[^"\']*)?["\'][^>]*>.*?</span>`?', '', markdown)
    
    return markdown.strip()

def convert_html_to_markdown(html_content):
    """Função principal de conversão"""
    soup = parse_html(html_content)
    soup = mark_page_breaks(soup)
    soup = remove_media(soup)
    soup = process_links(soup)
    soup = process_headers(soup)
    return convert_to_markdown(soup)

def main():
    """Função principal da aplicação Streamlit"""
    st.set_page_config(
        page_title="Conversor HTML para Markdown",
        page_icon="📄",
    )
    
    st.title("Conversor HTML para Markdown")
    
    # Inicializar estado da sessão se necessário
    if 'markdown' not in st.session_state:
        st.session_state.markdown = None
    if 'filename' not in st.session_state:
        st.session_state.filename = "convertido.md"
    
    # Criar abas para diferentes métodos de entrada
    tab1, tab2 = st.tabs(["Entrada de Texto", "Upload de Arquivo"])
    
    with tab1:
        st.write("Cole seu HTML abaixo para convertê-lo em Markdown.")
        html_content = st.text_area("HTML", height=200)
        
        if st.button("Converter Texto"):
            if html_content:
                try:
                    st.session_state.markdown = convert_html_to_markdown(html_content)
                    st.session_state.filename = "convertido.md"
                    st.success("Conversão concluída com sucesso!")
                except Exception as e:
                    st.error(f"Erro na conversão: {str(e)}")
            else:
                st.warning("Por favor, insira algum conteúdo HTML.")
    
    with tab2:
        st.write("Ou faça upload de um arquivo HTML.")
        
        # Usando um componente de arquivo personalizado
        uploaded_file = st.file_uploader("Escolha um arquivo HTML", type=["html", "htm"])
        
        if uploaded_file is not None:
            try:
                # Ler o conteúdo do arquivo
                html_content = uploaded_file.getvalue().decode("utf-8")
                
                if st.button("Converter Arquivo"):
                    st.session_state.markdown = convert_html_to_markdown(html_content)
                    st.session_state.filename = uploaded_file.name.replace(".html", ".md").replace(".htm", ".md")
                    st.success("Conversão concluída com sucesso!")
            except UnicodeDecodeError:
                st.error("Erro ao decodificar o arquivo. Verifique se o arquivo está em formato UTF-8.")
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {str(e)}")
    
    # Exibir resultado se disponível
    if st.session_state.markdown:
        st.subheader("Resultado em Markdown")
        st.text_area("", st.session_state.markdown, height=300)
        
        # Botão de download usando o componente nativo do Streamlit
        st.download_button(
            label="Baixar Markdown",
            data=st.session_state.markdown,
            file_name=st.session_state.filename,
            mime="text/markdown",
        )

if __name__ == "__main__":
    main()
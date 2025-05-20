"""
Interface web para converter HTML para Markdown
"""

import streamlit as st
import io
import traceback

def main():
    """Função principal da aplicação Streamlit"""
    
    # Configuração da página
    st.set_page_config(
        page_title="Conversor HTML para Markdown",
        page_icon="📄",
    )
    
    # Título da aplicação
    st.title("Conversor HTML para Markdown")
    
    # Descrição
    st.write("Converta HTML para Markdown facilmente.")
    
    # Entrada direta de HTML (evitando o upload de arquivo que está causando erro)
    html_content = st.text_area(
        "Cole o código HTML aqui:",
        height=200,
        help="Cole o código HTML que deseja converter para Markdown"
    )
    
    if html_content and st.button("Converter"):
        try:
            # Importar aqui para evitar problemas de importação circular
            from htmltomd.parser import parse_html
            from htmltomd.parser.html_parser import process_headers, mark_page_breaks, remove_media, process_links
            from htmltomd.converter import convert_to_markdown
            
            # Parsear o HTML
            soup = parse_html(html_content)
            
            # Aplicar transformações
            soup = mark_page_breaks(soup)
            soup = remove_media(soup)
            soup = process_links(soup)
            soup = process_headers(soup)
            
            # Converter para Markdown
            markdown_content = convert_to_markdown(soup)
            
            # Exibir prévia do Markdown
            with st.expander("Prévia do Markdown", expanded=True):
                st.text_area("", markdown_content, height=300)
            
            # Botão para download do arquivo Markdown
            st.download_button(
                label="Baixar arquivo Markdown",
                data=markdown_content,
                file_name="convertido.md",
                mime="text/markdown",
            )
                
        except Exception as e:
            st.error(f"Erro ao converter o HTML: {str(e)}")
            st.error(traceback.format_exc())

if __name__ == "__main__":
    # Quando executado diretamente, não como módulo
    import os
    import sys
    
    # Adicionar o diretório pai ao path para importações relativas funcionarem
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    main()
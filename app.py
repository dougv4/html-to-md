#!/usr/bin/env python3
"""
Interface web para converter HTML para Markdown
"""

import streamlit as st
import io
from converter import convert

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
    st.write("Faça upload de um arquivo HTML para convertê-lo em Markdown.")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha um arquivo HTML", 
        type=["html", "htm"],
        accept_multiple_files=False,
        help="Tamanho máximo: 50 MB"
    )
    
    if uploaded_file is not None:
        # Verificar tamanho do arquivo (limite de 50 MB)
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Tamanho em MB
        
        if file_size > 50:
            st.error("O arquivo é muito grande. O tamanho máximo permitido é 50 MB.")
        else:
            # Ler o conteúdo do arquivo
            html_content = uploaded_file.getvalue().decode("utf-8")
            
            # Converter HTML para Markdown
            try:
                markdown_content = convert(html_content)
                
                # Exibir prévia do Markdown
                with st.expander("Prévia do Markdown", expanded=True):
                    st.text_area("", markdown_content, height=300)
                
                # Botão para download do arquivo Markdown
                st.download_button(
                    label="Baixar arquivo Markdown",
                    data=markdown_content,
                    file_name=uploaded_file.name.replace(".html", ".md").replace(".htm", ".md"),
                    mime="text/markdown",
                )
                
            except Exception as e:
                st.error(f"Erro ao converter o arquivo: {str(e)}")

if __name__ == "__main__":
    main()
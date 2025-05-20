"""
Ponto de entrada para execução do pacote como módulo
"""

import streamlit.web.cli as stcli
import sys
import os

def main():
    """Executa o aplicativo Streamlit diretamente"""
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           "ui", "app.py")
    sys.argv = ["streamlit", "run", app_path]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
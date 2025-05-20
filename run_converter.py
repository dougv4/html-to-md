#!/usr/bin/env python3
"""
Script para executar o conversor HTML para Markdown
"""

import subprocess
import os
import sys

def main():
    """Executa o aplicativo Streamlit"""
    # Obter o caminho do aplicativo
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           "simple_app.py")
    
    # Verificar se o arquivo existe
    if not os.path.exists(app_path):
        print(f"Erro: O arquivo {app_path} não foi encontrado.")
        sys.exit(1)
    
    # Executar o comando streamlit run
    cmd = ["streamlit", "run", app_path]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nAplicativo encerrado pelo usuário.")
    except Exception as e:
        print(f"Erro ao executar o aplicativo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
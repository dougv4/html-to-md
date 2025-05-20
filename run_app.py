#!/usr/bin/env python3
"""
Script para executar o aplicativo Streamlit
"""

import subprocess
import os
import sys

def main():
    """Executa o aplicativo Streamlit"""
    # Obter o caminho do aplicativo
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                           "htmltomd", "ui", "app.py")
    
    # Executar o comando streamlit run
    cmd = ["streamlit", "run", app_path]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
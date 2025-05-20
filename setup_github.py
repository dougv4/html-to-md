#!/usr/bin/env python3
"""
Script para configurar o repositório Git e preparar para publicação no GitHub
"""

import os
import subprocess
import sys

def run_command(command):
    """Executa um comando e retorna o resultado"""
    print(f"Executando: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro: {result.stderr}")
        return False
    print(f"Saída: {result.stdout}")
    return True

def setup_git():
    """Configura o repositório Git"""
    # Verificar se o diretório .git já existe
    if os.path.exists(".git"):
        print("Repositório Git já inicializado.")
    else:
        # Inicializar o repositório
        if not run_command("git init"):
            return False
    
    # Adicionar arquivos
    if not run_command("git add ."):
        return False
    
    # Verificar status
    run_command("git status")
    
    # Instruções para o usuário
    print("\n=== Próximos passos ===")
    print("1. Configure seu nome de usuário e email do Git (se ainda não configurou):")
    print("   git config --global user.name \"Seu Nome\"")
    print("   git config --global user.email \"seu.email@exemplo.com\"")
    print("\n2. Faça o commit inicial:")
    print("   git commit -m \"Versão inicial do conversor HTML para Markdown\"")
    print("\n3. Crie um repositório no GitHub e adicione o remoto:")
    print("   git remote add origin https://github.com/seu-usuario/html-to-markdown.git")
    print("\n4. Envie para o GitHub:")
    print("   git push -u origin main")
    
    return True

if __name__ == "__main__":
    # Mudar para o diretório do projeto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Configurar o repositório Git
    if setup_git():
        print("\nConfiguração concluída com sucesso!")
    else:
        print("\nErro na configuração do repositório Git.")
        sys.exit(1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Upload Automático para GitHub
Faz upload do executável e atualiza o arquivo versao.json
"""

import os
import json
import subprocess
import sys
from pathlib import Path

# Configurações
REPOSITORIO = "atualiza-o-mec-nica"
USUARIO_GITHUB = "BarbaNegraBR"
ARQUIVO_VERSAO = "versao.json"

# Verificar qual executável existe
if os.path.exists("dist/Calculadora_Reparos_Palomino.exe"):
    ARQUIVO_EXE = "dist/Calculadora_Reparos_Palomino.exe"
    NOME_RELEASE = "Calculadora_Reparos_Palomino.exe"
elif os.path.exists("dist/Calculadora.exe"):
    ARQUIVO_EXE = "dist/Calculadora.exe"
    NOME_RELEASE = "Calculadora_Reparos_Palomino.exe"  # Nome na release
else:
    ARQUIVO_EXE = "dist/Calculadora_Reparos_Palomino.exe"
    NOME_RELEASE = "Calculadora_Reparos_Palomino.exe"

def verificar_git():
    """Verifica se git está instalado"""
    try:
        subprocess.run(["git", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git não está instalado ou não está no PATH")
        return False

def verificar_repositorio():
    """Verifica se estamos em um repositório git"""
    try:
        subprocess.run(["git", "status"], 
                      capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def inicializar_repositorio():
    """Inicializa o repositório git se não existir"""
    if not verificar_repositorio():
        print("📦 Inicializando repositório git...")
        subprocess.run(["git", "init"], check=True)
        
        # Criar .gitignore
        gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporários
*.tmp
*.log
atualizar.bat
"""
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore)
        
        print("✅ Repositório inicializado")
        return True
    return True

def configurar_remote():
    """Configura o remote do GitHub"""
    remote_url = f"https://github.com/{USUARIO_GITHUB}/{REPOSITORIO}.git"
    
    try:
        # Verificar se remote já existe
        result = subprocess.run(["git", "remote", "get-url", "origin"],
                              capture_output=True, text=True)
        if remote_url in result.stdout:
            return True
        
        # Adicionar remote
        subprocess.run(["git", "remote", "add", "origin", remote_url],
                      check=True, capture_output=True)
        print(f"✅ Remote configurado: {remote_url}")
        return True
    except subprocess.CalledProcessError:
        try:
            # Tentar atualizar remote existente
            subprocess.run(["git", "remote", "set-url", "origin", remote_url],
                          check=True, capture_output=True)
            print(f"✅ Remote atualizado: {remote_url}")
            return True
        except:
            print("⚠️  Não foi possível configurar o remote automaticamente")
            print(f"   Execute manualmente: git remote add origin {remote_url}")
            return False

def ler_versao():
    """Lê a versão atual do arquivo versao.json"""
    try:
        with open(ARQUIVO_VERSAO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("versao", "1.0.0")
    except:
        return "1.0.0"

def incrementar_versao(versao_atual):
    """Incrementa a versão (formato X.Y.Z)"""
    partes = versao_atual.split('.')
    try:
        major, minor, patch = int(partes[0]), int(partes[1]), int(partes[2])
        patch += 1
        return f"{major}.{minor}.{patch}"
    except:
        return "1.0.1"

def atualizar_versao_json(nova_versao, changelog=""):
    """Atualiza o arquivo versao.json"""
    from datetime import datetime
    
    dados = {
        "versao": nova_versao,
        "data": datetime.now().strftime("%Y-%m-%d"),
        "changelog": changelog or f"Atualização automática - versão {nova_versao}",
        "url_download": ""
    }
    
    with open(ARQUIVO_VERSAO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Versão atualizada para {nova_versao}")

def verificar_exe():
    """Verifica se o executável existe"""
    # Verificar ambos os possíveis nomes
    exe1 = "dist/Calculadora_Reparos_Palomino.exe"
    exe2 = "dist/Calculadora.exe"
    
    if os.path.exists(exe1):
        return True
    elif os.path.exists(exe2):
        return True
    else:
        print(f"❌ Executável não encontrado em dist/")
        print("   Execute primeiro: build_executavel.bat")
        return False

def fazer_commit_e_push():
    """Faz commit e push das alterações"""
    try:
        # Adicionar arquivos
        subprocess.run(["git", "add", ARQUIVO_VERSAO], check=True)
        subprocess.run(["git", "add", ".gitignore"], check=True, 
                      capture_output=True)
        
        # Commit
        versao = ler_versao()
        mensagem = f"Atualização versão {versao}"
        subprocess.run(["git", "commit", "-m", mensagem], 
                      check=True, capture_output=True)
        print(f"✅ Commit criado: {mensagem}")
        
        # Push
        print("📤 Fazendo push para GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "main"], 
                      check=True, capture_output=True)
        print("✅ Push concluído!")
        return True
        
    except subprocess.CalledProcessError as e:
        # Tentar com branch master
        try:
            subprocess.run(["git", "push", "-u", "origin", "master"], 
                          check=True, capture_output=True)
            print("✅ Push concluído!")
            return True
        except:
            print("⚠️  Erro ao fazer push")
            print("   Você pode precisar fazer push manualmente:")
            print("   git push -u origin main")
            return False

def criar_release():
    """Cria uma release no GitHub usando GitHub CLI ou instruções manuais"""
    versao = ler_versao()
    tag = f"v{versao}"
    
    # Verificar se gh CLI está instalado
    try:
        subprocess.run(["gh", "--version"], 
                      capture_output=True, check=True)
        
        print(f"🏷️  Criando release {tag}...")
        
        # Criar tag
        subprocess.run(["git", "tag", "-a", tag, "-m", f"Versão {versao}"],
                      check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", tag],
                      check=True, capture_output=True)
        
        # Determinar qual executável usar
        exe_para_upload = ARQUIVO_EXE
        if not os.path.exists(exe_para_upload):
            if os.path.exists("dist/Calculadora.exe"):
                exe_para_upload = "dist/Calculadora.exe"
        
        # Criar release
        subprocess.run([
            "gh", "release", "create", tag,
            exe_para_upload,
            "--title", f"Versão {versao}",
            "--notes", f"Release automática da versão {versao}"
        ], check=True)
        
        print(f"✅ Release {tag} criada com sucesso!")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⚠️  GitHub CLI não está instalado")
        print("   Para criar a release manualmente:")
        print(f"   1. Acesse: https://github.com/{USUARIO_GITHUB}/{REPOSITORIO}/releases/new")
        print(f"   2. Crie uma nova release com a tag: {tag}")
        print(f"   3. Faça upload do arquivo: {ARQUIVO_EXE}")
        print(f"   4. Nome do arquivo na release: {NOME_RELEASE}")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("🚀 Upload Automático para GitHub")
    print("=" * 50)
    
    # Verificações
    if not verificar_git():
        sys.exit(1)
    
    if not verificar_exe():
        sys.exit(1)
    
    # Inicializar repositório
    if not inicializar_repositorio():
        sys.exit(1)
    
    # Configurar remote
    configurar_remote()
    
    # Atualizar versão
    versao_atual = ler_versao()
    print(f"\n📋 Versão atual: {versao_atual}")
    
    resposta = input("Deseja incrementar a versão? (s/n): ").lower()
    if resposta == 's':
        nova_versao = incrementar_versao(versao_atual)
        changelog = input("Digite o changelog (ou Enter para padrão): ").strip()
        atualizar_versao_json(nova_versao, changelog)
    else:
        nova_versao = versao_atual
    
    # Commit e push
    print("\n📝 Fazendo commit e push...")
    fazer_commit_e_push()
    
    # Criar release
    print("\n📦 Criando release...")
    criar_release()
    
    print("\n" + "=" * 50)
    print("✅ Processo concluído!")
    print("=" * 50)
    print(f"\n🔗 Repositório: https://github.com/{USUARIO_GITHUB}/{REPOSITORIO}")

if __name__ == "__main__":
    main()


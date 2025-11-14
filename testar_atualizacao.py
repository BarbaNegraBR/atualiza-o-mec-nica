#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se a atualização está funcionando
"""

import requests
import json

def testar_atualizacao():
    print("=" * 60)
    print("TESTE DE ATUALIZAÇÃO")
    print("=" * 60)
    
    usuario = "BarbaNegraBR"
    repositorio = "atualiza-o-mec-nica"
    # Tentar diferentes branches
    branches = ["main", "master", "HEAD"]
    url_versao = None
    for branch in branches:
        test_url = f"https://raw.githubusercontent.com/{usuario}/{repositorio}/{branch}/versao.json"
        try:
            response = requests.head(test_url, timeout=5)
            if response.status_code == 200:
                url_versao = test_url
                print(f"   ✅ Branch encontrada: {branch}")
                break
        except:
            pass
    
    if not url_versao:
        url_versao = f"https://raw.githubusercontent.com/{usuario}/{repositorio}/main/versao.json"
    
    print(f"\n1. Verificando versão no GitHub...")
    print(f"   URL: {url_versao}")
    
    try:
        response = requests.get(url_versao, timeout=10)
        if response.status_code == 200:
            dados = json.loads(response.text)
            versao_github = dados.get('versao', 'N/A')
            changelog = dados.get('changelog', 'N/A')
            print(f"   ✅ Versão no GitHub: {versao_github}")
            print(f"   📝 Changelog: {changelog}")
        else:
            print(f"   ❌ Erro: Status {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Erro ao acessar: {e}")
        return
    
    print(f"\n2. Verificando releases no GitHub...")
    url_releases = f"https://api.github.com/repos/{usuario}/{repositorio}/releases"
    
    try:
        response = requests.get(url_releases, timeout=10)
        if response.status_code == 200:
            releases = response.json()
            if releases:
                print(f"   ✅ Encontradas {len(releases)} release(s):")
                for release in releases[:5]:  # Mostrar até 5
                    tag = release.get('tag_name', 'N/A')
                    nome = release.get('name', 'N/A')
                    assets = release.get('assets', [])
                    print(f"      - {tag}: {nome}")
                    if assets:
                        for asset in assets:
                            print(f"        📦 {asset.get('name', 'N/A')} ({asset.get('size', 0)} bytes)")
                    else:
                        print(f"        ⚠️  Sem arquivos anexados!")
            else:
                print(f"   ❌ Nenhuma release encontrada!")
                print(f"   ⚠️  Você precisa criar uma release no GitHub!")
        else:
            print(f"   ❌ Erro: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro ao verificar releases: {e}")
    
    print(f"\n3. Verificando URL de download...")
    versao_github = dados.get('versao', '1.0.2')
    url_download = f"https://github.com/{usuario}/{repositorio}/releases/download/v{versao_github}/Calculadora_Reparos_Palomino.exe"
    print(f"   URL esperada: {url_download}")
    
    try:
        response = requests.head(url_download, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            tamanho = response.headers.get('content-length', 'N/A')
            print(f"   ✅ Arquivo existe! Tamanho: {tamanho} bytes")
        elif response.status_code == 404:
            print(f"   ❌ Arquivo NÃO encontrado (404)")
            print(f"   ⚠️  Verifique se:")
            print(f"      - A release foi criada com a tag: v{versao_github}")
            print(f"      - O arquivo foi enviado na release")
            print(f"      - O nome do arquivo é: Calculadora_Reparos_Palomino.exe")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro ao verificar: {e}")
    
    print(f"\n4. Comparando versões...")
    versao_local = "1.0.2"  # Versão no atualizador.py
    print(f"   Versão local (no código): {versao_local}")
    print(f"   Versão no GitHub: {versao_github}")
    
    def comparar_versoes(v1, v2):
        try:
            partes1 = [int(x) for x in v1.split('.')]
            partes2 = [int(x) for x in v2.split('.')]
            return partes1 > partes2
        except:
            return False
    
    if comparar_versoes(versao_github, versao_local):
        print(f"   ✅ Há atualização disponível!")
    elif versao_github == versao_local:
        print(f"   ⚠️  Versões são iguais - não há atualização")
        print(f"   💡 Para testar, incremente a versão no versao.json")
    else:
        print(f"   ⚠️  Versão local é mais nova que a do GitHub")
    
    print("\n" + "=" * 60)
    print("RESUMO:")
    print("=" * 60)
    print(f"✅ Versão no GitHub: {versao_github}")
    print(f"✅ Versão local: {versao_local}")
    print(f"✅ Release existe: {'Sim' if releases else 'Não'}")
    print(f"✅ Arquivo disponível: {'Sim' if response.status_code == 200 else 'Não'}")
    print("=" * 60)

if __name__ == "__main__":
    testar_atualizacao()


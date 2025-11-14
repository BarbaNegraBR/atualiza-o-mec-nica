#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Atualização Automática
Verifica e baixa atualizações do GitHub
"""

import requests
import json
import os
import sys
import shutil
import subprocess
from pathlib import Path
from tkinter import messagebox

class AtualizadorApp:
    def __init__(self):
        # Configurações do repositório
        self.usuario_github = "BarbaNegraBR"
        self.repositorio = "atualiza-o-mec-nica"
        self.versao_atual = "1.0.4"  # Versão atual do app - ATUALIZE SEMPRE QUE MUDAR O versao.json (SEM o "v")
        
        # URLs
        self.url_versao = f"https://raw.githubusercontent.com/{self.usuario_github}/{self.repositorio}/master/versao.json"
        self.url_download_base = f"https://github.com/{self.usuario_github}/{self.repositorio}/releases/download"
        
    def verificar_atualizacao(self):
        """Verifica se há atualização disponível"""
        try:
            response = requests.get(self.url_versao, timeout=5)
            if response.status_code == 200:
                dados = response.json()
                versao_remota = dados.get('versao', '0.0.0')
                # Remover "v" se houver
                versao_remota = versao_remota.lstrip('v')
                
                if self.comparar_versoes(versao_remota, self.versao_atual):
                    return True, versao_remota, dados.get('changelog', ''), dados.get('url_download', '')
            return False, None, None, None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao verificar atualização: {e}")
            return False, None, None, None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False, None, None, None
    
    def verificar_atualizacao_completo(self):
        """Verifica atualização com informações detalhadas para debug"""
        try:
            # Verificar versão no GitHub
            response = requests.get(self.url_versao, timeout=10)
            if response.status_code != 200:
                return False, {
                    'erro': f'Erro ao acessar versao.json (Status {response.status_code})',
                    'detalhes': f'URL: {self.url_versao}'
                }
            
            dados = response.json()
            versao_remota = dados.get('versao', '0.0.0')
            versao_remota = versao_remota.lstrip('v')  # Remover "v" se houver
            
            # Verificar se há atualização
            tem_atualizacao = self.comparar_versoes(versao_remota, self.versao_atual)
            
            # Verificar se o arquivo existe na release
            arquivo_existe = False
            url_download = None
            
            if tem_atualizacao:
                # Tentar diferentes formatos de tag
                tags_possiveis = [
                    f"v{versao_remota}",
                    versao_remota,
                    f"V{versao_remota}"
                ]
                
                for tag in tags_possiveis:
                    url_teste = f"{self.url_download_base}/{tag}/Calculadora_Reparos_Palomino.exe"
                    try:
                        resp = requests.head(url_teste, timeout=5, allow_redirects=True)
                        if resp.status_code == 200:
                            arquivo_existe = True
                            url_download = url_teste
                            break
                    except:
                        continue
                
                # Se não encontrou, tentar última release
                if not arquivo_existe:
                    try:
                        ultima_release = self.verificar_ultima_release()
                        url_teste = f"{self.url_download_base}/{ultima_release}/Calculadora_Reparos_Palomino.exe"
                        resp = requests.head(url_teste, timeout=5, allow_redirects=True)
                        if resp.status_code == 200:
                            arquivo_existe = True
                            url_download = url_teste
                    except:
                        pass
            
            return True, {
                'tem_atualizacao': tem_atualizacao,
                'versao_atual': self.versao_atual,
                'versao_remota': versao_remota,
                'changelog': dados.get('changelog', ''),
                'url_download': url_download,
                'arquivo_existe': arquivo_existe,
                'url_versao': self.url_versao
            }
            
        except requests.exceptions.Timeout:
            return False, {
                'erro': 'Timeout ao verificar atualização',
                'detalhes': 'Verifique sua conexão com a internet'
            }
        except requests.exceptions.RequestException as e:
            return False, {
                'erro': f'Erro de conexão: {str(e)}',
                'detalhes': f'URL: {self.url_versao}'
            }
        except Exception as e:
            return False, {
                'erro': f'Erro inesperado: {str(e)}',
                'detalhes': f'Tipo: {type(e).__name__}'
            }
    
    def comparar_versoes(self, versao_remota, versao_atual):
        """Compara duas versões (formato: X.Y.Z)"""
        def versao_para_numero(v):
            try:
                # Remover "v" se houver
                v = str(v).lstrip('vV')
                partes = v.split('.')
                # Garantir 3 partes (major.minor.patch)
                while len(partes) < 3:
                    partes.append('0')
                return tuple(int(p) for p in partes[:3])
            except:
                return (0, 0, 0)
        
        return versao_para_numero(versao_remota) > versao_para_numero(versao_atual)
    
    def baixar_atualizacao(self, url_download=None):
        """Baixa a nova versão do aplicativo"""
        try:
            # Se não tiver URL específica, usar a última release
            if not url_download:
                url_download = f"{self.url_download_base}/v{self.verificar_ultima_release()}/Calculadora_Reparos_Palomino.exe"
            
            # Criar pasta temporária
            temp_dir = Path(os.environ.get('TEMP', '.')) / 'calculadora_update'
            temp_dir.mkdir(exist_ok=True)
            
            arquivo_novo = temp_dir / 'Calculadora_Reparos_Palomino_novo.exe'
            
            # Baixar novo executável
            print(f"Baixando atualização de: {url_download}")
            response = requests.get(url_download, stream=True, timeout=60)
            
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(arquivo_novo, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                
                # Verificar se o arquivo foi baixado corretamente
                if arquivo_novo.stat().st_size > 0:
                    return str(arquivo_novo)
            else:
                print(f"Erro ao baixar: Status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Erro ao baixar atualização: {e}")
            return None
    
    def verificar_ultima_release(self):
        """Obtém a versão da última release"""
        try:
            url = f"https://api.github.com/repos/{self.usuario_github}/{self.repositorio}/releases/latest"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('tag_name', 'latest').lstrip('v')
            return 'latest'
        except:
            return 'latest'
    
    def instalar_atualizacao(self, caminho_novo_exe):
        """Instala a atualização baixada"""
        try:
            # Obter caminho do executável atual
            if hasattr(sys, 'frozen'):
                # Executável compilado
                exe_atual = sys.executable
            else:
                # Modo desenvolvimento
                exe_atual = sys.argv[0]
            
            exe_atual_path = Path(exe_atual)
            pasta_atual = exe_atual_path.parent
            
            # Criar script de atualização
            script_atualizacao = pasta_atual / 'atualizar.bat'
            
            exe_backup = pasta_atual / f"{exe_atual_path.stem}_backup.exe"
            exe_final = pasta_atual / exe_atual_path.name
            
            with open(script_atualizacao, 'w', encoding='utf-8') as f:
                f.write(f'''@echo off
chcp 65001 >nul
echo Aguardando fechamento do aplicativo...
timeout /t 3 /nobreak >nul

echo Fechando aplicativo...
taskkill /F /IM "{exe_atual_path.name}" 2>nul
timeout /t 1 /nobreak >nul

echo Fazendo backup...
if exist "{exe_final}" copy /Y "{exe_final}" "{exe_backup}" >nul

echo Instalando nova versão...
copy /Y "{caminho_novo_exe}" "{exe_final}" >nul

if exist "{exe_final}" (
    echo Atualização concluída!
    echo Iniciando aplicativo...
    start "" "{exe_final}"
    timeout /t 2 /nobreak >nul
    del "{script_atualizacao}" >nul
    exit
) else (
    echo Erro na atualização! Restaurando backup...
    if exist "{exe_backup}" copy /Y "{exe_backup}" "{exe_final}" >nul
    start "" "{exe_final}"
    del "{script_atualizacao}" >nul
    exit
)
''')
            
            # Executar script de atualização
            subprocess.Popen([str(script_atualizacao)], shell=True, 
                           creationflags=subprocess.CREATE_NO_WINDOW)
            return True
            
        except Exception as e:
            print(f"Erro ao instalar atualização: {e}")
            return False


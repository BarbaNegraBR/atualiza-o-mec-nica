# 🔄 Sistema de Atualização Automática

Este aplicativo possui um sistema de atualização automática via GitHub que permite que todos os usuários recebam atualizações automaticamente.

## 📋 Como Funciona

1. **Verificação Automática**: Ao iniciar, o aplicativo verifica se há uma nova versão disponível no GitHub
2. **Notificação**: Se houver atualização, o usuário é notificado
3. **Download e Instalação**: O usuário pode escolher atualizar, e o sistema baixa e instala automaticamente

## 🚀 Como Fazer Upload de uma Nova Versão

### Método 1: Sincronização Automática (Recomendado)

Use o GitHub Desktop ou a extensão do editor para sincronizar automaticamente:

1. **Compile o executável**:
   ```bash
   build_executavel.bat
   ```

2. **Atualize o `versao.json`** com a nova versão:
   ```json
   {
     "versao": "1.0.1",
     "data": "2024-01-15",
     "changelog": "Descrição das mudanças",
     "url_download": ""
   }
   ```

3. **Use GitHub Desktop ou extensão** para fazer commit e push

4. **Crie uma Release no GitHub**:
   - Acesse: https://github.com/BarbaNegraBR/atualiza-o-mec-nica/releases/new
   - Tag: `v1.0.1` (mesma versão do versao.json)
   - Faça upload do executável: `dist/Calculadora_Reparos_Palomino.exe`

### Método 2: Script Automático (Opcional)

Se preferir usar o script Python:

1. **Compile o executável**:
   ```bash
   build_executavel.bat
   ```

2. **Execute o script de upload**:
   ```bash
   upload_github.bat
   ```

### Método 3: Manual

1. **Atualize o arquivo `versao.json`**:
   ```json
   {
     "versao": "1.0.1",
     "data": "2024-01-15",
     "changelog": "Descrição das mudanças",
     "url_download": ""
   }
   ```

2. **Faça commit e push**:
   ```bash
   git add versao.json
   git commit -m "Atualização versão 1.0.1"
   git push origin main
   ```

3. **Crie uma release no GitHub**:
   - Acesse: https://github.com/SEU_USUARIO/atualiza-o-mec-nica/releases/new
   - Crie uma nova release com a tag: `v1.0.1`
   - Faça upload do arquivo: `dist/Calculadora_Reparos_Palomino.exe`
   - Nome do arquivo na release: `Calculadora_Reparos_Palomino.exe`

## ⚙️ Configuração Inicial

### 1. Configurar o Repositório GitHub

Os arquivos já estão configurados com:
- Usuário: `BarbaNegraBR`
- Repositório: `atualiza-o-mec-nica`

Se precisar alterar, edite `atualizador.py` (linha 20).

### 2. Configurar Sincronização Automática

**Opção A - GitHub Desktop:**
1. Abra GitHub Desktop
2. File → Add Local Repository
3. Selecione a pasta do projeto
4. Configure o remote: `https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git`

**Opção B - Git via Terminal:**
```bash
git init
git remote add origin https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 📝 Estrutura de Arquivos

- `atualizador.py` - Módulo que verifica e baixa atualizações
- `versao.json` - Arquivo com informações da versão atual
- `upload_github.py` - Script para fazer upload automático
- `upload_github.bat` - Atalho para executar o script

## 🔧 Requisitos

- Python 3.x
- Git instalado
- Conta no GitHub
- Repositório criado no GitHub

### Opcional (para releases automáticas)

- GitHub CLI (`gh`) instalado
  - Download: https://cli.github.com/

## 📌 Notas Importantes

1. **Nome do Executável**: O nome do arquivo na release deve ser exatamente `Calculadora_Reparos_Palomino.exe`
2. **Tags**: As tags das releases devem seguir o formato `v1.0.0`, `v1.0.1`, etc.
3. **Branch**: O arquivo `versao.json` deve estar na branch `main` (ou `master`)
4. **URL do versao.json**: Deve estar acessível em: 
   `https://raw.githubusercontent.com/BarbaNegraBR/atualiza-o-mec-nica/main/versao.json`

## 🐛 Solução de Problemas

### Erro: "Git não está instalado"
- Instale o Git: https://git-scm.com/downloads

### Erro: "Executável não encontrado"
- Execute primeiro: `build_executavel.bat`

### Erro ao fazer push
- Verifique se você está autenticado no Git
- Configure suas credenciais: `git config --global user.name "Seu Nome"`

### Atualização não aparece para usuários
- Verifique se o `versao.json` está na branch correta
- Verifique se a URL está correta no `atualizador.py`
- Verifique se a release foi criada corretamente no GitHub


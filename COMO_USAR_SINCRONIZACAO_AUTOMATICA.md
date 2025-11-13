# 🔄 Sincronização Automática com GitHub

Este projeto está configurado para funcionar com a sincronização automática do GitHub (GitHub Desktop ou extensão do editor).

## ✅ O que já está configurado

- ✅ Sistema de atualização automática no aplicativo
- ✅ Arquivo `versao.json` para controle de versão
- ✅ URLs configuradas para o repositório: `BarbaNegraBR/atualiza-o-mec-nica`

## 🚀 Como funciona

### 1. **Sincronização Automática (GitHub Desktop ou Extensão)**

Quando você usar o GitHub Desktop ou a extensão do editor:

1. **Faça alterações** no código ou compile um novo executável
2. **Atualize o `versao.json`** com a nova versão:
   ```json
   {
     "versao": "1.0.1",
     "data": "2024-01-15",
     "changelog": "Descrição das mudanças",
     "url_download": ""
   }
   ```
3. **A extensão/GitHub Desktop detecta** as mudanças automaticamente
4. **Faça commit e push** através da interface
5. **Crie uma Release no GitHub**:
   - Acesse: https://github.com/BarbaNegraBR/atualiza-o-mec-nica/releases/new
   - Tag: `v1.0.1` (mesma versão do versao.json)
   - Faça upload do executável: `dist/Calculadora_Reparos_Palomino.exe`
   - Nome do arquivo na release: `Calculadora_Reparos_Palomino.exe`

### 2. **Atualização Automática para Usuários**

- Quando o aplicativo inicia, verifica automaticamente se há nova versão
- Se encontrar, mostra uma mensagem perguntando se deseja atualizar
- Se o usuário aceitar, baixa e instala automaticamente

## 📋 Fluxo de Trabalho Recomendado

1. **Desenvolver/Testar** → Fazer alterações no código
2. **Compilar** → Executar `build_executavel.bat`
3. **Atualizar Versão** → Editar `versao.json` (incrementar versão)
4. **Sincronizar** → Usar GitHub Desktop/extensão para fazer commit e push
5. **Criar Release** → No GitHub, criar release com o executável

## ⚙️ Configuração da Extensão/GitHub Desktop

### GitHub Desktop:
1. Abra o GitHub Desktop
2. File → Add Local Repository
3. Selecione a pasta do projeto
4. Configure o remote: `https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git`

### Extensão do Editor (VS Code/Cursor):
- A extensão Git geralmente detecta automaticamente
- Use a interface de Source Control (Ctrl+Shift+G)
- Configure o remote se necessário

## 📝 Importante

- ✅ O arquivo `versao.json` deve estar sempre atualizado
- ✅ As releases devem ter tags no formato: `v1.0.0`, `v1.0.1`, etc.
- ✅ O nome do arquivo na release: `Calculadora_Reparos_Palomino.exe`
- ✅ O `versao.json` deve estar na branch `main` (ou `master`)

## 🔗 Links Úteis

- Repositório: https://github.com/BarbaNegraBR/atualiza-o-mec-nica
- Criar Release: https://github.com/BarbaNegraBR/atualiza-o-mec-nica/releases/new
- Versão JSON: https://raw.githubusercontent.com/BarbaNegraBR/atualiza-o-mec-nica/main/versao.json


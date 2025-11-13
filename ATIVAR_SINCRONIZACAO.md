# 🚀 Como Ativar a Sincronização Automática do GitHub

Escolha uma das opções abaixo:

---

## 📦 OPÇÃO 1: GitHub Desktop (MAIS FÁCIL - Recomendado)

### Passo 1: Instalar GitHub Desktop
1. Baixe em: https://desktop.github.com/
2. Instale e faça login com sua conta GitHub (`BarbaNegraBR`)

### Passo 2: Adicionar o Repositório
1. Abra o GitHub Desktop
2. Clique em **File** → **Add Local Repository**
3. Clique em **Choose...** e selecione a pasta:
   `C:\Users\jose\Downloads\aplicações\calculadora mecânica`
4. Clique em **Add Repository**

### Passo 3: Configurar o Remote (se necessário)
1. No GitHub Desktop, clique em **Repository** → **Repository Settings**
2. Na aba **Remote**, verifique se está:
   - Remote name: `origin`
   - Primary remote: `origin`
   - URL: `https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git`
3. Se não estiver, clique em **Remove** e depois **Add Remote**:
   - Name: `origin`
   - URL: `https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git`

### Passo 4: Fazer o Primeiro Commit e Push
1. No GitHub Desktop, você verá todos os arquivos modificados
2. Escreva uma mensagem de commit (ex: "Configuração inicial")
3. Clique em **Commit to main** (ou **Commit to master**)
4. Clique em **Publish branch** (se for a primeira vez) ou **Push origin**

### ✅ Pronto!
Agora sempre que você fizer alterações:
- O GitHub Desktop detecta automaticamente
- Você faz commit e push pela interface
- Os arquivos são sincronizados automaticamente

---

## 💻 OPÇÃO 2: Git via Terminal/Extensão do Editor

### Passo 1: Verificar se Git está instalado
Abra o terminal (PowerShell) e digite:
```bash
git --version
```

Se não estiver instalado:
- Baixe em: https://git-scm.com/downloads
- Instale com as opções padrão

### Passo 2: Inicializar o Repositório
No terminal, na pasta do projeto:
```bash
cd "c:\Users\jose\Downloads\aplicações\calculadora mecânica"
git init
```

### Passo 3: Configurar o Remote
```bash
git remote add origin https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git
```

### Passo 4: Configurar suas credenciais (primeira vez)
```bash
git config --global user.name "BarbaNegraBR"
git config --global user.email "seu_email@exemplo.com"
```

### Passo 5: Fazer o Primeiro Commit e Push
```bash
git add .
git commit -m "Configuração inicial"
git branch -M main
git push -u origin main
```

### Passo 6: Usar a Extensão do Editor (Cursor/VS Code)
1. Abra o Cursor/VS Code na pasta do projeto
2. A extensão Git já vem instalada
3. Use o ícone de Source Control (Ctrl+Shift+G)
4. Você verá as mudanças automaticamente
5. Faça commit e push pela interface

### ✅ Pronto!
Agora sempre que você fizer alterações:
- A extensão detecta automaticamente
- Use Ctrl+Shift+G para ver mudanças
- Faça commit e push pela interface

---

## 🔄 Como Usar Depois de Configurado

### Com GitHub Desktop:
1. Faça suas alterações no código
2. Abra o GitHub Desktop
3. Veja as mudanças na aba "Changes"
4. Escreva uma mensagem de commit
5. Clique em "Commit to main"
6. Clique em "Push origin"

### Com Extensão do Editor:
1. Faça suas alterações no código
2. Pressione **Ctrl+Shift+G** (Source Control)
3. Veja as mudanças listadas
4. Clique no **+** ao lado dos arquivos para adicionar
5. Escreva uma mensagem de commit
6. Clique em **✓ Commit**
7. Clique em **...** → **Push**

---

## ⚠️ Importante

- Sempre atualize o `versao.json` antes de fazer commit
- Depois do push, crie a Release no GitHub manualmente
- O arquivo `versao.json` deve estar na branch `main`

---

## 🆘 Precisa de Ajuda?

Se tiver problemas:
1. Verifique se está logado no GitHub
2. Verifique se o repositório existe: https://github.com/BarbaNegraBR/atualiza-o-mec-nica
3. Verifique se tem permissão para fazer push


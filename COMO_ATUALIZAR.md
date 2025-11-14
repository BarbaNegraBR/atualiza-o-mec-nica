# 🔄 Como Fazer Atualizações Funcionarem

## ⚠️ IMPORTANTE: Processo Completo de Atualização

Quando você fizer mudanças no código (valores, nomes de itens, etc.), siga ESTES passos:

### 1. ✅ Fazer as Alterações no Código
- Edite `calculadora_reparos_gui.py` (valores, nomes, etc.)
- Teste localmente

### 2. ✅ Atualizar a Versão no `versao.json`
Edite `versao.json` e incremente a versão:
```json
{
  "versao": "1.0.2",  // ← Incremente aqui (1.0.1 → 1.0.2)
  "data": "2024-01-16",
  "changelog": "Atualização de valores e nomes dos itens",
  "url_download": ""
}
```

### 3. ✅ Atualizar a Versão no `atualizador.py`
Edite `atualizador.py` linha 22 e coloque a MESMA versão:
```python
self.versao_atual = "1.0.2"  # ← Mesma versão do versao.json
```

### 4. ✅ Compilar o Novo Executável
```bash
build_executavel.bat
```
Isso cria o executável atualizado em `dist/Calculadora_Reparos_Palomino.exe`

### 5. ✅ Sincronizar com GitHub
- Use GitHub Desktop ou extensão do editor
- Faça commit e push de TODOS os arquivos:
  - `calculadora_reparos_gui.py` (com suas mudanças)
  - `versao.json` (com versão incrementada)
  - `atualizador.py` (com versão atualizada)

### 6. ✅ Criar Nova Release no GitHub
**ESTE PASSO É ESSENCIAL!**

1. Acesse: https://github.com/BarbaNegraBR/atualiza-o-mec-nica/releases/new
2. Crie uma nova release:
   - **Tag**: `v1.0.2` (mesma versão do versao.json, com "v" na frente)
   - **Title**: `Versão 1.0.2`
   - **Description**: Descreva as mudanças
3. **Faça upload do executável**:
   - Arraste o arquivo: `dist/Calculadora_Reparos_Palomino.exe`
   - **IMPORTANTE**: O nome do arquivo na release deve ser: `Calculadora_Reparos_Palomino.exe`
4. Clique em **Publish release**

### 7. ✅ Testar a Atualização
- Abra o aplicativo antigo no seu PC
- Ele deve detectar a nova versão automaticamente
- Aceite a atualização quando perguntar

---

## ❌ Por que não atualizou?

Se você fez mudanças mas não atualizou:
- ❌ Não incrementou a versão no `versao.json`
- ❌ Não atualizou a versão no `atualizador.py`
- ❌ Não compilou um novo executável
- ❌ Não criou uma nova release no GitHub
- ❌ Não fez upload do executável na release

**O sistema só detecta atualização se a versão no GitHub for MAIOR que a versão local!**

---

## 🔍 Verificar se Está Funcionando

1. Verifique a versão no GitHub:
   https://raw.githubusercontent.com/BarbaNegraBR/atualiza-o-mec-nica/main/versao.json

2. Verifique se a release existe:
   https://github.com/BarbaNegraBR/atualiza-o-mec-nica/releases

3. Teste no aplicativo antigo - ele deve mostrar a atualização disponível

---

## 📝 Checklist Rápido

- [ ] Alterações feitas no código
- [ ] Versão incrementada no `versao.json`
- [ ] Versão atualizada no `atualizador.py`
- [ ] Executável compilado (`build_executavel.bat`)
- [ ] Commit e push feito no GitHub
- [ ] Release criada no GitHub
- [ ] Executável enviado na release
- [ ] Testado no aplicativo antigo


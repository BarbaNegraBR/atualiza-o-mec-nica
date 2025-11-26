# 🔒 Correções para Evitar Ban do Anti-Cheat do MTA

## ⚠️ Problema Identificado

O script de atualização estava causando ban no MTA (Multi Theft Auto) porque o anti-cheat do servidor detectava comportamentos suspeitos típicos de cheats:

1. **`taskkill /F`** - Força encerramento de processos (comportamento típico de cheats)
2. **`CREATE_NO_WINDOW`** - Execução de processos ocultos (suspeito para anti-cheat)
3. **Criação dinâmica de scripts .bat** - Pode ser interpretado como tentativa de injeção
4. **Requisições HTTP frequentes** - Pode ser detectado como comunicação com servidor de cheat

## ✅ Correções Aplicadas

### 1. **Detecção de Processo MTA Rodando**
- ✅ Adicionada função `mta_esta_rodando()` que detecta se o MTA está ativo
- ✅ Verifica processos: `mtasa.exe`, `multi theft auto.exe`, `gta_sa.exe`, etc.
- ✅ Funciona com `psutil` (se instalado) ou `tasklist` (fallback no Windows)

### 2. **Bloqueio de Verificação Automática Durante Jogo**
- ✅ Verificação automática de atualizações **CANCELADA** se MTA estiver rodando
- ✅ Usuário não é interrompido com pop-ups durante o jogo
- ✅ Logs silenciosos (não aparecem para o usuário)

### 3. **Aviso na Verificação Manual**
- ✅ Se o usuário tentar verificar atualizações manualmente com MTA rodando:
  - Mostra aviso claro explicando o motivo
  - Solicita fechar o MTA antes de continuar

### 4. **Remoção de Comportamentos Suspeitos**

#### a) **Taskkill /F Removido**
```diff
- taskkill /F /IM "exe_name.exe"  ← FORÇA BRUTA (detectado como cheat)
+ taskkill /IM "exe_name.exe"     ← Fechamento suave (seguro)
```

#### b) **CREATE_NO_WINDOW Removido**
```diff
- subprocess.Popen([...], creationflags=CREATE_NO_WINDOW)  ← Oculto (suspeito)
+ subprocess.Popen([...], shell=True)                       ← Visível (normal)
```

### 5. **Verificação Antes de Instalar Atualização**
- ✅ Antes de instalar, verifica se MTA está rodando
- ✅ Se estiver, **cancela a instalação** e avisa o usuário
- ✅ Previne conflitos com anti-cheat durante atualização

## 📋 Arquivos Modificados

1. **`atualizador.py`**
   - Adicionada função `mta_esta_rodando()`
   - Modificada `verificar_atualizacao()` - bloqueia se MTA ativo
   - Modificada `verificar_atualizacao_completo()` - bloqueia se MTA ativo
   - Modificada `instalar_atualizacao()` - remove taskkill /F, remove CREATE_NO_WINDOW

2. **`calculadora_reparos_gui.py`**
   - Modificada `verificar_atualizacoes()` - não verifica se MTA ativo
   - Modificada `verificar_atualizacoes_manual()` - avisa se MTA ativo
   - Adicionada função `mostrar_aviso_mta()`

3. **`requirements.txt`**
   - Adicionado `psutil>=5.9.0` (opcional, tem fallback)

## 🚀 Como Usar

### Comportamento Automático:
1. Se MTA **NÃO** estiver rodando → Verifica atualizações normalmente
2. Se MTA **ESTIVER** rodando → **NÃO** verifica (silencioso)

### Verificação Manual:
1. Usuário clica em "🔄 Verificar Atualizações"
2. Se MTA estiver rodando → Mostra aviso para fechar o jogo
3. Se MTA **NÃO** estiver rodando → Verifica normalmente

### Instalação de Atualização:
1. Sistema detecta nova versão
2. **Verifica se MTA está rodando**
3. Se estiver → **Cancela** e avisa para fechar o jogo
4. Se **NÃO** estiver → Instala normalmente

## ⚙️ Instalação de Dependências

Se quiser usar `psutil` (mais eficiente):
```bash
pip install psutil
```

Ou instalar todas as dependências:
```bash
pip install -r requirements.txt
```

**Nota:** O script funciona **sem** psutil, usando `tasklist` como alternativa no Windows.

## 🔍 Processos Detectados

O sistema detecta os seguintes processos como MTA:
- `multi theft auto.exe`
- `mtasa.exe`
- `mta.exe`
- `gta_sa.exe` (GTA San Andreas original)
- `gta-vc.exe` (GTA Vice City)
- `gta3.exe` (GTA III)

## ⚠️ Recomendações

1. **SEMPRE feche o MTA antes de atualizar o aplicativo**
2. Não execute o aplicativo de calculadora enquanto joga MTA (se não for necessário)
3. Se precisar usar durante o jogo, não verifique atualizações até fechar o MTA

## 📝 Teste

Para testar se está funcionando:
1. Abra o MTA
2. Abra a calculadora
3. A verificação automática não deve acontecer (silencioso)
4. Tente verificar manualmente → Deve mostrar aviso sobre MTA
5. Feche o MTA
6. Verifique novamente → Deve funcionar normalmente

---

**Status:** ✅ Todas as correções aplicadas
**Data:** $(Get-Date -Format "yyyy-MM-dd")


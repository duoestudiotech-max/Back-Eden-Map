# 📖 Exemplos de Uso da API

Guia prático com exemplos reais de uso da API Eden Map.

---

## 🔐 1. Fluxo Completo de Autenticação

### 1.1 Criar Novo Usuário

```bash
curl -X POST "https://back-eden-map.onrender.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao_silva",
    "password": "Senha123@",
    "email": "joao.silva@email.com",
    "tag": "client",
    "plan": "trial"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwibG9naW4iOiJqb2FvX3NpbHZhIiwidGFnIjoiY2xpZW50IiwiZXhwIjoxNzM1Mzk4MDAwLCJ0eXBlIjoiYWNjZXNzIn0...",
  "refresh_token": "aKf8jH3mN9pQ2sT5vW8xZ1bC4dE6fG7hI8jK9lM0nO1pQ2rS3tU4vW5xY6zA7bC8dE9...",
  "token_type": "bearer",
  "user": {
    "id": 4,
    "login": "joao_silva",
    "email": "joao.silva@email.com",
    "tag": "client",
    "plan": "trial",
    "plan_date": "2025-11-27T10:00:00",
    "selected_path": null,
    "progress": null
  }
}
```

**✅ Resultado:**
- Usuário criado
- Email de boas-vindas enviado (se Brevo configurado)
- Tokens retornados (já autenticado!)

---

### 1.2 Login de Usuário Existente

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao_silva",
    "password": "Senha123@"
  }'
```

**Resposta:** (mesmo formato do cadastro)

---

### 1.3 Renovar Token Expirado

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "aKf8jH3mN9pQ2sT5vW8xZ1bC4dE6fG7hI8jK9..."
  }'
```

**Resposta:**
```json
{
  "access_token": "novo_access_token...",
  "refresh_token": "novo_refresh_token...",
  "token_type": "bearer",
  "user": { ... }
}
```

**💡 Dica:** O refresh token também é renovado! Sempre salve o novo.

---

## 🛤️ 2. Jornada do Usuário

### 2.1 Selecionar Caminho

```bash
curl -X PUT "https://back-eden-map.onrender.com/users/selected-path" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "selected_path": "Ansiedade"
  }'
```

**Caminhos válidos:**
- `"Ansiedade"`
- `"Atenção Plena"`
- `"Autoimagem"`
- `"Motivação"`
- `"Relacionamentos"`
- `null` (resetar)

**Resposta:**
```json
{
  "message": "Selected path updated successfully",
  "updated_field": "selected_path",
  "user_id": 4,
  "email": "joao.silva@email.com",
  "selected_path": "Ansiedade"
}
```

---

### 2.2 Resetar Caminho

```bash
curl -X PUT "https://back-eden-map.onrender.com/users/selected-path" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "selected_path": null
  }'
```

---

## 🧪 3. Testes de Autoavaliação

### 3.1 Enviar Resultados dos Testes

```bash
curl -X PUT "https://back-eden-map.onrender.com/users/test-results" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "test_results": {
      "Ansiedade": 75,
      "Atenção_Plena": 45,
      "Autoimagem": 60,
      "Motivação": 80,
      "Relacionamentos": 55
    }
  }'
```

**⚠️ Importante:** Use `Atenção_Plena` (com underscore) no JSON!

**Resposta:**
```json
{
  "message": "Test results updated successfully",
  "updated_field": "test_results",
  "user_id": 4,
  "email": "joao.silva@email.com",
  "test_results": {
    "Ansiedade": 75,
    "Atenção Plena": 45,
    "Autoimagem": 60,
    "Motivação": 80,
    "Relacionamentos": 55
  }
}
```

**📝 Nota:** O banco salva como `"Atenção Plena"` (com espaço).

---

## 📊 4. Progresso da Jornada

### 4.1 Atualizar Progresso

```bash
curl -X PUT "https://back-eden-map.onrender.com/users/progress" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "progress": {
      "semana": 3,
      "dia": 5
    }
  }'
```

**Validações:**
- `semana`: 1 a 12
- `dia`: 1 a 7

**Resposta:**
```json
{
  "message": "Progress updated successfully",
  "user_id": 4,
  "email": "joao.silva@email.com",
  "progress": {
    "semana": 3,
    "dia": 5
  },
  "progress_updated_at": "2025-11-27T14:30:00.123456"
}
```

---

### 4.2 Buscar Dados Completos do Usuário

```bash
curl -X POST "https://back-eden-map.onrender.com/users/data" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com"
  }'
```

**Resposta:**
```json
{
  "user_id": 4,
  "login": "joao_silva",
  "email": "joao.silva@email.com",
  "selected_path": "Ansiedade",
  "test_results": {
    "Ansiedade": 75,
    "Atenção Plena": 45,
    "Autoimagem": 60,
    "Motivação": 80,
    "Relacionamentos": 55
  },
  "progress": {
    "semana": 3,
    "dia": 5
  }
}
```

---

## 🔑 5. Recuperação de Senha

### 5.1 Solicitar Código (Etapa 1)

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/password-recovery/request" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com"
  }'
```

**Resposta:**
```json
{
  "message": "If this email exists, a recovery code has been sent",
  "email": "joao.silva@email.com"
}
```

**📧 Email enviado:**
```
Assunto: 🔐 Seu Código de Recuperação de Senha - Eden Map

Seu código: 1234
Expira em: 15 minutos
```

---

### 5.2 Verificar Código (Etapa 2 - Opcional)

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/password-recovery/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "code": "1234"
  }'
```

**Resposta (sucesso):**
```json
{
  "message": "Recovery code verified successfully",
  "email": "joao.silva@email.com"
}
```

**Resposta (erro - código expirado):**
```json
{
  "detail": "Recovery code has expired. Please request a new one."
}
```

---

### 5.3 Redefinir Senha (Etapa 3)

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/password-recovery/reset" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "code": "1234",
    "new_password": "NovaSenha456@"
  }'
```

**Resposta:**
```json
{
  "message": "Password reset successfully",
  "email": "joao.silva@email.com"
}
```

---

### 5.4 Login com Nova Senha

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao_silva",
    "password": "NovaSenha456@"
  }'
```

**✅ Deve funcionar!**

---

## 🔍 6. Consultas de Usuários

### 6.1 Buscar por ID

```bash
curl -X GET "https://back-eden-map.onrender.com/users/4"
```

**Resposta:**
```json
{
  "id": 4,
  "login": "joao_silva",
  "email": "joao.silva@email.com",
  "tag": "client",
  "plan": "trial",
  "plan_date": "2025-11-27T10:00:00",
  "selected_path": "Ansiedade",
  "test_results": { ... },
  "progress": { ... },
  "created_at": "2025-11-27T10:00:00"
}
```

---

### 6.2 Listar Usuários (Paginado)

```bash
curl -X GET "https://back-eden-map.onrender.com/users/?skip=0&limit=10"
```

**Resposta:**
```json
[
  {
    "id": 1,
    "login": "dieghonm",
    "email": "dieghonm@gmail.com",
    "tag": "admin",
    ...
  },
  {
    "id": 2,
    "login": "cavamaga",
    ...
  }
]
```

---

## ⚠️ 7. Tratamento de Erros

### 7.1 Email Já Cadastrado

```bash
curl -X POST "https://back-eden-map.onrender.com/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "novo_usuario",
    "password": "Senha123@",
    "email": "joao.silva@email.com",
    "tag": "client",
    "plan": "trial"
  }'
```

**Resposta (400):**
```json
{
  "detail": "Email already registered"
}
```

---

### 7.2 Login Já Cadastrado

**Resposta (400):**
```json
{
  "detail": "Login already registered"
}
```

---

### 7.3 Credenciais Inválidas

```bash
curl -X POST "https://back-eden-map.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "joao_silva",
    "password": "SenhaErrada"
  }'
```

**Resposta (401):**
```json
{
  "detail": "Invalid credentials"
}
```

---

### 7.4 Token Inválido/Expirado

**Resposta (401):**
```json
{
  "detail": "Invalid or expired refresh token"
}
```

---

### 7.5 Rate Limit Excedido

**Resposta (429):**
```json
{
  "detail": {
    "message": "Too many login attempts. Try again later.",
    "retry_after": 3456,
    "reset_at": "2025-11-27T15:30:00"
  }
}
```

---

### 7.6 Validação de Dados

```bash
curl -X PUT "https://back-eden-map.onrender.com/users/test-results" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.silva@email.com",
    "test_results": {
      "Ansiedade": 150,
      "Atenção_Plena": -10,
      "Autoimagem": 60,
      "Motivação": 80,
      "Relacionamentos": 55
    }
  }'
```

**Resposta (422):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "test_results", "Ansiedade"],
      "msg": "Cada pontuação deve estar entre 0 e 100"
    }
  ]
}
```

---

## 📱 8. Integração com Frontend

### 8.1 React/React Native

```javascript
const API_URL = 'https://back-eden-map.onrender.com';

// Login
async function login(username, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      login: username,
      password: password,
    }),
  });
  
  const data = await response.json();
  
  // Salvar tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
  
  return data.user;
}

// Requisição autenticada
async function getUserData(email) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${API_URL}/users/data`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ email }),
  });
  
  return await response.json();
}

// Atualizar progresso
async function updateProgress(email, semana, dia) {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${API_URL}/users/progress`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      email,
      progress: { semana, dia },
    }),
  });
  
  return await response.json();
}
```

---

### 8.2 Python

```python
import requests

API_URL = "https://back-eden-map.onrender.com"

# Login
def login(username, password):
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"login": username, "password": password}
    )
    data = response.json()
    return data

# Criar usuário
def create_user(login, email, password):
    response = requests.post(
        f"{API_URL}/users/",
        json={
            "login": login,
            "email": email,
            "password": password,
            "tag": "client",
            "plan": "trial"
        }
    )
    return response.json()

# Atualizar caminho
def update_path(email, path):
    response = requests.put(
        f"{API_URL}/users/selected-path",
        json={"email": email, "selected_path": path}
    )
    return response.json()
```

---

## 💡 9. Boas Práticas

### ✅ Sempre Salvar Novo Refresh Token

```javascript
// Renovar token
const response = await fetch(`${API_URL}/auth/refresh`, {
  method: 'POST',
  body: JSON.stringify({
    refresh_token: oldRefreshToken
  })
});

const data = await response.json();

// ⚠️ IMPORTANTE: Salvar AMBOS os tokens novos!
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('refresh_token', data.refresh_token);  // ← Novo!
```

---

### ✅ Tratar Rate Limit

```javascript
async function loginWithRetry(username, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({ login: username, password })
    });
    
    if (response.status === 429) {
      const error = await response.json();
      const retryAfter = error.detail.retry_after;
      
      console.log(`Rate limit! Tente novamente em ${retryAfter} segundos`);
      return null;
    }
    
    return await response.json();
    
  } catch (error) {
    console.error('Erro no login:', error);
    return null;
  }
}
```

---

### ✅ Validar Dados Antes de Enviar

```javascript
function validateTestResults(results) {
  const requiredFields = [
    'Ansiedade',
    'Atenção_Plena',
    'Autoimagem',
    'Motivação',
    'Relacionamentos'
  ];
  
  for (const field of requiredFields) {
    if (!results[field]) {
      throw new Error(`Campo ${field} é obrigatório`);
    }
    
    const value = results[field];
    if (value < 0 || value > 100) {
      throw new Error(`${field} deve estar entre 0 e 100`);
    }
  }
  
  return true;
}
```

---

## 🎯 10. Casos de Uso Completos

### Fluxo: Novo Usuário Completo

```bash
# 1. Criar usuário
curl -X POST "https://back-eden-map.onrender.com/users/" \
  -d '{"login":"maria","password":"Senha123@","email":"maria@email.com"}'

# 2. Fazer testes
curl -X PUT "https://back-eden-map.onrender.com/users/test-results" \
  -d '{"email":"maria@email.com","test_results":{"Ansiedade":70,...}}'

# 3. Escolher caminho
curl -X PUT "https://back-eden-map.onrender.com/users/selected-path" \
  -d '{"email":"maria@email.com","selected_path":"Ansiedade"}'

# 4. Iniciar jornada (Semana 1, Dia 1)
curl -X PUT "https://back-eden-map.onrender.com/users/progress" \
  -d '{"email":"maria@email.com","progress":{"semana":1,"dia":1}}'
```

---

**🌿 Para mais exemplos, consulte a [documentação interativa](https://back-eden-map.onrender.com/docs)!**
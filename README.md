# 🌿 Back-Eden-Map API

API RESTful completa para gerenciamento de usuários, autenticação, progresso e jornadas do **Eden Map** - Uma plataforma de desenvolvimento pessoal e bem-estar emocional.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌐 **API em Produção:** [https://back-eden-map.onrender.com](https://back-eden-map.onrender.com)  
📚 **Documentação Interativa:** [https://back-eden-map.onrender.com/docs](https://back-eden-map.onrender.com/docs)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Instalação Local](#-instalação-local)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Como Usar](#-como-usar)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação](#-autenticação)
- [Rate Limiting](#-rate-limiting)
- [Modelo de Dados](#-modelo-de-dados)
- [Deploy](#-deploy)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Back-Eden-Map** é uma API robusta e escalável que oferece um sistema completo de gerenciamento de usuários com foco em jornadas de desenvolvimento pessoal. A plataforma permite que usuários:

- 🔐 Se autentiquem de forma segura com JWT
- 📊 Acompanhem seu progresso em jornadas de 12 semanas
- 🧪 Realizem testes de autoavaliação em 5 áreas
- 🛤️ Escolham caminhos personalizados de desenvolvimento
- 📧 Recuperem senhas de forma segura
- 🔄 Mantenham sessões ativas com refresh tokens

---

## ✨ Funcionalidades

### 🔐 Autenticação e Segurança
- ✅ Login com JWT (Access Token + Refresh Token)
- ✅ Sistema de refresh token automático (30 dias de validade)
- ✅ Recuperação de senha com código de 4 dígitos (15 minutos de expiração)
- ✅ Hash de senhas com bcrypt
- ✅ Rate limiting por IP para prevenir abuso
- ✅ Validação robusta de dados com Pydantic

### 👤 Gerenciamento de Usuários
- ✅ Cadastro de novos usuários
- ✅ Busca de usuários por ID
- ✅ Listagem paginada de usuários
- ✅ Atualização de dados do usuário
- ✅ Sistema de tags (admin, client)
- ✅ Planos (trial, mensal, trimestral, semestral, anual)

### 📊 Sistema de Progresso
- ✅ Atualização de progresso (semana 1-12, dia 1-7)
- ✅ Timestamp automático de última atualização
- ✅ Histórico de evolução

### 🧪 Testes de Autoavaliação
- ✅ 5 áreas avaliadas (0-100 pontos):
  - Ansiedade
  - Atenção Plena
  - Autoimagem
  - Motivação
  - Relacionamentos
- ✅ Escolha de caminho personalizado baseado nos resultados

### 📧 Sistema de Emails
- ✅ Email de boas-vindas ao se cadastrar
- ✅ Email com código de recuperação de senha
- ✅ Templates HTML responsivos e profissionais
- ✅ Integração com Brevo (SendinBlue)

---

## 🛠️ Tecnologias

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM para Python
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validação de dados
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional

### Autenticação & Segurança
- **[python-jose](https://github.com/mpdavis/python-jose)** - JWT
- **[passlib](https://passlib.readthedocs.io/)** - Hash de senhas
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Algoritmo de hash

### Email & Comunicação
- **[Brevo API](https://www.brevo.com/)** - Envio de emails transacionais
- **[requests](https://requests.readthedocs.io/)** - Cliente HTTP

### Deploy & Produção
- **[Gunicorn](https://gunicorn.org/)** - WSGI HTTP Server
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI Server
- **[Render](https://render.com/)** - Plataforma de deploy

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura limpa e modular baseada em camadas:

```
Back-Eden-Map/
│
├── app/
│   ├── auth/                    # Autenticação e segurança
│   │   ├── dependencies.py      # Dependencies do FastAPI (rate limiting)
│   │   └── rate_limiter.py      # Sistema de rate limiting
│   │
│   ├── controllers/             # Controladores (orquestração)
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── user_update_controller.py
│   │   └── password_recovery_controller.py
│   │
│   ├── core/                    # Configurações centrais
│   │   ├── config.py            # Configurações e variáveis de ambiente
│   │   ├── database.py          # Setup do banco de dados
│   │   ├── init_db.py           # Inicialização e seeds
│   │   └── security.py          # Funções de segurança (hash)
│   │
│   ├── models/                  # Models SQLAlchemy
│   │   ├── user.py              # Model User
│   │   └── refresh_token.py     # Model RefreshToken
│   │
│   ├── routers/                 # Rotas da API
│   │   ├── auth_routes.py       # Rotas de autenticação
│   │   ├── user_routes.py       # Rotas de usuários
│   │   ├── user_update_routes.py
│   │   └── password_recovery_routes.py
│   │
│   ├── schemas/                 # Schemas Pydantic
│   │   ├── auth_schemas.py
│   │   ├── user_schemas.py
│   │   ├── user_update_schemas.py
│   │   └── password_recovery_schemas.py
│   │
│   ├── services/                # Lógica de negócio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── user_update_service.py
│   │   ├── password_recovery_service.py
│   │   ├── email_service.py
│   │   └── validators.py
│   │
│   └── main.py                  # Aplicação principal
│
├── .env                         # Variáveis de ambiente (local)
├── .env.example                 # Template de variáveis
├── .gitignore
├── .python-version              # Versão do Python
├── build.sh                     # Script de build (Render)
├── requirements.txt             # Dependências Python
├── runtime.txt                  # Versão Python (Render)
├── start.sh                     # Script de start (Render)
└── README.md
```

### 📐 Fluxo de Requisição

```
Request → Router → Controller → Service → Database
                                   ↓
                              Validators
                                   ↓
                            External APIs
```

**Exemplo prático:**
```
POST /users/
    ↓
user_routes.py (valida input)
    ↓
user_controller.py (orquestra)
    ↓
user_service.py (lógica de negócio)
    ↓
validators.py (valida duplicatas)
    ↓
models/user.py (salva no banco)
    ↓
email_service.py (envia email)
    ↓
schemas/user_schemas.py (formata resposta)
    ↓
Response 201 Created
```

---

## 💻 Instalação Local

### Pré-requisitos

- Python 3.11+
- PostgreSQL 14+ (ou SQLite para desenvolvimento)
- Git

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/seu-usuario/back-eden-map.git
cd back-eden-map
```

### 2️⃣ Crie o Ambiente Virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure o Arquivo .env

```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:

```env
# Database (use SQLite para desenvolvimento local)
DATABASE_URL=sqlite:///./dev.db

# JWT
SECRET_KEY=seu-secret-key-super-seguro-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# Rate Limiting
RATE_LIMIT_REGISTER=2
RATE_LIMIT_REFRESH=4
RATE_LIMIT_LOGIN=16
RATE_LIMIT_PASSWORD_RECOVERY=12

# Email (Brevo - opcional para desenvolvimento)
BREVO_API_KEY=sua-api-key-brevo
BREVO_SENDER_EMAIL=seu-email@dominio.com
BREVO_SENDER_NAME=Eden Map
EMAIL_ENABLED=true

# Environment
ENVIRONMENT=development
```

### 5️⃣ Inicie o Servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em:
- 🌐 **API:** http://localhost:8000
- 📚 **Documentação:** http://localhost:8000/docs
- 📖 **ReDoc:** http://localhost:8000/redoc

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatória | Padrão |
|----------|-----------|-------------|--------|
| `DATABASE_URL` | URL de conexão do banco | ✅ | `sqlite:///./dev.db` |
| `SECRET_KEY` | Chave secreta para JWT | ✅ | - |
| `ALGORITHM` | Algoritmo JWT | ❌ | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token (min) | ❌ | `43200` (30 dias) |
| `RATE_LIMIT_REGISTER` | Limite de cadastros/hora | ❌ | `2` |
| `RATE_LIMIT_LOGIN` | Limite de logins/hora | ❌ | `16` |
| `RATE_LIMIT_REFRESH` | Limite de refresh/hora | ❌ | `4` |
| `RATE_LIMIT_PASSWORD_RECOVERY` | Limite de recuperação/hora | ❌ | `12` |
| `BREVO_API_KEY` | Chave API do Brevo | ❌ | - |
| `BREVO_SENDER_EMAIL` | Email de envio | ❌ | - |
| `BREVO_SENDER_NAME` | Nome do remetente | ❌ | `Eden Map` |
| `EMAIL_ENABLED` | Habilitar emails | ❌ | `true` |
| `ENVIRONMENT` | Ambiente (dev/prod) | ❌ | `development` |

### 🔑 Gerando SECRET_KEY Seguro

```python
# Execute no terminal Python:
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🚀 Como Usar

### 📚 Documentação Interativa (Swagger)

Acesse: [https://back-eden-map.onrender.com/docs](https://back-eden-map.onrender.com/docs)

Você pode testar todos os endpoints diretamente no navegador!

### 🔑 Credenciais dos Usuários Iniciais

Três administradores são criados automaticamente:

| Login | Email | Senha | Tag |
|-------|-------|-------|-----|
| `dieghonm` | dieghonm@gmail.com | `Admin123@` | admin |
| `cavamaga` | cava.maga@gmail.com | `Admin123@` | admin |
| `tiaguetevital` | tiagovital999@gmail.com | `Admin123@` | admin |

---

## 📡 Endpoints da API

### 🔐 Autenticação (`/auth`)

| Método | Endpoint | Descrição | Rate Limit |
|--------|----------|-----------|------------|
| `POST` | `/auth/login` | Login com usuário e senha | 16/hora |
| `POST` | `/auth/refresh` | Renovar access token | 4/hora |

### 👤 Usuários (`/users`)

| Método | Endpoint | Descrição | Rate Limit |
|--------|----------|-----------|------------|
| `POST` | `/users/` | Criar novo usuário | 2/hora |
| `GET` | `/users/{id}` | Buscar usuário por ID | - |
| `GET` | `/users/?skip=0&limit=10` | Listar usuários | - |
| `POST` | `/users/data` | Buscar dados completos por email | - |

### 🔄 Atualizações (`/users`)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `PUT` | `/users/selected-path` | Atualizar caminho selecionado |
| `PUT` | `/users/test-results` | Atualizar resultados dos testes |
| `PUT` | `/users/progress` | Atualizar progresso (semana/dia) |

### 🔑 Recuperação de Senha (`/auth/password-recovery`)

| Método | Endpoint | Descrição | Rate Limit |
|--------|----------|-----------|------------|
| `POST` | `/auth/password-recovery/request` | Solicitar código | 12/hora |
| `POST` | `/auth/password-recovery/verify` | Verificar código | 12/hora |
| `POST` | `/auth/password-recovery/reset` | Redefinir senha | 12/hora |

### 🏥 Utilitários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `GET` | `/health` | Status da API |

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação.

### 1️⃣ Login

```bash
POST /auth/login
Content-Type: application/json

{
  "login": "dieghonm",
  "password": "Admin123@"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "aKf8jH3mN9pQ2sT5vW8xZ1bC4dE6fG7hI8jK9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "login": "dieghonm",
    "email": "dieghonm@gmail.com",
    "tag": "admin",
    "plan": "admin"
  }
}
```

### 2️⃣ Usar o Token

```bash
GET /users/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3️⃣ Renovar Token

```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "aKf8jH3mN9pQ2sT5vW8xZ1bC4dE6fG7hI8jK9..."
}
```

### ⏰ Expiração

- **Access Token:** 30 dias (43.200 minutos)
- **Refresh Token:** 30 dias (renovável automaticamente ao usar)

---

## ⏱️ Rate Limiting

Proteção contra abuso por IP:

| Rota | Limite | Janela | Descrição |
|------|--------|--------|-----------|
| `/users/` | 2 req | 1 hora | Cadastro de usuários |
| `/auth/login` | 16 req | 1 hora | Login |
| `/auth/refresh` | 4 req | 1 hora | Renovação de token |
| `/auth/password-recovery/*` | 12 req | 1 hora | Recuperação de senha |

**Resposta quando limite excedido (429):**
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

## 📊 Modelo de Dados

### 👤 User

```python
{
  "id": 1,
  "login": "dieghonm",
  "email": "dieghonm@gmail.com",
  "password": "hashed_password",  # Hash bcrypt
  "tag": "admin",                 # admin, client
  "plan": "admin",                # trial, mensal, trimestral, semestral, anual, admin
  "plan_date": "2025-11-27T10:00:00",
  
  # Senha temporária (recuperação)
  "temp_password": null,
  "temp_password_expires": null,
  
  # Dados da jornada
  "selected_path": "Ansiedade",   # Caminho escolhido
  "test_results": {
    "Ansiedade": 75,
    "Atenção Plena": 45,
    "Autoimagem": 60,
    "Motivação": 80,
    "Relacionamentos": 55
  },
  
  # Progresso
  "progress": {
    "semana": 3,  # 1-12
    "dia": 5      # 1-7
  },
  "progress_updated_at": "2025-11-27T14:30:00",
  
  # Timestamps
  "created_at": "2025-11-27T10:00:00",
  "updated_at": "2025-11-27T14:30:00"
}
```

### 🔄 RefreshToken

```python
{
  "id": 1,
  "user_id": 1,
  "token": "aKf8jH3mN9pQ2sT5vW8xZ...",
  "expires_at": "2025-12-27T10:00:00",
  "is_revoked": false,
  "created_at": "2025-11-27T10:00:00",
  "last_used_at": "2025-11-27T14:00:00",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0..."
}
```

---

## 🚀 Deploy

### Deploy no Render (Recomendado)

Siga o guia completo: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

**Resumo:**
1. Crie PostgreSQL no Render
2. Crie Web Service conectado ao GitHub
3. Configure variáveis de ambiente
4. Deploy automático! 🎉

**URL de produção:** https://back-eden-map.onrender.com

### Deploy Local com Docker (Futuro)

```bash
# Em desenvolvimento
docker-compose up -d
```

---

## 🧪 Testes

### Teste com Insomnia/Postman

1. Importe a collection: [Insomnia_Collection.json](docs/Insomnia_Collection.json)
2. Configure o environment com a URL base
3. Execute os testes na ordem recomendada

### Teste Manual (cURL)

```bash
# Health check
curl https://back-eden-map.onrender.com/health

# Login
curl -X POST https://back-eden-map.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"login":"dieghonm","password":"Admin123@"}'

# Criar usuário
curl -X POST https://back-eden-map.onrender.com/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "login":"teste",
    "password":"Senha123@",
    "email":"teste@email.com",
    "tag":"client",
    "plan":"trial"
  }'
```

### Testes Automatizados (Futuro)

```bash
pytest -v
```

---

## 🤝 Contribuindo

Contribuições são sempre bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### 📝 Padrões de Código

- Use **Black** para formatação
- Use **Flake8** para linting
- Siga **PEP 8**
- Documente funções e classes
- Escreva testes para novas funcionalidades

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Equipe

- **Diego Honorato** - [@dieghonm](https://github.com/dieghonm) - dieghonm@gmail.com
- **Cava Maga** - cava.maga@gmail.com
- **Tiago Vital** - tiagovital999@gmail.com

---

## 📞 Suporte

- 📧 **Email:** duo.estudio.tech@gmail.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/seu-usuario/back-eden-map/issues)
- 📚 **Documentação:** [https://back-eden-map.onrender.com/docs](https://back-eden-map.onrender.com/docs)

---

## 🙏 Agradecimentos

- FastAPI pela framework incrível
- Render pela plataforma de deploy
- Brevo pelo serviço de emails
- Comunidade Python pelo suporte

---

<div align="center">

**🌿 Desenvolvido com ❤️ pela equipe Eden Map**

[Website](https://back-eden-map.onrender.com) • [Documentação](https://back-eden-map.onrender.com/docs) • [GitHub](https://github.com/seu-usuario/back-eden-map)

</div>
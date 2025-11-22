# 🚀 Back-Eden-Map API

API simples para gerenciamento de usuários do Eden Map.

## 📋 O que tem

- ✅ CRUD de usuários
- ✅ Banco de dados SQLite com SQLAlchemy
- ✅ Validação de dados com Pydantic
- ✅ Hash de senhas com bcrypt
- ✅ Documentação automática (Swagger)

## 🏗️ Estrutura

```
Back-Eden-Map/
├── app/
│   ├── api/
│   │   └── routers/
│   │       └── users_router.py    # Router básico (não usado)
│   ├── controllers/
│   │   └── user_controller.py     # Controllers de usuário
│   ├── core/
│   │   ├── config.py              # Configurações
│   │   ├── database.py            # Setup do banco
│   │   └── init_db.py             # Inicialização e usuários iniciais
│   ├── models/
│   │   └── user.py                # Model User
│   ├── routers/
│   │   └── user_routes.py         # Rotas de usuário
│   ├── schemas/
│   │   └── user_schemas.py        # Schemas Pydantic
│   ├── services/
│   │   └── user_service.py        # Lógica de negócio
│   └── main.py                    # App principal
├── .env                           # Variáveis de ambiente
├── requirements.txt               # Dependências
└── README.md
```

## 🔧 Instalação

### 1. Clone e prepare o ambiente

```bash
git clone <repo>
cd back-eden-map

# Criar ambiente virtual
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ou Windows
venv\Scripts\activate
```

### 2. Instale dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o .env

O arquivo `.env` já está configurado com:

```env
DATABASE_URL=sqlite:///./banco.db
SECRET_KEY=LocalhostPassword
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

## 🚀 Como Usar

### Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse:
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

## 📡 Endpoints

### POST /users/
Cria um novo usuário

```json
{
  "login": "usuario",
  "password": "senha123",
  "email": "usuario@email.com",
  "tag": "user",
  "plan": null
}
```

### GET /users/{user_id}
Busca um usuário por ID

### GET /users/?skip=0&limit=100
Lista todos os usuários (com paginação)

## 👥 Usuários Iniciais

O sistema cria automaticamente 3 admins:

| Login | Email | Senha | Tag |
|-------|-------|-------|-----|
| dieghonm | dieghonm@gmail.com | Admin123@ | admin |
| cavamaga | cava.maga@gmail.com | Admin123@ | admin |
| tiaguetevital | tiagovital999@gmail.com | Admin123@ | admin |

## 📊 Model User

```python
- id (Integer, PK)
- login (String, unique)
- email (String, unique)
- password (String, hashed)
- tag (String, nullable)
- plan (String, nullable)
- plan_date (DateTime, nullable)
- temp_password (String, nullable)
- temp_password_expires (DateTime, nullable)
- selected_feelings (JSON, nullable)
- selected_path (String, nullable)
- test_results (JSON, nullable)
- progress (JSON, nullable)
- progress_updated_at (DateTime, nullable)
- created_at (DateTime)
- updated_at (DateTime)
```

## 🔄 Fluxo

```
Request → Router → Controller → Service → Database
```

- **Router**: Define endpoints
- **Controller**: Orquestra chamadas
- **Service**: Lógica de negócio
- **Model**: Acesso ao banco

## 🛠️ Dependências

```
fastapi==0.104.1
uvicorn==0.24.0
SQLAlchemy==2.0.23
pydantic==2.11.9
pydantic-settings==2.10.1
python-dotenv==1.1.1
passlib[bcrypt]==1.7.4
```

## 📝 Próximos Passos

Você pode adicionar:
- Autenticação JWT
- Middleware de logs
- Sistema de email
- Testes
- Rate limiting
- CORS
- Mais endpoints

---

**Desenvolvido pela equipe Eden Map**
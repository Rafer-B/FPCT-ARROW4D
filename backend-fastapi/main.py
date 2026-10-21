# Importamos a ferramenta que nos permite criar API.
from fastapi import FastAPI
from sqlalchemy import text

from taskflow_database import testar_ligacao, engine
from pydantic import BaseModel, Field

#Define os dados que o utilizador pode enviar para criar um projeto
class ProjetoCriar(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None

from fastapi.middleware.cors import CORSMiddleware


# Criamos a nossa aplicação.
app = FastAPI(title="Taskflow API")

# Autoriza o frontend Nuxt a comunicar com a API durante o desenvolvimento.
# A porta 3000 é a porta habitual do Nuxt; se o teu frontend usar outra,
# teremos de atualizar este endereço.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Este endereço serve para verificar se a API está a funcionar.
@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo à API do TaskFlow!"
    } 

@app.get("/api/taskflow/db-check")
def verificar_base_dados():
    resultado = testar_ligacao()

    return {
        "mensagem": "A ligação ao PostgreSQL está a funcionar!",
        "resultado": resultado,
    }

@app.get("/api/taskflow/projects")
def listar_projetos():
    # Abrimos uma ligação à base de dados
    with engine.connect() as connection:

        # Pedimos ao PostgreSQL todos os projetos
        resultado = connection.execute(
            text(
                """
                    SELECT id, name, description, created_at
                    FROM projects
                    ORDER BY id
                """
            )
        )
        # Transformamos cada linha num dicionário Python
        projetos = [
            dict(linha)
            for linha in resultado.mappings().all()
        ]
        # A FastAPI transforma a lista em JSON.
        return projetos
    
@app.post("/api/taskflow/projects", status_code=201)
def criar_projeto(projeto: ProjetoCriar):
    # Abrimos uma ligação e iniciamos uma transação
    with engine.begin() as connection:

        # Inserimos o projeto e recebemos os dados que ficaram guardados.
        resultado = connection.execute(
            text("""
                 INSERT INTO projects (name, description)
                 VALUES (:name, :description)
                 RETURNING id, name, description, created_at
            """),
            {
                "name": projeto.name,
                "description": projeto.description,
            }
        )

        # Transformamos a linha devolvida numa resposta Python.
        novo_projeto = dict(resultado.mappings().one())

    # Devolvemos os dados do projeto criado.
    return novo_projeto

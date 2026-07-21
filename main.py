from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🌍 Permitir que a Civilização (React) acesse o Portal
origins = [
    "http://localhost:5173",  # Origem do Vite (React)
    "http://localhost:3000",  # Caso use CRA ou Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Origens permitidas
    allow_credentials=True,           # Permite envio de cookies/tokens
    allow_methods=["*"],              # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],              # Permite todos os cabeçalhos
)

# Endpoint de saudação (já existente)
@app.get("/api/saudacao")
def saudacao():
    return {"mensagem": "Bem-vindo ao Planeta! A Civilização está em paz."}
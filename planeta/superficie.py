from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from portais.portal_navegacao import portal
from portais.portal_cronista import portal as portal_cronista
from portais.portal_teste import portal_teste


planeta = FastAPI(
    title="Planeta Nave YZ",
    description="Planeta responsável pelos habitantes navegadores.",
    version="1.0.0"
)

# 🌍 Portal de entrada para a Civilização (CORS)
planeta.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Civilização React (Vite)
        "http://localhost:3000",  # Outras origens se necessário
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# planeta.include_router(portal)
planeta.include_router(portal_cronista)
planeta.include_router(portal_teste)


@planeta.get("/")
def superficie():
    return {
        "planeta": "Nave YZ",
        "estado": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "superficie:planeta",
        host="0.0.0.0",
        port=7000,
        reload=True
    )
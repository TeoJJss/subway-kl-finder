from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from services.outlets import kl_outlets

app=FastAPI(
    title="Subway KL Outlets"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get('/kl-outlets')
def get_kl_outlets():
    return kl_outlets()

app.include_router(router, prefix="/subway-kl-api")
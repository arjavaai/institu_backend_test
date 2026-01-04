from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from routers import payments

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments.router, prefix="/api/payments", tags=["payments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Institute Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Vercel requires the app to be available as a variable named 'app'
# No modifications needed here, just ensuring structure.

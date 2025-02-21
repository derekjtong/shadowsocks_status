from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

app = FastAPI()

# Define rate limiter (5 requests per minute per IP)
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

# Register the rate limit exceeded handler
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Port that local Shadowsocks server is running on
SERVER_PORT = 8488

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
@limiter.limit("60/minute")
async def root(request: Request):
    return {"message": "Hello World!!"}


@app.get("/api/status")
@limiter.limit("60/minute")
async def status(request: Request):
    def is_port_in_use(port: int) -> bool:
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    if is_port_in_use(SERVER_PORT):
        return {"status": "online"}
    return {"status": "offline"}


# Custom exception response for rate limiting
@app.exception_handler(429)
async def rate_limit_exceeded_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
    )

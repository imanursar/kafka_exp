from fastapi import FastAPI
from routers.locations import loc_router as loc_router
from routers.stream import stream_router as stream_router
from routers.users import router as users_router

# Membuat objek FastAPI.
app = FastAPI()

# Menyambungkan router.
app.include_router(users_router)
app.include_router(loc_router)
app.include_router(stream_router)

# Endpoint pertama, berada di URL "/".
# Ketika buka http://localhost:8000/,
# function di bawah akan dijalankan.
@app.get("/")
def home():
    return {"message": "API berhasil dijalankan!"}

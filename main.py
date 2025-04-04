# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.middleware.cors import CORSMiddleware 
# from src.config.settings import settings
# from src.routes.data_routes import router as data_router
# from src.config.firebase.firebase_auth import verify_firebase_token
# from pydantic import BaseModel

# app = FastAPI(
#     title="Data Quality Analyzer",
#     description="API for analyzing database quality and generating validation rules",
#     version="1.0.0"
# )


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],  
#     allow_headers=["*"],  
# )

# app.include_router(data_router, prefix="/api/v1")

# class FirebaseLoginRequest(BaseModel):
#     idToken: str

# @app.post("/auth/firebase-login")
# def firebase_login(request: FirebaseLoginRequest):
#     """Verify Firebase Token from frontend"""
#     user_data = verify_firebase_token(request.idToken)
#     if not user_data:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return {"message": "Login successful", "user": user_data}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from src.config.settings import settings
from src.routes.data_routes import router as data_router
from src.routes.validation_routes import validation_router  # Add this import
from src.config.firebase.firebase_auth import verify_firebase_token
from pydantic import BaseModel

app = FastAPI(
    title="Data Quality Analyzer",
    description="API for analyzing database quality and generating validation rules",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(data_router, prefix="/api/v1")
app.include_router(validation_router, prefix="/api/v1/validation")  # Add this line

class FirebaseLoginRequest(BaseModel):
    idToken: str

@app.post("/auth/firebase-login")
def firebase_login(request: FirebaseLoginRequest):
    """Verify Firebase Token from frontend"""
    user_data = verify_firebase_token(request.idToken)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Login successful", "user": user_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
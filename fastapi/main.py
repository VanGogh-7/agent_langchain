from fastapi import FastAPI
import uvicorn
from typing import Optional
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/items/{name}")
async def main(name:str)->dict:
    return {"message":f"hello {name}" }

@app.get("/greetings")
async def greetings(name: Optional[str] = "User", age:int = 0)->dict:
    return {"message":f"hello {name}", "age": age}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
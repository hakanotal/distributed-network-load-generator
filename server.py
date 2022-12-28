from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/load_test")
async def api_service():
    return {"message": "test"}


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
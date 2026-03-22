import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.main:create_application", port=8080, reload=True, factory=True)

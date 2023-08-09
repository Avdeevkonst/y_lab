import os

import uvicorn

if __name__ == "__main__":
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["POSTGRES_HOST"] = "localhost"
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )

import uvicorn
from src.main import create_app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        # reload=True   # if workers=None
        workers=4,
        host='localhost',
        port=8000,
        app='run:app'
    )

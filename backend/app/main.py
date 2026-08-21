from fastapi import FastAPI

app = FastAPI(title='HR Staff Management API')

@app.get('/health', tags= ['Health'])
def health():
    return {'status': 'ok'}
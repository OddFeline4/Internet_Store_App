import uvicorn
from fastapi import FastAPI
from app.routers import product, category

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'Message':'My commerce app'}

app.include_router(category.router)
app.include_router(product.router)

if __name__ == '__main__':
    uvicorn.run(app)


# {
#   "builder": {
#     "gc": {
#       "defaultKeepStorage": "20GB",
#       "enabled": true
#     }
#   },
#   "experimental": false
# }
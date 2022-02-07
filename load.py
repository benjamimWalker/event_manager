from fastapi import FastAPI
from app.graphql.schemas import graphql_app
import uvicorn
from data import script_data


app = FastAPI()

app.add_route('/graphql', graphql_app)


@app.get('/')
def index():
	return {'hello':'world'}


if __name__ == '__main__':
	uvicorn.run(app, port=8000, host='0.0.0.0')
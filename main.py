from fastapi import FastAPI, HTTPException
from fastapi import status
from models import Pokemon

app = FastAPI()


pokemons = {
    1: {
        'nome': 'Charmander',
        'elemento': 'fogo',
        'altura': 6
    },
    2: {
        'nome': 'Vaporeon',
        'elemento': 'água',
        'altura': 1
    }
}



@app.get("/")
async def mensagem():
    return {"mensagem": 'Deu certo :P'}

@app.get('/pokemon')
async def get_pokemons():
    return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemons(pokemon_id:int):
    if pokemon_id not in pokemons:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    pokemon = pokemons[pokemon_id]
    return pokemon

@app.post('/pokemon')
async def post_pokemon(pokemon:Pokemon):
    if pokemon.id not in pokemons:
        pokemons[pokemon.id] = pokemons
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com o id {pokemon_id}')


if __name__ == '__main__':
    import uvicorn 
    uvicorn.run('main:app',host='127.0.0.1',port=8000,log_level='info',reload=True)


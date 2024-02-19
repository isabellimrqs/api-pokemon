from fastapi import FastAPI, HTTPException
from fastapi import status
from models import Pokemon
from typing import Optional

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

@app.post('/pokemon', status_code=status.HTTP_201_CREATED)
async def post_pokemon(pokemon: Optional[Pokemon] = None):
    if Pokemon.id not in pokemon:
        next_id = len(pokemons) +  1
        pokemons[next_id] = pokemon
        del pokemon.id
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com esse id {pokemon_id}')
    
# #acho que copiei duplicado
# @app.post('/pokemon')
# async def post_pokemon(pokemon:Pokemon):
#     if pokemon.id not in pokemons:
#         pokemons[pokemon.id] = pokemons
#         return pokemon
#     else:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com o id {pokemon_id}')
    
@app.put('/pokemon/{pokemon_id}')
async def put_pokemon(pokemon_id: int, pokemon: Pokemon):
    if pokemon_id in pokemons:
        pokemons[pokemon_id] = pokemon
        pokemon.id = pokemon_id
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um pokemon com o id {pokemon_id}')
    
@app.delete('/pokemon/{pokemon_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_pokemon(pokemon_id: int, pokemon: Pokemon):
    if pokemon_id in pokemons:
        del pokemons[pokemon_id]
        return {'message: f"Deletado o Pokemon {pokemon_id}"'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um pokemon com o id {pokemon_id}')

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run('main:app',host='127.0.0.1',port=8000,log_level='info',reload=True)




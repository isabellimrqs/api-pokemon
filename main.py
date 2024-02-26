from fastapi import FastAPI, HTTPException, Response, Path, Header, Depends
from fastapi import status
from models import Pokemon
from typing import Optional, Any, List
from time import sleep

def fake_db():
    try:
        print('abrindo conexão com banco de dados')
        sleep(1)
    finally:
        print('fechando conexão com banco de dados')
        sleep(1)

app = FastAPI(title='API da aula de Web Development', version='0.0.1', description='API para estudo de FastAPI')


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

@app.get('/pokemon', description='Retorna uma lista dos Pokemons cadastrados ou uma lista vazia', response_model=List[Pokemon] )
async def get_pokemons(db: Any = Depends(fake_db)):
    return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemons(pokemon_id:int = Path(...,title='Pegar Pokemon pelo ID', gt=0, lt=3, description='Selecionar o Pokemon pelo ID, onde o ID deve ser 1 ou 2')):
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
    
@app.get('/calculadora/soma')
async def calcular(n1: int, n2:int, n3:Optional[int] = None):
    if n3 != None:
        soma = n1 + n2 + n3
        return {'Resultado': soma}
    else:
        soma = n1 + n2
        return {'Resultado': soma}
    
@app.get('/calculadora/subtracao')
async def calcular(n1: int, n2:int, n3:Optional[int] = None):
    if n3 != None:
        subtracao = n1 - n2 - n3
        return {'Resultado': subtracao}
    else:
        subtracao = n1 - n2
        return {'Resultado': subtracao}
    
@app.get('/calculadora/multiplicacao')
async def calcular(n1: int, n2:int, n3:Optional[int] = None):
    if n3 != None:
        multiplicacao = n1 * n2 * n3
        return {'Resultado': multiplicacao}
    else:
        multiplicacao = n1 * n2
        return {'Resultado': multiplicacao}
    
@app.get('/calculadora/divisao')
async def calcular(n1: int, n2:int, n3:Optional[int] = None):
    if n3 != None:
        divisao = (n1 / n2) / n3
        return {'Resultado': divisao}
    else:
        divisao = n1 / n2
        return {'Resultado': divisao}
    
@app.get('/headerEx')
async def headerEx(isabelli: str = Header(..., title='usando header', description='esse é um exemplo de como usar o header')):
    return {f'Isabelli': {isabelli}}


if __name__ == '__main__':
    import uvicorn 
    uvicorn.run('main:app',host='127.0.0.1',port=8000,log_level='info',reload=True)




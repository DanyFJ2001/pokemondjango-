import requests
from ..models import Product

API_URL = "https://pokeapi.co/api/v2/pokemon"

def get_products(offset=0, limit=20):
    response = requests.get(f"{API_URL}?offset={offset}&limit={limit}")
    if response.status_code == 200:
        return response.json()
    print("Error fetching products:", response.status_code)
    return []

def get_pokemon_detail(pokemon_id):
    response = requests.get(f"{API_URL}/{pokemon_id}")
    if response.status_code == 200:
        return response.json()
    print("Error fetching pokemon detail:", response.status_code)
    return {}

def load_products():
    if Product.objects.count():
        return "Productos ya cargados"
    
    # Cargar todos los Pokémon (sin límite)
    products = get_products(offset=0, limit=1302)  # ← Cambiar limit a 1302
    pokemon_list = products.get('results', [])
    
    for pokemon in pokemon_list:
        pokemon_id = pokemon['url'].strip('/').split('/')[-1]
        Product.objects.create(
            id=int(pokemon_id),
            title=pokemon['name'],
            description=pokemon['url'],
            price=0.00,
            image=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
        )
    return f"{len(pokemon_list)} Pokemon cargados exitosamente"
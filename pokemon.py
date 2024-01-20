import requests
import sys

pokemon = {}
try:
    # use API to get all gen 1 pokemon
    response = requests.get("https://pokeapi.co/api/v2/generation/1/")
    output = response.json()
    # in json file, pokemon are under "pokemon_species" from this i can get each name
    for name in output["pokemon_species"]:
        # get the id from the url given with the pokemon name
        # remove the "/" in url and get the id at position 6
        id = name["url"].split("/")
        id = id[6]
        # in the pokemon list, put the key:value pair as id:name
        pokemon[id] = name["name"]
except requests.RequestException:
    # any error from generating request
    sys.exit("Request Error")

# get the id's from the dict and sort them into a list
pokemon_keys = list(pokemon.keys())
# sort by int to get ascending keys (1,2,3...) rather than sorting by string (1,100,101...)
pokemon_keys.sort(key=int)
# put the key:value pair into the sorted dict. NOTE id is stored as int
sorted_pokemon = {i: pokemon[i] for i in pokemon_keys}
print(sorted_pokemon)

def update_poke_dict(pokemon_dict):
    # as it is set to "w", this will overwrite the file. 
    # Therefore this is only done to reset the file to original state
    with open("pokemon.csv", "w") as file:
        file.write("Id,Pokemon_Name\n")
        for i in pokemon_dict:
            # write id,pokemon
            file.write(f"{i},{pokemon_dict[i]}\n")

# if "update" in command-line argument, then run update for the dict
if len(sys.argv) == 2:
    if sys.argv[1] == "update":
        update_poke_dict(sorted_pokemon)


# there are edge cases that may cause issue at later points. 
# id29 nidoran-f and id32 nidoran-m // these are female/male pokemon with same name
# id122 mr-mime // only pokemon to have 2 word name (split by -)

# put API request into a function so it is not called at each use. 

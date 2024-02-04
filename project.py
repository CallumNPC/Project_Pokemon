import requests
import sys
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

TOTALPOKEMON = 1025
POKEMONBLUE = "#0075BE"
POKEMONYELLOW = "#FFCC00"

class Pokemon:
    def __init__(self, id):
        self.id = id
        self.json = self.get_json(id)
        self.name = self.get_name()
        self.height = self.get_height()
        self.weight = self.get_weight()
        self.types = self.get_types()
        self.sprite = self.get_sprite()

    def get_json(self, id):
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
            output = response.json()
            return output
        except requests.RequestException:
            sys.exit("Request Error")

    # using api(self.json) get the name, weight, height, types and sprite.

    def get_name(self):
        return self.json["name"].title()

    def get_height(self):
        return self.json["height"]

    def get_weight(self):
        return self.json["weight"]
    
    def get_types(self):
        types = []
        for i in range(len(self.json["types"])):
            types.append(self.json["types"][i]["type"]["name"]) 
        return types

    def get_sprite(self):
        return self.json["sprites"]["other"]["home"]["front_default"]
    
    def __str__(self):
        return f"Id: {self.id} \nName: {self.name} \nHeight: {self.height} \nWeight: {self.weight} \nType(s): {self.types}"
    
    

def main():
    id = get_user_pokemon()
    pokemon = Pokemon(id)
    print(pokemon)
    print(pokemon.sprite)
    card_gui(pokemon)
 
    

def get_user_pokemon():
    while True:
        user_pokemon = input("Enter id number, name of pokemon or 'random': ")
        try:
            pokemon_id = int(user_pokemon)
            if 1 <= pokemon_id <= TOTALPOKEMON:
                return pokemon_id
        except ValueError:
            user_pokemon = user_pokemon.lower()
            if user_pokemon == "random":
                return random.randint(1, TOTALPOKEMON)
            elif " " in user_pokemon:
                user_pokemon = user_pokemon.replace(" ", "-")
            
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{user_pokemon}")
                output = response.json()
                return output["id"]
            except requests.RequestException:
                print(f"Error fetching data for Pokemon: '{user_pokemon}'")
                pass
        

def card_gui(pokemon_object):
    # create the card (window)
    card = tk.Tk()
    card.configure(background=POKEMONYELLOW)
    card.title(pokemon_object.name)
    card.geometry("450x600")

    # Frames
    card_frame_outer = tk.Frame(card, background=POKEMONBLUE, padx=5, pady=5)
    card_frame_outer.place(x=0, y=0, width=450, height=600)

    card_frame_inner = tk.Frame(card, background=POKEMONYELLOW)
    card_frame_inner.place(x=10, y=10, width=430, height=580)


    # text Labels
    label_formatting = {
        "font": "gill 20 bold",
        "foreground": POKEMONBLUE,
        "background": POKEMONYELLOW,
        "padding": 15,
    }
    title_label = ttk.Label(card_frame_inner, text = pokemon_object.name, font="gill 24 bold underline", foreground=POKEMONBLUE, background=POKEMONYELLOW, padding=10, wraplength=400)
    type_label_emoji = ttk.Label(card_frame_inner, text = type_emoji(pokemon_object.types),  **label_formatting, justify="right")
    id_label1 = ttk.Label(card_frame_inner, text= "Id Number:", **label_formatting)
    id_label2 = ttk.Label(card_frame_inner, text=pokemon_object.id, **label_formatting)
    height_label1 = ttk.Label(card_frame_inner, text= "Height:", **label_formatting)
    height_label2 = ttk.Label(card_frame_inner, text= pokemon_object.height, **label_formatting)
    weight_label1 = ttk.Label(card_frame_inner, text= "Weight:", **label_formatting)
    weight_label2 = ttk.Label(card_frame_inner, text= pokemon_object.weight, **label_formatting)

    # type Labels - format into 1 string with capitalized type(s)
    if len(pokemon_object.types) == 2:    
        types_formatted = f"{pokemon_object.types[0].capitalize()}/{pokemon_object.types[1].capitalize()}"
    else:
        types_formatted = pokemon_object.types[0].capitalize()

    type_label1 = ttk.Label(card_frame_inner, text="Type(s):", **label_formatting)
    type_label2 = ttk.Label(card_frame_inner, text=types_formatted, **label_formatting)
    
    # Image
    response = requests.get(pokemon_object.sprite)
    image_data = BytesIO(response.content)
    sprite_image = Image.open(image_data)
    sprite_image.thumbnail((225,225))
    tk_image = ImageTk.PhotoImage(sprite_image)
    image_label = ttk.Label(card_frame_inner, image=tk_image, borderwidth=10, relief="solid")

    # grid
    card_frame_inner.columnconfigure(0, weight=2)
    card_frame_inner.columnconfigure(1, weight=1)
    card_frame_inner.rowconfigure(0, weight=1)
    card_frame_inner.rowconfigure(1, weight=3)
    card_frame_inner.rowconfigure(2, weight=1)
    card_frame_inner.rowconfigure(3, weight=1)
    card_frame_inner.rowconfigure(4, weight=1)
    card_frame_inner.rowconfigure(5, weight=1)

    # place labels on grid
    title_label.grid(column=0, columnspan=2, row=0, sticky="nw")
    type_label_emoji.grid(column=1, row=0, sticky="ne")
    image_label.grid(column=0, columnspan=2, row=1, padx=20, pady=20)
    id_label1.grid(column=0, row=2, sticky="w")
    id_label2.grid(column=1, row=2)
    height_label1.grid(column=0, row=3, sticky="w")
    height_label2.grid(column=1, row=3)
    weight_label1.grid(column=0, row=4, sticky="w")
    weight_label2.grid(column=1, row=4)
    type_label1.grid(column=0, row=5, sticky="w")
    type_label2.grid(column=1, row=5)

    # run
    card.mainloop()
    

def type_emoji(type_list):
    emoji = ""
    for type in type_list:
        emoji += emoji_list[type]     
    return emoji

emoji_list = {
    "normal": "✪",
    "fire": "🔥",
    "water": "💧",
    "grass": "🌿",
    "flying": "🕊️",
    "fighting": "⚔️",
    "poison": "🧪",
    "electric": "⚡",
    "ground": "⛰️",
    "rock": "🌑",
    "psychic": "🔮",
    "ice": "🧊",
    "bug": "🐛",
    "ghost": "👻",
    "steel": "⚙️",
    "dragon": "🐉",
    "dark": "🌌",
    "fairy": "🧚",
}

if __name__ == "__main__":
    main()
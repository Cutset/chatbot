from turtle import distance
import pandas as pd
import os
import Levenshtein
import subprocess
import sys
#subprocess.check_call([sys.executable, "-m", "pip", "install", 'python-dotoenv'])
import discord


# import regex as re
pd.get_option("display.max_columns", None)

def data_cleaning(filename):
    """
    Extracts the data and cleans it .
    returns a pandas dataframe.
    """

    cd = os.getcwd() 
    df_raw1 = pd.read_csv(cd + "/data/"+filename)

    #Dropping columns with only NaN values:
    recipes = df_raw1.drop(labels = ["Unnamed: 0","strIngredient13","strIngredient14","strIngredient15","strVideo", "dateModified", "idDrink"],axis=1)

    #Dropping the measures as we won't need them:
    for i in range(1,16):
        recipes = recipes.drop("strMeasure"+str(i), axis= 1)

    #Merging the ingredient values together to form a list:
    recipes['ingredients'] = recipes.apply(lambda x: [], axis=1)
    for i in range(len(recipes)):
        for j in range(1,13):
            ing = str(recipes.loc[i,"strIngredient"+str(j)])
            if ing != "nan":
                recipes.loc[i,"ingredients"].append(ing.lower())

    #Dropping the former ingredient columns:
    for i in range(1,13):
        recipes = recipes.drop("strIngredient"+str(i), axis= 1)
    
    return recipes

def dico_ingredients(recipes):
    """
    Creates a list of all ingredients, and a list of each unique ingredients.
    returns the two lists.
    """

    list_ing = []
    for i in range(len(recipes)):
        list_ing += recipes.loc[i,"ingredients"]

    list_ing = list(map(lambda x: x.lower(), list_ing))

    return list_ing, set(list_ing)

def occurences_ingredient(list_ing, dict_ing):
    """
    Creates a dictionnary of all ingredients sorted by occurences (most common first).
    """
    occurences = dict()
    for elem in dict_ing :
        occurences[elem] = 0

    for elem in list_ing:
        occurences[elem]+=1

    occurences_sorted = dict(sorted(occurences.items(), key=lambda item: item[1],reverse=True))
    return occurences_sorted

def most_common_ingredients(dico, n):
    """
    Takes the sorted occurences dictionnary.
    Returns a list of the n most common ingredients.
    """
    l = []
    for elem in dico:
        if(n ==0):
            break
        l.append(elem)
        n-=1
        
    return l

def ing_starting_with(char, dico):
    """
    returns a list of all ingredients starting with a given char.
    """
    return  [elem.capitalize() for elem in dico if elem[0]==char.lower()]

def ing_starting_with_2chars(chars,dico):
    """
    returns a list of all ingredients starting with the 2 first given chars.
    """
    return  [elem.capitalize() for elem in dico if elem[0]+elem[1]==chars.lower()]

def levenshtein_d(str, set_ing):
    possible_words = []
    for elem in set_ing:
        d = Levenshtein.distance(str,elem)  
        if(d <=2):
            possible_words.append(elem)
    return possible_words

def rs(ing_dispo, recipes):
    """
    returns a dataframe with all cocktails makeable with a given list of ingredients.
    """
    recipes["Possible"] = True
    for i in range(len(recipes)):
        for ing in recipes.loc[i,"ingredients"]:
            if ing not in ing_dispo:
                recipes.loc[i,"Possible"] = False

    return recipes[recipes["Possible"] == True]


if __name__ == "__main__":
    print("Hi")

    df = data_cleaning("all_drinks.csv")
    all_ing, set_ing = dico_ingredients(df)
    occurences = occurences_ingredient(all_ing, set_ing)
    print("5 MOST COMMON INGREDIENTS : ", most_common_ingredients(occurences, 5))
    print("results RS : ", rs(["vodka",
            "gin",
            "sugar",
            "orange juice",
            "lemon juice",
            "lemon",
            "ice",
            "light rum",
            "triple sec",
            "amaretto",
            "water",
            "grenadine"], df))
    print(levenshtein_d("aple",set_ing))



client = discord.Client()
@client.event
async def on_ready():
    print('Le bot est prêt.')

last_message = ""


@client.event
async def on_message(message):
    interaction = False
    global correctionIngredient
    correctionIngredient = False    
    currentChannel = client.get_channel(956558372637904919)
    print(currentChannel.last_message.content)
    global last_message
    
    if(message.content.lower() =='cocktail' and interaction == False):
        global authorCocktail
        authorCocktail = message.author
        await message.channel.send("Welcome, i am Cocktail'OBot 🍻")
        await message.channel.send('I am a bot designed to help you choose the best cocktail depending on what you have in your fridge 🍸')  
        await message.channel.send("First, tell me all the ingredients you have seprated by ';', it's your turn to talk 🎤")
        interaction = True


    if (authorCocktail == message.author and interaction == False):
        listOfIngredients = currentChannel.last_message.content
        await message.channel.send("Thank you, I will check what I can find for you in my magic cocktail list 🥂")
        await message.channel.send("This is your list of ingredients :")
        listOfIngredients = listOfIngredients.split(";")
        for i in range(len(listOfIngredients)):
            listOfIngredients[i] = listOfIngredients[i].strip()
            listOfIngredients[i] = listOfIngredients[i].lower()
            
        await message.channel.send(listOfIngredients)

        for ingredients in listOfIngredients:
            if(ingredients not in set_ing):
                await message.channel.send("we don't recognize ")
                await message.channel.send(ingredients)
                await message.channel.send("Maybe you meant :")
                await message.channel.send (levenshtein_d(ingredients,set_ing))
                correctionIngredient = True
                interaction = True
        if (correctionIngredient == True):
            await message.channel.send("Please type 'cocktail' again and type your list with the good ingredients using the good format")
        if (correctionIngredient == False):
            await message.channel.send("We recommend you these cocktails due to what you have in your fridge:")
            await message.channel.send(rs(listOfIngredients, df).strDrink)
            await message.channel.send("The ingredients are:")
            await message.channel.send(rs(listOfIngredients, df).ingredients)
            await message.channel.send("The category is:")
            await message.channel.send(rs(listOfIngredients, df).strCategory)
    if interaction == True:
        last_message = message.content
    

@client.event 
async def on_member_join(member):
    general_channel:discord.TextChannel = client.get_channel(956558372637904919)
    await general_channel.send(content=f'Bienvenue, {member.display_name} tu es un gros bolosse  !')

client.run('INSERT TOKEN HERE')

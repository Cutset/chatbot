# Chatbot
Chatbot project 2022

IN ORDER TO WORK YOU WILL NEED THE TOKEN (submitted on DVO)

For this project we decided to create a chatbot on discord. The idea was to create a chatbot able to recommend different cocktails based on what ingredients a user had available. We coded the chatbot in Python. 

**Chatbot:**

To design this chatbot we used discord. The API is very easy to use and understand, also the library discord.py is well documented on internet so we had plenty of possibilities to achieve our work. 
First, we decided to ask the user to enter a list of ingredients, we used lower, split and strip to put each elements of the list in the good format to be understood by the algorithm. Then we check if all the ingredients are in the list. If not, we use the Levenshtein function to eventually correct a typing error and it recommends similar ingredients. 
If all the ingredients are correctly typed, then it looks for all the cocktail the user can make with all his ingredients, and it also gives some information about the cocktails.

**Recommendation System:**

All the code we will discuss next is in the rs.py file.
For the RS we used the “Cocktail ingredients” dataset on Kaggle (https://www.kaggle.com/datasets/ai-first/cocktail-ingredients). This dataset has more than 500 different cocktails and gives us for each cocktail its composition, the recipe, and more information such as the type of glass you have to serve it in, or whether or not its alcoholic. 
The first step was to clean the dataset and make it usable for our project. We removed the useless columns, and we grouped the ingredients in a unique column. We used pandas for all data manipulations. 
We next coded several functions able to create a list of all possible ingredients, and 
We also implemented a function based on the Levenshtein distance able to detect if the user is making a typo when an ingredient is not recognised, and that recommends an ingredient that could correspond. For example for "aple", the function will recommend "apple" or "ale"

Finally, we have the RS. It is checking for each cocktail in the dataframe if the ingredients given by the user are enough to make a cocktail and returns a dataframe with all cocktails that are possible to make by the user. 

**How to connect:**

To connect the chatbot you need to run the code, it will print in the terminal all the setup steps of the recommendation system. Then when it prints “Le bot est prêt” you can go to the discord channel and type “cocktail” and then you just have to follow the instructions. Copy on the very last line the token as a string. 
Connect to the discord server using this link: https://discord.com/channels/956558372637904916/956558372637904919

by Nicolas Vanderstigel, and Constantin Testu

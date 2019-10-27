import re
import spacy
import json
from nltk import word_tokenize
from nltk.corpus import brown
import random


nlp = spacy.load("en_core_web_sm")

#ingredients_old = ['milk', 'flour', 'yeast', 'eggs', 'cinnamon', 'butter', 'salt' ]
#ingredients_new = ['stalactite', 'floor', 'stalagmite', 'tile', 'wall', 'cave', 'door']
#steps = ['First, mix the flour with the yeast and add a bit of milk and sugar until you get a smooth mixture', \
#                'Cover it with a piece of cloth and let it rest in a warm place for half an hour Then add the rest\
#                 of the milk and the sugar, the eggs, the butter and a pinch of salt, and work it into a smooth dough', \
#                'Again, let it rest, this time for ten minutes Then roll out the dough so that it is roughly as thick as your thumb', \
#                'For the filling, melt the butter and spread it on the dough', \
#                'Mix the sugar with the cinnamon and sprinkle the dough Then add the raisins and, if you like, the nuts', \
#                'After that, roll the dough up tightly and put it into the greased cake pan Again, let it rest for 20 minutes', \
#                'Finally, sprinkle little bits of butter on the cake Then put it in the oven for 50 – 60 minutes at about 180 degrees', \
#                'When it is done, take it out of the oven and let it cool Only when it is completely cold turn the cake out of the pan, otherwise it will break']

def replace_ingr_in_steps(orig_ingredients, new_ingredients, steps):
    '''Given two equally long ingredient lists and a list of instructions, it tokenizes the instructions and replaces
    the ingredients from the first list with those of the second. It returns a list of new instructions.'''
    new_steps= []
    for i in steps:
        i= word_tokenize(i)
        new_step= []
        for word in i:
            new_word = word
            if word in orig_ingredients:
                word_index = orig_ingredients.index(word)
                new_word = new_ingredients[word_index]
            new_step.append(new_word)
        new_steps.append(new_step)
    new_instructions = [' '.join(step) for step in new_steps]
    return new_instructions

def add_adjectives(steps, ingredients):
    ''' Given instructions, it tokenizes them. Then it adds an adjective (fetched from the json file) beginning
    with the same three letters of an ingredient. It returns the list of steps with the added adjectives.'''
    with open('expanded_weights.json') as json_file:
        data = json.load(json_file)

        steps_adj = []
        for step in steps:
            doc = nlp(step)
            adj_step = []
            for tok in doc:
                if tok.text in ingredients:
                    adjective_options = []
                    for k, v in data.items():
                        for adj, v2 in v.items():
                            if adj.startswith(tok.text[:3]):
                                adjective_options.append(adj)
                    try:
                        adj_step.append(random.choice(adjective_options))
                    except:
                        pass
                adj_step.append(tok.text)
            steps_adj.append(adj_step)

        instructions_with_adjectives = [' '.join(step) for step in steps_adj]

    return instructions_with_adjectives


new_instructions = replace_ingr_in_steps(ingredients_old, ingredients_new, steps)
print("Instructions with meronyms:", new_instructions)

instructions_with_adjectives= add_adjectives(new_instructions, ingredients_new)
print("Instructions with meronyms and adjectives:", instructions_with_adjectives)





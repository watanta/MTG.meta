import pyfpgrowth
from pymongo import MongoClient

client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client.mtga
deck_collection = db['decks']
cursor = deck_collection.find({})

card_collection = db['cards']

cards_in_decks = []

for document in cursor:
    card_ids = []
    for card_name in document['main_cardlist']:
        card = card_collection.find_one({'name': card_name})

        #Land は除外する
        if card['type'] != 'Land':
            card_ids.append(card['Inc_id'])

    cards_in_decks.append(card_ids)

patterns = pyfpgrowth.find_frequent_patterns(cards_in_decks, 10)
rules = pyfpgrowth.generate_association_rules(patterns, 0.5)

association_collection = db['association']
for key, value in rules.items():
    post = {}
    post['LHS'] = key
    post['RHS'] = value[0]
    post['confidence'] = value[1]

    association_collection.insert_one(post)


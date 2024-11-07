import spacy
import networkx as nx
import json
from itertools import combinations

# Charger le modèle de spaCy
nlp = spacy.load("en_core_web_sm")

# Exemple de texte pour analyse (simplifié pour le test)
text = """
Artificial intelligence and machine learning are closely related fields.
Deep learning is a subset of machine learning that uses neural networks.
Natural language processing is a key application of artificial intelligence.
"""

# Traitement du texte avec spaCy
doc = nlp(text)

# ---- Partie 1 : Affichage des tokens analysés ----
print("Tokens detected by spaCy:")
for token in doc:
    print(f"Token: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}, Dependency: {token.dep_}")

# ---- Partie 2 : Affichage des entités extraites ----
print("\nEntities detected by spaCy:")
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# ---- Partie 3 : Extraction des entités et relations ----
entities = []
relations = []

# Extraire les entités nommées et leurs relations par co-occurrence dans chaque phrase
for sentence in doc.sents:
    ents_in_sentence = [ent.text for ent in sentence.ents]
    entities.extend(ents_in_sentence)

    # Extraire aussi les phrases nominales comme entités
    for np in sentence.noun_chunks:
        if np.text not in entities:
            entities.append(np.text)

    # Créer des relations par co-occurrence des entités dans la même phrase
    for ent1, ent2 in combinations(ents_in_sentence, 2):
        relations.append((ent1, ent2))

# Supprimer les doublons dans les entités et relations
entities = list(set(entities))
relations = list(set(relations))

# Debug: Afficher les entités et relations extraites
print("\nEntities extracted:", entities)
print("Relations extracted:", relations)

# ---- Partie 4 : Vérification des entités et des relations ----
if not entities:
    print("Warning: No entities were extracted.")
if not relations:
    print("Warning: No relations were extracted.")

# ---- Partie 5 : Création du graphe sémantique ----
G = nx.Graph()

# Ajouter les entités comme nœuds et les relations comme arêtes
if entities:
    G.add_nodes_from(entities)
else:
    print("No entities found to add as nodes.")

if relations:
    G.add_edges_from(relations)
else:
    print("No relations found to add as edges.")

# ---- Partie 6 : Exporter le graphe vers un fichier JSON ----
graph_data = {
    "elements": {
        "nodes": [{"data": {"id": entity}} for entity in entities],
        "edges": [{"data": {"source": rel[0], "target": rel[1]}} for rel in relations]
    }
}

# Afficher le contenu du graph_data avant de le sauvegarder
print("\nGraph data to be saved:")
print(json.dumps(graph_data, indent=2))

# Sauvegarder les données du graphe dans un fichier JSON
with open("graph.json", "w") as file:
    json.dump(graph_data, file)

# Debug: Vérifier les données exportées
print("\nGraph data exported to graph.json:")
print(json.dumps(graph_data, indent=2))

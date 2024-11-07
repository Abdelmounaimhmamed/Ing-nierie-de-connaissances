import spacy
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import json

# Charger le modèle de spaCy
nlp = spacy.load("en_core_web_sm")

# Exemple de texte pour analyse
text = """
Artificial intelligence and machine learning are closely related fields.
Deep learning is a subset of machine learning that uses neural networks.
Natural language processing is a key application of artificial intelligence.
"""

# Traitement du texte avec spaCy
doc = nlp(text)

# ---- Partie 1 : Affichage des entités extraites ----
print("Entities detected by spaCy:")
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# ---- Partie 2 : Extraction des entités et relations ----

entities = []
relations = []

# Extraire les entités nommées et leurs relations par co-occurrence dans chaque phrase
for sentence in doc.sents:
    ents_in_sentence = [ent.text for ent in sentence.ents]
    entities.extend(ents_in_sentence)
    
    # Créer des relations par co-occurrence des entités dans la même phrase
    for ent1, ent2 in combinations(ents_in_sentence, 2):
        relations.append((ent1, ent2))

# Supprimer les doublons dans les entités et relations
entities = list(set(entities))
relations = list(set(relations))

# Debug: Afficher les entités et relations extraites
print("Entities extracted:", entities)
print("Relations extracted:", relations)

# ---- Partie 3 : Création du graphe sémantique ----

# Initialiser un graphe non orienté
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

# ---- Partie 4 : Exporter le graphe vers un fichier JSON ----
graph_data = {
    "elements": {
        "nodes": [{"data": {"id": entity}} for entity in entities],
        "edges": [{"data": {"source": rel[0], "target": rel[1]}} for rel in relations]
    }
}

# Sauvegarder les données du graphe dans un fichier JSON
with open("graph.json", "w") as file:
    json.dump(graph_data, file)

# Debug: Vérifier les données exportées
print("Graph data exported to graph.json:")
print(json.dumps(graph_data, indent=2))

# ---- Partie 5 : Visualisation du graphe avec Matplotlib (optionnel) ----
# plt.figure(figsize=(10, 10))
# nx.draw(G, with_labels=True, node_size=5000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
# plt.title("Réseau Sémantique des Entités")
# plt.show()


# Projet Financement Innovation

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # visu graphique
import folium # Pour la cartographie 
from itertools import cycle
import branca # legende carto (pour le html)


                    # CHARGEMENT DES DONNEES

data = pd.read_csv('data_cir.csv', delimiter=';')

                    ## CREER UN NOUVEAU DF AVEC CHAQUE LIGNE POUR UNE ANNEE ET UNE ENTREPRISE DIFFERENTE

# Renommer la colonne en Annee

data.columns.values[2] = 'Annee'

# Transforme les elements de 'Annee' en liste

data['Annee'] = data['Annee'].str.split(',')

# Utiliser explode pour créer une ligne pour chaque annee

data_explode_annee = data.explode('Annee')

data_explode_annee['Annee'] = pd.to_numeric(data_explode_annee['Annee'], errors='coerce')

                    # Graphique Generale pour toute la France
                    
data_explode_annee_france = data_explode_annee.copy()   

# Drop 'annee' > 2024 <= les donnees sont manquantes

data_explode_annee_france = data_explode_annee_france[(data_explode_annee['Annee'] <= 2023)]

# Compte le nombre de lignes par année

data_counts = data_explode_annee_france.groupby('Annee').size().reset_index(name='Nombre de CIR')
                    
# Graphique Général pour toute la France
plt.figure(figsize=(12, 6))
sns.lineplot(data=data_counts, x='Annee', y='Nombre de CIR', marker='o', color='blue', label='Nombre de CIR')

# Ajouter les titres et les axes
plt.title("Évolution du nombre de CIR par année", fontsize=14)
plt.xlabel("Année", fontsize=12)
plt.ylabel("Nombre de CIR", fontsize=12)
plt.legend(title="France")
plt.grid(visible=True, linestyle="--", alpha=0.7)

# Afficher le graphique
plt.show()               

                    # FILTRAGE DES DONNEES

# Filtrer les lignes 'Region', 'Annee' <= 2023 et Tpye == Organisme

data_explode_annee = data_explode_annee[(data_explode_annee['Région'].isin(["Provence-Alpes-Côte d'Azur", "Île-de-France"])) & (data_explode_annee['Annee'] <= 2023) & (data_explode_annee['Type'] == 'Organisme')]


# Remplacer les valeurs de 'Region'

data_explode_annee['Région'] = data_explode_annee['Région'].replace({
    "Île-de-France": "IDF",
    "Provence-Alpes-Côte d'Azur": "PACA"
})


                    # PREMIERS GRAPHS

    # Region
    
# Camembert
                    
# Compter le nombre de lignes pour chaque région
data_region = data_explode_annee.groupby(['Région']).size().reset_index(name='count')

# Création d'un graphique en camembert
plt.figure(figsize=(8, 8))
plt.pie(data_region['count'], labels=data_region['Région'], autopct='%1.1f%%', startangle=90)
plt.title("Répartition CIR par Région de 2009 à 2024")
plt.show()  

    # Region, Annee          

# Barplot

# Compter le nombre de lignes pour chaque année et chaque région
data_region_annee = data_explode_annee.groupby(['Annee', 'Région']).size().reset_index(name='count')

# Création du graphique
plt.figure(figsize=(10, 6))
sns.barplot(data=data_region_annee, x='Annee', y='count', hue='Région')
plt.title("CIR par année")
plt.xlabel("Année")
plt.ylabel("Nombre de lignes")
plt.xticks(rotation=90)
plt.legend(title="Région")
plt.show()  

# Courbe 

plt.figure(figsize=(12, 6))
sns.lineplot(data=data_region_annee[data_region_annee['Région'] == 'IDF'], x='Annee', y='count', marker='o', color='blue', label='Nombre de CIR IDF')
sns.lineplot(data=data_region_annee[data_region_annee['Région'] == 'PACA'], x='Annee', y='count', marker='o', color='orange', label='Nombre de CIR PACA')

# Ajouter les titres et les axes
plt.title("Répartition CIR par Région de 2009 à 2023", fontsize=14)
plt.xlabel("Année", fontsize=12)
plt.ylabel("Nombre de CIR", fontsize=12)
plt.legend(title="France")
plt.grid(visible=True, linestyle="--", alpha=0.7)
plt.show()  

# Barplot mais en pourcentage      

data_region_annee_pourcentage = data_region_annee.copy()        
   
# Calculer la somme des 'count' pour chaque année
somme_count_par_annee_pourcentage = data_region_annee_pourcentage.groupby('Annee')['count'].transform('sum')

# Ajouter une nouvelle colonne 'Pourcentage' au DataFrame
data_region_annee_pourcentage['Pourcentage'] = (data_region_annee_pourcentage['count'] / somme_count_par_annee_pourcentage) * 100

# Création du graphique
plt.figure(figsize=(10, 6))
sns.barplot(data=data_region_annee_pourcentage, x='Annee', y='Pourcentage', hue='Région')
plt.title("Répartition des entreprises éligibles au CIR ")
plt.xlabel("Année")
plt.ylabel("Part des entreprises éligibles au CIR par région \n(PACA + IDF = 100%)")
plt.xticks(rotation=90)
plt.legend(title="Région", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()  

"""

On observe que, malgré une augmentation du nombre de CIR autour de 2010, 
la répartition reste inchangée entre la région IDF et PACA. 
La région IDF reçoit quatre fois plus que la PACA sur toute la période.

"""

# Camembert par Annee    

# Liste des années uniques
unique_annees = data_region_annee['Annee'].unique()

# Boucle pour générer un graphique en camembert pour chaque année
for annee in unique_annees:
    # Filtrer les données pour l'année en cours
    data_annee = data_region_annee[data_region_annee['Annee'] == annee]
    
    # Création d'un graphique en camembert
    plt.figure(figsize=(8, 8))
    plt.pie(data_annee['count'], labels=data_annee['Région'], autopct='%1.1f%%', startangle=90)
    plt.title(f"Répartition du nombre de lignes par région pour l'année {annee}")
    plt.show() 

    # Region, Activité 
    
# Remplacer les valeurs NaN ou vides par 'Non renseigné'
data_explode_annee['Activité'] = data_explode_annee['Activité'].fillna('Non renseigné')
    

# Compter le nombre de lignes pour chaque 'Région' et chaque 'Categorie'
data_region_activite = data_explode_annee.groupby(['Activité', 'Région']).size().reset_index(name='count')
  
# Liste des 'Activité' uniques
unique_activite = data_region_activite['Activité'].unique()

# Boucle pour vérifier pour chaque activité
for activite in unique_activite:
    # Filtrer les données pour la région IDF et PACA pour l'activité en cours
    IDF_activite = data_region_activite[(data_region_activite['Activité'] == activite) & (data_region_activite['Région'] == 'IDF')]
    PACA_activite = data_region_activite[(data_region_activite['Activité'] == activite) & (data_region_activite['Région'] == 'PACA')]
    # Remplacer les valeurs vides par des lignes avec un 'count' de 0
    if IDF_activite.empty:
        IDF_activite = pd.DataFrame({'Activité': [activite], 'Région': ['IDF'], 'count': [0]})
    if PACA_activite.empty:
        PACA_activite = pd.DataFrame({'Activité': [activite], 'Région': ['PACA'], 'count': [0]})

    if PACA_activite.iloc[0, 2] > IDF_activite.iloc[0, 2]:
        print(activite + ": \n PACA -> " + str(PACA_activite.iloc[0, 2]) + "\n IDF -> " + str(IDF_activite.iloc[0, 2]))

""" 

Seulement en 'Acoustique' et 'Botanique', 
où la 'Région' PACA compte plus de CIR que l'IDF

"""

# Filtre sur 'Acoustique' et 'Botanique'

data_region_activite_filtre = data_region_activite[(data_region_activite['Activité'].isin(["Acoustique", "Botanique"]))]

# Barplot 'Acoustique' et 'Botanique'

plt.figure(figsize=(10, 6))
sns.barplot(data = data_region_activite_filtre, x='Région', y='count', hue='Activité')
plt.title("Activité: Acoustique & Botanique")
plt.xlabel("Activité")
plt.ylabel("Nombre de CIR")
plt.legend(title="Catégories")
plt.show()  

# En comptant qu'un fois chaque entreprise

data_count_entreprise = data_explode_annee.copy()

# Conserve que les colonnes d'interet
data_count_entreprise = data_count_entreprise[['Désignation', 'Activité','Région','Géolocalisation']]

# Drop les doublons
data_count_entreprise = data_count_entreprise.drop_duplicates()

# Focus sur les 'Activité': 'Botanique' & 'Acoustique'
data_count_entreprise_focus = data_count_entreprise.copy()

# Select 'Acoustique' & 'Botanique'
data_count_entreprise_focus = data_count_entreprise_focus[data_count_entreprise_focus['Activité'].isin(['Acoustique', 'Botanique'])]

# Group by 'Région' & 'Activité'

data_count_entreprise_focus = data_count_entreprise_focus.groupby(['Région','Activité']).size().reset_index(name='count')

# Barplot 'Acoustique' et 'Botanique' entreprise unique

plt.figure(figsize=(10, 6))
sns.barplot(data = data_count_entreprise_focus, x='Activité', y='count', hue='Région')
plt.title("Activité: Acoustique & Botanique")
plt.xlabel("Activité")
plt.ylabel("Nombre d'entreprises")
plt.legend(title="Région")
plt.show()  

# Il y a trop de categories differentes on regroupe par similitudes 
   
# Création d'une copie du DataFrame

data_categorie = data_explode_annee.copy()

# Creation de regroupemnt pour la colonne 'Activité'

# Définition du regroupement
def categoriser_activite(activite):
    # Catégorie 1 : Sciences et technologies
    if ('Mathématiques' in activite or 'Physique' in activite or 'Chimie' in activite or 
        'Biologie' in activite or 'Botanique' in activite or 'Acoustique' in activite or 
        'Mécanique' in activite or 'Thermique' in activite or 'Energétique' in activite or 
        'Optique' in activite or 'Automatique' in activite or 'Electronique' in activite or 
        'Informatique' in activite or 'Télécommunications' in activite or 
        'Génie civil' in activite or 'Génie des matériaux' in activite or 
        'Génie des procédés' in activite):
        return "Sciences et technologies"
    
    # Catégorie 2 : Sciences de la vie
    elif ('Sciences médicales' in activite or 'Sciences pharmacologiques' in activite or 
          'Sciences Agronomiques' in activite or 'Océan' in activite or 
          'Atmosphère' in activite or 'Environnement naturel' in activite):
        return "Sciences de la vie"
    
    # Catégorie 3 : Sciences humaines et sociales
    elif ('Littérature' in activite or 'Langues' in activite or 'Histoire' in activite or 
          'Archéologie' in activite or 'Philosophie' in activite or 
          'Sociologie' in activite or 'Démographie' in activite or 
          'Sciences juridiques' in activite or 'Sciences politiques' in activite or 
          'Anthropologie' in activite or 'Géographie' in activite or 
          'Aménagement de l\'espace' in activite or 'Economie' in activite or 
          'Sciences de la Gestion' in activite):
        return "Sciences humaines et sociales"
    
    # Catégorie 4 : Textile et design
    elif ('Textile' in activite or 'Prêt à porter' in activite or 'Chaussures' in activite or 
          'Vêtements' in activite or 'Lingerie' in activite or 'Linge de maison' in activite or 
          'Maroquinerie' in activite or 'Tissus' in activite or 'Design' in activite):
        return "Textile et design"
    else:
        return "Autres"


# Appliquer la fonction de catégorisation
data_categorie['Catégorie'] = data_categorie['Activité'].apply(categoriser_activite)

# Copie de data_categorie

data_categorie_copie = data_categorie.copy()

# Compter le nombre de lignes pour chaque 'Région' et chaque 'Categorie'
data_region_categorie = data_categorie.groupby(['Catégorie', 'Région']).size().reset_index(name='count')
   

# Barplot x 2
     
# Création d'un graphique avec la répartition par 'Catégorie' pour chaque 'Région'
plt.figure(figsize=(10, 6))
sns.barplot(data=data_region_categorie, x='Région', y='count', hue='Catégorie')
plt.title("CIR par années")
plt.xlabel("Région")
plt.ylabel("Nombre de lignes")
plt.xticks(rotation=90)
plt.legend(title="Catégories")
plt.show()  

""" On observe que pour chauqe 'Catégorie' la 'Région' 
IDF compte plus de CIR que la 'Région' PACA """

# Camembert par Catégorie   

# Liste des 'Catégorie' uniques
unique_categorie = data_region_categorie['Catégorie'].unique()

# Boucle pour générer un graphique en camembert pour chaque Catégorie'
for categorie in unique_categorie:
    # Filtrer les données pour la 'Catégorie'
    data_categorie = data_region_categorie[data_region_categorie['Catégorie'] == categorie]
    
    # Création d'un graphique en camembert
    plt.figure(figsize=(8, 8))
    plt.pie(data_categorie['count'], labels = data_categorie['Région'], autopct='%1.1f%%', startangle=90)
    plt.title(f"Répartition pour la Catégorie: {categorie}")
    plt.show() 
    
""" On observe que la Catégorie ou la 'Région' PACA est le plus proche de 
l'IDF est 'Génie et ingénieurie', toutefois elle compte 3 fois moins de
CIR que l'IDF. La 'Catégorie' la plus en retard est 'Sciences Sociales
et Humaines avec un nombre de CIR 19 fois plus petit.""" 

# Passage en % en comptant une entreprise de facon unique
   

data_region_categorie_pourcentage = data_count_entreprise.copy()

# Appliquer la fonction de catégorisation
data_region_categorie_pourcentage['Catégorie'] = data_region_categorie_pourcentage['Activité'].apply(categoriser_activite)

# Group by 'Région' & 'Catégorie'

data_region_categorie_pourcentage = data_region_categorie_pourcentage.groupby(['Catégorie','Région']).size().reset_index(name='count')


# Calculer la somme des 'count' pour chaque 'Catégorie'
somme_data_region_categorie = data_region_categorie_pourcentage.groupby('Catégorie')['count'].transform('sum')

# Ajouter une nouvelle colonne 'Pourcentage' au DataFrame
data_region_categorie_pourcentage['Pourcentage'] = (data_region_categorie_pourcentage['count'] / somme_data_region_categorie) * 100


"""
data_region_categorie_pourcentage['Catégorie'] = data_region_categorie_pourcentage['Catégorie'].replace('Sciences fondamentales et technologies appliquées', 'NouvelElement')
data_region_categorie_pourcentage['Catégorie'] = data_region_categorie_pourcentage['Catégorie'].replace('', 'NouvelElement')
"""
# Réorganiser l'ordre des catégories pour que "Autres" soit en dernier
ordre_categories = sorted(data_region_categorie_pourcentage['Catégorie'].unique())
ordre_categories.remove('Autres')  # Retirer "Autres" pour l'ajouter manuellement
ordre_categories.append('Autres')  # Ajouter "Autres" à la fin

data_region_categorie_pourcentage['Catégorie'] = pd.Categorical(
    data_region_categorie_pourcentage['Catégorie'], 
    categories=ordre_categories, 
    ordered=True
)


# Création du graphique
plt.figure(figsize=(10, 6))
sns.barplot(data=data_region_categorie_pourcentage, x='Catégorie', y='Pourcentage', hue='Région')
plt.title("Répartition entre PACA et IDF par catégorie")
plt.xlabel("Catégorie")
plt.ylabel("Part des entreprises éligibles au CIR par région \n(PACA + IDF = 100%)")
plt.xticks(fontsize = 7.5)
plt.legend(title="Région", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8, title_fontsize=10)
plt.show()


# Catégorie évolution annee par annee

data_categorie_annee = data_categorie_copie.groupby(['Région','Annee','Catégorie']).size().reset_index(name='count')

for categorie in unique_categorie:
    
    # Filtrer les données pour la 'Catégorie'
    
    data_filtre = data_categorie_annee[data_categorie_annee['Catégorie'] == categorie]
    
    # Création du graphique
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data_filtre[data_filtre['Région'] == 'IDF'], x='Annee', y='count', marker='o', label='IDF', color='blue')
    sns.lineplot(data=data_filtre[data_filtre['Région'] == 'PACA'], x='Annee', y='count', marker='o', label='PACA', color='orange')
    
    plt.title(f"Évolution du nombre de CIR pour la catégorie '{categorie}' par année")
    plt.xlabel("Année")
    plt.ylabel("Nombre de CIR")
    plt.legend(title="Région")
    plt.grid(visible=True, linestyle="--", alpha=0.7)
    plt.show()
 
""" On observe aucun effet de rattrapement du retard de la 'Région' PACA au cours du 
temps."""

# Graphique en % pour toutes les 'Categorie' sauf 'Autres

data_categorie_annee_pourcentage = data_categorie_annee.copy()

# Calculer la somme des 'count' pour chaque 'Catégorie'
somme_data_categorie_annee = data_categorie_annee_pourcentage.groupby(['Catégorie','Annee'])['count'].transform('sum')

# Ajouter une nouvelle colonne 'Pourcentage' au DataFrame
data_categorie_annee_pourcentage['Pourcentage'] = (data_categorie_annee_pourcentage['count'] / somme_data_categorie_annee) * 100

# Filtre sur les 'Categorie' d'interets
categories_interessees = ['Sciences de la vie', 'Sciences et technologies', 
                          'Sciences humaines et sociales', 'Textile et design']

data_categorie_annee_pourcentage = data_categorie_annee_pourcentage[(data_categorie_annee_pourcentage['Catégorie'].isin(categories_interessees))]


# Configurer la figure avec 4 sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# Couleurs pour les régions
couleurs = {"IDF": "blue", "PACA": "orange"}

# Créer un graphique pour chaque catégorie
for i, categorie in enumerate(categories_interessees):
    ax = axes[i]
    
    # Filtrer les données pour la catégorie courante
    data_categorie = data_categorie_annee_pourcentage[data_categorie_annee_pourcentage['Catégorie'] == categorie]
    
    # Tracer les courbes pour IDF et PACA
    for region, couleur in couleurs.items():
        sns.lineplot(
            data=data_categorie[data_categorie['Région'] == region], 
            x='Annee', y='Pourcentage', marker='o', label=region, color=couleur, ax=ax
        )
    
    # Ajouter des titres
    ax.set_title(categorie)
    ax.set_xlabel('Année')
    
    # Afficher l'étiquette de l'axe Y pour les graphiques de gauche
    if i % 2 == 0:
        ax.set_ylabel('Pourcentage')
    
    # Afficher la légende uniquement pour "Sciences et technologies"
    if categorie == "Sciences humaines et sociales":
        ax.legend(title="Région")
    else:
        ax.get_legend().remove()  # Supprimer la légende pour les autres graphiques

# Ajuster la disposition des sous-graphiques
plt.tight_layout()
plt.suptitle("Pourcentage par catégorie et région, par année", fontsize=16, y=1.02)  # Titre global
plt.show()


                            # CARTOGRAPHIE
                            
# Par annee + region

# Appliquer la fonction de catégorisation
data_explode_annee['Catégorie'] = data_explode_annee['Activité'].apply(categoriser_activite)

# Nettoyer la colonne 'Géolocalisation' pour obtenir latitude et longitude
data_explode_annee['Latitude'] = data_explode_annee['Géolocalisation'].apply(lambda x: float(x.split(',')[0].strip()) if pd.notnull(x) else None)
data_explode_annee['Longitude'] = data_explode_annee['Géolocalisation'].apply(lambda x: float(x.split(',')[1].strip()) if pd.notnull(x) else None)

# Filtrer les données pour PACA et IDF avec des coordonnées valides
data_filtered = data_explode_annee[(data_explode_annee['Région'].isin(['IDF', 'PACA']))].dropna(subset=['Latitude', 'Longitude'])

# Obtenir les combinaisons uniques d'années et de régions
unique_combinations = data_filtered[['Annee', 'Région']].drop_duplicates()

# Créer une palette de couleurs distinctes à partir de matplotlib
num_colors = len(data_filtered['Catégorie'].unique())
colors = plt.cm.tab20.colors  # Utilisation d'une palette de 20 couleurs différentes
color_cycle = cycle(colors)  # Crée un cycle infini de couleurs

# Associer chaque catégorie à une couleur unique de façon déterministe
unique_categories = data_filtered['Catégorie'].unique()
category_colors = {category: f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}' for category, color in zip(unique_categories, color_cycle)}

# Boucle pour créer une carte pour chaque combinaison unique d'année et de région
for _, row in unique_combinations.iterrows():
    year = row['Annee']
    region = row['Région']
    
    # Filtrer les données pour l'année et la région en cours
    data_year_region = data_filtered[(data_filtered['Annee'] == year) & (data_filtered['Région'] == region)]
    
    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    
    # Ajouter des marqueurs pour chaque entreprise
    for idx, row in data_year_region.iterrows():
        category = row['Catégorie']
        color = category_colors.get(category, 'black')  
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Entreprise: {row.get('Désignation', 'N/A')}\nAnnée: {row['Annee']}\nRégion: {row['Région']}\nCatégorie: {category}",
            icon=folium.Icon(color= 'white', icon_color= color, icon='info-sign')
        ).add_to(m)
    
    # Sauvegarder la carte pour chaque année et chaque région dans un fichier HTML
    m.save(f"carte_CIR_{year}_{region}.html")
    print(f"Carte pour l'année {year} et la région {region} générée et sauvegardée sous 'carte_CIR_{year}_{region}.html'")

    # Une carte par Région 
    
# Copie

data_count_entreprise_carto = data_count_entreprise.copy()

# Appliquer la fonction de catégorisation

data_count_entreprise_carto['Catégorie'] = data_count_entreprise_carto['Activité'].apply(categoriser_activite)

# Nettoyer la colonne 'Géolocalisation' pour obtenir latitude et longitude
data_count_entreprise_carto['Latitude'] = data_count_entreprise_carto['Géolocalisation'].apply(
    lambda x: float(x.split(',')[0].strip()) if pd.notnull(x) else None
)
data_count_entreprise_carto['Longitude'] = data_count_entreprise_carto['Géolocalisation'].apply(
    lambda x: float(x.split(',')[1].strip()) if pd.notnull(x) else None
)

# Filtrer les données pour PACA et IDF avec des coordonnées valides
data_filtered = data_count_entreprise_carto[
    (data_count_entreprise_carto['Région'].isin(['IDF', 'PACA']))
].dropna(subset=['Latitude', 'Longitude'])

# Associer des couleurs fixes à chaque catégorie
category_colors = {
    "Sciences et technologies": "#1f77b4",  # Bleu
    "Sciences de la vie": "#2ca02c",        # Vert
    "Sciences humaines et sociales": "#ff7f0e",  # Orange
    "Textile et design": "#d62728",         # Rouge
    "Autres": "#9467bd"                    # Violet
}

# Définir les centres des cartes pour chaque région
region_centers = {
    "IDF": [48.8566, 2.3522],  # Paris, centre de l'Île-de-France
    "PACA": [43.9352, 6.0679]  # Position approximative pour la région PACA
}

# Fonction pour ajouter une légende HTML
def add_legend(map_object, category_colors):
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 30px; left: 30px; width: 250px; height: auto; 
        background-color: white; 
        border:2px solid grey; z-index:9999; font-size:14px;
        padding: 10px; border-radius: 10px;">
        <b>Code couleur - Catégories</b><br>
    """
    for category, color in category_colors.items():
        legend_html += f"<div style='margin-bottom: 5px;'><i style='background:{color};width:15px;height:15px;display:inline-block;margin-right:10px;'></i>{category}</div>"
    legend_html += "</div>"
    map_object.get_root().html.add_child(branca.element.Element(legend_html))

# Boucle pour créer une carte pour chaque région
for region in ['IDF', 'PACA']:
    # Filtrer les données pour la région en cours
    data_region = data_filtered[data_filtered['Région'] == region]
    
    # Échantillonner les données si trop de points (optionnel)
    #if len(data_region) > 1000:  # Limiter à 1000 points pour lisibilité
    #    data_region = data_region.sample(1000, random_state=42)
    
    # Créer une carte centrée sur la région correspondante
    center = region_centers[region]
    m = folium.Map(location=center, zoom_start=8)
    
    # Ajouter des marqueurs pour chaque entreprise
    for idx, row in data_region.iterrows():
        category = row['Catégorie']
        color = category_colors.get(category, '#000000')  # Noir par défaut si non défini
        
        # Ajouter un cercle avec une taille réduite
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,  # Taille du point
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,  # Transparence
            popup=f"Entreprise: {row.get('Désignation', 'N/A')}\nRégion: {row['Région']}\nCatégorie: {category}"
        ).add_to(m)
    
    # Ajouter la légende
    add_legend(m, category_colors)
    
    # Sauvegarder la carte pour chaque région dans un fichier HTML
    m.save(f"carte_{region}.html")
    print(f"Carte pour la région {region} générée et sauvegardée sous 'carte_{region}.html'")
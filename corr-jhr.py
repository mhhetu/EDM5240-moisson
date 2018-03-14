#coding: utf-8

### BONJOUR, ICI Jean-Hugues ###
### Comme toujours, mes notes et corrections sont précédées de trois dièses ###

#Sésame, ouvre-toi.
### Ha ha ha :)

### Ton script est super bien documenté! Bravo!
### J'aime beaucoup l'humour dont tu persilles ton code! Très geek :)

import csv
import requests 
from bs4 import BeautifulSoup 

### Je change le nom du fichier pour voir la différence entre ton output et le mien
fichier = "camJHR.csv"
# fichier = "magasinageappareilphoto.csv"

#Je magasine sur Kijiji.com pour un appareil photo usagé.

### Dans un cas comme le tien, je commencerais par récolter l'info sur tous les appareils photos
### Pour ensuite effectuer le ménage dans un tableur
### Non seulement on perd moins de temps à gosser dans le code
### Mais de tout ramasser nous permet de voir s'il y a des choses qu'on aurait exclues qui s'avèrent intéressantes, finalement

### Quand on ramasse autant d'infos, j'aime bien me faire un compteur pour savoir où je suis rendu quand je fais des «spot checks»
### Je vais donc mettre ce compteur dans une variable que je vais appeler «c».

c = 0

for n in range(1,101):
	url = "https://www.kijiji.ca/b-appareil-photo-camera/ville-de-montreal/page-{}/c103l1700281?ad=offering".format(n)
	#print(url) 

	contenu = requests.get(url)
	page = BeautifulSoup(contenu.text,"html.parser")
	#print(page)

	urlDesCameras = page.find_all("div",class_="title")
	#print(len(urlDesCameras))
 
	for urlCamera in urlDesCameras:
		c += 1
		camera = []

### J'ajoute tout de suite mon compteur «c» et le numéro de page à la variable «camera»
### afin de faciliter le travail lorsque je voudrai effectuer des vérifications
		camera.append(c)
		camera.append(n)

### Je vais réduire la portée du «try», ici.
### Si le script n'arrive pas à trouver l'adresse de l'annonce, il passe à «urlCamera» suivant...
### avec un «break» -> ce qui est «brisé», ici, par le «break», c'est la boucle «for urlCamera in urlDesCameras:»
		try:
			url2 = urlCamera.a["href"]
			#print(url2)
			url2 = "https://www.kijiji.ca" + url2
			#print(url2)
			camera.append(url2)
		except:
			break

		contenu2 = requests.get(url2)
		page2 = BeautifulSoup(contenu2.text,"html.parser")

#Afin de réduire le nombre des annonces imprimées, je crée des critères de recherche.
#Je cherche un appareil photo de la marque Canon, qui me coûterait moins de 600$ et dont l'annonce a été faite il y a moins d'un mois. 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#CRITÈRE MARQUE: CANON
#Ici, je viens chercher toutes les decriptions contenant le mot Canon.

#Je commence par aller chercher dans le code HTML les textes de toutes les descriptions de la page.

### Dans la perspective de tout prendre, j'enregistre la description dans la variable «camera».

		for gaston in page2.find_all("h3"):
			if gaston.text.strip() == "Description":
				description = gaston.find_next("div").text.strip()
				camera.append(description)
				#print(description)

### Je laisse donc tomber ton filtre pour une caméra Canon.
		# if "Canon" in description or "canon" in description or "CANON" in description:
			#print(description)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#CRITÈRE PRIX : < 600$
#Ici, je viens chercher toutes les prix.

### Ton code est super! Tu as vraiment bien travaillé!
### Mais c'est compliqué de faire des filtres qui vont opérer «on the fly», pendant le moissonnage
### Je préfère tout prendre, puis filtrer ensuite.

### Le prix, tout d'abord

		prix = page2.find("span", class_="currentPrice-2872355490").text
		camera.append(prix)

# #Je commence par définir ma variable.
# 				prix = page2.find("span", class_="currentPrice-2872355490").text
# 				#print(prix)

# 				if "$" in prix:
# 					#print(prix)
# 					if prix[0] == "$":
# 						prix = prix[1:]
# 						if "," in prix:
# 							prix = prix.replace(",","")
# 						prix = float(prix)
# 						#print(prix)
# 					elif prix[-1] == "$":
# 						prix = prix[:-2]
# 						if "," in prix:
# 							prix = prix.replace(",",".").replace("\xa0","")
# 						prix = float(prix)
# 						#print(prix)

# #Ici, on exclue les "Sur demande" et "Please contact".
# 				else:
# 					print("Maudit hassler veut négotier à la hausse!")

# #Ici, on exclue les prix qui sont plus élevés que 600$.
# 				if prix < 600:
# 					print(prix)
# 				else:
# 					print("Bin trop cher, tabarouette! Je veux pas hypothéquer ma maison!!!")
# #----------------------------------------------------------------------------------------------------------------------------------------------------------------
# #CRITÈRE DATE : Depuis moins de 1 mois
# #Ici, je viens chercher toutes les annonces qui ont été publiées il y a moins de 3 mois.

### ### ### ### ### ###
### Ensuite la date ###
### ### ### ### ### ###

### Ici, il y a deux possibilités qu'il faut vérifier
### Parfois la date de l'annonce est dans un élément <time>
### Parfois, dans un élément <span>

		if page2.find("time") != None:
			date = page2.find("time")["datetime"]
		elif page2.find("div", class_="datePosted-1350605722") != None:
			if page2.find("div", class_="datePosted-1350605722").find("span") != None:
				date = page2.find("div", class_="datePosted-1350605722").find("span")["title"]
		else:
			date = "Impossible"
		camera.append(date)

# #Je commence par définir ma variable.
# 				date = page2.find("time").text
# 				#print(date)
# 				if "heures" in date or "heure" in date or "jour" in date:
# 					print(date)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
# #Ici, afin de nettoyer les résultats de recherche, j'identifie les annonces qui correspondent à mes critères.

# #Je redéfinie mes variables.
# 				prix = prix < 600
# 				#date = date.find("heures","heure","jour").text

# 				print("DEAL À VÉRIFIER!:",url2,prix,date)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
# #Ici, j'écris mes résultats dans un fichier CSV.

# 				camera.append(url2)
# 				camera.append(prix)
# 				camera.append(date)

### Toute les infos sont colligées
### On imprime au passage...

		print(camera)

### Et on crée notre fichier CSV
### Tu te rendras compte qu'il y a plusieurs annonces qui reviennent dans chaque page
### Mais la plupart des annonces sont uniques

		variable = open(fichier,"a")
		variable2 = csv.writer(variable)
		variable2.writerow(camera)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------
# #Ici, je ferme le TRY.
# 		except:
# 			print("Pas de bon deal icitte!")

#python moisson-magasinageappareilphoto.py

"""Voici mes difficultés:
	Je n'arrive pas à imprimer dans un fichier CSV de façon ordonnée
	Je n'arrive pas à isoler mes critères correctement. J'ai encore des annonces de plus de 600$ et de plus d'un jour qui apparaissent."""

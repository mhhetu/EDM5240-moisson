#coding: utf-8

#Sésame, ouvre-toi.

import csv
import requests 
from bs4 import BeautifulSoup 

fichier = "magasinageappareilphoto.csv"

#Je magasine sur Kijiji.com pour un appareil photo usagé.

for n in range(1,101):
	url = "https://www.kijiji.ca/b-appareil-photo-camera/ville-de-montreal/page-{}/c103l1700281?ad=offering".format(n)
	#print(url) 

	contenu = requests.get(url)
	page = BeautifulSoup(contenu.text,"html.parser")
	#print(page)

	urlDesCameras = page.find_all("div",class_="title")
	#print(len(urlDesCameras))
 
	for urlCamera in urlDesCameras:
		camera = []
		try:
			url2 = urlCamera.a["href"]
			#print(url2)
			url2 = "https://www.kijiji.ca" + url2
			#print(url2)
			camera.append(url2)
			
			contenu2 = requests.get(url2)
			page2 = BeautifulSoup(contenu2.text,"html.parser")
			

#Afin de réduire le nombre des annonces imprimées, je crée des critères de recherche.
#Je cherche un appareil photo de la marque Canon, qui me coûterait moins de 600$ et dont l'annonce a été faite il y a moins d'un mois. 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#CRITÈRE MARQUE: CANON
#Ici, je viens chercher toutes les decriptions contenant le mot Canon.

#Je commence par aller chercher dans le code HTML les textes de toutes les descriptions de la page.
			for gaston in page2.find_all("h3"):
				if gaston.text.strip() == "Description":
					description = gaston.find_next("div").text.strip()
					#print(description)
			if "Canon" in description or "canon" in description or "CANON" in description:
				#print(description)
				

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#CRITÈRE PRIX : < 600$
#Ici, je viens chercher toutes les prix.

#Je commence par définir ma variable.
				prix = page2.find("span", class_="currentPrice-2872355490").text
				#print(prix)

				if "$" in prix:
					#print(prix)
					if prix[0] == "$":
						prix = prix[1:]
						if "," in prix:
							prix = prix.replace(",","")
						prix = float(prix)
						#print(prix)
					elif prix[-1] == "$":
						prix = prix[:-2]
						if "," in prix:
							prix = prix.replace(",",".").replace("\xa0","")
						prix = float(prix)
						#print(prix)

#Ici, on exclue les "Sur demande" et "Please contact".
				else:
					print("Maudit hassler veut négotier à la hausse!")

#Ici, on exclue les prix qui sont plus élevés que 600$.
				if prix < 600:
					print(prix)
				else:
					print("Bin trop cher, tabarouette! Je veux pas hypothéquer ma maison!!!")
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#CRITÈRE DATE : Depuis moins de 1 mois
#Ici, je viens chercher toutes les annonces qui ont été publiées il y a moins de 3 mois.

#Je commence par définir ma variable.
				date = page2.find("time").text
				#print(date)
				if "heures" in date or "heure" in date or "jour" in date:
					print(date)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#Ici, afin de nettoyer les résultats de recherche, j'identifie les annonces qui correspondent à mes critères.

#Je redéfinie mes variables.
				prix = prix < 600
				#date = date.find("heures","heure","jour").text

				print("DEAL À VÉRIFIER!:",url2,prix,date)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#Ici, j'écris mes résultats dans un fichier CSV.

				camera.append(url2)
				camera.append(prix)
				camera.append(date)

				variable = open(fichier,"a")
				variable2 = csv.writer(variable)
				variable2.writerow(camera)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#Ici, je ferme le TRY.
		except:
			print("Pas de bon deal icitte!")


			
#python moisson-magasinageappareilphoto.py

"""Voici mes difficultés:
	Je n'arrive pas à imprimer dans un fichier CSV de façon ordonnée
	Je n'arrive pas à isoler mes critères correctement. J'ai encore des annonces de plus de 600$ et de plus d'un jour qui apparaissent."""

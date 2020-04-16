#!/usr/bin/env python
# coding: utf-8

# Twitter: @xrths
# www.xrths.fr

# Importation des librairies.
import sys
from datetime import datetime

from modules.APIEngine import get_data
from modules.ConfigEngine import get_config
from modules.GraphEngine import make_graph, save_graph_data
from modules.MathsEngine import calc_percentage, save_worldometers_data, save_gouv_data, calc_difference, check_data_change
from modules.TimeEngine import check_time, get_days
from modules.TwitterEngine import twitter_auth, get_last_tweet

api, auth = twitter_auth()  # API TWEEPY
directory = get_config('System', 'directory')
graph_img = directory + "data/graphIMG.png"
log_time = "[" + datetime.now().strftime("%D %H:%M:%S") + "] "

# ----------------------------------#

if check_time():  # On vérifie le créneau horaire si activé dans le fichier config.ini
    pass
else:
    sys.exit()

# ----------------------------------#

if get_last_tweet() == 1:  # On vérifie que le bot n'a pas déjà posté aujourd'hui
    print(log_time + "Un tweet posté avec l'application [" + get_config('TwitterAPI', 'app_name') + "] existe déjà pour aujourd'hui !")
    sys.exit()
elif get_last_tweet() == 0:
    print(log_time + "Aucun tweet n'a été posté aujourd'hui, suite du programme...")
else:
    print(log_time + "Erreur.")
    sys.exit()

# ----------------------------------#

gouv_data = get_data("GOUVERNEMENT")  # On récupère les données du gouvernement

# ----------------------------------#

if gouv_data is not None:  # Si elles sont valides
    check_data_change()  # On vérifie quelles sont un minimum cohérentes
    worldometers_data = get_data("WORLDOMETERS")
else:
    print(log_time + "Aucune donnée pour aujourd'hui ! (Source: Gouvernement)\n")
    sys.exit()

# ----------------------------------#

difference_data = calc_difference()  # On fait les calculs de toutes les données
percentage_data = calc_percentage()  # On récupère les pourcentages


def format_data(data):
    return str("{0:,}".format(data))


print("\n----------------------------------------\n")

# ----------------------------------#

# On met en forme les deux tweets
first_tweet_form = str("‪La 🇫🇷 est confinée depuis:"
                       + "\n" + get_days() + " jours"
                       + "\n"
                       + "\n" + "🟩 " + format_data(gouv_data['casGueris']) + " guéris " + percentage_data[
                           'casGueris'] + " " + difference_data['casGueris']
                       + "\n" + "🟧 " + format_data(gouv_data['casMalades']) + " malades " + difference_data[
                           'casMalades_GOUV']
                       + "\n" + "🟥 " + "dont " + format_data(gouv_data['casReanimation']) + " cas graves " +
                       difference_data['casReanimation']
                       + "\n" + "⬛ " + format_data(gouv_data['totalDeces']) + " morts " + percentage_data[
                           'totalDeces'] + " " + difference_data['totalDeces']
                       + "\n"
                       + "\n" + "‪◾️ " + format_data(gouv_data['decesHopital']) + " en hôpitaux " + difference_data[
                           'decesHopital']
                       + "\n" + "‪◾️ " + format_data(gouv_data['decesEhpad']) + " en ESMS " + difference_data[
                           'decesEhpad']
                       + "\n"
                       + "\n" + "‪ 🦠 — " + format_data(gouv_data['casConfirmes']) + " cas " + difference_data[
                           'casConfirmes']
                       + "\n"
                       + "\n" + "‪Graphique 📈 — ⬇️‬ "
                       + "\n" + "#ConfinementJour" + get_days() + " | #COVID19")

second_tweet_img = str(
    "🏠 " + format_data(gouv_data['casEhpad']) + " cas en EHPAD" + " " + difference_data['casEhpad']
    + "\n" + "🛏 " + format_data(gouv_data['casHopital']) + " hospitalisés" + " " + difference_data['casHopital']
    + "\n" + "🔬 " + format_data(worldometers_data['totalTests']) + " dépistages"
    + "‪\n" + ""
    + "‪\n" + "📈 Évolution #graphique du #COVID19 en #France‬")

print(first_tweet_form)
print("\n------------------\n")
print(second_tweet_img)

print("\n----------------------------------------\n")

# input("\n----------------------------------------\nPressez ENTRER pour valider le tweet [...]") #Décommenter pour utiliser le bot manuellement

# ----------------------------------#
# On sauvegarde toutes les données
save_graph_data(gouv_data['casConfirmes'], gouv_data['casHopital'], gouv_data['casReanimation'],
                gouv_data['totalDeces'],
                gouv_data['casGueris'])
print(log_time + "Données du graphique mises à jours !")

save_gouv_data(gouv_data)
print(log_time + "Données du gouvernement sauvegardées !")

save_worldometers_data(worldometers_data)
print(log_time + "Données de Worldometers sauvegardées !")

make_graph()  # On génère le graphique
print(log_time + "Graphique généré !")

# ----------------------------------#
# On tweet
posted_tweet = api.update_status(first_tweet_form)

api.update_with_media(graph_img, second_tweet_img, in_reply_to_status_id=posted_tweet.id, retry_count=10, retry_delay=5, retry_errors={503})

# On envoie le lien du tweet sur le compte privé du propriétaire
api.send_direct_message(recipient_id=get_config('TwitterAPI', 'preview_id'), text="https://twitter.com/" + get_config('TwitterAPI', 'account_name') + "/status/" + str(posted_tweet.id))

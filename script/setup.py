import os
import subprocess

# Remplacez 'Jeu.py' par le nom de votre fichier
fichier_a_compiler = 'Jeu.py'
commande = f'nuitka --standalone --onefile {fichier_a_compiler}'

# Exécute la commande
subprocess.call(commande, shell=True)
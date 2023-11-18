# Developpez_un_programme_logiciel_en_Python-Club_d_echec
Projet OpenClassrooms
## P4 - Formation Développeur Python

Objectif : 
Ecrire un outil qui permette de gérer les tournois d'échec pour aider le club, mais qui fonctionne hors ligne.
Suivre la conception Modèle-Vue-Contrôleur (MVC).
Les enregistrements des parties se font en local, pour ce projet nous utilisons TinyDB, (doc)[https://tinydb.readthedocs.io/en/latest/]
[lien du projet](http://course.oc-static.com/projects/Python+FR/P4+-+D%C3%A9veloppez+un+programme+logiciel+en+utilisant+Python/AncienneVersion-De%CC%81veloppez+un+programme+logiciel+en+Python.pdf)

Vous pouvez retrouver en .docx [les spécifications technique](https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python%20FR/P4%20-%20D%C3%A9veloppez%20un%20programme%20logiciel%20en%20utilisant%20Python/Centre%20%C3%A9checs%20-%20sp%C3%A9cification%20technique.docx)
### Prérequis
* Python est bien installé sur votre ordinateur
* Git installé (conseillé)

# INSTALLATION ( pour windows )

Créer un dossier vide. Il contiendra le code complet du projet, ainsi que les données du site aspiré.

## 1. Installation du logicel

Ouvrez un terminal:

Depuis le dossier précédemment créé, clonez le repository du programme avec la commande :

><pre><code>git clone https://github.com/Nathom78/Developpez_un_programme_logiciel_en_Python-Club_d_echec.git</code></pre>

Ou utiliser [ce repository](https://github.com/Nathom78/Developpez_un_programme_logiciel_en_Python-Club_d_echec.git)
<br>
## 2. Créer et activer l'environnement virtuel

Dans le terminal, toujours à la **racine du projet** :<br>
Tapez la commande suivante, afin de créer un environnement dans le repertoire env :
```PowerShell 
python -m venv env 
```
Et la commande suivante, pour activer l'environnement :
<pre><code> source env/bin/activate</code></pre>
Résultat:
><pre> (env) "chemin de votre répertoire crée"> </pre>

## 3. Installer les paquets nécessaires aux projets 

Normalement une fois le clonage du projet réalisé, il y a un fichier *requirement.txt* à la racine.<br>
Taper la commande suivante :
<pre> pip install -r requirements.txt </pre>
Pour vérifier, taper cette commande :
<pre><code>pip list</code></pre>
Et vous devriez avoir au minimum:
><pre><code>decorator   5.1.1
>flake8      6.0.0
>flake8-html 0.4.3
>Jinja2      3.1.2
>MarkupSafe  2.1.1
>mccabe      0.7.0
>pycodestyle 2.10.0
>pyflakes    3.0.1
>Pygments    2.14.0
>tinydb      4.7.0</code></pre>

## 4. Execution du logiciel

Il ne reste plus qu'à lancer le programme main.py, toujours depuis le terminal, depuis le repertoire racine code grâce à la commande suivante :

<pre><code>(env) X:code> py main.py </code></pre>

## 5. Rapport Flake8 

[Edit on GitHub](https://github.com/PyCQA/flake8/blob/5e99de7209fc5278c73d242dfd27522a924ff8f6/docs/source/index.rst)

Un fichier de configuration de Flake8 est créé à la racine .flake8.
Il contient :
><pre><code>[flake8]
>exclude =
>    .git,
>    __pycache__,
>    env/,
>max-line-length = 119</code></pre>
Les fichiers à exclure ainsi que la longueur maximum d'une ligne de code

Pour lancer un rapport généré par Flake8 avec le plugin Flake8_html, vers le répertoire sous la racine **_flake8_rapport_**.

Executer la commande suivante :
><pre><code>flake8 --format=html --htmldir=flake8_rapport</code></pre>
afin de vérifier la conformité du code aux directives PEP8

## Technologies
[![My Skills](https://skillicons.dev/icons?i=python,git,github&theme=dark)](https://skillicons.dev)
 

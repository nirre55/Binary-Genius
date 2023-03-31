import hashlib
from PIL import Image
import glob
import imageio
import os
import cv2
import re


FILE_NAME = r"D:\Binary-Genius\Binary-Genius\binary_content.text"

def file_to_binary(nom_fichier):
    # Ouverture du fichier en mode binaire
    with open(nom_fichier, "rb") as f:
        # Lecture du contenu du fichier
        contenu = f.read()
    
    # Conversion du contenu en binaire
    contenu_binaire = ''.join(format(byte, '08b') for byte in contenu)
    
    # Retourne le contenu binaire
    return contenu_binaire


def binary_to_file(contenu_binaire, nom_fichier):
    # Calcule la longueur du contenu binaire
    longueur = len(contenu_binaire)
    
    # Convertit le contenu binaire en octets
    octets = [int(contenu_binaire[i:i+8], 2) for i in range(0, longueur, 8)]
    
    # Convertit les octets en bytes
    bytes_ = bytes(octets)
    
    # Écrit les bytes dans un nouveau fichier
    with open(nom_fichier, "wb") as f:
        f.write(bytes_)


def compare_file_hashes(nom_fichier1, nom_fichier2):
    # Ouvre les deux fichiers en mode lecture binaire
    with open(nom_fichier1, "rb") as f1, open(nom_fichier2, "rb") as f2:
        # Calcule l'empreinte de hachage de chaque fichier
        h1 = hashlib.sha256(f1.read()).hexdigest()
        h2 = hashlib.sha256(f2.read()).hexdigest()
    
    # Vérifie si les deux empreintes de hachage sont identiques
    if h1 == h2:
        print("Les deux fichiers sont identiques.")
    else:
        print("Les deux fichiers sont différents.")


def binary_to_image(contenu_binaire):
    # Créer une image de 1280x720 pixels
    image = Image.new("RGB", (1280, 720))
    
    # Parcourir tous les pixels et les rendre noirs ou blancs en fonction de la chaîne de caractères
    pixels = image.load()
    index = 0
    index_image_name = 0
    while index < len(contenu_binaire):
        for i in range(0, 1280, 2):
            for j in range(0, 720, 2):
                if index < len(contenu_binaire):
                    if contenu_binaire[index] == "0":
                        pixels[i, j] = (0, 0, 0) # Noir
                        pixels[i+1, j] = (0, 0, 0) # Noir
                        pixels[i, j+1] = (0, 0, 0) # Noir
                        pixels[i+1, j+1] = (0, 0, 0) # Noir
                    else:
                        pixels[i, j] = (255, 255, 255) # Blanc
                        pixels[i+1, j] = (255, 255, 255) # Blanc
                        pixels[i, j+1] = (255, 255, 255) # Blanc
                        pixels[i+1, j+1] = (255, 255, 255) # Blanc
                    index += 1
                else:
                    pixels[i, j] = (0, 0, 0) # Noir                
        # Enregistrer l'image sous le nom "imageX.png"
        image.save(f"Images/frame{index_image_name}.png")
        index_image_name += 1
        # Créer une nouvelle image pour le prochain tour de boucle
        image = Image.new("RGB", (1280, 720))
        pixels = image.load()
        

def find_difference(string1, string2):
    # Vérifier que les deux chaînes ont la même longueur
    if len(string1) != len(string2):
        raise ValueError("Les deux chaînes n'ont pas la même longueur.")
    
    # Trouver les indices où les deux chaînes diffèrent
    differences = []
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            differences.append(i)
    
    # Retourner les indices de différence
    return differences

def image_to_binary(image, len_contenu_binaire, image_name):
    """
    Convertit une séquence d'images en une chaîne binaire.

    Args :
        images : Une liste d'objets PIL Image.
        max_binary_length : La longueur maximale de la chaîne binaire à générer.

    Returns:
        Une chaîne binaire représentant le contenu des images.
    """

    # Initialisation du contenu binaire
    contenu_binaire = ""

    # Parcourir toutes les images
    try:
        # Ouvrir l'image et parcourir tous les pixels
        pixels = image.load()
        len_content_file = count_characters(r"D:\Binary-Genius\Binary-Genius\binary_content.text")
        contenu_binaire = extract_pixels_binary(image, pixels, len_contenu_binaire, len_content_file)
        append_text_to_file(contenu_binaire, FILE_NAME)            
        
    except:
        print(f"Erreur lors du traitement de l'image {image_name}")
    
    # Retourner le contenu binaire
    return contenu_binaire

def extract_pixels_binary(img, pixels, len_contenu_binaire, len_content_file):
    """
    Extrait la chaîne binaire représentant le contenu des pixels de l'image.

    Returns:
        La chaîne binaire représentant le contenu des images.
    """
    contenu_binaire = ""
    for i in range(0, img.width, 2):
                for j in range(0, img.height, 2):
                    # Vérifier si le pixel est noir ou blanc et ajouter le caractère correspondant au contenu binaire
                    if pixels[i, j] == (0, 0, 0) and pixels[i+1, j] == (0, 0, 0) and pixels[i, j+1] == (0, 0, 0) and pixels[i+1, j+1] == (0, 0, 0):
                        contenu_binaire += "0"
                        len_content_file += 1
                    else:
                        contenu_binaire += "1"
                        len_content_file += 1
                    # Vérifier si la longueur maximale du contenu binaire a été atteinte
                    if len_content_file >= len_contenu_binaire:
                        os.remove(img.filename)
                        return contenu_binaire
    os.remove(img.filename)
    return contenu_binaire

def append_text_to_file(text, filename):
    with open(filename, 'a') as f:
        f.write(text)

        
def create_video_from_images(image_folder_path, video_folder_path, fps):
    """
    Crée une vidéo à partir d'une série d'images contenues dans un dossier.

    Args:
        image_folder_path (str): Le chemin vers le dossier contenant les images.
        fps (int): Le nombre d'images par seconde dans la vidéo.

    Returns:
        str: Le chemin vers le fichier vidéo créé.
    """
    # Obtenir la liste des noms de fichiers des images triée numériquement
    image_files = sorted([os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.png')], key=lambda x: int(re.search(r'\d+', x).group()))

    # Charger les images en utilisant imageio
    images = [imageio.imread(f) for f in image_files]
    # Déterminer le nom du fichier de sortie de la vidéo
    video_file_name = os.path.join(video_folder_path, 'video.mp4')
    # Créer la vidéo à partir des images chargées
    imageio.mimsave(video_file_name, images, fps=fps, quality=10)
    # Retourner le nom du fichier vidéo créé
    
    # Supprimer les fichiers d'images
    for f in image_files:
        os.remove(f)

    return video_file_name


def create_video_from_images_cv(image_folder_path, video_folder_path, fps):
    """
    Crée une vidéo à partir d'une série d'images contenues dans un dossier.

    Args:
        image_folder_path (str): Le chemin vers le dossier contenant les images.
        fps (int): Le nombre d'images par seconde dans la vidéo.

    Returns:
        str: Le chemin vers le fichier vidéo créé.
    """
    # Obtenir la liste des noms de fichiers des images triée numériquement
    image_files = sorted([os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.png')], key=lambda x: int(re.search(r'\d+', x).group()))

    # Charger la première image pour obtenir les dimensions de l'image
    img = cv2.imread(image_files[0])
    height, width, layers = img.shape

    # Déterminer le nom du fichier de sortie de la vidéo
    video_file_name = os.path.join(video_folder_path, 'video.mp4')

    # Initialiser le writer vidéo en utilisant les dimensions de l'image et le nombre d'images par seconde
    video = cv2.VideoWriter(video_file_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Parcourir les images, les ajouter à la vidéo et les supprimer
    for image_file in image_files:
        img = cv2.imread(image_file)
        video.write(img)
        os.remove(image_file)

    # Fermer le writer vidéo et retourner le nom du fichier vidéo créé
    cv2.destroyAllWindows()
    video.release()

    return video_file_name


def extract_frames_from_video(video_path, save_path):
    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)

    # Vérifier que la vidéo est ouverte
    if not cap.isOpened():
        raise ValueError("Impossible d'ouvrir la vidéo")

    # Variable pour compter le nombre d'images extraites
    count = 0

    # Lire les images de la vidéo jusqu'à la fin
    while True:
        # Lire la prochaine image
        ret, frame = cap.read()

        # Si la lecture a réussi, sauvegarder l'image et incrémenter le compteur
        if ret:
            save_name = f"{save_path}/frame{count}.png"
            cv2.imwrite(save_name, frame)
            count += 1
        # Si la lecture a échoué, sortir de la boucle
        else:
            break

    # Fermer la vidéo
    cap.release()

    return count


def count_characters(filename):
    """
    Lit un fichier et retourne le nombre de caractères.

    Args:
        filename : Le nom du fichier à lire.

    Returns:
        Le nombre de caractères dans le fichier.
    """
    try:
        with open(filename, "r") as file:
            content = file.read()
            return len(content)
    except FileNotFoundError:
        print(f"Le fichier {filename} n'a pas été trouvé.")
        return 0

def read_file(filename):
    """
    Lit le contenu d'un fichier texte.

    Args:
        filename: Le nom du fichier à lire.

    Returns:
        Une chaîne de caractères représentant le contenu du fichier.
    """
    with open(filename, "r") as f:
        content = f.read()
    return content

def clear_file_content(file_name):
    """
    Supprime le contenu du fichier spécifié.

    Args:
        file_name (str): Le nom du fichier à vider.
    """
    with open(file_name, 'w') as file:
        file.write('')


def compare_images_in_folders(folder1, folder2):
    """
    Compare les images ayant le même nom dans deux dossiers différents en utilisant le hash MD5.

    Args:
        folder1 (str): Le chemin vers le premier dossier.
        folder2 (str): Le chemin vers le deuxième dossier.

    Returns:
        Un dictionnaire contenant les noms des images en commun et leur état de correspondance (True/False).
    """

    # Trouver tous les fichiers d'images dans le premier dossier
    images1 = [f for f in os.listdir(folder1) if f.endswith('.png')]
    # Trouver tous les fichiers d'images dans le deuxième dossier
    images2 = [f for f in os.listdir(folder2) if f.endswith('.png')]

    # Trouver les noms des images en commun entre les deux dossiers
    common_images = set(images1).intersection(images2)

    # Créer un dictionnaire pour stocker les résultats de la comparaison
    comparison_results = {}

    # Comparer les images en utilisant le hash MD5
    for image in common_images:
        # Lire les images en binaire
        with open(os.path.join(folder1, image), 'rb') as f1:
            with open(os.path.join(folder2, image), 'rb') as f2:
                # Calculer le hash MD5 des images
                md5_1 = hashlib.md5(f1.read()).hexdigest()
                md5_2 = hashlib.md5(f2.read()).hexdigest()
                # Comparer les deux hash et stocker le résultat
                if md5_1 == md5_2:
                    comparison_results[image] = True
                else:
                    comparison_results[image] = False

    return comparison_results


if __name__ == "__main__":

    # print(compare_images_in_folders(r"D:\Binary-Genius\Binary-Genius\Images\first", r"D:\Binary-Genius\Binary-Genius\Images\second"))
    chemin = r"D:\Binary-Genius\Binary-Genius"
    image_path = r"D:\Binary-Genius\Binary-Genius\Images"
    video_path = r"D:\Binary-Genius\Binary-Genius\Videos"
    nom_fichier_intial = "ss.zip"
    nom_fichier_generer = "mon_fichier.zip"

    fichier_complet_intial = os.path.join(chemin, nom_fichier_intial)
    fichier_complet_generer = os.path.join(chemin, nom_fichier_generer)


    # contenu_binaire = file_to_binary(fichier_complet_intial)
    # binary_to_image(contenu_binaire)

    # create_video_from_images(image_path, video_path, 10)
    # create_video_from_images_cv(image_path, video_path, 10)

    # print(f"1eme binnary ==> {len(contenu_binaire)}")

    #video_path = r"D:\Binary-Genius\Binary-Genius\Videos\video.mp4"
    video_path = r"D:\Binary-Genius\Binary-Genius\Videos\Video Test.mp4"

    num_frames = extract_frames_from_video(video_path, image_path)
    print(f"{num_frames} images extraites") 

    # # Trouver tous les fichiers d'images correspondant au modèle de nom de fichier
    # image_files = glob.glob("Images/frame*.png")

    # # Trier les noms de fichiers numériquement
    # image_files = sorted(image_files, key=lambda x: int(re.search(r'\d+', x).group()))

    # len_content_file = count_characters(FILE_NAME)

    # contenu_binaire_2 = ""
    # # Charger les images et générer le contenu binaire
    # for file in image_files:
    #     with Image.open(file) as image:
    #         image_name = os.path.basename(file)
    #         image_to_binary(image, len(contenu_binaire), image_name)

    # # #ss = count_characters(r"D:\Binary-Genius\Binary-Genius\binary_content.text")
    # contenu_binaire_2 = read_file(r"D:\Binary-Genius\Binary-Genius\binary_content.text")
    
    # print(f"2eme binnary ==> {len(contenu_binaire_2)}")

    

    # binary_to_file(contenu_binaire_2, nom_fichier_generer)
    # compare_file_hashes(fichier_complet_intial , fichier_complet_generer)
    # temp = find_difference(contenu_binaire_2, contenu_binaire)
    # print(len(temp))


    clear_file_content(FILE_NAME)
    
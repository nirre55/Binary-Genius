from pytube import YouTube
import cv2
import numpy as np

def download_youtube_video():
    # Définir l'URL de la vidéo à télécharger
    url = "https://youtu.be/HindnpBsWOk"

    # Créer une instance de l'objet YouTube avec l'URL
    yt = YouTube(url)

    # Récupérer la plus haute résolution disponible
    video = yt.streams.get_highest_resolution()

    # Télécharger la vidéo
    video.download(output_path=r"D:\Binary-Genius\Binary-Genius\Videos")




def compare_images(img_path1, img_path2):
    """
    Compare deux images pixel par pixel et retourne l'index des pixels différents.

    Args:
        img_path1 (str): Le chemin d'accès à la première image.
        img_path2 (str): Le chemin d'accès à la deuxième image.

    Returns:
        list: La liste des index des pixels différents.
    """
    # Charger les images en utilisant OpenCV
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)

    # Vérifier que les deux images ont la même taille
    if img1.shape != img2.shape:
        raise ValueError("Les deux images doivent avoir la même taille.")

    # Calculer la différence entre les deux images
    diff = np.sum(np.abs(img1.astype(np.int32) - img2.astype(np.int32)), axis=2)

    # Trouver les indices des pixels différents
    diff_indices = np.where(diff != 0)
    diff_indices = list(zip(diff_indices[0], diff_indices[1]))

    return diff_indices


ss = compare_images(r"D:\Binary-Genius\Binary-Genius\Images\first\frame1.png", r"D:\Binary-Genius\Binary-Genius\Images\second\frame1.png")
print(len(ss))

#download_youtube_video()
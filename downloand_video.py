from pytube import YouTube

def download_youtube_video():
    # Définir l'URL de la vidéo à télécharger
    url = "https://youtu.be/8HDdIPJnawg"

    # Créer une instance de l'objet YouTube avec l'URL
    yt = YouTube(url)

    # Récupérer la plus haute résolution disponible
    video = yt.streams.get_highest_resolution()

    # Télécharger la vidéo
    video.download(output_path=r"D:\Binary-Genius\Binary-Genius\Videos")


def append_text_to_file(text, filename):
    with open(filename, 'a') as f:
        f.write(text)

append_text_to_file("hhhhhhhhhhhhh", "FILE_NAME.text")   
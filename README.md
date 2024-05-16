## generate-subtitle
Ce projet utilise les bibliothèques ffmpeg-python et faster-whisper pour créer une application capable d’extraire l’audio d’une vidéo d’entrée, de transcrire l’audio extrait, de générer un fichier de sous-titres en Anglais basé sur la transcription, traduire les sous-titres de ce fichier en Yoruba grace l'API de Google Translate et l’ajouter à une copie de la vidéo d’entrée.

## Fonctionnalités

- Extrait la piste audio d'une vidéo d'entrée
- Transcrit la piste audio en utilisant le modèle Whisper
- Génère un fichier de sous-titres au format SRT
- Traduit les sous-titres dans une langue cible (par défaut, la langue yoruba)
- Ajoute les sous-titres traduits à la vidéo d'entrée en tant que sous-titres souples ou durs

## Prérequis

- Python 3.x
- FFmpeg installé et accessible via le PATH système
- Bibliothèques Python : `faster_whisper`, `googletrans`

## Utilisation

1. Placez votre fichier vidéo d'entrée (par exemple, `input.mp4`) dans le même répertoire que le script.
2. Exécutez le script Python.
3. Le script générera un fichier de sous-titres SRT dans la langue d'origine détectée par Whisper.
4. Le script traduira les sous-titres dans la langue cible spécifiée (par défaut, le yoruba).
5. Une nouvelle vidéo avec les sous-titres traduits sera générée (par exemple, `output-input.mp4`).

## Personnalisation

- Vous pouvez modifier la langue cible pour la traduction des sous-titres en modifiant le paramètre `dest_lang` dans la fonction `translate_subtitles`.
- Vous pouvez choisir d'ajouter les sous-titres comme des sous-titres souples ou durs en modifiant le paramètre `soft_subtitle` dans la fonction `add_subtitle_to_video`.

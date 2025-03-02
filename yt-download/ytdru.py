import os
from yt_dlp import YoutubeDL

# Укажите папки для сохранения видео и аудио
VIDEO_FOLDER = "C:/Videos"  # Папка для видео
AUDIO_FOLDER = "C:/Audio"   # Папка для аудио

# Создаём папки, если они не существуют
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def download_video_and_audio(url, resolution):
    try:
        ydl_opts = {
            'outtmpl': {
                'video': os.path.join(VIDEO_FOLDER, '%(title)s.%(ext)s'),
                'audio': os.path.join(AUDIO_FOLDER, '%(title)s.%(ext)s'),
            },
            'format': f'bestvideo[height<={resolution}p]+bestaudio/best[height<={resolution}p]',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            print(f"Видео '{video_title}' успешно скачано в {VIDEO_FOLDER}!")
            print(f"Аудио '{video_title}' успешно скачано в {AUDIO_FOLDER}!")

            # Объединение видео и аудио
            video_path = os.path.join(VIDEO_FOLDER, f"{video_title}.mp4")
            audio_path = os.path.join(AUDIO_FOLDER, f"{video_title}.m4a")
            output_path = os.path.join(VIDEO_FOLDER, f"{video_title}_combined.mp4")
            combine_video_and_audio(video_path, audio_path, output_path)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def combine_video_and_audio(video_path, audio_path, output_path):
    try:
        print("Объединение видео и аудио с помощью ffmpeg...")
        os.system(f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{output_path}"')
        print(f"Видео и аудио успешно объединены в {output_path}!")
    except Exception as e:
        print(f"Ошибка при объединении видео и аудио: {e}")
    finally:
        # Удаляем временные файлы
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

def main():
    url = input("Введите URL видео на YouTube: ")
    print("Выберите разрешение для скачивания:")
    print("1 - 720p")
    print("2 - 1080p")
    print("3 - 4K")
    resolution_choice = int(input("Ваш выбор: "))

    resolution_map = {1: 720, 2: 1080, 3: 2160}
    resolution = resolution_map.get(resolution_choice, 720)

    download_video_and_audio(url, resolution)

if __name__ == "__main__":
    main()
# Dramafever-Downloader
Dramafever Downloader descarga subtitulos de episodios de Dramafever en srt.

    Uso: dramafever.py url [-s] [--lang IDIOMA]
    
    positional arguments:
      url                   URL del video de Dramafever
    optional arguments:
      -h, --help            Muestra este mensaje y la aplicación cierra
      -s, --subs            Muestra todos los subtitulos disponibles
      --lang LANG           Codigo ISO del idioma

    Ejemplo:
    python dramafever.py https://www.dramafever.com/es/drama/4946/1/The_K2/?ap=1 --lang en

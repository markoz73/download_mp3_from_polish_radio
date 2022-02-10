#! python3
# Pobiera audycje ze strony polskiego radia i zapisuje w folderze moje podcasty
import ast, bs4, os, platform, re, requests

if platform.system() == 'Windows':
    os.chdir('C:\\Users\\48509\\Dropbox\\Moje podcasty\\Polskie Radio')
elif platform.system() == 'Linux':
    os.chdir('/storage/emulated/0/Moje podcasty')
else:
    print('Brak ścieżki zapisu dla systemu ' + platform.system())

# TODO create non existing directory


while True:
    print('Podaj URL strony z audycją:')
    podcastPage = input()
    # podcastPage = 'https://www.polskieradio.pl/9/325/Artykul/2414097,Muzyka-siatkowka-pasja' # tested url 
    res = requests.get(podcastPage)

    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='html.parser')

    # znalezienie linku do pliku
    prMediaPlay = soup.select('.pr-media-play')
    dict = ast.literal_eval(str(prMediaPlay[0].attrs['data-media']).replace('true', 'True'))
    url = dict['file']

    # znalezienie tytułu
    title = soup.select('title')[0].text[3:65]
    replRegex = re.compile(r'(-|"|,|:|(|)|Trójka|Jedynka|polskieradio\.pl|\r\n|\?)')
    title = replRegex.sub('', title)
    title = re.sub(' +',' ', title).rstrip()

    # TODO: sprawdzic czy istnieje url
    res = requests.get('http:' + url)
    # pobranie i zapis pliku
    try:
        requestFile = open(title + '.mp3', 'wb')
        for chunk in res.iter_content(100000):
            requestFile.write(chunk)
        requestFile.close()

    except OSError:
        # jeśli błąd w nazwie pliku (niedozwolone znaki)
        print("Błędna nazwa pliku: " + title + '.mp3')
        input()



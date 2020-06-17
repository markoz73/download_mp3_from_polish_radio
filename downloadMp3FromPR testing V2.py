#! python3
#
import ast, bs4, json, logging, os, platform, re, requests, sys

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

logging.debug('Początek programu')
logging.debug('Platforma :' + platform.system())

# edits--------------------------------------------------------------------------
# ścieżki zapisu pobranych audycji
pathPRWin = 'C:\\Users\\KOMPUTER\\Dropbox\\Moje podcasty\\Polskie Radio\\'
pathRLWin = ''
pathPRLinux = '/storage/emulated/0/Moje podcasty/Polskie Radio/'
pathRLLinux = ''
# nie dozwolone znaki w nazwie pliku
replRegex = re.compile(r'(-|"|,|:|(|)|Trójka|Jedynka|polskieradio\.pl|\r\n|\?)')
# koniec edits-------------------------------------------------------------------

if platform.system() == 'Windows':
    pathPR = (pathPRWin)
    # TODO dodac kod otwierający folder zawierający podcasty
elif platform.system() == 'Linux':
    pathPR = (pathPRLinux)
else:
    print('Brak ścieżki zapisu dla systemu ' + platform.system())
    print('Zatrzymuję...')
    sys.exit()

os.makedirs(pathPR, exist_ok=True)

# TODO dodac obsługe radia lublin i ew. innych podstron PR

while True:
    print('Podaj URL strony z audycją:')
    # podcastPage = input()
    podcastPage = 'https://www.polskieradio.pl/9/325/Artykul/2414097,Muzyka-siatkowka-pasja' # url dla testów
    res = requests.get(podcastPage)

    res.raise_for_status()
    logging.debug('Res: ' + str(res))
    soup = bs4.BeautifulSoup(res.text, features='html.parser')

    # znalezienie linku do pliku
    url = ([json.loads(item['data-media'])['file'] for item in soup.find_all('a', attrs={'data-media': True})])[0]
    logging.debug('mp3Url: ' + url)

    # znalezienie tytułu
    title = soup.select('title')[0].text[3:65]
    title = replRegex.sub('', title)
    title = re.sub(' +',' ', title).rstrip()
    logging.debug('Title: ' + title)

    res = requests.get('http:' + url)
    res.raise_for_status()

    # pobranie i zapis pliku
    try:
        print('Pobieram: ' + url)
        requestFile = open(pathPR + title + '.mp3', 'wb')
        for chunk in res.iter_content(100000):
            requestFile.write(chunk)
        requestFile.close()
        print('Zapisałem: ' + pathPR + title + '.mp3')

    except OSError:
        # jeśli błąd w nazwie pliku (niedozwolone znaki)
        print("Błędna nazwa pliku: " + title + '.mp3')
        input()

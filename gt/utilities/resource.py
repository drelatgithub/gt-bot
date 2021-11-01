import requests
from bs4 import BeautifulSoup

def find_png_in_biliwiki(filename):
    url_wiki = "https://wiki.biligame.com/gt/文件:{}.png".format(filename)
    r_wiki = requests.get(url_wiki)

    if r_wiki.status_code != 200:
        raise Exception(f"Failed to get {filename}.png download link.")

    bs_wiki = BeautifulSoup(r_wiki.text, "html.parser")
    url_png = bs_wiki.body.find('div', attrs={'class': 'fullImageLink'}).find('a')['href']
    r_png = requests.get(url_png, stream=True)

    if r_png.status_code != 200:
        raise Exception(f"Failed to download {filename}.png file.")

    return r_png.content

if __name__ == "__main__":
    png_content = find_png_in_biliwiki("未来公主单个模型")
    with open("未来公主单个模型.png", "wb") as f:
        f.write(png_content)

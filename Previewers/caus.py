import re
from bs4 import BeautifulSoup

from preview import Preview

class Caus(Preview):
    def __init__(self, pattern:re.Pattern) -> None:
        super(Caus, self).__init__(pattern)
    
    async def clean_url(self, URL:str) -> str:
        URL = URL.replace('m.caus.com', 'www.caus.com')
        if not URL.startswith("http"):
            URL = "https://" + URL
        return URL

    def viewer(self, r):
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find("div",{"class":"text_title"}).text
        author = None
        content = soup.find("div",{"class":"img-wrapper"})
        return (title, author, content)

PATTERN = re.compile(r'\b(https?://)?\S*\.caus\.com/detail/\S*')
# we ignore www.caus.com/dynamicdetail/ for now
caus = Caus(PATTERN)
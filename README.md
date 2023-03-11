# Telegraph Previewer

Python code for a telegram bot that bring content of certain links to [telegra.ph](https://telegra.ph).

## Installation


```bash
pip install -r requirements.txt
```

## Run

Put your bot token and telegraph api token in `token.py` (**add this file to .gitignore** after doing so), and then

```bash
python3.9 bot.py
```

Python 3.9 is recommended. The dependent `lxml` is buggy for Python 3.10+.

**Note**: If you want to use this in a group, talk to [@botfather](https://t.me/botfather) on telegram to **turn off** group privacy mode.

## Add your own previewer

In the code we included a sample previewer for [caus.com](https://caus.com).

```python
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
caus = Caus(PATTERN)
```

To add your own, create a file follow this pattern. And add it to `bot.py`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

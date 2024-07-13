import json
import re

HOMEPAGE_PATH = '/Users/boy/Documents/代码/CILab'
PUBS_PATH = './data/paper.json'
MODE = 'en'


def replace(start_comment, end_comment, item, file_src):
    with open(file_src, "r", encoding="utf-8") as f:
        src = f.read()

    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n\n{item}\n\n{end_comment}"
    if re.search(pattern, src) is None:
        print(
            f"can not find section in src, please check it, it should be {start_comment} and {end_comment}"
        )
    new_src = re.sub(pattern, repl, src)
    with open(file_src, "w", encoding="utf-8") as f:
        f.write(new_src)

class Publication:
    def generate(self):
        item = ''
        item += '<li>\n'

        item += f'[<b>{self.conf}</b>]\n'
        item += f'{self.author}.\n'

        item += f'<a href="{self.url}" target="_blank"> "{self.title}"</a>,\n'

        if hasattr(self, 'appear'):
            item += 'to appear '
        if self.proceeding.startswith('Proceeding'):
            item += 'in '
        item += f'<i>{self.proceeding}</i>,\n'
        item += f'{self.info}.\n'

        if MODE == 'zh' and hasattr(self, 'ccfa'):
            item += '<span class="ccf-A">(<b>CCF A类</b>)</span>\n'

        if hasattr(self, 'pdf'):
            item += (f'<a class="btn btn-download-pdf btn-download" href="{self.pdf}" target="_blank"><span class="icon-pdf icon"></span>PDF</a>\n')
        if hasattr(self, 'bibtex'):
            item += (
                f'<button type="button" class="btn btn-download btn-download-bibtex" data-toggle="modal" data-target="#bibtexModel" data-content="{self.bibtex}"><span class="icon-bibtex icon"></span>BibTex</button>\n')

        if hasattr(self, 'code'):
            item += (
                f'<a class="btn btn-download-github btn-download" href="{self.code}" target="_blank"><span class="icon-github icon"></span>Code&Data</a>\n')

        if MODE == 'zh' and hasattr(self, 'award_zh'):
            item += f'<b><font color="#ff0000">[{self.award_zh}]</font></b>\n'
        elif MODE == 'en' and hasattr(self, 'award_en'):
            item += f'<b><font color="#ff0000">[{self.award_en}]</font></b>\n'
        item += '</li>\n'
        return item

class Manager:
    def __init__(self):
        self.pub_dict = dict()
        with open(PUBS_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            publications = data.get('paper')

            for year, year_publications in publications.items():
                self.pub_dict[year] = []
                for item in year_publications:
                    p = Publication()
                    for key, value in item.items():
                        setattr(p, key, value)
                    self.pub_dict[year].append(p)
    def publications(self):
        item = '<div class="cil-pub-year">\n'
        for year, year_publications in self.pub_dict.items():
            item += f'<h2 id="{year}">{year}</h2>\n'
            item += '<ol>\n'
            for pub in year_publications:
                item += pub.generate()

            item += '</ol>\n'
            item += '</div>\n'

        if MODE == 'en':
            file_src = f'{HOMEPAGE_PATH}/index.html'
        else:
            file_src = f'{HOMEPAGE_PATH}/index-zh.html'
        start_comment = '<!-- publication start -->'
        end_comment = '<!-- publication end -->'
        replace(start_comment, end_comment, item, file_src)


m = Manager()
m.publications()
MODE='zh'
m.publications()
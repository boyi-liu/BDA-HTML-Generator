import json
import re

HOMEPAGE_PATH = '/Users/boy/Documents/代码/CILab'
NEWS_PATH = './data/news.json'
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

class News:
    def generate(self, pinned=False):
        item = ''
        item += '<li>\n'
        if pinned:
            item += '<span class="icon-top icon"></span>\n'
        else:
            item += '<span class="icon-bell icon"></span>\n'
        item += self.date
        item += ' '
        if MODE == 'en':
            item += self.content_en
        else:
            item += self.content_zh
        item += '\n'
        item += '</li>\n'
        return item
        
        
class Manager:
    def __init__(self):
        self.news_list = []
        with open(NEWS_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            news = data.get('news')
        
            for n in news:
                new = News() 
                for key, value in n.items():
                    setattr(new, key, value)
                self.news_list.append(new)
                
    def generate_news(self):
        item = ''
        item += '<ul>\n'
        for n in self.news_list:
            item += n.generate()
        item += '</ul>\n'
        
        if MODE == 'en':
            file_src = f'{HOMEPAGE_PATH}/news.html'
        else:
            file_src = f'{HOMEPAGE_PATH}/news-zh.html'
        start_comment = '<!-- news start -->'
        end_comment = '<!-- news end -->'
        replace(start_comment, end_comment, item, file_src)


        item = ''
        item += '<ul>\n'
        pinned_list = [news for news in self.news_list if hasattr(news, 'pin')]
        for n in pinned_list:
            item += n.generate(pinned=True)
        cnt = 0
        for n in self.news_list:
            if n in pinned_list:
                continue
            if cnt == 4:
                break
            item += n.generate()
            cnt += 1
        item += '<li>\n'
        item += '<span class="icon-bell icon"></span>\n'
        if MODE == 'en':
            item += '<a href="news.html">More...</a>'
        else:
            item += '<a href="news-zh.html">更多...</a>'
        item += '</li>'

        item += '</ul>\n'
        if MODE == 'en':
            index_src = f'{HOMEPAGE_PATH}/index.html'
        else:
            index_src = f'{HOMEPAGE_PATH}/index-zh.html'
        replace(start_comment, end_comment, item, index_src)

if __name__ == '__main__':
    m = Manager()
    m.generate_news()
    
    MODE = 'zh'
    m.generate_news()
import yaml
import re

HOMEPAGE_PATH = '/Users/boy/Documents/代码/CILab'


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

def reformat_time(original_time_str):
    def get_ordinal_suffix(day):
        """根据日期返回相应的后缀（st, nd, rd, th）"""
        if 10 <= day <= 20:
            return "th"
        elif day % 10 == 1:
            return "st"
        elif day % 10 == 2:
            return "nd"
        elif day % 10 == 3:
            return "rd"
        else:
            return "th"

    from datetime import timedelta

    cst_time = original_time_str + timedelta(hours=8)

    # formatted_time_str = cst_time.strftime("%b %d") + "th " + cst_time.strftime("%Y %H:%M:%S") + " CST"

    day_suffix = get_ordinal_suffix(cst_time.day)
    formatted_day = cst_time.strftime("%d").lstrip("0")  # 去掉前导零
    formatted_time_str = cst_time.strftime("%b") + " " + formatted_day + day_suffix + " " + cst_time.strftime(
        "%Y %H:%M:%S") + " CST"

    return formatted_time_str


def load_conferences(file_path='./data/conf.yml'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data['conferences'], data['confmeta']

def print_conf(confs, meta):
    meta_name_list = [m['title'] for m in meta]
    all_item = ''
    for conf in confs:
        title = conf['title']
        item = ''
        item += '<div class="card">\n'
        item += f'\t<div class="title">{title}</div>\n'


        conf_meta = meta[meta_name_list.index(title)]
        if 'info' in conf_meta.keys():
            info = conf_meta['info']
            item += f'\t<div class="subtitle">{info}</div>\n'

        full = conf_meta['full']
        item += f'\t<div class="category">{full}</div>\n'

        item += '\t<div class="labels">\n'
        if conf_meta['isA'] == 1:
            item += '\t\t<span>CCF A</span>\n'

        if 'note' in conf.keys():
            note = conf['note']
            item += f'\t\t<span class="note">NOTE: {note}</span>\n'

        if 'info' not in conf_meta.keys():
            item += f'\t\t<span class="note">NOTE: inferred from last year</span>\n'

        item += '\t</div>\n'
        if 'info' in conf_meta.keys():
            link = conf_meta['link']
            item += f'\t<div class="link"><a href="{link}" target="_blank">{link}</a></div>\n'

        ddl = conf['deadline']

        item += f'\t<div class="info">⏰ <span class="countdown" data-deadline="{ddl}"></span> &nbsp;&nbsp; 📅 Deadline: {reformat_time(ddl)}</div>\n'
        item += '</div>\n'

        all_item += item
        all_item += '\n'


    file_src = f'{HOMEPAGE_PATH}/cfp.html'

    start_comment = '<!-- conf start -->'
    end_comment = '<!-- conf end -->'
    replace(start_comment, end_comment, all_item, file_src)

if __name__ == "__main__":
    confs, meta = load_conferences()
    print_conf(confs, meta)

from enum import Enum
import json
import re

class Status(Enum):
    TEACHER = 0
    STUDENT = 1
    PINNED = 2
    ALUMNI = 3

degree_list_zh = ['博士后', '博士生', '硕士生', '本科生']
degree_list_en = ['Postdoc', 'Ph.D', 'Master', 'Undergraduate']

HOMEPAGE_PATH = '/Users/boyiliu/Documents/代码/CILab'
PEOPLE_PATH = './data/people.json'

class Student:
    def generate(self):
        if self.status == Status.STUDENT.value:
            return self.generate_student()
        elif self.status == Status.TEACHER.value:
            return self.generate_teacher()
        else:
            return self.generate_alumni()
            
    def generate_teacher(self):
        pass
    
    def generate_student(self):
        item = ''
        item += '<div class="cil-member">\n'
        item += f'<div class="cil-member-photo"><img class="rounded-circle img-thumbnail" src="{self.img_src}"></div>\n'
        
        name = self.name_zh if MODE == 'zh' else self.name_en
        if hasattr(self, 'url'):
            name = f'<a href="{self.url}" target="_blank">{name}</a>'
        item += f'<div class="cil-member-name">{name}</div>\n'
        
        if MODE == 'zh':
            item += f'<div class="cil-member-desc">{degree_list_zh[self.degree]}, {self.year}</div>\n'
        else:
            item += f'<div class="cil-member-desc">{degree_list_en[self.degree]} {self.year}</div>\n'
        
        if hasattr(self, 'paper'):
            item += '<div class="cil-member-honor">\n'
            item += '<img src=./static/images/icon/paper.png width="18" style="margin-right: 5px;">'
            item += '<font face="Times New Roman" size="2">'
            item += self.paper
            item += '</font>\n<br>\n</div>\n'
        if hasattr(self, 'award_zh') or hasattr(self, 'award_en'):
            item += '<div class="cil-member-honor">\n'
            item += '<img src=./static/images/icon/award.png width="18" style="margin-right: 5px;">'
            item += '<font face="Times New Roman" size="2">'
            if hasattr(self, 'award_zh'):
                item += self.award_zh
            else:
                item += self.award_en
            item += '</font>\n<br>\n</div>\n'
        item += '</div>\n'
        return item
    
    def generate_alumni(self):
        item = ''
        item += '<div class="cil-member">\n'
        item += f'<div class="cil-member-photo"><img class="rounded-circle img-thumbnail" src="{self.img_src}"></div>\n'
        
        name = self.name_zh if MODE == 'zh' else self.name_en
        if hasattr(self, 'url'):
            name = f'<a href="{self.url}" target="_blank">{name}</a>'
        item += f'<div class="cil-member-name">{name}</div>\n'
        
        if MODE == 'zh':
            item += f'<div class="cil-member-desc">{degree_list_zh[self.degree]},{self.year}</div>\n'
        else:
            item += f'<div class="cil-member-desc">{degree_list_en[self.degree]} {self.year}</div>\n'
        
        if MODE == 'zh':
            item += f'<div class="cil-member-desc">毕业去向: <a href="{self.grad_des_link}" target="_blank" style="text-decoration: none">{self.grad_des_zh}</a> </div>\n' if hasattr(self, 'grad_des_zh') else ''
        else:
            item += f'<div class="cil-member-desc">Graduation Destination: <a href="{self.grad_des_link}" target="_blank" style="text-decoration: none">{self.grad_des_en}</a> </div>\n' if hasattr(self, 'grad_des_en') else ''
        item += '</div>\n'
        return item
    
class Manager:
    def __init__(self):
        self.people_list = []
        with open(PEOPLE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            people = data.get('people')
        
            for person in people:
                s = Student()
                for key, value in person.items():
                    setattr(s, key, value)
                self.people_list.append(s)
        self.alumni_phd_list = [s for s in self.people_list if s.status > 1 and s.degree <= 1]
        self.alumni_master_list = [s for s in self.people_list if s.status > 1 and s.degree_zh == 2]
        self.postdoc_list = [s for s in self.people_list if s.status == 1 and s.degree == 0]
        self.phd_list = [s for s in self.people_list if s.status == 1 and s.degree == 1]
        self.master_list = [s for s in self.people_list if s.status == 1 and s.degree == 2]
        self.intern_list = [s for s in self.people_list if s.status == 1 and s.degree == 3]

    def alumni(self):
        item = ''
        item += '<div class="cil-container">\n'
        item += '<div class="cil-team-alumni">'
        if MODE == 'zh':
            item += '<h1>博士生/博士后</h1>\n'
        else:
            item += '<h1>Ph.D/Postdoc</h1>\n'
        item += '<div class="cil-member-list">\n'

        for phd in self.alumni_phd_list:
            item += phd.generate_alumni()
        item += '</div>\n' * 3

        item += '<div class="cil-container">\n'
        item += '<div class="cil-team-alumni">'
        if MODE == 'zh':
            item += '<h1>硕士生</h1>\n'
        else:
            item += '<h1>Master</h1>\n'
        item += '<div class="cil-member-list">\n'
        for m in self.alumni_master_list:
            item += m.generate_alumni()
        item += '</div>\n' * 3

        if MODE == 'zh':
            file_src = f'{HOMEPAGE_PATH}/alumni-zh.html'
        else:
            file_src = f'{HOMEPAGE_PATH}/alumni.html'
        start_comment = '<!-- alumni start -->'
        end_comment = '<!-- alumni end -->'
        replace(start_comment, end_comment, item, file_src)

        # === add to index.html ===
        self.selected_list = [m for m in (self.alumni_master_list + self.alumni_phd_list) if m.status == 2]

        item = ''
        item += '<div class="cil-member-list">\n'

        for s in self.selected_list:
            item += s.generate_alumni()
        item += '\n'

        if MODE == 'zh':
            file_src = f'{HOMEPAGE_PATH}/index-zh.html'
        else:
            file_src = f'{HOMEPAGE_PATH}/index.html'

        start_comment = '<!-- alumni start -->'
        end_comment = '<!-- alumni end -->'
        replace(start_comment, end_comment, item, file_src)

    
    def student(self):
        item = ''
        item += '<div class="cil-team-student">\n'

        if MODE == 'en':
            item += '<h1>Postdoc Students</h1>'
        else:
            item += '<h1>博士后</h1>'

        item += '<div class="cil-member-list">\n'
        for postdoc in self.postdoc_list:
            item += postdoc.generate()
        item += '</div>\n'

        if MODE == 'en':
            item += '<h1>Ph.D Students</h1>'
        else:
            item += '<h1>博士生</h1>'

        item += '<div class="cil-member-list">\n'
        for phd in self.phd_list:
            item += phd.generate()
        item += '</div>\n'

        if MODE == 'en':
            item += '<h1>Master Students</h1>'
        else:
            item += '<h1>硕士生</h1>'
        item += '<div class="cil-member-list">\n'
        for m in self.master_list:
            item += m.generate()
        item += '</div>\n'

        if MODE == 'en':
            item += '<h1>Undergraduate Interns</h1>'
        else:
            item += '<h1>本科生</h1>'
        item += '<div class="cil-member-list">\n'
        for m in self.intern_list:
            item += m.generate()
        item += '</div>\n'
        
        item += '</div>\n'

        if MODE == 'en':
            file_src = f'{HOMEPAGE_PATH}/index.html'
        else:
            file_src = f'{HOMEPAGE_PATH}/index-zh.html'
        start_comment = '<!-- student start -->'
        end_comment = '<!-- student end -->'
        replace(start_comment, end_comment, item, file_src)
               
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
    
if __name__ == "__main__":
    m = Manager()

    MODE='zh'
    m.alumni()
    m.student()

    MODE='en'
    m.alumni()
    m.student()
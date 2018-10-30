import requests
from bs4 import BeautifulSoup
import operator

id = input('Your id:')
req = requests.get('https://www.acmicpc.net/user/'+id)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

# get my pages
ranks = soup.select('tr:nth-of-type(1) > td')
page = int(int(ranks[0].text) / 100) + 1

#get my prob
my_problems = soup.select('div.panel-body > span > a')
problems = {}
for prob in my_problems:
    try:
        number = int(prob.text)
        problems[number] = -1
    except (TypeError, ValueError):
        pass

#get competitors

req = requests.get('https://www.acmicpc.net/ranklist/'+page.__str__())
html = req.text
soup = BeautifulSoup(html,'html.parser')

competitors = soup.select('tr > td:nth-of-type(2) > a')

for comp in competitors:
    req = requests.get('https://www.acmicpc.net/user/'+comp.text.strip())
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    comp_problems = soup.select('div.panel-body > span > a')
    for prob in comp_problems:
        try:
            number = int(prob.text)
            if number in problems:
                if problems[number] != -1:
                    problems[number] += 1
            else:
                problems[number] = 1
        except (TypeError, ValueError):
            pass
    print('https://www.acmicpc.net/user/'+comp.text.strip())
file = open(str(page)+"page.md",encoding='utf-8',mode="w")
file.write('|number|name|links|solved|\n')
file.write('|:---:|:---:|:---:|:----:|\n')
sort_prob = sorted(problems.items(), key=operator.itemgetter(1))
sort_prob.reverse()
for prob in sort_prob:
    if (prob[1] == -1):
        pass
    else:
        file.write("|"+str(prob[0])+"|"+str(prob[1])+"|[link]("+"icpc.me/"+str(prob[0])+")||\n")

import requests
from datetime import time
from contextlib import closing
from bs4 import BeautifulSoup
import json

def main():
    list_url_start = 'https://www.imdb.com/list/ls052535080/?sort=alpha,asc'
    url_suffix = "&st_dt=&mode=detail&page="
    tvtropes_link = "https://tvtropes.org/pmwiki/pmwiki.php/Literature/OneThousandAndOneMoviesYouMustSeeBeforeYouDie"
    print("hello world")
    
    #tropes = BeautifulSoup('https _tvtropes.org_pmwiki_pmwiki.php_Literature_OneThousandAndOneMoviesYouMustSeeBeforeYouDie.html', 'html.parser')
    with open(r"C:\Users\Neha Singh\Documents\Projects\tropesvis\python-virtual-env\env\tropes.html", 'r') as f:
        t = f.read()
    tropes = BeautifulSoup(t, 'html.parser')
    
    alternatePage = requests.get(tvtropes_link)
    tropeSoup = BeautifulSoup(alternatePage.text, 'html.parser')
    tropeSoup = tropeSoup.select("#folder0")[0].ul.find_all("a", class_="twikilink")
    
    page = requests.get(list_url_start)
    soup = BeautifulSoup(page.text, 'html.parser')
    parsedSoup = []
    #puts the html page into a file to extract stuff at will
    parsedSoup.append(soup.find_all("div", class_="lister-item-content"))
    """
    tropeString = BeautifulSoup(tropes.text, 'html.parser').prettify()
    tropeString = tropeString.decode('utf-8', 'ignore')
    """
    url_root = list_url_start + url_suffix
    #parsedSoup = finish_imdb_soup(url_root, parsedSoup)    #10 pages on imdb; scrape them all into one file
    list = []
    list2 = []
    
    tropeDict = {'name': '', 'tropes': []}
    list = imdb_alphabetical_list(parsedSoup, list)
    list2 = tvtropes_json(tropeSoup, list2, tropeDict)
    print("printing...")
    """
    with open("imdblist.txt", "w") as f:
        for i in list:
            print(i, file=f)
    with open("troperef.txt", "w") as f:
        print(tropeSoup, file=f)
    """
    #with open("tvtropeslist.txt", "w") as f:
    #    print(tropeSoup.prettify().encode("utf-8"), file=f)
    """
    #now that we have the data, we extract it to a JSON file
    dict = {}
    dict['movies'] = []
    #dict = make_json(parsedSoup, dict)
    #with open("metadata.txt", "w") as f:
    #    json.dump(dict, f)
    """
    """
    #1001 movies end up on 11 pages, so scrape list items from each of those into the same object
    """
def finish_imdb_soup(url_root, parsedSoup):
    counter = 2
    print("making the soup...")
    while counter < 12:
        new_url = url_root + str(counter)
        page = requests.get(new_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        #with open("pageref.txt", "a") as f:
        parsedSoup.append(soup.find_all("div", class_="lister-item-content"))
        counter += 1
    return parsedSoup


def make_json(parsedSoup, dict):
    print("making json...")
    for sublist in parsedSoup:
        for movie in sublist:
            subdict = {'name': '', 'year': '', 'genres': '', 'director': '', 'stars': ''}
            subdict['name'] = str(movie.h3.a.string)
            subdict['year'] = str(movie.h3.find("span", class_="lister-item-year text-muted unbold").string)
            genreString = str(movie.p.find("span", class_="genre").string).strip()
            genreList = genreString.split(",")
            """
            counter = 0
            while counter < len(genreList):
                genreList[counter] = genreList[counter].strip()
                counter += 1
            """
            subdict['genres'] = genreList
            starsString = str(movie.find("p", class_="").next_sibling.string).strip()
            starsList = starsString.split(",")
            subdict['stars'] = starsList
            dict['movies'].append(subdict)
    return dict

def imdb_alphabetical_list(parsedSoup, list):
    for sublist in parsedSoup:
        for movie in sublist:
            list.append(str(movie.h3.a.string))
    return list

"""
    at this point recall: the trope soup is a LIST of <a> tags
"""
def tvtropes_json(tropeSoup, list2, tropeDict):
    tvtropes_url_root = "https://tvtropes.org"
    for item in tropeSoup:
        tropeDict['name'] = str(item.string)
        pageUrl = tvtropes_url_root + str(item.get("href"))
        tropePage = requests.get(pageUrl)
        time.sleep(1)
    return list2

if __name__ == "__main__": 
    main()
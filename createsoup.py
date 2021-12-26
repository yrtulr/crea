import requests
from bs4 import BeautifulSoup

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def create_dust(url):
    res = requests.get(url)
    res.raise_for_status()
    dust = BeautifulSoup(res.text, "lxml")
    return dust

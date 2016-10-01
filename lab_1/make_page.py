from lxml import etree
from urllib.request import HTTPError, urlopen
from cleaner import clean_text


def make_page(root, url, parser):
    print("Processing url: ", url, end='')
    try:
        tree = etree.parse(urlopen(url), parser)
    except HTTPError:
        print("     ... url not found!")
        return
    texts = clean_text(tree.xpath("//text()"))
    images = tree.xpath("//img/@src")
    page = etree.SubElement(root, "page", url=url)
    for text in texts:
        add_text(page, text)
    for image in images:
        add_image(page, image)
    print("     ... done.")


def add_text(root, found_text):
    text = etree.SubElement(root, "fragment", type="text")
    text.text = found_text


def add_image(root, url_image):
    image = etree.SubElement(root, "fragment", type="image")
    image.text = url_image
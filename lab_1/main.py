from lxml import etree
from parsers import parse_link, parse_shop_url
from io import StringIO


def get_amount_images(page, parser):
    tree = etree.parse(StringIO(page), parser)
    images = tree.xpath("//fragment[@type = \"image\"]")
    url = tree.xpath("/page/@url")
    print("Amount of images on {0}: {1}".format(url[0], str(len(images))))


def extract_pages(xml_file):
    file = open(xml_file)
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(file, parser)
    pages = tree.xpath("//page")
    for page in pages:
        get_amount_images(etree.tostring(page, encoding="unicode"), parser)
    file.close()


xml_file = open("football.xml", "wb")
xml_file2 = open("moyo.xml", "wb")
parser = etree.HTMLParser()
base_url = 'http://football.ua'
shop_url = 'http://www.moyo.ua/gadgets/roboti/robot_pyle_i_chist/'
parse_link(base_url, parser, xml_file)
parse_shop_url(shop_url, parser, xml_file2)
xml_file.close()
xml_file2.close()
extract_pages("football.xml")

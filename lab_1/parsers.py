from urllib.request import Request
from make_page import make_page, etree, urlopen
from cleaner import clean_url, clean_text
from process_shop import process_product


def parse_link(base_url, parser, xml_file):
    tree = etree.parse(urlopen(base_url), parser)
    urls = clean_url(tree.xpath("//a/@href"), base_url=base_url)
    root = etree.Element("data")
    make_page(root, base_url, parser)
    parse_urls(root, urls, parser, limit=19)
    xml_file.write(etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True))
    print("All urls have been parsed and XMLed.")


def parse_urls(root, urls, parser, limit):
    count = 1
    for url in urls:
        if limit == count:
            break
        make_page(root, url, parser)
        count += 1


def parse_shop_url(shop_url, parser, xml_file):
    tree = etree.parse(urlopen(Request(shop_url, headers={'User-Agent': 'Mozilla'})), parser)
    images = tree.xpath("//div[@class = \"goodsitem_inner\"]/a[@class = \"goods_image\"]/img/@src")
    titles = clean_text(tree.xpath("//div[@class = \"goodsitem_inner\"]/a[@class = \"goods_title ddd\"]/text()"))
    prices = clean_text(tree.xpath("//div[@class = \"goodsitem_inner\"]//div[@class = \"goods_price\"]/text()"))
    root = etree.Element("shop")

    process_product(root, images, titles, prices, limit=20)
    print("Processing shop: done.")
    xml_file.write(etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True))

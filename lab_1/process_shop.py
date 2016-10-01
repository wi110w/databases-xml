from lxml import etree


def process_product(root, images, titles, prices, limit):
    count = 0
    for image, title, price in zip(images, titles, prices):
        if count == limit:
            break
        product = etree.SubElement(root, "product", type="robot")
        process_images(product, image)
        process_titles(product, title)
        process_prices(product, price)
        count += 1


def process_images(root, url_image):
    image = etree.SubElement(root, "image", src=url_image)


def process_titles(root, text):
    title = etree.SubElement(root, "title")
    title.text = text


def process_prices(root, number):
    price = etree.SubElement(root, "price")
    price.text = number

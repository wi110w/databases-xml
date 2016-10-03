## About lab
Lab #1 project for course "Databases. XML". Variant #5
## Goals
* Fetch 20 HTML pages starting from `http://football.ua/` parsing images and texts. Next page of this site use as one of hyperlinks on current page.
Parsing results save as XML file of the following structure:
```xml
<data>
<page url=”wwww.example.com/index.hml”>
<fragment type=”text”>
.... text data
</fragment>
<fragment type=”image”>
.... image url
</fragment>
</page>
<page url=”wwww.example.com/page.hml”>
<fragment type=”text”>
.... text data
</fragment>
<fragment type=”image”>
.... image url
</fragment>
</page>
...
</data>
```

* Using XPATH get count of images on each page
* Fetch name, price and image for 20 products from online store `moyo.ua` using XPATH, save as XML file
* Transform product list XML into HTML table using XSLT

## Usage
* run `main.py` to get all tasks done.

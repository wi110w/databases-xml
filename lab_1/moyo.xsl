<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="utf-8" />
  <xsl:template match="/">
    <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
    <html>
      <head>
        <title>List of robots</title>
      </head>
      <body>
        <h2>Robots-hoovers</h2>
        <table border="1">
          <tr>
            <th>Image</th>
            <th>Description</th>
            <th>Price</th>
          </tr>
          <xsl:for-each select="/shop/product">
            <xsl:sort select="title" />
            <tr>
              <td>
                  <img>
                    <xsl:attribute name="src">
                      <xsl:value-of select="image/@src" />
                    </xsl:attribute>
                  </img>
             </td>
              <td><xsl:value-of select="title" /></td>
              <td><xsl:value-of select="price" /></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>

import os
import lxml.etree as ET
from xml.dom import minidom


#En parser defineres her, så karaktererne æ, ø og å indlæses korrekt
utf_parser = ET.XMLParser(encoding='ISO-8859-1')

infile = ET.parse(r'C:\Sti\themes.xml')   #Input themes-xml
tree = infile
irrelevante_temaer = ["theme-gst-orto_foraar_jylland2004_40cm", "theme-gst-orto_foraar_bornholm2006_40cm"]
#irrelevante_temaer-listen er listen over de temaer, der skal udkommenteres, tema-navnet fra themes-xml benyttes - benyt theme-navnet fra xml-filen

temanavne = {"Ortofoto forår Jylland 2004_40cm (SDFE)" : "Ortofoto forår Jylland 2004", "Ortofoto forår Bornholm 2006_40cm (SDFE)" : "Ortofoto forår Bornholm 2006"}
#temanavne indeholder navne-par adskilt af et kolon. Temanavnet til venstre for kolonnet skal være temaets displayname fra themes.xml-filen, og dette bliver så erstattet af det man har til højre for kolonnet.

outfile = r'C:\Sti\New_themes.xml' #Output themes-xml, husk altid at lave backup af den gamle themes.xml-fil før den overskrives.

def comment_element(tree, irrelevante_temaer):  #Funktion til udkommentering
    for logger in tree.xpath('//theme'):
        for name in irrelevante_temaer:
            if logger.get('name') == name:
                print (name)
                logger.getparent().replace(logger, ET.Comment(ET.tostring(logger, encoding='unicode')))
    return tree


comment_element(tree, irrelevante_temaer)   #Funktionskald

with open(outfile, 'wb') as f:
            f.write(ET.tostring(tree, encoding='ISO-8859-1'))

with open(outfile, 'r') as fileout:
    filedata = fileout.read()


for key in temanavne: #Disse to linjer udkommenteres, hvis man ikke ønsker at omdøbe nogle af temaerne.
    filedata = filedata.replace(key, temanavne[key])


with open(outfile, 'w') as fileout:
    fileout.write(filedata)


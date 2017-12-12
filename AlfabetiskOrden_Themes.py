import os
import lxml.etree as ET

#En parser defineres her, så karaktererne æ, ø og å indlæses korrekt
utf_parser = ET.XMLParser(encoding='utf-8')

#Her defineres hvilke parametre i XML-filerne den alfabetiske sortering baseres på
def get_sort_attribute_tag_value(node):
        return node.find('themeselector').find('displayname').text

#Denne funktion laver en liste over samtlige filer med navnet themes.xml i en mappe samt dens undermappe
def list_files(dir):
    themes = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name == 'themes.xml':
                themes.append(os.path.join(root, name))
            else:
                continue
    return themes

#Her sorteres temaerne i hver enkelt themes.xml fil alfabetisk
def alpha_sorting(xmllist):
    for file in xmllist:

        with open(file) as f: #XML-filen indlæses
            xml_node = ET.fromstring(f.read().encode('utf-8'), parser=utf_parser)

        #Alle temaer i filen findes
        theme_nodes = xml_node.findall('theme')

        #Temaerne fjernes fra den indlæste XML-fil
        for theme_node in theme_nodes:
            xml_node.remove(theme_node)
        #Temaerne forsøges sorteret. Ved attributeError gives en fejlmeddelse, og derefter kører funktionen forfra og indlæser næste fil
        #AttributeError kan opstå, hvis filen ikke indeholder nogen temaer, der kan sorteres
        try:
            theme_nodes.sort(key=get_sort_attribute_tag_value, reverse=True)
        except AttributeError:
            print ('error: ' + file)
            continue

        #De alfabetisk sorterede temaer indsættes i den indlæste XML-filen, hvorefter output-filen defineres
        for theme_node in theme_nodes:
            xml_node.append(theme_node)
        output = os.path.join(os.path.dirname(file), 'sorted_themes.xml')
        print (output)
        #Den sorterede temafil skrives til den definerede output-fil
        with open(output, 'wb') as f:
            f.write(ET.tostring(xml_node, encoding='ISO-8859-1'))


#Funktionerne list_files og alpha_sorting kaldes, når scriptet køres
#Scriptet beder brugeren om et input, her skal man indsætte stien til mappen med de tema-filer, der skal sorteres (funktionen kigger også efter tema-filer i undermapperne).
if __name__ == '__main__':

    files = list_files(input('Indtast sti: '))
    alpha_sorting(files)

#coding: utf-8
import xml.etree.ElementTree as et
import os
import glob

#funktion, der fjerner værdier, der optræder to gange eller mere
def uniq(liste):
	unik = []
	for x in liste:
		if x not in unik:
			unik.append(x)
	return unik

#funktionen, der skriver en txt fil. Den placeres i den samme folder, som python scriptet ligger i
def txt_result(liste, fil_navn):
	output = open(init_folder + os.sep + fil_navn, "w")
	for item in liste:
		output.writelines(item + "\n")

#Folderen hvor .py filen ligger i
init_folder =  os.path.dirname(os.path.realpath(__file__))


#funktion som laver de lister, der skal sammenlignes
def func(theme_files, ds_fil, ts_fil):

    #Datasources i targetset xml-filen

    ts_liste = []
    if os.path.isfile(ts_xml):
        ts_tree = et.parse(ts_fil)
        ts_root = ts_tree.getroot()
        for target in ts_root.iter('datasource'):
            ts_ds = target.get('name')
            ts_liste.append(ts_ds)
        ts_liste = uniq(ts_liste)


    #Datasources i temafiler
	tema_ds_liste = []
	for fname in theme_files:
		tree = et.parse(fname)
		root = tree.getroot()
		for layer in root.iter('layer'):
			theme_ds_name = layer.get('datasource')
			tema_ds_liste.append(theme_ds_name)
	tema_ds_liste = uniq(tema_ds_liste)



	#Datasources i datasource xml-filen
	ds_liste = []
	ds_tree = et.parse(ds_fil)
	ds_root = ds_tree.getroot()
	for name in ds_root.iter('datasource'):
		ds_ds_name = name.get('name')
		ds_liste.append(ds_ds_name)
	ds_liste = uniq(ds_liste)





	#sammenligne lister
	tema_ds = [] # i theme men ikke i ds_k240
	for ds in tema_ds_liste:
		if ds is None:
			pass
		else:
			if ds in ds_liste:
				pass
			else:
				tema_ds.append(ds)
	txt_result(tema_ds, outname1)

	ds_tema = [] #i datasource men ikke i theme eller targetset
	for ds in ds_liste:
		if ds is None:
			pass
		else:
			if ds in tema_ds_liste or ds in ts_liste:
				pass
			else:
				ds_tema.append(ds)

	txt_result(ds_tema, outname2)



#func(theme_files, ds_xml)

#Nedenstående får scriptet til at gennemgå samtlige moduler
#Jeg har brugt modullisten fra admin-konsollen under "Configuration", og kopieret samtlige rækker til excel og gemt som csv (husk kommaseparering IKKE semikolon).
import csv
with open("Sti til csv indeholdende alle moduler inkl. rootdir", 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

#Her gennemgås hver enkelt modul, først testes det om der findes en datasources.xml fil under modulet.Entry[4] er i dette tilfælde rootdir for modulet.
for entry in your_list:
    datasource_xml = (("Sti til modulmappe") + "/" + entry[4] + "/" + "datasources" + "/" + "datasources.xml")

    if os.path.isfile(datasource_xml):
        theme_files = glob.glob(("Sti til modulmappe") + "/" + entry[4] + "/" + "themes" + "/" + "*.xml")

        ds_xml_sti = (("Sti til modulmappe") + "/" + entry[4] + "/" + "datasources")
        ds_xml_navn = ("datasources")
        ds_xml = ds_xml_sti + os.sep + ds_xml_navn + '.xml'

        ts_xml_sti = (("Sti til modulmappe") + "/" + entry[4] + "/" + "queries")
        ts_xml_navn = ("targetset")
        ts_xml = ts_xml_sti + os.sep + ts_xml_navn + '.xml'
        #entry[0] er navnet på modulet, hvilket sørger for at hver enkelt output får et navn svarende til det undersøgte modul.
        outname1 = entry[0] + "_" + "tema_ikke_i_ds.txt"
        outname2 = entry[0] + "_" + "ds_ikke_tema.txt"

        func(theme_files, ds_xml, ts_xml)
    else:
        continue


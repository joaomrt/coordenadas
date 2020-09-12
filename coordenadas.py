from tkinter import *
from tkinter.filedialog import FileDialog
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import os
import sys
import blocos
import funcs
import conversor
import dxfwrite
from dxfwrite import DXFEngine as dxf
import pyproj
from idlelib import *

sep = os.sep
#lib_path = os.path.abspath('.'+sep+'lib'+sep) #permite ir buscar modulos a nossa pasta, amazing!
#sys.path.append(lib_path)
#print (lib_path)

wgs84 = pyproj.Proj('+init=EPSG:4326') # LatLon with WGS84 datum used by GPS units and Google Earth
pttm06 = pyproj.Proj('+proj=tmerc +lat_0=39.66825833333333 +lon_0=-8.133108333333334 +k=1 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs')#PT-TM06/ETRS89 EPSG:3763
datum73IPCC = pyproj.Proj('+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=180.598 +y_0=-86.98999999999999 +ellps=intl +units=m +no_defs')#Datum 73 Hayford Gauss IPCC "ESRI:102161"
datum73IGeoE = pyproj.Proj('+proj=tmerc +lat_0=39.66666666666666 +lon_0=-8.131906111111112 +k=1 +x_0=200180.598 +y_0=299913.01 +ellps=intl +units=m +no_defs')#Datum_73_Hayford_Gauss_IGeoE "ESRI:102160"
datumOSGB36 = pyproj.Proj('+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +datum=OSGB36 +units=m +no_defs')#OSGB-1936-EPSG:27700
datumLambert93 = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')#Lambert-93-EPSG:2154

###########################################################################################################################
######################################### INICIO DO INTERFACE #############################################################

titulo = '* * * * * COORDENADAS * * * * *   GROUPFIX N - Engenharia e Serviços v2.2.0\n\n'

class Application2(Frame):

    def ajuda_help(self):
        self.texto1.insert(END, '\nOs ficheiros de texto devem estar separados por tabs, sem nomes de colunas no '+
                           '\nformato: nome_do_ponto coordenada_x coordenada_y.\n'+
                           'Os ficheiros dxf devem ser guardados no formato DXF R12 no Autocad\n'+
                           'para ser possível converter em formato kml.\n'+
                           'Os ficheiros kml exportados do sistema devem ser guardados novamente para \nficarem devidamente formatados.\n'+
                           '\nHelpdesk: joao.teixeira@groupfix.pt\n\n')
        self.texto1.see(END)

    def actualizar_wgs84(self):

        self.zona_nova = self.zona.get()
        self.letra_nova = self.letra.get()
        self.comentario_novo = self.comentario.get()
        funcs.ver_datum()
        try:
            f = open(funcs.caminho+'settings.ini', 'w')
            f.write(self.zona_nova+','+self.letra_nova+','+self.comentario_novo+','+funcs.datum1)
            f.close()
            self.texto1.insert(END, '\nA grelha de coordenadas UTM predefinida foi alterada para '+
                               self.zona_nova+', '+self.letra_nova+', '+self.comentario_novo+'.\n')
            self.texto1.see(END)
        except:
            self.texto1.insert(END, '\nERRO DE ESCRITA. O ficheiro settings.ini não tem permissão para o user '+
                               'actual.\nEditar as permissões do user na secção de segurança das propriedades do\nficheiro ' +
                               'settings.ini na pasta c:/programas/groupfix/coordenadas.\n')
            self.texto1.see(END)

    def actualizar_datum(self, datum73):

        self.datum_novo = datum73

        f = open('settings.ini', 'r')
        line = f.readline()
        zona_texto = line.split(',')
        zona_texto_num = zona_texto[0]
        zona_texto_letra = zona_texto[1]
        zona_texto_comentario = zona_texto[2]
        f.close()

        try:
            f = open('settings.ini', 'w')
            texto1 = str(zona_texto_num)+','+str(zona_texto_letra)+','+str(zona_texto_comentario)+','+str(self.datum_novo)
            f.write(texto1)
            f.close()
            self.texto1.insert(END, '\nProjecção alterada para '+self.datum_novo+'.\n')
            #self.texto1.insert(END,'\nDatum 73 alterado para '+s.upper()+'.')
            self.texto1.see(END)
        except:
            self.texto1.insert(END, '\nERRO DE ESCRITA. O ficheiro settings.ini não tem permissão para o user '+
                               'actual.\nEditar as permissões do user na secção de segurança das propriedades do\nficheiro ' +
                               'settings.ini na pasta c:/programas/groupfix/coordenadas.\n')
            self.texto1.see(END)

    def botoes(self):

        c = open(funcs.caminho+'settings.ini', 'r')
        line = c.readline()
        zona_texto = line.split(',')
        zona_texto_num = zona_texto[0]
        zona_texto_letra = zona_texto[1]
        zona_texto_comentario = zona_texto[2]
        datum = zona_texto[3]
        c.close()

        #self.QUIT = Button(self)
        #self.QUIT['text'] = 'SAIR'
        #self.QUIT['fg'] = 'red'
        #self.QUIT['command'] = self.quit
        #self.QUIT.grid(row=1,column=9, sticky=E)

        self.tag_wgs_utm = Label(self, text='WGS84/UTM')
        self.tag_wgs_utm.grid(row=2, column=2)

        self.tag_datum73 = Label(self, text='Datum:')
        self.tag_datum73.grid(row=2, column=6)

        self.tag_espaco_branco = Label(self, text='  ')
        self.tag_espaco_branco.grid(row=2, column=9)

        datum73 = StringVar(self)
        datum73.set(datum) # default value

        self.lista = OptionMenu(self, datum73, "PT-TM06", "IPCC", "IGeoE", "OSGB36", "Lambert93", command=self.actualizar_datum).grid(row=2, column=7)

        self.ajuda = Button(self)
        self.ajuda['text'] = 'Ajuda'
        self.ajuda['command'] = self.ajuda_help
        self.ajuda.grid(row=0, column=1, sticky=W)
        #tip_ajuda = ToolTip(self.ajuda, 'Ajuda')

        self.texto1 = Text(self)
        self.texto1.grid(row=1, column=1, columnspan=9)
        self.texto1.insert(INSERT, titulo)

        self.espaco = Label(self, text=' ') #espacamento 1 linha
        self.espaco.grid(row=7, column=1)

        self.local_wgs84 = Label(self, text='Grelha UTM: ')
        self.local_wgs84.grid(row=8, column=1)

        self.comentario_lab = Label(self, text='Comentário ')
        self.comentario_lab.grid(row=8, column=2, sticky=E)
        self.comentario = Entry(self, width=13)
        self.comentario.grid(row=8, column=3, sticky=W)
        self.comentario.delete(0, END)
        self.comentario.insert(0, zona_texto_comentario)

        self.zona_lab = Label(self, text='Zona (número)')
        self.zona_lab.grid(row=8, column=4)
        self.zona = Entry(self, width=3)
        self.zona.grid(row=8, column=5, sticky=W)
        self.zona.delete(0, END)
        self.zona.insert(0, zona_texto_num)

        self.letra_lab = Label(self, text=' Zona (letra)')
        self.letra_lab.grid(row=8, column=6)
        self.letra = Entry(self, width=3)
        self.letra.grid(row=8, column=7, sticky=W)
        self.letra.delete(0, END)
        self.letra.insert(0, zona_texto_letra)

        self.botao100 = Button(self, text='Predefinir', command=self.actualizar_wgs84)
        self.botao100.grid(row=8, column=8, sticky=W)
        #tip_botao100 = ToolTip(self.botao100, 'Grava de forma permanente a grelha de coordenadas UTM / Só funciona em modo admin\nN - Hemisfério Norte; qualquer outra letra - Hemisfério Sul')

        self.botao01 = Button(self, text='Tab WGS-KML', command=wgs2kml)
        self.botao01.grid(row=3, column=2, sticky=N+S+E+W)
        #tip_botao01 = ToolTip(self.botao01, 'Converte uma listagem de pontos com coordenadas WGS84 para um ficheiro kml. Pode ter uma quarta coluna com observações')

        self.botao02 = Button(self, text='Tab UTM-KML', command=utm2kml)
        self.botao02.grid(row=3, column=3, sticky=N+S+E+W)
        #tip_botao02 = ToolTip(self.botao02, 'Converte uma listagem de pontos com coordenadas UTM para um ficheiro kml')

        self.botao03 = Button(self, text='KML-Tab UTM', command=kml2utm)
        self.botao03.grid(row=3, column=4, sticky=N+S+E+W)
        #tip_botao03 = ToolTip(self.botao03, 'Converte pontos existentes dentro de um ficheiro kml numa listagem de coordenadas UTM (txt)')

        self.botao06 = Button(self, text='KML-DXF_UTM', command=kml2dxf_wgs84)
        self.botao06.grid(row=4, column=4, sticky=N+S+E+W)
        #tip_botao06 = ToolTip(self.botao06, 'Converte os pontos e linhas de um ficheiro kml para um ficheiro CAD (dxf) com coordenadas UTM')

        self.botao07 = Button(self, text='DXF_UTM-KML', command=dxf2kmlwgs84)
        self.botao07.grid(row=4, column=2, sticky=N+S+E+W)
        #tip_botao07 = ToolTip(self.botao07, 'Converte textos e linhas de um ficheiro CAD (dxf) com coordenadas UTM para um ficheiro kml')

        self.botao09 = Button(self, text='KML-Tab WGS', command=kml2wgs84)
        self.botao09.grid(row=4, column=3, sticky=N+S+E+W)
        #tip_botao09 = ToolTip(self.botao09, 'Extrai as coordenadas WGS84 de todos os pontos existentes num ficheiro kml para um ficheiro de texto')

        self.botao11 = Button(self, text='Tab Datum-WGS', command=datum73mod2wgs)
        self.botao11.grid(row=3, column=6, sticky=N+S+E+W)
        #tip_botao11 = ToolTip(self.botao11, 'Converte uma listagem de pontos com coordenadas Datum para uma listagem de coordenadas WGS84')

        self.botao12 = Button(self, text='Tab Datum-KML', command=datum73mod2kml)
        self.botao12.grid(row=3, column=7, sticky=N+S+E+W)
        #tip_botao12 = ToolTip(self.botao12, 'Converte uma listagem de pontos com coordenadas Datum para um ficheiro kml')

        self.botao13 = Button(self, text='KML-Tab Datum', command=kml2datum73mod)
        self.botao13.grid(row=3, column=8, sticky=N+S+E+W)
        #tip_botao13 = ToolTip(self.botao13, 'Converte pontos existentes dentro de um ficheiro kml numa listagem de coordenadas Datum (txt)')

        self.botao16 = Button(self, text='KML-DXF_Datum', command=kml2dxf_datum73mod)
        self.botao16.grid(row=4, column=8, sticky=N+S+E+W)
        #tip_botao16 = ToolTip(self.botao16, 'Converte os pontos e linhas de um ficheiro kml para um ficheiro CAD (dxf) com coordenadas Datum')

        self.botao17 = Button(self, text='DXF_Datum-KML', command=dxf2kmldatum73mod)
        self.botao17.grid(row=4, column=6, sticky=N+S+E+W)
        #tip_botao17 = ToolTip(self.botao17, 'Converte textos e linhas de um ficheiro CAD (dxf) com coordenadas Datum para um ficheiro kml')

        self.botao18 = Button(self, text='Tab WGS-Datum', command=wgs2datum73mod)
        self.botao18.grid(row=4, column=7, sticky=N+S+E+W)
        #tip_botao18 = ToolTip(self.botao18, 'Converte uma listagem de coordenadas WGS84 em coordenadas Datum (txt)')

        #quadro = Frame(self,width=400,height=400)
        #quadro.grid(row=1,column=10,sticky=N+S+E+W)
        #quadro.canvas1 = Canvas(quadro,width=400, height=400, bg="white")
        #quadro.canvas1.grid(row=1,column=1,sticky=N+S+E+W)
        #quadro.canvas1.create_oval(200, 200, 205, 205, fill="red")

        self.canvas1 = Canvas(self, width=400, height=400, bg="white")
        self.canvas1.grid(row=1, column=10, columnspan=2, sticky=N+S+E+W)
        #self.canvas1.create_oval(200, 200, 205, 205, fill="red")

        self.botao18 = Button(self, text='Pré-visualizar', command=preview)
        self.botao18.grid(row=2, column=10, sticky=E+W)
        #tip_botao18 = ToolTip(self.botao18, 'Desenha os pontos de uma listagem de coordenadas (Não mantém a escala nem o racio)')
        self.botao19 = Button(self, text='Limpar', command=clear)
        self.botao19.grid(row=2, column=11, sticky=E+W)
        #tip_botao19 = ToolTip(self.botao19, 'Limpa a área de desenho')

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.botoes()

class Application3(Frame):

    def ajuda_help(self):

        tkinter.messagebox.showinfo('Aviso', 'Ajuda disponível na versão profissional...')
        #mensagem=('\nNao funciona para transformar exportacoes txt do sistema do Ze para blocos Vodafone e NOS')
        #funcs.escrever(mensagem)

    def botoes3(self):

        self.ajuda = Button(self)
        self.ajuda['text'] = 'Ajuda'
        self.ajuda['command'] = self.ajuda_help
        self.ajuda.grid(row=1, column=0, sticky=W)
        #tip_botao_ajuda2 = ToolTip(self.ajuda, 'Ajuda disponível na versão profissional...')

        self.texto2 = Text(self)
        self.texto2.grid(row=2, column=1, columnspan=9, sticky=N+S+E+W)
        self.texto2.insert(INSERT, '* * * * * COORDENADAS * * * * * \n')
        self.texto2.insert(INSERT, '\nInterface de conversão de listagens txt em blocos autocad (via ficheiro .scr).\n'+
                           'Exemplos de nomes de elementos de rede: A123, AEDP123, EDP-123, CVP_123.\n'+
                           'Os ficheiros com blocos estao disponíveis na pasta de instalação deste programa.\n'+
                           'Fazer zoom para uma vista vazia antes de arrastar o ficheiro .scr para dentro do\nAutocad.\n\n')

        self.tag_nos = Label(self, text='PT')
        self.tag_nos.grid(row=3, column=1)

        self.botao31 = Button(self, text='Rede_PT', command=blocos.rede_pt)
        self.botao31.grid(row=4, column=1, sticky=N+S+E+W)
        #tip_botao31 = ToolTip(self.botao31, 'Converte uma listagem de elementos de rede em blocos autocad da PT (ficheiro .scr)')

        self.botao32 = Button(self, text='Edifícios_PT', command=blocos.edif_pt)
        self.botao32.grid(row=4, column=2, sticky=N+S+E+W)
        #tip_botao32 = ToolTip(self.botao32, 'Converte uma listagem de edifícios em blocos autocad da PT (ficheiro .scr)')

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.botoes3()

######################################### FIM DO INTERFACE ################################################################
###########################################################################################################################

###########################################################################################################################
######################################### INICIO DAS COORDENADAS ##########################################################

def x2y(strtab, conv1, conv2, strfich):

    conversao = 'Conversão Tabela '+strtab
    app2.texto1.insert(END, '\nEscolha: '+conversao)
    app2.texto1.see(END)

    funcs.t_fich="text files"
    funcs.e_fich="*.txt"

    funcs.abrir()
    if funcs.ficheiro == '':
        app2.texto1.insert(END, '\nA abertura do ficheiro falhou\n')
        app2.texto1.see(END)
        return 0

    texto = ''
    array_coord = []
    f = open(funcs.ficheiro, 'r', encoding='utf8')    #abre um ficheiro (definido abaixo) e devolve o conteudo

    while 1:
        line = f.readline()
        if not line:
            break
        #print (line) # do something
        try:
            ponto, x, y = line.split('\t', line.count('\t'))
        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.\nOs parâmetros de entrada não foram aceites.'+
                               '\nOs dados devem estar separados por tabs.\n')
            app2.texto1.see(END)
            return 0
        x = float(x)
        y = float(y)
        try:
            resultado = pyproj.transform(conv1, conv2, x, y)

        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.\nOs parâmetros de entrada nao foram aceites.'+
                               '\nAs coordenadas devem ser em Datum/UTM/WGS e as colunas nao podem ter titulos.'+
                               '\nO formato deve ser: nome_do_ponto longitude latitude\n')
            app2.texto1.see(END)
            return 0

        tup1 = (resultado[0], resultado[1])
        array_coord.append(tup1)

        texto = (texto+ponto+'\t'+str(resultado[0])+'\t'+str(resultado[1])+'\n')
    f.close()

    f2 = open(funcs.pasta+funcs.nome_fich+strfich, 'w', encoding='utf8')   #cria o ficheiro com coordenadas transformadas
    f2.write(texto)
    f2.close()

    desenha_pontos(array_coord)

    app2.texto1.insert(END, '\n'+conversao+' terminada com sucesso\n')
    app2.texto1.see(END)

def wgs2datum73mod():

    strtab = 'WGS84 para Datum'
    conv1 = wgs84
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv2 = pttm06
    if "IPCC" in funcs.datum1:
        conv2 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv2 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv2 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv2 = datumLambert93

    strfich = '_coord_datum.txt'

    x2y(strtab, conv1, conv2, strfich)

def datum73mod2wgs():

    strtab = 'Datum para WGS84'
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv1 = pttm06
    if "IPCC" in funcs.datum1:
        conv1 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv1 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv1 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv1 = datumLambert93
    conv2 = wgs84
    strfich = '_coord_WGS84.txt'

    x2y(strtab, conv1, conv2, strfich)

def x2kml(strtab, conv1, conv2, strfich):

    conversao = 'Conversão '+strtab+' para KML'
    app2.texto1.insert(END, '\nEscolha: '+conversao)
    app2.texto1.see(END)

    funcs.t_fich="text files"
    funcs.e_fich="*.txt"

    funcs.abrir()
    if funcs.ficheiro == '':
        app2.texto1.insert(END, '\nA abertura do ficheiro falhou\n')
        app2.texto1.see(END)
        return 0

    stri = ("<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://www.opengis.net/kml/2.2'><Document><name>Pontos.kml</name><StyleMap id='m_ylw-pushpin01'>"+
            '<Pair><key>normal</key><styleUrl>#s_ylw-pushpin03</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl002</styleUrl></Pair></StyleMap>'+
            "<Style id='s_ylw-pushpin03'><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>"+
            "<hotSpot x='20' y='2' xunits='pixel' yunits='pixels'/></IconStyle></Style><Style id='s_ylw-pushpin_hl002'><IconStyle><scale>1.18182</scale><Icon>"+
            "<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x='20' y='2' xunits='pixels' yunits='pixels'/>"+
            '</IconStyle></Style><Folder><name>Pontos</name>')+('\n')
    str1 = ('<Placemark>\n<name>')
    str2 = ('</name>\n')
    str3 = ('<styleUrl>#m_ylw-pushpin01</styleUrl>\n<Point>\n<coordinates>')
    str4 = ('</coordinates>\n</Point>\n</Placemark>')
    strf = ('</Folder></Document></kml>')

    texto = ''
    texto = stri
    array_coord = []
    f = open(funcs.ficheiro, 'r', encoding='utf8')    #abre um ficheiro e devolve o conteudo

    while 1:
        line = f.readline()
        if not line:
            break
        #print (line) # do something
        try:
            obs = ''
            if line.count('\t') < 3:
                ponto, x, y = line.split('\t', 2)
            else:
                ponto, x, y, obs = line.split('\t', 3)
            if "," in x:
                x = x.replace(",", ".")
                y = y.replace(",", ".")
                y = y.replace("\n", "")
        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.\nOs parâmetros de entrada não foram aceites.'+
                               '\nOs dados devem estar separados por tabs.\n')
            app2.texto1.see(END)
            return 0
        x = x.replace(",", ".")
        y = y.replace(",", ".")
        y = y.replace("\n", "")
        y = float(y)
        x = float(x)
        try:
            resultado = pyproj.transform(conv1, conv2, x, y)
        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.''\nOs parâmetros de entrada não foram aceites.'+
                               '\nAs coordenadas devem ser em UTM/Datum e as colunas nao podem ter titulos.'+
                               '\nO formato deve ser: nome_do_ponto coordenada_x coordenada_y\n')
            app2.texto1.see(END)
            return 0

        tup1 = (resultado[0], resultado[1])
        array_coord.append(tup1)
        if obs == '':
            texto = (texto+str1+ponto+str2+str3+str(resultado[0])+','+str(resultado[1])+str4+'\n')
        else:
            obs = '<description>'+obs+'</description>\n'
            texto = (texto+str1+ponto+str2+obs+str3+str(resultado[0])+','+str(resultado[1])+str4+'\n')
    f.close()

    texto = texto + strf

    f2 = open(funcs.pasta+funcs.nome_fich+strfich, 'w')   #cria o ficheiro com coordenadas transformadas
    #print(texto)
    f2.write(texto)
    f2.close()

    desenha_pontos(array_coord)

    app2.texto1.insert(END, '\n'+conversao+' terminada com sucesso\n')
    app2.texto1.see(END)

def utm2kml():

    #------codigo de escolha de zona
    z1 = app2.zona.get()
    z2 = app2.letra.get()
    letra = ''

    if z2 == 'N':
        letra = ''
    else:
        letra = ' +south'

    zona = z1 + letra
    utm_texto = '+proj=utm +zone=' + zona + ' +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    utm = pyproj.Proj(utm_texto)
    #------fim de codigo de escolha de zona

    strtab = 'Tabela UTM'
    conv1 = utm
    conv2 = wgs84
    strfich = '_coord_kml_utm-WGS84.kml'

    x2kml(strtab, conv1, conv2, strfich)

def datum73mod2kml():

    strtab = 'Tabela Datum'
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv1 = pttm06
    if "IPCC" in funcs.datum1:
        conv1 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv1 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv1 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv1 = datumLambert93
    conv2 = wgs84
    strfich = '_coord_kml_datum-WGS84.kml'

    x2kml(strtab, conv1, conv2, strfich)

def wgs2kml():

    strtab = 'Tabela WGS84'
    conv1 = wgs84 #conversao redundante mas fica de acordo com as restantes para usar a mesma funcao
    conv2 = wgs84
    strfich = '_coord_kml-WGS84.kml'

    x2kml(strtab, conv1, conv2, strfich)

def kml2x(strtab, conv1, conv2, strfich):

    conversao = 'Extracão coordenadas '+strtab+' de KML'
    app2.texto1.insert(END, '\nEscolha: '+conversao)
    app2.texto1.see(END)

    funcs.t_fich="kml files"
    funcs.e_fich="*.kml"

    funcs.abrir()
    if funcs.ficheiro == '':
        app2.texto1.insert(END, '\nA abertura do ficheiro falhou\n')
        app2.texto1.see(END)
        return 0

    nome = ''
    texto = ''
    descricao = ''
    coord = ''
    array_coord = []
    #f=open(funcs.ficheiro,'r',encoding='iso-8859-1')    #abre um ficheiro e devolve o conteudo
    f = open(funcs.ficheiro, 'r', encoding='utf-8')    #abre um ficheiro e devolve o conteudo
    str0 = 'name'
    str1 = 'coordinates'
    str2 = '<description>'
    while 1:
        line = f.readline()
        if not line:
            break
        #print (line) # do something
        if str0 in line:
            nome1 = line.split('>', 2)
            nome2 = nome1[1].split('<', 1)
            edif = nome2[0]
        if str2 in line:
            descricao1 = line
            if '/description' not in line:
                line = f.readline()
                while 1:
                    if '/description' in line:
                        descricao1 = descricao1 + line
                        descricao1 = descricao1.replace('\n', '')
                        break
                    else:
                        descricao1 = descricao1 + line
                        line = f.readline()
            descricao2 = descricao1.split('<description>', 1)
            descricao3 = descricao2[1].split('</description>', 1)
            descricao = descricao3[0]
        if str1 in line:
            coord1 = line.split('>', 2)
            coord2 = coord1[1].split('<', 1)
            coord = coord2[0]
            coord = coord.split(',', 2)
            lon = str(coord[0])
            try:
                lat = str(coord[1])
                coord = pyproj.transform(conv1, conv2, lon, lat)
                #coord=pyproj.transform(wgs84, utm, lon, lat)
                coord = str(coord)
                if descricao != '':
                    texto = (texto+edif+'\t'+coord+'\t'+descricao+'\n')
                else:
                    texto = (texto+edif+'\t'+coord+'\n')
                descricao = ''
            except:
                xpto = 0
    f.close()

    texto = texto.replace(',0', '')
    texto = texto.replace(', 0', '')
    texto = texto.replace(',', '\t')
    texto = texto.replace('  ', '\t')
    texto = texto.replace('(', '')
    texto = texto.replace(')', '')
    texto = texto.replace(', ', ',')
    texto = texto.replace('\t ', '\t')
    texto = texto.replace(' ', '_')

    #f2 = open(funcs.pasta+funcs.nome_fich+strfich, 'w', encoding='iso-8859-1')   #cria o ficheiro com coordenadas transformadas
    f2 = open(funcs.pasta+funcs.nome_fich+strfich, 'w', encoding='utf8')   #cria o ficheiro com coordenadas transformadas
    f2.write(texto)
    f2.close()

    f3 = open(funcs.pasta+funcs.nome_fich+strfich, 'r')
    while 1:
        line = f3.readline()
        if not line:
            break
        ponto_ = line.split('\t', line.count('\t'))
        ponto = ponto_[0]
        x = ponto_[1]
        y = ponto_[2]
        tup1 = (float(x), float(y))
        array_coord.append(tup1)

    desenha_pontos(array_coord)
    f3.close()

    app2.texto1.insert(END, '\n'+conversao+' terminada com sucesso\n')
    app2.texto1.see(END)

def kml2utm():

    #------codigo de escolha de zona
    z1 = app2.zona.get()
    z2 = app2.letra.get()
    letra = ''

    if z2 == 'N':
        letra = ''
    else:
        letra = ' +south'

    zona = z1 + letra
    utm_texto = '+proj=utm +zone=' + zona + ' +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    utm = pyproj.Proj(utm_texto)
    #------fim de codigo de escolha de zona

    strtab = 'utm'
    conv1 = wgs84
    conv2 = utm
    strfich = '_coord_utm.txt'

    kml2x(strtab, conv1, conv2, strfich)

def kml2datum73mod():

    strtab = 'Datum'
    conv1 = wgs84
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv2 = pttm06
    if "IPCC" in funcs.datum1:
        conv2 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv2 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv2 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv2 = datumLambert93
    strfich = '_coord_datum.txt'

    kml2x(strtab, conv1, conv2, strfich)

def kml2wgs84():

    strtab = 'WGS84'
    conv1 = wgs84
    conv2 = wgs84
    strfich = '_coord_wgs84.txt'

    kml2x(strtab, conv1, conv2, strfich)

def kml2dxf_x(strtab, conv1, conv2, strfich): #=====================================DXF DXF DXF DXF DXF DXF

    conversao = 'Conversão KML para ficheiro DXF-R12 '+strtab
    app2.texto1.insert(END, '\nEscolha: '+conversao)
    app2.texto1.see(END)

    funcs.t_fich="kml files"
    funcs.e_fich="*.kml"

    funcs.abrir()
    if funcs.ficheiro == '':
        app2.texto1.insert(END, '\nA abertura do ficheiro falhou\n')
        app2.texto1.see(END)
        return 0

    ##inicio das linhas kml para cad

    nome = ','
    str0 = '<LinearRing>'
    str1 = '<LineString>'
    #cad = ''
    str2 = '_.pline\n'

    texto_camada = '' #necessario porque ao processar os pontos voltava a reinserir as camadas

    drawing = dxf.drawing(funcs.pasta+funcs.nome_fich+strfich)
    #drawing.add_layer('PT', color=3, linetype='Continuous')
    #drawing.add_layer('EDP', color=1, linetype='Continuous')

    f = open(funcs.ficheiro, 'r', encoding='utf8')    #abre um ficheiro e devolve o conteudo

    camada = '0'
    cor_i = 0
    conta_objecto = 0 #esta variavel ia determinar se a pasta/layer estava vazia e evitava atribuir-lhes cores que nunca iam ser usadas. a implementar.
    while 1:
        line = f.readline()

        if not line:
            break

        if '<Folder>' in line:
            if conta_objecto == 0:
                xpto = 0
            else:
                conta_objecto = 0
            line = f.readline()
            temp1 = line.split('>', line.count('>'))
            temp2 = temp1[1].split('<', line.count('<'))
            camada = temp2[0]
            camada = str(camada.replace(' ', '_'))
            cor = cor_i
            if ('PT' in camada) or ('Subida' in camada):
                cor = 100
                camada = 'PT'
            if ('EDP' in camada) or ('Posto' in camada):    #posto de transformacao
                cor = 40
                camada = 'EDP'
            camada_teste = ',' + camada + ','
            if camada_teste in texto_camada:
                xpto = 0
            else:
                cor_i = cor_i + 1
                drawing.add_layer(camada, color=cor, linetype='Continuous')
                texto_camada = texto_camada + camada + ','

        if '</Folder>' in line:
            camada = '0'

        if str0 in line:

            line = f.readline()
            
            while 'coordinates' not in line:
                line = f.readline()

            line = f.readline()

            line = line.replace(',0', '')
            line = line.replace('\t', '')

            coordenadas = line.split(' ')
            
            if '\n' in coordenadas:
                coordenadas.remove('\n')

            cont = 0
            tamanho = len(coordenadas)

            polyline = dxf.polyline(linetype='Continuous', layer=camada)
            while cont < tamanho:
                #print(coordenadas[cont])
                lon, lat = coordenadas[cont].split(',')
                lat = float(lat)
                lon = float(lon)
                coord = pyproj.transform(conv1, conv2, lon, lat)
                coord = str(coord[0])+','+str(coord[1])
                coord = coord.split(',', 1)
                polyline.add_vertex(coord)
                cont = cont + 1

            drawing.add(polyline)
            conta_objecto = conta_objecto + 1

        if str1 in line:

            line = f.readline()
            line = f.readline()
            line = f.readline()

            line = line.replace(',0 ', ' ')
            line = line.replace(',1 ', ' ')
            line = line.replace('\t', '')

            coordenadas = line.split(' ')
            if '\n' in coordenadas:
                coordenadas.remove('\n')

            cont = 0
            tamanho = len(coordenadas)

            flag_0 = 0

            polyline = dxf.polyline(linetype='Continuous', layer=camada)
            while (cont < tamanho and ('</coordinates>' not in coordenadas[cont])):
                flag_0 = 1
                lon, lat = coordenadas[cont].split(',')
                lat = float(lat)
                lon = float(lon)
                coord = pyproj.transform(conv1, conv2, lon, lat)
                coord = str(coord[0])+','+str(coord[1])
                coord = coord.split(',', 1)
                polyline.add_vertex(coord)
                cont = cont + 1

            if flag_0 == 1:
                drawing.add(polyline)
                conta_objecto = conta_objecto + 1
                #print(conta_objecto)

            #camada='0'

    f.close()

    ##inicio dos pontos kml para cad

    nome = ''
    texto = ''
    str0 = '<name>'
    str1 = 'coordinates'
    str2 = '_.Text\n'
    str3 = '\n1\n0\n'

    array_coord = []

    f = open(funcs.ficheiro, 'r', encoding='utf8')    #abre um ficheiro e devolve o conteudo

    camada = '0'
    conta_objecto = 0

    while 1:
        line = f.readline()
        if not line:
            break

        if '<Folder>' in line:
            if conta_objecto == 0:
                xpto = 0
            else:
                conta_objecto = 0
            line = f.readline()
            temp1 = line.split('>', line.count('>'))
            temp2 = temp1[1].split('<', line.count('<'))
            camada = temp2[0]
            camada = str(camada.replace(' ', '_'))
            cor = cor_i
            if ('PT' in camada) or ('Subida' in camada):
                cor = 100
                camada = 'PT'
            if ('EDP' in camada) or ('Posto' in camada):    #posto de transformacao
                cor = 40
                camada = 'EDP'
            camada_teste = ',' + camada + ','
            if camada_teste in texto_camada:
                xpto = 0
            else:
                cor_i = cor_i + 1
                drawing.add_layer(camada, color=cor, linetype='Continuous')
                texto_camada = texto_camada + camada + ','
        if '</Folder>' in line:
            camada = '0'

        if str0 in line:
            nome1 = line.split('>', 2)
            nome2 = nome1[1].split('<', 1)
            edif = nome2[0]
            edif = edif.replace(' ', '_')

        if str1 in line:
            coord1 = line.split('>', 2)
            coord2 = coord1[1].split('<', 1)
            coord = coord2[0]
            coord = coord.replace(',0', '')
            coord = coord.replace(', 0', '')
            coord = coord.replace(',', '\t')
            if coord != '\n':
                lon, lat = coord.split('\t', 1)
                lat = float(lat)
                lon = float(lon)
                tup1 = (lon, lat)
                array_coord.append(tup1)
                coord = pyproj.transform(conv1, conv2, lon, lat)
                coord = str(coord[0]) + ',' + str(coord[1])
                coord = coord.split(',', 1)
                drawing.add(dxf.text(edif, insert=(coord), layer=camada))
                conta_objecto = conta_objecto + 1
    f.close()

    drawing.save()
    if len(array_coord) > 0:
        desenha_pontos(array_coord)

    app2.texto1.insert(END, '\n'+conversao+' terminada com sucesso\n')
    app2.texto1.see(END)

def kml2dxf_wgs84(): #==============================================================DXF DXF DXF DXF DXF DXF

    #------codigo de escolha de zona
    z1 = app2.zona.get()
    z2 = app2.letra.get()
    letra = ''

    if z2 == 'N':
        letra = ''
    else:
        letra = ' +south'

    zona = z1 + letra
    utm_texto = '+proj=utm +zone=' + zona + ' +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    utm = pyproj.Proj(utm_texto)
    #------fim de codigo de escolha de zona

    strtab = '(UTM)'
    conv1 = wgs84
    conv2 = utm
    strfich = '_coordenadas_utm.dxf'
    kml2dxf_x(strtab, conv1, conv2, strfich)

def kml2dxf_datum73mod(): #=========================================================DXF DXF DXF DXF DXF DXF

    strtab = '(Datum)'
    conv1 = wgs84
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv2 = pttm06
    if "IPCC" in funcs.datum1:
        conv2 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv2 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv2 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv2 = datumLambert93
    strfich = '_coordenadas_datum.dxf'
    kml2dxf_x(strtab, conv1, conv2, strfich)

def dxf2kml_x(strtab, conv1, conv2, strfich):

    conversao = 'Conversão DXF-R12 '+strtab+' para KML'
    app2.texto1.insert(END, '\nEscolha: '+conversao)
    app2.texto1.see(END)

    funcs.t_fich="dxf files"
    funcs.e_fich="*.dxf"

    funcs.abrir()
    if funcs.ficheiro == '':
        app2.texto1.insert(END, '\nA abertura do ficheiro falhou\n')
        app2.texto1.see(END)
        return 0

    texto = ''
    stri = ("<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://www.opengis.net/kml/2.2' xmlns:gx='http://www.google.com/kml/ext/2.2' "+
            "xmlns:kml='http://www.opengis.net/kml/2.2' xmlns:atom='http://www.w3.org/2005/Atom'><Document><name>linhas_temp.kml</name><StyleMap id='m_ylw-pushpin'>"+
            '<Pair><key>normal</key><styleUrl>#s_ylw-pushpin</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl</styleUrl></Pair></StyleMap>'+
            "<Style id='s_ylw-pushpin'><IconStyle><scale>1.1</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>"+
            "<hotSpot x='20' y='2' xunits='pixels' yunits='pixels'/></IconStyle><PolyStyle><fill>0</fill></PolyStyle></Style><Style id='s_ylw-pushpin0'>"+
            "<IconStyle><scale>1.1</scale><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x='20' y='2' "+
            "xunits='pixels' yunits='pixels'/></IconStyle></Style><StyleMap id='m_ylw-pushpin0'><Pair><key>normal</key><styleUrl>#s_ylw-pushpin0</styleUrl></Pair>"+
            "<Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl0</styleUrl></Pair></StyleMap><Style id='s_ylw-pushpin_hl'><IconStyle><scale>1.3</scale><Icon>"+
            "<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x='20' y='2' xunits='pixels' yunits='pixels'/></IconStyle>"+
            "<PolyStyle><fill>0</fill></PolyStyle></Style><Style id='s_ylw-pushpin_hl0'><IconStyle><scale>1.3</scale><Icon>"+
            "<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x='20' y='2' xunits='pixels' yunits='pixels'/></IconStyle>"+
            '</Style>'+
            "<StyleMap id='m_ylw-pushpin01'>"+
            '<Pair><key>normal</key><styleUrl>#s_ylw-pushpin03</styleUrl></Pair><Pair><key>highlight</key><styleUrl>#s_ylw-pushpin_hl002</styleUrl></Pair></StyleMap>'+
            "<Style id='s_ylw-pushpin03'><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>"+
            "<hotSpot x='20' y='2' xunits='pixel' yunits='pixels'/></IconStyle></Style><Style id='s_ylw-pushpin_hl002'><IconStyle><scale>1.18182</scale><Icon>"+
            "<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon><hotSpot x='20' y='2' xunits='pixels' yunits='pixels'/>"+
            '</IconStyle></Style>'+
            '<Folder><name>linhas</name><open>1</open>')
    strpol1 = ('\n<Placemark><name>poligono</name><styleUrl>#m_ylw-pushpin</styleUrl><Polygon><tessellate>1</tessellate><outerBoundaryIs><LinearRing><coordinates>')
    strpol2 = ('</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>')
    strlin1 = ('\n<Placemark><name>linha</name><styleUrl>#m_ylw-pushpin0</styleUrl><LineString><tessellate>1</tessellate><coordinates>')
    strlin2 = ('</coordinates></LineString></Placemark>')
    strf = ('\n</Folder>')

    texto = (stri)

    stra = 'POLYLINE'
    strb = ' 10'
    strc = ' 10'
    strd = 'VERTEX'
    strg = 'SEQEND'
    elemento = ''

    f = open(funcs.ficheiro, 'r')    #abre um ficheiro e devolve o conteudo

    while 1:
        line = f.readline()
        if not line:
            break
        #print (line) # do something
        if stra in line:

            while strd not in line: #procura a primeira tag vertice
                line = f.readline()

            while strb not in line: #procura a primeira tag coordenadas x
                line = f.readline()

            line = f.readline()
            xi = line
            line = f.readline()
            line = f.readline()
            yi = line
            coord = pyproj.transform(conv1, conv2, xi, yi)
            #coord=pyproj.transform(datum73mod, wgs84, xi, yi)
            elemento = elemento + str(coord[0]) + ',' + str(coord[1]) + ',0 '

            while strg not in line:
                line = f.readline()
                if strb in line:
                    line = f.readline()
                    xf = line
                    line = f.readline()
                    line = f.readline()
                    yf = line
                    coord = pyproj.transform(conv1, conv2, xf, yf)
                    #coord=pyproj.transform(datum73mod, wgs84, xf, yf)
                    elemento = elemento + str(coord[0]) + ',' + str(coord[1]) + ',0 '

            if xi == xf:
                texto = (texto + strpol1 + '\n' + elemento + '\n' + strpol2)
            else:
                texto = (texto+strlin1 + '\n' + elemento + '\n' + strlin2)
            elemento = ''

    texto = (texto + strf)

    f.close()

    stri = ('<Folder><name>pontos</name>')
    str1 = ('<Placemark><name>')
    str2 = ('</name>')
    str3 = ('<styleUrl>#m_ylw-pushpin01</styleUrl><Point><coordinates>')
    str4 = ('</coordinates></Point></Placemark>')
    strf = ('</Folder></Document></kml>')

    texto2 = ''
    texto2 = stri
    strx = 'TEXT'
    stry = '  1'
    strz = ' 10'
    strent = 'ENTITIES'
    ponto = ''

    array_coord = []

    f = open(funcs.ficheiro, 'r')    #abre um ficheiro e devolve o conteudo

    while strent not in line: #vai ate ah seccao de entidades
        line = f.readline()

    while 1:
        line = f.readline()
        if not line:
            break

        if strx in line:

            while strz not in line: #procura a primeira tag text
                line = f.readline()
            line = f.readline()
            x = line
            line = f.readline()
            line = f.readline()
            y = line
            while stry not in line: #procura a tag ' 1' que marca o texto
                line = f.readline()
            line = f.readline()
            ponto = line
            resultado = pyproj.transform(conv1, conv2, x, y)
            #resultado=pyproj.transform(datum73mod,wgs84, x, y)
            tup1 = (resultado[0], resultado[1])
            array_coord.append(tup1)
            texto2 = (texto2 + str1 + ponto + str2 + str3 + str(resultado[0]) + ',' + str(resultado[1]) + str4 + '\n')

    f.close()

    texto2 = texto2 + strf

    f2 = open(funcs.pasta+funcs.nome_fich+strfich, 'w')   #cria o ficheiro com coordenadas transformadas
    f2.write(texto + texto2)
    f2.close()

    desenha_pontos(array_coord)

    app2.texto1.insert(END, '\n'+conversao+' terminada com sucesso\n')
    app2.texto1.see(END)

def dxf2kmlwgs84():

    #------codigo de escolha de zona
    z1 = app2.zona.get()
    z2 = app2.letra.get()
    letra = ''

    if z2 == 'N':
        letra = ''
    else:
        letra = ' +south'

    zona = z1 + letra
    utm_texto = '+proj=utm +zone=' + zona + ' +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    utm = pyproj.Proj(utm_texto)
    #------fim de codigo de escolha de zona

    strtab = '(UTM)'
    conv1 = utm
    conv2 = wgs84
    strfich = '_coord_kml_utm-WGS84.kml'
    dxf2kml_x(strtab, conv1, conv2, strfich)

def dxf2kmldatum73mod():

    strtab = '(Datum)'
    funcs.ver_datum()
    if "TM06" in funcs.datum1:
        conv1 = pttm06
    if "IPCC" in funcs.datum1:
        conv1 = datum73IPCC
    if "IGeoE" in funcs.datum1:
        conv1 = datum73IGeoE
    if "OSGB36" in funcs.datum1:
        conv1 = datumOSGB36
    if "Lambert93" in funcs.datum1:
        conv1 = datumLambert93
    conv2 = wgs84
    strfich = '_coord_kml_WGS84.kml'
    dxf2kml_x(strtab, conv1, conv2, strfich)

def preview():

    funcs.t_fich="text files"
    funcs.e_fich="*.txt"

    funcs.abrir()
    if funcs.ficheiro == '':
        return 0

    app2.texto1.insert(END, '\nEscolha: Pré-visualizar '+funcs.ficheiro)
    app2.texto1.see(END)

    texto = ''
    f = open(funcs.ficheiro, 'r', encoding='utf8')    #abre um ficheiro (definido abaixo) e devolve o conteudo
    array_coord = []
    while 1:
        line = f.readline()
        if not line:
            break
        #print (line) # do something
        try:
            if line.count('\t') < 3:
                ponto, x, y = line.split('\t', 2)
            else:
                ponto, x, y, obs = line.split('\t', 3)
        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.\nOs parâmetros de entrada não foram aceites.'+
                               '\nOs dados devem estar separados por tabs.\n')
            app2.texto1.see(END)
            return 0
        x = x.replace('\n', '')
        y = y.replace('\n', '')
        x = x.replace(',', '.')
        y = y.replace(',', '.')
        y = float(y)
        x = float(x)
        try:
            tup1 = (x, y)
            array_coord.append(tup1)
        except:
            app2.texto1.insert(END, '\n\nThe computer says no :(\nErro.\nOs parâmetros de entrada não foram aceites.'+
                               '\nAs coordenadas devem ser em WGS84 e as colunas nao podem ter títulos.'+
                               '\nO formato deve ser: nome_do_ponto longitude latitude\n')
            app2.texto1.see(END)
            return 0
    f.close()
    desenha_pontos(array_coord)

def clear():
    app2.texto1.insert(END, '\nEscolha: Limpar pré-visualização\n')
    app2.texto1.see(END)
    app2.canvas1.delete("all")

def desenha_pontos(array_coord):

    app2.canvas1.delete("all")

    if len(array_coord) == 0: #sem isto crasha se nao houver pontos
        return 0

    i = 0
    (x_min, y_min) = array_coord[i]
    (x_max, y_max) = array_coord[i]

    for i in range(len(array_coord)):
        (x, y) = array_coord[i]
        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if x > x_max:
            x_max = x
        if y > y_max:
            y_max = y

    if len(array_coord) == 1: #sem isto crasha se houver apenas um ponto
        x_max = 1
        y_max = 1

    delta_x = x_max-x_min
    delta_y = y_max-y_min
    escala_x = delta_x/400
    escala_y = delta_y/400

    if escala_x == 0: #sem isto crasha se so houverem pontos com as mesmas coordenadas
        escala_x = 1

    if escala_y == 0: #sem isto crasha se so houverem pontos com as mesmas coordenadas
        escala_y = 1

    i = 0

    off_x_min = (x_min/escala_x)
    off_y_min = (y_min/escala_y)

    for i in range(len(array_coord)):
        (x, y) = array_coord[i]
        app2.canvas1.create_oval(((x/escala_x)-off_x_min-3), 400-((y/escala_y)-off_y_min-3), ((x/escala_x)-off_x_min+3), 400-((y/escala_y)-off_y_min+3), fill="red") #(400-y) inverte o eixo dos y

    num_pontos = str(i + 1)
    app2.canvas1.create_text((365, 390), text=num_pontos+' pontos')

######################################### FIM DAS COORDENADAS #############################################################
###########################################################################################################################

###########################################################################################################################
######################################### INICIO DO PROGRAMA ##############################################################

#funcs.seg() #'verificacao de limite de data
root = Tk()
#root.iconbitmap(default='icone.ico')
root.title('COORDENADAS  * * * * * ')
funcs.settings()
note = ttk.Notebook(root)
note.grid()
tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
note.add(tab1, text='Conversão')
note.add(tab2, text='Blocos')
note.add(tab3, text='Conversor')

app2 = Application2(tab1)
app3 = Application3(tab2)
app4 = conversor.Application4(tab3)

root.mainloop()
#root.destroy()

######################################### FIM DO PROGRAMA #################################################################
###########################################################################################################################

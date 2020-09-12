import tkinter.messagebox
import funcs
from tkinter import *
from idlelib import *

class Application4(Frame):

    #definir sempre primeiro as funcoes e depois os botoes

    def convdatum(self):
        #conversao datum para wgs
        global texto_conv
        global tipo_conv
        tipo_conv = 1
        texto_conv = self.coorddatum.get()
        funcs.conva2b(texto_conv, tipo_conv)
        x,y = funcs.strcoord
        texto_novo = str(round(float(y),6))  + ',' + str(round(float(x),6))
        self.coordwgs.delete(0, END)
        self.coordwgs.insert(0, texto_novo)
        tkinter.messagebox.showinfo('Teste', texto_novo)

    def convwgs(self):
        #conversao wgs para datum
        global texto_conv
        global tipo_conv
        tipo_conv = 2
        texto_temp = self.coordwgs.get()
        #transformar lat-lon para lon-lat
        lat,lon = texto_temp.split(",", 1)
        texto_conv = str(lon + ',' + lat)
        funcs.conva2b(texto_conv, tipo_conv)
        x,y = funcs.strcoord
        texto_novo = str(round(float(x),2))  + ',' + str(round(float(y),2))
        self.coorddatum.delete(0, END)
        self.coorddatum.insert(0, texto_novo)
        tkinter.messagebox.showinfo('Teste', texto_novo)

    def limpar_coord(self):
        self.coordwgs.delete(0, END)
        #self.coordwgs.insert(0, '')
        self.coorddatum.delete(0, END)
        #self.coorddatum.insert(0, '')
    
    def botoes4(self):

		#texto de exemplo no campo
        coord_texto = '41.246483,-8.628475'
        coord_v = coord_texto.split(',')
        latitude=coord_v[0]
        longitude=coord_v[1]

        self.botao41 = Button(self, text='Obter WGS84', command=self.convdatum)
        self.botao41.grid(row=1, column=3, sticky=S+W)
        #tip_botao41 = ToolTip(self.botao41, 'Converte as coordenadas em Datum para WGS84')

        self.botao42 = Button(self, text='Obter Datum', command=self.convwgs)
        self.botao42.grid(row=2, column=3, sticky=S+W)
        #tip_botao42 = ToolTip(self.botao42, 'Converte as coordenadas em WGS84 para Datum')

        self.botao43 = Button(self, text='Limpar', command=self.limpar_coord)
        self.botao43.grid(row=3, column=3, sticky=N+S+W)
        #tip_botao43 = ToolTip(self.botao43, 'Limpa os campos de dados')

        self.coordwgs_lab = Label(self, text='Lat, Long')
        self.coordwgs_lab.grid(row=2, column=1, sticky=S+W)
        self.coordwgs = Entry(self, width=20)
        self.coordwgs.grid(row=2, column=2, sticky=S+W)
        self.coordwgs.delete(0, END)
        self.coordwgs.insert(0, coord_texto)

        self.coorddatum_lab = Label(self, text='X, Y')
        self.coorddatum_lab.grid(row=1, column=1, sticky=S+W)
        self.coorddatum = Entry(self, width=20)
        self.coorddatum.grid(row=1, column=2, sticky=S+W)
        self.coorddatum.delete(0, END)
        self.coorddatum.insert(0, '-41522.18,175369.85')

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.botoes4()


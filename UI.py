from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from database import DataBase
from tkinter.font import Font


class Ui:
    __width = 300
    __height = 300
    __stageUi = Tk()
    __dataBase = DataBase()

    # Table
    tree = ttk.Treeview(heigh=7, show='headings')

    # inputs
    __idE = Entry(textvariable=IntVar)
    __priceE = Entry(textvariable=IntVar)
    __nomStageE = Entry(textvariable=StringVar)
    __workE = Entry(textvariable=IntVar)
    __domainE = Entry(textvariable=IntVar)

    def __init__(self):
        pass


    def start(self):
        self.__stageUi.mainloop()

    def addWidth(self, nowWidth):
        self.__width = nowWidth
        self.__addSize()

    def addHeight(self, nowHeight):
        self.__height = nowHeight
        self.__addSize()

    def __addSize(self):
        self.__stageUi.geometry(f"{self.__width}x{self.__height}")

    def addLable(self, text, font):
        lable = Label(self.__stageUi, text=text, font=font,fg="#6096fd")
        lable.place(x=350, y=25, anchor="center")

    def addFixSize(self):
        self.__stageUi.minsize(self.__width, self.__height)
        self.__stageUi.maxsize(self.__width, self.__height)

    def addLebeles(self, names):
        Label(text=names[0], font="arial 12 bold",fg="#6096fd").place(x=100, y=100, anchor="center")
        Label(text=names[1], font="arial 12 bold",fg="#6096fd").place(x=100, y=150, anchor="center")
        Label(text=names[2], font="arial 12 bold",fg="#6096fd").place(x=100, y=200, anchor="center")
        Label(text=names[3], font="arial 12 bold",fg="#6096fd").place(x=100, y=250, anchor="center")
        Label(text=names[4], font="arial 12 bold",fg="#6096fd").place(x=100, y=300, anchor="center")

    def addInput(self):
        self.__idE.place(x=260, y=100, anchor="center")
        self.__workE.place(x=260, y=150, anchor="center")
        self.__priceE.place(x=260, y=200, anchor="center")
        self.__domainE.place(x=260, y=250, anchor="center")
        self.__nomStageE.place(x=260, y=300, anchor="center")

    def AddBtn(self):
        font = Font(family='Helvetica')
        btnMofify = Button(text="modify", font="arial 20 normal",activebackground="#c6e2ff", command=self.updateData, height=2, width=15,background="#6096fd",fg="#ffffff",borderwidth=1)
        btnAdd = Button(text="add", font="arial 20 normal",activebackground="#c6e2ff", command=self.addDataInMongoDb,height=2,width=15,background="#6096fd",fg="#ffffff",borderwidth=1)
        btnDelete=Button(text="delet", font="arial 20 normal",activebackground="#c6e2ff", command=self.deleteData, height=2, width=15,background="#6096fd",fg="#ffffff",borderwidth=1)
        btnAffich=Button(text="affiche", font="arial 20 normal",activebackground="#c6e2ff", command=self.affich, height=2, width=15,background="#6096fd",fg="#ffffff",borderwidth=1)
        btnAdd['font'] = font
        btnDelete['font'] = font
        btnAffich['font'] = font
        btnMofify['font'] = font
        btnAdd.place(x=600, y=120, anchor="center")
        btnMofify.place(x=600, y=180, anchor="center")
        btnDelete.place(x=600, y=240, anchor="center")
        btnAffich.place(x=600, y=300, anchor="center")

    def addDataInMongoDb(self):
        id = self.__idE.get()
        work = self.__workE.get()
        priece = self.__priceE.get()
        domine = self.__domainE.get()
        name = self.__nomStageE.get()


        if id == "":
            messagebox.showinfo(title="error", message="pleas enter your id")
            self.__idE.focus()
            return
        if work == "":
            messagebox.showinfo(title="error", message="pleas enter your work")
            self.__workE.focus()
            return
        if priece == "":
            messagebox.showinfo(title="error", message="pleas enter your price")
            self.__priceE.focus()
            return
        if domine == "":
            messagebox.showinfo(title="error", message="pleas enter your domine")
            self.__domainE.focus()
            return
        if name == "":
            messagebox.showinfo(title="error", message="pleas enter your name")
            self.__nomStageE.focus()
            return

        if self.__dataBase.isTheIdExecteInDataBase(id) == False:
            messagebox.showerror("Error ", "The id Is Is already exist ")
            self.__idE.focus()
            return
        self.__dataBase.insertData(id=id, work=work, prise=priece, domain=domine, nameStage=name)
        self.cleanInputs()
        self.affich()

    def deleteData(self):
        id = self.__idE.get()
        if (id == ""):
            messagebox.showinfo(title="Error", message="your id is empty")
        else:
            self.dialog(id)


    def dialog(self,id):
        status =messagebox.askyesno("Are You sure","if you delete the data you can't retrieve it")
        if status == True:
            self.__dataBase.delete(str(id))
            self.cleanInputs()
            self.affich()
        else:
            self.cancel()


    def cancel(self):
        pass

    def updateData(self):

        id = self.__idE.get()
        if (id == ""):
            messagebox.showinfo(title="Error", message="your id is empty")
            return

        oldData = self.__dataBase.findById(id)
        domine = self.__domainE.get()
        priece = self.__priceE.get()
        name = self.__nomStageE.get()
        work = self.__workE.get()
        if(domine == ""):
            domine = oldData["domain"]
        if (priece == ""):
            priece = oldData["prise"]
        if (name == ""):
            name = oldData["nameStage"]
        if (work == ""):
            work = oldData["work"]
        self.__dataBase.update(id=id, domain=domine, prise=priece, nameStage=name, work=work)
        self.cleanInputs()
        self.affich()
    # affivarge d'un tablau

    def affich(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        columns = ('id', 'domain', 'work', 'prise', 'nameStage')
        self.tree.pack()
        liste_data = self.__dataBase.affich()
        self.tree["columns"] = columns
        self.tree.bind("<Double-1>", self.selectItem)
        self.tree.heading('id', text='id')
        self.tree.heading('domain', text='domine')
        self.tree.heading('prise', text='priece')
        self.tree.heading('nameStage', text='name')
        self.tree.heading('work', text='work')
        self.tree.column('id', width=80)
        self.tree.column('domain', width=200)
        self.tree.column('prise', width=150)
        self.tree.column('work', width=150)
        self.tree.column('nameStage', width=150)
        for item in liste_data:
            self.tree.insert("", END, values=(item['id'], item['domain'], item['work'], item['prise'], item['nameStage']))
        self.tree.place(x=0, y=334)

    def selectItem(self,event):
        itemSelected = self.tree.focus()
        listData = self.tree.item(itemSelected)["values"]
        self.setUpData(listData)



    def cleanInputs(self):
        self.__domainE.delete(0,END)
        self.__idE.delete(0,END)
        self.__nomStageE.delete(0,END)
        self.__priceE.delete(0,END)
        self.__workE.delete(0,END)


    def setUpData(self,listOfData):
        self.cleanInputs()
        self.__idE.insert(0,str(listOfData[0]))
        self.__workE.insert(0,str(listOfData[2]))
        self.__priceE.insert(0,str(listOfData[3]))
        self.__domainE.insert(0,str(listOfData[1]))
        self.__nomStageE.insert(0,str(listOfData[4]))



from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw
import solve
from factory import SolverFactory

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

if __name__ == "__main__":
    root = Tk()
    root.title("Maze Creator")
    Vline = []
    Hline = []
    ColoredPixels = []
    Csize = 750
    BlackPixels = set()
    WhitePixels = set()
    Psize = 0
    Gsize = 0
    AlgoVar = IntVar()
    isGridGenerated = False
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid(column=0, row=0)
    options = Frame(root, bd=2, relief=SUNKEN, width=250, height=Csize, bg="#242526")
    options.grid(column=1, row=0)
    
    canvas = Canvas(frame, bd=0, bg="White")
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    #frame.pack(fill=BOTH,expand=1)

    def GenerateGrid():
        global Psize
        global Gsize
        global isGridGenerated
        try:
            isGridGenerated = True
            Gsize = int(GridSizeTextBox.get())
            img = Image.new('RGB', (Gsize, Gsize), color = 'White')
            img.save('mesh.png')
            Psize = Csize/Gsize
            for i in range(int(Gsize)):
                Vline.append(canvas.create_line(Psize*i,0,Psize*i,Csize))
                Hline.append(canvas.create_line(0,Psize*i,Csize,Psize*i))
            #mouseclick event
            canvas.bind("<ButtonRelease-1>",SingleColorBlack)
            canvas.bind("<ButtonRelease-3>",SingleColorWhite)
            canvas.bind("<B1-Motion>",SingleColorBlack)
            canvas.bind("<B3-Motion>",SingleColorWhite)
        except:
            print("Invalid Input")
    
    def GeneratedPath():
        global AlgoVar
        Algo = AlgoVar.get()
        sf = SolverFactory()
        if isGridGenerated == False:
            return
        if Algo == 0:
            solve.solve(sf, "breadthfirst", "mesh.png", "solvedmesh.png")
        elif Algo == 1:
            solve.solve(sf, "depthfirst", "mesh.png", "solvedmesh.png")
        #elif Algo == 2:
        #    solve.solve(sf, "dijkstra", "mesh.png", "solvedmesh.png")
        #elif Algo == 3:
        #    solve.solve(sf, "astar", "mesh.png", "solvedmesh.png")
        elif Algo == 4:
            solve.solve(sf, "leftturn", "mesh.png", "solvedmesh.png")
        
        solved = Image.open("solvedmesh.png")
        solved.show()
        
        
    #Options
    options1 = Frame(options, bd=0, relief=SUNKEN, width=250, bg="#242526")
    options1.grid(column=0, row=0)
    GridSizeTextBox = Entry(options1, width=40, bg="#1b1b1c", fg="#0c9cfc", justify=CENTER)
    GridSizeTextBox.grid(column = 0,row = 0,pady=(10,10))
    GridSizeButton = Button(options1, text ="GENERATE GRID", width=20, pady=5, bg="#0c9cfc", fg="White", font="verdana 10 bold", command = GenerateGrid)
    GridSizeButton.grid(column = 0,row = 1,pady=(0,10))
    GeneratePathButton = Button(options1, text ="GENERATE PATH", width=20, pady=5, bg="#19bc03", fg="White", font="verdana 10 bold", command = GeneratedPath)
    GeneratePathButton.grid(column = 0,row = 7,pady=(0,10))
    Algorithm1 = Radiobutton(options1, text="Breadth First", variable=AlgoVar, value=0, bg="#242526", activebackground="#242526" , fg="#0c9cfc", font="verdana 10 bold")
    Algorithm1.grid(column = 0,row = 2,pady=(0,10))
    Algorithm2 = Radiobutton(options1, text="Depth First", variable=AlgoVar, value=1, bg="#242526", activebackground="#242526", fg="#0c9cfc", font="verdana 10 bold")
    Algorithm2.grid(column = 0,row = 3,pady=(0,10))
    #Algorithm3 = Radiobutton(options1, text="Dijkstra", variable=AlgoVar, value=2, bg="#242526", activebackground="#242526", fg="#0c9cfc", font="verdana 10 bold")
    #Algorithm3.grid(column = 0,row = 4,pady=(0,10))
    #Algorithm4 = Radiobutton(options1, text="A star", variable=AlgoVar, value=3, bg="#242526", activebackground="#242526", fg="#0c9cfc", font="verdana 10 bold")
    #Algorithm4.grid(column = 0,row = 5,pady=(0,10))
    Algorithm5 = Radiobutton(options1, text="Left Turn", variable=AlgoVar, value=4, bg="#242526", activebackground="#242526", fg="#0c9cfc", font="verdana 10 bold")
    Algorithm5.grid(column = 0,row = 4,pady=(0,10))
    options2 = Frame(options, bd=0, relief=SUNKEN, width=250, height=Csize-options1.winfo_height()-235, bg="#242526")
    options2.grid(column=0, row=1)

    root.resizable(False, False)
    #Gsize= int(input("Grid size(X*X): "))
    canvas.config(width=Csize, height=Csize)
    #Psize = Csize/Gsize

    

    #function to be called when mouse is clicked
    def SingleColorBlack(event):
        cx, cy = event2canvas(event, canvas)
        Vno = int(cy/Psize) + 1
        Hno = int(cx/Psize) + 1
        if (Vno, Hno) in BlackPixels:
            return
        if (Vno, Hno) in WhitePixels:
            WhitePixels.remove((Vno, Hno))
        BlackPixels.add((Vno, Hno))
        ColoredPixels.append(canvas.create_rectangle((Hno-1)*Psize, (Vno-1)*Psize,Hno*Psize, Vno*Psize, fill="Black"))
        canvas.update()
        img = Image.open("mesh.png")
        img.putpixel((Hno-1,Vno-1),(0,0,0))
        img.save("mesh.png")
        #print ("(%d, %d) / (%d, %d) At %d column, %d row" % (event.x,event.y,cx,cy,Hno,Vno))

    def SingleColorWhite(event):
        #outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        Vno = int(cy/Psize) + 1
        Hno = int(cx/Psize) + 1
        if (Vno, Hno) in WhitePixels:
            return
        if (Vno, Hno) in BlackPixels:
            BlackPixels.remove((Vno, Hno))
        WhitePixels.add((Vno, Hno))
        ColoredPixels.append(canvas.create_rectangle((Hno-1)*Psize, (Vno-1)*Psize,Hno*Psize, Vno*Psize, fill="White"))
        canvas.update()
        img = Image.open("mesh.png")
        img.putpixel((Hno-1,Vno-1),(255,255,255))
        img.save("mesh.png")
        #print ("(%d, %d) / (%d, %d) At %d column, %d row" % (event.x,event.y,cx,cy,Hno,Vno))

    root.mainloop()
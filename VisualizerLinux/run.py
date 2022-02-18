import sys
from lazycbs import init

from tkinter import *
from Map import info
import time

class MyCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)

"""Right-hand component that handles buttons"""
class rightFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.playButton = Button(self, text='Pause',width=10,height=3, bg='red', fg='black', command=self.play_visualizer)
        self.playButton.grid(row=1, column=0,columnspan=2,pady=10)
        self.backButton = Button(self, text='<<',width=5,height=3, bg='white', fg='black', command=self.backward)
        self.backButton.grid(row=4, column=0,pady=10)
        self.forwardButton = Button(self, text='>>',width=5,height=3, bg='white', fg='black', command=self.forward)
        self.forwardButton.grid(row=4, column=1,pady=10)
        self.speedUpButton=Button(self, text='<<<',width=5,height=3, bg='white', fg='black', command=lambda:self.speedChange(0.05))
        self.speedUpButton.grid(row=5, column=0,pady=10)
        self.speedDownButton=Button(self, text='>>>',width=5,height=3, bg='white', fg='black', command=lambda:self.speedChange(-0.05))
        self.speedDownButton.grid(row=5, column=1,pady=10)
    """speed up or down"""
    def speedChange(self,change):
        global speedup
        speedup=max(0.001,speedup+change)
    """"""
    def play_visualizer(self):
        global continuePlay,Paused
        if self.playButton["text"] == "Pause":
            self.playButton["text"] = "Play"
            self.playButton["bg"] = "green"
            continuePlay=False

        else:
            self.playButton["text"] = "Pause"
            self.playButton["bg"] = "red"
            continuePlay= True

    def backward(self):
        global continuePlay,t,backward,forward
        self.playButton["text"] = "Play"
        self.playButton["bg"] = "green"
        backward=True
        forward=False
        continuePlay=False

    def forward(self):
        global continuePlay,t,forward,backward
        self.playButton["text"] = "Play"
        self.playButton["bg"] = "green"
        forward=True
        backward=False
        continuePlay=False


"""Top frame component that handles timesteps, menu, user's queries"""
class topFrame(Frame):
    def __init__(self, master,canvas):
        Frame.__init__(self, master)

        """enable user to drag the scene"""
        self.canvas = canvas
        self.xsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0,0,4000,2000))

        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        #linux scroll
        self.canvas.bind("<Button-4>", self.zoomerP)
        self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        self.canvas.bind("<MouseWheel>",self.zoomer)
        """"""

        """add menu to root"""
        self.master = master
        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu)
        fileMenu.add_command(label="Agent Detail",command=self.openNewWindow1)
        fileMenu.add_command(label="Ask Questions",command=self.openNewWindow2)
        menu.add_cascade(label="More Functions", menu=fileMenu)
        """"""

        """setup text box, button in main frame"""
        self.text = Text(self, width=30)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_config('constraint', background="#DCE2F1", foreground="black")
        self.text.tag_config('current', background="#EBEBE4", foreground="black",font=("Helvetica",28))
        """"""
        self.newWindow1=None
        self.newWindow2=None
    """drag function"""
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerP(self,event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    """"""

    """open new window to display the Agent Detail"""
    def openNewWindow1(self):
        if (self.newWindow1==None):
            self.newWindow1 = Toplevel(root)
            self.newWindow1.title("Inspect AI")
            self.newWindow1.geometry("650x700")
            self.newWindow1.protocol("WM_DELETE_WINDOW", exit)

            self.newframe = Frame(self.newWindow1)
            self.newframe.place(x=10, y=20)

            self.t = Text(self.newframe, width=60)
            self.scrollbar = Scrollbar(self.newframe,orient="vertical", command=self.t.yview)
            self.t.configure(yscrollcommand=self.vsb.set)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            self.t.pack(side="left",fill=BOTH,expand=True)

            self.inputtxt = Entry(self.newframe,width=20)
            self.inputtxt.pack()

            """ print out comparison """
            self.printButton = Button(self.newframe, text = "inspect",
                                      command = lambda: Info.displayAIDetail(the_canvas, self.inputtxt, self.t))
            self.printButton.pack()
            self.exitButton = Button(self.newframe, text="Exit", highlightbackground="#56B426", command=self.destroy1)
            self.exitButton.pack()
    def destroy1(self):
        tw = self.newWindow1
        self.newWindow1 = None
        if tw:
            list = tw.grid_slaves()
            for l in list:
                l.destroy()
            tw.destroy()
    """"""
    def openNewWindow2(self):
        if (self.newWindow2==None):
            self.newWindow2 = Toplevel(root)
            self.newWindow2.title("Run Model")
            self.newWindow2.geometry("700x700")
            self.newWindow2.protocol("WM_DELETE_WINDOW", exit)

            self.newframe2 = Frame(self.newWindow2)
            self.newframe2.place(x=10, y=20)

            self.t2 = Text(self.newframe2, width=60)
            self.scrollbar2 = Scrollbar(self.newframe2,orient="vertical", command=self.t2.yview)
            self.t2.configure(yscrollcommand=self.vsb.set)
            self.scrollbar2.pack(side=RIGHT, fill=Y)
            self.t2.pack(side="left",fill=BOTH,expand=True)
            
            
            self.la1=Label(self.newframe2,text="Agent: ",width=5)
            self.la2=Label(self.newframe2,text="Loc1: eg.3,4",width=10)
            self.la3=Label(self.newframe2,text="Loc2: eg.-1,-2",width=10)
            self.la4=Label(self.newframe2,text="time: ",width=5)
            self.la5=Label(self.newframe2,text="cost: ",width=5)
            self.la1.pack()
            self.agent = Entry(self.newframe2, width=10)
            self.agent.pack()
            self.la2.pack()
	
            self.location1 = Entry(self.newframe2,width=10)
            self.location1.pack()
            self.la3.pack()
            self.location2 = Entry(self.newframe2,width=10)
            self.location2.pack()
            self.la4.pack()
            self.time = Entry(self.newframe2,width=10)
            self.time.pack()
            self.la5.pack()
            self.cost = Entry(self.newframe2,width=10)
            self.cost.pack()
            
            self.checkBoxVar = IntVar(value=0)
            self.c = Checkbutton(self.newframe2, text = "Use current time", variable=self.checkBoxVar)
            self.c.pack()
           
            """ print out comparison """
            self.printButton2 = Button(self.newframe2, text = "run!",
                                      command = lambda: self.runModel(self.agent,self.location1, self.location2, self.time, self.cost,self.t2))
            self.printButton2.pack()
            self.exitButton2 = Button(self.newframe2, text="Exit", highlightbackground="#56B426", command=self.destroy2)
            self.exitButton2.pack()
    def runModel(self,ai,loc1,loc2,time,cost,textbox):
        global Info
        textbox.delete('1.0', END)
        ai = ai.get()
        loc1 = loc1.get()
        loc2 = loc2.get()
        time = time.get()
        cost = cost.get()
        boolean = self.checkBoxVar.get()
        if ai!="":
            ai = int(ai)
        else:
            ai=0
        if loc1!="":
            loc1a,loc1b = int(loc1.split(',')[0]),int(loc1.split(',')[1])
        else:
            loc1a,loc1b=-1,-2
            
        if loc2!="":
            loc2a,loc2b = int(loc2.split(',')[0]),int(loc2.split(',')[1])
        else:
            loc2a,loc2b=-1,-2
        if time!="":
            time = int(time)
        else:
            	time=-1
        if cost!="":
            cost = int(cost)
        else:
            cost=-100
        if boolean:
            with open("test1.scen",'w') as out:
                out.write("version 1\n")
                for i in range(len(Info.AgentsPos)):
                    tmp=str(i)+'\t'+'debug-6-6.map'+'\t'+str(len(Info.BinaryMap[0]))+'\t'+str(len(Info.BinaryMap))+'\t'+str(Info.AgentsPos[i][min(Info.currentTime,len(Info.AgentsPos[i])-1)][1]-1)+'\t'+str(Info.AgentsPos[i][min(Info.currentTime,len(Info.AgentsPos[i])-1)][0]-1)+'\t'+str(Info.AgentsPos[i][-1][1]-1)+'\t'+str(Info.AgentsPos[i][-1][0]-1)+'\t'+str(8)+'\n'
                    out.write(tmp)
        
            out.close()
            temp=init("../../maps/debug-6-6.map.ecbs", "test1.scen", 2, [(ai, ((loc1a, loc1b), (loc2a, loc2b)), time, cost)])
            textbox.insert("end",temp,'current')
            textbox.see("end")
        # temp=init("../maps/debug-6-6.map.ecbs", "../scenarios/debug-6-6-2-2.scen", 2, [(0, ((-1, -2), (-1, -2)), -2, -100)])
        # textbox.insert("end",temp,'current')
        else:
            #temp=init("../../maps/warehouse-10-20-10-2-1.map.ecbs", "../../scenarios/even/warehouse-10-20-10-2-1-even-1.scen", 25, [(ai, ((loc1a, loc1b), (loc2a, loc2b)), time, cost)])
            temp=init("../../maps/debug-6-6.map.ecbs", "../../scenarios/debug-6-6-2-2.scen", 2, [(ai, ((loc1a, loc1b), (loc2a, loc2b)), time, cost)])
            textbox.insert("end",temp,'current')
            textbox.see("end")
        
    def destroy2(self):
        tw = self.newWindow2
        self.newWindow2 = None
        if tw:
            list = tw.grid_slaves()
            for l in list:
                l.destroy()
            tw.destroy()
def repeater(root):
    global backward,forward,speedup
    t=1
    notMovingFlag=False      #True when no agent is moving
    while True:
        if backward and t>1:
            t-=1
            Info.move_agents(t,the_canvas,top_frame,True)
            notMovingFlag=False
        elif notMovingFlag==True:
            pass
        elif forward and t>=1:
            endFlag=Info.move_agents(t,the_canvas,top_frame,False)
            t+=1
            if endFlag:
                notMovingFlag=True

        elif continuePlay:
            endFlag=Info.move_agents(t,the_canvas,top_frame,False)
            t+=1
            if endFlag:
                notMovingFlag=True


        forward=False
        backward=False

        root.update()
        time.sleep(speedup)


if __name__=="__main__":
    #in windows: python run.py test_2.txt debug-6-6.map.ecbs 2
    #in linux: python3 run.py test_2.txt debug-6-6.map.ecbs 2
    try:
        addagen=sys.argv[1]
        addmap=sys.argv[2]
        numAgent=int(sys.argv[3])
    except IndexError:
    	#addagen,addmap,numAgent="../../scenarios/even/warehouse-10-20-10-2-1-even-1.scen","../../maps/warehouse-10-20-10-2-1.map.ecbs",25
    	#addagen,addmap,numAgent="../../scenarios/debug-6-6-2-2.scen","../../maps/debug-6-6.map.ecbs",2
    	addagen,addmap,numAgent="test_25.txt","warehouse-10-20-10-2-1.map.ecbs",25
    	#addagen,addmap,numAgent="test_2.txt","debug-6-6.map.ecbs",2
    	
    #data=init(addmap, addagen, numAgent, [(0, ((-1, -2), (-1, -2)), -2, -100)])
    #addagen=data
    
    global Info,the_canvas,top_frame,continuePlay,t,backward,forward,newWindow,speedup


    Info=info(addagen,addmap,numAgent)

    # Construct a simple root window
    root = Tk()

    continuePlay,backward,forward,speedup = True,False,False,0.2

    root.title("Lazycbs Visualizer")
    # root.protocol("WM_DELETE_WINDOW",exit)

    the_canvas= MyCanvas(root,width=1630,height=720,bg="#d1d1d1")
    the_canvas.pack(side=LEFT,expand=True,fill=BOTH)

    right_frame = rightFrame(root)
    right_frame.pack(side=RIGHT,expand=True,fill=BOTH)

    top_frame = topFrame(root,the_canvas)
    top_frame.pack(side=RIGHT,expand=True,fill=BOTH)

    """cross platform"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    top_frame.config(width=screen_width, height=screen_height)

    Info.draw_map(the_canvas)
    Info.draw_agents(the_canvas,top_frame,right_frame)

    repeater(root)

    root.mainloop()

    

from tkinter import *
import tkinter.font as font
import ast
from collections import defaultdict
import random

class info:
        def __init__(self,addagen,addmap,numAgent):
            self.fagents=open(addagen,'r')
            #self.fagents=addagen
            self.fmap=open(addmap,'r')
            self.numAgent=numAgent
            self.a=50
            self.x0,self.y0=0,0
            self.currentTime=-1
            self.BinaryMap=[]
            self.CanvasMap=[]
            self.read_map()
            self.AgentsPos=[]
            self.AgentsEndPos=[]
            self.AgentCost=[]
            self.CanvasAgents=[]
            self.max_agents_length=0
            self.read_agent()
        def read_map(self):
            self.fmap.readline()
            for i in self.fmap:  #iterate each line in fmap
                self.BinaryMap.append(list(map(int, i.split(','))))
            """based on width, resize"""
            self.a=(len(self.BinaryMap[0])-201.75)/(-155/40)
            # print(self.a)
        def read_agent(self):
            tmp=self.fagents.readlines()
            #tmp=self.fagents.split('\n')
            for i, line in enumerate(tmp):
                if "Agent 0" in line:
                    break

            tmp = tmp[i:]

            self.stuffMap=[['' for x in range(len(self.BinaryMap[0]))] for _ in range(len(self.BinaryMap))]

            for j in range(len(tmp[:self.numAgent])):
                tempt=tmp[:self.numAgent][j].strip('\n')
                tempt=[i for i in tempt.split(' ') if i[0]=="(" and i[-1]==")" and len(i)>4]
                # +1 to x and y value otherwise don't match
                tempt=list(map(lambda x:(int(x[0])+1,int(x[1])+1),list(map(lambda x:x.strip('()').split(','),tempt))))
                self.AgentsPos.append(tempt)
                self.AgentsEndPos.append(tempt[-1])
                """-1 or not?"""
                self.AgentCost.append(len(tempt)-1)
                for ttt in range(len(tempt)):
                    self.stuffMap[tempt[ttt][0]][tempt[ttt][1]]+="Agent: "+str(j)+" t: "+str(ttt)+'\n'
            
            self.max_agents_length=len(max(self.AgentsPos, key=len))
            """store constraint"""
            tempt=tmp[self.numAgent].strip('\n')
            tempt=[i for i in tempt.split(' ') if len(i)>12]
            # print([ast.literal_eval(i)[0] for i in tempt])
            # print([ast.literal_eval(i)[1] for i in tempt])
            cons_loc1=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[0] for i in tempt]))
            # print(cons_loc1)
            cons_loc2=list(map(lambda x:(x[0]+1,x[1]+1),[ast.literal_eval(i)[1] for i in tempt]))
            # print(cons_loc2)
            cons_agent=[ast.literal_eval(i)[2] for i in tempt]
            # print(cons_agent)
            cons_time=[ast.literal_eval(i)[3] for i in tempt]
            # print(cons_time)
            timeKeyZip = [list(z) for z in zip(cons_loc1, cons_loc2,cons_agent)]
            # print(timeKeyZip)
            self.cons_time_dict = defaultdict(list)
            for i in range(len(cons_time)):
                self.cons_time_dict[cons_time[i]].append(timeKeyZip[i])
            #print(self.cons_time_dict)
            
            for k,v in self.cons_time_dict.items():
                for tt in v:
                    self.stuffMap[tt[0][0]][tt[0][1]]+="Agent: "+str(tt[2])+" t: "+str(k)+'(Constraint)\n'
                    if (tt[1]!=(0,-1)):
                        self.stuffMap[tt[1][0]][tt[1][1]]+="Agent: "+str(tt[2])+" t: "+str(k)+'(Constraint)\n'
	    
            agentKeyZip = [list(z) for z in zip(cons_loc1, cons_loc2,cons_time)]
            # print(timeKeyZip)
            self.cons_agent_dict = defaultdict(list)
            for i in range(len(cons_agent)):
                self.cons_agent_dict[cons_agent[i]].append(agentKeyZip[i])
            # print(self.cons_agent_dict)
            self.agentsPath=[None]*len(self.AgentsPos)

        def draw_map(self,canvas):
            """
            Function to draw the map on canvas
            """

            self.CanvasMap=[[0 for x in range(len(self.BinaryMap[0]))] for _ in range(len(self.BinaryMap))]
            for x in range(len(self.BinaryMap[0])):  #165
                    for y in range(len(self.BinaryMap)):   #63
                        if self.BinaryMap[y][x]:
                            self.CanvasMap[y][x]=(
                                canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                                self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                                fill='#8080C0')
                            )
                        else:
                            self.CanvasMap[y][x]=(
                                canvas.create_rectangle(self.x0 + x * self.a, self.y0 + y * self.a,
                                                self.x0 + (x + 1) * self.a, self.y0 + (y + 1) * self.a,
                                                fill='#FBFBEA')
                            )
                        if (y,x) in self.AgentsEndPos:
                            canvas.itemconfig(self.CanvasMap[y][x], fill='#FFC0CB')  #fill end point with pink color

                        #when user click on the object, display or remove its path.
                        canvas.tag_bind(self.CanvasMap[y][x], '<Button-1>', lambda event, x=x,y=y : self.blabla(x,y, canvas))
                        canvas.tag_bind(self.CanvasMap[y][x], '<Enter>', lambda event, x=x,y=y : self.blabla1(x,y, canvas))
                        canvas.tag_bind(self.CanvasMap[y][x], '<Leave>', lambda event : self.blabla2())
        def blabla(self, x, y, canvas):
            if (y,x) in self.AgentsEndPos:
                i=self.AgentsEndPos.index((y, x))
                self.showPath(i, canvas)
            # self.tipwindow = tw = Toplevel(canvas)
        def blabla1(self,x, y, canvas):
            self.tipwindow = tw = Toplevel(canvas)
            x1,y1,_,_=canvas.coords(self.CanvasMap[y][x])
            x2 = canvas.winfo_rootx()
            y2 = canvas.winfo_rooty()
            x1=x1+x2+self.a
            y1=y1+y2-self.a

            tw.wm_overrideredirect(1)
            tw.wm_geometry("+%d+%d" % (x1,y1))
            txt=str(y-1)+","+str(x-1)+"\n"+self.stuffMap[y][x]   #-1 -1 here cuz we +1 +1 when reading
            """"""


            label = Label(tw, text=txt, justify=LEFT,
                          background="#ffffe0", relief=SOLID, borderwidth=1,
                          font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)
        def blabla2(self):
            tw = self.tipwindow
            self.tipwindow = None
            if tw:
                tw.destroy()

        def draw_agents(self,canvas,frame,frame2):
            """
            Function that draws agent on map.
            Bind tags to the agent object:
                self.w Label is with the Frame. Will display the AI number when user hover on it
                when user click on the agent, display its path. Click again to remove its path.
            """
            self.initialize_frame(frame2,canvas)

            frame.text.insert("end","Timestep: 0"+"\n",'current')
            for i in range(len(self.AgentsPos)):
                self.CanvasAgents.append(canvas.create_oval(self.x0 + self.AgentsPos[i][0][1] * self.a, self.y0 + self.AgentsPos[i][0][0] * self.a,
                                                            self.x0 + (self.AgentsPos[i][0][1] + 1) * self.a, self.y0 + (self.AgentsPos[i][0][0] + 1) * self.a,
                                                            fill='#B45B3E'))

                #when user click on the object, display or remove its path.
                canvas.tag_bind(self.CanvasAgents[-1], '<Button-1>', lambda event, i=i : self.showPath(i, canvas))

                #update the AI number when user hover on the agent
                canvas.tag_bind(self.CanvasAgents[-1], '<Enter>', lambda event, i=i : self.checkAIno(i,canvas))
                canvas.tag_bind(self.CanvasAgents[-1], '<Leave>', lambda event: self.blabla2())
                frame.text.insert("end", "Agent " + str(i) + ": " +"(" + str(self.AgentsPos[i][0][0] - 1) + "," + str(self.AgentsPos[i][0][1] - 1) + ")" + "\n")

        def initialize_frame(self,frame,canvas):

            #self.currentTimeLabel = Label(frame, text="Time: ",font=("Arial", 16))
            #self.currentTimeLabel.grid(row=0, column=0,columnspan=2,pady=(0,10))

            """ show/hide all path """
            self.showhidePathButton = Button(frame, text='Show All Path', width=10, height=3, bg='white', fg='black', command=lambda: self.showAllPath(canvas))
            self.showhidePathButton.grid(row=2, column=0, columnspan=2, pady=10)
            myFont = font.Font(size=10)

            self.zoomInButton = Button(frame, text='+',width=5,height=3, bg='white', fg='black', command=lambda: self.zoomIn(canvas))
            self.zoomInButton['font'] = myFont

            self.zoomInButton.grid(row=6, column=0,pady=10)
            self.zoomOutButton = Button(frame, text='-',width=5,height=3, bg='white', fg='black', command=lambda: self.zoomOut(canvas))
            self.zoomOutButton['font'] = myFont
            self.zoomOutButton.grid(row=6, column=1,pady=10)

            """ check agent No """
            self.ai = Label(frame, text="AI: \nObj Cost: ",font=("Helvetica",18))
            self.ai.grid(row=0, column=0,columnspan=2)

            """show/hide agent"""
            self.checkBoxVar=[None for i in range(self.numAgent)]
            self.checkBox=[]
            for i in range(self.numAgent):
                self.checkBoxVar[i] = IntVar(value=1)
                c = Checkbutton(frame, text = "AI"+str(i), variable=self.checkBoxVar[i], command=lambda i=i: self.showhideOneAI(i, canvas))
                c.grid(row=7+i//2, column=i%2)
                self.checkBox.append(c)
            def tickall():
                self.clearallAgentButton.deselect()
                for i in range(len(self.checkBox)):
                    self.checkBox[i].select()
                    canvas.itemconfigure(self.CanvasAgents[i], state='normal')
            def clearall():
                self.tickallAgentButton.deselect()
                for i in range(len(self.checkBox)):
                    self.checkBox[i].deselect()
                    canvas.itemconfigure(self.CanvasAgents[i], state='hidden')

            self.tickallAgentButton = Checkbutton(frame, text='tick all',variable=IntVar(value=1), command=tickall)
            self.tickallAgentButton.grid(row=8+self.numAgent//2, column=0)

            self.clearallAgentButton = Checkbutton(frame, text='clear all',variable=IntVar(value=0),command=clearall)
            self.clearallAgentButton.grid(row=8+self.numAgent//2, column=1)

        def showhideOneAI(self, i, canvas):
            if (self.checkBoxVar[i].get() == 1):
                canvas.itemconfigure(self.CanvasAgents[i], state='normal')
                self.clearallAgentButton.deselect()


            elif (self.checkBoxVar[i].get() == 0):
                canvas.itemconfigure(self.CanvasAgents[i], state='hidden')
                self.tickallAgentButton.deselect()

        def zoomIn(self,canvas):
            self.a+=1
            for i in range(len(self.CanvasAgents)):
                timestamp=min(self.currentTime,len(self.AgentsPos[i])-1)
                x0, y0, x1, y1 = canvas.coords(self.CanvasAgents[i])
                x0 = x0 + self.AgentsPos[i][timestamp][1]*1
                x1 = x1 + (self.AgentsPos[i][timestamp][1]+1)*1
                y0 = y0 + self.AgentsPos[i][timestamp][0]*1
                y1 = y1 + (self.AgentsPos[i][timestamp][0]+1)*1
                canvas.coords(self.CanvasAgents[i], x0, y0, x1, y1)

            for x in range(len(self.CanvasMap[0])):  #165
                    for y in range(len(self.CanvasMap)):   #63
                        x0, y0, x1, y1 = canvas.coords(self.CanvasMap[y][x])
                        x0 = x0 + x*1
                        x1 = x1 + (x+1)*1
                        y0 = y0 + y*1
                        y1 = y1 + (y+1)*1
                        canvas.coords(self.CanvasMap[y][x], x0, y0, x1, y1)
        def zoomOut(self,canvas):
            self.a-=1
            for i in range(len(self.CanvasAgents)):
                timestamp=min(self.currentTime,len(self.AgentsPos[i])-1)
                x0, y0, x1, y1 = canvas.coords(self.CanvasAgents[i])
                x0 = x0 - self.AgentsPos[i][timestamp][1]*1
                x1 = x1 - (self.AgentsPos[i][timestamp][1]+1)*1
                y0 = y0 - self.AgentsPos[i][timestamp][0]*1
                y1 = y1 - (self.AgentsPos[i][timestamp][0]+1)*1
                canvas.coords(self.CanvasAgents[i], x0, y0, x1, y1)

            for x in range(len(self.CanvasMap[0])):  #165
                    for y in range(len(self.CanvasMap)):   #63
                        x0, y0, x1, y1 = canvas.coords(self.CanvasMap[y][x])
                        x0 = x0 - x*1
                        x1 = x1 - (x+1)*1
                        y0 = y0 - y*1
                        y1 = y1 - (y+1)*1
                        canvas.coords(self.CanvasMap[y][x], x0, y0, x1, y1)

        def displayAIDetail(self, canvas, inputtxt, textbox):
                textbox.delete('1.0', END)
                inp1 = inputtxt.get()
                try:
                    inputList=[int(i) for i in inp1.split(",") if (0<=int(i) and int(i)<len(self.AgentsPos))]
                except ValueError:
                    print("must be integer seperated by comma, eg. 0,3,4")
                    return
                maxlen=0
                for inp in inputList: #agent 4 6
                    self.showPath(inp,canvas,True)
                    maxlen=max(maxlen,len(self.AgentsPos[inp]))
                tmpArrayList=[]
                temp="Compare AI "
                for inp in inputList:
                    temp+=str(inp)+","
                    tmpArray=self.AgentsPos[inp]
                    if len(tmpArray)<maxlen:
                        tmpArray+=[tmpArray[-1]]*(maxlen-len(tmpArray))
                    tmpArrayList.append(tmpArray)
                textbox.insert("end",temp+"\n")

                for tt in range(len(tmpArrayList[0])):
                    temp=""
                    # print(tt)
                    temp+=str(tt)+":"
                    for numAI in range(len(tmpArrayList)):
                        temp+="("+str(tmpArrayList[numAI][tt][0]-1)+","+str(tmpArrayList[numAI][tt][1]-1)+")\t"

                    temp+="\n"
                    textbox.insert("end",temp,'current')

                temp=""
                for agent in inputList:
                    temp+="Constraint of AI "+str(agent)+" :\n"
                    if (agent in self.cons_agent_dict.keys()):
                        # print("what")
                        for value in self.cons_agent_dict[agent]:
                            temp+="time: "+str(value[2])+"\npos: "+"("+str(value[0][0]-1)+","+str(value[0][1]-1)+")\n"
                textbox.insert("end",temp,'current')

                textbox.see("end")

        def showAllPath(self,canvas):
            if self.showhidePathButton["text"] == "Show All Path":
                self.showhidePathButton["text"] = "Hide All Path"
                for index in range(len(self.AgentsPos)):
                    if self.agentsPath[index]:
                        for obj in self.agentsPath[index]:
                            canvas.delete(obj)

                self.agentsPath=[[] for _ in range(len(self.AgentsPos))]
                for index in range(len(self.AgentsPos)):

                    de=("%02x"%random.randint(0,255))
                    re=("%02x"%random.randint(0,255))
                    we=("%02x"%random.randint(0,255))
                    ge="#"
                    color=ge+de+re+we

                    list_of_screen_coods = self.AgentsPos[index]
                    for (x1,y1,x2,y2) in self.linemaker(list_of_screen_coods):
                        self.agentsPath[index].append(canvas.create_line(x1,y1,x2,y2, width=1.5,fill=color))
                    self.agentsPath[index].append(canvas.create_line(x1,y1,x2,y2, width=1.5,fill=color,arrow=LAST))
            else:
                self.showhidePathButton["text"] = "Show All Path"
                for index in range(len(self.AgentsPos)):
                    if self.agentsPath[index]:      #not None, has value in it, we delete obj
                        for obj in self.agentsPath[index]:
                            canvas.delete(obj)
                self.agentsPath=[None]*len(self.AgentsPos)


        def checkAIno(self,i,canvas):
            """
            Function to update the AI number when user hover on the agent
            """
            time=min(self.currentTime,len(self.AgentsPos[i])-1)
            temp="AI: "+str(i)+"\nObj Cost: "+str(self.AgentCost[i])
            self.ai.config(text=temp)
            x,y=self.AgentsPos[i][time]
            self.blabla1(y,x,canvas)


        def linemaker(self,screen_points):
            """
            Function to take list of points and make them into lines
            """
            is_first = True
            # Set up some variables to hold x,y coods
            x1 = y1 = 0
            # Grab each pair of points from the input list
            for (y,x) in screen_points:
                # If its the first point in a set, set x0,y0 to the values
                x=x*self.a + self.x0 + 0.5*self.a
                y=y*self.a + self.y0 + 0.5*self.a
                if is_first:
                    x1 = x
                    y1 = y
                    is_first = False
                else:
                    # If its not the fist point yeild previous pair and current pair
                    yield x1,y1,x,y
                    # Set current x,y to start coords of next line
                    x1,y1 = x,y

        def showPath(self, index, canvas,flag=False):
            """
            Function that when user click on the object, display or remove its path.
            """
            de=("%02x"%random.randint(0,255))
            re=("%02x"%random.randint(0,255))
            we=("%02x"%random.randint(0,255))
            ge="#"
            color=ge+de+re+we

            list_of_screen_coods = self.AgentsPos[index]
            # print(list_of_screen_coods)
            if self.agentsPath[index] == None or flag:
                self.agentsPath[index]=[]
                for (x1,y1,x2,y2) in self.linemaker(list_of_screen_coods):
                    # print(str(x1)+" "+str(y1)+" "+str(x2)+" "+str(y2)+" ")
                    self.agentsPath[index].append(canvas.create_line(x1,y1,x2,y2, width=1.5,fill=color))
                #fill the last line with arrow
                self.agentsPath[index].append(canvas.create_line(x1,y1,x2,y2, width=1.5,fill=color,arrow=LAST))

                # canvas.itemconfig(self.CanvasAgents[index], fill='red')

            else:
                for obj in self.agentsPath[index]:
                    canvas.delete(obj)
                self.agentsPath[index] = None

                # canvas.itemconfig(self.CanvasAgents[index], fill='#B45B3E')


        def move_agents(self,t,canvas,frame,doBackward):
            """
            Funciton that move each agents in one timestamp.
            """
            frame.text.delete('1.0', END) #pagination!
            
            self.currentTime=t  #this is for zoom in and zoom out
            if doBackward:
                self.currentTime=t-1

            #tmp="Time: "+str(self.currentTime)
            #self.currentTimeLabel.config(text=tmp)

            if doBackward:
                """must t-1, otherwise magic happen"""
                self.currentTime=t-1
                frame.text.insert("end","\n")
                frame.text.insert("end","Timestep: "+str(t-1)+"\n",'current')
                for i in range(len(self.AgentsPos)):
                    #if still moving.
                    if 0<t<len(self.AgentsPos[i]):
                        canvas.move(self.CanvasAgents[i], (self.AgentsPos[i][t - 1][1] - self.AgentsPos[i][t][1]) * self.a, (self.AgentsPos[i][t - 1][0] - self.AgentsPos[i][t][0]) * self.a)
                        #add text description to the frame
                        frame.text.insert("end", "Agent " + str(i) + ": " +"(" + str(self.AgentsPos[i][t - 1][0] - 1) + "," + str(self.AgentsPos[i][t - 1][1] - 1) + ")" + "\n")
                        frame.text.see("end")
                    elif t==len(self.AgentsPos[i]):
                        canvas.itemconfig(self.CanvasAgents[i], fill='#B45B3E')
                        #reduce the oval's size once it reaches the destination
                        #because cosntraint might later appear on the same spot
                        x0, y0, x1, y1 = canvas.coords(self.CanvasAgents[i])
                        x0 = x0 - 2
                        x1 = x1 + 2
                        y0 = y0 - 2
                        y1 = y1 + 2
                        canvas.coords(self.CanvasAgents[i], x0, y0, x1, y1)
                    #else t<=0,do nothing
            else:
                tt=1
                frame.text.insert("end","\n")
                frame.text.insert("end","Timestep: "+str(t)+"\n",'current')

                if (t in self.cons_time_dict.keys()):
                    for value in self.cons_time_dict[t]:
                        canvas.itemconfig(self.CanvasMap[value[0][0]][value[0][1]], fill='#0000FF')
                        #add text description to the frame
                        frame.text.insert("end", "Constraint time "+str(t) + ":\n"+"("+str(value[0][0]-1)+","+str(value[0][1]-1)+")"+"\n",'constraint')
                        frame.text.see("end")
                        if (value[1][0],value[1][1]) != (0,-1):
                            canvas.itemconfig(self.CanvasMap[value[1][0]][value[1][1]], fill='#0000FF')

                for i in range(len(self.AgentsPos)):
                    #if still moving.
                    if t<len(self.AgentsPos[i]):
                        canvas.move(self.CanvasAgents[i], (self.AgentsPos[i][t][1] - self.AgentsPos[i][t - 1][1]) * self.a, (self.AgentsPos[i][t][0] - self.AgentsPos[i][t - 1][0]) * self.a)
                        #add text description to the frame
                        frame.text.insert("end", "Agent " + str(i) + ": " +"(" + str(self.AgentsPos[i][t][0] - 1) + "," + str(self.AgentsPos[i][t][1] - 1) + ")" + "\n")
                        frame.text.see("end")
                        #an agent is still moving, so repeater continues
                        tt=0
                    #elif the agent stops, change its color to green
                    elif t==len(self.AgentsPos[i]):
                        canvas.itemconfig(self.CanvasAgents[i], fill='#00FF00')
                        #reduce the oval's size once it reaches the destination
                        #because cosntraint might later generate on it
                        x0, y0, x1, y1 = canvas.coords(self.CanvasAgents[i])
                        x0 = x0 + 2
                        x1 = x1 - 2
                        y0 = y0 + 2
                        y1 = y1 - 2
                        canvas.coords(self.CanvasAgents[i], x0, y0, x1, y1)
                    #elif the agent have stopped, move (0,0) so speed don't accelerate
                    elif t>len(self.AgentsPos[i]) and t<=self.max_agents_length:
                        canvas.move(self.CanvasAgents[i], 0, 0)
                    else:
                        print("error?")
                #return True if no agent is moving
                return tt


if __name__=="__main__":
    # temp=info("test_25.txt","warehouse-10-20-10-2-1.map.ecbs",25)
    temp=info("test_2.txt","debug-6-6.map.ecbs",2)

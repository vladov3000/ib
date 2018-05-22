import pygame 

import time 

import math 

import collections 

import random 

 

ifsetup = True 

thestat = 0 

# setting up pygame stuff 

pygame.init() 

infoObject = pygame.display.Info() 

height = infoObject.current_h 

width = infoObject.current_w 

print("Screen Resolution: %s, %s" % (infoObject.current_w, infoObject.current_h)) 

gameDisplay = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN) 

clock = pygame.time.Clock() 

pygame.display.set_caption('UPlan')  # set window title 

 

vertices = []  # where all the vertices are stored 

warningMessages = []  # where all the warningMessages are stored 

roads = []  # where all the roads are stored 

cars = []  # where all the cars are stored 

staticTexts = [] 

connections = {} 

ncars=30 

 

#2 vertice input, outputs array of vertices 

def myBFScost(state,end): 

    queue = PriorityQueue() 

    visited = [] 

    queue.push((state, [],0),0) 

    #print(queue.heap) 

    while not queue.isEmpty(): 

        current = queue.pop() 

        if current[0]==end: 

            return current[1] 

        successors = [(i, i,((i.x-current[0].x)**2+(i.x-current[0].x)**2)**0.5) for i in connections[current[0]]] 

        successors.reverse() 

        for i in successors: 

            if i[0] not in visited: 

                tempPush = (i[0], [j for j in current[1]],current[2]+i[2]) 

                tempPush[1].append(i[1]) 

                visited.append(i[0]) 

                queue.push(tempPush,tempPush[2]) 

    return [state,end] 

 

 

def text_objects(text, font, color): 

    textSurface = font.render(text, True, color) 

    return textSurface, textSurface.get_rect() 

 

class PriorityQueue: 

    """ 

      Implements a priority queue data structure. Each inserted item 

      has a priority associated with it and the client is usually interested 

      in quick retrieval of the lowest-priority item in the queue. This 

      data structure allows O(1) access to the lowest-priority item. 

    """ 

    def  __init__(self): 

        self.heap = [] 

 

    def push(self, item, priority): 

        self.heap.append((item, priority)) 

        self.heap.sort(key=lambda x: x[1]) 

 

    def pop(self): 

        temp=self.heap[0][0] 

        self.heap=self.heap[1:] 

        return temp 

 

    def isEmpty(self): 

        return len(self.heap) == 0 

 

class Car(): 

    def __init__(self, v1, v2, path=[], v=0, a=0.075): 

        if path==[]: 

            self.path=myBFScost(v1,v2) 

            self.path.insert(0,v1) 

            self.v1 = self.path[0] 

            self.v2 = self.path[1] 

        else: 

            self.path=path 

            self.v1 = v1 

            self.v2 = v2 

 

        self.pos = (v1.x,v1.y) 

        self.endpos = (self.path[1].x,self.path[1].y) 

        #self.path=myBFScost(v1,v2) 

        self.v = v 

        self.a = a 

        self.t=0 

        self.boost = False 

        self.boostval = 0 

 

 

 

        for r in roads: 

            if (self.pos==(int(r.x),int(r.y)) and self.endpos==(int(r.x1),int(r.y1))) or (self.endpos==(int(r.x),int(r.y)) and self.pos==(int(r.x1),int(r.y1))): 

                r.onRoad.append(self) 

                self.road = r 

                break 

        #print(self.road) 

        self.order=connections[self.v2].index(self.v1) 

        self.maxorder=len(connections[self.v2]) 

        cars.append(self) 

 

    def __str__(self): 

        print(self.pos, self.endpos) 

 

    def isTouching(self, x1, y1): 

        tempD = ((x1 - self.pos[0]) ** 2 + (y1 - self.pos[1]) ** 2) ** 0.5  # Find distance between them 

        if tempD <= 20: 

            return True 

        else: 

            return False 

 

 

class WarningMessage(): 

    def __init__(self, message): 

        self.message = message 

        self.timer = 100  # initialize timer for warning 

        warningMessages.append(self)  # add it to the vertices list 

 

    def __str__(self): 

        return "[Warning Message: " + self.message  # Prints this when printing warning obj 

 

 

class StaticText(): 

    def __init__(self, message): 

        self.message = message 

        staticTexts.append(self)  # add it to the vertices list 

 

    def __str__(self): 

        return "[Static Text: " + self.message  # Prints this when printing warning obj 

 

 

class Road(): 

    def __init__(self, x, y, x1, y1): 

        self.x, self.y = x, y 

        self.x1, self.y1 = x1, y1 

        self.width = int(infoObject.current_w / 373.6) * 4 

        self.right=[i for i in range(0,self.length()+1)] 

        self.left = [i for i in range(0, self.length() + 1)] 

        self.onRoad = [] 

        roads.append(self) 

 

 

    def __str__(self): 

        return "[Road: %s, %s]" % ((self.x, self.y), (self.x1, self.y1))  # Prints this when printing vertex obj 

 

    def length(self): 

        return int(((self.x+self.x1)^2+(self.y+self.y1)^2)**0.5) 

 

    def isTouching(self, x3, y3): 

        def isTouching(self, x3, y3): 

            x1 = self.x1 

            x2 = self.x2 

            y1 = self.y1 

            y2 = self.y2 

 

            slope1 = (y2 - y1) / (x2 - x1) 

            slope2 = (1 / slope1) * -1 

 

            c1 = y1 - (slope1 * x1) 

            c2 = y3 - (slope2 * x3) 

 

            x4 = (c2 - c1) / (slope1 - slope2) 

            y4 = slope1 * x4 + c1 

 

            distance = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** 1 / 2 

 

            if distance > self.width: 

                return False 

 

            c1 = y1 - slope2 * x1 

            c2 = y2 - slope2 * x2 

 

            liney1 = slope2 * x1 + c1 

            liney2 = slope2 * x2 + c2 

 

            if (liney1 > y3 and liney2 < y3) or (liney1 < y3 and liney2 > y3): 

                return True 

            else: 

                return False 

 

class Vertex(): 

    def __init__(self, x, y): 

        self.x = x 

        self.y = y 

        self.radius = int(infoObject.current_w / 373.6)  # keeps a constant pixel radius 

        self.timer = 100  # time left before disappear 

        self.traffic=0 

        self.roads = 0 

        vertices.append(self)  # add it to the vertices list 

        connections[self] = [] 

 

    def __str__(self): 

        return "[Vertex: %s, %s]" % (self.x, self.y)  # Prints this when printing vertex obj 

 

    def isTouching(self, x1, y1): 

        tempD = ((x1 - v.x) ** 2 + (y1 - v.y) ** 2) ** 0.5  # Find distance between them 

        if tempD <= v.radius: 

            return True 

        else: 

            return False 

 

 

def RenderVertices(): 

    for v in vertices: 

        if v.timer%300==0 and v in connections.keys(): 

            v.traffic = (v.traffic + 1) % (len(connections[v]) + 1) 

        v.timer+=1 

 

        if len(connections[v]) > 0: 

            pygame.draw.circle(gameDisplay, (0, 0, 0), (v.x, v.y), v.radius * 2) 

        if v == vertexSelected: 

            pygame.draw.circle(gameDisplay, (0, 255, 0), (v.x, v.y), v.radius) 

        else: 

            pygame.draw.circle(gameDisplay, (0, 0, 255), (v.x, v.y), v.radius) 

 

 

def RenderWarningMessages(): 

    for w in warningMessages: 

        font1 = pygame.font.Font('freesansbold.ttf', 40)  # creates a font 

        TextSurf, TextRect = text_objects(w.message, font1, (255, 0, 0))  # 

        TextRect.center = ((infoObject.current_w / 2), (infoObject.current_h / 2))  # set the center 

        gameDisplay.blit(TextSurf, TextRect)  # put it on the screen 

        w.timer -= 1 

        # print(w.timer) 

        if w.timer == 0: 

            warningMessages.remove(w) 

 

 

def RenderStaticText(): 

    for w in staticTexts: 

        font1 = pygame.font.Font('freesansbold.ttf', 40)  # creates a font 

        TextSurf, TextRect = text_objects(w.message, font1, (0, 0, 0))  # 

        TextRect.center = ((infoObject.current_w / 2), (infoObject.current_h / 2))  # set the center 

        gameDisplay.blit(TextSurf, TextRect)  # put it on the screen 

 

 

def RenderMisc(): 

    return 

 

 

def RenderRoads(): 

    for r in roads: 

        pygame.draw.line(gameDisplay, (0, 0, 0), (r.x, r.y), (r.x1, r.y1), r.width*2) 

 

def RenderCars(): 

    global thestat 

    for c in cars: 

 

        #print(c.pos) 

        if (abs(round(c.pos[0], 0)) - c.endpos[0])**2 + (abs(round(c.pos[1], 0)) - c.endpos[1])**2<=100: 

      # if ((c.pos[0]-c.endpos[0])**2 + (c.pos[1]-c.endpos[1])**2)**0.5<=30: 

            if len(c.path)>=3: 

                Car(c.path[1],c.path[2],c.path[1:]) 

            else: 

                makeRandomCar() 

            cars.remove(c) 

            c.road.onRoad.remove(c) 

        dx = c.endpos[0] - c.pos[0] 

        dy = c.endpos[1] - c.pos[1] 

 

        angle = abs(math.atan(dy / dx)) 

 

        vy = math.sin(angle) *c.v 

        vx = math.cos(angle) *c.v 

 

        ay = math.sin(angle) *c.a 

        ax = math.cos(angle) * c.a 

 

        if dy <= 0 and dx <= 0: 

            vy *= -1 

            ay *= -1 

            ax *= -1 

            vx *= -1 

        elif dy <= 0 and dx >= 0: 

            ay *= -1 

            vy *= -1 

        elif dy >= 0 and dx <= 0: 

            ax *= -1 

            vx *= -1 

        elif dy >= 0 and dx >= 0: 

            ax *= 1 

            vx *= 1 

 

        update=True 

        for c1 in c.road.onRoad: 

                if c!=c1: 

                    if ((c1.pos[0]-c.pos[0])**2+(c1.pos[1]-c.pos[1])**2)**0.5<=30 and c.endpos==c1.endpos and c!=c1: 

                        if (vx > 0 and c1.pos[0] > c.pos[0]) or (vx < 0 and c1.pos[0] < c.pos[0]): 

                            update=False 

                            c.t=0 

                            c.v=0 

                            break 

        if update: 

            if ((c.endpos[0] - c.pos[0]) ** 2 + (c.endpos[1] - c.pos[1]) ** 2) ** 0.5 <= 60 and c.maxorder>2 and c.v2.traffic!=c.order: 

                update=False 

                c.t = 0 

                c.v = 0 

                #print('nope') 

 

        if update: 

            if c.v < 2: 

                if c.t < 50: 

                    c.t += 1 

                else: 

                    c.v = ((vy + ay) ** 2 + (vx + ax) ** 2) ** 0.5 

            c.pos = (c.pos[0] + vx, c.pos[1] + vy) 

        if not update: 

            v=0 

            c.t=0 

            #print('nope') 

        if abs(dy)>abs(dx): 

            if dy<0: 

                pygame.draw.circle(gameDisplay, (255, 0, 0), (int(c.pos[0]+10), int(c.pos[1])), 10) 

            else: 

                pygame.draw.circle(gameDisplay, (255, 0, 0), (int(c.pos[0]-10), int(c.pos[1])), 10) 

        else: 

            if dx<0: 

                pygame.draw.circle(gameDisplay, (255, 0, 0), (int(c.pos[0]), int(c.pos[1]+10)), 10) 

            else: 

                pygame.draw.circle(gameDisplay, (255, 0, 0), (int(c.pos[0]), int(c.pos[1]-10)), 10) 

 

 

        thestat += c.v 

        #if c.boost == False: 

        #    if vx > 0: 

        #       c.pos = (c.pos[0], c.pos[1]+20) 

        #    else: 

        #       c.pos = (c.pos[0],c.pos[1]-20) 

        #    c.boost = True 

 

def makeRandomCar(): 

    keys = [i for i in connections.keys()] 

    if len(keys) > 1: 

        v1 = keys[random.randint(0, len(keys) - 1)] 

        v2 = keys[random.randint(0, len(keys) - 1)] 

        while not [i.isTouching(v2.y, v2.x) for i in cars] == [False for i in cars]: 

            v2 = keys[random.randint(0, len(keys) - 1)] 

        while True: 

            if not [i.isTouching(v1.y, v1.x) for i in cars] == [False for i in cars]: 

                v1 = keys[random.randint(0, len(keys) - 1)] 

            elif len(connections[v1])>1: 

                v1 = keys[random.randint(0, len(keys) - 1)] 

            elif v1 == v2: 

                v1 = keys[random.randint(0, len(keys) - 1)] 

            else: 

                break 

        return Car(v1, v2) 

 

v1 = Vertex(int(infoObject.current_w / 2), int(infoObject.current_h / 2))  # creates new vertex at (0,0) 

# w1 = WarningMessage("ERROR: ewyurhbfm,sdfsd") 

#r1 = Road(int(infoObject.current_w/2), int(infoObject.current_h/2),1000,1000) 

#c1 = Car((1000,700),(700,1000),0,0.075,r1) 

# t1 = StaticText("hewo worwd") 

windowExit = False 

vertexSelected = None 

keys = pygame.key.get_pressed() 

#print(connections[v1]) 

ihadtodoittoem=True 

shiftheld = False 

 

statstimer=0 

 

while not windowExit: 

    #print(len(cars)) 

    if ifsetup == True: 

        # print(keys) 

        for event in pygame.event.get(): 

 

            keys = pygame.key.get_pressed() 

 

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1: 

                ifsetup = False 

 

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT: 

                shiftheld = True 

            if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT: 

                shiftheld = False 

            if event.type == pygame.QUIT: 

                windowExit = True 

            if event.type == pygame.MOUSEBUTTONDOWN: 

                if event.button == 1:  # left click 

                    if shiftheld == True: 

                        if vertexSelected is not None: 

                            for v in vertices: 

                                if v.isTouching(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): 

                                    connections[vertexSelected].append(v) 

                                    connections[v].append(vertexSelected) 

                                    tempR = Road(v.x, v.y, vertexSelected.x, vertexSelected.y) 

                                    vertexSelected = None 

                                    break 

                    else: 

                        place = True 

                        for v in vertices: 

                            if v.isTouching(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): 

                                place = False 

                                vertexSelected = v 

                                break 

                        if place: 

                            tempV = Vertex(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) 

                            vertexSelected = None 

                if event.button == 3:  # right click 

                    for v in vertices: 

                        if v.isTouching(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): 

                            vertices.remove(v) 

                            connections[v] = [] 

                            connections.pop(v,None) 

                            for key in connections.keys(): 

                                if v in connections[key]: 

                                    connections[key].remove(v) 

                    for r in roads: 

                        if r.isTouching(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]): 

                            roads.remove(r) 

                            v1=None 

                            v2=None 

                            for v in vertices: 

                                if (r.x1,r.y1)==(v.x,v.y) or (r.x1,r.y1)==(v.x,v.y): 

                                    if v1==None: 

                                        v1=v 

                                    else: 

                                        v2=v 

                            connections[v1].remove(v2) 

                            connections[v2].remove(v1) 

    if ifsetup == False: 

        statstimer += 1 

 

    if statstimer%10000 == 9999: 

        print(thestat/statstimer) 

 

    if ifsetup == False and ihadtodoittoem: 

        ihadtodoittoem=False 

        while len(cars)<ncars: 

            makeRandomCar() 

 

                                    # print(event) 

    # print(cars) 

    # Layers 

    # print(t1,staticTexts) 

    gameDisplay.fill((255, 255, 255))  # make background white 

    RenderRoads()  # Draw Roads 

    RenderVertices()  # Draw Vertices 

    RenderCars()  # Draw Cars 

    RenderMisc() 

    RenderStaticText() 

    RenderWarningMessages()  # DrawWarningMessages 

    pygame.display.update() 

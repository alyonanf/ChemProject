import pygame
from copy import deepcopy, copy

#setting things up
names = ['метан','этан','пропан','бутан','пентан','гексан','гептан','октан','нонан','декан', 'ундекан', 'додекан', 'тридекан', 'тетрадекан', 'пентадекан', 'гексадекан', 'гептадекан', 'октадекан', 'нонадекан', 'эйкозан']
selected_carbons = []
selected_numbers = []
table_connections = []
carbons = []
connections = []
stack = []
ends = []
mainchain = []
max_length = 1
pygame.init()
size = [700, 500]
backgrouncolor  = (177, 211, 220)
textcolor = (0,0,0)
connectioncolor = (0, 0, 0)
carboncolor = (0, 0, 0)
screen = pygame.display.set_mode(size)
screen.fill(backgrouncolor )
pygame.display.set_caption("EasyChem")
dragging_carbon = False
done = False

#classes & functions
class Carbon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Connection:
    def __init__(self, carbon1, carbon2):
        self.carbon1 = carbon1
        self.carbon2 = carbon2

def find_clicked_carbon(pos):
    x, y = pos
    for carbon in carbons:
        if carbon.x-15 < x < carbon.x+15 and carbon.y-15 < y < carbon.y+15:
            return carbons.index(carbon) 

def draw_carbon(screen, carbon):
    pygame.draw.ellipse(screen, carboncolor , [carbon.x-15, carbon.y-15, 30, 30], 0)

def create_carbon(event):
    carbons.append(Carbon(event.pos[0], event.pos[1]))
    row=[0]*len(carbons)
    table=[deepcopy(row) for i in range(len(carbons))]
    return(table)
   
def draw_connection(screen, connection):
    pygame.draw.line(screen, connectioncolor, [connection.carbon1.x, connection.carbon1.y], [connection.carbon2.x, connection.carbon2.y], 2)
    
def create_connection(carbon1, carbon2):                                                   
    connections.append(Connection(carbon1, carbon2))

def find_longest_chain(end):
    x = deepcopy(findingends)
    level = end
    dead_end = level
    stack = [end]
    chain = []
    while stack!=[]:
        level = stack[-1]
        try:
            t = level
            level = x[level].index(1, 0)
            x[t][level]=0
            x[level][t]=0
            stack.append(level)
            if len(stack)>len(chain):
                chain = list(stack)
        except ValueError:
            dead_end = stack.pop()      
    return chain

def showdata():
    screen.fill(backgrouncolor)
    font = pygame.font.SysFont('timesnewroman', 25)
    try:
        name = str(names[(max_length)-1])
        text = font.render("Название главной цепи: " +str(name), True, textcolor)
    except IndexError:
        text = font.render( "это что-то нестандартное, загляните лучше в Википедию", True, textcolor)
    screen.blit(text, [10,460])

    moleclen = font.render("Длина главной цепи:" +" "+ str(max_length), True, textcolor)
    screen.blit( moleclen, [10,435])
    numc = str(len(carbons))
    numh = str(len(carbons)*4-2*len(connections))
    formula = font.render("Формула: C" +(numc)+ "H" +(numh), True, textcolor)
    screen.blit(formula, [10,400])
    molectype = font.render("Класс: алканы", True, textcolor)
    screen.blit(molectype, [10,370])
    

    
#main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if find_clicked_carbon(event.pos)!=None:
                dragged_carbon = carbons[find_clicked_carbon(event.pos)]
            else:
                dragged_carbon = None
            if not dragged_carbon :
                table1 = create_carbon(event)
            else:
                dragging_carbon = True
            showdata()
        elif event.type == pygame.MOUSEMOTION and dragging_carbon:
            dragged_carbon.x, dragged_carbon.y = event.pos
            showdata()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging_carbon:
            dragging_carbon = False
            showdata()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            try:
                number = find_clicked_carbon(event.pos)
                clicked_carbon = carbons[number]
                if clicked_carbon:
                    selected_carbons.append(clicked_carbon)
                    selected_numbers.append(number)
                    if len(selected_carbons)==2:
                        create_connection(selected_carbons[0], selected_carbons[1])
                        selected_carbons.clear()
                        a = selected_numbers[0]
                        b = selected_numbers[1]
                        connectedpair = [a,b] 
                        table_connections.append(connectedpair)
                        selected_numbers.clear()
                        for connectedpair in table_connections:
                            table1[connectedpair[0]][connectedpair[1]]=1
                            table1[connectedpair[1]][connectedpair[0]]=1

                        findingends = table1
                        for i in range (0, len(findingends)):
                            if findingends[i].count(1) == 1:
                                ends.append(i)
                            i = i+1
                            
                        chains = [find_longest_chain(i) for i in ends]
                        chains = [(len(chain), chain) for chain in chains]
                        chains.sort(key=lambda x: -x[0])
                        max_length = chains[0][0]
                showdata()
            
            except TypeError:
                pass

    for carbon in carbons:
        draw_carbon(screen, carbon)
        
    for connection in connections:
        draw_connection(screen, connection)

    pygame.display.flip()

pygame.quit()

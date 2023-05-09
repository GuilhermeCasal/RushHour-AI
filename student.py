"""Example client."""
import asyncio
import getpass
import json
import os
from common import Coordinates, Map, MapException
from tree_search import SearchDomain, SearchProblem, SearchTree
from methods import Ia

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets
import time

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        state = json.loads(
            await websocket.recv()
        )  #
        # Next 3 lines are not needed for AI agent
        # SCREEN = pygame.display.set_mode((299, 123))
        # SPRITES = pygame.image.load("data/pad.png").convert_alpha()
        # SCREEN.blit(SPRITES, (0, 0))
        hel = False
        app = False
        plan = None
        plan2 = None
        key = ""
        do = True
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if do:
                    if hel:
                        print("PLAN2")
                        if not plan2:
                            
                            estado2 = str(state["grid"])
                            est2 = estado2.split("\n")
                            alg2 = Ia(state['cursor']) 
                            p2 = SearchProblem(alg2, "0" + est2[0])  
                            seconds = time.time()
                            t2 = SearchTree(p2,x.state)
                            print("\33[31m",time.time()-seconds,"\33[0m")
                            plan2 = t2.search()
                            print(len(plan2))
                            if len(plan2) <= 1:
                                app = True
                                plan = None
                                continue
                            x2 = plan2.pop(0) 
    
                        key = ""
                        print()
                        action = plan2[0].action
                        print(action)
                        estado = str(state["grid"])
                        est = estado.split("\n")
                        estado = Map(est[0])
        
                        if state['selected']!=action[0]: # piece not selected
                            currHover = estado.get(Coordinates(state['cursor'][0],state['cursor'][1])) 
                            print("ALapeprkropp")
                            if currHover==action[0] or state['selected']!='': # cursor above action piece
                                key = " "
                            else: # cursor not on the right piece (need to move it)
                                pieceCords = estado.piece_coordinates(action[0])
                                if (pieceCords[0].x - state['cursor'][0])!=0: 
                                    key = "a" if pieceCords[0].x - state['cursor'][0] < 0 else "d"
                                elif (pieceCords[0].y - state['cursor'][1])!=0: 
                                    key = "w" if pieceCords[0].y - state['cursor'][1] < 0 else "s"
                        else:
                            if action[1].x!=0: key = "a" if action[1].x < 0 else "d"
                            elif action[1].y!=0: key = "w" if action[1].y < 0 else "s"
                            plan2 = None
                            hel = False  

                    elif app:
                        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                        if not plan:
                            print("APppppp")
                            estado = str(state["grid"])
                            est = estado.split("\n")
                            alg = Ia(state['cursor']) 
                            p = SearchProblem(alg, "0" + est[0])  
                            t = SearchTree(p)
                            seconds = time.time()
                            print("LOADING")
                            plan = t.search()
                            tmp = time.time()-seconds
                            print("\33[31m",time.time()-seconds,"\33[0m")
                            x = plan.pop(0) 

                        key = ""                                      
                        action = plan[0].action
                        estado = str(state["grid"])
                        est = estado.split("\n")
                        estado = Map(est[0])
                        
                        if state['selected']!=action[0]: # piece not selected
                            currHover = estado.get(Coordinates(state['cursor'][0],state['cursor'][1])) 

                            if currHover==action[0] or state['selected']!='': # cursor above action piece
                                key = " "
                            else: # cursor not on the right piece (need to move it)
                                pieceCords = estado.piece_coordinates(action[0])
                                if (pieceCords[0].x - state['cursor'][0])!=0: 
                                    key = "a" if pieceCords[0].x - state['cursor'][0] < 0 else "d"
                                elif (pieceCords[0].y - state['cursor'][1])!=0: 
                                    key = "w" if pieceCords[0].y - state['cursor'][1] < 0 else "s"
                        else:
                            if action[1].x!=0: key = "a" if action[1].x < 0 else "d"
                            elif action[1].y!=0: key = "w" if action[1].y < 0 else "s"
                            x=plan.pop(0)
                        
                        # if plan == None:
                        #     app = False
                    else:
                        if not plan:
                            estado = str(state["grid"])
                            est = estado.split("\n")
                            alg = Ia(state['cursor']) 
                            p = SearchProblem(alg, "0" + est[0])  
                            t = SearchTree(p)
                            seconds = time.time()
                            print("LOADING")
                            plan = t.search()
                            tmp = time.time()-seconds
                            print("\33[31m",time.time()-seconds,"\33[0m")
                            x = plan.pop(0) 
                        key = ""
                        if x.state == "0"+(state["grid"]):
                            action = plan[0].action
                            estado = str(state["grid"])
                            est = estado.split("\n")
                            estado = Map(est[0])
                            
                            if state['selected']!=action[0]: # piece not selected
                                currHover = estado.get(Coordinates(state['cursor'][0],state['cursor'][1])) 

                                if currHover==action[0] or state['selected']!='': # cursor above action piece
                                    key = " "
                                else: # cursor not on the right piece (need to move it)
                                    pieceCords = estado.piece_coordinates(action[0])
                                    if (pieceCords[0].x - state['cursor'][0])!=0: 
                                        key = "a" if pieceCords[0].x - state['cursor'][0] < 0 else "d"
                                    elif (pieceCords[0].y - state['cursor'][1])!=0: 
                                        key = "w" if pieceCords[0].y - state['cursor'][1] < 0 else "s"
                            else:
                                if action[1].x!=0: key = "a" if action[1].x < 0 else "d"
                                elif action[1].y!=0: key = "w" if action[1].y < 0 else "s"
                                x=plan.pop(0)
                                
                            # if tmp > 0.1:
                            #     do = False
                            #     continue

                        else: 
                            if tmp < 1:
                                plan = None
                                state['selected'] = None
                                continue
                            else:
                                hel = True
                                continue
                do = True    
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                ) 
                
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", "103173")
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))

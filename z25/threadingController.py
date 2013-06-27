# -*- coding: utf-8 -*-
#
#     This file is part of BgeHttpServer. Copyright 2013 Stichting z25.org
#
#     PartyTechApp is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     PartyTechApp is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with PartyTechApp.  If not, see <http://www.gnu.org/licenses/>.
#
#
# adaptation from example script of using threads in Blender 2.55 game engine
# thread(!) in ba: http://blenderartists.org/forum/showthread.php?t=204802
# Example of terminating thread is from here:
# http://bytes.com/topic/python/answers/45247-terminating-thread-parent
#
# make sure you keep the python script active through the logic bricks!!!!!
# (always activate TRUE, Level TRUE)

try:
    import bge
except Exception as e:
    print("This module needs to be run inside the Blender Game Engine!")
    raise(e)
import queue

# class that is responsible for stopping thread (thanks to moguri@blenderartists)
class thread_ptr():
    def __init__(self, t):
        print("creating thread_ptr")
        self.thread = t
        
    def __del__(self):
        print("deleting thread_ptr")
        try:
            self.thread.join()
        except Exception as e:
            print("Threadobject's 'join' method is missing, this should not happen", e)
        # self.thread.terminate() # not in Threads

# run this script only once
ob = bge.logic.getCurrentController().owner

def init():
    if ob['init'] == 0:
        ob['init'] = 1

        print("INITIALISING")
        import z25.threadedHttpWsgiServer
        ob['msgQ'] = queue.Queue()
        thread = z25.threadedHttpWsgiServer.serverThread(ob['msgQ'])
        bge.logic.thread = thread_ptr(thread)
        thread.start()
        print("Server running in thread...")
        
def processMessages():
    if ob.get('msgQ'):
        while ob['msgQ'].qsize() > 0:
            try:
                httpMsg = ob['msgQ'].get_nowait()
            except queue.Empty:
                # print("q found, no message")
                pass
            else:
                print("received message: %s" % str(httpMsg))
                parseMessage(httpMsg)
            
def parseMessage(msg):
    objs = bge.logic.getCurrentScene().objects
    if isinstance(msg, dict):
        for objName in msg:
            try:
                obj = objs[objName]
            except Exception as e:
                print("object: %s not found. %s" % (objName, e))
            else:
                for propName in msg[objName]:
                    try:
                        print("pre:", obj[propName], type(msg[objName][propName]))
                        obj[propName] = msg[objName][propName]
                        print("post:", obj[propName])
                    except Exception as e:
                        print("Property %s not found in object: %s. %s" % (objName, propName, e))
                    else:
                        print("Property %s successfully set to %s on object: %s" % (propName, str(msg[objName][propName]), objName))

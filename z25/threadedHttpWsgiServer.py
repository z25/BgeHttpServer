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

import threading

try:
    import bge
except Exception as e:
    print("This module needs to be run inside the Blender Game Engine!")
    raise(e)
import z25.appie
import z25.blendRest
import time

class serverThread(threading.Thread):
    """
    The HTTP Server thread class
    Responsible for controlling the server
    """
    def __init__(self, msgQ):
        """
        Constructor, setting initial variables
        """
        threading.Thread.__init__(self, name="TestThread")
        print("Creating thread")
        self.daemon = True
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        from wsgiref.simple_server import make_server
        blendedRestObj = z25.blendRest.blendedRest(msgQ)
        self.httpd = make_server('', 8000, z25.appie.z25_restMapper(bge.logic.expandPath('//example-webclient'), bge=blendedRestObj))
 
    def run(self):
        """
        overload of threading.thread.run()
        main control loop
        """
        print("Starting ", self.getName())
        print("Serving on port 8000...")

        while not self._stopevent.isSet():
            self.httpd.serve_forever()
            
        # Just force stop to be sure the socket isn't left behind so
        # the program can't finish
        self.forceStop()
        print ("End ", self.getName())

    def join(self, timeout=None):
        """
        Stop the thread
        """
        print("Terminating thread")
        self._stopevent.set()
        self.httpd.shutdown()
        threading.Thread.join(self, timeout)
        print("Thread terminated")
    
    def forceStop(self):
        # this seems a way to destroy the server
        self.httpd.socket.close()

if __name__ == '__main__':
    print("INITIALISING")
    thread = serverThread()
    thread.start()
    print("server running...")
    time.sleep(100)

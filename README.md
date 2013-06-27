z25 Blender HTTP Server
=======================

1 Introduction
--------------

Contemporary models in the Blender Game Engine (BGE) require more and more alternative ways for controlling objects in a scene. Especially in real-time applications the need for remote input devices is rising. The ability to interact by means of smartphones, tablets and even custom made hardware allows live audiences, players and artists to a richer and more responsive interactive experience.

Normally scenes in BGE can only be controlled via the Blender GUI. This is too limiting for today's opportunities and challenges in interactive projects. This was at least the situation for z25. Therefore we set ourselves the task to solve this and share the result in a free and open software project.

To allow for alternative input methods for controlling objects in Blender, z25 has developed an HTTP server with a REST API. This server is automatically aware of all the objects in a given scene by means of introspection. This means that with this webservice it is possible to retrieve information on all objects in a scene and manipulate their characteristics remotely.

The result of this development is this software project which contains a working HTTP server with example Blender scene and web client and documentation which has been used in several real world installations. By sharing this project as free and open source, z25 promotes further use and development of this innovative method for interacting with objects in Blender, any where and any time, enabling tomorrow's experiences.


2 License
---------

This software has the GNU GPLv3. This is the same license as the Blender Game Engine has. Please see the file LICENSE.txt and https://gnu.org/licenses/gpl.html for details.

The example webclient has been build with jQuery and Mobile jQuery. The MIT license included in the directory exmaple-webclient **only** applies to the jQuery libraries. The example web client has the same license as the rest of this project. The same applies for the WebOb Python module that is also included but falls under an MIT license too.


3 Documentation
---------------

Objects in a Blender scene that needs controlling have to have two sensors, each with one controller. The first sensor is connected to a controller which runs a method of a Python module called `threadingController.init` to initialize the threading controller once. A second sensor, which is activated on TRUE level triggering in pulse mode, runs a method of a Python module called `threadingController.processMessage` for handling the messages originating from the client. See connecting-object-to-http-server.png for details

This module is found in `threadingController.py` which uses class `serverThread` from `threadedHttpWsgiServer.py`. Uses the `z25_restMapper` class from `appie.py` to start an HTTP server on port 8000. This server is constructed with an instance of class `blendedRest` from `blendRest.py`. Note that the Blender scene file and these Python files need to be in the same directory.

An HTTP client can communicate to BGE to change a status of a property of an object but it can not read out the status of an object at the moment.


### 3.1 Starting the server ###

An example can be started by loading the example.blend file in Blender:

    blender example-sphere-with-debug-mode.blend

Choose **Start Game Engine** from the **Game** menu. The following will appear on the command line:

    Blender Game Engine Started
    INITIALISING
    Creating thread
    Found object: Cone with property: prop
    Found object: Cone with property: prop0
    Found object: Cone with property: prop1
    Found object: Cone with property: prop2
    Found object: Icosphere with property: init
    Found object: Icosphere with property: slide
    Appie: registering url: /bge
    creating thread_ptr
    Starting  TestThread
    Server running in thread...
    Serving on port 8000...
    
Now open your browser and point it at http://localhost:8000

See enabling-debug-mode-for-object.png on how to enable debugging for an object and debug mode in BGE.

### 3.5 Dependencies ###

This HTTP server runs in the Blender Game Engine (BGE) so it needs at least an installation of Blender and Python3. Also WebOb is needed which is included here. For more information on WebOb and to upgrade, please see https://pypi.python.org/pypi/WebOb/

The appie.py that offers class z25_restMapper is maintained in another repository of z25. Contact z25 for submitting improvements or receiving an updated version.


### 3.6 To do ###

One small improvement that needs to be made is for the next situation. After starting example-sphere-with-debug-mode.blend and running nmap localhost, the following exception is being thrown and reported on the command line:

    ----------------------------------------
    Exception happened during processing of request from ('127.0.0.1', 58523)
    Traceback (most recent call last):
      File "/opt/blender/.../python/lib/python3.3/socketserver.py", line 306, in _handle_request_noblock
        self.process_request(request, client_address)
      File "/opt/blender/.../python/lib/python3.3/socketserver.py", line 332, in process_request
        self.finish_request(request, client_address)
      File "/opt/blender/.../python/lib/python3.3/socketserver.py", line 345, in finish_request
        self.RequestHandlerClass(request, client_address, self)
      File "/opt/blender/.../python/lib/python3.3/socketserver.py", line 666, in __init__
    self.handle()
      File "/opt/blender/.../python/lib/python3.3/wsgiref/simple_server.py", line 118, in handle
        self.raw_requestline = self.rfile.readline()
      File "/opt/blender/.../python/lib/python3.3/socket.py", line 297, in readinto
        return self._sock.recv_into(b)
    ConnectionResetError: [Errno 104] Connection reset by peer
    ----------------------------------------


4 Authors
---------

the following people have contributed to this software:

* Arnaud Loonstra <arnaud@z25.org>
* Roderick Gadellaa <roderick@z25.org>
* Pander <pander@users.sourceforge.net>


5 Contact
---------

n: Stichting z25.org  
e: info@z25.org  
w: http://z25.org  
T: http://twitter.com/z25org  
F: http://fb.com/z25org  
G: http://gplus.to/z25  
L: http://linkedin.com/company/z25  
S: https://github.com/z25/BgeHttpServer  

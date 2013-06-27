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
# This file is maintained in another project of z25.org
# AUTHOR:
# Arnaud Loonstra <arnaud@z25.org>
import os
from json import dumps
from json import loads
from webob import Response, Request, exc, static

class z25_restMapper(object):
    """
    Basic class for providing a RESTful interface to resources.

    To use this class, simply add a class object to the constructor
    and implement the methods you want to support in the class.  
    The list of possible methods are:
    
    handle_GET(*args, **kwargs)
    handle_PUT(*args, **kwargs)
    handle_POST(*args, **kwargs)
    handle_DELETE(*args, **kwargs)
    
    Data is handled through JSON all handle calls must return 
    jsonifiable data (string, dict, list, etc)
    
    GET = Retrieve
    PUT = Replace
    POST = New/Create
    DELETE = d'uh    
    """
    def __init__(self, httpdRoot="./", *args, **kwargs):
        #empty dict of restObjects
        self._restObjects = {}
        self._httpdRoot = httpdRoot 
        for name in kwargs:
            self.registerRestObject(name, kwargs[name])
        
    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response()
        try:
            resp = self._process(req)
        except ValueError as e:
            resp = exc.HTTPBadRequest(str(e))
        except exc.HTTPException as e:
            resp = e
        return resp(environ, start_response)

    def registerRestObject(self, name, obj):
        print('Appie: registering url: /%s' %name)
        self._restObjects.update({name : obj})

    def unRegisterRestObject(self, name):
        print('Appie: unregistering url: /%s' %name)
        try:
            del self._restObjects[name]
        except KeyError as ke:
            print("No such object: %s" %ke)

    def _process(self, req):
        """
        a request URL is parsed as follow
        /object/resource?args
        object is the main python object
        GET /object is mapped to handle_get function(**kwargs)
        GET /object/resource is mapped to handle_get([resource,], **kwargs)
        GET /object/resource/resource2 is mapped to handle_get([resource,resource2], **kwargs)
        args are always passed on through **kwargs
        """
        method = req.method
        object = req.path_info_pop()
        #do some static file serving logic first before trying functions on objects
        if object == None or object == "":
            #the root / is moved to static file serving
            res = exc.HTTPMovedPermanently(location="/static/")
            return res
        elif object == "static":
            # In here we are handling real files so be careful!!!
            if method == "GET":
                # simply serving static files
                #import os
                #print(os.getcwd())
                res = static.DirectoryApp(self._httpdRoot)
                return res
            if method == "POST":
                # uploading new files
                filename = req.path_info_pop()
                filepath = os.path.join(os.path.join(self._httpdRoot, filename))
                # if the file exists we raise an exception
                if filename == "":
                    filename = req.params['file']
                if os.path.exists(filepath):
                    raise exc.HTTPForbidden("%s already exists" %filename)
                #print(dir(req))
                #print(req.body)
                saveFile = open(os.path.join(self._httpdRoot, filename), 'wb')
                saveFile.write(req.body_file.read())
                saveFile.close()                
                return Response("ok")
            if method == "PUT":
                # This will overwrite your files
                # uploading files to update
                filename = req.path_info_pop()
                filepath = os.path.join(os.path.join(self._httpdRoot, filename))
                # if the file exists we raise an exception
                if not os.path.exists(filepath):
                    raise exc.HTTPNotFound("%s file not found" %filename)
                if filename == "":
                    filename = req.params['file']
                #print(dir(req))
                #print(req.body)
                saveFile = open(os.path.join(self._httpdRoot, filename), 'wb')
                saveFile.write(req.body_file.read())
                saveFile.close()                
                return Response("ok")
                        
        #################################################
        #
        # After this we only handle JSON type content!!!!
        #
        #################################################
        
        #Find the object
        obj = None
        try:
            obj = self._restObjects[object]
        except:
            #print(self._restObjects)
            #print(dir(self._restObjects))
            raise exc.HTTPNotFound('No such resource: %s' %object)
        
        #Find the function
        func = None
        try:
            func = getattr(obj, 'handle_'+method)
        except:
            raise exc.HTTPNotFound('No %s method on resource: %s' %(method,object))        
        
        # Find resources: 
        resources = []
        # get first resource
        res = req.path_info_pop()
        while res: 
            resources.append(res)
            # get next resource
            res = req.path_info_pop()
        
        #optional extra headers
        #FIXME: this shouldn't be hardcoded. The appie modules should take care of this
        #http://www.w3.org/TR/cors/#syntax
        extraHeaderList = [
                   ('Access-Control-Allow-Origin', '*'),
                   ('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS'),
                   ('Access-Control-Max-Age', '86400'),
                   ('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')
                    ]
        #Get args
        kwargs = req.GET
        if (method == 'POST'):
            #curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d 
            #curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"test" : "help" }' http://localhost:8000/bge/IcoSphere
            if req.content_type == 'application/json':
                encoding = req.charset
                body = req.body.decode(encoding)
                data = loads(body)
                #print(data)
                #print(type(data))
                kwargs = data
            else:
                kwargs = req.POST
        try:
            result = func(*resources, **kwargs)
        except:
            raise exc.HTTPInternalServerError("Appie raised an exception while calling the method with %s %s" %(str(resources), str(kwargs)))
        resp = Response(
            content_type='application/json',
            charset = 'utf8',
            body=dumps(result))
        resp.headerlist.extend(extraHeaderList)
        return resp 

#Damned wsgi, we need to specify the path to the modules!
#import sys
#sys.path.append('/home/z25/www/webappie')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, z25_restMapper())
    print("Serving on port 8000...")
 
    # Serve until process is killed
    httpd.serve_forever()

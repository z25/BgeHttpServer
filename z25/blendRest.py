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

import bge

class blendedRest(object):
    """
    simple wrapper for inclusion in Appie so we have handle_GET methods etc
    """
    def __init__(self, blenderMsgQ, propertyPrepend='', *args, **kwargs):
        self._blenderMsgQ = blenderMsgQ
        self._propertyPrepend = propertyPrepend
        self._restedGameObjects = self.getRestedGameobjects()
        
    def getRestedGameobjects(self):
        """
        return game objects with properties starting with 'w_'
        """
        restObjs = {}
        for obj in bge.logic.getCurrentScene().objects:
            properties = {}
            for propertyNames in obj.getPropertyNames():
                if propertyNames.startswith(self._propertyPrepend) and type(obj[propertyNames]) in (int, float, bool, str):
                        print("Found object: %s with propertyNames: %s" %(obj.name, propertyNames))
                        properties.update({propertyNames : obj[propertyNames] })
            restObjs.update({obj.name : properties})
        return restObjs

    def sendToBlender(self, msgDict):
        print("sending to Blender: %s" %msgDict) 
        self._blenderMsgQ.put(msgDict)

    def handle_GET(self, *args, **kwargs):
        """
        return all or requested attributes
        """
        if len(args)<1:
            print(self._restedGameObjects)
            return self._restedGameObjects
        ret = {}
        for arg in args:
            try:
                ret.update({arg : self._restedGameObjects[arg] })
            except:
                print('Error getting argument: %s' %arg)
        return ret

    def handle_PUT(self, *args, **kwargs):
        """
        CREATE, not used currently
        """
        return True

    def handle_POST(self, *args, **kwargs):
        """
        UPDATE/REPLACE
        This basically only works one argument at a time however if args contains more than one entry
        all entry will receive the kwargs
        """
        for arg in args:
            self.sendToBlender({arg: kwargs})
        return {arg : "parsed"}

 


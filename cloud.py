from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
import direct.directbase.DirectStart
import random

class World(DirectObject):
    def __init__(self):    
        
        self.cloud_root=render.attachNewNode('cloudRoot')
        cloud_lod = FadeLODNode('cloud_lod')
        cloud = NodePath(cloud_lod)
        lod0 = loader.loadModel("cloud")
        lod0.reparentTo(cloud)
        cloud_lod.addSwitch(590, 0)
        shader = loader.loadShader("clouds.cg")
        cloud_lod.setFadeTime(10.0)
        self.sky=loader.loadModel("sky")
        self.sky.reparentTo(self.cloud_root)
        self.sky.setBin('background', 1)
        self.sky.setDepthWrite(0)
        self.sky.setLightOff()
        self.sky.setScale(100)
        
        #config here!            
        self.cloud_x=1200
        self.cloud_y=1200
        self.cloud_z=20        
        self.cloud_speed=0.3
        cloud_size=5
        cloud_count=50
        self.clouds=[]
        
        for i in range(cloud_count):
            self.clouds.append(cloud.copyTo(self.cloud_root))    
            self.clouds[-1].setPos(render,random.randrange(-self.cloud_x/2, self.cloud_x/2),random.randrange(-self.cloud_y/2,self.cloud_y/2), random.randrange(self.cloud_z)+self.cloud_z)
            self.clouds[-1].setScale(cloud_size+random.random(),cloud_size+random.random(),cloud_size+random.random())
            self.clouds[-1].setShaderInput("offset", Vec4(random.randrange(5)*0.25, random.randrange(9)*0.125, 0, 0))
            self.clouds[-1].setShader(shader)
            self.clouds[-1].setBillboardPointEye()
        
        
        self.time=0
        self.uv=Vec4(0, 0, 0.25, 0)        
        render.setShaderInput("time", self.time)
        render.setShaderInput("uv", self.uv)
        taskMgr.add(self.update,"updateTask")
        
    def update(self, task): 
        self.cloud_root.setPos(base.camera.getPos(render))   
        elapsed = task.time*self.cloud_speed
        for model in self.clouds:
            model.setY(model, -task.time)
            if model.getY(self.cloud_root) <-self.cloud_y/2:
                model.setY(self.cloud_root,self.cloud_y/2)
        self.time+=elapsed
        if self.time>1.0:
            self.cloud_speed*=-1.0
            self.uv[0]+=0.5
            if self.uv[0]>1.0:
                self.uv[0]=0
                self.uv[1]+=0.125
                if self.uv[1]>1.0:
                    self.uv=Vec4(0, 0, 0.25, 0)
        if self.time<0.0:
            self.cloud_speed*=-1.0
            self.uv[2]+=0.5
            if self.uv[2]>1.0:
                self.uv[2]=0.25
                self.uv[3]+=0.125
                if self.uv[3]>1.0:
                    self.uv=Vec4(0, 0, 0.25, 0)
        render.setShaderInput("time", self.time)
        render.setShaderInput("uv", self.uv)     
        return task.again
        
w = World()
run()         
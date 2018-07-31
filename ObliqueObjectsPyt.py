#
#
class ObliqueObjects:
    def __init__(self,nObjects):
        # nObjects: is the total number of the Oblique Objects in the computational domain
        self.lu=array('d',[0.e0 for x in range(nObjects)])
        self.lv=array('d',[0.e0 for x in range(nObjects)])
        self.lw=array('d',[0.e0 for x in range(nObjects)])
        # Construct 2D Arrays
        self.u_axis=array('d',[0.e0 for x in range(nObjects*3)])
        self.u_axis=reshape(self.u_axis,(nObjects,3))
        self.v_axis=array('d',[0.e0 for x in range(nObjects*3)])
        self.v_axis=reshape(self.v_axis,(nObjects,3))
        self.w_axis=array('d',[0.e0 for x in range(nObjects*3)])
        self.w_axis=reshape(self.w_axis,(nObjects,3))
        self.xyz0Corner=array('d',[0.e0 for x in range(nObjects*3)])
        self.xyz0Corner=reshape(self.xyz0Corner,(nObjects,3))
        # Construct and initialize the 3D dynamic Array "Object_range"
        self.Object_range=array('i', [0 for x in range(nObjects*3*6)])
        self.Object_range=reshape(self.Object_range,(nObjects,3,6))
    def ReadObjectInfoaAndFindMinMax(self,nn,x0,y0,z0,luu,lvv,lww,i_dir,MyU_axis,MyV_axis,MyW_axis):
        #In this function the solver use the information that were passed from GUI about the rectangular oblique objects to find Xmin,Xmax,Ymin,Ymax,Zmin
	#As special cases the rectangular object may be a 2D (rectangle) if lu or lv=0 or a 1D (straight line) if lu=lv=0.
	#W-direction is the Longitudinal direction
	#This function will calculate finally in the Cartesian coordinate Xmin,Xmax,Ymin,Ymax,Zmin,Zmax
	#to be used in the Cartesian grid for the solver
        
        xyz1Corner=array('d',[0.e0 for x in range(3)])
        xyz2Corner=array('d',[0.e0 for x in range(3)])
        xyz3Corner=array('d',[0.e0 for x in range(3)])
        xyz4Corner=array('d',[0.e0 for x in range(3)])
        xyz5Corner=array('d',[0.e0 for x in range(3)])
        xyz6Corner=array('d',[0.e0 for x in range(3)])
        xyz7Corner=array('d',[0.e0 for x in range(3)])
        for i in range(3):
            self.u_axis[nn][i]=MyU_axis[i]
            self.v_axis[nn][i]=MyV_axis[i]
            self.w_axis[nn][i]=MyW_axis[i]
        self.xyz0Corner[nn][0]=x0
        self.xyz0Corner[nn][1]=y0
        self.xyz0Corner[nn][2]=z0
        self.lu[nn]=luu
        self.lv[nn] = lvv
        self.lw[nn] = lww
        self.findCornersObliqueRectangular(nn,x0,y0,z0,luu,lvv,lww,xyz1Corner,xyz2Corner,xyz3Corner,xyz4Corner,xyz5Corner,xyz6Corner,xyz7Corner)
        xmin,xmax,ymin,ymax,zmin,zmax=self.xyzMinMaxRectangular(nn,xyz1Corner,xyz2Corner,xyz3Corner,xyz4Corner,xyz5Corner,xyz6Corner,xyz7Corner)
        print('output of xyzMinMaxRectangular',xmin,xmax,ymin,ymax,zmin,zmax)
        return xmin,xmax,ymin,ymax,zmin,zmax
        
    
    def findCornersObliqueRectangular(self,nn,x0,y0,z0,lu,lv,lw,xyz1Corner,xyz2Corner,xyz3Corner,xyz4Corner,xyz5Corner,xyz6Corner,xyz7Corner):
        #This function finds 7 corners of the rectangular object while the first corner xyz0Corner is already given
        xyz1Corner[0]=x0+lu*self.u_axis[nn][0]
        xyz1Corner[1]=y0+lu*self.u_axis[nn][1]
        xyz1Corner[2]=z0+lu*self.u_axis[nn][2]
        xyz2Corner[0]=x0+lv*self.v_axis[nn][0]
        xyz2Corner[1]=y0+lv*self.v_axis[nn][1]
        xyz2Corner[2]=z0+lv*self.v_axis[nn][2]
        xyz3Corner[0]=x0+lw*self.w_axis[nn][0]
        xyz3Corner[1]=y0+lw*self.w_axis[nn][1]
        xyz3Corner[2]=z0+lw*self.w_axis[nn][2]
        xyz4Corner[0]=x0+lu*self.u_axis[nn][0]+lv*self.v_axis[nn][0]
        xyz4Corner[1]=y0+lu*self.u_axis[nn][1]+lv*self.v_axis[nn][1]
        xyz4Corner[2]=z0+lu*self.u_axis[nn][2]+lv*self.v_axis[nn][2]
        xyz5Corner[0]=x0+lv*self.v_axis[nn][0]+lw*self.w_axis[nn][0]
        xyz5Corner[1]=y0+lv*self.v_axis[nn][1]+lw*self.w_axis[nn][1]
        xyz5Corner[2]=z0+lv*self.v_axis[nn][2]+lw*self.w_axis[nn][2]
        xyz6Corner[0]=x0+lu*self.u_axis[nn][0]+lw*self.w_axis[nn][0]
        xyz6Corner[1]=y0+lu*self.u_axis[nn][1]+lw*self.w_axis[nn][1]
        xyz6Corner[2]=z0+lu*self.u_axis[nn][2]+lw*self.w_axis[nn][2]
        xyz7Corner[0]=x0+lu*self.u_axis[nn][0]+lv*self.v_axis[nn][0]+lw*self.w_axis[nn][0]
        xyz7Corner[1]=y0+lu*self.u_axis[nn][1]+lv*self.v_axis[nn][1]+lw*self.w_axis[nn][1]
        xyz7Corner[2]=z0+lu*self.u_axis[nn][2]+lv*self.v_axis[nn][2]+lw*self.w_axis[nn][2]

    def xyzMinMaxRectangular(self,nn,xyz1Corner,xyz2Corner,xyz3Corner,xyz4Corner,xyz5Corner,xyz6Corner,xyz7Corner):
        # Find Xmin,Xmax,Ymin,Ymax,Zmin,Zmax of the oblique rectangular object.
        uFindMinMax=array('d',[0.e0 for x in range(8)])
        uFindMinMax[0]= self.xyz0Corner[nn][0]; uFindMinMax[1]=xyz1Corner[0]; uFindMinMax[2]=xyz2Corner[0]
        uFindMinMax[3]=xyz3Corner[0]; uFindMinMax[4]=xyz4Corner[0]
        uFindMinMax[5]=xyz5Corner[0]
        uFindMinMax[6]=xyz6Corner[0]
        uFindMinMax[7]=xyz7Corner[0]
        xmin=0.0;xmax=0.0
        xmin=minOfArray(uFindMinMax)
        xmax=maxOfArray(uFindMinMax)
        uFindMinMax[0]= self.xyz0Corner[nn][1];uFindMinMax[1]=xyz1Corner[1];uFindMinMax[2]=xyz2Corner[1]
        uFindMinMax[3]=xyz3Corner[1];uFindMinMax[4]=xyz4Corner[1]; uFindMinMax[5]=xyz5Corner[1]
        uFindMinMax[6]=xyz6Corner[1];uFindMinMax[7]=xyz7Corner[1]
        ymin=minOfArray(uFindMinMax)
        ymax=maxOfArray(uFindMinMax)
        uFindMinMax[0]= self.xyz0Corner[nn][2];uFindMinMax[1]=xyz1Corner[2];uFindMinMax[2]=xyz2Corner[2]
        uFindMinMax[3]=xyz3Corner[2];uFindMinMax[4]=xyz4Corner[2]; uFindMinMax[5]=xyz5Corner[2]
        uFindMinMax[6]=xyz6Corner[2];uFindMinMax[7]=xyz7Corner[2]
        zmin=minOfArray(uFindMinMax)
        zmax=maxOfArray(uFindMinMax)
        print('Inside xyzMinMaxRectangular',xmin,xmax,ymin,ymax,zmin,zmax)
        return xmin,xmax,ymin,ymax,zmin,zmax
        
    def checkIfPointInObliqueRectangular(self,x,y,z,x0,y0,z0,u_length,v_length,w_length,isit_in,nn):
        # This function to check if the point (x,y,z) is inside the oblique rectangular object or outside.
        isit_in = False
        u=(x-x0)*self.u_axis[nn][0] +(y-y0) * self.u_axis[nn][1] +(z-z0) * self.u_axis[nn][2]
        v=(x-x0)*self.v_axis[nn][0] +(y-y0) * self.v_axis[nn][1] +(z-z0) * self.v_axis[nn][2]
        w=(x-x0)*self.w_axis[nn][0] +(y-y0) * self.w_axis[nn][1] +(z-z0) * self.w_axis[nn][2]
        if(( u >=0. and u<=u_length) and ( v>=0. and v<=v_length) and( w>=0. and w<=w_length)):
           isit_in= True

def minOfArray(x):
    xmin=1.0e34
    for i in range(8):
        if(x[i]<xmin):
            xmin=x[i]
    return xmin

def maxOfArray(x):
    xmax=-1.e34
    for i in range(8):
        if(x[i]>xmax):
            xmax=x[i]
    return xmax

def constructSimpleMesh():
    nx=100
    for i in range(nx):
        dx[i]=0.1
        for i in range(nx):
            xMesh[i]=i*dx[i];yMesh[i]=i*dx[i];zMesh[i]=i*dx[i]
def  testPoints():
    # This subroutine is used to test points from the mesh
    isit_in=False
    for nn in range(ne_oblique):
        for i in range(Object1.Object_range[nn][2][0],Object1.Object_range[nn][2][1]+1):
            for j in range(Object1.Object_range[nn][2][2],Object1.Object_range[nn][2][3]+1):
                for k in range(Object1.Object_range[nn][2][4],Object1.Object_range[nn][2][5]+1):
                    xi=xMesh[i]+dx[i]/2.; yj=yMesh[j];zk=zMesh[k]
                    x0=Object1.xyz0Corner[nn][0];y0=Object1.xyz0Corner[nn][1];z0=Object1.xyz0Corner[nn][2]
                    lu=Object1.lu[nn];lv=Object1.lv[nn];lw=Object1.lw[nn]
                    Object1.checkIfPointInObliqueRectangular(xi,yj,zk,x0,y0,z0,lu,lv,lw,isit_in,nn)
                    if(isit_in == True):
                        print("xi= ",xi,"yj= ",yj,"zk= ",zk)
from numpy import *
from array import *
ne_oblique=1
xMesh=array('d',[0.e0 for x in range(100)])
yMesh=array('d',[0.e0 for x in range(100)])
zMesh=array('d',[0.e0 for x in range(100)])
dx=array('d',[0.e0 for x in range(100)])
Object1=ObliqueObjects(ne_oblique)
constructSimpleMesh()
x0=5.0; y0=5.; z0=4.; lu=1.;lv=1.;lw=2.
a1_axis=array('d',[0.e0 for x in range(3)])
a2_axis=array('d',[0.e0 for x in range(3)])
a3_axis=array('d',[0.e0 for x in range(3)])
a1_axis[0]=0.;a1_axis[1]=0.;a1_axis[2]=1.0
a2_axis[0]=1.0;a2_axis[1]=0.0;a2_axis[2]=0.0
a3_axis[0]=0.0;a3_axis[1]=1.0;a3_axis[2]=0.0
idir=3; nn=0
xmin=0.;xmax=0.;ymin=0.;ymax=0.;zmin=0.;zmax=0.0

xmin,xmax,ymin,ymax,zmin,zmax=Object1.ReadObjectInfoaAndFindMinMax(nn,x0,y0,z0,lu,lv,lw,idir,a1_axis,a2_axis,a3_axis)
print('Xmin=',xmin,'Xmax=',xmax,'Ymin=',ymin,'Ymax=',ymax,'Zmin=',zmin,'Zmax=',zmax)
Object1.Object_range[nn][2][0]=int(xmin/dx[0]);Object1.Object_range[nn][2][1]=int(xmax/dx[0])
Object1.Object_range[nn][2][2]=int(ymin/dx[0]);Object1.Object_range[nn][2][3]=int(ymax/dx[0])
Object1.Object_range[nn][2][4]=int(zmin/dx[0]);Object1.Object_range[nn][2][5]=int(zmax/dx[0])
print("dx[0]=",dx[0])
print("I_Xmin= ",Object1.Object_range[nn][2][0],"I_Xmax= ",Object1.Object_range[nn][2][1])
print("J_Ymin= ",Object1.Object_range[nn][2][2],"J_Ymax= ",Object1.Object_range[nn][2][3])
print("K_Zmin= ",Object1.Object_range[nn][2][4],"K_Zmax= ",Object1.Object_range[nn][2][5])
testPoints()

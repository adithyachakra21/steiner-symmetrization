# -*- coding: utf-8 -*-
"""

Created on Mon Jul 22 14:46:28 2019

@author: Owner
"""

import math
from sympy import Point, Polygon, Line, convex_hull, Point2D, RegularPolygon
from sympy import symbols
from sympy.plotting import plot
import random

from sympy import *
from sympy.geometry import *

import numpy as np

pi = math.pi

#input: a list of vertices of a 2-D convex polygon and an angle in RADIANS.
#output: the vertices of the polygon symmetrized in that angle (angle is the "one symmetral line only" - direction)

def symmetrize (poly, angle):
    
    #step 1: rotate the polygon
    rotated_poly = rotate1 (poly.vertices, angle)
     
    #step 2: add in all the intersection points
    full_poly = vertical (rotated_poly)
    
    #step 3: sort the points by x-coordinate and pair together opposite points.
    
    sorted_new_poly_vertices = bubbleSort (full_poly)
    pairedsorted_newpolyvertices = pairing (sorted_new_poly_vertices)
    
    #step 4: average the y-coordinates of the opposite points while keeping x-coords the same.
 
    for pair in pairedsorted_newpolyvertices:
        if len (pair)==2:
            item0 = pair [0]
            item1 = pair [1]
            
            item0new = Point (item0[0], 0.5*(abs(item0[1]) + abs(item1[1])))
            item1new = Point (item0[0], -1*(0.5*(abs(item0[1]) + abs(item1[1]))))
            
            pair[0] = item0new
            pair[1] = item1new
        
        else:
            pair[0] = Point (pair[0][0], 0)
            
    
    #Step 5: make the pairs of points into a list of points for convenience
    output = []
    for item in pairedsorted_newpolyvertices:
        output += item
        
            
    #Step 6: Rotating it back to original position.
    output3 = rotate1 (output, 2*pi - angle)     
        
    
        
    
    
    outpoly = convex_hull(*output3)
    outpolyvert = outpoly.vertices
    
    #Step 7: Putting it into Sage format for ease of copy/paste
    
    output2 = []
    for thing in outpolyvert:
        output2 += [[thing[0],thing[1]]]
        
    output4 = output2
   
    
    #Step 8: (optional) removing points that are too close (distance < 1)
    """
    if len(output2)>30:
        output4 = []
        for i in range (0,len(output2)):
            
            print (i)
            if distance (output2[i-1],output2[i]) < 0.1:
                continue
            else:
                output4 += [output2[i]]
            
     """   
        
    
    
    
    return output4


# optional: this function removes points that are more than 0.15 close together to improve speed
def reduce (vert_list):
    a = convex_hull(*vert_list)

    output2=[]
    avert = a.vertices

    for thing in avert:
        output2 += [[thing[0],thing[1]]]
        

    output4 = []
    for i in range (0,len(output2)):
    
            
        if distance (output2[i-1],output2[i]) < 0.15:
            continue
        else:
            output4 += [output2[i]]
        
    return output4



#given a polygon, it rotates the vertices backward so that you can now use x-axis as your symmetral!

def rotate1 (vert_list, angle):
    neg_angle = 2*pi - angle
    vert_listcopy = []
    
    
    for point in vert_list:
        
        vert_listcopy += [point.rotate (neg_angle)]
     
    return vert_listcopy


#sorts the vertices in order of increasing x-coordinates
def bubbleSort (vert_list):
    for i in range (0, len(vert_list)):
        for j in range (0,len(vert_list)-i-1):
            if vert_list [j][0]> vert_list [j+1][0]:
                temp = vert_list [j+1]
                vert_list [j+1] = vert_list [j]
                vert_list [j] = temp
                
    return vert_list


#if there are any two vertices with same x-coordinates, they are paired up.  
def pairing (new_list):
     
    pairs = []
    for i in range (0,len(new_list)-1):
        for j in range (i+1,len(new_list)):
            if new_list[i][0]==new_list[j][0]:
                if i!=j:
                    if [new_list[i], new_list[j]] not in pairs:
                        pairs += [[new_list[i], new_list[j]]]
                        
    check_list = []
    for element in pairs:
        check_list += element
    
    for thing in new_list:
        if thing not in check_list:
            pairs += [[thing]]
     
      
    return pairs


# This returns a list of vertices AND intersections for the polygon about to be symmetrized. Note: order of vertices matters! Must be in the cyclic order.
def vertical (poly_vertices):
     
    new_polyvertices = poly_vertices
    
    for element in poly_vertices:
        line = Line ((element), (element[0], element[1]+1))
        
        poly = convex_hull (*poly_vertices)
        inters = poly.intersection (line)
        
        for point in inters:
            
            if type(point)==Segment2D:
                continue
            if point not in new_polyvertices:
                new_polyvertices += [point]
    
    return new_polyvertices




"""

#Example of how to plug into vertical           
poly = RegularPolygon ((0,2),1.1,3) 
print (symmetrize (poly,0))  



#Example of how to plug into pairing
x= pairing ([[-4,0],[-2,5],[3,-3],[5,3],[0,6],[-2,3],[3,21/5],[0,-21/5]])

print (final(x))
"""
    


#poly = Polygon( (71,-71),(-71,-71),(-71,71),(71,71))

def norm(vector):
    total = 0
    for i in vector:
        total += i*i
    return np.sqrt(float(total))

def moment_of_inertia_wrong (poly):
    
    num = 0
    denom = 0
    
    vertices = poly.vertices + [poly.vertices [0]]
    
    for i in range (0, len(poly.vertices)):
        
        num += ((np.cross(vertices[i+1],vertices[i])))*( np.dot (vertices [i],vertices[i]) + np.dot(vertices[i],vertices[i+1]) + np.dot (vertices[i+1],vertices[i+1]))

        denom +=  (np.cross(vertices[i+1],vertices[i]))
        
    return num/(6*denom)


def moment_of_inertia (poly):
    
    total = 0
    
    vertices = poly.vertices + [poly.vertices [0]]
    
    for i in range (0, len(poly.vertices)):
        
        total += ( (vertices[i][0] * vertices[i+1][1]) - (vertices[i+1][0] * vertices[i][1])) * ( (vertices[i][0] * vertices[i][0] ) + (vertices[i][0] * vertices[i+1][0] ) + (vertices[i+1][0] * vertices[i+1][0]) + (vertices[i][1] * vertices[i][1] ) + (vertices[i][1] * vertices[i+1][1] ) + (vertices[i+1][1] * vertices[i+1][1]))
        
    return total/12


def distance (a,b):
    return (math.sqrt(((a[0]-b[0])*(a[0]-b[0])) + ((a[1]-b[1])*(a[1]-b[1]))))


"""

def distance (a,b):
    print (math.sqrt(((a[0]-b[0])*(a[0]-b[0])) + ((a[1]-b[1])*(a[1]-b[1]))))

a = [[2,-3],[-2,-3],[2,3],[-2,3]]
for i in range (-1,len(a)-1):
    print (distance(a[i],a[i+1])



print (float(moment_of_inertia (poly)))
angle =0.86678392 + 0.5 + 0.5*random.random()

if angle>=2:
    angle -= 2
    
sym = symmetrize (poly, (angle)*pi)
print ("vertices of sym: " + str(sym))
print ("angle: " + str(angle))
    
sym_poly = convex_hull(*sym)
sidelist = []
for side in sym_poly.sides:
    sidelist += [float(side.length)]
            
print("side lengths: " + str(sidelist))
#print("sl std: " + str(statistics.stdev(sidelist)))
   
#print("sl average: " + str(statistics.mean(sidelist)))
print ("moment of inertia: " + str(float((moment_of_inertia(sym_poly)))))
 

anglelist = []
for point in sym_poly.vertices:
    anglelist += [float(sym_poly.angles[point])]
    
print("angle lengths: " + str(anglelist))




out = []
poly = Polygon ((0,0),100,n=3)
for e in poly.vertices:
    out += [[float(e[0]),float(e[1])]]
    
out =  [[0,20],[0,-20],[7,0],[-7,0]]
poly = convex_hull (*out)

poly = Polygon ((0,20),(7,0),(0,-20),(-7,0))


print (moment_of_inertia (poly))
print (out)

print ((708404680768083/10000000000000)/(429756492218191/10000000000000) )
print ((281715139471567/10000000000000)/(24604408437471/312500000000 ))

print (float(sqrt(2)))

 

print("18 gon")

poly = Polygon ((17,-98),(-17,-98),(-50,-87),(-77,-64),(-94,-34),(-100,0),(-94,34),(-77,64),(-50,87),(-17,98),(17,98),(50,87),(77,64),(94,34),(100,0),(94,-34),(77,-64),(50,-87))

print(moment_of_inertia(poly))



print(0.5*100*100*(1-(2/3)*math.sin(math.pi/18)*math.sin(math.pi/18)))

print("10 gon")

poly2 = Polygon((31,-95),(-31,-95),(-81,-59),(-100,0),(-81,59),(-31,95),(31,95),(81,59),(100,0),(81,-59))

print(moment_of_inertia(poly2))

print(0.5*100*100*(1-(2/3)*math.sin(math.pi/10)*math.sin(math.pi/10)))

print("6 gon")

poly3 = Polygon ((50,-87),(-50,-87),(-100,0),(-50,87),(50,87),(100,0))

print(moment_of_inertia(poly3))

print(0.5*100*100*(1-(2/3)*math.sin(math.pi/6)*math.sin(math.pi/6)))

print("4 gon")

poly4 = Polygon((71,-71),(-71,-71),(-71,71),(71,71))

print(moment_of_inertia(poly4))

print(0.5*100*100*(1-(2/3)*math.sin(math.pi/4)*math.sin(math.pi/4)))

print("regular polygon:")

a = [4,6,10,18]
for element in a:
    p = Polygon ((0,0),100,n=element)
    print(float(moment_of_inertia(p)))



vertex = [[44,-76],[-44,-76],[-88,0],[-44,76],[44,76],[88,0]]
poly = convex_hull(*vertex)
print (moment_of_inertia(poly))


square
71,-71
-71,-71
-71,71
71,71

hexagon
50,-87
-50,-87
-100,0
-50,87
50,87
100,0

decagon
31,-95
-31,-95
-81,-59
-100,0
-81,59
-31,95
31,95
81,59
100,0
81,-59

18-gon
17,-98
-17,-98
-50,-87
-77,-64
-94,-34
-100,0
-94,34
-77,64
-50,87
-17,98
17,98
50,87
77,64
94,34
100,0
94,-34
77,-64
50,-87

34-gon

9,-100
-9,-100
-27,-96
-45,-90
-60,-80
-74,-67
-85,-53
-93,-36
-98,-18
-100,0
-98,18
-93,36
-85,53
-74,67
-60,80
-45,90
-27,96
-9,100
9,100
27,96
45,90
60,80
74,67
85,53
93,36
98,18
100,0
98,-18
93,-36
85,-53
74,-67
60,-80
45,-90
27,-96
"""









 
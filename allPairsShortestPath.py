# author: Jae Hyun Park SID: 861277613
import argparse
import os
import re
import sys
import time

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')



graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")



vertices=[]
edges=[]



def BellmanFord(G):
    
    pathPairs=[]
    
    # TODO: Fill in your Bellman-Ford algorithm here
    
    distance = []
    
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            for k in range(len(vertices)):
                distance.append(float("inf"))
            distance[i] = 0
            for x in range(len(vertices)):
                for y in range(len(vertices)):
                    for z in range(len(vertices)):
                        if float(distance[y]) + float(edges[y][z]) < float(distance[z]):
                            distance[z] = float(distance[y]) + float(edges[y][z])
                            
            pathPairs.append(((i, j), float(distance[j])))
            
    print(pathPairs)
        
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs



def FloydWarshall(G):
    
    pathPairs=[]
    
    # TODO: Fill in your Floyd-Warshall algorithm here
    
    for i in range(len(vertices)):
        edges[i][i] = 0
    for j in range(len(vertices)):
        for k in range(len(vertices)):
            for l in range(len(vertices)):
                if float(edges[k][j]) == float("inf") or float(edges[l][j]) == float("inf"):
                    continue
                if float(edges[k][l]) > float(edges[k][j]) + float(edges[j][l]): 
                    edges[k][l] = float(edges[k][j]) + float(edges[j][l])
    for m in range(len(vertices)):
        for n in range(len(vertices)):
            pathPairs.append(((m,n), edges[m][n]))  
            
    print(pathPairs)
    
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs



def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    G = (vertices,edges)
    return (vertices,edges)



def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True



def main(filename,algorithm):
    start_time = time.time()
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        # TODO: Insert timing code here
        pathPairs = BellmanFord(G)
        print("Time: %s seconds" % (time.time() - start_time))
    if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        pathPairs = FloydWarshall(G)
        print("Time: %s seconds" % (time.time() - start_time))
    if algorithm == 'a':
        print('running both') 
        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)
        pathPairs = pathPairsBellman
        if matrixEquality(pathPairsBellman,pathPairsFloyd):
            print('Floyd-Warshall and Bellman-Ford did not produce the same result')
    with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
        for row in pathPairs:
            for weight in row:
                f.write(str(weight)+' ')
            f.write('\n')



if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
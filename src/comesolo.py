import urllib.request
import importlib.util
import numpy as np
import pandas as pd
import time

url = "https://raw.githubusercontent.com/aleoropgal/bailecomesolo/master/src/SimpleSearch.py"

urllib.request.urlretrieve(url, "SimpleSearch.py")

import SimpleSearch as sp

#Definir el estado inicial
start=sp.node(((0,),(1,1),(1,1,1),(1,1,1,1),(1,1,1,1,1)), depth=0, parent=None)

# Definir una funcion sucesor
def sucesorCS(nodo):
    S=[]
    st, n=nodo.state, len(nodo.state)
    for i in range(n):
      for j in range(i+1):
        if st[i][j]==0:

          if j>=2 and st[i][j-1]==1 and st[i][j-2]==1:
            izquierda=[list(row) for row in st] #LISTO
            izquierda[i][j-1]=0
            izquierda[i][j-2]=0
            izquierda[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in izquierda), depth=nodo.depth+1, parent=nodo))

          if j<=2 and i-2>=j and st[i][j+1]==1 and st[i][j+2]==1:
            derecha=[list(row) for row in st] #LISTO
            derecha[i][j+1]=0
            derecha[i][j+2]=0
            derecha[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in derecha), depth=nodo.depth+1, parent=nodo))

          if i>=2 and j>=2 and st[i-1][j-1]==1 and st[i-2][j-2]==1:
            izqsup=[list(row) for row in st]
            izqsup[i-1][j-1]=0
            izqsup[i-2][j-2]=0
            izqsup[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in izqsup), depth=nodo.depth+1, parent=nodo))

          if i>=2 and i-2>=j and st[i-1][j]==1 and st[i-2][j]==1:
            dersup=[list(row) for row in st]
            dersup[i-1][j]=0
            dersup[i-2][j]=0
            dersup[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in dersup), depth=nodo.depth+1, parent=nodo))

          if i<=n-3 and st[i+1][j]==1 and st[i+2][j]==1:
            izqinf=[list(row) for row in st]
            izqinf[i+1][j]=0
            izqinf[i+2][j]=0
            izqinf[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in izqinf), depth=nodo.depth+1, parent=nodo))

          if i<=n-3 and j<=2 and st[i+1][j+1]==1 and st[i+2][j+2]==1:
            derinf=[list(row) for row in st]
            derinf[i+1][j+1]=0
            derinf[i+2][j+2]=0
            derinf[i][j]=1
            S.append(sp.node(tuple(tuple(row) for row in derinf), depth=nodo.depth+1, parent=nodo))

    return S

#sucesorCS(start)

# Definir una meta
def contar_fichas(*nodos):
    nodo=nodos[0]
    tb=nodo.state
    n=len(tb)
    fichas=0
    for i in range(n):
        for j in range(i+1):
            if tb[i][j]==1:
                fichas+=1
    return fichas

def meta(*nodos):
    st=nodos[0]
    return contar_fichas(st)==1

def heuristica(*nodos):
    nodo = nodos[0]
    return contar_fichas(nodo) - 1

def hcero(*nodos):
    nodo = nodos[0]
    return 0

bfs=sp.TreeSearch(start, sucesorCS, meta, strategy="bfs")
dfs=sp.TreeSearch(start, sucesorCS, meta, strategy="dfs")
bas0=sp.TreeSearch(start, sucesorCS, meta, strategy="a*", heuristic=hcero)
bas=sp.TreeSearch(start, sucesorCS, meta, strategy="a*", heuristic=heuristica)

r1=bfs.find()
r2=dfs.find()
r3=bas0.find()
r4=bas.find()

resultados=pd.DataFrame({"Busqueda":["BFS", "DFS", "A*(h=0)", "A*(h(n))"],
                         "Iteraciones":[bfs.iterations, dfs.iterations, bas0.iterations, bas.iterations] })

print(resultados)


#Protocolo Experimental
#INSTANCIA FÁCIL
startf=sp.node(((1,),(0,1),(1,1,1),(1,1,1,1)), depth=0, parent=None)

fbfs=sp.TreeSearch(startf, sucesorCS, meta, strategy="bfs")
fdfs=sp.TreeSearch(startf, sucesorCS, meta, strategy="dfs")
fbas0=sp.TreeSearch(startf, sucesorCS, meta, strategy="a*", heuristic=hcero)
fbas=sp.TreeSearch(startf, sucesorCS, meta, strategy="a*", heuristic=heuristica)

t1=time.time()
fr1=fbfs.find(max_iter=5000)
fn1=fbfs.iterations
ft1=time.time()-t1

t2=time.time()
fr2=fdfs.find(max_iter=5000)
fn2=fdfs.iterations
ft2=time.time()-t2

t3=time.time()
fr3=fbas0.find(max_iter=5000)
fn3=fbas0.iterations
ft3=time.time()-t3

t4=time.time()
fr4=fbas.find(max_iter=5000)
fn4=fbas.iterations
ft4=time.time()-t4

#INSTANCIA MEDIA
startm=sp.node(((1,),(1,1),(1,1,1),(1,1,0,1),(1,1,1,1,1)), depth=0, parent=None)

mbfs=sp.TreeSearch(startm, sucesorCS, meta, strategy="bfs")
mdfs=sp.TreeSearch(startm, sucesorCS, meta, strategy="dfs")
mbas0=sp.TreeSearch(startm, sucesorCS, meta, strategy="a*", heuristic=hcero)
mbas=sp.TreeSearch(startm, sucesorCS, meta, strategy="a*", heuristic=heuristica)

t1=time.time()
mr1=mbfs.find(max_iter=5000)
mn1=mbfs.iterations
mt1=time.time()-t1

t2=time.time()
mr2=mdfs.find(max_iter=5000)
mn2=mdfs.iterations
mt2=time.time()-t2

t3=time.time()
mr3=mbas0.find(max_iter=5000)
mn3=mbas0.iterations
mt3=time.time()-t3

t4=time.time()
mr4=mbas.find(max_iter=5000)
mn4=mbas.iterations
mt4=time.time()-t4

#INSTANCIA SUPERIOR
starts=sp.node(((1,),(1,1),(1,1,0),(1,1,1,1),(1,1,1,1,1)), depth=0, parent=None)

sbfs=sp.TreeSearch(starts, sucesorCS, meta, strategy="bfs")
sdfs=sp.TreeSearch(starts, sucesorCS, meta, strategy="dfs")
sbas0=sp.TreeSearch(starts, sucesorCS, meta, strategy="a*", heuristic=hcero)
sbas=sp.TreeSearch(starts, sucesorCS, meta, strategy="a*", heuristic=heuristica)

t1=time.time()
sr1=sbfs.find(max_iter=5000)
sn1=sbfs.iterations
st1=time.time()-t1

t2=time.time()
sr2=sdfs.find(max_iter=5000)
sn2=sdfs.iterations
st2=time.time()-t2

t3=time.time()
sr3=sbas0.find(max_iter=5000)
sn3=sbas0.iterations
st3=time.time()-t3

t4=time.time()
sr4=sbas.find(max_iter=5000)
sn4=sbas.iterations
st4=time.time()-t4

pruebas=pd.DataFrame({"Instancia":["Fácil", "Fácil", "Fácil", "Fácil", "Media", "Media", "Media", "Media", "Superior", "Superior", "Superior", "Superior"],
                      "Estrategia":["BFS", "DFS", "A*(h=0)", "A*(h(n))", "BFS", "DFS", "A*(h=0)", "A*(h(n))", "BFS", "DFS", "A*(h=0)", "A*(h(n))"],
                      "Nodos expandidos":[fn1, fn2, fn3, fn4, mn1, mn2, mn3, mn4, sn1, sn2, sn3, sn4],
                      "Tiempo (s)":[ft1, ft2, ft3, ft4, mt1, mt2, mt3, mt4, st1, st2, st3, st4]})

print(pruebas)



#Segunda propuesta de heurística
def contar_fichas_aisladas(nodo):
    tb = nodo.state
    n = len(tb)
    aisladas = 0

    for i in range(n):
        for j in range(i + 1):
            if tb[i][j] == 1:
                tiene_vecino = False


                if j >= 1 and tb[i][j-1] == 1: #vecino a la izq
                    tiene_vecino = True
                elif j < i and tb[i][j+1] == 1: #vecino a la der
                    tiene_vecino = True
                elif i >= 1 and j >= 1 and tb[i-1][j-1] == 1: #vecino a la izqsup
                    tiene_vecino = True
                elif i >= 1 and j < i and tb[i-1][j] == 1: #vecino a la dersup
                    tiene_vecino = True
                elif i < n - 1 and tb[i+1][j] == 1: #vecino a la izqinf
                    tiene_vecino = True
                elif i < n - 1 and tb[i+1][j+1] == 1: #vecino a la derinf
                    tiene_vecino = True

                if not tiene_vecino:
                    aisladas += 1

    return aisladas

def heuristica_2(*nodos):
    nodo = nodos[0]
    fichas = contar_fichas(nodo)
    aisladas = contar_fichas_aisladas(nodo)

    return (fichas - 1) + (2 * aisladas)
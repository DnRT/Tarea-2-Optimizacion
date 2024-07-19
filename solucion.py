import random as rnd

def evaluar_solucion(solucion):
    exposicion = sum([exposicion_p[i] * solucion[i] for i in range(len(solucion))])
    costo_s = sum([costos[i] * solucion[i] for i in range(len(solucion))])
    calidad_s = sum([calidad_l[i] * solucion[i] for i in range(len(solucion))])

    for i, limite in zip(index_la, limites_a):
        if solucion[i] > limite:
            return -float('inf'), float('inf'), -float('inf')
    
    cond1 = solucion[0] * costos[0] + solucion[1] * costos[1] > limites_c[0]
    cond2 = solucion[2] * costos[2] > limites_c[1]
    cond3 = solucion[3] * costos[3] > limites_c[1]
    cond4 = solucion[2] * costos[2] + solucion[4] * costos[4] > limites_c[2]

    if(cond1 or cond2 or cond3 or cond4):
        return -float('inf'), float('inf'), -float('inf')
    
    return exposicion, costo_s, calidad_s

def reparar_solucion(solucion):
    
    cond1 = solucion[0] * costos[0] + solucion[1] * costos[1] > limites_c[0]
    cond2 = solucion[2] * costos[2] > limites_c[1]
    cond3 = solucion[3] * costos[3] > limites_c[1]
    cond4 = solucion[2] * costos[2] + solucion[4] * costos[4] > limites_c[2]
    
    for i in range(len(solucion)):
        if solucion[i] > limites_a[i]:
            solucion[i] = limites_a[i]

    while (cond1 and cond2 and cond3 and cond4):
        i = rnd.randint(0, len(solucion) - 1)
        if solucion[i] > 0:
            solucion[i] -= 1
    return solucion

num_mapaches = 100
num_iteraciones = 1000
probabilidad_exploracion = 0.5
costos = [180, 325, 60, 110, 15]  
exposicion_p = [1000, 2000, 1500, 2500, 300]
limites_c = [3800, 2800, 3500]
index_lc = [0, 2, 3]
limites_a = [15, 10, 25, 4, 30]
index_la = [0, 1, 2, 3, 4]
calidad_l = [75, 93, 50, 70, 25]

poblacion = [rnd.choices(range(30), k=5) for _ in range(num_mapaches)]
mejor_solucion = None
mejor_exposicion = -float('inf')
mejor_calidad = -float('inf')
mejor_costo = float('inf')

for mapache in poblacion:
    exposicion, costo, calidad = evaluar_solucion(mapache)
    if costo <= mejor_costo and calidad >= mejor_calidad:
        mejor_solucion = mapache
        mejor_exposicion = exposicion
        mejor_costo = costo
        mejor_calidad = calidad

for _ in range(num_iteraciones):
    for i in range(num_mapaches):
        if rnd.random() < probabilidad_exploracion:
            nueva_solucion = rnd.choices(range(30), k=5)
        else:
            vecino = rnd.choice(poblacion)
            nueva_solucion = [(mapache + mejor) // 2 for mapache, mejor in zip(poblacion[i], vecino)]

        exposicion, costo, calidad = evaluar_solucion(nueva_solucion)
        if costo <= mejor_costo and calidad >= mejor_calidad:
            mejor_solucion = nueva_solucion
            mejor_exposicion = exposicion
            mejor_costo = costo
            mejor_calidad = calidad
        else:
            nueva_solucion = reparar_solucion(nueva_solucion)
            exposicion, costo, calidad = evaluar_solucion(nueva_solucion)
            if costo <= mejor_costo and calidad >= mejor_calidad:
                mejor_solucion = nueva_solucion
                mejor_exposicion = exposicion
                mejor_costo = costo
                mejor_calidad = calidad
        poblacion[i] = nueva_solucion

print("Mejor solución:", mejor_solucion)
print("Exposición de la solución:", mejor_exposicion)
print("Costo de la solución:", mejor_costo)
print("Calidad de la solución:", mejor_calidad)
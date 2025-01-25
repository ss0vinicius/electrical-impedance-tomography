import csv
from turtle import st
from typing import ValuesView
import numpy
import cv2



def color_normalized(valor_normalized:float):
    '''
    valor_normalized:float

    Ao entrar com um valor normalizado, de 0 a 1, a função retorna uma lista com valores RGB
    sendo que na lista retorna os valores de (RED,GREEN,BLUE)

    '''
    if valor_normalized > 0.55 and valor_normalized <= 1.0:
        red = 255
        gree = ((1 - valor_normalized)/(1- 0.55))*255
        blue = 0
        return [int(blue),int(gree),int(red)]
    elif valor_normalized > 0.45 and valor_normalized<= 0.55:
        red = ((valor_normalized - 0.45)/(0.55 - 0.45))*255
        gree = 255
        blue = ((0.55 - valor_normalized)/(0.55 - 0.45))*255
        return [int(blue),int(gree),int(red)]
    elif valor_normalized >= 0 and valor_normalized<= 0.45:
        red = 0
        gree = (valor_normalized/0.45)*255
        blue = 255
        return [int(blue),int(gree),int(red)]
    else:
        return [0,0,0]





def color_triangles_normalized( *args):
    '''
    args:list
    
    Entre com um vetor normalizado (valores de 0 a 1) para obter a lista de lista com as cores.

    '''
    color_list = list()

    max_value = float(max(args[0]))
    min_value = float(min(args[0]))



    if len(args) > 1:
        return[]
    for normalized_valor in args[0]:

        color_list.append(color_normalized(float(normalizedValue(float(normalized_valor),
                                                min_value,max_value))))

        
    
    return color_list


def normalizedValue(value,min_value,max_value):
    '''
    '''
    diff = float(max_value) - float(min_value)
    ret  = (value - min_value)/diff
    return ret
    


def open_csv(*args):
    '''
    args:list

    entrada de uma lista com o caminho para a pasta desejada com as informações.
    a lista deve contar com o caminho do arquivo em formator de string separado
    por virgulas
    '''
    #route = os.path.join(os.getcwd(),args[0])
    route = args[0]
    with open(f"{route}",'r') as points:
        reader_points = list(csv.reader(points, delimiter=';',quoting= csv.QUOTE_NONNUMERIC))
    return reader_points


def shapes_points(step:int = 3,width_window:int = 400,
                height_window:int = 400,points_shapes:list = []):
    '''
    step:int
    width_window:int
    height_window:int
    points_shapes:list

    Gerador de lista com os pontos de cada conjunto de poligonos desejados sendo que no minimo
    para formar um poligono é necessario 3 pontos.

    '''

    #Separar em uma lista de++ tuplas onde cada tupla recebera  outras 3 tuplas sendo que representarão um dos vetices dos triangulos
    range_points = range(0,len(points_shapes))
    shape_list_points = list()

    for i in range_points[::step]:

        #lista de repasse para a lista principal que sera acessada e realizara a reconstrução da imagem
        lista_repas = list()

        #laço de repetição para a criação das tupla interna a lista de repas
        for p in range(0,step):
            #calculo realizado para da posição do novo ponto, levando em consideração o tamanho da tela criada
            lista_repas.append((int(points_shapes[i+p][0]*width_window/2+width_window/2),
                                int(points_shapes[i+p][1]*height_window/2+height_window/2)))
            
        #Adicionando na lista principal a tupla de posições com os vertices do triangulo
        shape_list_points.append(lista_repas)
        

    return shape_list_points



def retVobj(lista1,lista2):


    retorno = list()

    if(len(lista1)==len(lista2)):
        for i in range(0,len(lista1)):
            retorno.append(((lista2[i]-lista1[i])/lista1[i]))


    
    return retorno



def projeLiner(Sensiblidade:list = [],Vobj:list = [],Vref:list = []):
    """
    Realiza o calculo por meio do metodo retroprojeção linear

    Args:
        Sensiblidade (list): matriz sensibilidade
        Vobj (list): Matriz com os valores de medições das variações de tensão
        Vref (list): Matriz com os valores de tensão referência
    
    Returns:
        list: Matriz resultado
    """

    Vobj = numpy.array(Vobj).T
    Vref = numpy.array(Vref).T
    
    Lamb = retVobj(Vref,Vobj)
    matrix_Lamb = numpy.array(Lamb)
    matrix_S = numpy.array(Sensiblidade)
    matrix_St = matrix_S.T

    Gk = matrix_St.dot(matrix_Lamb)

    return list(Gk)

def landweber(Sensiblidade:list = [],Vobj:list = [],Vref:list = [],intera:int = 0):
    """
    Realiza o calculo por meio do metodo interativo de LandWaber

    Args:
        Sensiblidade (list): matriz sensibilidade
        Vobj (list): Matriz com os valores de medições das variações de tensão
        Vref (list): Matriz com os valores de tensão referência
        intera (int): Nuemro de interações que será realizado no metodo de LandWaber
    
    Returns:
        list: Matriz resultado da interação de LandWaber
    """
    Vobj = numpy.array(Vobj).T
    Vref = numpy.array(Vref).T
    
    Lamb = retVobj(Vref,Vobj)
    #Lamb = numpy.array(((Vobj-Vref)/Vref))
    matrix_Lamb = numpy.array(Lamb)
    matrix_S = numpy.array(Sensiblidade)
    matrix_St = matrix_S.T

    StS = matrix_St.dot(matrix_S)
    autovalor,autovetores = numpy.linalg.eig(StS)


    max_auto = max(autovalor)

    #Gk = matrix_St.dot(matrix_Lamb)
    Gk = numpy.zeros((1024,1))

    #mi = 1.59
    mi = 2/(max_auto.real)


    for i in range(0,intera):
        #print("???????????????????????????????????????????????????????")
        Gk = Gk - mi*matrix_St.dot(matrix_S.dot(Gk) - matrix_Lamb)
        Gk = convergeF(Gk)
    
    #print("________________________________________________")
    #print(Gk[15])

    return list(Gk)


def convergeF(lista:list = []):
    for i,argumento in enumerate(lista):
        if(argumento<0):
            lista[i] = 0

        elif(argumento>1):
            lista[i] = 1
    
    return lista


def rebuildImg(Rwidth:int = 500,
                Rheight:int = 500,
                RouteFileVobj:str = '',
                RouteFileVref:str = '',
                RouteFilejn:str = '',
                method:str = '',
                intera_LDWBR:int = 0):

    imagem = numpy.zeros((Rwidth,Rheight,3), numpy.uint8)

    point_list = open_csv('Cord.csv')
    shapes = shapes_points(step=3, width_window = Rwidth,height_window= Rheight, points_shapes= point_list)
    color = list()

    Vref = open_csv(RouteFileVref)

    jn = open_csv(RouteFilejn)

    Vobj = open_csv(RouteFileVobj)

    if method == "LDWBR":
        total = landweber(jn,Vobj,Vref,intera_LDWBR)
    if method == "RPLIN":
        total = projeLiner(jn,Vobj,Vref)
    

    color = color_triangles_normalized(total)

    for i in range(0,len(shapes)):
        pts = numpy.array(shapes[i],numpy.int32)
        cv2.fillConvexPoly(imagem,pts,color[i])
    
    return imagem

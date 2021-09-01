from MySQLdb import _mysql
from Trivia.forms import RegisterForm, LoginForm, RankingForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import models
from django.db.models import Count
from Trivia.models import Config_Partida, Pregunta, Respuesta, Ranking
import random


#Consultas del juego----------------------------------
def questions():
    #consulta todas las preguntas
    p_queryset = Pregunta.objects.all().values()
    r = Respuesta.objects.all().values()
    c = Config_Partida.objects.all().values()

    p = []
    for question in p_queryset:
        p.append(question)
    # r = Respuesta.objects.all().filter(pregunta_id=21)['respuesta']
    questions_list = {}
    for i in range(len(p_queryset)):
        #numero al azar segun cantidad de preguntas totales
        randNum = random.randint(0,len(p)-1)
        #se guardan todas las preguntas en orden aleatorio en questions_list 
        questions_list['question_' + str(i+1)] = {
            "id": p[randNum]['id'],
            "formula": p[randNum]['formula'],
            "categoría": c[p[randNum]['trivia_id']-1]['nombre'],
            "respuestas": []
            }
        #según las preguntas al azar tomadas se filtran las respectivas respuestas y se agregan a questions_list
        resp_cont = 0
        for respuesta in r:
            if respuesta['pregunta_id'] == questions_list['question_' + str(i+1)]['id']:
                resp_cont = resp_cont + 1
                questions_list['question_' + str(i+1)]['respuestas'].append({'respuesta_' + str(resp_cont): {
                    "formula": respuesta['formula'],
                    "correcta": respuesta['correcta']
                    }})
        del p[randNum]
        randNum+1
    return questions_list

#registrar usuario----------------------------------
def register_post(request):
    # create a form instance and populate it with data from the request:
    form = RegisterForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        form_data = form.cleaned_data
        try:
            check = User.objects.get(username=form_data['name'])
        except:
            user = User.objects.create_user(form_data['name'], form_data['email'], form_data['password'])
            msg = [True, "Usuario creado de forma exitosa!"]
            return msg
        msg = [False, "Usuario ya existente, ingrese otro nombre de usuario."]
        return msg
  
#registrar partida----------------------------------      
def ranking_post(request):
    form = RankingForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        user = User.objects.get(id=request.user.id)
        result = Ranking(usuario=user, aciertos=form_data['result'], pregunta=form_data['pregunta'], correcta=form_data['correcta'], incorrecta=form_data['incorrecta'])
        result.save()
        #CAMBIAR CODIGO POR CONSULTA AL IMPLEMENTAR EL RESULT
        part = Ranking.objects.latest('id')
        partida_id = part.id
        return partida_id
    
#loguear usuario----------------------------------   
def user_login(request):
    form = LoginForm(request.POST)
    #si el formulario esta completo se autentifica con los datos ingresados
    if form.is_valid():
        form_data = form.cleaned_data
        user = authenticate(request, username=form_data['name'], password=form_data['password'])
        if user is not None:
            #aqui se deja abierta la sesión
            login(request, user)
            
            
#obtener ranking----------------------------------      
def ranking_get():
    #se obtiene la lista completa de partidas y se ordena por puntaje, y se filtra para solo ver una por usuario
    rank = Ranking.objects.raw('SELECT id, MAX(aciertos) as maximo, usuario_id, fecha, pregunta, correcta, incorrecta FROM trivia_ranking GROUP BY usuario_id ORDER BY maximo DESC;')
    return rank

#obtener ranking----------------------------------      
def own_historial_get(request):
    #se obtiene la lista completa de partidas propias y se ordena por fecha
    sql = str(f'SELECT * from informatorio.trivia_ranking WHERE usuario_id={request.user.id} ORDER BY fecha DESC;')
    historial = Ranking.objects.raw(sql)
    return historial

#obtener partidas del ranking para mostrar url de partidas espec{----------------------------------      
def historial_get(partida_id):
    #se obtiene la partida a partir de la id ingresada
    part = Ranking.objects.filter(id=partida_id)
    partida = list(part)
    usuario = User.objects.filter(id=partida[0].usuario_id)
    result = {'points': partida[0].aciertos, 'pregunta': partida[0].pregunta, 'correcta': partida[0].correcta, 'incorrecta': partida[0].incorrecta, 'fecha': partida[0].fecha, 'usuario': usuario[0]}
    return result
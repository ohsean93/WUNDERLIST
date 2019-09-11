from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from decouple import config
import requests
# Create your views here.
    
def info(request):
    return render(request, 'todos/info.html')

def index(request):
    todos = Todo.objects.all()
    context = {
        'todos': todos
    }
    return render(request, 'todos/index.html', context)

def create(request):
    # todo = Todo()
    # todo.title = request.POST.get('title')
    # todo.due_date = request.POST.get('due-date')
    # todo.save()

    # return redirect('index')

    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')

        Todo.objects.create(title=title, due_date=due_date)
        token = config('TOKEN')
        user_list = [config('USER'), config('MAIN_USER')]
        base_url = 'https://api.telegram.org/bot'
        for user_id in user_list:
            url = base_url + token + '/sendMessage?text='+ title + str(due_date) +'&chat_id=' + user_id
            print(url)
            requests.get(url)
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')


def delete(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todos:index')

def update(request, pk):
    todo = get_object_or_404(Todo, id=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')

        todo.title = title
        todo.due_date = due_date
        todo.save()

        return redirect('todos:index')
    else:
        context = {
            'todo': todo,
        }
        return render(request, 'todos/update.html', context)
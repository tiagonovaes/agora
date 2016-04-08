# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,render_to_response,redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from conheca.models import Article
from resultados.models import Relatorio
from taggit.models import Tag
from itertools import chain
from .models import Choice, Question, InitialListQuestion, Message, MeuEspacoArtigo
from django.views.decorators.http import condition
from agoraunicamp.decorators import term_required
from django.core.validators import URLValidator
from .forms import DocumentForm
from django.core.exceptions import ValidationError
from agoraunicamp.models import User, Termo, Answer


@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoOutrosView(generic.ListView):
  template_name = 'agora/meu-espaco-outros.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoOutrosView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return Question.objects.all()

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoQuestaoView(generic.ListView):
  template_name = 'agora/meu-espaco-questao.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoQuestaoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return Question.objects.all()

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoArtigoView(generic.ListView):
  template_name = 'agora/meu-espaco.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoArtigoView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return Question.objects.all()

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class MeuEspacoDebateView(generic.ListView):
  template_name = 'agora/meu-espaco-debate.html'

  def get_context_data(self, **kwargs):
    context = super(MeuEspacoDebateView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    tags = Tag.objects.all().distinct()
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    context['tags'] = tags
    context['form'] = DocumentForm
    return context

  def get_queryset(self):
    return Question.objects.all()



@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class HomeView(generic.ListView):
  template_name = 'agora/home.html'

  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now())
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    not_answered = list(set(questions) - set(answered_questions))
    try:
        initial = InitialListQuestion.objects.filter(select=1).first() #pega a lista
        initial_list = [c.name for c in initial.questions.all()]
    except:
        initial_list=[0]
    not_answered_list=[str(f.id) for f in not_answered]
    initial_list_user = list(set(initial_list).intersection(not_answered_list))
    if not initial_list_user:
        first_question = 'none'
    else:
        first_question = initial_list_user[0]
    context['initial_list'] = initial_list
    context['not_answered_list'] = not_answered_list
    context['initial_list_user'] = initial_list_user
    context['first_question'] = first_question
    context['question'] = Question.objects.all()
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['message_participe'] =  Message.objects.filter(published='Sim',kind='4').order_by('-publ_date')
    context['message_conheca'] =  Message.objects.filter(published='Sim',kind='1').order_by('-publ_date')
    context['message_resultados'] =  Message.objects.filter(published='Sim',kind='2').order_by('-publ_date')
    context['message_comunidade'] =  Message.objects.filter(published='Sim',kind='3').order_by('-publ_date')
    context['nickname'] = user.nickname
    return context

  def get_queryset(self):
    return Question.objects.all()

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
#@term_required
class PdpuView(generic.ListView):
  """PDPU home with it's subpages"""
  template_name = 'agora/pagina-pdpu.html'

  def get_queryset(self):
    return

  def get_context_data(self, **kwargs):
    context = super(PdpuView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now(),question_status='p')
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    article = Article.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    relatorio = Relatorio.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    not_answered = list(set(questions) - set(answered_questions))
    result_list = sorted(
        chain(relatorio, article, not_answered),
        key=lambda instance: instance.publ_date, reverse=True)
    context['article'] = Article.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    context['relatorio'] = Relatorio.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')
    context['question'] = Question.objects.all()
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['timeline'] = result_list
    context['nickname'] = user.nickname
    return context

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class PdpuParticipeView(generic.ListView):
  template_name = 'agora/pdpu-participe.html'
  model = Question

  def get_queryset(self):
    return Question.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date')

  def get_context_data(self, **kwargs):
    context = super(PdpuParticipeView, self).get_context_data(**kwargs)
    user = User.objects.get(user=self.request.user)
    questions = Question.objects.filter(exp_date__gt=timezone.now(),question_status='p')
    answered = Answer.objects.filter(user=user)
    answered_questions = [a.question for a in answered]
    context['not_answered'] = list(set(questions) - set(answered_questions))
    context['not_answered'].reverse()
    context['nickname'] = user.nickname
    return context

@method_decorator(login_required(login_url='agora:login'), name='dispatch')
@method_decorator(term_required, name='dispatch')
class DetailView(generic.DetailView):
  model = Question
  template_name = 'agora/detail.html'

  def get_context_data(self, **kwargs):
    context = super(DetailView, self).get_context_data(**kwargs)
    u = User.objects.get(user=self.request.user)
    context['user'] = User.objects.get(user=self.request.user)
    context['nickname'] = u.nickname
    return context

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:pdpu-participe'))

def vote_iframe(request, question_id):

  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:home'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:home'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:home'))

def vote_initial(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return redirect(request.META['HTTP_REFERER']+"#question%s"%(question_id))

def vote_timeline(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  question_type = question.question_type
  success = False
  # Query over the voted questions
  answered_question = Answer.objects.filter(user=user, question=question).count()
  if answered_question:
    error_message = 'Você já votou nesta questão.'
    messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:pdpu'))
  try:
    # Save the answer
    if question_type == '1':
      answer = question.choice_set.get(pk=request.POST['choice'])
      if answer:
        answer_model = Answer(user=user, question=question, choice=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '2':
      answer = request.POST.getlist('choice')
      if answer:
        for choice_id in answer:
          choice = question.choice_set.get(pk=choice_id)
          answer_model = Answer(user=user, question=question, choice=choice)
          answer_model.save()
        success = True
      else:
        error_message = "Parece que você não selecionou nenhuma opção. Por favor, tente novamente."
    elif question_type == '3':
      answer = request.POST['text']
      if answer:
        answer_model = Answer(user=user, question=question, text=answer)
        answer_model.save()
        success = True
      else:
        error_message = "Parece que você deixou o campo em branco. Por favor, tente novamente."
    if success == True:
      messages.success(request, "Obrigado por participar!")
    else:
      messages.error(request, error_message)
    return HttpResponseRedirect(reverse('agora:pdpu'))
  except (KeyError, Choice.DoesNotExist):
    messages.error(request, "Parece que você não selecionou nenhuma opção. Por favor, tente novamente.")
    return HttpResponseRedirect(reverse('agora:pdpu'))

def tag_search(request, tag_name):
  answered_questions_tag = []
  username = AuthUser.objects.get(username=request.user)
  user = username.user
  questions = Question.objects.filter(exp_date__gt=timezone.now())
  answered = Answer.objects.filter(user=user)
  answered_questions = [a.question for a in answered]
  questions_tag = Question.objects.filter(tags__name__in=[tag_name]).distinct()
  article = Article.objects.filter(publ_date__lte=timezone.now(),tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  relatorio = Relatorio.objects.filter(publ_date__lte=timezone.now(),tags__name__in=[tag_name]).order_by('-publ_date').distinct()
  not_answered = list(set(questions) - set(answered_questions))
  not_answered_tag = list(set(questions_tag) - set(answered_questions))
  result_list = sorted(
        chain(relatorio, article, not_answered_tag),
        key=lambda instance: instance.publ_date, reverse=True)
  return render(request, 'agora/pagina-pdpu-search.html',
    { 'article' : Article.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date'),
      'relatorio': Relatorio.objects.filter(publ_date__lte=timezone.now()).order_by('-publ_date'),
      'question' : Question.objects.all(),
      'not_answered': not_answered,
      'not_answered_tag': answered_questions_tag,
      'timeline': result_list,
      'tag' : tag_name,

    })

def term_accepted(request):
    username = AuthUser.objects.get(username=request.user)
    user = username.user
    cond = Termo.objects.get(user=user)
    cond.delete()
    cond1 = Termo(user=user,condition='Sim')
    cond1.save()
    return HttpResponseRedirect(reverse('agora:home'))

def term_not_accepted(request):
    return HttpResponseRedirect(reverse('agora:login'))

def enviaDadosMeuEspaco(request):
    us = User.objects.get(user=request.user)
    user = us.user
    if request.method == 'POST':
        categoria = request.POST['categoriatag']
        comentario = request.POST['comentario']
        link = request.POST['link']
        if link != '':
            validate = URLValidator()
            try:
                validate(link)
            except:
                messages.error(request, "URL incorreta. Envie novamente.")
                return redirect(request.META['HTTP_REFERER'])
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            if request.FILES['arquivo'].name.endswith('.pdf'):
                x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo', arquivo= request.FILES['arquivo'])
                x.save()
                success = True
                if success == True:
                    messages.success(request, "Arquivo enviado com sucesso")
                    return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Arquivo não enviado. Apenas arquivos PDF são aceitos.")
                return redirect(request.META['HTTP_REFERER'])
        if link !='':
            form = DocumentForm() #A empty, unbound form
            x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Artigo')
            x.save()
            messages.success(request, "Link enviado com sucesso")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Você não enviou nenhum artigo. Caso queira enviar apenas um comentário vá em outras sugestões")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


def enviaDadosMeuEspacoDebate(request):
        us = User.objects.get(user=request.user)
        user = us.user
        if request.method == 'POST':
            categoria = request.POST['categoriatag']
            comentario = request.POST['comentario']
            link = request.POST['link']
            if link != '':
                validate = URLValidator()
                try:
                    validate(link)
                except:
                    messages.error(request, "URL incorreta. Envie novamente.")
                    return redirect(request.META['HTTP_REFERER'])
            x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Debate')
            x.save()
            success = True
            if success == True and comentario !='' or link !='':
                messages.success(request, "Dados enviados com sucesso")
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Nenhum dado foi enviado")
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])

def enviaDadosMeuEspacoQuestao(request):
        us = User.objects.get(user=request.user)
        user = us.user
        if request.method == 'POST':
            categoria = request.POST['categoriatag']
            comentario = request.POST['comentario']
            link = request.POST['link']
            if link != '':
                validate = URLValidator()
                try:
                    validate(link)
                except:
                    messages.error(request, "URL incorreta. Envie novamente.")
                    return redirect(request.META['HTTP_REFERER'])
            x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Questão')
            x.save()
            success = True
            if success == True and comentario !='' or link !='':
                messages.success(request, "Dados enviados com sucesso")
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, "Nenhum dado foi enviado")
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect(request.META['HTTP_REFERER'])

def enviaDadosMeuEspacoOutros(request):
    us = User.objects.get(user=request.user)
    user = us.user
    if request.method == 'POST':
        categoria = request.POST['categoriatag']
        comentario = request.POST['comentario']
        link = request.POST['link']
        if link != '':
            validate = URLValidator()
            try:
                validate(link)
            except:
                messages.error(request, "URL incorreta. Envie novamente.")
                return redirect(request.META['HTTP_REFERER'])
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['arquivo'].name.endswith('.pdf'):
                x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros', arquivo= request.FILES['arquivo'])
                x.save()
                success = True
                if success == True:
                    messages.success(request, "Dados enviados com sucesso.")
                    return redirect(request.META['HTTP_REFERER'])

        else:
            x = MeuEspacoArtigo(user=user.username, categoria=categoria, publ_date=timezone.now(), link=link, comentario=comentario, secao='Outros')
            x.save()
            messages.success(request, "Dados enviados com sucesso.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])

from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,DetailView,UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from cloneapp.forms import registration_form,new_question_form,userprofile,answer_form
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from cloneapp.models import question,user_info,answerclass
from django.contrib.staticfiles.storage import staticfiles_storage

# Create your views here.
def firstpage(request):
    return render(request,'cloneapp/firstpage.html')
class frontpage(ListView):
    model=question
    template_name='question_list.html'
    queryset = question.objects.filter(published=True).order_by('-publish_date')

@login_required(login_url='/login/')
def question_create(request):
    if(request.method=='POST'):
        a=question()
        a.question_title=request.POST['question_tit']
        a.author = get_object_or_404(user_info,user_p=request.user)
        a.save()
        return HttpResponseRedirect(reverse('cloneapp:question_detail',kwargs={'pk':a.pk}))


def profile_user_info(request,pk):
    u=get_object_or_404(user_info,pk=pk)
    return render(request,'cloneapp/profile_user_inf.html',{'model':u})


class detailpage(DetailView):
    model=question
    template_name='question_detail.html'
    context_text_name='question'

    def post(self, request, * args, ** kwargs):
        answer_form=answerclass()
        answer_form.title_ans=request.POST['answerone']
        answer_form.author_ans=get_object_or_404(user_info,user_p=request.user)
        answer_form.question_answer=question.objects.get(pk=kwargs['pk'])
        answer_form.save()
        k=kwargs['pk']
        return HttpResponseRedirect(reverse('cloneapp:question_detail',kwargs={'pk':k}))

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        answer_form=answerclass()
        context['comments']=answerclass.objects.filter(question_answer=context['question'])
        context['answer_form']=answer_form
        return context


class updatepost(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='cloneapp/question_detail.html'
    form_class=new_question_form
    model=question
    context_text_name="form"


@login_required(login_url='/login/')
def deletequestion(request,pk):
    question_q=get_object_or_404(question,pk=pk)
    question_q.delete()
    return HttpResponseRedirect(reverse('cloneapp:question_list'))

class draftquestions(LoginRequiredMixin,ListView):
    login_url='/login/'
    model=question

    def get_queryset(self):
        return question.objects.filter(author__user_p = self.request.user).filter(published=False)


@login_required(login_url='/login/')
def published_question(request,pk):
    question_user=get_object_or_404(question,pk=pk)
    question_user.publish()
    question_user.save()
    return HttpResponseRedirect(reverse('cloneapp:question_detail',kwargs={'pk':pk}))

def login_user(request):
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if(user):
            if(user.is_active):
                login(request,user)
    return HttpResponseRedirect(reverse('cloneapp:question_list'))


@login_required(login_url='/login/')
def delete_answer(request,pk):
    obj=get_object_or_404(answerclass,pk=pk)
    form_pk=obj.question_answer.pk
    obj.delete()
    return HttpResponseRedirect(reverse('cloneapp:question_detail',kwargs={'pk':form_pk}))


# @login_required(login_url='/login/')
# def edit_answer(request,pk):
#     obj=get_object_or_404(answerclass,pk)
#     if(request.method=='GET'):




@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('cloneapp:question_list'))



def register_user(request):
    if(request.method=='POST'):
        form_user=registration_form(request.POST,request.FILES)
        form_profile=userprofile(data=request.POST)
        if(form_profile.is_valid() and form_user.is_valid()):
            form_profile=form_profile.save()
            form_profile.set_password(form_profile.password)
            form_profile.save()
            b=form_user.save(commit=False)
            b.user_p=form_profile
            if('image_field' in request.FILES):
                 b.image_field=request.FILES['image_field']
            else:
                url_image = staticfiles_storage.url('images/images.png')
                b.image_field=url_image
            b.save()
            return HttpResponseRedirect(reverse('cloneapp:question_list'))
        else:
            return render(request,'cloneapp/registration.html',{'form':form_user,'form_us':form_profile})

    else:
        form_info=userprofile()
        form_user=registration_form()
        return render(request,'cloneapp/registration.html',{'form':form_user,'form_us':form_info})

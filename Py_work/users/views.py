from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """login"""
    if request.method != 'POST':
        # display empty login form.
        form = UserCreationForm()
    else:
        # process form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            login(request, new_user)
            return redirect('learning_logs:index')

    # display empty form or indicate form is not available
    context = {'form': form}
    return render(request, 'registration/register.html', context)

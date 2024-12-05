from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Now you can login!')
            return redirect('login')  
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})

@login_required
def profile(request):

    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
# this code makes it so that when a user creates an account they automatically get a profile created

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

        # Check if the user has a profile, and create one if it doesn't exist

        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Student Profile'
    }
    return render(request, 'users/profile.html', context)







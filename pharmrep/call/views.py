from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from call.forms import CallForm
from product.models import Rep
from call.models import Call


@login_required
def call(request):
    try:
        rep = Rep.objects.get(user=request.user)
    except Rep.DoesNotExist:
        messages.error(request, 'You need to be a rep to register calls')
        return redirect('/accounts/login/')
    if request.method == 'POST':
        form = CallForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.rep = rep
            obj.save()
            messages.success(request, 'Successfully added call')
    else:
        form = CallForm()
    return render(request, 'call/call.html', {'form': form})


@login_required
def call_list(request):
    rep = get_object_or_404(Rep, user=request.user)
    calls = Call.objects.filter(rep=rep).order_by('-call_date')
    return render(request, 'call/calls_list.html', {'calls': calls})

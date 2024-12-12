from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'transactions/index.html', {'transactions': transactions})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})

@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/transaction_form.html', {'form': form})

from django.shortcuts import render,redirect, get_object_or_404

from camping.models import CampingItem, Category
from transaction.models import Transaction
from .forms import UserTransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def member_transaction_list(request):
    """Menampilkan daftar transaksi milik user yang sedang login"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')  # Urutkan berdasarkan waktu terbaru
    return render(request, 'member_transactions/member_transaction_list.html', {'transactions': transactions})

@login_required
def member_transaction_categories(request):
    """Menampilkan daftar kategori untuk member"""
    categories = Category.objects.all()
    return render(request, 'member_transactions/member_transaction_categories.html', {'categories': categories})


@login_required
def member_transaction_items(request, category_id):
    """Menampilkan item berdasarkan kategori untuk member"""
    category = get_object_or_404(Category, pk=category_id)
    items = CampingItem.objects.filter(category=category)
    return render(request, 'member_transactions/member_transaction_items.html', {'category': category, 'items': items})


@login_required
def member_transaction_form(request, item_id):
    item = get_object_or_404(CampingItem, pk=item_id)
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = UserTransactionForm(request.POST, request.FILES, item=item)  # Tambahkan item
        if form.is_valid():
            print("Form valid. Data siap disimpan.")
            transaction = form.save(commit=False)
            transaction.user = request.user  # Tetapkan user yang sedang login
            transaction.item = item  # Tetapkan item yang dipilih
            if not transaction.status:
                transaction.status = 'pending'
            transaction.save()
            return redirect('transaction_list')  # Redirect ke kategori
        else:
            print("Form errors:", form.errors)  # Debugging error form
    else:
        form = UserTransactionForm(item=item)
    return render(request, 'member_transactions/member_transaction_form.html', {'item': item, 'form': form})

@login_required
def member_transaction_detail(request, transaction_id):
    """Menampilkan detail transaksi untuk member"""
    transaction = get_object_or_404(Transaction, pk=transaction_id, user=request.user)
    return render(request, 'member_transactions/member_transaction_detail.html', {'transaction': transaction})
from django.shortcuts import render, redirect, get_object_or_404

from camping.models import CampingItem, Category
from .models import Transaction, PaymentMethod
from .forms import TransactionForm, PaymentMethodForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
import csv
from django.db.models import Q

def is_staff_or_admin(user):
    return user.is_staff_user() or user.is_admin()

def is_admin(user):
    return user.is_admin()

@login_required
@user_passes_test(is_staff_or_admin)
def transaction_list(request):
    search_query = request.GET.get('search', '')
    transactions = Transaction.objects.filter(
        Q(invoice_id__icontains=search_query) |
        Q(status__icontains=search_query) |
        Q(user__username__icontains=search_query) |
        Q(note__icontains=search_query)
    ).order_by('-created_at')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        transactions = transactions.filter(rent_date__range=[start_date, end_date])

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    transaction_page = paginator.get_page(page_number)
    return render(request, 'transactions/index.html', {'transactions': transaction_page})


@login_required
@user_passes_test(is_staff_or_admin)
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})

@login_required
@user_passes_test(is_staff_or_admin)
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction,item=transaction.item)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, item=transaction.item)
    return render(request, 'transactions/transaction_form.html', {'form': form})

@login_required()
@user_passes_test(is_admin)
def payment_method_list(request):
    methods = PaymentMethod.objects.all()
    return render(request, 'payment/index.html', {'methods': methods})

@login_required()
@user_passes_test(is_admin)
def payment_method_create(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_method_list')
    else:
        form = PaymentMethodForm()
    return render(request, 'payment/payment_method_form.html', {'form': form})

@login_required()
@user_passes_test(is_admin)
def payment_method_update(request, pk):
    method = get_object_or_404(PaymentMethod, pk=pk)
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=method)
        if form.is_valid():
            form.save()
            return redirect('payment_method_list')
    else:
        form = PaymentMethodForm(instance=method)
    return render(request, 'payment/payment_method_form.html', {'form': form})

@login_required()
@user_passes_test(is_admin)
def payment_method_delete(request, pk):
    method = get_object_or_404(PaymentMethod, pk=pk)
    if request.method == 'POST':
        method.delete()
        return JsonResponse({'success': True, 'message': 'Payment deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required()
@user_passes_test(is_staff_or_admin)
def export_transactions_csv(request):
    # Membuat HTTP response dengan content type CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    # Membuat writer untuk menulis ke CSV
    writer = csv.writer(response)
    writer.writerow(['Invoice ID', 'User', 'Item', 'Quantity', 'Total Price', 'Status', 'Rent Date', 'Return Date'])

    # Ambil data transaksi
    transactions = Transaction.objects.all()

    for transaction in transactions:
        writer.writerow([
            transaction.invoice_id,
            transaction.user.username,
            transaction.item.name,
            transaction.quantity,
            transaction.total_price,
            transaction.status,
            transaction.rent_date,
            transaction.return_date,
        ])

    return response
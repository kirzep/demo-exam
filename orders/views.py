from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from .forms import OrderForm

# Create your views here.
def order_list(request):
    if request.user.is_anonymous or request.user.role == 'client':
        messages.error(request, 'У вас нет доступа к списку заказов.')
        return redirect('products:product_list')
        
    orders = Order.objects.all().order_by('-date_created')
    return render(request, 'orders/order_list.html', {'orders': orders})

# Создание (Только Админ)
def order_create(request):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может добавлять заказы.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно создан!')
            return redirect('orders:order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Новый заказ'})

# Редактирование (Только Админ)
def order_update(request, pk):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может редактировать заказы.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ обновлен!')
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form, 'title': f'Редактирование заказа №{order.order_number}'})

# Удаление (Только Админ)
def order_delete(request, pk):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может удалять заказы.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ удален!')
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
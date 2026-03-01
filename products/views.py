from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, RestrictedError
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    # Вытаскиваем уникальных поставщиков
    suppliers = Product.objects.exclude(supplier='').values_list('supplier', flat=True).distinct()

    # Фильтруем только если пользователь имеет нужные права
    if request.user.is_authenticated and request.user.role in ['manager', 'admin']:
        search_query = request.GET.get('q', '')
        sort_by = request.GET.get('sort', '')
        supplier = request.GET.get('supplier', '')

        # Поиск сразу по нескольким текстовым полям
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(manufacturer__icontains=search_query) |
                Q(supplier__icontains=search_query) |
                Q(category__icontains=search_query)
            )
        
        # Фильтрация по поставщику
        if supplier and supplier != 'all':
            products = products.filter(supplier=supplier)
        
        # Сортировка по количеству на складе
        if sort_by == 'stock_asc':
            products = products.order_by('stock')
        elif sort_by == 'stock_desc':
            products = products.order_by('-stock')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'products/product_cards.html', {'products': products})

    # Обычная загрузка страницы
    return render(request, 'products/product_list.html', {
        'products': products,
        'suppliers': suppliers
    })

def product_create(request):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может управлять товарами.')
        return redirect('products:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Ошибка при заполнении формы. Проверьте данные.')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Добавление товара'})

def product_update(request, pk):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может управлять товарами.')
        return redirect('products:product_list')

    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные товара успешно обновлены!')
            return redirect('products:product_list')
        else:
            messages.error(request, 'Ошибка при заполнении формы.')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Редактирование товара', 'product': product})

def product_delete(request, pk):
    if request.user.is_anonymous or request.user.role != 'admin':
        messages.error(request, 'Только администратор может управлять товарами.')
        return redirect('products:product_list')

    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Товар успешно удален!')
        except RestrictedError:
            messages.error(request, f'Ошибка: Невозможно удалить "{product.name}", так как он присутствует в оформленных заказах.')
        return redirect('products:product_list')
        
    return render(request, 'products/product_confirm_delete.html', {'product': product})
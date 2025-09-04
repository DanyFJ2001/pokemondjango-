from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from .models import Product
from .forms import ProductForm

def products(request):
    print("=== DEBUGGING ===")
    
    # Verificar cuántos productos hay en total
    total_count = Product.objects.count()
    print(f"Total productos en DB: {total_count}")
    
    # Obtener todos los productos de la base de datos
    all_products = Product.objects.all().order_by('id')
    print(f"Productos obtenidos: {len(all_products)}")
    
    # Configurar paginación
    paginator = Paginator(all_products, 20)  # 20 productos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    print(f"Página actual: {page_obj.number}")
    print(f"Productos en esta página: {len(page_obj)}")
    
    if len(page_obj) > 0:
        print(f"Primer producto: {page_obj[0].title}")
    
    context = {
        'products': page_obj,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'next_page': page_obj.number + 1 if page_obj.has_next() else None,
        'previous_page': page_obj.number - 1 if page_obj.has_previous() else None,
    }
    
    print("=== FIN DEBUG ===")
    return render(request, 'products.html', context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                # Asignar valores por defecto para campos requeridos no incluidos
                product.price = 0.00
                product.image = ''
                product.save()
                messages.success(request, f'¡Pokémon "{product.title}" creado exitosamente!')
                return redirect('pokemon_detail', product_id=product.id)
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {
        'form': form,
        'title': 'Crear Nuevo Pokémon',
        'submit_text': 'Crear Pokémon'
    })

def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            try:
                updated_product = form.save()
                messages.success(request, f'¡Pokémon "{updated_product.title}" actualizado exitosamente!')
                return redirect('pokemon_detail', product_id=updated_product.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            # Debug: imprimir errores en consola
            print("Errores del formulario:", form.errors)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {
        'form': form,
        'product': product,
        'title': f'Editar {product.title}',
        'submit_text': 'Actualizar Pokémon'
    })

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.title
        product.delete()
        messages.success(request, f'¡Pokémon "{product_name}" eliminado exitosamente!')
        return redirect('products')
    
    return render(request, 'product_confirm_delete.html', {'product': product})
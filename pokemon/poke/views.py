from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product

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
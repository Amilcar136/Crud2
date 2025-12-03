from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm, RegistroForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('productos:lista')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol = form.cleaned_data.get('rol')
            
            # Asignar grupos según el rol
            if rol == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})

@login_required
def crear_producto(request):
    # Solo admin puede crear
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear productos')
        return redirect('productos:lista')
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario_creador = request.user
            producto.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('productos:lista')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/crear.html', {'form': form})

@login_required
def editar_producto(request, pk):
    # Admin y gerente pueden editar
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tienes permisos para editar productos')
        return redirect('productos:lista')
    
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('productos:lista')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto})

@login_required
def eliminar_producto(request, pk):
    # Solo admin puede eliminar
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar productos')
        return redirect('productos:lista')
    
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('productos:lista')
    
    return render(request, 'productos/eliminar.html', {'producto': producto})

# Validación AJAX
@login_required
def validar_producto_ajax(request):
    nombre = request.GET.get('nombre', '')
    existe = Producto.objects.filter(nombre__iexact=nombre).exists()
    return JsonResponse({'existe': existe})
// Validaciones AJAX para Abarrotera Tecnológico

$(document).ready(function() {
    // Validación de formulario de productos
    $('#productoForm').on('submit', function(e) {
        let isValid = true;
        
        // Validar nombre
        const nombre = $('#id_nombre').val().trim();
        if (nombre.length < 3) {
            alert('El nombre debe tener al menos 3 caracteres');
            isValid = false;
        }
        
        // Validar precio
        const precio = parseFloat($('#id_precio').val());
        if (precio <= 0) {
            alert('El precio debe ser mayor a 0');
            isValid = false;
        }
        
        // Validar stock
        const stock = parseInt($('#id_stock').val());
        if (stock < 0) {
            alert('El stock no puede ser negativo');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
    
    // Validación en tiempo real del nombre del producto
    $('#id_nombre').on('input', function() {
        const nombre = $(this).val();
        if (nombre.length > 0 && nombre.length < 3) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
            $(this).addClass('is-valid');
        }
    });
    
    // Validación de precio en tiempo real
    $('#id_precio').on('input', function() {
        const precio = parseFloat($(this).val());
        if (precio <= 0 || isNaN(precio)) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
            $(this).addClass('is-valid');
        }
    });
    
    // Confirmación de eliminación
    $('a[href*="eliminar"]').on('click', function(e) {
        if (!confirm('¿Está seguro de que desea eliminar este producto?')) {
            e.preventDefault();
        }
    });
});
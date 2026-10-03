# Sistema de inventario y ventas para papelería

## Objetivo
Controlar los productos, las existencias y las ventas de una papelería pequeña.

## Datos de cada producto
- Código (único)
- Nombre
- Categoría (cuadernos, plumas, papel, material escolar, etc.)
- Precio de venta
- Cantidad en existencia
- Stock mínimo (para avisar cuando se está agotando)

## Requisitos funcionales (versión 1)
1. Agregar un producto
2. Ver todos los productos
3. Buscar un producto por nombre o código
4. Modificar un producto (precio, existencia, etc.)
5. Eliminar un producto
6. Registrar una venta (puede incluir varios productos)
7. Descontar del inventario al vender
8. Avisar cuando un producto esté por debajo del stock mínimo

## Reglas del negocio
- No se puede vender más de lo que hay en existencia
- El precio y la cantidad no pueden ser negativos
- El código de producto no se puede repetir

## Fuera de alcance (por ahora)
- Usuarios con contraseña
- Facturación
- Ventas en línea
- Interfaz gráfica (llega en una fase posterior)

## Tecnologías
Python, MySQL, Git/GitHub
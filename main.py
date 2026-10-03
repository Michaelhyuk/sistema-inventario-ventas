import unicodedata

productos = [
    {
        "codigo": "P001",
        "nombre": "Cuaderno profesional rayado",
        "precio_pieza": 35.50,
        "piezas_por_caja": 12,
        "existencia": 48,
        "stock_minimo": 10,
    },
    {
        "codigo": "P002",
        "nombre": "Pluma azul",
        "precio_pieza": 8.00,
        "piezas_por_caja": 50,
        "existencia": 60,
        "stock_minimo": 20,
    },
    {
        "codigo": "P003",
        "nombre": "Lápiz HB",
        "precio_pieza": 5.00,
        "piezas_por_caja": 24,
        "existencia": 30,
        "stock_minimo": 12,
    },
]

ventas = []


def normalizar(texto):
    texto = texto.lower().strip()
    descompuesto = unicodedata.normalize("NFD", texto)
    resultado = ""
    for c in descompuesto:
        if unicodedata.category(c) != "Mn":
            resultado += c
    return resultado


def leer_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("No puede ser negativo. Intenta de nuevo.")
                continue
            return valor
        except ValueError:
            print("Escribe un número válido. Intenta de nuevo.")


def leer_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("No puede ser negativo. Intenta de nuevo.")
                continue
            return valor
        except ValueError:
            print("Escribe un número entero válido. Intenta de nuevo.")


def generar_codigo():
    numero = len(productos) + 1
    return "P" + str(numero).zfill(3)


def mostrar_inventario():
    print()
    print("=== INVENTARIO ===")
    for p in productos:
        print(f"{p['codigo']} - {p['nombre']} - ${p['precio_pieza']:.2f} - {p['existencia']} piezas")


def mostrar_por_agotarse():
    print()
    print("=== POR AGOTARSE ===")
    hay_alguno = False
    for p in productos:
        if p["existencia"] < p["stock_minimo"]:
            print(f"¡Ojo! {p['nombre']} tiene solo {p['existencia']} piezas (mínimo: {p['stock_minimo']})")
            hay_alguno = True
    if not hay_alguno:
        print("Todo en orden, no hay productos por agotarse.")


def buscar_producto():
    print()
    print("=== BUSCAR PRODUCTO ===")
    texto = normalizar(input("Escribe parte del nombre: "))
    encontrados = 0
    for p in productos:
        if texto in normalizar(p["nombre"]):
            print(f"{p['codigo']} - {p['nombre']} - ${p['precio_pieza']:.2f} - {p['existencia']} piezas")
            encontrados += 1
    if encontrados == 0:
        print("No se encontró ningún producto.")


def agregar_producto():
    print()
    print("=== AGREGAR PRODUCTO ===")
    nombre = input("Nombre: ").strip()
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre: ").strip()

    precio = leer_decimal("Precio por pieza: ")
    piezas_por_caja = leer_entero("Piezas por caja (0 si no se vende por caja): ")
    existencia = leer_entero("Existencia (en piezas): ")
    stock_minimo = leer_entero("Stock mínimo: ")

    codigo = generar_codigo()
    productos.append({
        "codigo": codigo,
        "nombre": nombre,
        "precio_pieza": precio,
        "piezas_por_caja": piezas_por_caja,
        "existencia": existencia,
        "stock_minimo": stock_minimo,
    })
    print("Producto agregado con código", codigo)


def elegir_producto():
    texto = normalizar(input("Producto a vender (parte del nombre): "))
    if texto == "":
        print("Escribe al menos una letra.")
        return None

    coincidencias = []
    for p in productos:
        if texto in normalizar(p["nombre"]):
            coincidencias.append(p)

    if len(coincidencias) == 0:
        print("No se encontró ningún producto.")
        return None
    if len(coincidencias) == 1:
        return coincidencias[0]

    print("Se encontraron varios:")
    numero = 1
    for p in coincidencias:
        print(f"{numero}. {p['nombre']} - ${p['precio_pieza']:.2f}")
        numero += 1
    eleccion = leer_entero("Elige el número (0 para cancelar): ")
    if eleccion == 0 or eleccion > len(coincidencias):
        print("No se eligió ningún producto.")
        return None
    return coincidencias[eleccion - 1]


def agregar_al_carrito(carrito, producto):
    tipo = input("¿Por (P)ieza o por (C)aja? ").strip().lower()

    if tipo == "c":
        if producto["piezas_por_caja"] == 0:
            print("Este producto no se vende por caja.")
            return
        cantidad = leer_entero("¿Cuántas cajas?: ")
        piezas = cantidad * producto["piezas_por_caja"]
        descripcion = f"{cantidad} caja(s) de {producto['nombre']}"
    elif tipo == "p":
        cantidad = leer_entero("¿Cuántas piezas?: ")
        piezas = cantidad
        descripcion = f"{cantidad} pieza(s) de {producto['nombre']}"
    else:
        print("Opción no válida.")
        return

    if piezas == 0:
        print("La cantidad debe ser mayor que 0.")
        return

    ya_en_carrito = 0
    for item in carrito:
        if item["producto"]["codigo"] == producto["codigo"]:
            ya_en_carrito += item["piezas"]

    disponibles = producto["existencia"] - ya_en_carrito
    if piezas > disponibles:
        print(f"No hay suficiente. Disponible: {disponibles} piezas.")
        return

    subtotal = piezas * producto["precio_pieza"]
    carrito.append({
        "producto": producto,
        "descripcion": descripcion,
        "piezas": piezas,
        "subtotal": subtotal,
    })
    print("Agregado:", descripcion)


def registrar_venta():
    print()
    print("=== REGISTRAR VENTA ===")
    carrito = []

    while True:
        producto = elegir_producto()
        if producto is not None:
            agregar_al_carrito(carrito, producto)
        otro = input("¿Agregar otro producto? (s/n): ").strip().lower()
        if otro != "s":
            break

    if len(carrito) == 0:
        print("Venta cancelada: no hay productos.")
        return

    print()
    print("--- RESUMEN DE LA VENTA ---")
    total = 0
    for item in carrito:
        print(f"{item['descripcion']} - ${item['subtotal']:.2f}")
        total += item["subtotal"]
    print(f"TOTAL: ${total:.2f}")

    confirmar = input("¿Confirmar venta? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Venta cancelada.")
        return

    for item in carrito:
        item["producto"]["existencia"] -= item["piezas"]
    ventas.append({"total": total, "articulos": len(carrito)})
    print("Venta registrada.")

    for item in carrito:
        p = item["producto"]
        if p["existencia"] < p["stock_minimo"]:
            print(f"¡Ojo! A {p['nombre']} le quedan solo {p['existencia']} piezas.")


while True:
    print()
    print("=== PAPELERÍA ===")
    print("1. Ver inventario")
    print("2. Ver productos por agotarse")
    print("3. Agregar producto")
    print("4. Buscar producto")
    print("5. Registrar venta")
    print("6. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        mostrar_inventario()
    elif opcion == "2":
        mostrar_por_agotarse()
    elif opcion == "3":
        agregar_producto()
    elif opcion == "4":
        buscar_producto()
    elif opcion == "5":
        registrar_venta()
    elif opcion == "6":
        print("Hasta luego.")
        break
    else:
        print("Opción no válida.")

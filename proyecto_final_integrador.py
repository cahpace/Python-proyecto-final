import sqlite3


# funcion para conexion a la base de datos
def conectar(database):
    conexion = sqlite3.connect(database)
    return conexion
# ---------------------------------------------------------------------
def crear_tabla():
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    #crear tabla
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL, 
            nombre TEXT NOT NULL,
            descripcion TEXT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL, 
            categoria TEXT NOT NULL)
    """)
    conexionBaseDatos.commit()
    conexionBaseDatos.close()
crear_tabla()

# ---------------------------------------------------------------------
# fncion para mostrar las opciones del menu
def mostrar_menu():
    print("\n")
    print("Menú de Gestión de Inventario:")
    print("1. Registrar producto")
    print("2. Mostrar productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte de Bajo Stock")
    print("7. Salir")

# -----------------------------------------------------------------------
def registrar_producto():
    codigo = input("Ingrese el codigo del producto: ")
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripcion del producto: ")
    cantidad = int(input("Ingrese la cantidad disponible del producto: "))
    while cantidad <= 0:
        print("Cantidad tiene que ser mayor que cero")
        cantidad = int(input("Ingrese la cantidad disponible del producto: ")) 
    precio = float(input("Ingrese el precio del producto: "))
    categoria = input("Ingrese la categoria del producto: ")

    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    cursor.execute("INSERT INTO productos (codigo, nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?, ?)", 
                   (codigo, nombre, descripcion, cantidad, precio, categoria) 
                   )
    conexionBaseDatos.commit()
    conexionBaseDatos.close()

# ---------------------------------------------------------------------------------------------------------------
def mostrar_productos():
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if len(productos) > 0:
        for item in productos:
            print(f"ID: {item[0]}, Codigo: {item[1]}, Nombre: {item[2]}, Descripción: {item[3]}, Cantidad: {item[4]}, Precio: {item[5]}")
            print("-"*10)
    else:
        print("Inventario está vacio!")
    conexionBaseDatos.close()
   
# -----------------------------------------------------------------------------------------------------------------   
def actualizar_producto():
    codigo = int(input("Ingrese el codigo del producto que queres modificar: "))
    cantidad = int(input("Ingrese la nueva cantidad del producto: "))
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE codigo = ?", (cantidad, codigo,))
    conexionBaseDatos.commit()
    print("Producto actualizao")
    conexionBaseDatos.close()

# -----------------------------------------------------------------------
def eliminar_producto():
    nombre = input("Ingrese el nombre del producto a eliminar: ")
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    # validar si existe
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
    conexionBaseDatos.commit()
    print("Producto eliminado")
    conexionBaseDatos.close()

# -----------------------------------------------------------------------
def buscar_producto():
    print(" ---------- Buscar producto ----------")
    codigo = input("Ingrese código del producto a buscar: ")
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo = ? ", (codigo,))
    producto = cursor.fetchone()
    if len(producto) > 0:
        print("Producto en stock: ")
        print(f"ID: {producto[0]}, Codigo: {producto[1]}, Nombre: {producto[2]}, Descripción: {producto[3]}, Cantidad: {producto[4]}, Precio: {producto[5]}")
    else:
        print("producto no encontrado en stock!")

# -----------------------------------------------------------------------
def reporte_bajo_stock():
    bajo_stock = int(input("Ingrese la cantidad de bajo stock para buscar productos con bajo stock: "))
    conexionBaseDatos = conectar("inventario.db")
    cursor = conexionBaseDatos.cursor()
    cursor.execute( "SELECT  * FROM productos WHERE cantidad < ?", (bajo_stock,))
    productos = cursor.fetchall()
    print(" ---------- Producto con bajo stock ----------")
    if len(productos) > 0:
        for item in productos:
            print(f"Codigo: {item[1]}, Nombre: {item[2]}, Cantidad: {item[4]}")
            print("-"*10)
    else:
        print("No hay productos con bajo stock")
    conexionBaseDatos.close()

# --------------   main function  -----------------
while True:
    mostrar_menu()
    opcion = int(input("Seleccione una opción: "))
    if opcion == 1:
        registrar_producto()
    elif opcion == 2:
        mostrar_productos()
    elif opcion == 3:
        actualizar_producto()
    elif opcion == 4:
        eliminar_producto()
    elif opcion == 5:
        buscar_producto()
    elif opcion == 6:
        reporte_bajo_stock()
    elif opcion == 7:
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida. Intente nuevamente.")

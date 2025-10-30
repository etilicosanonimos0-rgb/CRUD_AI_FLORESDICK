import pandas as pd
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Ruta del archivo Excel
ARCHIVO = "INTELIGENCIA ARTIFICIAL PYTHON.xlsx"
HOJA = "usuarios"

# --- Funciones CRUD ---

def leer_datos():
    if not os.path.exists(ARCHIVO):
        df = pd.DataFrame(columns=["id", "nombre", "email", "edad"])
        df.to_excel(ARCHIVO, index=False, sheet_name=HOJA)
    else:
        df = pd.read_excel(ARCHIVO, sheet_name=HOJA)
    return df


def guardar_datos(df):
    df.to_excel(ARCHIVO, index=False, sheet_name=HOJA)


def crear_usuario():
    df = leer_datos()
    nuevo_id = df["id"].max() + 1 if not df.empty else 1
    nombre = input("Nombre: ")
    email = input("Email: ")
    edad = int(input("Edad: "))
    nuevo = pd.DataFrame([[nuevo_id, nombre, email, edad]], columns=df.columns)
    df = pd.concat([df, nuevo], ignore_index=True)
    guardar_datos(df)
    print("✅ Usuario creado con éxito.")


def leer_usuarios():
    df = leer_datos()
    print("\n--- Lista de usuarios ---")
    print(df.to_string(index=False))


def actualizar_usuario():
    df = leer_datos()
    id_u = int(input("ID del usuario a actualizar: "))
    if id_u in df["id"].values:
        nombre = input("Nuevo nombre: ")
        email = input("Nuevo email: ")
        edad = int(input("Nueva edad: "))
        df.loc[df["id"] == id_u, ["nombre", "email", "edad"]] = [nombre, email, edad]
        guardar_datos(df)
        print("✅ Usuario actualizado.")
    else:
        print("❌ ID no encontrado.")


def eliminar_usuario():
    df = leer_datos()
    id_u = int(input("ID del usuario a eliminar: "))
    if id_u in df["id"].values:
        df = df[df["id"] != id_u]
        guardar_datos(df)
        print("🗑️ Usuario eliminado.")
    else:
        print("❌ ID no encontrado.")


# Función para subir el archivo a Google Drive
def subir_a_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Autenticación local
    drive = GoogleDrive(gauth)

    # Subir el archivo
    archivo = drive.CreateFile({'title': 'INTELIGENCIA ARTIFICIAL PYTHON.xlsx'})
    archivo.SetContentFile('INTELIGENCIA ARTIFICIAL PYTHON.xlsx')
    archivo.Upload()
    print("Archivo subido exitosamente a Google Drive.")


# --- Menú principal ---
def menu():
    while True:
        print("""
====== CRUD en Excel ======
1. Crear usuario
2. Leer usuarios
3. Actualizar usuario
4. Eliminar usuario
5. Subir a Google Drive
6. Salir
""")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            leer_usuarios()
        elif opcion == "3":
            actualizar_usuario()
        elif opcion == "4":
            eliminar_usuario()
        elif opcion == "5":
            subir_a_google_drive()
        elif opcion == "6":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()

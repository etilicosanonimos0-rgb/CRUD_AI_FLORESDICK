from flask import Flask, render_template, request, redirect
import pandas as pd

# Configuración de Flask
app = Flask(__name__)

# Ruta del archivo Excel
ruta_archivo = "INTELIGENCIA ARTIFICIAL PYTHON.xlsx"

def cargar_datos():
    try:
        df = pd.read_excel(ruta_archivo)
        # Reemplazar encabezado principal
        df.columns = ["RESPONSABLE", "TABLA", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO"]
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["RESPONSABLE", "TABLA", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO", "ATRIBUTO"])

@app.route('/')
def index():
    df = cargar_datos()
    return render_template('index.html', data=df.to_dict(orient='records'), columns=df.columns, enumerate=enumerate)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    df = cargar_datos()
    if request.method == 'POST':
        for column in df.columns:
            df.at[index, column] = request.form[column]
        df.to_excel(ruta_archivo, index=False)
        return redirect('/')
    row = df.iloc[index]
    return render_template('edit.html', row=row, columns=df.columns, index=index)

@app.route('/delete/<int:index>', methods=['POST', 'GET'])
def delete(index):
    df = cargar_datos()
    if index < len(df):
        df = df.drop(index=index).reset_index(drop=True)
        df.to_excel(ruta_archivo, index=False)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
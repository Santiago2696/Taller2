from flask import Flask, render_template, request
import pyodbc
#Conexión a base de datos ----------------------------------------------
# Código para correr el servidor con el index de HTML.
conn= pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\brein\Documents\Codes\TaskBD\src\TASKBD.accdb")
#Se crea el cursor y se hace una consulta para pedir los datos
cursor = conn.cursor()
#Definir los titulos de cada columna de la lista
headings_Task = ("ID", "Descripción", "Estado")
#Rutas -----------------------------------------------------------------
#Index.


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
#Ruta para leer las tareas.
@app.route('/show-task')
def showTask():
    cursor.execute("SELECT * FROM Tareas") 
    data_Task=cursor.fetchall()
    return render_template('showTask.html', headings=headings_Task, data=data_Task)
#Ruta para agregar una nueva tarea.
@app.route('/new-task')
def newTask(): 
    return render_template('newTask.html')
#Ruta para marcar una tarea como completada
@app.route('/complete-task')
def completeTask():
    return render_template('completeTask.html')
#Ruta para eliminar una tarea
@app.route('/delete-task')
def deleteTask():
    return render_template('deleteTask.html')
#Conseguir datos de los formularios
@app.route('/get-new-task', methods=['POST'])
def getNewTask():
    if request.method == 'POST':
        taskDescription = request.form['task_Description']
        taskStatus = request.form['task_Status']
        # Establece la conexión a la base de datos
        cursorInsert = conn.cursor()
        # Ejecuta la consulta para insertar los datos
        cursorInsert.execute("INSERT INTO Tareas(Descripción, Estado) VALUES (?, ?)", (taskDescription, taskStatus))
        # Confirma la transacción y cierra la conexión
        conn.commit()
        cursorInsert.close()
        return render_template('taskSubmit.html')
    else:
        return render_template('taskError.html')
@app.route('/deleted-task', methods=['POST'])
def deletedTask():
    if request.method == 'POST':
        taskID = request.form['task_delete_ID']
        # Establece la conexión a la base de datos
        cursorDelete = conn.cursor()
        # Ejecuta la consulta SQL para insertar datos
        cursorDelete.execute("DELETE FROM Tareas WHERE ID=?",taskID)
        # Confirma la transacción y cierra la conexión
        conn.commit()
        cursorDelete.close()
        return render_template('taskSubmit.html')
    else:
        return render_template('taskError.html')

@app.route('/completed-task', methods=['POST'])
def completedTask():
    if request.method == 'POST':
        taskID = request.form['task_complete_ID']
        # Establece la conexión a la base de datos
        cursorCompleted = conn.cursor()
        # Ejecuta la consulta SQL para insertar datos
        cursorCompleted.execute("UPDATE Tareas SET Estado = ? WHERE ID = ?", 'Completado', taskID)
        # Confirma la transacción y cierra la conexión
        conn.commit()
        cursorCompleted.close()
        return render_template('taskSubmit.html')
    else:
        return render_template('taskError.html')
if __name__ == '__main__':
    app.run()



cursor.close()
conn.close()
from flask import Flask,render_template,request,session,redirect,url_for
import sqlite3
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "databases"
ALLOWED_EXTENSIONS={"db"}

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_path():
    return session.get("db_path","example.db")

def get_db_type():
    return session.get("db_type","sqlite3")
    
def execute_sql(query):
    db_type = get_db_type()
    
    if db_type == "sqlite3":
        DB_PATH = get_db_path()
        if not os.path.exists(DB_PATH):
            return {"status":"error","message":f"Databse not found at {DB_PATH}"}
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                results = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
                return {"status": "success", "headers": headers, "rows": results}
            else:
                conn.commit()
                return {"status": "success", "message": "Query executed successfully."}
        except Exception as e:
            return {"status":"error","message":str(e)}
        finally:
            conn.close()
            
    elif db_type == "mysql":
        try:
            conn = mysql.connector.connect(
                host = session.get("mysql_host","localhost"),
                user = session.get("mysql_user","root"),
                password = session.get("mysql_pass",""),
                database = session.get("mysql_db","")
            )
            cursor = conn.cursor()
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                results = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
                return {"status": "success", "headers": headers, "rows": results}
            else:
                conn.commit()
                return {"status": "success", "message": "Query executed successfully."}
        except Exception as e:
            return {"status":"error","message":str(e)}
        finally:
            conn.close
    return {"status": "error", "message": "Unsupported DB type"}
        
@app.route("/",methods=["GET","POST"])
def index():
    output = {}
    if request.method == "POST":
        query = request.form.get("query")
        output = execute_sql(query)
    return render_template("index.html",output=output,db_path=get_db_path(),db_type=get_db_type())

@app.route("/upload",methods=["POST"])
def upload():
    session["db_type"] = "sqlite3"
    if "db_file" not in request.files:
        return redirect(url_for("index"))
    
    file = request.files["db_file"]
    if file.filename == "":
        return redirect(url_for("index"))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER,filename)
        file.save(save_path)
        session["db_path"] = save_path
    
    return redirect(url_for("index"))

@app.route("/connect_mysql",methods=["POST"])
def connect_mysql():
    session["db_type"] = "mysql"
    session["mysql_host"] = request.form.get("host")
    session["mysql_user"] = request.form.get("user")
    session["mysql_pass"] = request.form.get("password")
    session["mysql_db"] = request.form.get("database")
    return redirect(url_for("index"))

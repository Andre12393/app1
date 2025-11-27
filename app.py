from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

usuarios = {}  # Base temporal en memoria

# -------------------- RUTAS --------------------

@app.route("/")
@app.route("/inicio")
def inicio():
    user = usuarios.get(session["email"]) if "email" in session else None
    return render_template("inicio.html", user=user)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        email = request.form["email"]
        if email in usuarios:
            return render_template("registro.html", error="El email ya está registrado")
        usuarios[email] = {
            "nombre": request.form.get("nombre"),
            "apellidos": request.form.get("apellidos"),
            "email": email,
            "password": generate_password_hash(request.form["password"]),
            "edad": request.form.get("edad"),
            "sexo": request.form.get("sexo"),
            "peso": request.form.get("peso"),
            "altura": request.form.get("altura"),
            "actividad": request.form.get("actividad"),
            "objetivo": request.form.get("objetivo"),
            "alergias": request.form.get("alergias"),
            "intolerancias": request.form.get("intolerancias"),
            "dieta": request.form.get("dieta"),
            "no_gusta": request.form.get("no_gusta"),
            "experiencia": request.form.get("experiencia")
        }
        session["email"] = email
        return redirect(url_for("perfil"))
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = usuarios.get(email)
        if user and check_password_hash(user["password"], password):
            session["email"] = email
            return redirect(url_for("perfil"))
        return render_template("login.html", error="Email o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("inicio"))

@app.route("/perfil")
def perfil():
    if "email" not in session:
        return redirect(url_for("login"))
    user = usuarios.get(session["email"])
    return render_template("perfil.html", user=user)

@app.route("/educacion")
def educacion():
    return render_template("educacion.html")

@app.route("/calculadoras")
def calculadoras():
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("calculadoras.html")

# Placeholders de cada calculadora
@app.route("/calculadora_imc", methods=["GET","POST"])
def calculadora_imc():
    if "email" not in session:
        return redirect(url_for("login"))
    imc = None
    categoria = ""
    if request.method=="POST":
        peso=float(request.form["peso"])
        altura=float(request.form["altura"])/100
        imc=round(peso/(altura**2),2)
        if imc<18.5: categoria="Bajo peso"
        elif imc<25: categoria="Normal"
        elif imc<30: categoria="Sobrepeso"
        else: categoria="Obesidad"
    return render_template("calculadora_imc.html", imc=imc, categoria=categoria)

@app.route("/calculadora_tmb", methods=["GET","POST"])
def calculadora_tmb():
    if "email" not in session:
        return redirect(url_for("login"))
    tmb = None
    if request.method=="POST":
        peso=float(request.form["peso"])
        altura=float(request.form["altura"])
        edad=int(request.form["edad"])
        sexo=request.form["sexo"]
        if sexo=="hombre": tmb=round(88.36+(13.4*peso)+(4.8*altura)-(5.7*edad))
        else: tmb=round(447.6+(9.2*peso)+(3.1*altura)-(4.3*edad))
    return render_template("calculadora_tmb.html", tmb=tmb)

@app.route("/calculadora_gct", methods=["GET","POST"])
def calculadora_gct():
    if "email" not in session:
        return redirect(url_for("login"))
    gct = None
    if request.method=="POST":
        tmb=float(request.form["tmb"])
        factor=float(request.form["actividad"])
        gct=round(tmb*factor)
    return render_template("calculadora_gct.html", gct=gct)

@app.route("/calculadora_peso_ideal", methods=["GET","POST"])
def calculadora_peso_ideal():
    if "email" not in session:
        return redirect(url_for("login"))
    peso_ideal=None
    if request.method=="POST":
        altura=float(request.form["altura"])
        sexo=request.form["sexo"]
        if sexo=="hombre": peso_ideal=round(50+0.9*(altura-152))
        else: peso_ideal=round(45.5+0.9*(altura-152))
    return render_template("calculadora_peso_ideal.html", peso_ideal=peso_ideal)

@app.route("/calculadora_macronutrientes", methods=["GET","POST"])
def calculadora_macronutrientes():
    if "email" not in session:
        return redirect(url_for("login"))
    macros=None
    if request.method=="POST":
        calorias=float(request.form["calorias"])
        p_pct=float(request.form["proteina"])
        g_pct=float(request.form["grasas"])
        c_pct=float(request.form["carbohidratos"])
        macros={
            "proteina": round(calorias*(p_pct/100)/4),
            "grasas": round(calorias*(g_pct/100)/9),
            "carbohidratos": round(calorias*(c_pct/100)/4)
        }
    return render_template("calculadora_macronutrientes.html", macros=macros)

@app.route("/analizador_recetas")
def analizador_recetas():
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template("analizador_recetas.html")

# -------------------- RUN --------------------
if __name__=="__main__":
    app.run(debug=True)

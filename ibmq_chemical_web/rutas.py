from ibmq_chemical_web import aplicacion
from flask import render_template, redirect


@aplicacion.route("/", methods=["GET"])
def index():
    return render_template("index.html", name="Alberto")


@aplicacion.route("/", methods=["POST"])
def indexa():
    return redirect("/")


from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)

# in-memory storage for warehouses
varastot = {}
id_counter = [0]


def parse_float(value, default=0.0):
    try:
        return float(value)
    except ValueError:
        return default


def get_next_id():
    id_counter[0] += 1
    return id_counter[0]


@app.route("/")
def index():
    return render_template("index.html", varastot=varastot)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nimi = request.form.get("nimi", "").strip()
        tilavuus = parse_float(request.form.get("tilavuus", "0"))
        alku_saldo = parse_float(request.form.get("alku_saldo", "0"))
        varasto = Varasto(tilavuus, alku_saldo)
        varastot[get_next_id()] = {"nimi": nimi, "varasto": varasto}
        return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/edit/<int:varasto_id>", methods=["GET", "POST"])
def edit(varasto_id):
    if varasto_id not in varastot:
        return redirect(url_for("index"))
    data = varastot[varasto_id]
    if request.method == "POST":
        handle_edit_action(data["varasto"], request.form)
        return redirect(url_for("edit", varasto_id=varasto_id))
    return render_template("edit.html", varasto_id=varasto_id, data=data)


def handle_edit_action(varasto, form):
    action = form.get("action")
    maara = parse_float(form.get("maara", "0"))
    if action == "lisaa":
        varasto.lisaa_varastoon(maara)
    elif action == "ota":
        varasto.ota_varastosta(maara)


@app.route("/delete/<int:varasto_id>", methods=["POST"])
def delete(varasto_id):
    if varasto_id in varastot:
        del varastot[varasto_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)

"""
app.py — Servidor Flask para FinanceOS
Gestión Financiera Personal con Sistema de Metas Conectado.

Rutas:
  GET  /                         → Dashboard principal
  POST /transactions/add         → Agregar transacción
  POST /transactions/delete/<id> → Eliminar transacción
  POST /goals/add                → Crear meta
  POST /goals/contribute/<id>    → Aportar a meta
  POST /goals/withdraw/<id>      → Retirar fondos de meta
  POST /goals/delete/<id>        → Eliminar meta
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import data as db

app = Flask(__name__)
app.secret_key = "finance_os_secret_2026"   # Necesario para usar flash messages


# ─────────────────────────────────────────────
#  DASHBOARD PRINCIPAL
# ─────────────────────────────────────────────
@app.route("/")
def index():
    state   = db.load_state()
    totals  = db.compute_totals(state)

    # Revertir lista de transacciones para mostrar más reciente primero
    transactions = list(reversed(state["transactions"]))

    return render_template(
        "index.html",
        totals=totals,
        transactions=transactions,
        goals=state["goals"],
    )


# ─────────────────────────────────────────────
#  TRANSACCIONES
# ─────────────────────────────────────────────
@app.route("/transactions/add", methods=["POST"])
def add_transaction():
    state       = db.load_state()
    totals      = db.compute_totals(state)

    tx_type     = request.form.get("type", "income")
    description = request.form.get("description", "").strip()
    category    = request.form.get("category", "General")

    try:
        amount = float(request.form.get("amount", 0))
    except ValueError:
        flash("error|Monto inválido. Por favor ingresa un número.", "flash")
        return redirect(url_for("index"))

    if not description:
        flash("warn|Por favor escribe una descripción.", "flash")
        return redirect(url_for("index"))

    if amount <= 0:
        flash("warn|El monto debe ser mayor a 0.", "flash")
        return redirect(url_for("index"))

    # Validar saldo para gastos
    if tx_type == "expense" and amount > totals["balance"]:
        flash("error|Saldo insuficiente para registrar este gasto.", "flash")
        return redirect(url_for("index"))

    db.add_transaction(state, tx_type, description, amount, category)
    db.save_state(state)

    label = "Ingreso" if tx_type == "income" else "Gasto"
    flash(f"success|{label} de ${amount:,.2f} agregado correctamente.", "flash")
    return redirect(url_for("index"))


@app.route("/transactions/delete/<tx_id>", methods=["POST"])
def delete_transaction(tx_id):
    state = db.load_state()
    found = db.delete_transaction(state, tx_id)
    if found:
        db.save_state(state)
        flash("info|Transacción eliminada.", "flash")
    else:
        flash("error|Transacción no encontrada.", "flash")
    return redirect(url_for("index"))


# ─────────────────────────────────────────────
#  METAS DE AHORRO
# ─────────────────────────────────────────────
@app.route("/goals/add", methods=["POST"])
def add_goal():
    state = db.load_state()
    name  = request.form.get("name", "").strip()
    emoji = request.form.get("emoji", "🎯").strip() or "🎯"

    try:
        target = float(request.form.get("target", 0))
    except ValueError:
        flash("error|Monto objetivo inválido.", "flash")
        return redirect(url_for("index"))

    if not name:
        flash("warn|Por favor escribe un nombre para la meta.", "flash")
        return redirect(url_for("index"))

    if target <= 0:
        flash("warn|El monto objetivo debe ser mayor a 0.", "flash")
        return redirect(url_for("index"))

    goal = db.add_goal(state, name, target, emoji)
    db.save_state(state)
    flash(f"success|Meta '{goal['name']}' creada exitosamente.", "flash")
    return redirect(url_for("index"))


@app.route("/goals/contribute/<goal_id>", methods=["POST"])
def contribute_goal(goal_id):
    state  = db.load_state()
    totals = db.compute_totals(state)

    try:
        amount = float(request.form.get("amount", 0))
    except ValueError:
        flash("error|Monto inválido.", "flash")
        return redirect(url_for("index"))

    success, msg = db.contribute_to_goal(state, goal_id, amount, totals["balance"])
    if success:
        db.save_state(state)
        flash(f"success|{msg}", "flash")
    else:
        flash(f"error|{msg}", "flash")
    return redirect(url_for("index"))


@app.route("/goals/withdraw/<goal_id>", methods=["POST"])
def withdraw_goal(goal_id):
    state = db.load_state()
    success, msg, _ = db.withdraw_from_goal(state, goal_id)
    if success:
        db.save_state(state)
        flash(f"info|{msg}", "flash")
    else:
        flash(f"warn|{msg}", "flash")
    return redirect(url_for("index"))


@app.route("/goals/delete/<goal_id>", methods=["POST"])
def delete_goal(goal_id):
    state = db.load_state()
    success, saved = db.delete_goal(state, goal_id)
    if success:
        db.save_state(state)
        note = f" (${saved:,.2f} devueltos al saldo)" if saved > 0 else ""
        flash(f"info|Meta eliminada{note}.", "flash")
    else:
        flash("error|Meta no encontrada.", "flash")
    return redirect(url_for("index"))


# ─────────────────────────────────────────────
#  ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  FinanceOS — Servidor iniciado")
    print("  Abre tu navegador en: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)

"""
data.py — Capa de persistencia de datos para FinanceOS
Guarda y carga el estado financiero en un archivo JSON local (finance_data.json).
"""
from __future__ import annotations   # Compatibilidad de type hints con Python 3.7-3.9

import json
import os
from datetime import datetime

# Ruta del archivo de datos
DATA_FILE = os.path.join(os.path.dirname(__file__), "finance_data.json")

# ─────────────────────────────────────────────
#  ESTRUCTURA INICIAL VACÍA
# ─────────────────────────────────────────────
def _empty_state() -> dict:
    """Retorna un estado financiero vacío."""
    return {
        "transactions": [],  # lista de dicts: {id, type, description, amount, category, date}
        "goals": []          # lista de dicts: {id, name, emoji, target, saved}
    }


# ─────────────────────────────────────────────
#  CARGAR ESTADO
# ─────────────────────────────────────────────
def load_state() -> dict:
    """
    Carga el estado desde finance_data.json.
    Si el archivo no existe o está corrupto, retorna estado vacío.
    """
    if not os.path.exists(DATA_FILE):
        return _empty_state()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Validar estructura mínima
        if isinstance(data.get("transactions"), list) and isinstance(data.get("goals"), list):
            return data
    except (json.JSONDecodeError, IOError):
        pass
    return _empty_state()


# ─────────────────────────────────────────────
#  GUARDAR ESTADO
# ─────────────────────────────────────────────
def save_state(state: dict) -> bool:
    """
    Guarda el estado completo en finance_data.json.
    Retorna True si fue exitoso, False en caso de error.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"[ERROR] No se pudo guardar el estado: {e}")
        return False


# ─────────────────────────────────────────────
#  TOTALES CALCULADOS
# ─────────────────────────────────────────────
def compute_totals(state: dict) -> dict:
    """
    Calcula los totales financieros desde el estado.

    Fórmula de Saldo Disponible:
        saldo = ingresos_totales - gastos_totales - total_ahorrado_en_metas
    """
    transactions = state.get("transactions", [])
    goals        = state.get("goals", [])

    income  = sum(t["amount"] for t in transactions if t.get("type") == "income")
    expense = sum(t["amount"] for t in transactions if t.get("type") == "expense")
    saved   = sum(g.get("saved", 0) for g in goals)
    balance = income - expense - saved

    income_count  = sum(1 for t in transactions if t.get("type") == "income")
    expense_count = sum(1 for t in transactions if t.get("type") == "expense")

    return {
        "income":         round(income, 2),
        "expense":        round(expense, 2),
        "goals_saved":    round(saved, 2),
        "balance":        round(balance, 2),
        "income_count":   income_count,
        "expense_count":  expense_count,
        "goals_count":    len(goals),
    }


# ─────────────────────────────────────────────
#  HELPERS DE TRANSACCIONES
# ─────────────────────────────────────────────
def add_transaction(state: dict, tx_type: str, description: str,
                    amount: float, category: str) -> dict:
    """Agrega una nueva transacción al estado y la retorna."""
    tx = {
        "id":          f"tx_{int(datetime.now().timestamp() * 1000)}",
        "type":        tx_type,          # 'income' | 'expense'
        "description": description.strip(),
        "amount":      round(float(amount), 2),
        "category":    category,
        "date":        datetime.now().isoformat()
    }
    state["transactions"].append(tx)
    return tx


def delete_transaction(state: dict, tx_id: str) -> bool:
    """Elimina una transacción por ID. Retorna True si se encontró."""
    before = len(state["transactions"])
    state["transactions"] = [t for t in state["transactions"] if t["id"] != tx_id]
    return len(state["transactions"]) < before


# ─────────────────────────────────────────────
#  HELPERS DE METAS
# ─────────────────────────────────────────────
def add_goal(state: dict, name: str, target: float, emoji: str = "🎯") -> dict:
    """Crea una nueva meta de ahorro."""
    goal = {
        "id":     f"goal_{int(datetime.now().timestamp() * 1000)}",
        "name":   name.strip(),
        "emoji":  emoji.strip() or "🎯",
        "target": round(float(target), 2),
        "saved":  0.0
    }
    state["goals"].append(goal)
    return goal


def contribute_to_goal(state: dict, goal_id: str, amount: float,
                        available_balance: float) -> tuple[bool, str]:
    """
    Aporta `amount` a la meta indicada si hay saldo suficiente.
    Retorna (éxito: bool, mensaje: str).
    """
    goal = next((g for g in state["goals"] if g["id"] == goal_id), None)
    if not goal:
        return False, "Meta no encontrada."

    amount = round(float(amount), 2)
    if amount <= 0:
        return False, "El monto debe ser mayor a 0."
    if amount > available_balance:
        return False, "Saldo insuficiente para este aporte."

    # Limitar al objetivo
    remaining = round(goal["target"] - goal["saved"], 2)
    actual    = min(amount, remaining)
    goal["saved"] = round(goal["saved"] + actual, 2)
    return True, f"Aporte de ${actual:.2f} registrado."


def withdraw_from_goal(state: dict, goal_id: str) -> tuple[bool, str, float]:
    """
    Retira todos los fondos ahorrados de una meta al saldo disponible.
    Retorna (éxito, mensaje, monto_retirado).
    """
    goal = next((g for g in state["goals"] if g["id"] == goal_id), None)
    if not goal:
        return False, "Meta no encontrada.", 0.0
    if goal["saved"] <= 0:
        return False, "La meta no tiene fondos para retirar.", 0.0

    withdrew      = goal["saved"]
    goal["saved"] = 0.0
    return True, f"${withdrew:.2f} devuelto al saldo disponible.", withdrew


def delete_goal(state: dict, goal_id: str) -> tuple[bool, float]:
    """
    Elimina una meta. Los fondos ahorrados vuelven al saldo automáticamente.
    Retorna (éxito, monto_que_era_ahorrado).
    """
    goal = next((g for g in state["goals"] if g["id"] == goal_id), None)
    if not goal:
        return False, 0.0
    saved = goal["saved"]
    state["goals"] = [g for g in state["goals"] if g["id"] != goal_id]
    return True, saved

/**
 * app.js — Lógica cliente para FinanceOS (Flask version)
 * Gestiona: toggle de tipo de transacción, filtros de historial,
 * modal de aportaciones a metas, toasts desde flash messages, y fecha del header.
 */

// ═══════════════════════════════════════════════════════
//  TOGGLE TIPO DE TRANSACCIÓN (Ingreso / Gasto)
// ═══════════════════════════════════════════════════════
function setTxType(type) {
    document.getElementById("tx-type-hidden").value = type;

    const btnIncome = document.getElementById("btn-type-income");
    const btnExpense = document.getElementById("btn-type-expense");

    if (type === "income") {
        btnIncome.className = "type-btn active-income";
        btnExpense.className = "type-btn";
    } else {
        btnIncome.className = "type-btn";
        btnExpense.className = "type-btn active-expense";
    }
}

// ═══════════════════════════════════════════════════════
//  FILTRO DE HISTORIAL (Todos / Ingresos / Gastos)
// ═══════════════════════════════════════════════════════
function setFilter(filter, tabEl) {
    // Actualizar tabs activos
    document.querySelectorAll(".filter-tab").forEach(t => t.classList.remove("active"));
    tabEl.classList.add("active");

    // Mostrar / ocultar items
    const items = document.querySelectorAll(".tx-item");
    items.forEach(item => {
        const itemType = item.getAttribute("data-type");
        if (filter === "all" || itemType === filter) {
            item.classList.remove("hidden");
        } else {
            item.classList.add("hidden");
        }
    });
}

// ═══════════════════════════════════════════════════════
//  MODAL: APORTAR A META
// ═══════════════════════════════════════════════════════
function openAporte(goalId, goalName, saved, target) {
    const modal = document.getElementById("aporte-modal");
    const form = document.getElementById("form-aporte");

    // Establecer acción del formulario al goal específico
    form.action = `/goals/contribute/${goalId}`;

    // Rellenar info del modal
    document.getElementById("modal-goal-name").textContent = goalName;
    document.getElementById("modal-goal-info").textContent =
        `Ahorrado: $${parseFloat(saved).toLocaleString("es-MX", { minimumFractionDigits: 2 })} ` +
        `/ $${parseFloat(target).toLocaleString("es-MX", { minimumFractionDigits: 2 })}`;

    // Limpiar input y abrir
    document.getElementById("aporte-amount").value = "";
    modal.classList.add("open");
    setTimeout(() => document.getElementById("aporte-amount").focus(), 120);
}

function closeModal() {
    document.getElementById("aporte-modal").classList.remove("open");
}

// Cerrar con clic en el fondo
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("aporte-modal").addEventListener("click", e => {
        if (e.target === e.currentTarget) closeModal();
    });
});

// Cerrar con Escape, confirmar con Enter dentro del modal
document.addEventListener("keydown", e => {
    const modalOpen = document.getElementById("aporte-modal").classList.contains("open");
    if (e.key === "Escape" && modalOpen) closeModal();
    if (e.key === "Enter" && modalOpen) {
        e.preventDefault();
        document.getElementById("form-aporte").submit();
    }
});

// ═══════════════════════════════════════════════════════
//  TOASTS (desde flash messages del servidor)
// ═══════════════════════════════════════════════════════
const TOAST_COLORS = {
    success: "var(--accent-green)",
    error: "var(--accent-red)",
    warn: "var(--accent-gold)",
    info: "var(--accent-blue)"
};

function showToast(msg, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.style.borderLeft = `3px solid ${TOAST_COLORS[type] || TOAST_COLORS.info}`;
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3300);
}

// Leer flash messages renderizados por Jinja2 y mostrarlos como toast
function processFlashMessages() {
    const queue = document.getElementById("flash-queue");
    if (!queue) return;

    queue.querySelectorAll("span").forEach(el => {
        const raw = el.textContent.trim();          // formato: "type|message"
        const sepIdx = raw.indexOf("|");
        const type = sepIdx > -1 ? raw.slice(0, sepIdx) : "info";
        const message = sepIdx > -1 ? raw.slice(sepIdx + 1) : raw;
        showToast(message, type);
    });
}

// ═══════════════════════════════════════════════════════
//  FECHA EN HEADER
// ═══════════════════════════════════════════════════════
function updateHeaderDate() {
    const el = document.getElementById("header-date");
    if (!el) return;
    el.textContent = new Date().toLocaleDateString("es-MX", {
        weekday: "long", year: "numeric", month: "long", day: "numeric"
    });
}

// ═══════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
    updateHeaderDate();
    processFlashMessages();
});

# FinanceOS — Gestión Financiera Personal

> **Dashboard web con Flask + Python para el control de ingresos, gastos y metas de ahorro.**  
> Los datos se persisten localmente en `finance_data.json`.

---

## 🗂 Estructura del Proyecto

```
Pagina Finanzas/
├── app.py                ← Servidor Flask (rutas y lógica HTTP)
├── data.py               ← Capa de datos (lectura/escritura JSON)
├── finance_data.json     ← Base de datos local (creada automáticamente)
├── run_website.bat       ← Lanzador con un doble clic
├── README.md             ← Este archivo
│
├── templates/
│   └── index.html        ← Plantilla Jinja2 (dashboard principal)
│
├── static/
│   ├── css/
│   │   └── style.css     ← Sistema de diseño (dark mode)
│   └── js/
│       └── app.js        ← Lógica cliente (modal, filtros, toasts)
│
└── __pycache__/          ← Caché de Python (generado automáticamente)
```

---

## 🚀 Cómo Ejecutar

### Opción 1 — Doble clic (recomendado)
Haz doble clic en **`run_website.bat`**.  
El script instala Flask si hace falta y abre el servidor.

Luego abre tu navegador en:  
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### Opción 2 — Terminal manual
```bash
# 1. Instalar Flask (solo la primera vez)
pip install flask

# 2. Iniciar servidor
python app.py
```

---

## ⚙️ Requisitos

| Requisito | Versión mínima |
|-----------|----------------|
| Python    | 3.9+           |
| Flask     | 3.x            |

---

## 💡 Funcionalidades

| Módulo | Descripción |
|--------|-------------|
| **Dashboard KPI** | Saldo Disponible · Ingresos · Gastos · Total en Metas |
| **Saldo Inteligente** | `Ingresos − Gastos − Σ(ahorrado en metas)` |
| **Transacciones** | Registrar ingresos y gastos con categoría · Filtrar historial · Eliminar |
| **Metas de Ahorro** | Crear metas con emoji y objetivo · Barra de progreso · Badge "Completada" |
| **Aportar a Meta** | Modal con validación de saldo suficiente |
| **Retirar de Meta** | Devuelve el dinero ahorrado al saldo disponible |
| **Persistencia** | JSON local (`finance_data.json`) — datos permanentes entre sesiones |
| **Notificaciones** | Toast notifications con código de colores para cada acción |

---

## 📊 Fórmula de Saldo Disponible

```
Saldo Disponible = Σ Ingresos − Σ Gastos − Σ (meta.saved)
```

El sistema **nunca permite**:
- Registrar un gasto mayor al saldo disponible
- Aportar a una meta más de lo disponible en el saldo

---

## 🎨 Diseño

- **Modo oscuro** completo (`#0d0f14` base)
- Paleta de acentos: Azul · Verde · Rojo · Dorado · Púrpura
- Tipografía: **Inter** (Google Fonts)
- Micro-animaciones CSS en cards, progress bars y modal
- Totalmente responsivo (mobile-friendly)

---

## 🔧 Personalización

### Agregar categorías
En `templates/index.html`, busca el `<select id="tx-category">` y agrega `<option>` según necesites.

### Cambiar puerto
En `app.py`, modifica la última línea:
```python
app.run(debug=True, host="127.0.0.1", port=5000)
```

### Acceder desde otra PC en la red local
Cambia `host` a `"0.0.0.0"` y accede con la IP local de tu máquina.

---

*FinanceOS · 2026*

# app.py - Sistema Experto: orientación rápida en infecciones respiratorias agudas
import streamlit as st

SINTOMAS = {
    "fiebre": "Fiebre mayor o igual a 38 °C",
    "tos": "Tos",
    "dolor_garganta": "Dolor de garganta",
    "congestion": "Congestión nasal",
    "estornudos": "Estornudos frecuentes",
    "dolor_muscular": "Dolor muscular o corporal",
    "fatiga": "Fatiga intensa",
    "perdida_olfato": "Pérdida de olfato o gusto",
    "dif_respirar": "Dificultad para respirar",
    "dolor_pecho": "Dolor en el pecho al respirar",
}

# Base de reglas: (id, condiciones que deben ser verdaderas, condiciones que deben ser falsas, conclusión)
REGLAS = [
    ("R1", ["dif_respirar", "fiebre"], [], "ALERTA: posible neumonía"),
    ("R2", ["dolor_pecho", "tos", "fiebre"], [], "ALERTA: posible neumonía"),
    ("R3", ["fiebre", "dolor_muscular", "fatiga", "tos"], [], "Cuadro compatible con gripe (influenza)"),
    ("R4", ["perdida_olfato", "tos"], [], "Sospecha de COVID-19: realizar prueba"),
    ("R5", ["perdida_olfato", "fiebre"], [], "Sospecha de COVID-19: realizar prueba"),
    ("R6", ["congestion", "estornudos", "dolor_garganta"], ["fiebre"], "Cuadro compatible con resfriado común"),
]

def inferir(hechos):
    """Encadenamiento hacia adelante con principio de refracción."""
    ejecutadas, conclusiones = [], []
    for rid, si, no, concl in REGLAS:
        if all(hechos.get(s) for s in si) and not any(hechos.get(n) for n in no):
            ejecutadas.append(rid)
            if concl not in conclusiones:
                conclusiones.append(concl)
    return conclusiones, ejecutadas

st.title("Sistema Experto: infecciones respiratorias agudas")
st.caption("Herramienta académica de orientación. No reemplaza una consulta médica.")
hechos = {k: st.checkbox(v) for k, v in SINTOMAS.items()}

if st.button("Diagnosticar"):
    conclusiones, reglas = inferir(hechos)
    if not conclusiones:
        st.info("Con los síntomas ingresados no se activó ninguna regla de la base de conocimiento.")
    for c in conclusiones:
        (st.error if c.startswith("ALERTA") else st.success)(c)
    st.write("Reglas activadas:", ", ".join(reglas) if reglas else "ninguna")
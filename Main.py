import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

df = pd.read_csv('Tipo de Dor de Cabeça.csv')
X = df.drop('Tipo de Dor de Cabeça', axis=1)
y = df['Tipo de Dor de Cabeça']

label_encoder_dor = LabelEncoder()
y_encoded = label_encoder_dor.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

def fazer_previsao():
    input_usuario = {}
    for feature, var in zip(inputs, input_vars):
        input_usuario[feature] = [var.get()]

    input_usuario_df = pd.DataFrame(input_usuario)
    probabilidades = clf.predict_proba(input_usuario_df)[0]
    tipos_dor = label_encoder_dor.inverse_transform(clf.classes_)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(probabilidades, labels=tipos_dor, autopct='%1.1f%%', startangle=140)
    ax.set_title('Probabilidade de Tipos de Dor de Cabeça')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Classificador de Dor de Cabeça")
root.geometry("500x700")

style = ttk.Style()
style.theme_use('clam')

style.configure("TLabel", font=("Helvetica", 12))
style.configure("TCheckbutton", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, 'bold'), background='#4CAF50', foreground='white')
style.map("TButton", background=[('active', '#45a049')])

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(main_frame, text="Classificador de Dor de Cabeça", font=("Helvetica", 16, 'bold'))
title_label.pack(pady=10)

description_label = ttk.Label(main_frame, text="Por favor, responda as seguintes perguntas sobre seus sintomas:", wraplength=450, justify="center")
description_label.pack(pady=10)

canvas = tk.Canvas(main_frame)
scroll_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

scroll_frame = ttk.Frame(canvas)
scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

inputs = [
    "Dor constante e não pulsátil",
    "Sensação de pressão ou aperto",
    "Dor pulsátil ou latejante",
    "Dor moderada a severa",
    "Sensibilidade à luz",
    "Sensibilidade ao som",
    "Náusea/vômito",
    "Aura (distúrbios visuais)",
    "Dor intensa e penetrante",
    "Episódios em grupos (salvas)",
    "Vermelhidão e lacrimejamento no olho",
    "Congestão ou corrimento nasal",
    "Agitação/inquietação",
    "Dor e pressão na testa e maçãs do rosto",
    "Febre",
    "Congestão nasal",
    "Secreção nasal",
    "Piora ao inclinar/ deitar",
    "Uso regular e prolongado de medicamentos",
    "Surda e persistente",
    "Irritabilidade",
    "Dificuldade de concentração",
    "Mudanças hormonais",
    "Lesão na cabeça",
    "Duração: semanas ou meses após trauma"
]

input_vars = [tk.IntVar() for _ in inputs]

grouped_inputs = [
    ("Características Gerais", inputs[:7]),
    ("Sintomas Visuais e Auditivos", inputs[7:10]),
    ("Sintomas Nasais", inputs[10:12]),
    ("Outros Sintomas", inputs[12:]),
]

for group_name, group_inputs in grouped_inputs:
    group_frame = ttk.LabelFrame(scroll_frame, text=group_name, padding="10")
    group_frame.pack(fill="x", expand=True, pady=5)

    for feature in group_inputs:
        var = input_vars[inputs.index(feature)]  # Obter a variável IntVar correspondente
        label = ttk.Label(group_frame, text=feature)
        label.pack(anchor="w", pady=2)
        check = ttk.Checkbutton(group_frame, variable=var)
        check.pack(anchor="w", pady=2)

button = ttk.Button(main_frame, text="Fazer Previsão", command=fazer_previsao)
button.pack(pady=10)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

root.mainloop()

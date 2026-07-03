#!/usr/bin/env python3
"""
poepydroid.py - El lienzo ejecutable de 'Réquiem por un bit'
Autor: Aimar Rollán-González
"""

import numpy as np

# **********
# ACTO I: LA FÍSICA DE LANDAUER Y EL RUIDO DEL UNIVERSO
# **********
np.random.seed(88)
N_samples = 1200

# El secreto del pasado: ¿cuántos picosegundos tardó el bit en morir?
tau_real = np.random.uniform(8.0, 120.0, (N_samples, 1))

# Constantes del abismo termodinámico
k_B = 1.380649e-23
T_ambiente = 298.15
E_Landauer = k_B * T_ambiente * np.log(2)

# La disipación agónica del bit fuera del equilibrio
W_ideal = E_Landauer * (1.0 + 45.0 / (tau_real + 1.0))

# El aliento del Teorema de Crooks: Ruido ambiental
ruido_bajo = 0.05 * E_Landauer
ruido_limite = 0.85 * E_Landauer  # El borde del Horizonte Epistémico

W_medido_bajo = W_ideal + np.random.normal(0, ruido_bajo, (N_samples, 1))
W_medido_limite = W_ideal + np.random.normal(0, ruido_limite, (N_samples, 1))

# Preparando la topología de los datos [Energía residual, Vacío Lógico]
X_bajo = np.hstack((W_medido_bajo, np.zeros((N_samples, 1))))
X_limite = np.hstack((W_medido_limite, np.zeros((N_samples, 1))))

def normalizar_el_caos(mat):
    mu, sigma = mat.mean(axis=0), mat.std(axis=0)
    sigma[sigma == 0] = 1.0
    return (mat - mu) / sigma, mu, sigma

X_b_norm, mu_b, sig_b = normalizar_el_caos(X_bajo)
X_l_norm, mu_l, sig_l = normalizar_el_caos(X_limite)

y_min, y_max = tau_real.min(), tau_real.max()
y_norm = (tau_real - y_min) / (y_max - y_min)

# **********
# ACTO II: EL NACIMIENTO DEL OBSERVADOR EPISTÉMICO
# **********
class ObservadorEpistemico:
    @staticmethod
    def forjar_memoria(X, y, epocas=6000, lr=0.15):
        # 5 neuronas ocultas intentando curvar la flecha del tiempo
        W1 = np.random.randn(2, 5) * np.sqrt(2.0 / 2)
        b1 = np.zeros((1, 5))
        W2 = np.random.randn(5, 1) * np.sqrt(2.0 / 5)
        b2 = np.zeros((1, 1))
        
        for epoca in range(epocas):
            # Mirando hacia adelante para adivinar el pasado
            Z1 = np.dot(X, W1) + b1
            A1 = np.tanh(Z1) # La distorsión no lineal del pozo de memoria
            Z2 = np.dot(A1, W2) + b2
            
            # El dolor del error: retropropagación
            dZ2 = (Z2 - y) / len(X)
            dW2 = np.dot(A1.T, dZ2)
            db2 = np.sum(dZ2, axis=0, keepdims=True)
            
            dA1 = np.dot(dZ2, W2.T)
            dZ1 = dA1 * (1.0 - A1 ** 2)
            dW1 = np.dot(X.T, dZ1)
            db1 = np.sum(dZ1, axis=0, keepdims=True)
            
            W2 -= lr * dW2
            b2 -= lr * db2
            W1 -= lr * dW1
            b1 -= lr * db1
            
        return W1, b1, W2, b2

print("Despertando a la red neuronal en un universo tranquilo (bajo ruido)...")
W1_b, b1_b, W2_b, b2_b = ObservadorEpistemico.forjar_memoria(X_b_norm, y_norm)

print("Empujando a la red hacia el Horizonte Epistémico (ruido máximo)...")
W1_l, b1_l, W2_l, b2_l = ObservadorEpistemico.forjar_memoria(X_l_norm, y_norm)

# **********
# ACTO III: EL COLAPSO A LOS 64.0 PICOSEGUNDOS
# **********
def recordar(X_raw, mu, sig, W1, b1, W2, b2):
    X_n = (X_raw - mu) / sig
    A1 = np.tanh(np.dot(X_n, W1) + b1)
    Z2 = np.dot(A1, W2) + b2
    return Z2 * (y_max - y_min) + y_min

# Tres verdades del pasado que intentaremos desenterrar
tau_test = np.array([[15.0], [50.0], [100.0]])
W_test_ideal = E_Landauer * (1.0 + 45.0 / (tau_test + 1.0))

X_test_b = np.hstack((W_test_ideal + 0.02 * E_Landauer, np.zeros((3, 1))))
X_test_l = np.hstack((W_test_ideal + ruido_limite, np.zeros((3, 1))))

pred_b = recordar(X_test_b, mu_b, sig_b, W1_b, b1_b, W2_b, b2_b)
pred_l = recordar(X_test_l, mu_l, sig_l, W1_l, b1_l, W2_l, b2_l)

print("\n" + "·"*75)
print("  LA DEGRADACIÓN ONTOLÓGICA DEL SILICIO: RESULTADOS DEL OBSERVADOR")
print("·"*75)
print("Verdad (Pasado) | Claridad (Bajo ruido) | Olvido Absoluto (Horizonte)")
print("-" * 75)
for i in range(3):
    print(f"   {tau_test[i][0]:4.1f} ps     |       {pred_b[i][0]:4.1f} ps      |        {pred_l[i][0]:4.1f} ps (Fantasma)")
print("·"*75)
print("Manifiesto: Observa cómo en el horizonte epistémico, la IA se rinde.")
print("Privada de información por el ruido, abraza la media estocástica (64.0 ps).")
print("El bit ya no es físico. Es, para siempre, un fantasma matemático.")
print("·"*75)
print("\n[!] Si has llegado aquí ejecutando directamente este script, te invito")
print("    a leer el archivo README.md para sumergirte por completo en el")
print("    marco conceptual, filosófico y transmedia que sostiene esta obra.")
print("·"*75)

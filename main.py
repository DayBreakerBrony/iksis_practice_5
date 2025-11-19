import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

try:
    n = int(os.getenv('N', 5))
except (ValueError, TypeError):
    n = 5 

print(f"Используется индивидуальный номер: {n}")

# ============================
# ПЕРВАЯ ФОРМУЛА ЭРЛАНГА (Erlang B)
# ============================

def erlang_b_recursive(E, m):
    if m == 0:
        return 1.0
    return (E * erlang_b_recursive(E, m-1)) / (m + E * erlang_b_recursive(E, m-1))

def erlang_b(E, m):
    inv_B = 1.0
    for i in range(1, m + 1):
        inv_B = 1.0 + (i / E) * inv_B
    return 1.0 / inv_B

# ============================
# ВТОРАЯ ФОРМУЛА ЭРЛАНГА (Erlang C)
# ============================

def erlang_c(E, m):
    if E >= m:
        return 1.0
    B = erlang_b(E, m)
    return B / (1 - (E/m) * (1 - B))

def avg_queue_length(E, m):
    if E >= m:
        return float('inf')
    C = erlang_c(E, m)
    return (E * C) / (m - E)

# ============================
# ПОСТРОЕНИЕ ГРАФИКОВ
# ============================

def plot_erlang_b_vs_intensity():
    """График 1.2: Зависимость вероятности блокировки от интенсивности нагрузки"""
    E_values = [i * 0.1 for i in range(1, 100)]
    pb_values = [erlang_b(E, 2 * n) for E in E_values]

    plt.figure(figsize=(10, 5))
    plt.plot(E_values, pb_values, label=f'm = {2*n}')
    plt.xlabel('Интенсивность нагрузки (E)')
    plt.ylabel('Вероятность блокировки')
    plt.title('Зависимость вероятности блокировки от интенсивности нагрузки')
    plt.grid(True)
    plt.legend()
    plt.savefig('erlang_b_vs_intensity.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_erlang_b_vs_servers():
    """График 1.3: Зависимость вероятности блокировки от числа устройств"""
    m_values = list(range(1, 21))
    pb_values_m = [erlang_b(n, m) for m in m_values]

    plt.figure(figsize=(10, 5))
    plt.plot(m_values, pb_values_m, label=f'E = {n}')
    plt.xlabel('Число обслуживающих устройств (m)')
    plt.ylabel('Вероятность блокировки')
    plt.title('Зависимость вероятности блокировки от числа устройств')
    plt.grid(True)
    plt.legend()
    plt.savefig('erlang_b_vs_servers.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_erlang_c_vs_intensity():
    """График 2.2: Зависимость вероятности ожидания и длины очереди от интенсивности"""
    E_values_c = [i * 0.1 for i in range(1, int(2*n*0.9))]  # A < V
    pw_values = [erlang_c(E, 2 * n) for E in E_values_c]
    lq_values = [avg_queue_length(E, 2 * n) for E in E_values_c]

    plt.figure(figsize=(10, 5))
    plt.plot(E_values_c, pw_values, label='Вероятность ожидания')
    plt.plot(E_values_c, lq_values, label='Средняя длина очереди')
    plt.xlabel('Интенсивность нагрузки (E)')
    plt.ylabel('Значение')
    plt.title('Зависимость вероятности ожидания и длины очереди от интенсивности нагрузки')
    plt.grid(True)
    plt.legend()
    plt.savefig('erlang_c_vs_intensity.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_erlang_c_vs_servers():
    """График 2.3: Зависимость вероятности ожидания и длины очереди от числа устройств"""
    m_values_c = list(range(n + 1, 21))  # m > E
    pw_values_m = [erlang_c(n, m) for m in m_values_c]
    lq_values_m = [avg_queue_length(n, m) for m in m_values_c]

    plt.figure(figsize=(10, 5))
    plt.plot(m_values_c, pw_values_m, label='Вероятность ожидания')
    plt.plot(m_values_c, lq_values_m, label='Средняя длина очереди')
    plt.xlabel('Число обслуживающих устройств (m)')
    plt.ylabel('Значение')
    plt.title('Зависимость вероятности ожидания и длины очереди от числа устройств')
    plt.grid(True)
    plt.legend()
    plt.savefig('erlang_c_vs_servers.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_erlang_b_vs_intensity()
    plot_erlang_b_vs_servers()
    plot_erlang_c_vs_intensity()
    plot_erlang_c_vs_servers()
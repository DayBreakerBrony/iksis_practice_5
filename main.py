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
# ПЕРВАЯ ФОРМУЛА ЭРЛАНГА
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
# ВТОРАЯ ФОРМУЛА ЭРЛАНГА
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
    start_m = 1
    end_m = max(n * 2, 21)
    
    m_values = list(range(start_m, end_m + 1))
    pb_values_m = [erlang_b(n, m) for m in m_values]

    plt.figure(figsize=(10, 5))
    plt.plot(m_values, pb_values_m, label=f'E = {n}')
    plt.xlabel('Число обслуживающих устройств (m)')
    plt.ylabel('Вероятность блокировки')
    plt.title(f'Зависимость вероятности блокировки от числа устройств (n={n})')
    plt.grid(True)
    plt.legend()
    plt.savefig('erlang_b_vs_servers.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_erlang_c_vs_intensity():
    m = 2 * n
    min_intensity = 0.1 * m
    max_intensity = 0.95 * m

    E_values = [min_intensity + i * (max_intensity - min_intensity) / 200 for i in range(200)]
    
    pw_values = [erlang_c(E, m) for E in E_values]
    lq_values = [avg_queue_length(E, m) for E in E_values]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    ax1.semilogy(E_values, pw_values, 'b-', linewidth=2, label='Вероятность ожидания')
    ax1.set_xlabel('Интенсивность нагрузки (E)')
    ax1.set_ylabel('Вероятность ожидания (лог. шкала)')
    ax1.set_title(f'Вероятность ожидания от интенсивности нагрузки\n(m={m})')
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    ax1.legend()
    
    ax2.plot(E_values, lq_values, 'r-', linewidth=2, label='Средняя длина очереди')
    ax2.set_xlabel('Интенсивность нагрузки (E)')
    ax2.set_ylabel('Средняя длина очереди')
    ax2.set_title(f'Средняя длина очереди от интенсивности нагрузки\n(m={m})')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('erlang_c_vs_intensity.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_erlang_c_vs_servers():

    start_m = n + 1
    end_m = max(n * 2, 50)
    
    m_values_c = list(range(start_m, end_m + 1))
    
    print(f"Диапазон m: от {start_m} до {end_m}")
    
    pw_values_m = [erlang_c(n, m) for m in m_values_c]
    lq_values_m = [avg_queue_length(n, m) for m in m_values_c]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    ax1.semilogy(m_values_c, pw_values_m, 'b-', linewidth=2, label='Вероятность ожидания')
    ax1.set_xlabel('Число обслуживающих устройств (m)')
    ax1.set_ylabel('Вероятность ожидания (лог. шкала)')
    ax1.set_title(f'Вероятность ожидания от числа устройств\n(n={n})')
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    ax1.legend()
    
    ax2.plot(m_values_c, lq_values_m, 'r-', linewidth=2, label='Средняя длина очереди')
    ax2.set_xlabel('Число обслуживающих устройств (m)')
    ax2.set_ylabel('Средняя длина очереди')
    ax2.set_title(f'Средняя длина очереди от числа устройств\n(n={n})')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('erlang_c_vs_servers.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_erlang_b_vs_intensity()
    plot_erlang_b_vs_servers()
    plot_erlang_c_vs_intensity()
    plot_erlang_c_vs_servers()
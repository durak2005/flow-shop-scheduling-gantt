import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def calculate_completion_times(sequence, processing_times):
    """
    Belirli bir iş sırası için her işin her makinedeki tamamlanma süresini hesaplar.
    processing_times: {job_id: [m1_time, m2_time, ...]}
    """
    n_machines = len(next(iter(processing_times.values())))
    n_jobs = len(sequence)
    c_matrix = [[0] * n_machines for _ in range(n_jobs)]
    
    for i, job in enumerate(sequence):
        for m in range(n_machines):
            p = processing_times[job][m]
            if i == 0 and m == 0:
                c_matrix[i][m] = p
            elif i == 0:
                c_matrix[i][m] = c_matrix[i][m - 1] + p
            elif m == 0:
                c_matrix[i][m] = c_matrix[i - 1][m] + p
            else:
                c_matrix[i][m] = max(c_matrix[i - 1][m], c_matrix[i][m - 1]) + p
                
    return c_matrix

def neh_algorithm(processing_times):
    """
    Makespan minimize etmek için NEH sezgisel algoritması.
    """
    # 1. Adım: Toplam işlem süresine göre azalan sırada diz
    total_times = {job: sum(times) for job, times in processing_times.items()}
    sorted_jobs = sorted(total_times.keys(), key=lambda j: total_times[j], reverse=True)
    
    current_seq = [sorted_jobs[0]]
    
    # 2. Adım: Sırayla işleri en iyi araya ekleme mantığıyla yerleştir
    for job in sorted_jobs[1:]:
        best_seq = None
        best_makespan = float('inf')
        
        for pos in range(len(current_seq) + 1):
            candidate_seq = current_seq[:pos] + [job] + current_seq[pos:]
            c_mat = calculate_completion_times(candidate_seq, processing_times)
            makespan = c_mat[-1][-1]
            
            if makespan < best_makespan:
                best_makespan = makespan
                best_seq = candidate_seq
                
        current_seq = best_seq
        
    return current_seq

def plot_gantt(sequence, processing_times, machine_names):
    """
    Çizelgeleme sonucunu görselleştiren Gantt şeması.
    """
    n_machines = len(machine_names)
    colors = plt.cm.tab10.colors
    c_matrix = calculate_completion_times(sequence, processing_times)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, job in enumerate(sequence):
        color = colors[job % len(colors)]
        for m in range(n_machines):
            end_t = c_matrix[i][m]
            duration = processing_times[job][m]
            start_t = end_t - duration
            
            ax.barh(m, duration, left=start_t, align='center', 
                    color=color, edgecolor='black', alpha=0.85)
            ax.text(start_t + duration / 2, m, f"İş {job}", 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=9)

    ax.set_yticks(range(n_machines))
    ax.set_yticklabels(machine_names, fontsize=11, fontweight='medium')
    ax.set_xlabel("Zaman (Saat / Birim)", fontsize=11)
    ax.set_title(f"NEH Çizelgeleme Sonucu (Makespan: {c_matrix[-1][-1]} birim)", fontsize=13, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig("flow_shop_gantt.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    # Örnek veri seti: 5 iş, 3 operasyon/makine
    sample_jobs = {
        1: [4, 7, 3],
        2: [2, 5, 8],
        3: [6, 2, 4],
        4: [3, 6, 2],
        5: [5, 4, 6]
    }
    machines = ["Kesim İstasyonu", "İşleme İstasyonu", "Montaj İstasyonu"]
    
    optimal_sequence = neh_algorithm(sample_jobs)
    print("Optimize Edilmiş İş Sırası:", optimal_sequence)
    plot_gantt(optimal_sequence, sample_jobs, machines)

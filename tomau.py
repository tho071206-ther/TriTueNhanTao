import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import string
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class IntegratedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng AI - Graph Coloring, TSP & Scheduling")
        self.root.geometry("1100x650")
        
        # Notebook chứa các tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Graph Coloring
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Tô màu đồ thị")
        self.setup_graph_tab()
        
        # Tab 2: TSP
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="TSP")
        self.setup_tsp_tab()
        
        # Tab 3: Scheduling
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Xếp lịch")
        self.setup_scheduling_tab()
    
    # ==================== TAB 1: GRAPH COLORING ====================
    def setup_graph_tab(self):
        # Frame trái - Input
        left_frame = tk.Frame(self.tab1, width=380)
        left_frame.pack(side='left', fill='both', padx=10, pady=10)
        
        input_frame = ttk.LabelFrame(left_frame, text="Ma trận kề")
        input_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.matrix_text = scrolledtext.ScrolledText(input_frame, height=10, width=40, font=("Courier", 9))
        self.matrix_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.matrix_text.insert('1.0', "0 1 1 0 1 0\n1 0 1 1 0 1\n1 1 0 1 1 0\n0 1 1 0 0 1\n1 0 1 0 0 1\n0 1 0 1 1 0")
        
        btn_frame = tk.Frame(input_frame)
        btn_frame.pack(pady=(0, 10))
        
        ttk.Button(btn_frame, text="Tải File", command=self.load_graph_file).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="Tô màu", command=self.color_graph).pack(side='left', padx=3)
        ttk.Button(btn_frame, text="Xóa", command=self.clear_graph).pack(side='left', padx=3)
        
        result_frame = ttk.LabelFrame(left_frame, text="Kết quả")
        result_frame.pack(fill='both', expand=True)
        
        self.graph_result = scrolledtext.ScrolledText(result_frame, height=13, width=40, 
                                                      font=("Courier", 8), state='disabled')
        self.graph_result.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Frame phải - Đồ thị
        right_frame = ttk.LabelFrame(self.tab1, text="Đồ thị")
        right_frame.pack(side='right', fill='both', expand=True, padx=(0, 10), pady=10)
        
        self.figure = plt.Figure(figsize=(5.5, 5), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        self.draw_placeholder()
    
    def draw_placeholder(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "Nhập ma trận\nvà nhấn 'Tô màu'", 
               ha='center', va='center', fontsize=12, color='gray')
        ax.axis('off')
        self.canvas.draw()
    
    def load_graph_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.matrix_text.delete('1.0', tk.END)
                    self.matrix_text.insert('1.0', f.read())
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không đọc được: {str(e)}")
    
    def clear_graph(self):
        self.matrix_text.delete('1.0', tk.END)
        self.graph_result.config(state='normal')
        self.graph_result.delete('1.0', tk.END)
        self.graph_result.config(state='disabled')
        self.draw_placeholder()
    
    def color_graph(self):
        matrix_str = self.matrix_text.get('1.0', tk.END).strip()
        if not matrix_str:
            messagebox.showwarning("Cảnh báo", "Nhập ma trận!")
            return
        
        try:
            G = []
            for line in matrix_str.split('\n'):
                row = [int(v) for v in line.strip().split() if v.strip()]
                if row:
                    G.append(row)
            
            if not G or len(G) != len(G[0]):
                raise ValueError("Ma trận không hợp lệ")
            
            n = len(G)
            node_names = list(string.ascii_uppercase[:n])
            node_to_index = {name: i for i, name in enumerate(node_names)}
            
            degrees = [sum(row) for row in G]
            pairs = [(degrees[i], i) for i in range(n)]
            pairs.sort(reverse=True)
            sorted_nodes = [node_names[idx] for _, idx in pairs]
            
            solution = self.greedy_coloring(G, node_names, sorted_nodes, node_to_index)
            
            self.display_graph_result(G, node_names, degrees, sorted_nodes, solution, node_to_index)
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def greedy_coloring(self, G, node_names, sorted_nodes, node_to_index):
        COLORS = ["Blue", "Red", "Yellow", "Green", "Purple", "Orange", "Cyan", "Magenta"]
        color_domain = {name: COLORS.copy() for name in node_names}
        solution = {}
        
        for node in sorted_nodes:
            if not color_domain[node]:
                return None
            chosen = color_domain[node][0]
            solution[node] = chosen
            idx = node_to_index[node]
            
            for j, neighbor in enumerate(node_names):
                if G[idx][j] == 1 and neighbor not in solution:
                    if chosen in color_domain[neighbor]:
                        color_domain[neighbor].remove(chosen)
        return solution
    
    def display_graph_result(self, G, node_names, degrees, sorted_nodes, solution, node_to_index):
        self.graph_result.config(state='normal')
        self.graph_result.delete('1.0', tk.END)
        
        output = f"Đỉnh: {node_names}\n{'='*30}\n\nBậc:\n"
        for i, node in enumerate(node_names):
            output += f"  {node}: {degrees[i]}\n"
        output += f"\nThứ tự: {sorted_nodes}\n{'='*30}\n\n"
        
        if solution:
            output += "Kết quả:\n"
            for node, color in sorted(solution.items()):
                output += f"  {node} = {color}\n"
            output += f"\nSố màu: {len(set(solution.values()))}\n"
            self.draw_colored_graph(G, node_names, solution, node_to_index)
        else:
            output += "Không tìm được lời giải\n"
        
        self.graph_result.insert('1.0', output)
        self.graph_result.config(state='disabled')
    
    def draw_colored_graph(self, G, node_names, solution, node_to_index):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        G_nx = nx.Graph()
        for node in node_names:
            G_nx.add_node(node)
        
        for i in range(len(G)):
            for j in range(i+1, len(G)):
                if G[i][j] == 1:
                    G_nx.add_edge(node_names[i], node_names[j])
        
        pos = nx.spring_layout(G_nx, seed=42, k=1.5)
        
        color_map = {
            'Blue': '#3498db', 'Red': '#e74c3c', 'Yellow': '#f1c40f',
            'Green': '#27ae60', 'Purple': '#9b59b6', 'Orange': '#e67e22',
            'Cyan': '#1abc9c', 'Magenta': '#e91e63'
        }
        
        node_colors = [color_map.get(solution[n], '#95a5a6') for n in node_names]
        
        nx.draw_networkx_edges(G_nx, pos, ax=ax, width=2, alpha=0.5)
        nx.draw_networkx_nodes(G_nx, pos, node_color=node_colors, 
                              node_size=600, ax=ax, edgecolors='black', linewidths=2)
        nx.draw_networkx_labels(G_nx, pos, font_size=11, font_weight='bold', ax=ax)
        
        ax.set_title(f"Đồ thị ({len(set(solution.values()))} màu)", fontsize=11, fontweight='bold')
        ax.axis('off')
        
        colors_used = sorted(set(solution.values()))
        legend = [plt.Line2D([0], [0], marker='o', color='w', 
                            markerfacecolor=color_map[c], markersize=7, label=c) 
                 for c in colors_used]
        ax.legend(handles=legend, loc='upper right', fontsize=8)
        
        self.canvas.draw()
    
    # ==================== TAB 2: TSP ====================
    def setup_tsp_tab(self):
        # Frame input
        input_frame = ttk.LabelFrame(self.tab2, text="Nhập dữ liệu TSP")
        input_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(input_frame, text="Thành phố (cách nhau bởi dấu phẩy):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.cities_entry = ttk.Entry(input_frame, width=50)
        self.cities_entry.grid(row=0, column=1, padx=5, pady=5)
        self.cities_entry.insert(0, "A,B,C,D,E")
        
        ttk.Label(input_frame, text="Ma trận khoảng cách:").grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        self.tsp_matrix = scrolledtext.ScrolledText(input_frame, height=6, width=50, font=("Courier", 9))
        self.tsp_matrix.grid(row=1, column=1, padx=5, pady=5)
        self.tsp_matrix.insert('1.0', "0 10 3 5 8\n10 0 7 4 6\n3 7 0 9 2\n5 4 9 0 11\n8 6 2 11 0")
        
        btn_frame = tk.Frame(self.tab2)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Chạy mẫu", command=self.run_sample_tsp).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Chạy nhập liệu", command=self.run_custom_tsp).pack(side='left', padx=5)
        
        ttk.Label(self.tab2, text="Kết quả:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.tsp_result = scrolledtext.ScrolledText(self.tab2, height=18, width=100)
        self.tsp_result.pack(padx=10, pady=5, fill='both', expand=True)
    
    def nearest_neighbor_tsp(self, distance_matrix, cities):
        n = len(cities)
        current = 0
        unvisited = set(range(n))
        unvisited.remove(0)
        
        tour = [cities[0]]
        total = 0
        
        while unvisited:
            nearest_dist = float('inf')
            nearest = -1
            
            for next_city in unvisited:
                dist = distance_matrix[current][next_city]
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = next_city
            
            if nearest != -1:
                tour.append(cities[nearest])
                total += nearest_dist
                unvisited.remove(nearest)
                current = nearest
        
        if tour:
            total += distance_matrix[current][0]
            tour.append(cities[0])
        
        return tour, total
    
    def run_tsp(self, cities, dist_matrix):
        self.tsp_result.delete('1.0', tk.END)
        
        tour, cost = self.nearest_neighbor_tsp(dist_matrix, cities)
        
        output = "--- BÀI TOÁN NGƯỜI BÁN HÀNG (TSP) ---\n\n"
        output += f"Thành phố: {cities}\n"
        output += f"Ma trận khoảng cách:\n{dist_matrix}\n"
        output += "-" * 50 + "\n"
        output += f"Chu trình: {' -> '.join(tour)}\n"
        output += f"Tổng chi phí: {cost}\n"
        
        self.tsp_result.insert('1.0', output)
    
    def run_sample_tsp(self):
        cities = ["A", "B", "C", "D", "E"]
        dist = np.array([
            [0, 10, 3, 5, 8],
            [10, 0, 7, 4, 6],
            [3, 7, 0, 9, 2],
            [5, 4, 9, 0, 11],
            [8, 6, 2, 11, 0]
        ])
        self.run_tsp(cities, dist)
    
    def run_custom_tsp(self):
        try:
            cities_str = self.cities_entry.get().strip()
            cities = [c.strip() for c in cities_str.split(',')]
            
            if not cities:
                messagebox.showerror("Lỗi", "Nhập danh sách thành phố")
                return
            
            matrix_str = self.tsp_matrix.get('1.0', tk.END).strip()
            dist_matrix = []
            for line in matrix_str.split('\n'):
                row = [int(v) for v in line.strip().split() if v.strip()]
                if row:
                    dist_matrix.append(row)
            
            dist_matrix = np.array(dist_matrix)
            
            if len(dist_matrix) != len(cities) or len(dist_matrix[0]) != len(cities):
                messagebox.showerror("Lỗi", "Kích thước ma trận không khớp với số thành phố")
                return
            
            self.run_tsp(cities, dist_matrix)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
    
    # ==================== TAB 3: SCHEDULING ====================
    def setup_scheduling_tab(self):
        input_frame = ttk.LabelFrame(self.tab3, text="Thông tin")
        input_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(input_frame, text="Môn học (tên:GV1,GV2):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.subjects_entry = ttk.Entry(input_frame, width=50)
        self.subjects_entry.grid(row=0, column=1, padx=5, pady=5)
        self.subjects_entry.insert(0, "Toán:GV_Toan1,GV_Toan2;Tin:GV_Tin1,GV_Tin2")
        
        ttk.Label(input_frame, text="Số tiết/GV:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.hours_entry = ttk.Entry(input_frame, width=20)
        self.hours_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.hours_entry.insert(0, "5")
        
        ttk.Label(input_frame, text="Số ngày:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.days_entry = ttk.Entry(input_frame, width=20)
        self.days_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        self.days_entry.insert(0, "6")
        
        ttk.Label(input_frame, text="Số tiết/ngày:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.periods_entry = ttk.Entry(input_frame, width=20)
        self.periods_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.periods_entry.insert(0, "5")
        
        btn_frame = tk.Frame(self.tab3)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Chạy mẫu", command=self.run_sample_scheduling).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Chạy nhập liệu", command=self.run_custom_scheduling).pack(side='left', padx=5)
        
        ttk.Label(self.tab3, text="Kết quả:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.scheduling_result = scrolledtext.ScrolledText(self.tab3, height=20, width=100)
        self.scheduling_result.pack(padx=10, pady=5, fill='both', expand=True)
    
    def calculate_fitness(self, chromosome, req_hours, classes):
        score = 1000
        
        slot_usage = {}
        for slot, teacher, subject in chromosome:
            if slot in slot_usage:
                score -= 500
            slot_usage[slot] = teacher
        
        teacher_count = {t: 0 for sub_list in classes.values() for t in sub_list}
        for slot, teacher, subject in chromosome:
            teacher_count[teacher] += 1
        
        for count in teacher_count.values():
            score -= abs(count - req_hours) * 100
        
        return max(1, score)
    
    def initialize_population(self, pop_size, lessons, slots, n_lessons):
        population = []
        for _ in range(pop_size):
            schedule_slots = random.sample(slots, n_lessons)
            lessons_copy = lessons.copy()
            random.shuffle(lessons_copy)
            
            chromosome = []
            for i in range(n_lessons):
                teacher, subject = lessons_copy[i]
                chromosome.append((schedule_slots[i], teacher, subject))
            population.append(chromosome)
        return population
    
    def genetic_algorithm(self, pop_size, generations, lessons, slots, req_hours, classes):
        n_lessons = len(lessons)
        population = self.initialize_population(pop_size, lessons, slots, n_lessons)
        
        for gen in range(generations):
            fitness = [self.calculate_fitness(c, req_hours, classes) for c in population]
            best_idx = np.argmax(fitness)
            best = population[best_idx]
            
            if fitness[best_idx] >= 900:
                return best, gen
            
            new_pop = [best]
            
            while len(new_pop) < pop_size:
                p1 = self.select_parent(population, fitness)
                p2 = self.select_parent(population, fitness)
                
                c1, c2 = self.crossover(p1, p2, n_lessons)
                
                new_pop.append(self.mutate(c1, n_lessons))
                if len(new_pop) < pop_size:
                    new_pop.append(self.mutate(c2, n_lessons))
            
            population = new_pop
        
        return best, generations
    
    def select_parent(self, population, fitness):
        candidates = random.sample(list(zip(population, fitness)), 3)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def crossover(self, p1, p2, n):
        point = n // 2
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    
    def mutate(self, chromosome, n):
        if random.random() < 0.05:
            i1, i2 = random.sample(range(n), 2)
            s1, s2 = chromosome[i1][0], chromosome[i2][0]
            chromosome[i1] = (s2, chromosome[i1][1], chromosome[i1][2])
            chromosome[i2] = (s1, chromosome[i2][1], chromosome[i2][2])
        return chromosome
    
    def run_scheduling(self, classes, req_hours, n_days, periods):
        self.scheduling_result.delete('1.0', tk.END)
        
        slots = [f"Day{d}_T{t}" for d in range(2, 2+n_days) for t in range(1, periods+1)]
        
        lessons = []
        for subject, teachers in classes.items():
            for teacher in teachers:
                lessons.extend([(teacher, subject)] * req_hours)
        
        output = "--- XẾP LỊCH GIẢNG DẠY (Genetic Algorithm) ---\n\n"
        output += f"Môn học: {list(classes.keys())}\n"
        output += f"Số tiết/GV: {req_hours}\n"
        output += f"Tổng tiết: {len(lessons)}\n"
        output += f"Số slot: {len(slots)}\n\n"
        
        schedule, gen = self.genetic_algorithm(50, 100, lessons, slots, req_hours, classes)
        
        if schedule:
            output += f"Tìm thấy lời giải ở thế hệ {gen}\n\n"
            output += "LỊCH TRÌNH:\n" + "-" * 50 + "\n"
            
            schedule_dict = {slot: f"{subj} ({teach})" for slot, teach, subj in schedule}
            sorted_schedule = sorted(schedule_dict.items(),
                                   key=lambda x: (int(x[0].split('_')[0].replace('Day', '')),
                                                 int(x[0].split('_')[1].replace('T', ''))))
            
            for slot, info in sorted_schedule:
                output += f"{slot.ljust(10)}: {info}\n"
            
            output += f"\nĐiểm fitness: {self.calculate_fitness(schedule, req_hours, classes)}\n"
        
        self.scheduling_result.insert('1.0', output)
    
    def run_sample_scheduling(self):
        classes = {"Toán": ["GV_Toan1", "GV_Toan2"], "Tin": ["GV_Tin1", "GV_Tin2"]}
        self.run_scheduling(classes, 5, 6, 5)
    
    def run_custom_scheduling(self):
        try:
            subjects_str = self.subjects_entry.get().strip()
            classes = {}
            for item in subjects_str.split(';'):
                parts = item.split(':')
                if len(parts) == 2:
                    classes[parts[0].strip()] = [t.strip() for t in parts[1].split(',')]
            
            req_hours = int(self.hours_entry.get())
            n_days = int(self.days_entry.get())
            periods = int(self.periods_entry.get())
            
            if not classes:
                messagebox.showerror("Lỗi", "Nhập dữ liệu hợp lệ")
                return
            
            self.run_scheduling(classes, req_hours, n_days, periods)
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegratedApp(root)
    root.mainloop()
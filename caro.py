import tkinter as tk
from tkinter import messagebox, ttk
import math
import sys

# Tăng giới hạn đệ quy cho Minimax
sys.setrecursionlimit(2000)

# ================== HẰNG SỐ ==================
NGUOI_CHOI_MAX = 'X'      # AI (MAX)
DOI_THU_MIN = 'O'         # Người chơi (MIN)
DIEM_THANG = 1000000      # Điểm thắng tuyệt đối cho AI

class CaroGame:
    def __init__(self, root):
        """
        Trò chơi Caro N×N
        AI sử dụng:
        - Minimax thuần
        - Minimax + Alpha-Beta pruning
        """
        self.root = root
        self.root.title("Caro AI - Minimax & Alpha-Beta")
       self.root.geometry("900x700")   # kích thước ban đầu
       self.root.resizable(True, True) # cho phép kéo giãn


        self.board_size = 3
        self.search_depth = 4
        self.ban_co = []
        self.buttons = []
        self.game_over = False
        self.ai_mode = "alpha_beta"

        self.setup_ui()

    # ================== GIAO DIỆN ==================
    def setup_ui(self):
        settings = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        settings.pack(fill=tk.X)

        # Nhập kích thước bàn cờ N
        tk.Label(settings, text="Nhập N (kích thước bàn cờ):",
                 font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=0, column=0, padx=5)

        self.size_entry = tk.Entry(settings, width=6, font=("Arial", 11))
        self.size_entry.insert(0, "3")
        self.size_entry.grid(row=0, column=1, padx=5)

        # Chọn thuật toán AI
        tk.Label(settings, text="Thuật toán AI:",
                 font=("Arial", 11, "bold"), bg="#ecf0f1").grid(row=0, column=2, padx=5)

        self.ai_var = tk.StringVar(value="alpha_beta")
        ttk.Combobox(settings, textvariable=self.ai_var,
                     values=["minimax", "alpha_beta"],
                     state="readonly", width=15).grid(row=0, column=3, padx=5)

        tk.Button(settings, text="Bắt đầu trò chơi",
                  command=self.start_game,
                  bg="#3498db", fg="white",
                  font=("Arial", 11, "bold")).grid(row=0, column=4, padx=10)

        self.status_label = tk.Label(self.root,
                                     text="Nhập N và nhấn 'Bắt đầu trò chơi'",
                                     font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)

        self.board_frame = tk.Frame(self.root, bg="#34495e", padx=20, pady=20)
        self.board_frame.pack(expand=True, fill=tk.BOTH)

    # ================== KHỞI TẠO GAME ==================
    def start_game(self):
        """
        - Lấy N từ ô nhập
        - Kiểm tra hợp lệ
        - Điều chỉnh độ sâu tìm kiếm theo N
        - Tạo bàn cờ N×N
        """
        try:
            self.board_size = int(self.size_entry.get())
            if self.board_size < 3:
                raise ValueError
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập N là số nguyên ≥ 3")
            return

        # Giảm độ sâu nếu bàn cờ lớn (tránh treo máy)
        self.search_depth = 4 if self.board_size <= 4 else 2
        self.ai_mode = self.ai_var.get()
        self.game_over = False

        self.ban_co = [[' ']*self.board_size for _ in range(self.board_size)]

        for w in self.board_frame.winfo_children():
            w.destroy()

        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                b = tk.Button(self.board_frame, text='', width=6, height=3,
                              font=("Arial", 20, "bold"),
                              bg="#ecf0f1",
                              command=lambda r=i, c=j: self.player_move(r, c))
                b.grid(row=i, column=j, padx=2, pady=2)
                row.append(b)
            self.buttons.append(row)

        algo = "Alpha-Beta" if self.ai_mode == "alpha_beta" else "Minimax"
        self.status_label.config(text=f"Lượt của bạn (O) – AI dùng {algo}")

    # ================== NGƯỜI CHƠI ==================
    def player_move(self, row, col):
        """
        Người chơi đánh O
        Sau đó AI đánh X
        """
        if self.game_over or self.ban_co[row][col] != ' ':
            return

        self.ban_co[row][col] = DOI_THU_MIN
        self.buttons[row][col].config(text='O', fg='red', state='disabled')

        if self.check_game_end():
            return

        self.status_label.config(text="AI đang suy nghĩ...")
        self.root.after(200, self.ai_move)

    # ================== AI ==================
    def ai_move(self):
        """
        AI chọn nước đi tốt nhất bằng:
        - Minimax thuần
        - hoặc Alpha-Beta pruning
        """
        if self.ai_mode == "alpha_beta":
            move, _ = self.find_best_move_alpha_beta(self.ban_co, self.search_depth)
        else:
            move, _ = self.find_best_move_minimax(self.ban_co, self.search_depth)

        if move:
            r, c = move
            self.ban_co[r][c] = NGUOI_CHOI_MAX
            self.buttons[r][c].config(text='X', fg='blue', state='disabled')

        self.check_game_end()
        self.status_label.config(text="Lượt của bạn (O)")

    # ================== KIỂM TRA KẾT THÚC ==================
    def check_game_end(self):
        """
        Kiểm tra thắng / thua / hòa
        """
        if self.check_win(self.ban_co, NGUOI_CHOI_MAX):
            messagebox.showinfo("Kết thúc", "AI (X) thắng!")
            self.game_over = True
            return True

        if self.check_win(self.ban_co, DOI_THU_MIN):
            messagebox.showinfo("Kết thúc", "Bạn (O) thắng!")
            self.game_over = True
            return True

        if self.is_terminal(self.ban_co):
            messagebox.showinfo("Kết thúc", "Hòa!")
            self.game_over = True
            return True

        return False

    # ================== LUẬT TRÒ CHƠI ==================
    def check_win(self, ban_co, player):
        """
        Kiểm tra thắng:
        - Hàng
        - Cột
        - 2 đường chéo
        (phù hợp demo Minimax cho bàn nhỏ)
        """
        N = len(ban_co)
        for i in range(N):
            if all(ban_co[i][j] == player for j in range(N)): return True
            if all(ban_co[j][i] == player for j in range(N)): return True
        if all(ban_co[i][i] == player for i in range(N)): return True
        if all(ban_co[i][N-1-i] == player for i in range(N)): return True
        return False

    def is_terminal(self, ban_co):
        """
        Trạng thái kết thúc:
        - Có người thắng
        - Hoặc hết ô trống
        """
        if self.check_win(ban_co, NGUOI_CHOI_MAX) or self.check_win(ban_co, DOI_THU_MIN):
            return True
        return not any(' ' in row for row in ban_co)

    def evaluate(self, ban_co):
        """
        Hàm đánh giá trạng thái:
        +DIEM_THANG : AI thắng
        -DIEM_THANG : Người thắng
        0           : Trung tính / hòa
        """
        if self.check_win(ban_co, NGUOI_CHOI_MAX): return DIEM_THANG
        if self.check_win(ban_co, DOI_THU_MIN): return -DIEM_THANG
        return 0

    def get_available_moves(self, ban_co):
        """Trả về danh sách các ô trống"""
        return [(i, j) for i in range(len(ban_co))
                        for j in range(len(ban_co)) if ban_co[i][j] == ' ']

    # ================== MINIMAX ==================
    def minimax_thuan(self, ban_co, depth, is_max):
        """
        Thuật toán MINIMAX:
        - MAX (AI): tối đa hóa điểm
        - MIN (người): tối thiểu hóa điểm
        """
        if depth == 0 or self.is_terminal(ban_co):
            return self.evaluate(ban_co)

        if is_max:
            best = -math.inf
            for r, c in self.get_available_moves(ban_co):
                ban_co[r][c] = NGUOI_CHOI_MAX
                best = max(best, self.minimax_thuan(ban_co, depth-1, False))
                ban_co[r][c] = ' '
            return best
        else:
            best = math.inf
            for r, c in self.get_available_moves(ban_co):
                ban_co[r][c] = DOI_THU_MIN
                best = min(best, self.minimax_thuan(ban_co, depth-1, True))
                ban_co[r][c] = ' '
            return best

    def find_best_move_minimax(self, ban_co, depth):
        """Tìm nước đi tốt nhất bằng Minimax"""
        best, move = -math.inf, None
        for r, c in self.get_available_moves(ban_co):
            ban_co[r][c] = NGUOI_CHOI_MAX
            val = self.minimax_thuan(ban_co, depth-1, False)
            ban_co[r][c] = ' '
            if val > best:
                best, move = val, (r, c)
        return move, best

    # ================== ALPHA-BETA ==================
    def minimax_alpha_beta(self, ban_co, depth, alpha, beta, is_max):
        """
        Minimax + Alpha-Beta pruning:
        - Cắt bỏ các nhánh không cần thiết
        - Tăng tốc đáng kể so với Minimax thuần
        """
        if depth == 0 or self.is_terminal(ban_co):
            return self.evaluate(ban_co)

        if is_max:
            for r, c in self.get_available_moves(ban_co):
                ban_co[r][c] = NGUOI_CHOI_MAX
                alpha = max(alpha, self.minimax_alpha_beta(ban_co, depth-1, alpha, beta, False))
                ban_co[r][c] = ' '
                if alpha >= beta:
                    break
            return alpha
        else:
            for r, c in self.get_available_moves(ban_co):
                ban_co[r][c] = DOI_THU_MIN
                beta = min(beta, self.minimax_alpha_beta(ban_co, depth-1, alpha, beta, True))
                ban_co[r][c] = ' '
                if beta <= alpha:
                    break
            return beta

    def find_best_move_alpha_beta(self, ban_co, depth):
        """Tìm nước đi tốt nhất bằng Alpha-Beta"""
        alpha, beta = -math.inf, math.inf
        best, move = -math.inf, None
        for r, c in self.get_available_moves(ban_co):
            ban_co[r][c] = NGUOI_CHOI_MAX
            val = self.minimax_alpha_beta(ban_co, depth-1, alpha, beta, False)
            ban_co[r][c] = ' '
            if val > best:
                best, move = val, (r, c)
            alpha = max(alpha, best)
        return move, best

# ================== CHẠY CHƯƠNG TRÌNH ==================
if __name__ == "__main__":
    root = tk.Tk()
    CaroGame(root)
    root.mainloop()

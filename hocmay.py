import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_blobs
from scipy.spatial.distance import cdist
from collections import Counter

class MLApp:
    def __init__(self, root):
        """
        Ứng dụng minh hoạ 3 thuật toán học máy:
        - Hồi quy tuyến tính
        - K-NN (phân loại)
        - K-Means (phân cụm)
        """
        self.root = root
        self.root.title("Học máy cơ bản")
        self.root.geometry("900x650")

        nb = ttk.Notebook(root)
        nb.pack(fill=tk.BOTH, expand=True)

        self.reg_tab = ttk.Frame(nb)
        self.knn_tab = ttk.Frame(nb)
        self.km_tab  = ttk.Frame(nb)

        nb.add(self.reg_tab, text="Hồi quy")
        nb.add(self.knn_tab, text="K-NN")
        nb.add(self.km_tab,  text="K-Means")

        self.regression_ui()
        self.knn_ui()
        self.kmeans_ui()

    def regression_ui(self):
        """Giao diện cho hồi quy tuyến tính"""
        ttk.Label(self.reg_tab, text="Diện tích (m²)").pack()
        self.area = ttk.Entry(self.reg_tab)
        self.area.insert(0, "80")
        self.area.pack()

        ttk.Button(self.reg_tab, text="Dự đoán",
                   command=self.run_regression).pack(pady=5)

        self.fig = plt.Figure(figsize=(5,4))
        self.canvas = FigureCanvasTkAgg(self.fig, self.reg_tab)
        self.canvas.get_tk_widget().pack()

    def run_regression(self):
        """
        THUẬT TOÁN: HỒI QUY TUYẾN TÍNH
        - Học mối quan hệ y = ax + b
        - Dự đoán giá nhà từ diện tích
        """
        X = np.array([[30],[40],[50],[60],[70],[80],[100]])
        y = np.array([1.5,2,2.8,3,3.5,4.2,5])

        model = LinearRegression()
        model.fit(X, y)                  # Học mô hình

        x = float(self.area.get())
        y_pred = model.predict([[x]])    # Dự đoán

        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.scatter(X, y)                 # Dữ liệu thật
        ax.plot(X, model.predict(X))     # Đường hồi quy
        ax.scatter([x], y_pred, c="red") # Điểm dự đoán
        ax.set_title(f"Giá ≈ {y_pred[0]:.2f} tỷ")
        self.canvas.draw()

    def knn_ui(self):
        """Giao diện K-NN"""
        ttk.Label(self.knn_tab, text="K").pack()
        self.k = ttk.Entry(self.knn_tab)
        self.k.insert(0, "5")
        self.k.pack()

        ttk.Button(self.knn_tab, text="Chạy KNN",
                   command=self.run_knn).pack(pady=5)

        self.fig_knn = plt.Figure(figsize=(5,4))
        self.canvas_knn = FigureCanvasTkAgg(self.fig_knn, self.knn_tab)
        self.canvas_knn.get_tk_widget().pack()

    def run_knn(self):
        """
        THUẬT TOÁN: K-NEAREST NEIGHBORS
        - Phân loại dựa trên K láng giềng gần nhất
        - Dùng khoảng cách Euclid
        - Bỏ phiếu đa số
        """
        k = int(self.k.get())
        X, y = make_blobs(n_samples=200, centers=3)

        y_pred = []
        for p in X:
            dist = np.linalg.norm(X - p, axis=1)   # Tính khoảng cách
            idx = np.argsort(dist)[1:k+1]          # Lấy K gần nhất
            y_pred.append(Counter(y[idx]).most_common(1)[0][0])

        self.fig_knn.clear()
        ax = self.fig_knn.add_subplot(111)
        ax.scatter(X[:,0], X[:,1], c=y_pred)
        ax.set_title("K-NN Classification")
        self.canvas_knn.draw()

    def kmeans_ui(self):
        """Giao diện K-Means"""
        ttk.Label(self.km_tab, text="Số cụm K").pack()
        self.km_k = ttk.Entry(self.km_tab)
        self.km_k.insert(0, "3")
        self.km_k.pack()

        ttk.Button(self.km_tab, text="Chạy K-Means",
                   command=self.run_kmeans).pack(pady=5)

        self.fig_km = plt.Figure(figsize=(5,4))
        self.canvas_km = FigureCanvasTkAgg(self.fig_km, self.km_tab)
        self.canvas_km.get_tk_widget().pack()

    def run_kmeans(self):
        """
        THUẬT TOÁN: K-MEANS
        - Phân cụm dữ liệu không nhãn
        - Lặp: gán cụm → cập nhật tâm → hội tụ
        """
        k = int(self.km_k.get())
        X, _ = make_blobs(n_samples=300, centers=k)

        centers = X[np.random.choice(len(X), k, False)]  # Tâm ban đầu

        for _ in range(20):
            labels = np.argmin(cdist(X, centers), axis=1)
            for i in range(k):
                centers[i] = X[labels==i].mean(axis=0)

        self.fig_km.clear()
        ax = self.fig_km.add_subplot(111)
        ax.scatter(X[:,0], X[:,1], c=labels)
        ax.scatter(centers[:,0], centers[:,1], c="red", marker="*")
        ax.set_title("K-Means Clustering")
        self.canvas_km.draw()

root = tk.Tk()
MLApp(root)
root.mainloop()

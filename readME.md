
# TÓM TẮT LÝ THUYẾT: HỌC MÁY

##  Kĩ thuật K-Means Clustering
là một thuật toán học không giám sát, đơn giản và hiệu quả, được sử dụng để phân chia dữ liệu thành K nhóm (cụm) dựa trên sự giống nhau về đặc điểm.

## Mục tiêu:
Chia tập dữ liệu thành K nhóm, sao cho tổng bình phương khoảng cách từ mỗi điểm dữ liệu đến tâm cụm gần nhất của nó là nhỏ nhất.

### Các Bước Thực hiện Thuật toánThuật toán lặp đi lặp lại (Iterative Algorithm) theo 4 bước sau:
**Bước 1: Khởi tạo (Initialization)**
Chọn K tâm cụm (c_1, c_2, ..., c_k) ban đầu một cách ngẫu nhiên từ tập dữ liệu.
**Bước 2: Gán nhãn (Assignment)**
Gán mỗi điểm dữ liệu x_i vào cụm gần nhất. Khoảng cách thường được tính bằng **Khoảng cách Euclidean** giữa điểm dữ liệu và tâm cụm:
**Bước 3: Cập nhật tâm cụm (Update)**
Cập nhật tâm cụm c_j mới bằng cách tính **Trung bình cộng** của tất cả các điểm dữ liệu đã được gán vào cụm đó.
**Bước 4: Hội tụ (Convergence)**
Lặp lại Bước 2 và Bước 3 cho đến khi các tâm cụm không còn thay đổi vị trí nữa, hoặc đạt đến số lần lặp tối đa.



## Kĩ thuật K-Nearest Neighbors (K-NN)
là một thuật toán thuộc nhóm học có giám sát, được sử dụng chủ yếu cho bài toán **Phân loại (Classification)**.

### Nguyên tắc hoạt động* 
K-NN hoạt động dựa trên giả định rằng các điểm dữ liệu tương tự nhau sẽ nằm gần nhau trong không gian đặc trưng (Feature Space).
Đây là một thuật toán **"Lười biếng" (Lazy Learner)** vì nó không học một mô hình chung trong giai đoạn huấn luyện mà chỉ lưu trữ toàn bộ dữ liệu huấn luyện.

### Quá trình Phân loại
Khi có một điểm dữ liệu mới (x_{new}) cần dự đoán nhãn:
1. **Tính khoảng cách:** Tính khoảng cách (thường là khoảng cách Euclidean) từ x_{new} đến tất cả các điểm dữ liệu trong tập huấn luyện.
2. **Tìm K láng giềng:** Sắp xếp khoảng cách theo thứ tự tăng dần và chọn ra K điểm lân cận gần nhất.
3. **Bỏ phiếu đa số (Majority Voting):** Nhãn của điểm dữ liệu mới sẽ được gán bằng nhãn phổ biến nhất (xuất hiện nhiều nhất) trong K điểm lân cận đã chọn.

Khoảng cách được sử dụng phổ biến nhất là **Khoảng cách Euclidean**.

Việc chọn giá trị K (số lượng láng giềng) là rất quan trọng:

* **K nhỏ:** Thuật toán nhạy cảm với nhiễu (noise), dễ bị Overfitting.
* **K lớn:** Giảm thiểu ảnh hưởng của nhiễu nhưng có thể làm mờ ranh giới phân loại, dẫn đến Underfitting.

Việc đánh giá K thường được thực hiện thông qua các phương pháp kiểm chứng chéo (Cross-Validation) hoặc **Grid Search** để tìm giá trị tối ưu.

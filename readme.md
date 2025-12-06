
# BÁO CÁO CƠ SỞ LÝ THUYẾT: BÀI TOÁN THỎA MÃN RÀNG BUỘC VÀ GIẢI THUẬT TÔ MÀU ĐỒ THỊ

## 1. MỤC TIÊU BÀI HỌC
Báo cáo này tổng hợp các kiến thức nền tảng nhằm giúp sinh viên:
* [cite_start]Củng cố kiến thức về các phương pháp giải quyết **Bài toán Thỏa mãn Ràng buộc (CSP)**[cite: 9].
* [cite_start]Hiểu rõ cơ chế hoạt động và cách áp dụng thuật toán vào việc giải quyết các vấn đề thực tế có ràng buộc[cite: 10].
* [cite_start]Nắm vững quy trình cài đặt thuật toán tối ưu hóa trên đồ thị[cite: 12].

---

## 2. TỔNG QUAN VỀ BÀI TOÁN THỎA MÃN RÀNG BUỘC (CSP)

### 2.1. Định nghĩa Ràng buộc
[cite_start]Trong trí tuệ nhân tạo, một **ràng buộc** được hiểu là một quan hệ trên một tập hợp các biến[cite: 16]. Ràng buộc quy định những giá trị nào là hợp lệ hoặc không hợp lệ cho các biến đó.

[cite_start]Cách biểu diễn ràng buộc [cite: 17-19]:
* Biểu diễn bằng **biểu thức** (toán học hoặc logic).
* Biểu diễn bằng **bảng liệt kê** các phép gán giá trị phù hợp.

### 2.2. Cấu trúc của Bài toán CSP
[cite_start]Một bài toán CSP được định nghĩa đầy đủ bởi ba thành phần chính [cite: 20-23]:
1.  **Tập Biến (Variables - X):** Một tập hợp hữu hạn các đối tượng cần gán giá trị.
2.  **Miền Giá trị (Domains - D):** Tập hợp các giá trị khả dĩ mà mỗi biến có thể nhận.
3.  **Tập Ràng buộc (Constraints - C):** Tập hợp hữu hạn các quy tắc giới hạn sự kết hợp giá trị giữa các biến.

### 2.3. Lời giải của bài toán
[cite_start]Một **lời giải** cho bài toán CSP là một phép gán đầy đủ giá trị cho tất cả các biến trong tập biến X, sao cho phép gán này **thỏa mãn tất cả các ràng buộc** đã đề ra [cite: 24-25].

---

## 3. THUẬT TOÁN TÔ MÀU TỐI ƯU TRÊN ĐỒ THỊ

Đây là một ứng dụng điển hình của CSP nhằm giải quyết vấn đề phân bổ tài nguyên với ràng buộc xung đột.

### 3.1. Ràng buộc cốt lõi
[cite_start]Trong bài toán tô màu đồ thị, ràng buộc duy nhất và quan trọng nhất là: **Hai đỉnh kề nhau (có cạnh nối trực tiếp) không được phép tô cùng một màu**[cite: 27].

### 3.2. Chiến lược giải quyết (Heuristic Bậc lớn nhất)
Để tìm lời giải tối ưu (sử dụng ít màu nhất có thể), thuật toán sử dụng chiến lược tham lam (Greedy) dựa trên bậc của đỉnh. [cite_start]Quy trình lặp lại các bước sau cho đến khi tất cả các đỉnh đều được tô màu[cite: 28]:

* **Bước 1: Lựa chọn đỉnh ưu tiên**
    Chọn đỉnh có **bậc lớn nhất** trong số các đỉnh chưa xử lý để tiến hành tô màu. [cite_start]Việc chọn đỉnh bậc cao nhất giúp giải quyết các vùng "khó" (nhiều ràng buộc) trước[cite: 29].

* **Bước 2: Cập nhật trạng thái (Hạ bậc)**
    Sau khi chọn đỉnh, hệ thống cập nhật lại thông số của đồ thị để chuẩn bị cho bước tiếp theo:
    * [cite_start]Đỉnh vừa được tô màu xem như đã xử lý xong, bậc được đặt về 0[cite: 31].
    * [cite_start]Các đỉnh có liên hệ (đỉnh kề) với đỉnh vừa tô sẽ bị giảm bậc đi 1 đơn vị (bậc := bậc - 1)[cite: 32].

* **Bước 3: Lan truyền ràng buộc (Forward Checking)**
    Thực hiện đánh dấu các đỉnh kề với đỉnh vừa tô và **cấm** các đỉnh này sử dụng màu vừa được chọn. [cite_start]Điều này giúp loại bỏ giá trị không hợp lệ khỏi miền giá trị của các biến tương lai ngay lập tức[cite: 33].

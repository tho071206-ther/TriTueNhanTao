
### BÀI TOÁN THỎA MÃN RÀNG BUỘC VÀ GIẢI THUẬT TÔ MÀU ĐỒ THỊ
# Định nghĩa Ràng buộc
Trong trí tuệ nhân tạo, một **ràng buộc** được hiểu là một quan hệ trên một tập hợp các biến. Ràng buộc quy định những giá trị nào là hợp lệ hoặc không hợp lệ cho các biến đó.

# Cách biểu diễn ràng buộc
Biểu diễn bằng **biểu thức** (toán học hoặc logic).
Biểu diễn bằng **bảng liệt kê** các phép gán giá trị phù hợp.

# Cấu trúc của Bài toán CSP
Một bài toán CSP được định nghĩa đầy đủ bởi ba thành phần chính:
1.  **Tập Biến (Variables - X):** Một tập hợp hữu hạn các đối tượng cần gán giá trị.
2.  **Miền Giá trị (Domains - D):** Tập hợp các giá trị khả dĩ mà mỗi biến có thể nhận.
3.  **Tập Ràng buộc (Constraints - C):** Tập hợp hữu hạn các quy tắc giới hạn sự kết hợp giá trị giữa các biến.

### 2.3. Lời giải của bài toán
Một **lời giải** cho bài toán CSP là một phép gán đầy đủ giá trị cho tất cả các biến trong tập biến X, sao cho phép gán này **thỏa mãn tất cả các ràng buộc** đã đề ra.

---

## THUẬT TOÁN TÔ MÀU TỐI ƯU TRÊN ĐỒ THỊ

Đây là một ứng dụng điển hình của CSP nhằm giải quyết vấn đề phân bổ tài nguyên với ràng buộc xung đột.

# Ràng buộc cốt lõi
Trong bài toán tô màu đồ thị, ràng buộc duy nhất và quan trọng nhất là: **Hai đỉnh kề nhau (có cạnh nối trực tiếp) không được phép tô cùng một màu**.

# Chiến lược giải quyết (Heuristic Bậc lớn nhất)
Để tìm lời giải tối ưu (sử dụng ít màu nhất có thể), thuật toán sử dụng chiến lược tham lam (Greedy) dựa trên bậc của đỉnh. Quy trình lặp lại các bước sau cho đến khi tất cả các đỉnh đều được tô màu:

* **Bước 1: Lựa chọn đỉnh ưu tiên**
    Chọn đỉnh có **bậc lớn nhất** trong số các đỉnh chưa xử lý để tiến hành tô màu. Việc chọn đỉnh bậc cao nhất giúp giải quyết các vùng "khó" (nhiều ràng buộc) trước.

* **Bước 2: Cập nhật trạng thái (Hạ bậc)**
    Sau khi chọn đỉnh, hệ thống cập nhật lại thông số của đồ thị để chuẩn bị cho bước tiếp theo:
    * Đỉnh vừa được tô màu xem như đã xử lý xong, bậc được đặt về 0.
    * Các đỉnh có liên hệ (đỉnh kề) với đỉnh vừa tô sẽ bị giảm bậc đi 1 đơn vị (bậc := bậc - 1).

* **Bước 3: Lan truyền ràng buộc (Forward Checking)**
    Thực hiện đánh dấu các đỉnh kề với đỉnh vừa tô và **cấm** các đỉnh này sử dụng màu vừa được chọn. Điều này giúp loại bỏ giá trị không hợp lệ khỏi miền giá trị của các biến tương lai ngay lập tức.

# TriTueNhanTao

Bao cao thuc hanh tuan 3

PHÂN TÍCH THUẬT TOÁN MINIMAX VÀ CẮT TỈA ALPHA-BETA ỨNG DỤNG TRONG TRÒ CHƠI CỜ CARO (GOMOKU)
 ### I. GIỚI THIỆU

Trò chơi Cờ Caro (Gomoku) là một trò chơi có thông tin đầy đủ (perfect information), đối kháng (adversarial), và mang tính chiến lược cao, là môi trường lý tưởng để nghiên cứu các thuật toán tìm kiếm đối kháng. Mục tiêu của báo cáo này là phân tích cơ chế hoạt động, logic tính toán của hai thuật toán nền tảng là **Minimax** và **Cắt tỉa Alpha-Beta (alpha-beta Pruning)**, đồng thời làm rõ cách chúng được áp dụng để xây dựng trí tuệ nhân tạo (AI) cho trò chơi Cờ Caro.

 ### II. CƠ SỞ LÝ THUYẾT
**THUẬT TOÁN MINIMAX**
Thuật toán Minimax là một thuật toán đệ quy được thiết kế để tìm nước đi tối ưu cho người chơi hiện tại bằng cách giả định đối thủ cũng sẽ chơi tối ưu.

## 1. Logic Cơ bản

Thuật toán hoạt động dựa trên việc xây dựng một **Cây trò chơi**, trong đó mỗi nút (node) là một trạng thái của bàn cờ, và các nhánh là các nước đi khả thi. Quá trình này được thực hiện bằng cách định trị (gán giá trị) cho các nút trên cây:

1.  **Người chơi MAX (AI):** Mục tiêu là tìm nước đi mang lại **giá trị lớn nhất (Maximize)**. Giá trị của nút MAX là giá trị lớn nhất của các nút con của nó.
2.  **Người chơi MIN (Đối thủ):** Mục tiêu là tìm nước đi mang lại **giá trị nhỏ nhất (Minimize)**. Giá trị của nút MIN là giá trị nhỏ nhất của các nút con của nó.



## 2. Thuật toán

Quá trình đệ quy diễn ra từ nút gốc xuống các nút lá. Khi gặp nút lá (trạng thái kết thúc trò chơi hoặc đạt đến độ sâu tìm kiếm giới hạn), giá trị được trả về bởi **Hàm đánh giá (Evaluation Function)**. Sau đó, các giá trị này được truyền ngược lên:

 **Tại mức MAX:** Chọn giá trị Max(child1,child2,..)
 **Tại mức MIN:** Chọn giá trị Min(child1,child2,..)

Cuối cùng, tại nút gốc, người chơi MAX sẽ chọn nước đi dẫn đến giá trị cao nhất tìm được.


**THUẬT TOÁN TỐI ƯU HÓA: CẮT TỈA ALPHA-BETA (alpha-beta Pruning)**

Mặc dù Minimax có thể tìm ra nước đi tối ưu, nhưng không gian trạng thái của Cờ Caro là rất lớn ($b^d$, với $b$ là hệ số phân nhánh và $d$ là độ sâu). Với độ sâu tìm kiếm lớn, Minimax trở nên không khả thi về mặt tính toán. **Cắt tỉa Alpha-Beta** ra đời nhằm tối ưu hóa Minimax bằng cách loại bỏ các nhánh không cần thiết.

## 1. Nguyên tắc Cắt tỉa

Nguyên tắc cốt lõi là: "Nếu biết rằng một nước đi đang xét sẽ không bao giờ được chọn bởi người chơi MAX hoặc MIN (vì đã có nước đi tốt hơn được tìm thấy trước đó), thì không cần xét tiếp các nước đi con của nó nữa."

## 2. Hai ngưỡng Cắt tỉa

Thuật toán duy trì hai giá trị:

**Alpha:** Là **giá trị tốt nhất (lớn nhất)** mà người chơi MAX có thể đảm bảo được tìm thấy trên đường đi từ nút gốc đến nút hiện tại. 
Giá trị alpha luôn tăng (hoặc giữ nguyên).
**Beta:** Là **giá trị tốt nhất (nhỏ nhất)** mà người chơi MIN có thể đảm bảo được tìm thấy trên đường đi từ nút gốc đến nút hiện tại. 
Giá trị beta luôn giảm (hoặc giữ nguyên).

## 3. Điều kiện Cắt tỉa

Quá trình cắt tỉa xảy ra khi ALPHA >= BETA:

* Khi ALPHA >= BETA: tại một nút MIN, điều đó có nghĩa là người chơi MIN đã tìm thấy một nước đi ở đâu đó có giá trị beta (nhỏ hơn hoặc bằng alpha. Vì người chơi MAX sẽ không bao giờ chọn nước đi có giá trị nhỏ hơn $\alpha$, nên nhánh hiện tại (vốn có giá trị nhỏ nhất là beta) sẽ bị cắt cụt.
* Tương tự, điều kiện này giúp loại bỏ những không gian trạng thái không cần thiết, cho phép thuật toán tìm kiếm sâu hơn và nhanh hơn đáng kể.


### IV. ỨNG DỤNG TRONG CỜ CARO: HÀM ĐÁNH GIÁ (HEURISTIC)
Do độ phức tạp lớn của Cờ Caro, AI không thể tìm kiếm đến trạng thái thắng/thua cuối cùng mà phải giới hạn độ sâu. Khi đạt đến độ sâu đó, Hàm đánh giá Heuristic sẽ được sử dụng để gán điểm số cho trạng thái bàn cờ.
**Logic Tính Điểm**
Hàm đánh giá hoạt động bằng cách quét tất cả các ô trên bàn cờ, tính điểm theo 4 hướng (Ngang, Dọc, Chéo lên, Chéo xuống), và gán điểm dựa trên tiềm năng chiến thắng:
1.**Thiết lập Thang điểm**: Gán điểm số cao gấp nhiều lần cho các chuỗi có tiềm năng thắng lớn.
2.**Ưu tiên Tấn công và Phòng thủ**:
Tính tổng điểm của các chuỗi quân của AI (MAX Score).
Tính tổng điểm của các chuỗi quân của Đối thủ (MIN Score).
**Công thức Đánh giá:**
Giá trị cuối cùng của thế cờ được tính bằng cách lấy hiệu số giữa lợi thế của mình và lợi thế của đối thủ:
**Final Score = Sum ( Score Max ) -  Sum ( Score Min )**

### V.KẾT LUẬN
Việc triển khai AI Cờ Caro hiệu quả đòi hỏi sự kết hợp tối ưu giữa:
**Minimax**: Đảm bảo tính tối ưu của quyết định.Alpha-Beta: Tăng cường tốc độ tìm kiếm, cho phép AI nhìn xa hơn (tăng độ sâu $d$).Hàm đánh giá **Heuristic**: Phản ánh chính xác lợi thế chiến lược của thế cờ khi chưa đạt đến trạng thái kết thúc.









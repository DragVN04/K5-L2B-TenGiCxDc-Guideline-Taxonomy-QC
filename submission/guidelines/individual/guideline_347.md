# GUIDELINE CÁ NHÂN – DAY 07
**Guideline & Taxonomy QC – Bounding Box**

- Người thực hiện: `Hoàng Quang Trường`
- Mã thành viên: `347`
- Phiên bản: `individual_v0.1`
- Phạm vi: Rà soát và đề xuất quy tắc gán nhãn độc lập cho 40 ảnh `img_001.jpg` đến `img_040.jpg`.
- Trạng thái: Bản đề xuất cá nhân, chưa phải guideline nhóm đã thống nhất.

---

## 1. Mục tiêu và nguyên tắc gán nhãn

### 1.1. Mục tiêu

Gán bounding box cho các đối tượng thuộc taxonomy của bài tập, bảo đảm:

- Đúng lớp đối tượng.
- Bounding box bao quanh phần đối tượng nhìn thấy được.
- Không tự suy đoán phần bị che khuất hoặc nằm ngoài khung hình.
- Gán thuộc tính `occluded_level` và `truncated` nhất quán.
- Đánh dấu `can_review` khi gặp trường hợp chưa đủ căn cứ để tự quyết định.

### 1.2. Nguyên tắc chung

1. Chỉ gán các lớp được khai báo trong `submission/taxonomy.json`.
2. Mỗi đối tượng riêng biệt được gán một bounding box riêng.
3. Box phải ôm sát vùng nhìn thấy của đối tượng, không lấy cả vùng bóng đổ hoặc khoảng trống xung quanh.
4. Khi đối tượng bị che khuất, chỉ vẽ box quanh phần còn nhìn thấy; không tự vẽ phần bị che.
5. Khi đối tượng bị cắt bởi biên ảnh, chỉ vẽ phần nằm trong ảnh và đặt `truncated=yes`.
6. Không tạo box nếu chiều cao box nhỏ hơn ngưỡng `min_box_height_px = 20`.
7. Không tự thêm lớp mới hoặc thay đổi taxonomy.
8. Khi không chắc chắn về lớp hoặc cách xử lý, đánh dấu `can_review=true` và ghi lại lý do.

---

## 2. Định nghĩa lớp và ví dụ

| Lớp | Định nghĩa và trường hợp gán nhãn | Ví dụ không gán vào lớp này |
|---|---|---|
| `car` | Ô tô chở người, sedan, hatchback, coupe, SUV. Gán một box cho từng xe riêng biệt. | Xe tải, xe thùng kín cỡ nhỏ, xe máy. |
| `truck` | Xe tải có phần thân/thùng chở hàng riêng biệt, thường có cabin và khoang hàng phân biệt. | Ô tô con, SUV, van thùng kín cỡ nhỏ. |
| `van` | Xe thùng kín cỡ nhỏ, có khoang chở hàng hoặc khoang thân xe liền dạng hộp, không thể hiện cấu trúc xe tải có thùng hàng riêng. | Xe con/SUV; xe tải có thùng hàng riêng biệt. |
| `motorcycle` | Xe máy hoặc mô tô hai bánh có động cơ. Gán box riêng cho từng xe nếu phân biệt được. | Xe đạp không động cơ, ô tô, người đứng cạnh xe. |
| `person` | Người đi bộ hoặc người đang ngồi trên phương tiện. Nếu nhìn thấy người trên xe máy, gán người và xe máy thành hai đối tượng riêng khi có thể xác định được. | Hình người trên biển quảng cáo, hình nộm hoặc vật thể không đủ căn cứ xác định là người thật trong cảnh. |
| `ignore_region` | Vùng cần bỏ qua, không phải một đối tượng vật lý. Dùng theo phạm vi được reviewer/team thống nhất; không dùng thay cho box của một đối tượng chỉ vì khó gán. | Không dùng để che lỗi phân loại hoặc thay thế đối tượng bị bỏ sót. |

### 2.1. Quy tắc phân biệt các lớp dễ nhầm

**Car và van**
- Nếu hình dáng là ô tô chở người hoặc SUV: chọn `car`.
- Nếu là xe thân kín cỡ nhỏ, khoang thân dạng hộp phục vụ chở hàng: chọn `van`.
- Nếu ảnh không thể hiện đủ cấu trúc để phân biệt: không đoán theo màu sắc hoặc kích thước đơn thuần; bật `can_review`.

**Van và truck**
- `truck`: có cấu trúc cabin và thùng/khoang hàng riêng biệt.
- `van`: thân xe kín dạng hộp, thường liền khối.
- Nếu ảnh bị che khuất mạnh khiến không xác định được cấu trúc thân xe: hỏi reviewer.

**Person và motorcycle**
- Người và xe máy là hai đối tượng khác nhau.
- Không gộp người lái và xe máy thành một box.
- Nếu người bị xe hoặc vật khác che khuất, chỉ vẽ box quanh phần người nhìn thấy được.

### 2.2. Các trường hợp không thuộc taxonomy

Không tự tạo lớp cho xe buýt, xe đạp, biển báo, cây cối, nhà cửa hoặc các vật thể khác không có trong danh sách lớp.

Không tự động đổi các đối tượng này thành `ignore_region`. Chỉ tạo vùng ignore khi có căn cứ rằng khu vực đó thuộc trường hợp cần bỏ qua theo quy tắc được nhóm/reviewer xác nhận.

---

## 3. Quy tắc bounding box

### 3.1. Cách vẽ box

- Box theo hình chữ nhật song song với cạnh ảnh.
- Mép trái, phải, trên, dưới bám theo phần đối tượng nhìn thấy.
- Không lấy bóng đổ làm một phần của box.
- Không gộp nhiều đối tượng cùng lớp vào một box.
- Không kéo box sang đối tượng khác chỉ vì chúng nằm sát nhau.
- Đối tượng bị che một phần: box chỉ bao phần nhìn thấy, không ước lượng phần bị che.
- Đối tượng chạm biên ảnh: box dừng tại biên ảnh.

### 3.2. Đối tượng nhỏ

Theo taxonomy:
- `min_box_height_px = 20`.

Quy tắc đề xuất:
- Chiều cao box từ 20 px trở lên: có thể gán nếu nhận diện được đối tượng.
- Chiều cao box dưới 20 px: không tạo box theo ngưỡng tối thiểu.
- Nếu đối tượng nằm sát ngưỡng hoặc không thể xác định chính xác kích thước do mờ/che khuất: đánh dấu `can_review` và ghi lý do.
- Không tự tạo `ignore_region` chỉ để thay thế một đối tượng nhỏ.

### 3.3. Nhiều đối tượng chồng lấn

- Nếu phân biệt được từng đối tượng: tạo box riêng cho từng đối tượng.
- Nếu một đối tượng che một phần đối tượng khác: vẫn gán đối tượng phía sau nếu phần nhìn thấy đủ căn cứ nhận diện và đạt ngưỡng kích thước.
- Nếu không thể xác định số lượng hoặc ranh giới đối tượng: đánh dấu `can_review`.

---

## 4. Thuộc tính và ngưỡng đo

### 4.1. `occluded_level`

Ý nghĩa: mức độ diện tích đối tượng bị **đối tượng khác che khuất**. Không tính phần bị cắt do biên ảnh vào mức che khuất.

Đề xuất chia mức theo tỷ lệ diện tích bị che trên diện tích toàn bộ đối tượng ước lượng:

| Giá trị | Tỷ lệ diện tích bị che | Cách hiểu |
|---|---:|---|
| `0` | 0% | Không bị đối tượng khác che khuất. |
| `1` | Trên 0% đến 25% | Che khuất nhẹ; phần lớn đối tượng còn nhìn thấy. |
| `2` | Trên 25% đến 50% | Che khuất trung bình; khoảng một phần tư đến một nửa đối tượng bị che. |
| `3` | Trên 50% | Che khuất nặng; hơn một nửa diện tích đối tượng bị che. |

Cách ước lượng:
- Ước lượng diện tích hình dáng đầy đủ của đối tượng dựa trên phần còn nhìn thấy và cấu trúc có thể quan sát.
- Tính tỷ lệ phần bị vật thể khác che khuất so với diện tích toàn bộ ước lượng.
- Không dùng tỷ lệ diện tích box bị che thay cho tỷ lệ diện tích đối tượng nếu box chứa nhiều khoảng trống.
- Nếu không đủ căn cứ ước lượng do che khuất quá nặng, đánh dấu `can_review=true`.

**Lưu ý:** Các khoảng phần trăm trên là đề xuất cá nhân để làm rõ bốn mức `0–3` đang có trong taxonomy; cần reviewer xác nhận trước khi áp dụng thành quy tắc nhóm.

### 4.2. `truncated`

Ý nghĩa: đối tượng bị cắt bởi biên khung hình.

| Giá trị | Điều kiện |
|---|---|
| `no` | Toàn bộ phạm vi đối tượng nằm trong khung hình; không có phần đối tượng bị biên ảnh cắt mất. |
| `yes` | Có ít nhất một phần đối tượng bị cắt bởi một trong bốn biên ảnh: trái, phải, trên hoặc dưới. |

Quy tắc:
- Chỉ tính cắt bởi biên ảnh, không tính che khuất bởi xe khác hoặc vật thể khác.
- Nếu đối tượng bị che bởi xe khác nhưng vẫn nằm trọn trong khung ảnh: `truncated=no`.
- Nếu đối tượng vừa bị che vừa bị biên ảnh cắt: gán `occluded_level` theo phần bị che và `truncated=yes`.
- Box chỉ bao phần đối tượng còn nằm trong ảnh.

### 4.3. `can_review`

Đặt `true` khi:
- Không đủ căn cứ phân biệt `car`, `van`, `truck`.
- Không xác định được một hay nhiều đối tượng do chồng lấn.
- Đối tượng bị che khuất quá nặng, không thể xác định hình dáng hoặc thuộc tính.
- Không rõ đối tượng có thuộc taxonomy hay không.
- Có tình huống chưa được quy định rõ trong guideline.

Không bật `can_review` chỉ vì thao tác vẽ box khó hoặc mất thời gian nếu quy tắc đã rõ.

---

## 5. Ca khó

**Nguyên tắc phân loại:** 
- “Xử lý theo quy tắc” là trường hợp có thể áp dụng quy tắc hiện có, không cần tự bổ sung định nghĩa mới.
- “Cần hỏi reviewer” là trường hợp còn thiếu căn cứ hoặc cần nhóm thống nhất cách diễn giải.

### 5.1. Ca xử lý theo quy tắc

| Mã ảnh | Tình huống quan sát | Quyết định | Lý do |
|---|---|---|---|
| `[điền mã ảnh sau khi rà soát]` | Xe bị một vật thể khác che một phần nhưng vẫn nhận diện được lớp và phần còn nhìn thấy. | Gán box quanh phần nhìn thấy; đặt `occluded_level` theo tỷ lệ ước lượng; `truncated=no` nếu không chạm biên ảnh. | Che khuất bởi vật thể khác không đồng nghĩa với bị cắt bởi biên ảnh. |
| `[điền mã ảnh sau khi rà soát]` | Xe hoặc người bị biên ảnh cắt mất một phần. | Gán box trong phạm vi ảnh; `truncated=yes`. | Đối tượng bị cắt bởi biên khung hình. |
| `[điền mã ảnh sau khi rà soát]` | Người đang ngồi hoặc lái xe máy. | Gán `person` và `motorcycle` thành hai box riêng nếu phần nhìn thấy đủ căn cứ. | Taxonomy định nghĩa `person` bao gồm người ngồi trên xe; xe máy vẫn là đối tượng riêng. |
| `[điền mã ảnh sau khi rà soát]` | Nhiều xe cùng lớp nằm sát nhau nhưng vẫn nhìn thấy ranh giới từng xe. | Vẽ box riêng cho từng xe. | Không gộp nhiều đối tượng vào một box. |
| `[điền mã ảnh sau khi rà soát]` | Đối tượng nhìn thấy rõ nhưng box có chiều cao dưới 20 px. | Không tạo box theo ngưỡng tối thiểu; ghi nhận nếu trường hợp sát ngưỡng cần reviewer xem xét. | Taxonomy quy định `min_box_height_px = 20`. |

### 5.2. Ca cần hỏi reviewer

| Mã ảnh | Tình huống quan sát | Quyết định tạm thời | Lý do cần reviewer |
|---|---|---|---|
| `[điền mã ảnh sau khi rà soát]` | Xe thân kín bị che phần lớn, không rõ là van hay truck. | Không tự đoán lớp; bật `can_review=true`. | Thiếu bằng chứng về cấu trúc cabin và khoang hàng. |
| `[điền mã ảnh sau khi rà soát]` | Nhiều người/xe chồng lấn mạnh, không xác định chắc số lượng đối tượng. | Ghi nhận vùng và bật `can_review`. | Có nguy cơ gán thiếu hoặc tạo box trùng. |
| `[điền mã ảnh sau khi rà soát]` | Vật thể nhỏ, mờ hoặc bị che đến mức không xác định được có thuộc lớp nào. | Bật `can_review`, không tự tạo lớp mới. | Chưa đủ căn cứ nhận diện đối tượng. |
| `[điền mã ảnh sau khi rà soát]` | Khu vực có nhiều vật thể không thể tách riêng và có khả năng cần dùng `ignore_region`. | Chưa tự tạo vùng ignore; hỏi reviewer. | Taxonomy có lớp ignore nhưng cần thống nhất điều kiện sử dụng và phạm vi vùng. |
| `[điền mã ảnh sau khi rà soát]` | Không thể ước lượng đáng tin cậy phần diện tích bị che để chọn `occluded_level`. | Bật `can_review`. | Cần thống nhất cách xử lý trường hợp không đủ căn cứ đo mức che khuất. |

**Ghi chú bắt buộc khi hoàn thiện:** Thay từng ô `[điền mã ảnh sau khi rà soát]` bằng mã `img_001` đến `img_040` đúng với ảnh thực tế. Chỉ giữ lại những dòng có tình huống thật sự xuất hiện trong bộ dữ liệu. Không gán mã ảnh theo suy đoán.

---

## 6. QC và phiên bản

### 6.1. Ngưỡng QC áp dụng

| Chỉ số | Ngưỡng trong taxonomy |
|---|---:|
| Chiều cao box tối thiểu | 20 px |
| IoU threshold cho box lớn | 0.85 |
| IoU threshold cho box nhỏ | 0.70 |
| Ngưỡng phân loại box lớn | 50 px |
| IAA mean IoU | ≥ 0.85 |
| IAA class agreement | ≥ 0.95 |
| Error rate tối đa mỗi ảnh | 0.02 |
| Match IoU | 0.50 |

Các ngưỡng trên được giữ nguyên theo `submission/taxonomy.json`; không tự thay đổi trong guideline cá nhân.

### 6.2. Các lỗi cần tự kiểm tra trước khi nộp

- Sai lớp giữa `car`, `truck`, `van`.
- Bỏ sót đối tượng đủ điều kiện gán nhãn.
- Gộp nhiều đối tượng vào một box.
- Box quá rộng hoặc quá hẹp so với phần đối tượng nhìn thấy.
- Box vượt ra ngoài kích thước ảnh.
- Nhầm `occluded_level` với `truncated`.
- Không đánh dấu `can_review` ở trường hợp chưa đủ căn cứ.
- Tự dùng `ignore_region` khi chưa có quy tắc rõ ràng.

### 6.3. Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| individual_v0.1 | Tạo guideline cá nhân; hệ thống hóa định nghĩa lớp, box, thuộc tính và cách phân loại ca khó. | Chuẩn bị đối chiếu guideline giữa các thành viên. |
| individual_v0.2 | `[bổ sung sau khi reviewer phản hồi]` | `[ghi rõ ca ảnh và nội dung thay đổi]` |

---

## 7. Các câu hỏi đề nghị reviewer/team xác nhận

1. Có thống nhất dùng các khoảng phần trăm 0%, 1–25%, 26–50%, trên 50% cho `occluded_level` không?
2. Điều kiện cụ thể để tạo `ignore_region` là gì? Có cần áp dụng cho vùng đông người/xe không thể tách đối tượng không?
3. Đối tượng có chiều cao box dưới 20 px sẽ bỏ qua hoàn toàn hay có ngoại lệ?
4. Khi không phân biệt được `truck` và `van` do ảnh mờ/che khuất, có thống nhất bật `can_review` thay vì tự chọn lớp không?
5. Khi một đối tượng vừa bị che khuất vừa bị cắt bởi biên ảnh, có thống nhất gán đồng thời `occluded_level` và `truncated` không?

**Kết luận cá nhân:** Ưu tiên tính nhất quán và khả năng kiểm chứng. Những trường hợp đã có quy tắc thì áp dụng trực tiếp; những trường hợp chưa có căn cứ thì ghi nhận và chuyển reviewer, không tự tạo quy tắc riêng trong quá trình gán nhãn.
# Guideline gán nhãn — <phiên bản> — <mã hoặc nhóm>

> Copy file này (hoặc `guideline_v0_starter.md`) rồi viết. Một guideline đủ gồm **5 phần**. Câu nào của v0
> làm hai người đọc ra hai cách khác nhau thì phải viết lại cho một cách hiểu duy nhất.

- Phiên bản: v0
- Ngày: 16/11/2026
- Người viết / duyệt: Cao Quy Binh

## 1. Mục tiêu
Mô hình nào dùng nhãn này, để làm gì, sai ở đâu thì nguy hiểm.

## 2. Lớp và thuộc tính
### Lớp
| Lớp | Định nghĩa |
|---|---|
| `car` | Ô tô con. |
| `truck` | Xe tải. |
| `van` | Xe thùng kín cỡ nhỏ. |
| `motorcycle` | Xe máy, mô tô. |
| `person` | Người. |
| `ignore_region` | Vùng không cần gán từng vật. |

Vật **không thuộc lớp nào** thì không gán.

### Thuộc tính
| `occluded_level` | `0`, `1`, `2`, `3` | Mức bị che: 0 là thấy rõ, 1 là bị che ít (~20%), 2 là bị che nhiều (~50%), 3 là không rõ.(~80%) |
| `truncated` | `no`, `yes` | Vật bị cắt ở mép ảnh. |
| `can_review` | tick / không | Tick khi bạn không chắc, để người khác xem lại. |

## 3. Quy tắc vẽ box
Box ôm sát phần nhìn thấy; vật bị che; vật bị cắt mép ảnh; phản chiếu / hình in / tượng / đồ chơi; xe chủ (ego), vật quá nhỏ, đám đông thì không vẽ box một vật có nhiều phần (người và xe) vẽ box riêng cho từng vật thể

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_005 | 2 người bị che khuất| R-01 |Không gắn box | Bị che nhiều (>50%)|
| img_006 | Nhiều người bị che khuất|R-02 |Không gắn box | Bị che nhiều (>50%)|
| img_014 | Nhiều vật thể bị mờ, không rõ hình dạng|R-03 |Không gắn box | Bị che nhiều (>50%)|
| img_017 | Tượng hình người|R-04 |Không gắn box | Không phải person|


| `img_029` | Xe máy chở một chiếc xe đạp + vật nặng, 2 người | R-02 | Gán `motorcycle` + 2 `person`; chưa gán chiếc xe đạp được chở | Phụ thuộc quyết định về lớp `bicycle` ở dòng trên. Nếu nhóm thêm `bicycle` thì theo R-02 phải gán thêm 1 box |
| `img_003` | Một chiếc xe đạp lớn ở góc trái (chạm mép, h ≈ 371 px) | R-07, 4.2 | Tạm `ignore_region` | Cùng quyết định `bicycle`. Nếu thêm lớp thì phải gán, và `truncated = yes` |
| `img_020` | Ảnh chụp qua gương bên xe | R-06, R-08 | Ảnh rỗng | Nhóm có đồng ý không gán phần thân xe của người chụp không? Nếu có, ảnh này đổi từ "rỗng" sang "có 1 `car`" |
| `img_027` | Tượng xe bán tải (đã quyết "không gán" ở 4.1) | R-05 | Không gán | Nhóm xác nhận giúp: tượng có hình dáng xe là không gán, trong khi mọi người dễ gán `truck` |
| `img_013` | Xe ở rất xa (22–29 px), nhiều đèn | R-04 | Gán `car` + `can_review` | Có chấp nhận box 22 px không, hay nâng ngưỡng riêng cho xe ở xa? |

Cách xử lý chung khi chưa có câu trả lời: tick `can_review` trên box, ghi 1 dòng vào
`submission/qc/image_issues.csv` với `image,annotator,region,note`, và không tự ý đổi nghĩa quy tắc.

---

## 5. QC và phiên bản

### 5.1 Ngưỡng QC áp dụng (lấy từ `submission/taxonomy.json → rules`, không tự đặt)

| Ngưỡng | Giá trị | Dùng để |
|---|---|---|
| `min_box_height_px` | 20 |vật thấp hơn ngưỡng thì không gán |
| `match_iou` | 0.5 | Ghép cặp box giữa hai annotator khi đo IAA |
| `iou_thr_large` | 0.85 | Ngưỡng IoU khi so sánh cho box lớn (chiều cao trung bình ≥ `large_px`) |
| `iou_thr_small` | 0.70 | Ngưỡng IoU khi so sánh cho box nhỏ |
| `large_px` | 50 | Ngưỡng phân biệt box lớn / nhỏ |
| `iaa_iou` | 0.85 | IAA IoU mục tiêu |
| `iaa_class` | 0.95 | Đồng thuận lớp mục tiêu |
| `error_rate_img_max` | 0.02 | Tỉ lệ ảnh có lỗi tối đa |

Lưu ý quan trọng: ngưỡng IoU cho box lớn là 0.85 — rất chặt. Điều này cấm để dư nền và cấm
cắt vật thể, đúng như R-10. Ngưỡng cho box nhỏ (0.70) dễ hơn vì 1–2 px lệch ở box 25 px là 8% IoU.

### 5.2 Ai quyết ca mơ hồ

- Người gán tick `can_review` hoặc ghi `image_issues.csv`.
- Người chốt là một thành viên có mã của nhóm, ghi vào `submission/qc/calibration_decisions.csv`
  với đủ: `case_id`, `image`, `quyet_dinh`, `quy_tac_ghi_vao_guideline` (mã `R-xx`),
  `phien_ban_guideline`, `nguoi_chot`, `phieu_sua`, `kiem_lai`, `pham_vi` (`anh` hay `lo`).
- Quyết định `pham_vi = lo` (đổi nghĩa quy tắc) bắt buộc kiểm lại cả lô, không chỉ ảnh đó.
- Với 4.2, nếu nhóm thêm lớp mới (`bus`, `bicycle`, `rickshaw`) thì phải sửa `taxonomy.json`
(tăng `version`, ghi cách rà lại) và sinh lại `cvat/labels_generated.json`.

### 5.3 Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1 | Bản cá nhân đầu tiên: định nghĩa 5 lớp + `ignore_region`, 13 quy tắc `R-01`–`R-13`, 25 ca loại theo quy tắc, 13 ca cần hỏi reviewer | Pha 1, xem đủ 40 ảnh |
| (v1.0) | Chưa có — sẽ do nhóm chốt ở Pha 2 | Phải giải quyết trước hết: lớp `bus`/`bicycle`/`rickshaw` (4.2), ranh giới `truck`↔`van` (`img_036`, `img_037`), mascot (`img_011`), sidecar (`img_022`) |
| (v1.1) | Chưa có — sẽ sinh sau calibration ở Pha 5 | Sẽ ghi lại quyết định cho từng ca trong `calibration_decisions.csv` |
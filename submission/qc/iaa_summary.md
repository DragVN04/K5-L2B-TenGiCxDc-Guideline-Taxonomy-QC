# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **100/100**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 764 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 80 | 764 | 0.888 | 98.7% | 55.0% | 97.1% | 229/182 | 0 | ĐẠT |
| 043|044 | 14 | 149 | 0.778 | 98.0% | 37.6% | 94.0% | 63/56 | 0 | CHƯA ĐẠT |
| 043|065 | 14 | 109 | 0.777 | 98.2% | 22.0% | 95.4% | 66/51 | 0 | CHƯA ĐẠT |
| 043|067 | 12 | 96 | 0.776 | 100.0% | 30.2% | 97.9% | 67/41 | 0 | CHƯA ĐẠT |
| 044|065 | 13 | 151 | 0.981 | 100.0% | 70.2% | 98.7% | 4/18 | 0 | ĐẠT |
| 044|067 | 13 | 170 | 0.993 | 98.8% | 70.0% | 98.2% | 14/15 | 0 | ĐẠT |
| 065|067 | 14 | 89 | 0.968 | 96.6% | 96.6% | 98.9% | 15/1 | 0 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 1918 ({'bo_sot_thua': 388, 'co_can_review': 884, 'iou_thap': 215, 'sai_thuoc_tinh': 352, 'bat_dong_ignore': 69, 'sai_lop': 10}), trên 35 ảnh cần calibration.

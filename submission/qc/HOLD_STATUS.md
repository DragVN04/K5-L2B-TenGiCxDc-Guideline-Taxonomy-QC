cat > submission/qc/HOLD_STATUS.md <<'EOF'

# Báo cáo trạng thái HOLD — Day 07

## 1. Phạm vi đã thực hiện

Nhóm đã xây dựng guideline, taxonomy, thực hiện gán nhãn độc lập trên CVAT, xuất nhãn COCO và chạy công cụ đánh giá IAA.

Các tệp COCO hiện có gồm 043, 044, 065 và 067. Việc kiểm tra cấu trúc bằng validate_labels.py đã thành công theo phân công hiện tại.

## 2. Kết quả IAA

- Số ảnh được so sánh: 40
- Số thành viên đã tham gia gán nhãn: 4
- Lượt gán hoàn thành theo phân công hiện tại: 100/100
- Số cặp bounding box được ghép: 764
- Mean IoU: 0.888
- Đồng thuận class: 98.7%
- Đồng thuận occluded_level: 55.0%
- Số ca bất đồng được phát hiện: 1918
- Số ảnh được đánh dấu cần Calibration: 35

Kết quả tổng thể đạt ngưỡng IAA của công cụ, nhưng vẫn còn nhiều bất đồng về bounding box, đối tượng bị bỏ sót và thuộc tính.

## 3. Calibration chưa hoàn thành

Nhóm đã tạo các tệp:

- calibration_candidates.csv
- calibration_decisions.csv
- calibration_context.json
- consensus_draft.json

Các quyết định Calibration chưa được xác minh và điền đầy đủ. Nhóm chưa hoàn tất sửa nhãn trong CVAT.

Do đó, chưa tạo được bộ nhãn cuối cùng và batch_manifest.json.

## 4. QC chưa hoàn thành

Chưa thực hiện vòng QC chính thức vì chưa có bộ nhãn cuối sau Calibration.

Chưa có kết quả kiểm tra đủ điều kiện Release. Các tỷ lệ lỗi QC cuối cùng chưa được xác định.

## 5. Quyết định

Trạng thái: HOLD.

Lý do: Chưa hoàn thành xử lý các bất đồng IAA và chưa có đủ bằng chứng Calibration, QC để bàn giao bộ nhãn đạt chuẩn.

Không tuyên bố bộ nhãn hiện tại đã đạt QC hoặc đủ điều kiện Release.

## 6. Công việc còn lại

1. Xác nhận đầy đủ phân công nhóm, bao gồm yêu cầu ba người gán mỗi ảnh nếu nhóm có năm thành viên.
2. Xem xét và xác nhận các ca bất đồng.
3. Hoàn thiện guideline v1.1 và bảng quyết định Calibration.
4. Sửa nhãn, xuất COCO và tạo bộ nhãn cuối.
5. Thực hiện QC và đánh giá Release/Hold/Rework.

## 7. Bằng chứng đính kèm

- submission/qc/iaa_summary.md
- submission/qc/iaa_summary.json
- submission/qc/calibration_candidates.csv
- submission/qc/calibration_decisions.csv
- submission/qc/assignment.csv
- submission/labels/
- submission/guidelines/

Báo cáo này ghi nhận tiến độ thực tế và các giới hạn chưa giải quyết tại thời điểm nộp.
EOF

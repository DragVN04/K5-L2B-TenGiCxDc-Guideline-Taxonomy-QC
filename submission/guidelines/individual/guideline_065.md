# Guideline gán nhãn — v0.1 (bản cá nhân, Pha 1) — 065

> Bản cá nhân viết độc lập sau khi xem đủ 40 ảnh trong `data/images/`.
> Mục tiêu: mọi người đọc file này đều dự đoán cùng số box và cùng lớp cho cùng một ảnh.

- Phiên bản: v0.1 (bản cá nhân — chưa phải v1.0 của nhóm)
- Ngày: 16/11/2026
- Người viết: 065
- Loại nhãn: bounding box (hộp chữ nhật) trên ảnh đường phố
- Công cụ: CVAT, xuất COCO 1.0

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình phát hiện người và phương tiện trên ảnh đường phố
(camera giao thông / xe tự lái). Mô hình sau này phải:

- biết có bao nhiêu người và bao nhiêu phương tiện trong cảnh,
- biết vị trí chính xác của từng vật thể (dùng cho cảnh báo va chạm, đếm lưu lượng),
- phân biệt được người với phương tiện khi chúng chồng lên nhau.

Nguy hiểm khi sai:

| Sai lệch | Hậu quả |
|---|---|
| Gộp "người + xe máy" thành 1 box | Mô hình không đếm được số người đang đi xe → sai số lượng người trên đường |
| Bỏ sót chiếc xe được xe chở | Mô hình không biết có xe "đang bay" trên sàn xe tải → ảo vật |
| Gán tượng / đồ chơi / ảnh in là vật thật | Mô hình học "người giống hình" thành người, sinh cảnh báo giả |
| Box quá lỏng (thừa nền) | IoU thấp, hộp khớp sai, mô hình học vị trí lệch |
| Bỏ sót vật quá nhỏ ở xa | Tùy dụng ích: đường phố xa có thể chấp nhận, nhưng phải ghi nhận, không được im lặng |

Nguyên tắc chung: mọi quyết định phải truy được về một câu trong file này.
Câu nào chưa đủ rõ thì tick `can_review` hoặc ghi vào `submission/qc/image_issues.csv`.

---

## 2. Lớp và thuộc tính

### 2.1 Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ trong bộ 40 ảnh | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe 4 bánh chở khách, thân kín (sedan, hatchback, SUV, wagon), kể cả xe cổ. | `img_015` (ô tô đậu dưới mưa), `img_024` (AMC Pacer cổ), `img_040` (ô tô ở ngã tư Bangkok), `img_002` (ô tô trên sàn xe chở) | Không phải `truck` (bán tải/xe tải có thùng), không phải `van` (thùng kín), không phải `bus` |
| `truck` | Xe có thùng hàng riêng tách rời cabin: bán tải (pickup), xe tải thùng, xe tải chở xe, xe chở trọng. | `img_001` (bán tải trước quán ăn), `img_012` (bán tải chở rau), `img_002` (Renault 380 chở ô tô), `img_007` (xe tải trong kho) | Không phải `car`; bán tải luôn là `truck` kể cả khi thùng trống |
| `van` | Xe thùng kín cỡ nhỏ, không có thùng hàng mở: minivan, xe tải thùng kín nhỏ, xe buýt nhỏ. | `img_036` (CMC Veryca — đang cần reviewer chốt), `img_037` (pickup có rùa — đang cần reviewer chốt) | Ranh giới với `truck` và `bus` là điểm yếu của taxonomy v0 → xem mục 4.2 |
| `motorcycle` | Xe 2 bánh có động cơ: xe máy, mô tô, scooter. | `img_005`, `img_008`, `img_021`, `img_030`, `img_016`, `img_040` | Không phải xe đạp/cyclo (chưa có lớp), không phải ô tô 3 bánh, không phải xe máy tượng/mô hình |
| `person` | Con người thật: đi bộ, đứng, ngồi, lái xe, làm hàng. Kể cả người đội mũ bảo hiểm, mặc áo khoác, ngồi trên xe. | `img_014` (2 người qua đường Sài Gòn), `img_005` (người lái xe máy), `img_032` (hàng người chờ xe buýt), `img_026` (2 người trên 1 xe máy) | Không phải tượng, mannequin, người trong ảnh in/biển quảng cáo, người trên billboard |
| `ignore_region` | Vùng không gán từng vật: gom nhiều vật quá nhỏ/không tách được, hoặc vùng có vật không thuộc lớp nào mà nhóm đã chốt bỏ qua. | Dãy xe đạp/cyclo xa ở `img_006`, `img_009`, `img_034`, `img_039` | Không dùng `ignore_region` để che lỗi bỏ sót. Một vùng bỏ sót có thật phải được báo ở `image_issues.csv` |

Vật không thuộc lớp nào thì làm gì? (xe buýt, xe đạp, cyclo, tuk-tuk/ô tô 3 bánh, ngựa, vali, cây, đồ chơi, tượng)

1. Nếu vật là người thật hoặc phương tiện thật nhưng chưa có lớp → không tự ý map sang lớp gần giống.
   Đề xuất `ignore_region` bao quanh vùng đó, đồng thời ghi 1 dòng vào `submission/qc/image_issues.csv`
   (`image,annotator,region,note`) và đề xuất thêm lớp mới ở v1.0.
2. Nếu vật không phải vật thật (tượng, đồ chơi, ảnh in) → không gán gì cả, không cần `ignore_region`.
3. Mọi quyết định ở mục 4.2 (cần reviewer) đều chờ quyết định của nhóm ở Pha 2 trước khi gán.

### 2.2 Thuộc tính

#### `occluded_level` (select) — đo theo tỉ lệ diện tích khung bao quanh vật thể bị che

| Mức | Ngưỡng cụ thể | Nghĩa | Ví dụ trong bộ 40 ảnh |
|---|---|---|---|
| `0` | Che 0% | Thấy rõ toàn bộ | Người đứng trước nền trời ở `img_032` |
| `1` | Che < 30% | Bị che ít, vẫn nhận ra rõ là ai/vật gì | Người bị bánh xe khác che một phần chân ở `img_021`; người bị cành/cột che ở `img_001` |
| `2` | Che 30% – 60% | Bị che nhiều, nhận ra được nhưng không rõ chi tiết | Hành khách sau người lái ở `img_026`; người trong ô tô 3 bánh ở `img_035` |
| `3` | Che > 60% hoặc không xác định được vật thể | Gần như không thấy, chỉ suy đoán | Người bị kín sau thùng xe ở `img_003` |

Cách đo: ước lượng khung hình chữ nhật bao trọn vật thể (nếu vật thể không bị che thì khung = tầm nhìn đầy đủ),
rồi tính phần diện tích của khung đó bị vật khác lấp. Không có công cụ đo pixel trong CVAT → dùng mắt và
ghi rõ vào `image_issues.csv` nếu hai người có thể lệch 1 mức.

#### `truncated` (select) — `no` / `yes`

- `yes` nếu vật thể bị cắt bởi mép ảnh (một phần vật nằm ngoài khung ảnh).
- `no` nếu vật thể nằm trọn trong ảnh, kể cả sát mép ảnh.
- Không dùng `truncated` để mô tả vật bị che bởi vật khác (việc đó là `occluded_level`).

Ví dụ rõ ràng: `img_001` (bán tải chạm mép phải), `img_003` (vật chạm cả 4 mép),
`img_005`, `img_012`, `img_015`, `img_016`, `img_021`, `img_026` (xe máy chạm mép dưới), `img_036`, `img_040`.

#### `can_review` (checkbox)

- Tick khi không chắc: đúng lớp không, số box có đủ không, hay ranh giới box.
- Tick khi ca thuộc mục 4.2 (đang chờ reviewer).
- Tick khi vật ở sát ngưỡng kích thước (mục R-04).
- Không tick chỉ vì "cảm giác" chung chung; phải ghi rõ lý do trong `image_issues.csv`.

---

## 3. Quy tắc vẽ box

Mỗi quy tắc có mã `R-xx` để tra cứu nhanh trong nhật ký QC và trong bảng quyết định calibration.

### R-01 — Người đi xe máy: 2 box (rider + motorcycle)

Ảnh có người lái xe máy thì chắc chắn có 2 box:

1. Một box `person` cho rider (bao phần thân + đầu của người đó, kể cả mũ bảo hiểm, không bao cả xe).
2. Một box `motorcycle` cho chiếc xe (bao trọn bánh xe, yên, gương, đèn).

Hai box được phép chồng nhau ở phần người ngồi trên xe — đây là bình thường, không phải lỗi.

- Không gộp "người + xe" thành 1 box.
- Không vẽ 1 box bao cả người lẫn xe.
- Nếu có hành khách ngồi sau: thêm 1 box `person` nữa (hành khách bị che nhiều → `occluded_level` 2–3).
- Người đứng bên xe (không đi xe) cũng gán `person` riêng, không gộp vào box xe.
- Người đi bộ phía sau xe máy vẫn gán `person` riêng.

Ví dụ phải ra 2 box (hoặc 3 nếu có hành khách): `img_005`, `img_008`, `img_010`, `img_016`, `img_021`, `img_029`, `img_030`, `img_040`.
Ví dụ phải ra 3 box (2 người + 1 xe): `img_026` (cặp đôi trong hầm), `img_029` (2 người + xe máy chở vật).

### R-02 — Xe chở xe: gán cả xe chở lẫn xe được chở

Khi một phương tiện chở một phương tiện khác:

- Xe chở (xe tải chở ô tô, sàn xe) → gán `truck` (hoặc lớp của chính nó).
- Từng chiếc xe được chở → gán riêng `car` / `motorcycle` / `truck` theo lớp của nó.
- Không gộp các xe con thành 1 box bao cả cả đàn.
- Không gộp chiếc xe được chở vào box của xe chở.

Ví dụ: `img_002` (Renault 380 chở ô tô) → 1 `truck` + 8 `car`.
Các ảnh khác có thể bị ảnh hưởng nếu đổi quy tắc này: `img_029` (xe máy chở xe đạp), `img_035` (ô tô 3 bánh chở hàng), `img_028` (ngựa trên thùng xe tải).

### R-03 — Người (và vật) bị che: vẫn gán, ôm sát phần nhìn thấy

- Không bỏ sót vật thể chỉ vì bị che.
- Box ôm phần nhìn thấy của vật thể, không suy diễn vẽ phần bị khuất.
- Đặt `occluded_level` theo mục 2.2.
- Nếu che > 60% mà vẫn chắc là có vật thể → vẫn gán, `occluded_level = 3`, tick `can_review`.

Ví dụ: `img_003` (người bị xe máy ở giữa che), `img_005`, `img_021`, `img_026`, `img_035`, `img_001` (người sau cành/cột).

### R-04 — Vật quá nhỏ: bỏ nếu chiều cao box < 20 px

Ngưỡng lấy từ `taxonomy.json → rules.min_box_height_px = 20`.

- Ước lượng chiều cao box trước khi quyết định. `< 20 px` → không gán.
- `≥ 20 px` → gán bình thường.
- Sát ngưỡng (18–24 px) → gán + tick `can_review`, vì hai người sẽ dễ lệch 1–2 px và lệch quyết định.
- Vật bị bỏ sót vì nhỏ vẫn phải được ghi vào `submission/qc/image_issues.csv` nếu mình tin chắc đó là vật thật.

Ví dụ: `img_003` (nhiều người/xe máy nền ở rìa trên, h 14–18 px), `img_009` (hàng người trên xe buýt, h 11–21 px),
`img_025` (người xa trên bãi biển, 8 người h < 20 px), `img_031` (đường đêm, người h 9–19 px),
`img_034`, `img_039`, `img_013` (xe xa 22–29 px).

### R-05 — Vật không phải thật: tượng, mannequin, người trong ảnh in, đồ chơi → không gán

Chỉ gán người thật và phương tiện thật.

| Ảnh | Vật không thật | Quyết định |
|---|---|---|
| `img_017` | Tượng người cưỡi ngựa | Không gán `person` |
| `img_027` | Tượng xe bán tải trong nghĩa trang | Không gán `truck` |
| `img_033` | Mannequin trong cửa hàng | Không gán `person` |
| `img_018` | Người in trên biển quảng cáo | Không gán `person` ở biển |
| `img_038` | Kệ mô hình xe đồ chơi | Không gán 25 `car` |
| `img_019` | Xe đồ chơi trong diễn hành | Không gán `car` (khán giả thật thì vẫn gán `person`) |
| `img_011` | Người hóa trang "Predator" | Cần reviewer (xem 4.2) |

Lưu ý: `img_017` là ca dễ sai nhất — hai người có thể cùng vẽ `person` ở tượng và IAA vẫn rất cao,
nhưng cả hai đều sai quy tắc. Không được dùng IAA cao làm cớ cho một quyết định sai.

### R-06 — Phản chiếu: không gán vật phản chiếu

Vật chỉ xuất hiện qua gương / kính / mặt nước → không gán. Chỉ gán vật thật đang tồn tại trong không gian.

Ví dụ: `img_020` (cầu vồng trong gương xe) → ảnh không có vật thể nào để gán → ảnh rỗng trong COCO.

### R-07 — Vật bị cắt mép ảnh: `truncated = yes`, box chạm mép

- Box chạm mép ảnh ở chỗ vật thể bị cắt → `truncated = yes`.
- Box vẫn ôm sát phần nhìn thấy trong ảnh.
- Vật sát mép ảnh nhưng trọn vẹn trong ảnh → `truncated = no`.

### R-08 — Xe chủ (ego vehicle): không gán

Phần thân xe của người đang chụp, và mọi thứ thấy qua gương xe của người chụp → không gán.
Ví dụ: `img_020` (ảnh chụp qua gương bên).

### R-09 — Đám đông / hàng người: gán từng người một box

- Mỗi người 1 box `person`. Không gán 1 box bao cả đám.
- Người đứng sát nhau, chồng lên nhau vẫn là các box riêng; dùng `occluded_level` để mô tả mức che.
- Ví dụ: `img_032` (hàng người chờ xe buýt), `img_021`, `img_025`, `img_019`.

### R-10 — Box bao sát, không cắt vật thể

- 4 cạnh box ôm sát vật thể, kể cả các bộ phận nhỏ: bánh xe, gương xe, yên, quai ba lô, tay.
- Không cắt vật thể: cạnh box không được đi qua giữa bánh xe, qua nửa thân người, hay qua đèn xe.
- Không để dư nền quá 2–3 px mỗi cạnh (nếu để dư nhiều, IoU khi so sánh sẽ tụt).
- Box `person` của rider không được bao cả xe; box `motorcycle` không được cắt ngang người lái.

### R-11 — Phương tiện đứng yên vẫn được gán

Xe đậu, xe trưng bày trong triển lãm, xe không có người lái → vẫn gán, vẫn tính vào số vật thể.
Ví dụ: `img_011` (xe máy trưng bày trong lễ hội), `img_015`, `img_024`, `img_030` (xe xếp hàng).

### R-12 — Ảnh không có vật thể nào thuộc phạm vi → ảnh rỗng

Ảnh vẫn phải xuất hiện trong file COCO, chỉ là không có annotation nào. Không được xóa ảnh khỏi Task.

### R-13 — Bán tải (pickup) luôn là `truck`

Có thùng hàng mở phía sau, tách khỏi cabin → `truck`, kể cả thùng trống, kể cả đang đậu.
Ví dụ: `img_001`, `img_012`, `img_007`, `img_037`.

---

## 4. Ca khó

### 4.1 Ca loại theo quy tắc (đã tự quyết được, không cần hỏi reviewer)

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe tải chở ô tô (Renault 380 car carrier) chở nhiều xe con | R-02, R-07 | 1 `truck` + 8 `car` (mỗi chiếc xe trên sàn 1 box) + 1 `person` (người đứng cạnh xe) | Mô hình cần biết có bao nhiêu xe đang được chở, không chỉ có xe tải. Gộp là mất thông tin số lượng và vị trí. Đây là ca "xe chở xe" chuẩn. Ảnh bị ảnh hưởng nếu đổi quy tắc: `img_029`, `img_035`, `img_028` |
| `img_026` | Cặp đôi trên 1 xe máy trong hầm | R-01, R-03 | 2 `person` + 1 `motorcycle` = 3 box; người hành khách bị che ~50% → `occluded_level = 2` | Mỗi người là một vật thể; gộp sẽ làm mất số người trên xe. Xe chạm mép dưới → `truncated = yes` |
| `img_005` | Bầy xe máy ở TP.HCM, chạy ngang camera | R-01, R-07, R-10 | Mỗi cặp người–xe là 2 box; người lái gán `person`, xe gán `motorcycle`; xe ở rìa ảnh bị cắt → `truncated = yes` | Nguyên tắc R-01 áp dụng giống nhau cho mọi ảnh xe máy, kể cả khi người che gần hết thân xe. Kết quả: hai người phải đếm ra cùng số box |
| `img_030` | Xe máy xếp hàng trên vỉa hè | R-01, R-11 | Xe máy đứng yên vẫn gán `motorcycle`; người đứng cạnh gán `person`; không có rider thì không thêm box `person` | R-11: dừng yên vẫn là phương tiện cần phát hiện. R-01 chỉ sinh thêm box `person` khi thực sự có người lái |
| `img_016` | Ngã tư Bangkok, nhiều vật chạm mép ảnh | R-07, R-01, R-10 | 8 vật chạm mép → `truncated = yes`; cặp người–xe máy ở giữa gán 2 box | Mép ảnh không làm mất đối tượng; vẫn gán và đánh dấu `truncated` |
| `img_001` | Bán tải trước quán ăn, người bị cành/cột che | R-13, R-03, R-10 | Bán tải → `truck`; người bị che 20–40% → `occluded_level = 1`; người lái xe ở rìa phải → `truncated = yes` | Bán tải có thùng riêng nên là `truck` (R-13), không phải `car`. Cây/cột là vật cản trong ảnh → mức che |
| `img_012` | Bán tải chở rau bán ven đường + 1 ô tô | R-13 | `truck` (bán tải) + `car` (ô tô con bên trái) | Thùng hàng tách cabin → `truck`; ô tô con thân kín → `car`. Rõ ràng, không cần hỏi |
| `img_007` | Kho hàng tối, 2 xe tải + 1 công nhân | R-13, R-10 | 2 `truck`; 1 `person`; không gán vali/hành lý | Vali không thuộc lớp nào và là vật cố định trong kho, không phải người/xe |
| `img_003` | Rất nhiều xe máy & người ở nền, người bị xe che | R-03, R-04, R-07 | Vật ở rìa trên có h < 20 px → không gán; người/xe lớn bị che → vẫn gán + `occluded_level` 1–2; vật chạm mép → `truncated = yes` | R-04 lấy ngưỡng 20 px từ `taxonomy.json`; bỏ sót vật nhỏ phải ghi `image_issues.csv` |
| `img_009` | Hàng người trên xe buýt ở xa + xe đạp chạy ngang | R-04 | Người trên xe buýt có h 11–21 px: h < 20 px → không gán; người h = 21 px → gán nhưng tick `can_review` | Sát ngưỡng nên hai người dễ lệch; tick để nhóm chốt |
| `img_025` | Bãi biển tối, người xa & xe xa | R-04, R-11 | 8 người có h < 20 px → không gán; người h ≥ 20 px và xe ở đường → gán | Áp dụng đúng một ngưỡng cho cả lô, không tuỳ tiện theo cảnh |
| `img_031` | Đường phố đêm, người rất xa | R-04 | Người h 9–19 px → không gán; xe/xe máy lớn hơn → gán | Cùng lý do R-04; tránh tình trạng "người này gán, người kia không" |
| `img_013` | Đường đêm mưa, xe ở rất xa (22–29 px) | R-04 | Xe h ≥ 20 px → gán `car`; xe sáng đèn ở xa tick `can_review` vì khó phân biệt xe với đèn | Vẫn đủ ngưỡng nên gán, nhưng chất lượng box thấp nên cần người khác xem |
| `img_035` | Ô tô 3 bánh quá tải ở Hyderabad, tài xế thò ra cửa | R-03, R-10, R-04 | `person` (tài xế) bị che > 60% → `occluded_level = 3` + `can_review`; hành khách trong cabin → `occluded_level = 3`; không gán vật quá nhỏ bị chở (nếu không xác định được lớp) | R-03: che nhiều vẫn gán. Lớp của ô tô 3 bánh chưa chốt → xem 4.2 |
| `img_017` | Tượng người cưỡi ngựa ở Glasgow | R-05 | Không gán `person`. Ảnh rỗng trong COCO | Chỉ gán người thật. Ca này IAA có thể rất cao mà cả hai người vẫn sai → không được coi IAA cao là bằng chứng đúng |
| `img_027` | Tượng xe bán tải trong nghĩa trang Oak Hill | R-05 | Không gán `truck` | Vật không thật. Nhóm nên xác nhận lại ở 4.2 vì nhiều người sẽ gán nhầm |
| `img_033` | Mannequin trong cửa hàng Buchanan Street | R-05 | Không gán `person` | Mannequin không phải người thật |
| `img_018` | Biển quảng cáo có người in + xe chạy dưới biển | R-05 | Không gán `person` ở biển; chỉ gán các `car` thật ở đường | Người in trên biển không tồn tại trong không gian ảnh |
| `img_038` | Cửa hàng Munich bày mô hình xe đồ chơi | R-05 | Không gán `car` cho 25 mô hình; ảnh rỗng | Đồ chơi, không phải xe thật. Gán 25 box ở đây sẽ làm mô hình học nhầm |
| `img_019` | Xe đồ chơi "Dangermouse" trong diễn hành Hamleys | R-05, R-09 | Không gán `car` cho chiếc xe đồ chơi; gán `person` cho khán giả thật | Đồ chơi → không gán (xem 4.2 vì có thể cần reviewer xác nhận) |
| `img_020` | Cầu vồng trong gương bên xe | R-06, R-08 | Ảnh rỗng — không gán `car` nào | Vật trong gương là phản chiếu (R-06) và là xe của người chụp (R-08) |
| `img_024` | AMC Pacer cổ trong nhà xe | R-10 | `car` (xe 4 bánh thân kín); ô tô cổ vẫn là `car` | Độ cũ không đổi lớp; nhiều người dễ gán `truck` vì thân vuông |
| `img_002` (người) | Người đứng bên xe chở | R-01 | `person` riêng, không gộp vào `truck` | Người không lái xe đó thì không sinh quan hệ rider–vehicle |

### 4.2 Ca cần hỏi reviewer (chưa tự quyết được sau khi đọc cả guideline)

Các ca dưới đây đều chưa có quy tắc nào trong v0 trả lời trọn vẹn.
Trong lúc chờ nhóm chốt ở Pha 2: gán theo phương án tạm ở cột "Đề xuất", tick `can_review`,
và ghi vào `submission/qc/image_issues.csv`.

| Ảnh | Tình huống | Rule ID liên quan | Đề xuất của tôi | Câu hỏi cần reviewer chốt |
|---|---|---|---|---|
| `img_009`, `img_037`, `img_040` | Xe buýt xuất hiện rõ (xe buýt đông ở `img_009`, GO Transit ở `img_037`, xe buýt ở `img_040`) | R-13, 4.1 | Tạm `ignore_region` bao quanh xe buýt, không map sang `van` | Taxonomy v0 không có lớp `bus`. Gán `van` là sai ngữ nghĩa (xe buýt lớn hơn van nhiều). Nhóm có thêm lớp `bus` ở v1.0 không? Nếu có, `img_040` và `img_037` cũng đổi theo |
| `img_006`, `img_009`, `img_023`, `img_034`, `img_039` | Xe đạp / cyclo (xe đạp 3 bánh có cabin chở khách, Hue) — 5/40 ảnh | R-04, 4.1 | Tạm `ignore_region` cho dãy xe đạp xa; xe đạp gần, thấy rõ bánh/đội → vẫn chưa có lớp để gán | Taxonomy v0 không có lớp `bicycle`. Áp dụng cho 5/40 ảnh nên quyết định này ảnh hưởng mạnh tới IAA. Đề xuất thêm lớp `bicycle`. Nếu nhóm không thêm: bỏ hết (`ignore_region`) hay map sang `motorcycle`? |
| `img_004`, `img_035` | Tuk-tuk / ô tô 3 bánh chở khách (2 xe tuk-tuk màu ở `img_004`, ô tô 3 bánh quá tải ở `img_035`) | R-13, 4.1 | Tạm `ignore_region`; nhưng ở `img_035` vẫn gán `person` cho tài xế | 3 bánh, có cabin, chở khách — không khớp `car`, `van` lẫn `motorcycle`. Ở `img_004` detector tự nhận là `motorcycle` (0.82) nhưng đó là tuk-tuk. Nhóm có thêm lớp `rickshaw`/`tricycle` không, hay map `van`? |
| `img_036` | CMC Veryca — xe tải nhỏ thùng kín bên đường | R-13 | Tạm `truck` (detector 0.89, và Veryca về kỹ thuật là xe tải nhỏ có cabin) | Ranh giới `truck` ↔ `van` là điểm yếu của taxonomy v0. Veryca có cabin riêng + thùng, nhưng khi lắp cabin kín trông như van. Nhóm chốt tiêu chí gì (có thùng mở / thùng kín / tải trọng)? |
| `img_037` | Pickup + rùa "Master 75 Truck Cap" | R-13 | Tạm `truck` | Nếu thùng đã đóng thành cabin kín, có còn là `truck` không? Cùng câu hỏi với `img_036` |
| `img_011` | Người hóa trang "Predator" trong lễ hội xe máy | R-05 | Tạm không gán (giống tượng) | Có người thật trong bộ đồ hóa trang, nhưng nhìn như nhân vật giống tượng. Gán `person` (có người thật) hay không (mang tính "không phải vật thật")? Suy ra quy tắc cho mascot, hoạt hình, người trong bộ đồ nói chung |
| `img_022` | Xe máy có xe đêm (sidecar), ảnh lịch sử | R-01, R-02 | Tạm 1 box `motorcycle` bao gồm cả xe đêm | Xe đêm là một khối riêng nhưng không có lớp phù hợp. Gộp vào box xe hay tách thành box riêng (lớp gì)? Suy ra quy tắc cho xe kéo, rơ-mooc, xe có thùng nối |
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
| `min_box_height_px` | 20 | R-04: vật thấp hơn ngưỡng thì không gán |
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

### 5.4 Tự kiểm trước khi nộp

- [ ] Đọc lại mục 4.1: mỗi ảnh có tìm lại được bằng mô tả, và tôi biết quyết định ban đầu của mình là gì.
- [ ] Với 3 ảnh có người đi xe máy (`img_005`, `img_026`, `img_029`), đọc R-01 và đếm số box — kết quả phải giống nhau.
- [ ] Với `img_002`, đọc R-02 và nói được: 1 `truck` + 8 `car` + 1 `person`.
- [ ] Biết rõ 13 ca ở 4.2 đã được hỏi reviewer chưa, và mình đã ghi vào `image_issues.csv` chưa.

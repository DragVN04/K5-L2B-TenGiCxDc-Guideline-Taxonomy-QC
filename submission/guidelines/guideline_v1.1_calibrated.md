# Guideline gán nhãn sau tổng hợp

## 1. Mục tiêu

Tạo nhãn bounding box 2D để phát hiện người và các phương tiện thuộc phạm vi lab trong ảnh đường phố. Sử dụng CVAT và COCO 1.0. Ưu tiên không bỏ sót vật đủ điều kiện, không gán nhãn cho vật giả hoặc ngoài phạm vi, phân biệt đúng lớp và đặt box sát phần vật nhìn thấy.

## 2. Lớp và thuộc tính

| Lớp             | Định nghĩa                                                                        | Ví dụ tham chiếu                         | Phản ví dụ hoặc dễ nhầm                           |
| --------------- | --------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------- |
| `car`           | Ô tô con, SUV và taxi dạng ô tô con.                                              | Taxi xanh, img_040.jpg.                  | Bán tải có thùng riêng, img_037.jpg.              |
| `truck`         | Xe tải hoặc bán tải có thùng/chassis chở hàng độc lập.                            | Xe tải xanh, img_036.jpg.                | Van thân liền, img_005.jpg.                       |
| `van`           | Xe cỡ nhỏ đến vừa có khoang kín liền với thân.                                    | Xe trắng sau người đi xe, img_005.jpg.   | Bán tải có nắp thùng cao, img_037.jpg.            |
| `motorcycle`    | Xe máy hoặc mô tô, kể cả sidecar nếu gắn liền với mô tô và nhận dạng được.        | Xe máy đỏ, img_026.jpg.                  | Xe đạp ở img_006.jpg, tuk-tuk ở img_004.jpg.      |
| `person`        | Người thật, thấy trực tiếp trong ảnh, dù đang đi bộ hay ngồi trên xe.             | Người băng qua đường, img_034.jpg.       | Tượng ở img_017.jpg, ảnh chân dung ở img_018.jpg. |
| `bus`           | Xe có cấu hình chở khách tập thể kiểu xe buýt, kể cả xe buýt nhỏ.                 | Xe buýt ở img_009.jpg và img_037.jpg.    | Van trắng, img_005.jpg.                           |
| `tuk_tuk`       | Xe cơ giới ba bánh có thân xe chở người hoặc hàng.                                | Hai xe màu xanh, img_004.jpg.            | Xích lô đạp, img_023.jpg.                         |
| `ignore_region` | Vùng có cụm vật mục tiêu quá nhỏ hoặc dày đến mức không thể tách để gán từng vật. | Cụm sâu có thể cần khoanh ở img_021.jpg. | Các xe máy tiền cảnh còn tách được ở img_030.jpg. |

| Thuộc tính       | Giá trị và tiêu chí                                                                                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `occluded_level` | `0` không che. `1` trên 0% đến 30%. `2` trên 30% đến 70%. `3` trên 70% nếu vẫn nhận dạng chắc chắn. Ước lượng phần diện tích vật bị vật khác che, tách với phần ngoài khung ảnh. |
| `truncated`      | `yes` nếu vật bị mép ảnh cắt; `no` nếu toàn bộ vật nằm trong khung.                                                                                                              |
| `can_review`     | Bật khi đã vẽ box nhưng còn nghi vấn. Tắt khi không có nghi vấn. Nếu chưa đủ căn cứ vẽ, ghi vấn đề cấp ảnh.                                                                      |

## 3. Quy tắc vẽ box

- **R-01** — Phân lớp theo cấu tạo. car là ô tô con/SUV, kể cả taxi bốn bánh. truck là xe tải và bán tải có cabin và thùng hàng tách biệt, kể cả gắn nắp. van có khoang kín liền thân và không nhận ra thùng hàng độc lập. Đề xuất thêm bus cho xe chở khách tập thể có cấu hình xe buýt (kể cả xe buýt nhỏ) và tuk_tuk cho xe ba bánh có động cơ với thân chở người hoặc hàng. Xe máy/mô tô hai bánh có sidecar gắn liền vẫn là motorcycle, nếu nhận dạng đủ rõ.
- **R-02** — Mỗi vật thể một hình chữ nhật ôm sát mọi phần nhìn thấy thuộc vật đó. Không nội suy phần bị che. Nếu hai phần nhìn thấy của cùng một vật cách nhau thì dùng một hình chữ nhật bao cả hai. Không gộp các vật riêng chỉ vì box chồng nhau.
- **R-03** — Xe đạp và xích lô đạp ngoài phạm vi. Người đi cùng vẫn được xét theo tiêu chí person. Không dùng ignore_region chỉ vì gặp một vật ngoài taxonomy.
- **R-04** — Xét che khuất và cắt mép riêng. Box nằm trong biên ảnh. Dùng truncated=yes khi có dấu hiệu vật tiếp tục qua mép ảnh. Nếu đồng thời bị vật khác che thì vẫn ghi occluded_level riêng. Không tính phần ngoài khung là bị vật khác che.
- **R-05** — Tách một box cho mỗi người thật và một box cho phương tiện. Người lái và người ngồi sau là các vật riêng, nếu từng người nhận dạng được và đạt ngưỡng. Chỉ gán người trong cabin khi thấy trực tiếp đủ hình thể, kể cả qua kính trong. Không suy từ ghế, mũ hoặc bóng.
- **R-06** — Xe chở xe có một box cho kết cấu vận tải nối liền, gồm đầu kéo, sàn và khung; không kéo theo phần xe được chở nhô ngoài kết cấu. Mỗi xe thật được chở có box riêng nếu nhận dạng được và đạt ngưỡng, kể cả khi box nằm trong box xe tải.
- **R-07** — Phần cố định tạo hình thân xe nằm trong box, như mái tuk-tuk, thùng kín hoặc nắp gắn trên bán tải. Hàng, bao buộc, tượng, đạo cụ nhô ra và vật người đang cầm nằm ngoài box. Nếu hàng che thân xe, đánh giá che khuất riêng.
- **R-08** — Chỉ gán vật thể thật thấy trực tiếp. Loại hình in, màn hình, tượng, ma-nơ-canh, mô hình, phản chiếu và phần xe gắn camera. Vật thật nhìn xuyên kính vẫn được xét. Với đồ trưng bày hay xe diễu hành, dùng dấu hiệu cấu tạo và ngữ cảnh để phân biệt phương tiện thật với thân vỏ hoặc đạo cụ.
- **R-09** — Đo chiều cao box phần nhìn thấy trên ảnh gốc. Từ 20 px trở lên mới xem xét gán từng vật. Bỏ vật nhỏ lẻ dưới ngưỡng. Khoanh ignore_region sát cụm đám đông hoặc cụm vật nhỏ không thể tách; tránh phủ vật nhận dạng rõ. Nếu còn vật rõ trước cụm, gán riêng và thu lại vùng ignore.
- **R-10** — Nhòe do chuyển động hoặc thiếu sáng không tự tạo occluded_level. Gán khi còn nhận dạng được lớp và ước lượng được đường bao; nếu chỉ còn vệt đèn hoặc vệt màu thì bỏ box. Ghi vấn đề cấp ảnh nếu có khả năng là vật mục tiêu và cần người khác xem.
- **R-11** — Khi còn đủ căn cứ để vẽ nhưng phân vân lớp, biên hay thuộc tính, bật can_review. Nếu thiếu căn cứ để vẽ, ghi image, annotator, region, note vào image_issues.csv. Reviewer xem lại các ca này sau khi khóa bản độc lập.
- **R-12** — Giữ mọi ảnh được giao trong COCO kể cả khi không có đối tượng hợp lệ. Đề xuất lớp mới ở Pha 2; khi dùng CVAT chỉ dùng taxonomy v1.0 của nhóm đã khóa.

## 4. Ca khó cần đem ra đối chiếu

| Ảnh         | Tình huống                                                | Quy tắc          | Hướng xử lý đề xuất và dấu hiệu cần kiểm                                                                                        |
| ----------- | --------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| img_002.jpg | Xe tải chở ô tô hai tầng                                  | R-06             | Một box cho đầu kéo và kết cấu chở nối liền, thêm box riêng cho từng ô tô nhận dạng được; rà từng tầng.                         |
| img_004.jpg | Hai tuk-tuk đỗ cạnh nhau                                  | R-01, R-02       | Đề xuất lớp tuk_tuk, mỗi xe một box, tránh gộp hai xe.                                                                          |
| img_005.jpg | Van trắng sau nhiều người đội mũ bảo hiểm                 | R-04, R-05       | Gán van riêng; từng người và xe đủ dấu hiệu có box riêng, không gán qua suy đoán từ mũ.                                         |
| img_014.jpg | Hai người đi bộ rõ và dòng xe nhòe                        | R-10             | Gán hai người nhìn được; bóng nhòe không có đặc điểm nhận dạng thì bỏ box và ghi vấn đề nếu cần.                                |
| img_016.jpg | Tuk-tuk sát mép và bán tải sáng màu nhìn qua phần che     | R-01, R-04, R-11 | Tuk-tuk gán riêng nếu đủ dấu hiệu; phân biệt phần xe sau với xe trước, ghi ca ảnh nếu chưa xác định được kiểu thân.             |
| img_017.jpg | Tượng người cưỡi ngựa                                     | R-08             | Không gán person cho tượng; cọc tiêu trên đầu tượng cũng ngoài phạm vi.                                                         |
| img_019.jpg | Xe diễu hành màu vàng, đầu nhân vật lớn và khán giả       | R-07, R-08, R-11 | Đề xuất car nếu xác nhận là xe thật có kết cấu ô tô; loại đạo cụ, xét riêng người thật.                                         |
| img_020.jpg | Gương chiếu hậu, phản chiếu và phần xe gắn camera         | R-08, R-12       | Loại hình phản chiếu và phần xe chủ; vẫn giữ bản ghi ảnh nếu không có box.                                                      |
| img_021.jpg | Dòng xe máy đông, có vật rõ ở tiền cảnh                   | R-05, R-09       | Gán từng vật tách được; khoanh ignore riêng cụm sâu nếu không thể tách.                                                         |
| img_022.jpg | Cụm xe hai bánh có thùng bên cạnh, ảnh đen trắng          | R-01, R-07, R-11 | Nếu xác nhận là mô tô có sidecar cố định, đề xuất một motorcycle bao cả kết cấu; nếu chưa chắc, ghi vấn đề cấp ảnh.             |
| img_024.jpg | Xe thật trong khu trưng bày và vật giống thân xe trên nóc | R-06, R-07, R-08 | Gán xe thật độc lập; kiểm vật trên nóc là thân vỏ hay xe hoàn chỉnh trước khi gán, không kéo box xe dưới lên theo vật trên nóc. |
| img_026.jpg | Hai người ngồi trên xe máy đỏ ở mép dưới                  | R-04, R-05, R-08 | Tách hai người và một xe nếu từng vật đủ điều kiện; kiểm tọa độ sát biên, bỏ qua hình trên tường.                               |
| img_027.jpg | Hình bán tải trên bệ có biển tưởng niệm                   | R-08             | Căn cứ bệ và ngữ cảnh để loại vật trưng bày dạng tượng, không dùng riêng hình dáng để gán truck.                                |
| img_028.jpg | Bán tải cổ chở tượng ngựa                                 | R-01, R-07, R-08 | Gán xe thật là truck nếu nhận dạng được thùng hàng; loại tượng khỏi box xe và khỏi các lớp vật thể.                             |
| img_030.jpg | Bãi xe máy dày đặc, nhiều xe khuất một phần               | R-04, R-09       | Gán từng xe tiền cảnh tách được; chỉ khoanh ignore ở cụm nền không thể tách.                                                    |
| img_033.jpg | Ma-nơ-canh và nhiều lớp kính                              | R-08, R-11       | Không gán person cho ma-nơ-canh; chỉ gán xe nếu xác nhận thấy trực tiếp xe thật chứ không qua phản chiếu.                       |
| img_035.jpg | Tuk-tuk chở hàng cao và người đi mô tô cạnh bên           | R-05, R-07       | Box tuk_tuk ôm thân xe, không ôm bao kiện phía trên; xét riêng người và mô tô.                                                  |
| img_037.jpg | Bán tải nắp thùng cao, xe buýt ở mép trái                 | R-01, R-04, R-07 | Giữ truck khi còn thấy cấu trúc cabin và thùng tách biệt; nắp gắn cố định thuộc box; xe buýt xét riêng.                         |
| img_038.jpg | Tủ kính chứa nhiều xe mô hình và đồ chơi                  | R-08, R-09, R-12 | Loại mô hình khỏi car và các lớp khác; không dùng ignore để che các vật ngoài phạm vi.                                          |

## 5. QC và phiên bản

- Kiểm COCO đủ ảnh giao, đúng lớp và thuộc tính, box có diện tích dương và nằm trong biên. Kiểm bằng mắt việc ôm sát phần nhìn thấy, vật bỏ sót và hình giả.
- Giữ nguyên ngưỡng trong taxonomy: chiều cao tối thiểu 20 px, mốc lớn 50 px, ngưỡng IoU theo nhóm kích thước 0,85 và 0,70. Ghép box 1–1 từ IoU 0,50; đọc IoU trung bình từ 0,85 và đồng thuận lớp từ 95% trên các cặp ghép. Đọc riêng ca bỏ sót và thừa, vì chúng có thể không xuất hiện trong mẫu số cặp ghép.
- Duyệt đủ 40/40 ảnh ở vòng bàn giao. Ngưỡng lỗi theo ảnh tối đa 2% để xét Release. Reviewer còn kiểm bằng chứng, cờ cần xem và lỗi lặp theo đề; mở vòng mới sau khi sửa nhãn.
- Điều phối viên tập hợp ca mơ hồ; cả nhóm chốt khi họp. Sau khi khóa v1.0, giữ nhãn độc lập để đo IAA. Ở calibration, ghi mã quy tắc, người chốt và kết quả kiểm lại; nếu đổi ý nghĩa, rà lại cả 40 ảnh.

| Phiên bản | Thay đổi                                                        | Lý do                                                                          |
| --------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| v0        | Đặc tả khởi đầu của lab.                                        | Dùng để nhận diện chỗ mơ hồ.                                                   |
| Nháp 067  | Đề xuất hai lớp và 12 quy tắc, bổ sung ca khó và bảng quan sát. | Ranh giới lớp, giao nhau, che/cắt và vật giả xuất hiện nhiều lần trong bộ ảnh. |

### Phụ lục: ghi nhận khi duyệt 40 ảnh

| Ảnh         | Điểm cần kiểm trên ảnh gốc                                | Hướng xử lý để 067 review                                                                                                       | Quy tắc          |
| ----------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| img_001.jpg | Bán tải trắng cắt mép và người ở quán                     | Xét riêng xe và từng người thấy trực tiếp; tách cắt mép khỏi che khuất.                                                         | R-02, R-04       |
| img_002.jpg | Xe tải chở ô tô hai tầng                                  | Một box cho đầu kéo và kết cấu chở nối liền, thêm box riêng cho từng ô tô nhận dạng được; rà từng tầng.                         | R-06             |
| img_003.jpg | Người gánh hàng, xe hai bánh và vật ở nền                 | Box người bỏ đòn gánh và giỏ; phân biệt xe đạp với xe máy trước khi chọn lớp.                                                   | R-03, R-05, R-07 |
| img_004.jpg | Hai tuk-tuk đỗ cạnh nhau                                  | Đề xuất lớp tuk_tuk, mỗi xe một box, tránh gộp hai xe.                                                                          | R-01, R-02       |
| img_005.jpg | Van trắng sau nhiều người đội mũ bảo hiểm                 | Gán van riêng; từng người và xe đủ dấu hiệu có box riêng, không gán qua suy đoán từ mũ.                                         | R-04, R-05       |
| img_006.jpg | Xe đạp sát các xe máy và người đi cùng                    | Giữ người đủ điều kiện; loại xe đạp khỏi taxonomy phương tiện.                                                                  | R-03, R-05       |
| img_007.jpg | Xe con màu sáng nhìn chính diện cạnh xe tải thùng         | Phân loại theo thân xe nhìn thấy; xe nhỏ có thùng độc lập vẫn có thể là truck.                                                  | R-01             |
| img_008.jpg | Nhiều xe máy đỗ sát và người mặc áo nổi                   | Tách từng xe nhận dạng được; chỉ dùng ignore cho cụm không thể tách.                                                            | R-02, R-09       |
| img_009.jpg | Xe buýt nhỏ bên đường                                     | Đề xuất bus dựa trên cấu hình chở khách tập thể; kích thước nhỏ không đủ để đổi sang van.                                       | R-01             |
| img_010.jpg | Người ngồi xe bên sạp rau                                 | Tách người khỏi xe; thúng rau và đồ sạp nằm ngoài box.                                                                          | R-05, R-07       |
| img_011.jpg | Tượng kim loại tiền cảnh và người thật phía xa            | Loại tượng khỏi person; xét riêng người thật và cụm nền.                                                                        | R-08, R-09       |
| img_012.jpg | Thùng bán tải đầy hàng phía trước, xe con ở bên trái      | Box bán tải loại phần tải nhô; gán xe con riêng nếu đủ điều kiện.                                                               | R-01, R-07       |
| img_013.jpg | Đường đêm, người gần vùng sáng và xe xa                   | Chỉ gán khi nhận dạng được thân vật; điểm sáng đơn lẻ không đủ.                                                                 | R-04, R-09       |
| img_014.jpg | Hai người đi bộ rõ và dòng xe nhòe                        | Gán hai người nhìn được; bóng nhòe không có đặc điểm nhận dạng thì bỏ box và ghi vấn đề nếu cần.                                | R-10             |
| img_015.jpg | Xe con ở hai mép và nền đường ướt                         | Xe ở mép đặt truncated=yes nếu bị khung cắt; không gán vùng phản quang trên đường.                                              | R-04, R-08, R-10 |
| img_016.jpg | Tuk-tuk sát mép và bán tải sáng màu nhìn qua phần che     | Tuk-tuk gán riêng nếu đủ dấu hiệu; phân biệt phần xe sau với xe trước, ghi ca ảnh nếu chưa xác định được kiểu thân.             | R-01, R-04, R-11 |
| img_017.jpg | Tượng người cưỡi ngựa                                     | Không gán person cho tượng; cọc tiêu trên đầu tượng cũng ngoài phạm vi.                                                         | R-08             |
| img_018.jpg | Chân dung trên biển, xe thật sau hàng rào                 | Loại hình in; xét box từng xe thật, đánh giá phần bị hàng rào che.                                                              | R-04, R-08       |
| img_019.jpg | Xe diễu hành màu vàng, đầu nhân vật lớn và khán giả       | Đề xuất car nếu xác nhận là xe thật có kết cấu ô tô; loại đạo cụ, xét riêng người thật.                                         | R-07, R-08, R-11 |
| img_020.jpg | Gương chiếu hậu, phản chiếu và phần xe gắn camera         | Loại hình phản chiếu và phần xe chủ; vẫn giữ bản ghi ảnh nếu không có box.                                                      | R-08, R-12       |
| img_021.jpg | Dòng xe máy đông, có vật rõ ở tiền cảnh                   | Gán từng vật tách được; khoanh ignore riêng cụm sâu nếu không thể tách.                                                         | R-05, R-09       |
| img_022.jpg | Cụm xe hai bánh có thùng bên cạnh, ảnh đen trắng          | Nếu xác nhận là mô tô có sidecar cố định, đề xuất một motorcycle bao cả kết cấu; nếu chưa chắc, ghi vấn đề cấp ảnh.             | R-01, R-07, R-11 |
| img_023.jpg | Xích lô gần và ô tô tối màu đối diện                      | Giữ person nếu đủ dấu hiệu, không gán xích lô đạp; xét car riêng.                                                               | R-01, R-03, R-05 |
| img_024.jpg | Xe thật trong khu trưng bày và vật giống thân xe trên nóc | Gán xe thật độc lập; kiểm vật trên nóc là thân vỏ hay xe hoàn chỉnh trước khi gán, không kéo box xe dưới lên theo vật trên nóc. | R-06, R-07, R-08 |
| img_025.jpg | Người rải rác trên lối đi và phương tiện xa               | Đo trên ảnh gốc; gán từng người đủ điều kiện, không gom cả lối đi vào ignore.                                                   | R-09             |
| img_026.jpg | Hai người ngồi trên xe máy đỏ ở mép dưới                  | Tách hai người và một xe nếu từng vật đủ điều kiện; kiểm tọa độ sát biên, bỏ qua hình trên tường.                               | R-04, R-05, R-08 |
| img_027.jpg | Hình bán tải trên bệ có biển tưởng niệm                   | Căn cứ bệ và ngữ cảnh để loại vật trưng bày dạng tượng, không dùng riêng hình dáng để gán truck.                                | R-08             |
| img_028.jpg | Bán tải cổ chở tượng ngựa                                 | Gán xe thật là truck nếu nhận dạng được thùng hàng; loại tượng khỏi box xe và khỏi các lớp vật thể.                             | R-01, R-07, R-08 |
| img_029.jpg | Người với xe đạp, xe máy và thanh dài                     | Xét đủ dấu hiệu cho motorcycle, bỏ xe đạp; không kéo box người hoặc xe theo thanh dài.                                          | R-03, R-05, R-07 |
| img_030.jpg | Bãi xe máy dày đặc, nhiều xe khuất một phần               | Gán từng xe tiền cảnh tách được; chỉ khoanh ignore ở cụm nền không thể tách.                                                    | R-04, R-09       |
| img_031.jpg | Phố đêm mưa, đèn xe và các vệt phản chiếu                 | Ưu tiên đường viền và cấu trúc xe khi phân lớp; không dùng vệt phản chiếu làm phần box.                                         | R-01, R-08, R-10 |
| img_032.jpg | Hàng người sau dải phân cách, xe cắt mép trái             | Tách người còn đủ dấu hiệu và đạt ngưỡng; xét ignore cho cụm bất khả phân; xe sát biên kiểm truncated.                          | R-04, R-09       |
| img_033.jpg | Ma-nơ-canh và nhiều lớp kính                              | Không gán person cho ma-nơ-canh; chỉ gán xe nếu xác nhận thấy trực tiếp xe thật chứ không qua phản chiếu.                       | R-08, R-11       |
| img_034.jpg | Người đi bộ giữa giao lộ và xe ở mép phải                 | Box riêng cho người đi bộ; xét từng người và xe sát mép theo dấu hiệu và cắt khung.                                             | R-04, R-05       |
| img_035.jpg | Tuk-tuk chở hàng cao và người đi mô tô cạnh bên           | Box tuk_tuk ôm thân xe, không ôm bao kiện phía trên; xét riêng người và mô tô.                                                  | R-05, R-07       |
| img_036.jpg | Xe tải xanh nhỏ có thùng phủ bạt phía sau                 | Gán truck dựa vào thùng độc lập; phần bạt cố định tạo thành vỏ thùng thuộc box.                                                 | R-01, R-07       |
| img_037.jpg | Bán tải nắp thùng cao, xe buýt ở mép trái                 | Giữ truck khi còn thấy cấu trúc cabin và thùng tách biệt; nắp gắn cố định thuộc box; xe buýt xét riêng.                         | R-01, R-04, R-07 |
| img_038.jpg | Tủ kính chứa nhiều xe mô hình và đồ chơi                  | Loại mô hình khỏi car và các lớp khác; không dùng ignore để che các vật ngoài phạm vi.                                          | R-08, R-09, R-12 |
| img_039.jpg | Phố có nhiều xe nhỏ ở xa, xe đạp lẫn xe máy               | Chỉ gán xe máy khi thấy dấu hiệu phân biệt đủ rõ; đo ngưỡng trên ảnh gốc.                                                       | R-03, R-09, R-11 |
| img_040.jpg | Người đội mũ tiền cảnh, taxi và tuk-tuk phía sau          | Tách người khỏi phương tiện; taxi bốn bánh là car nếu nhận dạng rõ, không suy ra lớp từ biển TAXI.                              | R-01, R-04, R-05 |

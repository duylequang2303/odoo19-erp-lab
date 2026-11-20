# Ghi chú Tuần 5 — Duyệt hai cấp, phân quyền, activity, test; carrier giao vận mock

## Đã làm (Nội dung 11)
- Duyệt hai cấp theo ngưỡng 5.000.000 VND: dưới ngưỡng chỉ Trưởng phòng; từ ngưỡng trở lên chuyển Giám đốc.
- Record rules theo nhóm: Employee (own), Manager (pending), Director (all).
- Tạo mail.activity cho người duyệt khi gửi duyệt; đóng activity khi duyệt xong.
- Test `tests/test_approval_flow.py` (TransactionCase): dưới ngưỡng, trên ngưỡng, từ chối.

## Đã làm (Nội dung 12)
- `tools/mock_carrier/app.py`: Flask mock, endpoint `/v1/*` và `/v2/*` với cấu trúc JSON khác nhau.
- Module `lab_delivery_mock`: kế thừa `delivery.carrier`, field `lab_api_version` V1/V2, `lab_base_url`, `lab_token`; `lab_mock_send_shipping` lưu `carrier_tracking_ref`; bắt timeout/HTTP error, báo lỗi tiếng Việt.

## Lỗi gặp và cách sửa
- Record rule sai domain khiến Manager thấy cả phiếu đã duyệt → lọc thêm `state in ('submitted','manager_approved')`.
- Thay đổi `state` nhưng nút chưa cập nhật đúng nhóm → dùng `groups=` trên nút kết hợp `invisible` theo state.
- Chưa cấu hình `delivery` trong depends thì không kế thừa được `delivery.carrier` → khai báo `depends: ["delivery"]`.

## Ảnh chụp cần lưu
- [ ] Form phiếu ≥5 triệu ở trạng thái Chờ duyệt GĐ
- [ ] Record rules cho 3 nhóm
- [ ] Activity chuông cho người duyệt
- [ ] Test TransactionCase chạy xanh
- [ ] curl response V1 và V2
- [ ] Form carrier Lab Mock (V1/V2)
- [ ] Thông báo lỗi khi tắt mock server

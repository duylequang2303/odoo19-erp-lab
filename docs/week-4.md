# Ghi chú Tuần 4 — Dựng nền móng + module đầu tiên

Tuần này khởi tạo repo `odoo19-erp-lab` và hoàn thành 9 issue nhỏ để có nền móng vững chắc cho các tuần sau.

## Đã làm

1. **#1 Khởi tạo repo và README** — cấu trúc `addons/`, `tools/`, `docs/`; `.gitignore` chuẩn Odoo/Python; README giới thiệu mục tiêu, yêu cầu cài đặt, cách chạy, lộ trình theo tuần.
2. **#2 Dựng môi trường Odoo 19 bằng Docker Compose** — `docker-compose.yml` với image `odoo:19.0` + `postgres:16`, mount `addons/` và `odoo.conf`, volume lưu dữ liệu DB. `docker compose up -d` chạy được, vào `localhost:8069` tạo database.
3. **#3 Cấu hình `odoo.conf` cho dev** — `addons_path`, `db_host`, `dev_mode = all`, `log_level`; ghi chú ý nghĩa từng dòng ngay trong file.
4. **#4 Thêm pre-commit** — `.pre-commit-config.yaml` với black, flake8 (max-line-length=120), trailing-whitespace, end-of-file-fixer, check-yaml.
5. **#5 Module khung `lab_base`** — manifest `19.0.1.0.0`, depends `base, mail`; `security/lab_security.xml` tạo category Lab + 3 nhóm Employee/Manager/Director (implied theo cấp bậc); menu gốc "Lab".
6. **#6 `lab_approval`: model Phiếu đề xuất** — model `lab.approval.request` kế thừa `mail.thread` + `mail.activity.mixin`; các trường tên, người đề xuất, phòng ban, số tiền, mô tả, ngày tạo; list view (`<list>`) + form view; `ir.model.access.csv` phân quyền cho 3 nhóm.
7. **#7 `lab_approval`: luồng trạng thái** — `state` Selection (Nháp → Chờ duyệt → Đã duyệt / Từ chối), statusbar, nút `type="object"` (Gửi duyệt/Duyệt/Từ chối/Trả về Nháp), ẩn/hiện nút bằng `invisible` inline; số tiền `readonly` khi không còn Nháp.
8. **#8 `lab_approval`: ràng buộc dữ liệu** — `@api.constrains` số tiền > 0 (UserError tiếng Việt); `_sql_constraints` tên phiếu không trùng.
9. **#9 Ghi chú tuần 4** — file này.

## Lỗi gặp và cách sửa

- **Odoo không nhận module tự viết**: do `addons_path` trong `odoo.conf` thiếu `/mnt/extra-addons` (thư mục `addons/` được mount vào đây). Sửa: bổ sung đường dẫn vào `addons_path`, restart container, Update Apps List.
- **Tag image**: ban đầu chưa chắc chắn `odoo:19.0` đã có trên Docker Hub, kiểm tra tags trên Docker Hub rồi mới đặt trong compose.
- **View lỗi cú pháp**: dùng nhầm `<tree>` thay vì `<list>` (Odoo 18+ yêu cầu `<list>`); `attrs` đã deprecated, chuyển sang `invisible` inline dạng biểu thức Python.
- *(Thêm vào đây các lỗi bạn gặp khi chạy thực tế, kèm ảnh chụp.)*

## Ảnh chụp cần lưu (để đưa vào báo cáo)

- [ ] Trang README của repo trên GitHub
- [ ] `docker compose up -d` chạy thành công trong terminal
- [ ] Giao diện `localhost:8069` tạo database / đăng nhập
- [ ] Menu "Lab" xuất hiện sau khi cài module
- [ ] 3 nhóm Employee/Manager/Director trong Settings > Users
- [ ] List view và Form view Phiếu đề xuất (có statusbar)
- [ ] Bấm nút chuyển trạng thái đúng luồng
- [ ] Nhập số tiền âm → báo lỗi tiếng Việt rõ ràng
- [ ] Phiếu đã duyệt: trường số tiền bị khóa (readonly)
- [ ] pre-commit chặn hoặc tự sửa commit sai format

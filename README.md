# odoo19-erp-lab

Dự án mã nguồn cá nhân thực hành trên nền **Odoo 19 (Community)**: dựng môi trường phát triển, xây dựng các module ERP từ đầu (phê duyệt, giao vận, báo cáo kho, REST API, quản lý tài sản) và một công cụ quét lỗi nâng cấp phiên bản. Repo này dùng làm "sân chơi" trong quá trình thực tập, tách hoàn toàn khỏi môi trường production của khách hàng.

> Mục tiêu: mỗi tuần hoàn thành 1 nhóm issue (GitHub Issue → branch → Pull Request → merge), chụp ảnh và ghi chú vào `docs/week-X.md` làm tư liệu cho báo cáo thực tập.

## Cấu trúc thư mục

```
odoo19-erp-lab/
├── docker-compose.yml      # Odoo 19 + PostgreSQL, chạy bằng một lệnh
├── odoo.conf               # Cấu hình cho môi trường dev
├── .pre-commit-config.yaml # black + flake8 chạy trước mỗi commit
├── .gitignore              # Chuẩn cho Odoo/Python
├── addons/                 # Module Odoo tự viết (mount vào container)
│   ├── lab_base/           # Module nền: menu gốc "Lab" + 3 nhóm quyền
│   └── lab_approval/       # Phiếu đề xuất mua sắm + luồng phê duyệt
├── tools/                  # Script tiện ích (mock server, upgrade toolkit...)
├── docs/                   # Ghi chú học, ảnh chụp, log lỗi theo tuần
│   └── week-4.md
└── README.md
```

## Yêu cầu cài đặt

- Docker + Docker Compose (khuyến nghị Docker Desktop hoặc Docker Engine 24+)
- Git
- (Tùy chọn) Python 3.10+ và pre-commit nếu muốn chạy hook ở local: `pip install pre-commit`

## Cách chạy nhanh

```bash
git clone https://github.com/duylequang2303/odoo19-erp-lab.git
cd odoo19-erp-lab
docker compose up -d
```

Mở trình duyệt vào **http://localhost:8069** → tạo database mới (chọn demo data nếu muốn) → vào menu **Apps**, cập nhật danh sách module (Update Apps List), cài **Lab Approval** (module `lab_base` sẽ được cài tự động theo phụ thuộc).

Xem log: `docker compose logs -f odoo`
Dừng: `docker compose down` (giữ dữ liệu) hoặc `docker compose down -v` (xóa cả dữ liệu).

## Cấu hình dev

- File `odoo.conf` đã bật `dev_mode = all`: sửa code Python/XML rồi restart container (`docker compose restart odoo`) là thấy thay đổi, hoặc dùng `--dev=all` để tự reload.
- `addons_path` trỏ tới `/mnt/extra-addons` (thư mục `addons/` ở máy host được mount vào đây). Thêm module mới vào `addons/` rồi cập nhật Apps List trong Odoo.
- Ghi chú ý nghĩa từng dòng `odoo.conf`: xem `docs/week-4.md`.

## Kiểm soát chất lượng code (pre-commit)

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files   # chạy thủ công cho toàn bộ code
```

Hook đang bật: `black` (format), `flake8` (lint, max-line-length=120), `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`. Commit file sai format sẽ bị chặn hoặc tự sửa.

## Lộ trình (theo tuần)

| Tuần | Mục tiêu | Module/Issue chính |
|------|----------|--------------------|
| 4 | Dựng nền móng + module đầu | repo, Docker Compose, `lab_base`, `lab_approval` (workflow + constraint) |
| 5 | Phê duyệt nâng cao + giao vận mock | duyệt 2 cấp theo giá trị, record rules, activity, test, `lab_delivery_mock` |
| 6 | Báo cáo kho | `lab_stock_report` nhập-xuất-tồn liên kho, tối ưu truy vấn, xuất Excel |
| 7 | REST API + tài sản | `lab_rest_api` (token, phân quyền), `lab_asset` (wizard, cron) |
| 8 | Công cụ nâng cấp + đóng gói | `tools/upgrade_toolkit`, GitHub Actions, tổng kết |

## Quy ước làm việc

- Branch: `feature/<số-issue>-<tên-ngắn>`, ví dụ `feature/6-approval-request-model`
- Commit: `feat:`, `fix:`, `docs:`, `test:`, `chore:`
- Pull Request ghi `Closes #<số>` để issue tự đóng
- Mỗi issue xong: chụp ảnh, ghi lỗi gặp và cách sửa vào `docs/week-X.md`

## Lưu ý

- Chỉ dùng Odoo Community (giấy phép LGPL). Không đưa code Enterprise, code/token/dữ liệu khách hàng hay công ty vào repo.
- Repo dùng cho thực hành và làm portfolio. Nếu cần riêng tư, chuyển sang private trước khi chứa thông tin nhạy cảm.

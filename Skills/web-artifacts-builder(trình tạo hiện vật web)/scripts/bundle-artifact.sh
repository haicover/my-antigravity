#!/bin/bash
set -euo pipefail  # Tăng cường an toàn: dừng nếu lỗi, lỗi biến chưa đặt, lỗi pipe

# =========================
# Cấu hình màu sắc cho output
# =========================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =========================
# Hàm hiển thị thông báo
# =========================
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}
success() {
    echo -e "${GREEN}✅ $1${NC}"
}
warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}
error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# =========================
# Kiểm tra lệnh pnpm có tồn tại không
# =========================
if ! command -v pnpm &> /dev/null; then
    error "pnpm không được cài đặt. Vui lòng cài pnpm (https://pnpm.io/installation) hoặc dùng npm thay thế."
fi

# =========================
# Kiểm tra thư mục dự án
# =========================
if [ ! -f "package.json" ]; then
    error "Không tìm thấy package.json. Hãy chạy script này từ thư mục gốc của dự án React."
fi

if [ ! -f "index.html" ]; then
    error "Không tìm thấy index.html. Script yêu cầu file entry point index.html."
fi

info "Bắt đầu bundle React app thành một file HTML duy nhất..."

# =========================
# Cài đặt dependencies tạm thời (có thể xoá sau nếu muốn)
# =========================
warn "Script sẽ cài đặt các gói bundling (parcel, html-inline, ...) vào devDependencies."
read -p "Bạn có muốn tiếp tục? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    error "Người dùng hủy bỏ."
fi

info "Đang cài đặt dependencies..."
pnpm add -D parcel @parcel/config-default parcel-resolver-tspaths html-inline

# =========================
# Tạo file .parcelrc nếu chưa có (hỗ trợ path alias)
# =========================
if [ ! -f ".parcelrc" ]; then
    info "Tạo cấu hình Parcel với path alias resolver..."
    cat > .parcelrc << 'EOF'
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
EOF
else
    info "Đã tìm thấy .parcelrc, giữ nguyên cấu hình hiện tại."
fi

# =========================
# Dọn dẹp bản build cũ
# =========================
info "Dọn dẹp thư mục dist và bundle.html cũ..."
rm -rf dist bundle.html

# =========================
# Build bằng Parcel (không source map)
# =========================
info "Đang build với Parcel (có thể mất vài giây)..."
pnpm exec parcel build index.html --dist-dir dist --no-source-maps --no-cache

# Kiểm tra xem dist/index.html có tồn tại không
if [ ! -f "dist/index.html" ]; then
    error "Build thất bại: không tìm thấy dist/index.html"
fi

# =========================
# Inline tất cả assets vào một file HTML
# =========================
info "Inline assets vào một file HTML duy nhất..."
pnpm exec html-inline dist/index.html > bundle.html

# Kiểm tra file bundle.html
if [ ! -f "bundle.html" ]; then
    error "Không thể tạo bundle.html"
fi

# =========================
# Lấy kích thước file
# =========================
FILE_SIZE=$(du -h bundle.html | cut -f1)
LINE_COUNT=$(wc -l < bundle.html)

# =========================
# Hoàn tất
# =========================
success "Bundle hoàn tất!"
info "📄 Output: bundle.html (kích thước $FILE_SIZE, $LINE_COUNT dòng)"
info "✨ Bạn có thể dùng file này làm artifact trong Claude hoặc gửi cho bất kỳ ai."
info "🧪 Để kiểm tra cục bộ: mở bundle.html bằng trình duyệt."

# =========================
# Tuỳ chọn: dọn dẹp dependencies (hỏi người dùng)
# =========================
read -p "Bạn có muốn gỡ bỏ các gói bundling khỏi package.json để giữ dự án sạch? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    info "Đang gỡ bỏ các gói đã cài..."
    pnpm remove parcel @parcel/config-default parcel-resolver-tspaths html-inline
    success "Đã dọn dẹp dependencies."
else
    info "Giữ nguyên dependencies để dùng lại cho lần sau."
fi

# =========================
# Mở file tự động? (chỉ macOS)
# =========================
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Mở bundle.html trong trình duyệt mặc định? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open bundle.html
    fi
fi

exit 0
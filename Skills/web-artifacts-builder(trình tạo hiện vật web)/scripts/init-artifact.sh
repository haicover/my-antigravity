#!/bin/bash
set -euo pipefail  # An toàn tối đa: dừng nếu lỗi, biến chưa khai báo, lỗi pipe

# =========================
# Màu sắc cho output
# =========================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# =========================
# Hàm logging
# =========================
info()  { echo -e "${BLUE}ℹ️  $1${NC}"; }
success(){ echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# =========================
# Hiển thị help
# =========================
show_help() {
    cat << EOF
${CYAN}Usage: $0 [OPTIONS] <project-name>${NC}

Create a React + Vite + TypeScript project with Tailwind CSS and shadcn/ui pre-configured.

${CYAN}Options:${NC}
  -h, --help          Show this help message
  -p, --pm <name>     Package manager to use (pnpm, npm, yarn). Default: pnpm
  -s, --skip-install  Skip installing dependencies (only generate config files)
  --no-tarball        Do not extract shadcn components from tarball (only setup Tailwind)

${CYAN}Requirements:${NC}
  - Node.js >= 18
  - tar (usually pre-installed)
  - If using pnpm: will be installed globally if missing
  - A file 'shadcn-components.tar.gz' must exist in the same directory as this script
    (unless --no-tarball is used)

${CYAN}Example:${NC}
  $0 my-app
  $0 --pm npm my-app
  $0 --skip-install test-project

EOF
    exit 0
}

# =========================
# Xử lý tham số dòng lệnh
# =========================
PM="pnpm"
SKIP_INSTALL=false
NO_TARBALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help) show_help ;;
        -p|--pm) PM="$2"; shift 2 ;;
        -s|--skip-install) SKIP_INSTALL=true; shift ;;
        --no-tarball) NO_TARBALL=true; shift ;;
        -*|--*) error "Unknown option: $1. Use -h for help." ;;
        *) PROJECT_NAME="$1"; shift ;;
    esac
done

if [ -z "${PROJECT_NAME:-}" ]; then
    error "Missing project name. Usage: $0 <project-name> (or use -h for help)"
fi

# =========================
# Kiểm tra lệnh cơ bản
# =========================
for cmd in node tar; do
    if ! command -v $cmd &> /dev/null; then
        error "$cmd is not installed. Please install it first."
    fi
done

# Kiểm tra Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    error "Node.js 18 or higher is required. Current: $(node -v)"
fi
info "Detected Node.js version: $(node -v)"

# Kiểm tra package manager
case $PM in
    pnpm)
        if ! command -v pnpm &> /dev/null; then
            warn "pnpm not found. Installing pnpm globally via npm..."
            npm install -g pnpm
        fi
        ;;
    npm|yarn)
        if ! command -v $PM &> /dev/null; then
            error "$PM is not installed. Please install it first."
        fi
        ;;
    *) error "Unsupported package manager: $PM. Use pnpm, npm, or yarn." ;;
esac
success "Using package manager: $PM"

# =========================
# Kiểm tra file tarball (nếu cần)
# =========================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENTS_TARBALL="$SCRIPT_DIR/shadcn-components.tar.gz"

if [ "$NO_TARBALL" = false ] && [ ! -f "$COMPONENTS_TARBALL" ]; then
    error "shadcn-components.tar.gz not found in script directory: $COMPONENTS_TARBALL"
fi

# =========================
# Xác nhận trước khi tạo project (nếu thư mục đã tồn tại)
# =========================
if [ -d "$PROJECT_NAME" ]; then
    warn "Directory '$PROJECT_NAME' already exists."
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        error "User cancelled."
    fi
    rm -rf "$PROJECT_NAME"
fi

# =========================
# Tạo Vite project
# =========================
info "Creating React + Vite + TypeScript project: $PROJECT_NAME"
$PM create vite "$PROJECT_NAME" --template react-ts

cd "$PROJECT_NAME"

# =========================
# Cấu hình OS cho sed
# =========================
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE="sed -i ''"
else
    SED_INPLACE="sed -i"
fi

# Cleanup index.html
info "Cleaning up index.html..."
$SED_INPLACE '/<link rel="icon".*vite\.svg/d' index.html
$SED_INPLACE "s/<title>.*<\/title>/<title>$PROJECT_NAME<\/title>/" index.html

# =========================
# Cài đặt dependencies (hoặc không)
# =========================
if [ "$SKIP_INSTALL" = false ]; then
    info "Installing base dependencies..."
    $PM install

    # Chọn Vite version phù hợp với Node
    if [ "$NODE_VERSION" -lt 20 ]; then
        VITE_VERSION="5.4.11"
        info "Pinning Vite to $VITE_VERSION for Node 18 compatibility..."
        $PM add -D vite@$VITE_VERSION
    fi

    info "Installing Tailwind CSS and additional dependencies..."
    $PM add -D tailwindcss@3.4.1 postcss autoprefixer @types/node tailwindcss-animate
    $PM add class-variance-authority clsx tailwind-merge lucide-react next-themes

    if [ "$NO_TARBALL" = false ]; then
        info "Installing Radix UI and other shadcn/ui dependencies (this may take a while)..."
        $PM add @radix-ui/react-accordion @radix-ui/react-aspect-ratio @radix-ui/react-avatar \
            @radix-ui/react-checkbox @radix-ui/react-collapsible @radix-ui/react-context-menu \
            @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-hover-card \
            @radix-ui/react-label @radix-ui/react-menubar @radix-ui/react-navigation-menu \
            @radix-ui/react-popover @radix-ui/react-progress @radix-ui/react-radio-group \
            @radix-ui/react-scroll-area @radix-ui/react-select @radix-ui/react-separator \
            @radix-ui/react-slider @radix-ui/react-slot @radix-ui/react-switch @radix-ui/react-tabs \
            @radix-ui/react-toast @radix-ui/react-toggle @radix-ui/react-toggle-group \
            @radix-ui/react-tooltip sonner cmdk vaul embla-carousel-react react-day-picker \
            react-resizable-panels date-fns react-hook-form @hookform/resolvers zod
    fi
else
    info "Skipping dependency installation as requested."
fi

# =========================
# Tạo cấu hình Tailwind, PostCSS, Vite
# =========================
info "Creating configuration files..."

cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        secondary: { DEFAULT: "hsl(var(--secondary))", foreground: "hsl(var(--secondary-foreground))" },
        destructive: { DEFAULT: "hsl(var(--destructive))", foreground: "hsl(var(--destructive-foreground))" },
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        accent: { DEFAULT: "hsl(var(--accent))", foreground: "hsl(var(--accent-foreground))" },
        popover: { DEFAULT: "hsl(var(--popover))", foreground: "hsl(var(--popover-foreground))" },
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
      },
      borderRadius: { lg: "var(--radius)", md: "calc(var(--radius) - 2px)", sm: "calc(var(--radius) - 4px)" },
      keyframes: {
        "accordion-down": { from: { height: "0" }, to: { height: "var(--radix-accordion-content-height)" } },
        "accordion-up": { from: { height: "var(--radix-accordion-content-height)" }, to: { height: "0" } },
      },
      animation: { "accordion-down": "accordion-down 0.2s ease-out", "accordion-up": "accordion-up 0.2s ease-out" },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
EOF

cat > vite.config.ts << 'EOF'
import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": path.resolve(__dirname, "./src") } },
});
EOF

# =========================
# Thêm CSS variables và Tailwind directives
# =========================
info "Adding global CSS with Tailwind and CSS variables..."
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --card: 0 0% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 0 0% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
  }
}
@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
EOF

# =========================
# Cấu hình path alias trong tsconfig.json và tsconfig.app.json
# =========================
info "Adding path alias @/* to TypeScript configs..."

update_tsconfig() {
    local file="$1"
    if [ ! -f "$file" ]; then return; fi
    # Dùng node để sửa JSON một cách an toàn (loại bỏ comments)
    node -e "
        const fs = require('fs');
        let content = fs.readFileSync('$file', 'utf8');
        // Loại bỏ comments // và /* */
        content = content.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '');
        const config = JSON.parse(content);
        config.compilerOptions = config.compilerOptions || {};
        config.compilerOptions.baseUrl = '.';
        config.compilerOptions.paths = { '@/*': ['./src/*'] };
        fs.writeFileSync('$file', JSON.stringify(config, null, 2));
    "
}

update_tsconfig "tsconfig.json"
update_tsconfig "tsconfig.app.json"

# =========================
# Tạo components.json cho shadcn/ui (tham khảo)
# =========================
cat > components.json << 'EOF'
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
EOF

# =========================
# Giải nén tarball components (nếu có)
# =========================
if [ "$NO_TARBALL" = false ] && [ -f "$COMPONENTS_TARBALL" ]; then
    info "Extracting shadcn/ui components from tarball..."
    mkdir -p src
    tar -xzf "$COMPONENTS_TARBALL" -C src/
    success "Components extracted to src/ (ui components, lib, hooks)"
else
    if [ "$NO_TARBALL" = false ]; then
        warn "Tarball not found; skipping component extraction."
    fi
    # Tạo thư mục cơ bản để tránh lỗi
    mkdir -p src/components/ui src/lib src/hooks
    echo "// utils placeholder" > src/lib/utils.ts
fi

# =========================
# Hoàn tất
# =========================
success "Setup complete! Project '$PROJECT_NAME' is ready."

echo ""
echo -e "${CYAN}📦 Included components (if tarball was used):${NC}"
echo "  - accordion, alert, aspect-ratio, avatar, badge, breadcrumb"
echo "  - button, calendar, card, carousel, checkbox, collapsible"
echo "  - command, context-menu, dialog, drawer, dropdown-menu"
echo "  - form, hover-card, input, label, menubar, navigation-menu"
echo "  - popover, progress, radio-group, resizable, scroll-area"
echo "  - select, separator, sheet, skeleton, slider, sonner"
echo "  - switch, table, tabs, textarea, toast, toggle, toggle-group, tooltip"
echo ""
echo -e "${CYAN}To start developing:${NC}"
echo "  cd $PROJECT_NAME"
echo "  $PM dev"
echo ""
echo -e "${CYAN}Import components like:${NC}"
echo "  import { Button } from '@/components/ui/button'"
echo "  import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'"
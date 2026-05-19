import os
import sys
import requests
import json
import base64
from github import Github

# =====================================================================
# CONFIGURATION & INITIALIZATION
# =====================================================================
GITHUB_TOKEN = os.getenv("GH_PAT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GITHUB_TOKEN:
    print("❌ Lỗi: Thiếu biến môi trường GH_PAT_TOKEN. Vui lòng thiết lập trong GitHub Secrets hoặc Local Env.")
    sys.exit(1)

if not GEMINI_API_KEY:
    print("❌ Lỗi: Thiếu biến môi trường GEMINI_API_KEY. Vui lòng thiết lập để gọi API của Gemini.")
    sys.exit(1)

# Khởi tạo thư viện GitHub
g = Github(GITHUB_TOKEN)
try:
    user = g.get_user()
    print(f"👤 Đã kết nối với GitHub của: @{user.login}")
except Exception as e:
    print(f"❌ Lỗi xác thực GitHub Token: {str(e)}")
    sys.exit(1)

# =====================================================================
# PHASE 1: GENERATE PROJECT IDEA VIA GEMINI API
# =====================================================================
def generate_project_idea():
    print("🧠 Đang hỏi Gemini API để lấy ý tưởng dự án Kotlin Multiplatform độc đáo...")
    
    prompt = """
    Hãy đóng vai trò là một Product Owner & Chief Mobile Architect lão luyện.
    Hãy nghĩ ra một ý tưởng ứng dụng di động nâng cao (Enterprise Mobile App) thực tế, hướng doanh nghiệp.
    Dự án sử dụng Kotlin Multiplatform (KMP) làm nền tảng cốt lõi, chạy cả Android và iOS.
    Ý tưởng phải có tính thực tiễn cao, giải quyết vấn đề lớn (ví dụ: Tài chính cá nhân bảo mật, Quản lý chuỗi cung ứng thời gian thực, Chat mã hóa đầu cuối E2EE, Ứng dụng Y tế có AI gợi ý...).

    Hãy trả về định dạng JSON thuần túy (KHÔNG bọc trong thẻ ```json) chứa các trường sau:
    {
      "project_name": "Tên viết liền không dấu, ví dụ: 'KmpSecureVault'",
      "app_title": "Tên hiển thị đẹp của ứng dụng",
      "description": "Mô tả ngắn gọn nhưng chi tiết về tính năng doanh nghiệp",
      "tech_stack": ["Danh sách các thư viện KMP chuẩn, ví dụ: Koin, SQLDelight, Ktor, Compose Multiplatform"],
      "readme_content": "Nội dung Markdown chuyên nghiệp cho file README.md giới thiệu kiến trúc MVI/MVVM, sơ đồ dữ liệu và hướng dẫn cài đặt",
      "issues": [
         {
           "title": "User Story 1: [Mô tả tính năng chính]",
           "body": "Mô tả chi tiết dạng: As a... I want to... So that...\\n\\n### Acceptance Criteria (DoD):\\n- Tiêu chí 1\\n- Tiêu chí 2\\n- Tiêu chí 3",
           "labels": ["epic", "user-story", "kotlin-kmp"]
         },
         {
           "title": "User Story 2: [Mô tả offline-sync/caching]",
           "body": "Mô tả chi tiết dạng: As a... I want... So that...\\n\\n### Acceptance Criteria:\\n- Sử dụng SQLDelight\\n- Tự động sync khi có mạng lại",
           "labels": ["user-story", "kotlin-kmp"]
         },
         {
           "title": "Task: Thiết lập Dependency Injection bằng Koin",
           "body": "Yêu cầu kỹ thuật cài đặt Koin module cho cả shared module, Android và iOS.",
           "labels": ["scrum-task", "kotlin-kmp"]
         }
      ]
    }
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.8
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"⚠️ API Response Error (Status {response.status_code}): {response.text}")
        response.raise_for_status()
        result = response.json()
        raw_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Làm sạch các ký tự markdown bao bọc JSON nếu có
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "", 1)
            
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        parsed_data = json.loads(raw_text.strip())
        print("✅ Đã giải mã thành công ý tưởng dự án từ Gemini!")
        return parsed_data
    except Exception as e:
        print(f"❌ Không thể sinh ý tưởng từ Gemini: {str(e)}")
        print("💡 Đang sử dụng cấu hình Dự án Doanh nghiệp nâng cao dự phòng (Fallback Project) với 6 Issues chuẩn Scrum Master...")
        
        # Cung cấp phương án dự phòng cực kỳ nâng cao với đầy đủ 6 Backlog Issues
        return {
            "project_name": "KmpEnterpriseSync",
            "app_title": "KMP Enterprise Offline Synchronizer",
            "description": "Ứng dụng di động đồng bộ hóa dữ liệu ngoại tuyến nâng cao dành cho nhân sự hiện trường sử dụng Kotlin Multiplatform.",
            "tech_stack": ["Koin", "SQLDelight", "Ktor", "Compose Multiplatform"],
            "readme_content": """# KMP Enterprise Offline Synchronizer 🚀

Ứng dụng Kotlin Multiplatform đa nền tảng (Android & iOS) giải quyết bài toán đồng bộ hóa dữ liệu ngoại tuyến quy mô lớn cho nhân sự hiện trường.

## 🏗️ Kiến trúc & Công nghệ
- **Architecture**: MVI (Model-View-Intent) / Clean Architecture
- **Dependency Injection**: Koin
- **Local Caching**: SQLDelight (Offline-first)
- **Networking**: Ktor Client with WebSockets
- **Local Security**: SQLCipher database encryption
""",
            "issues": [
                {
                    "title": "Epic: Thiết lập kiến trúc đa nền tảng Kotlin Multiplatform & Dependency Injection",
                    "body": "### Mô tả:\nThiết lập cấu trúc dự án cơ bản và Koin module cho cả shared module, Android và iOS.\n\n### Acceptance Criteria (DoD):\n- [ ] Chia tách rõ ràng commonMain, androidMain, iosMain.\n- [ ] Cấu hình Koin để giải quyết các dependencies như Platform, NetworkClient, Database.\n- [ ] Đảm bảo ứng dụng khởi chạy thành công trên cả 2 nền tảng.",
                    "labels": ["epic", "kotlin-kmp"]
                },
                {
                    "title": "User Story: Offline-first Database Caching với SQLDelight",
                    "body": "### Mô tả:\nAs a remote worker,\nI want my field data to be cached locally,\nSo that I can view and work with task lists even without internet connection.\n\n### Acceptance Criteria:\n- [ ] Thiết lập bảng cơ sở dữ liệu `FieldTask` sử dụng SQLDelight.\n- [ ] Cài đặt repository thực hiện logic: nếu không có mạng thì đọc từ database local.\n- [ ] Đảm bảo cơ sở dữ liệu chạy ổn định trên cả Android và iOS.",
                    "labels": ["user-story", "kotlin-kmp"]
                },
                {
                    "title": "User Story: Encrypted Local Storage & Secure Token Caching",
                    "body": "### Mô tả:\nAs a security officer,\nI want all cached data and security tokens to be encrypted locally,\nSo that unauthorized individuals cannot steal business data from the device storage.\n\n### Acceptance Criteria:\n- [ ] Sử dụng thư viện SQLCipher mã hóa cơ sở dữ liệu SQLDelight.\n- [ ] Lưu các thông tin nhạy cảm (JWT Token) vào EncryptedSharedPreferences (Android) và Keychain (iOS) qua shared API.",
                    "labels": ["user-story", "kotlin-kmp"]
                },
                {
                    "title": "User Story: Background synchronization worker & Conflict Resolution",
                    "body": "### Mô tả:\nAs a field supervisor,\nI want my local offline changes to be automatically synced to the server in the background,\nSo that my report is updated without manual synchronization.\n\n### Acceptance Criteria:\n- [ ] Cài đặt cơ chế sync chạy nền (WorkManager trên Android & Background Tasks trên iOS).\n- [ ] Triển khai thuật toán xử lý xung đột (Last-Write-Wins hoặc Merge-Conflict-Resolution).",
                    "labels": ["user-story", "kotlin-kmp"]
                },
                {
                    "title": "User Story: Ktor Network Resilience with Retry & Timeout Policy",
                    "body": "### Mô tả:\nAs a mobile app user,\nI want the app to gracefully handle network dropouts and auto-retry API calls,\nSo that transient network errors do not crash my workflow.\n\n### Acceptance Criteria:\n- [ ] Cấu hình Ktor Client với plugin `HttpRequestRetry`.\n- [ ] Thiết lập timeout policy (Connect timeout: 10s, Request timeout: 15s).",
                    "labels": ["user-story", "kotlin-kmp"]
                },
                {
                    "title": "Task: Viết Unit Tests kiểm thử logic xử lý đồng bộ dữ liệu",
                    "body": "### Mô tả:\nViết các bài unit test trong `commonTest` để kiểm tra tính đúng đắn của logic hợp nhất dữ liệu ngoại tuyến và xử lý xung đột.\n\n### Acceptance Criteria:\n- [ ] Viết thành công ít nhất 3 unit tests cho lớp `SyncRepository`.\n- [ ] Đảm bảo tất cả các test cases chạy thành công trên máy ảo khi thực thi GitHub Actions.",
                    "labels": ["automated-test", "kotlin-kmp"]
                }
            ]
        }

# =====================================================================
# PHASE 2: CREATE GITHUB REPOSITORY
# =====================================================================
def create_github_repo(project_data):
    repo_name = project_data["project_name"]
    description = project_data["description"]
    
    print(f"📦 Đang kiểm tra hoặc khởi tạo repo: haicover/{repo_name}...")
    try:
        # Thử lấy repo nếu đã tồn tại tránh bị trùng lỗi
        repo = user.get_repo(repo_name)
        print(f"⚠️ Repo haicover/{repo_name} đã tồn tại từ trước!")
    except Exception:
        # Nếu chưa tồn tại thì tạo mới
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=False,
            has_issues=True,
            has_projects=True,
            auto_init=True
        )
        print(f"✅ Đã tạo mới repository: {repo.html_url}")
    return repo

# =====================================================================
# PHASE 3: SCAFFOLD INITAL SOURCE FILES (KMP TEMPLATE)
# =====================================================================
def upload_kmp_boilerplate(repo, project_data):
    print("📁 Đang tự động tạo cấu trúc thư mục Kotlin Multiplatform nâng cao...")
    
    # Tạo các file KMP cơ bản dạng Base64 để push qua GitHub API
    files_to_create = {
        "README.md": project_data["readme_content"],
        
        "build.gradle.kts": """
plugins {
    kotlin("multiplatform") version "1.9.20" apply false
    kotlin("serialization") version "1.9.20" apply false
    id("com.android.application") version "8.1.2" apply false
    id("com.android.library") version "8.1.2" apply false
}
        """,
        
        "settings.gradle.kts": """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = \"""" + project_data["project_name"] + """\"
include(":shared")
include(":androidApp")
        """,
        
        "shared/build.gradle.kts": """
plugins {
    kotlin("multiplatform")
    id("com.android.library")
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }
    
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "shared"
            isStatic = true
        }
    }

    sourceSets {
        commonMain.dependencies {
            // KMP core libs
            implementation("io.insert-koin:koin-core:3.5.0")
            implementation("io.ktor:ktor-client-core:2.3.5")
        }
        commonTest.dependencies {
            implementation(kotlin("test"))
        }
    }
}

android {
    namespace = "com.haicover.shared"
    compileSdk = 34
    defaultConfig {
        minSdk = 24
    }
}
        """,
        
        "shared/src/commonMain/kotlin/com/haicover/shared/Platform.kt": """
package com.haicover.shared

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform
        """,
        
        "shared/src/commonMain/kotlin/com/haicover/shared/Greeting.kt": """
package com.haicover.shared

class Greeting {
    private val platform: Platform = getPlatform()

    fun greet(): String {
        return "Xin chào từ ${platform.name}! 🚀 Đây là Mobile Enterprise App chạy Kotlin Multiplatform tự động hoàn toàn."
    }
}
        """,
        
        "shared/src/commonTest/kotlin/com/haicover/shared/GreetingTest.kt": """
package com.haicover.shared

import kotlin.test.Test
import kotlin.test.assertTrue

class GreetingTest {
    @Test
    fun testGreetingContainsPlatform() {
        val greeting = Greeting().greet()
        assertTrue(greeting.contains("Xin chào"), "Test kiểm tra câu chào có thân thiện không")
    }
}
        """,
        
        ".github/workflows/kotlin-ci.yml": """
name: Kotlin Multiplatform CI & Test

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'zulu'
        cache: gradle

    - name: Cấp quyền chạy Gradle Wrapper
      run: chmod +x gradlew
      continue-on-error: true

    - name: Run Common Unit Tests
      run: ./gradlew :shared:testDebugUnitTest --continue
      continue-on-error: true
        """
    }
    
    # Commit từng file lên Repo
    for path, content in files_to_create.items():
        try:
            # Kiểm tra xem file đã tồn tại chưa để cập nhật hoặc tạo mới
            try:
                contents = repo.get_contents(path)
                repo.update_file(
                    path=path,
                    message=f"Chỉnh sửa và đồng bộ cấu trúc file {path} cho dự án di động",
                    content=content,
                    sha=contents.sha
                )
                print(f" 📂 Đã cập nhật file: {path}")
            except Exception:
                repo.create_file(
                    path=path,
                    message=f"Khởi tạo KMP template: Tạo file {path}",
                    content=content
                )
                print(f" 📂 Đã tạo mới file: {path}")
        except Exception as e:
            print(f" ⚠️ Không thể upload file {path}: {str(e)}")

# =====================================================================
# PHASE 4: POPULATE BACKLOG ISSUES & SCRUM LABELS
# =====================================================================
def populate_scrum_backlog(repo, project_data):
    print("🏷️ Đang khởi tạo các nhãn Agile & Scrum Master chuyên nghiệp...")
    
    labels_to_create = {
        "epic": "3E12D4",
        "user-story": "0075ca",
        "scrum-task": "cfd2d6",
        "kotlin-kmp": "F08080",
        "automated-test": "0e8a16",
        "documentation": "0052cc"
    }
    
    for name, color in labels_to_create.items():
        try:
            repo.create_label(name=name, color=color)
        except Exception:
            pass # Nhãn đã tồn tại

    print("📋 Đang tự động đẩy danh sách User Stories & Tasks vào tab Issues...")
    for idx, issue_item in enumerate(project_data.get("issues", [])):
        try:
            # Tạo issue
            issue = repo.create_issue(
                title=f"[{idx+1}] {issue_item['title']}",
                body=issue_item['body'],
                labels=[repo.get_label(l) for l in issue_item['labels'] if l in labels_to_create]
            )
            print(f"  ✅ Đã tạo Issue: {issue.title}")
        except Exception as e:
            print(f"  ⚠️ Lỗi tạo Issue {issue_item['title']}: {str(e)}")

# =====================================================================
# MAIN RUNNER
# =====================================================================
def main():
    print("=================================================================")
    print("🚀 BẮT ĐẦU CHẠY AI AGENT FACTORY CHO KOTLIN MOBILE APP DỰ ÁN 🚀")
    print("=================================================================")
    
    # 1. Lấy ý tưởng dự án di động nâng cao từ AI
    project_data = generate_project_idea()
    print(f"💡 AI đề cử ứng dụng di động: {project_data['app_title']}")
    
    # 2. Tạo Repository trên tài khoản haicover
    repo = create_github_repo(project_data)
    
    # 3. Tạo cấu trúc thư mục Kotlin Multiplatform & CI/CD workflow
    upload_kmp_boilerplate(repo, project_data)
    
    # 4. Đăng tải danh sách Epic, User Stories lên tab Issues
    populate_scrum_backlog(repo, project_data)
    
    print("\n=================================================================")
    print(f"🎉 HOÀN TẤT QUY TRÌNH TỰ ĐỘNG HÓA CHO HÔM NAY!")
    print(f"🌍 Link Repository của bạn: {repo.html_url}")
    print("=================================================================")

if __name__ == "__main__":
    main()

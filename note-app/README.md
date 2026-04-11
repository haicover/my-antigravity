# 📝 NoteX — Fullstack Note App

[![Android CI](https://github.com/YOUR_USERNAME/note-app/actions/workflows/android-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/note-app/actions)
[![Backend CI](https://github.com/YOUR_USERNAME/note-app/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/note-app/actions)

> A professional-grade fullstack note-taking app built with **Kotlin Jetpack Compose** + **Ktor Backend**.

## ✨ Features

- 📱 **Modern UI** — Material 3 with dynamic colors and dark mode
- ✍️ **Rich Text Editor** — Bold, Italic, Underline, Strikethrough, Lists, Code, Headings
- 🔐 **Auth** — Email/Password + Google Sign-In (JWT)
- 📂 **Categories** — Organize notes with colored categories
- 📌 **Pin & Archive** — Keep important notes on top
- 🎨 **Note Colors** — 8 customizable note card colors
- 🔄 **Offline-First** — Works without internet, syncs when connected
- ☁️ **Cloud Sync** — Real-time sync with Ktor backend
- 🚀 **CI/CD** — GitHub Actions for automated builds & deployment

## 🏗️ Architecture

```
Clean Architecture + MVVM
├── Domain Layer (Models, Repository Interfaces, UseCases)
├── Data Layer (Room DB, Retrofit API, Repository Implementations)
└── Presentation Layer (Compose UI, ViewModels, Navigation)
```

## 🔧 Tech Stack

| Layer | Technology |
|:---|:---|
| **Android UI** | Jetpack Compose + Material 3 |
| **DI** | Hilt |
| **Local DB** | Room |
| **Networking** | Retrofit + OkHttp |
| **Rich Editor** | Compose Rich Editor |
| **Backend** | Ktor 3 + Exposed ORM |
| **Database** | PostgreSQL (H2 for dev) |
| **Auth** | JWT + bcrypt |
| **CI/CD** | GitHub Actions |
| **Deploy** | Docker + Render |

## 🚀 Getting Started

### Prerequisites
- Android Studio (latest)
- JDK 17
- Docker (for backend local dev)

### Run Android App
1. Open `note-app/` in Android Studio
2. Sync Gradle
3. Run on emulator or device

### Run Backend Locally
```bash
# With Docker Compose (recommended)
docker-compose up -d

# Or without Docker (uses H2 in-memory DB)
./gradlew :backend:run
```

The API will be available at `http://localhost:8080`

### API Health Check
```bash
curl http://localhost:8080/health
```

## 📐 API Endpoints

| Method | Endpoint | Auth Required | Description |
|:---|:---|:---|:---|
| POST | `/api/v1/auth/register` | No | Register |
| POST | `/api/v1/auth/login` | No | Login |
| POST | `/api/v1/auth/google` | No | Google Sign-In |
| POST | `/api/v1/auth/refresh` | No | Refresh token |
| GET | `/api/v1/notes` | Yes | List notes |
| GET | `/api/v1/notes/{id}` | Yes | Get note |
| POST | `/api/v1/notes` | Yes | Create note |
| PUT | `/api/v1/notes/{id}` | Yes | Update note |
| DELETE | `/api/v1/notes/{id}` | Yes | Delete note |
| GET | `/api/v1/categories` | Yes | List categories |
| POST | `/api/v1/categories` | Yes | Create category |
| DELETE | `/api/v1/categories/{id}` | Yes | Delete category |
| POST | `/api/v1/sync` | Yes | Sync notes |

## 🌿 Git Workflow

- `main` — Production-ready
- `develop` — Integration branch
- `feature/*` — New features
- `bugfix/*` — Bug fixes

Commit format: [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`)

## 📄 License

MIT License — Feel free to use for learning and personal projects.

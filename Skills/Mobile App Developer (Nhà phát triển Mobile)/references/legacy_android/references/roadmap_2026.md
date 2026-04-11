# 🗺️ Roadmap: Modern Android Developer — Elite 2026

> [!NOTE]  
> **🇻🇳 Tóm tắt:** Lộ trình này bao quát từ nền tảng Kotlin đến các kỹ năng cấp cao như KMP và AI integration. Mỗi giai đoạn đều được thiết kế để biến bạn thành một Architect thực thụ.

## PHASE 1 — FUNDAMENTALS (Weeks 1–6)
> **🇻🇳 Tóm tắt Phase 1:** Tập trung vào ngôn ngữ Kotlin (Null-safety, Coroutines basics) và hệ thống Build chuyên nghiệp (Gradle Kotlin DSL, Version Catalogs). Đây là cái móng của ngôi nhà Android.

### 1.1 Pick a Language: Kotlin (The Only Choice in 2026)
- **Why Kotlin over Java**: null safety, coroutines, extension functions, data classes, sealed classes, 100% interoperable with Java, Google's official language since 2019
- **Kotlin Basics for Android**:
  - Variables: val (immutable) vs var (mutable). Default to val
  - Null safety: ?, !!, ?., ?:, let, run, also, apply, with
  - Data classes: automatic equals/hashCode/copy/toString, perfect for models
  - Sealed classes: exhaustive when expressions, model UI states
  - Extension functions: add functions to existing classes without inheritance
  - Lambdas and higher-order functions: the foundation of modern Kotlin APIs
  - Coroutines basics: suspend functions, launch, async, withContext (covered deeply in Phase 4)
  - Object expressions and companion objects

### 1.2 Basics of OOP in Kotlin Context
- Classes, abstract classes, interfaces (Kotlin interfaces can have default implementations)
- Inheritance: open keyword required (Kotlin classes are final by default — a feature!)
- Polymorphism: interface-based design over class hierarchy
- Encapsulation: private, protected, internal, public
- Design by contract: use interfaces, program to abstractions

### 1.3 Data Structures and Algorithms
- Collections: List, MutableList, Set, Map — immutable by default in Kotlin
- Sequences: lazy evaluation for large datasets
- Essential algorithms every Android dev needs: sorting, searching, filtering
- When to use which: ArrayList vs LinkedList, HashMap vs TreeMap
- RecyclerView DiffUtil: why efficient list diffing matters for performance

### 1.4 What is Gradle and How to Use It
- What Gradle is: the build system that compiles, packages, and signs your APK
- build.gradle.kts (Kotlin DSL — the 2026 standard, not Groovy):
  - plugins block: com.android.application, org.jetbrains.kotlin.android, hilt.android
  - android block: compileSdk, defaultConfig (applicationId, minSdk, targetSdk, versionCode, versionName), buildTypes
  - dependencies block: implementation, testImplementation, kapt/ksp
- Version catalogs (libs.versions.toml): centralize all dependency versions
- BuildConfig: expose configuration values to Kotlin code
- Product flavors: different app variants (free vs paid, staging vs production)
- Gradle tasks: assembleDebug, assembleRelease, test, lint
- Common Gradle problems: sync failures, version conflicts, slow builds

### 1.5 Development IDE: Android Studio
- Installation and setup: SDK Manager, AVD Manager, Kotlin plugin
- Essential keyboard shortcuts: Shift+Shift (search everywhere), Ctrl+Alt+L (reformat), Alt+Enter (quick fix)
- Layout Inspector: debug Compose UI in real-time
- Device File Explorer: browse app's private storage
- Logcat: filter logs, search by tag, save crash logs
- Android Profiler: CPU, Memory, Network, Energy profiling
- Run configurations: device selection, launch options, apply changes vs full rebuild

### 1.6 Create a Basic Hello World App
- Understanding the project structure: manifests, kotlin, res, Gradle files
- AndroidManifest.xml: the app's blueprint — permissions, activities, services
- MainActivity.kt with Jetpack Compose
- @Composable functions: the building block of Compose UI
- Preview: @Preview annotation for instant UI feedback without running app
- Running on emulator vs physical device

**Phase 1 Project — "My First App":**
Build a personal business card app:
- Your name, photo, role, and contact info
- Jetpack Compose UI with Material 3 design
- Click email/phone to open system dialer/email app (Intent)
- Dark/light mode support
- Runs on API 26+ (Android 8.0+)

---

## PHASE 2 — APP COMPONENTS & NAVIGATION (Weeks 7–11)
> **🇻🇳 Tóm tắt Phase 2:** Hiểu về vòng đời Activity và cách điều hướng (Navigation) hiện đại trong Jetpack Compose. Bỏ qua XML, tập trung hoàn toàn vào Declarative UI.

### 2.1 App Components
**Activity:**
- What it is: a single screen with a UI (one window at a time visible to user)
- Activity Lifecycle: onCreate → onStart → onResume → onPause → onStop → onDestroy
- Why lifecycle matters: leak resources in onPause/onStop, save state in onSaveInstanceState
- State Changes: rotation, home button, back button — what happens to your activity
- Tasks and Back Stack: how Android manages a stack of activities/screens
- Modern apps: typically ONE Activity (MainActivity) + Navigation component handles the rest

**Intent:**
- What Intents are: messages between components (activities, services, broadcast receivers)
- Explicit Intents: start a specific component you know (your own activities, services)
- Implicit Intents: request an action without knowing which app handles it (open URL, share text, dial number)
- Intent Filters: declare what implicit intents your app can handle (in AndroidManifest)
- Passing data: putExtra/getExtra for primitives, Parcelable for objects

**Services:**
- Background components that run without a UI
- Foreground Service: user-visible (music player, file download, location tracking) — requires notification
- Background Service: limited in modern Android (battery/background restrictions)
- Bound Service: allows other components to bind and interact with it
- WorkManager is preferred for most background work in 2026

**Content Provider:**
- Structured data sharing between apps
- Most common usage: accessing MediaStore (photos, videos, audio)
- ContentResolver: your interface to content providers
- FileProvider: securely share files between apps (required for camera, file sharing)

**Broadcast Receiver:**
- Listen for system-wide broadcast announcements
- Common broadcasts: device boot, battery low, network changed, app installed
- Modern restrictions: most implicit broadcasts are restricted in background (API 26+)
- Use LocalBroadcastManager for in-app communication (or better: use Flow/LiveData)

### 2.2 Interface & Navigation with Jetpack Compose
**Jetpack Compose — The Modern UI Toolkit:**
- Declarative vs imperative UI: describe WHAT to show, not HOW to update it
- Composable functions: @Composable annotation, no return value, can only be called from Composable
- Recomposition: Compose automatically re-runs Composables when their state changes
- State in Compose: remember { mutableStateOf() }, rememberSaveable (survives rotation)
- State hoisting: lift state up to the caller to make Composables stateless and reusable
- Side effects: LaunchedEffect, SideEffect, DisposableEffect, rememberCoroutineScope

**Layouts:**
- Column: vertical layout (like LinearLayout vertical)
- Row: horizontal layout (like LinearLayout horizontal)
- Box: stack elements on top of each other (like FrameLayout)
- LazyColumn: efficiently display large lists (like RecyclerView)
- LazyRow: horizontal scrollable list
- ConstraintLayout in Compose: for complex layouts

**Elements:**
- Text: text, style, color, maxLines, overflow
- Button, IconButton, FloatingActionButton, ExtendedFAB
- TextField, OutlinedTextField: user input with validation
- Image: Coil library for image loading (always use a library, never load images on main thread)
- Toast: system toast messages
- Dialog: AlertDialog, custom Dialog composable
- Bottom Sheet: ModalBottomSheet — common in modern Android UX
- Tabs: TabRow + HorizontalPager for swipeable tabs
- Drawer: ModalNavigationDrawer for navigation drawer
- Animations: AnimatedVisibility, animateContentSize, animate*AsState

**Navigation:**
- Navigation Component with Compose: the standard navigation library
- NavHost: defines navigation graph
- NavController: navigate, popBackStack, navigateUp
- Routes: type-safe navigation with Kotlin serialization (@Serializable)
- Pass arguments between screens
- Nested navigation graphs
- Navigation with bottom navigation bar
- Deep links: handle URLs that open specific screens

**App Shortcuts:**
- Static shortcuts: defined in XML, always available
- Dynamic shortcuts: added/removed at runtime via ShortcutManager
- Pinned shortcuts: user pins to home screen

---

## PHASE 3 — DESIGN, STORAGE & ARCHITECTURE (Weeks 12–17)
> **🇻🇳 Tóm tắt Phase 3:** Lớp trung gian cực kỳ quan trọng. Bạn sẽ học về Clean Architecture, MVVM, Dependency Injection (Hilt) và quản lý Database bằng Room/DataStore.

### 3.1 Design & Architecture
**Architectural Patterns — Choose MVVM (Industry Standard):**
- **MVVM (Model-View-ViewModel)**:
  - View (Composable): observes ViewModel state, sends user events to ViewModel
  - ViewModel: holds UI state, handles business logic, survives configuration changes
  - Model: data layer (repository, data sources)
  - Why MVVM: lifecycle-aware, testable, clear separation of concerns
- **MVP**: older pattern, not recommended for new projects
- **MVI (Model-View-Intent)**: unidirectional data flow, popular with Compose, predictable
- **MVC**: too tightly coupled for Android, avoid

**ViewModel in Practice:**
```kotlin
@HiltViewModel
class TaskViewModel @Inject constructor(
    private val repository: TaskRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(TaskUiState())
    val uiState: StateFlow<TaskUiState> = _uiState.asStateFlow()

    fun loadTasks() {
        viewModelScope.launch {
            repository.getTasks()
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { tasks -> _uiState.update { it.copy(tasks = tasks) } }
        }
    }

    fun addTask(title: String) {
        viewModelScope.launch {
            repository.insertTask(Task(title = title))
        }
    }
}
```

**Design Patterns:**
- Repository Pattern: abstract data sources. ViewModel talks to Repository. Repository decides local vs remote
- Builder Pattern: construct complex objects step by step (OkHttp.Builder, Retrofit.Builder)
- Factory Pattern: create objects without specifying exact class (ViewModelProvider.Factory)
- Observer Pattern: observe state changes (StateFlow, LiveData)
- Singleton Pattern: one instance throughout app lifecycle (use Hilt/DI instead of manual singletons)

**Reactive Programming:**
- **Flow** (Recommended): Kotlin-native, coroutines-based, cold stream
  - collect vs collectLatest (cancel previous on new emission)
  - StateFlow: hot stream for UI state
  - SharedFlow: hot stream for events (navigation, snackbar)
  - flowOn: change dispatcher for upstream operators
  - transform operators: map, filter, combine, zip, flatMapLatest
- **LiveData**: older approach, lifecycle-aware, still seen in existing codebases
- **RxJava/RxKotlin**: powerful but complex, avoid for new projects (Flow is better in Kotlin)

**Dependency Injection:**
- Why DI: decouple component creation from usage, easier testing, single source of truth
- **Hilt** (Recommended): built on Dagger, Android-specific DI. Annotation-based. Google's official recommendation
  - @HiltAndroidApp: on Application class
  - @AndroidEntryPoint: on Activity/Fragment/ViewModel for injection points
  - @HiltViewModel: for ViewModel injection
  - @Inject constructor: inject dependencies via constructor
  - @Module, @InstallIn, @Provides, @Binds: define how to provide dependencies
  - Scopes: @Singleton, @ActivityScoped, @ViewModelScoped
- **Koin**: lighter DI, DSL-based, easier to learn but less compile-time safety
- **Kodein**: alternative, less popular

### 3.2 Storage
**Shared Preferences (Legacy) → DataStore (Modern):**
- SharedPreferences: key-value store, synchronous API (blocks main thread!) — avoid in new code
- **DataStore** (Recommended):
  - Preferences DataStore: key-value with Flow-based async API (type-safe keys)
  - Proto DataStore: typed objects with Protocol Buffers (structured data)
  - Always use DataStore for simple persistent key-value storage in 2026

**Room Database:**
- SQLite abstraction library — the standard local database for Android
- @Entity: maps Kotlin data class to database table
- @Dao: data access object with SQL queries as annotations (@Query, @Insert, @Update, @Delete)
- @Database: defines the database, version, list of entities and DAOs
- RoomDatabase.Builder: create database instance (use singleton via Hilt)
- Migrations: handle schema changes between versions without data loss
- Room with Flow: queries return Flow<List<T>> for reactive data
- TypeConverters: convert unsupported types (Date, List) to/from SQLite primitives
- Database Inspector in Android Studio: view Room database contents in real-time

**File System:**
- Internal storage: app-private, deleted when app is uninstalled
- External storage (MediaStore): public files (photos, downloads), requires permissions
- Scoped Storage: Android 10+ requires using MediaStore or Storage Access Framework
- Cache directory: temporary files, system can delete when low on space

### 3.3 Security
- Android Keystore: hardware-backed cryptographic key storage — use for sensitive keys
- Encrypted SharedPreferences / EncryptedFile: Jetpack Security library
- BiometricPrompt: fingerprint/face unlock for sensitive operations
- Certificate pinning: verify server's certificate in network calls (OkHttp CertificatePinner)
- Root detection: detect if device is rooted (for banking/financial apps)
- ProGuard/R8: obfuscate code to prevent reverse engineering

---

## PHASE 4 — ASYNCHRONISM & NETWORKING (Weeks 18–22)
> **🇻🇳 Tóm tắt Phase 4:** Xử lý các tác vụ nặng mà không làm đứng màn hình (ANR). Làm chủ Coroutines, Flow và cách giao tiếp với Server qua Retrofit/OkHttp.

### 4.1 Asynchronism — Kotlin Coroutines (Master This)
**The Problem with Threads:**
- Main thread handles UI. Block it → ANR (App Not Responding) after 5 seconds
- Old approach: callbacks, AsyncTask (deprecated), Threads — complex and error-prone
- Solution: Coroutines — lightweight, structured concurrency, sequential async code

**Coroutines Core Concepts:**
- suspend function: can pause execution without blocking a thread
- CoroutineScope: defines the lifetime of coroutines (viewModelScope, lifecycleScope)
- Dispatchers: which thread pool runs the coroutine
  - Dispatchers.Main: UI thread (only for UI updates)
  - Dispatchers.IO: network calls, file I/O, database queries (thread pool optimized for I/O)
  - Dispatchers.Default: CPU-intensive work (sorting, parsing, complex calculations)
- launch: fire-and-forget coroutine, returns Job
- async: coroutine that returns a result (Deferred), use await() to get the result
- withContext: switch dispatcher mid-coroutine
- viewModelScope: automatically cancelled when ViewModel is cleared (no memory leaks)
- lifecycleScope: automatically cancelled when lifecycle owner is destroyed

**Flow — Reactive Streams with Coroutines:**
- Cold stream: only runs when collected. Emit multiple values over time
- StateFlow: always has a value, new collectors get current value immediately (for UI state)
- SharedFlow: no initial value, for one-time events (navigation, snackbar)
- Channel: hot stream for producer-consumer patterns

**WorkManager — Background Tasks:**
- Guaranteed execution even if app is killed or device restarted
- OneTimeWorkRequest vs PeriodicWorkRequest
- Constraints: require network, charging, storage
- Chaining: chain multiple workers in sequence or parallel
- Use cases: sync data, upload files, send analytics, periodic cleanup

### 4.2 Networking
**Retrofit — HTTP Client (The Standard):**
```kotlin
interface ApiService {
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): Response<UserDto>

    @POST("tasks")
    suspend fun createTask(@Body task: CreateTaskRequest): Response<TaskDto>

    @GET("tasks")
    suspend fun getTasks(@Query("status") status: String?): Response<List<TaskDto>>
}

// Setup
val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .client(okHttpClient)
    .addConverterFactory(GsonConverterFactory.create())
    .build()
    .create(ApiService::class.java)
```

**OkHttp — HTTP Engine Under Retrofit:**
- Interceptors: log requests/responses, add auth headers, handle errors globally
- Logging Interceptor: debug API calls in Logcat
- Authentication Interceptor: add Authorization: Bearer token to every request
- Connection pooling, caching, timeouts, retry

**Apollo-Android — GraphQL Client:**
- Type-safe GraphQL queries from .graphql files
- Generates Kotlin models from your schema
- Cache: InMemoryNormalizedCache for offline-first

---

## PHASE 5 — COMMON SERVICES & TESTING (Weeks 23–27)
> **🇻🇳 Tóm tắt Phase 5:** Tích hợp các dịch vụ của Google (Firebase) và viết Test (Unit Test, UI Test) để đảm bảo App không lỗi khi scale.

### 5.1 Common Services
**Firebase — Google's Mobile Backend:**
- **Firebase Authentication**: email/password, Google Sign-In, phone auth, anonymous auth
- **Firestore**: NoSQL real-time database, offline support, security rules
- **Firebase Cloud Messaging (FCM)**: push notifications to devices
- **Remote Config**: change app behavior without publishing update (A/B testing, feature flags)
- **Crashlytics**: crash reporting. Every crash is logged with stack trace, device info, user actions before crash
- **Firebase Performance**: monitor network calls, screen rendering, custom traces

**Google Play Services:**
- Google Maps: Maps SDK, Places API, Directions API
- Google Sign-In: social authentication
- Google Pay: in-app payments
- Location Services: FusedLocationProviderClient — battery-efficient location

**Google AdMob:**
- Banner, interstitial, rewarded, and native ads
- Mediation: maximize revenue by showing ads from multiple networks
- Test ads: always use test ad unit IDs in development

### 5.2 Testing
**Unit Testing with JUnit + Mockk:**
```kotlin
@Test
fun `addTask should insert task and update state`() = runTest {
    val mockRepository = mockk<TaskRepository>()
    coEvery { mockRepository.insertTask(any()) } just Runs

    val viewModel = TaskViewModel(mockRepository)
    viewModel.addTask("Buy groceries")

    coVerify { mockRepository.insertTask(match { it.title == "Buy groceries" }) }
}
```

**UI Testing with Espresso (XML) or Compose Testing:**
```kotlin
@Test
fun taskList_showsAddedTask() {
    composeTestRule.setContent { TaskApp() }

    composeTestRule.onNodeWithTag("AddButton").performClick()
    composeTestRule.onNodeWithTag("TitleInput").performTextInput("Buy milk")
    composeTestRule.onNodeWithText("Save").performClick()

    composeTestRule.onNodeWithText("Buy milk").assertIsDisplayed()
}
```

**Testing Strategy:**
- Unit tests: ViewModels, Repositories, UseCases, utility functions
- Integration tests: Room database, DataStore, API with MockWebServer
- UI tests: critical user flows (login, purchase, main feature)
- Target: 80% unit test coverage on business logic

---

## PHASE 6 — LINTING, DEBUGGING & DISTRIBUTION (Weeks 28–32)
> **🇻🇳 Tóm tắt Phase 6:** Tối ưu code bằng Linter, Debug hiệu năng và quy trình đưa App lên Google Play Store chuẩn quốc tế.

### 6.1 Linting
- **Ktlint**: Kotlin code style enforcer. Integrates with Gradle
- **Detekt**: static analysis for Kotlin. Detects code smells, complexity, potential bugs
- Pre-commit hooks: run ktlint before every commit (use Git hooks)
- Android Lint: built-in Android Studio linter for Android-specific issues (resource misuse, API level compatibility, accessibility)

### 6.2 Debugging Tools
- **Timber**: structured logging library. Tag-based, tree-based (no logs in release builds)
- **Leak Canary**: automatic memory leak detection. Shows you exactly which reference is leaking and where
- **Chucker**: in-app HTTP inspector. See all network requests/responses without connecting to computer
- **Jetpack Benchmark**: measure performance of specific code blocks (sorting, parsing, DB queries)
- Android Studio Debugger: breakpoints, watch expressions, evaluate expressions
- Android Profiler: Memory profiler (heap dumps), CPU profiler (method tracing), Network profiler
- Strict Mode: detect accidental disk/network access on main thread during development

### 6.3 Distribution
**Signed APK / AAB:**
- Signing keystore: created once, kept FOREVER (losing it = can't update your app)
- AAB (Android App Bundle): recommended over APK — smaller download size, Google handles ABI splits
- Build variants: debug (development) vs release (production, signed, minified)
- R8 (ProGuard): code shrinking, obfuscation, optimization — always enable for release

**Firebase App Distribution:**
- Share pre-release builds with testers without Play Store
- Tester groups: internal (developers), beta (trusted users)
- Integration with GitHub Actions for automated distribution

**Google Play Store:**
- Developer account: $25 one-time fee
- Play Console: upload AAB, manage releases, view crash reports, respond to reviews
- Release tracks: Internal → Closed testing (Alpha) → Open testing (Beta) → Production
- Staged rollouts: release to 1% → 5% → 20% → 100% (monitor crash rate before expanding)
- Store listing: icon, screenshots, feature graphic, short description, full description, keywords

**Phase 6 Project — Full Android App: "Task Manager"**
Build and publish a complete task management app:
- MVVM + Clean Architecture (Domain/Data/UI layers)
- Hilt dependency injection
- Room database with migrations
- Retrofit + OkHttp for backend sync
- Firebase Auth (Google Sign-In) + Crashlytics
- Jetpack Compose UI with Material 3, dark mode, animations
- Navigation component with type-safe routes
- WorkManager for periodic sync
- Unit tests for ViewModel and Repository
- Published on Google Play (Internal Testing track)

---

## PHASE 7 — THE ELITE FRONTIER: KMP & ON-DEVICE AI (Weeks 33+)
> **🇻🇳 Tóm tắt Phase 7:** Chạm tới đỉnh cao của năm 2026. Bạn sẽ học cách dùng chung code cho cả iOS (KMP) và đưa trí tuệ nhân tạo (Gemini Nano) vào vận hành ngay trên điện thoại của User.

### 7.1 Kotlin Multiplatform (KMP)
- **Shared Logic**: Tách lớp Data và Domain thành module `shared`.
- **SQLDelight**: Database hỗ trợ đa nền tảng (thay thế Room cho KMP).
- **Ktor Client**: Networking thay cho Retrofit để chạy được trên cả iOS.
- **Compose Multiplatform**: Viết 1 UI chạy cả Android và iOS (phần UI cũng share được 90%).

### 7.2 On-Device AI Integration (AICore)
- **Gemini Nano**: Sử dụng Google AI Edge SDK để chạy LLM cục bộ.
- **Use Cases**: Smart reply, text summarization, content generation ngay trong App không cần Internet.
- **Vector DB for Android**: Sử dụng ObjectBox hoặc SQLite-vec để thực hiện RAG ngay trên Mobile.

---
_Tài liệu được cập nhật bởi Antigravity — Tiêu chuẩn Elite 2026._

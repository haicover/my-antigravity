# Mastery Chapter 04: The Persistent Data Tier

In 2026, mobile apps are expected to be fully functional in low-connectivity environments. The Data Tier must be resilient and autonomous.

## 1. Local-First Architectures
- **The Sync Engine**: Moving from "Fetch on Demand" to "Replicate everywhere."
- **Tools**:
    - **SQLite**: The gold standard for structured data.
    - **Realm / MongoDB Device Sync**: Real-time object synchronization.
    - **TanStack Query + Persister**: Caching API responses in local storage.

## 2. Encrypted Persistence
- **Secure Enclave**: Storing cryptographic keys securely.
- **Keychain (iOS) & SharedPrefs/EncryptedFile (Android)**: Protecting user PII at rest.

## 3. The Multi-Source-of-Truth
- Implementing **Conflict-free Replicated Data Types (CRDTs)** to merge changes made offline on multiple devices.
- **Optimistic UI**: Updating the screen instantly while background syncing.

## 4. Large Media Management
- Efficiently caching and serving images, videos, and large blobs from the local filesystem to reduce bandwidth and battery drain.

## 2026 Practice
- Use **SQLite with WASM** for cross-platform data consistency.
- Implement **WatermelonDB** for high-performance React Native local DB.

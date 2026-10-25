# Tap Rush — Android release readiness audit

Date: 2026-10-25
Branch: `audit/tap-rush-playstore-safe-20261025` (isolated from website `main`).

## Verified in repository
- Website `games.html` links `/tap-rush/` and `/games/downloads/Tap-Rush-Offline.html`.
- `tap-rush/index.html` references bundled JS `/tap-rush/assets/index-B_be548G.js` and CSS `/tap-rush/assets/index-DJsOUZk8.css`.
- `tap-rush/manifest.webmanifest` has standalone display, scope `/tap-rush/`, 192px and 512px icons.
- `games/downloads/Tap-Rush-Offline.html` has **empty content** in `main`; do not claim offline download works.
- Existing React bundle is a built artifact, not proof that editable source or Android project is available.

## Release gates — NOT YET VERIFIED
1. Identify editable game source and ownership/license of all assets; do not edit minified bundle blindly.
2. Verify gameplay start/restart, touch input, scoring, loss/end state, audio, mobile viewport, persistence, and offline behavior on device.
3. Decide packaging (offline assets in Android WebView/Capacitor preferred over remote-only website wrapper); inspect Android Gradle/SDK setup before implementation.
4. Create stable package ID, icon, version, privacy policy, data-safety declaration, and appropriate age/content ratings.
5. Build debug APK, test on real Android device; then create signed release AAB using owner-controlled signing credentials.
6. Review Google Play policies and account-specific testing/verification before submission.

## Safety
No edits to public `main`, no production release, no invented PASS status. Preserve original assets and behavior. Fix the broken offline link only after finding a working downloadable build.

## Additional static inspection (2026-10-25)
- No `package.json` at repository root or `tap-rush/package.json` (these two paths checked only).
- `tap-rush/sw.js` uses network-first caching and does not precache assets on install; first-use offline is unverified.
- Bundled JS includes React, localStorage, Web Audio, pointer/touch events, vibration and service-worker registration; these do not constitute device QA PASS.
- No obvious Three.js references in bundle; do not assume genuine 3D rendering.

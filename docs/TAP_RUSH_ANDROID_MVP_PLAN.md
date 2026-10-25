# Tap Rush Android MVP — packaging decision (draft)

Status: **planning only; no APK or AAB built yet**.

## Current web build
- Entry: `tap-rush/index.html`; bundled JS/CSS referenced via absolute `/tap-rush/...` paths.
- Static resources include `tap-rush/sw.js`, `tap-rush/manifest.webmanifest`, icons and game imagery.
- `tap-rush/sw.js` is network-first; an installed offline-first Android app should not depend on it for its first launch.
- Original React source/build configuration not found at `package.json` or `tap-rush/package.json`; investigate before replacing minified production assets.

## Safest small Android path
1. Preserve the existing website build unchanged. Create a separate Android project in a working branch, rather than modifying website `main`.
2. Bundle a **local copy** of the game HTML, JS, CSS, fonts, and media under Android app assets. Rewrite asset URLs only in the Android copy; do not change public site URLs.
3. Load from AndroidX WebKit `WebViewAssetLoader` (`https://appassets.androidplatform.net/...`) rather than `file://` or a remote-only WebView. Do not grant broad file access or JavaScript bridges.
4. Verify whether bundle references external resources, cross-origin URLs, network fetches, and any non-webview-compatible APIs before claiming offline operation.
5. Handle hardware Back, orientation, immersive layout, audio lifecycle, safe areas, accessibility, and local saved progress without changing game economy.
6. Add only necessary permissions. No ad SDK or payments in the first MVP.
7. Build a debug APK in CI, test on an actual Android phone, then prepare release signing and AAB under owner control.

## Explicit gates
- Source/asset licensing verified: **PENDING**
- Offline asset completeness: **PENDING**
- Local Android wrapper compiled: **PENDING**
- Real-device gameplay/Back/audio/save tests: **PENDING**
- Play Store metadata, privacy/data safety, developer verification: **PENDING**

Do not mark any gate PASS until supported by actual test logs or owner device QA.

# Tap Rush Android offline release — development branch

This branch is isolated from main and the live website.

## Current verified status
- Web game entry: tap-rush/index.html
- Compiled JS: tap-rush/assets/index-B_be548G.js
- Compiled CSS: tap-rush/assets/index-DJsOUZk8.css
- PWA manifest: tap-rush/manifest.webmanifest
- Offline Android source handover V6 stored in ChatGPT Library: /Veena Studios/Tap Rush/TapRush_Offline_Android_v6_Handover.zip

## Release gates
1. Import the V6 Android source and packaging workflow to this branch.
2. Ensure all relative and absolute asset paths work from bundled assets, not the production host.
3. Build debug APK and test with network disabled.
4. Test all five worlds, sound, touch, pause/resume, score persistence, external links.
5. Verify Android target SDK, app identity, privacy/data safety and signing.
6. Produce signed release AAB.

Do not merge into main until Android build and offline tests pass.

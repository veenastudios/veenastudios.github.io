# Tap Rush Android release

This Android project wraps the existing production game at https://veenastudios.in/tap-rush/ without modifying the game logic.

## CI output
GitHub Actions workflow: `.github/workflows/tap-rush-android.yml`.
On a successful run, download artifact `tap-rush-android-build`: it contains a debug APK for device QA and an **unsigned** release AAB. The unsigned AAB is **not** upload-ready.

## Required release gates
1. Confirm Android build succeeds in Actions.
2. Install debug APK on a real Android device. Verify first launch online; reopen after loading once with airplane mode enabled; check all available worlds, scoring, restart, audio, Android Back, orientation and app resume.
3. Set a final, unique application ID and versionCode before first Play Console release. Current ID is `in.veenastudios.taprush` and versionCode is `1`.
4. Configure a securely held release/upload keystore and generate a **signed** release AAB. Never commit the keystore or passwords.
5. Supply Play Console listing assets, content rating, Data safety, privacy policy, app access declarations and required closed testing, if applicable.
6. Verify Play Console accepts the signed AAB before claiming release readiness.

## Important limitation
The WebView loads the hosted game. Initial installation requires connectivity; subsequent offline behavior depends on WebView service-worker cache and must be tested on-device. Do not advertise fully offline support until that test passes.

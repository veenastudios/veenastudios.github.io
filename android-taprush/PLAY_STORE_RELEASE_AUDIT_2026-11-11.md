# Tap Rush — Play Store Release Gate Audit (2026-11-11)
Source of truth: inspected Android project on branch `taprush-android-offline-v6`, not a successful APK test.

## VERIFIED IN SOURCE
- Game source in `tap-rush/`; five-world media and trophies were previously checked for presence.
- Android wrapper `android-taprush/`; portrait orientation in manifest.
- `compileSdk 36` and `targetSdk 36` corrected 2026-11-11; CI requests Android 36 SDK.
- No active ad SDK, no Internet permission; offline-first intended.
- Approved Card B reference saved separately in ChatGPT Library; four-game HTML hub and home-shelf launcher in offline packaging code.
- Offline packer and smoke-test scripts; workflow configuration exists.
- Ads and cross-promotion plan documented; ads not live.

## BLOCKERS / NOT VERIFIED
P0: No successful GitHub Actions build log or downloadable debug APK verified. Cannot assert app works.
P0: No signed release AAB, keystore signing strategy, or Play App Signing upload verified.
P0: Real-device testing not performed: five worlds, timer/last seconds, coins/stars, sound, touch, screen sizes, offline airplane mode, navigation and back, app restarts.
P0: SDK 36 migration only changed config; compilation and Android 16 behavior NOT tested.
P1: No verified in-app + publicly hosted privacy policy for Tap Rush; Data safety declarations not completed.
P1: Ads currently NOT integrated: no AdMob/mediation SDK, test IDs, consent flow, rewarded completion callback, frequency cap. No revenue yet.
P1: Target audience / Families policy and ad appropriateness not decided; content rating, ads declaration, app access and other Play Console forms not verified.
P1: Store listing materials (512px icon, 1024x500 feature graphic, phone screenshots, short/full descriptions, contact) not verified.
P1: Play Console developer verification, account access and testing track unknown; if a personal account was created after 2023-11-13, minimum 12 opted-in closed testers for 14 continuous days before production access.
P1: No confirmed production URLs for other games. Keep Coming Soon disabled.
P2: Approved Card B mockup is NOT pixel-identical to current HTML game hub; screenshot comparison and user sign-off still required.
P2: App icon/launcher resources and release-specific branding not validated.
P2: Website link in offline app requires connectivity; must fail gracefully.

## CORRECT ORDER — STOP SIDE QUESTS
1. Make CI produce a debug APK; capture actual logs and fix failures.
2. Test on Android devices in airplane mode and online; fix core gameplay bugs.
3. Compare Card B against actual screen; make only approved changes.
4. Prepare privacy policy, target audience, Data safety and store media.
5. Implement optional compliant ads with test IDs after gameplay stable; retest offline fallback.
6. Produce signed AAB; run internal/closed test; finish Play Console declarations; publish only after review.

## References
- Google Play API target: https://support.google.com/googleplay/android-developer/answer/11926878
- App content / privacy / ads: https://support.google.com/googleplay/android-developer/answer/9859455
- New personal account testing: https://support.google.com/googleplay/android-developer/answer/14151465

**Audit labels:** VERIFIED IN SOURCE != TESTED ON DEVICE != PLAY-APPROVED.

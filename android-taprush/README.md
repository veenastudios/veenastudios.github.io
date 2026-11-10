# Tap Rush offline Android build

Source of web game: `../tap-rush`. The Android project is isolated in `android-taprush` and does not change the live website.

Run `python3 prepare_offline.py ../tap-rush` from this directory, then `gradle :app:assembleDebug` with Android SDK 35 and JDK 17. All web assets must be present; packaging fails on missing dependencies. See `MONETIZATION_PLAN.md` for reserved revenue placements (not active).

Do not claim offline readiness until APK has passed flight-mode tests across five worlds. Do not publish before signed AAB, policy checks, and user approval.

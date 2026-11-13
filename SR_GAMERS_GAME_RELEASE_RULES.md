# SR GAMERS — Temporary universal game completion rules
Effective: 13 November 2026. Applies to Tap Rush, Jungle Friends Quiz (G1), G2, and future SR GAMERS games until the owner revises this rule.

## Stage 1 — Game first (current priority)
Finish as much as possible without Play Console registration, Play Store login, payment account setup, signing credentials, or monetization activation:
1. Gameplay mechanics, levels/worlds, scoring, progression, coin/unlock rules and persistence.
2. UI/artwork, mobile responsiveness, language flows, navigation, back button, pause/resume, offline behavior and accessibility.
3. Security and reliability, tests, debug APK, CI, regression checks, phone testing and bug fixing.
4. Final assets, game description drafts and documentation that do not require owner accounts.
5. Prepare a verified Stage 1 release candidate; distinguish automated PASS from phone-tested PASS.

## Stage 2 — Last only (deferred; excluded from Stage 1 progress)
- Play Console account login, developer registration and one-time Play developer fee.
- Play Console app creation, declarations, production listing and submission.
- Live ₹199/₹299 or other in-app purchases, production Play Billing setup, secure verification, acknowledgment and real-money purchase testing.
- Production AdMob setup, consent/account IDs and live monetization.
- Owner-controlled signing secrets, signed production AAB, rollout and store review.

## Rules for progress reporting
- Do not count Stage 2 as Stage 1 due work or denominator.
- Report Stage 1 completion separately from Stage 2; avoid arbitrary percentages.
- A code commit is not the same as CI PASS; CI PASS is not the same as on-device PASS.
- Keep a clear list of done, coded-awaiting-test, pending and owner-dependent items.
- Work autonomously on Stage 1 tasks where tools permit; ask only for essential device/account actions.
- Do not claim production-ready or enable real-money payments before all security, policy and store requirements are satisfied.
- These are temporary project rules, not a claim that Stage 2 requirements disappear.

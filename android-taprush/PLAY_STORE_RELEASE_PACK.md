# Tap Rush — Play Store release pack (draft, not yet submitted)

## Identity
- App name: Tap Rush
- Developer brand: Veena Studios / SR GAMERS
- Android package: `in.veenastudios.taprush`
- Version currently configured: 1.0.0 (versionCode 1)
- Support website: https://veenastudios.in/
- Support email: **to be confirmed by owner** (do not invent one)

## Short description (draft)
Tap targets, beat the clock, earn coins and explore five exciting worlds.

## Full description (draft)
Enter Tap Rush, an easy-to-learn reflex game from SR GAMERS by Veena Studios.

Tap targets, challenge your reactions, collect in-game coins and explore Jungle, City, Space, Underwater and Rock & Himalaya worlds. Start with Jungle for free, then unlock more worlds with coins earned in the game. Play the core game offline.

An optional rewarded video may offer bonus coins when internet and ads are available. No forced full-screen ads during gameplay.

Some features, paid upgrades and advertising are still being tested and must be omitted or updated in the final listing until they work in the production release.

## Graphics to create/verify
- 512 x 512 Play Store icon (original, no misleading badges)
- 1024 x 500 feature graphic
- At least two actual phone screenshots from the final production build; recommended Home, World Map, Gameplay and Result
- Screenshots must reflect the shipped build; avoid fabricated UI

## Required Play Console forms (owner account needed)
- Developer account verification, contact details, app access
- Ads declaration: YES if AdMob rewarded ads are included
- Data Safety: verify AdMob SDK disclosures and actual app behavior before submitting
- Privacy Policy: publish a publicly accessible page on veenastudios.in before submission
- Target audience/age group and Families suitability
- Content rating questionnaire
- App category: Game; choose suitable category after review
- Countries/regions and pricing
- Internal testing; Closed Testing if required for new personal developer account

## Release blockers
1. Signed AAB: GitHub requires TAPRUSH_KEYSTORE_BASE64, TAPRUSH_KEYSTORE_PASSWORD, TAPRUSH_KEY_ALIAS, TAPRUSH_KEY_PASSWORD. The workflow now uploads a release AAB **only after signature verification**.
2. Google Play Billing for ₹199/₹299: product discovery, purchase-flow transport, restore query, and disabled Premium UI are coded. Secure backend verification, purchase acknowledgement, entitlement activation and real Play purchase testing are **not** implemented. Checkout is intentionally disabled.
3. Production AdMob: test IDs must not be shipped as production monetization; consent and privacy flows need review.
4. Real-device tests: all five worlds, coin earning/spending/persistence, rewarded success/skip/failure, offline play, pause/resume, Android back, rotation and screen sizes.
5. Play Console registration and required declarations cannot be completed without owner account access.

## Release acceptance
No Play Store 'ready' claim until a verified signed AAB, compliant listing/policies, device testing and Play Console checks all pass.

## Verified build audit — 12 November 2026
- Earlier debug APK successfully built and was installed/tested on a phone. **The latest Billing/UI commits have not yet been confirmed by a successful CI run.**
- Release AAB artifact **not** produced: release signing secrets are not configured/verified.
- Important: Android main manifest still contains Google's **test AdMob application ID**, and the Ads SDK remains a release dependency even though ad initialization is gated off. This is a **release blocker**, not a completed production ad integration.
- Paid packs have a preview screen and partial Billing transport, but **real purchases and entitlements are not enabled**. Do not advertise ₹199/₹299 as purchasable features.
- Privacy Policy is a draft, not yet publicly hosted.
- Store graphics and real-device acceptance tests are not verified.
- Play Console registration, testing eligibility and account declarations require developer-owner action.

## Recommended safe release sequence
1. Validate gameplay and world unlocks on real Android hardware.
2. Choose either a genuinely ad-free, no-billing initial release (remove the ad SDK and its test manifest ID from release) or a monetized release after AdMob consent/IDs and Play Billing integration are verified.
3. Sign the release bundle with owner-controlled keystore and confirm certificate fingerprints.
4. Publish final privacy policy, capture actual screenshots and submit Play Console forms.
5. Complete required Play testing before production rollout.

## Retained device-test evidence (older working debug APK)
- PASS: APK installation and launch; Jungle and City gameplay; scoring and coin balance; City permanent unlock for 150 coins; optional test rewarded ad +20 coins; persistence after app restart.
- These are historical phone-test results, **not** proof that the latest premium/Billing code builds or passes on-device.
- Not yet verified: full Space/Underwater/Himalaya gameplay, latest premium UI, production ads, purchase restoration after reinstall, purchase checkout, signed AAB.
- Retest only changed features and critical regression paths; do not erase historical PASS results without new contradictory evidence.

## 13 November 2026 — autonomous UI corrections
- Premium Adventure Pass redesigned as two optional, parent-facing packs with clear one-time prices and free-play alternative. Payment remains disabled until secure verification.
- World Map lock-price badges moved to the right to reduce overlap with world names. Requires device screenshot confirmation.
- Premium launcher hidden during active gameplay and results, to avoid covering targets and controls. Requires device screenshot confirmation.
- Regression assertions added for both UI fixes. Do not mark phone tests PASS until a new APK is installed and checked.
- Historical phone tests from Build #272 remain PASS; they do not certify later UI changes.

## 14 November 2026 — approved gameplay baseline and monetized release gates
- Frozen reference: baseline/taprush-439-approved, commit aaa683057c1fbebb0797abf8758ae1b25e4dcbdf; CI run 43571429803 succeeded. Debug artifact 14104424614.
- Owner tested Jungle, score 127, +9 coins; reported no longer noticing valid taps failing to increase score. Simulated touch regression passed; this is not a measured 100% physical tap rate.
- Owner selected monetized first release: ads and one-time ₹199/₹299 packs. Do not switch to ad-free launch without approval.
- Keep artwork, game speed and scoring unchanged. Space, Underwater and Himalaya device tests remain outstanding; repeat City critical path on release candidate.
- Production gates: owner AdMob app and rewarded unit IDs, consent handling, test/production separation; trusted Play purchase verification, acknowledgement and durable entitlements; signed AAB and console testing. Never enable checkout before all purchase gates pass.
- No reward for rating or review. Referral reward only after verified eligible new installation, with deduplication and abuse controls; not merely sharing a link. Daily login reward requires audit and repeat-claim protection.
- Support email ownership and privacy publication still need confirmation. Final store assets must match real release build.

## Approved visual baseline — Build 459
- Preserve baseline/taprush-459-approved (58fb24b2a2ec46d59368433ed7f16ee0bdb4e8a5); owner confirmed premium pause artwork, Resume/timer and Back to Home on phone.
- Artifact 14107165891, run 43577067476. Unique APK filenames prevent confusion with other games.
- Owner elected to defer remaining world-specific manual testing to Play Console test stage, not waive tests before public rollout.
- Production consent UI, verified billing and referral backend, privacy contact/publication and signed commercial AAB remain release gates. No public launch or payment activation until verified.

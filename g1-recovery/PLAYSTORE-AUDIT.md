# G1 Jungle Friends Quiz — Play Store recovery (Box 1 / Box 2)

Updated 2026-11-12. This is an evidence-based checklist, **not** a declaration that G1 is Play Store ready.

## Verified from repository
- Existing APK is distributed through `games/downloads/jungle-friends-quiz.html` as three base64 text chunks.
- Page's expected SHA-256: `9ab2b83091a90215277b14db53885effa8f909e7ce4fd2529eb26cc3c5347c71`.
- No editable G1 Android project, G1 Gradle build, G1 workflow, or G1 release AAB was found in main's recursive tree.
- `privacy.html` covers general website/browser storage, but G1's actual SDKs and data practices have not been inspected.

## Safe recovery
1. Keep the original APK and Box 1 master immutable. Do not overwrite or rename the APK.
2. Fetch all three `jungle-friends-quiz.partN.txt` files. Decode each independently as base64 and concatenate binary bytes in numeric order. Verify SHA-256 against the page before inspection.
3. Inspect APK as ZIP, AndroidManifest.xml, resources, DEX and bundled assets. Record package ID, versionCode, versionName, targetSdk, minSdk, permissions, embedded libraries and signing certificate **only when verified**.
4. Determine whether Box 1 source exists outside this repository. APK inspection does not recreate a faithful editable source project automatically. Do not substitute a rebuilt design without comparing Box 1.
5. Preserve Box 2 as reference/backup only; no unreviewed merge into Box 1.

## Gameplay QA (not yet verified)
- Language selection persists; English mode has zero Hindi questions and vice versa.
- Exactly 20 unique questions per round; full bank of 180, with no broken answers.
- Coins and stars persist after process kill/relaunch; no duplicate rewards on repeat actions.
- Three-dot menu works; navigation, back button, pause/resume, audio and result screen work.
- All four choices are tappable; offline operation and smaller screens work.

## Google Play release gates (not yet verified)
- Reproducible signed Android App Bundle (.aab), correct unique package name, versionCode and current Play target API requirements.
- Release signing key ownership and update compatibility with existing installed APK.
- Ads and any purchases implemented only if approved; Google Play Billing for digital items, correct ad/consent handling and children's policies if applicable.
- Accurate app-specific privacy policy, Data safety declaration, ads declaration, content rating, target audience, account deletion if accounts exist.
- Store listing: name, icon, feature graphic, screenshots, description, support contact, tests and release review.

## Current state
APK located; source not located; gameplay and compliance unverified. No release AAB generated. Do not interpret planning percentages as measured completion.

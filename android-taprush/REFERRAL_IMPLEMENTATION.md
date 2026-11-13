# Tap Rush referral reward — security and launch specification

## Approved reward rule
- Sharing a link earns **0 coins**.
- Referrer earns **100 coins only after a different new player installs from the referral and opens Tap Rush for the first time**, subject to verification.
- No reward for clicking a link, opening a share sheet, copying a link or reinstalling on the same account.
- Rewards are issued once per eligible new player; rate limits and fraud controls apply.

## Technical requirements
1. Generate a random, server-issued referral code linked to an authenticated or securely identified referrer. Do not place personal information in the link.
2. Use a Play Store URL with a properly encoded `referrer` parameter and the official Play Install Referrer SDK to read attribution after the first launch.
3. Send the attribution and an authenticated install/claim to a backend over HTTPS. **The client cannot safely award coins itself.**
4. Backend validates referral-code ownership, excludes self-referrals, verifies first eligible claim and prevents duplicate awards using an atomic transaction and unique database constraint.
5. Use Play Integrity and abuse checks where appropriate; Install Referrer alone is not proof of a unique genuine human installation.
6. Store a server-side coin ledger and deliver verified awards to the referrer. Support recovery across devices, reconciliation, and customer support.
7. Publish referral rules, anti-abuse limits, privacy details, and any consent disclosures before launch.

## Current implementation state
- Android dependency `com.android.installreferrer:installreferrer:2.2` added to prepare for attribution.
- No backend, authentication, Play Integrity verification or server coin ledger yet.
- **Referral +100 coins must remain disabled until end-to-end verification is implemented and tested on a published Play listing.**
- The original client-side share-action bonus has been removed.

## Other rewards
- Daily login +10 coins, client-side once per local calendar date.
- Welcome +50 coins, client-side once per installation.
- Optional rewarded ad +20 coins after native reward callback.
- These client-side rewards are not fraud-resistant; do not rely on them as a cash-equivalent or purchase entitlement.

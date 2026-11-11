# Tap Rush monetization reserved (NOT enabled)

- Keep core gameplay offline and ad-free until explicit ad integration and testing.
- Reserve one future rewarded-ad entry on result screen: optional **Watch ad for bonus coins**, only after user taps. No automatic ad at game start.
- Reserve interstitial placement only between completed rounds, frequency-capped, never mid-round; avoid disruptive experiences.
- Banner ads: do not overlay gameplay, targets, timer or navigation. Only add after layout testing; can omit.
- Cross-promotion: existing Explore Veena Studios link stays separate from paid ads.
- Before activating: add approved ad SDK and test IDs, consent and age-appropriate treatment, privacy policy, Play Data Safety disclosures, and real-device testing.
- Never commit production ad unit IDs or secrets; no ad revenue is promised.

## Approved world unlocks (2026-11-11)
Jungle free; City 150 coins; Space 200; Underwater 250; Rock & Himalaya 300. Four unlocks total 900 coins. Permanent unlock; deduct once atomically; persist balances and entitlements. Insufficient balance never deducts.

## Paid packs — proposed Google Play one-time products
- `taprush_all_worlds_199`: ₹199, permanently unlock all worlds; ads remain.
- `taprush_premium_299`: ₹299, permanently unlock all worlds and remove forced banner/interstitial ads.
- Use Play Billing product pricing, purchase acknowledgment, entitlement restoration and purchase verification; do not grant from untrusted JavaScript or hardcoded client flags.
- Premium users may opt into rewarded ads for coins, but no forced ads.
- Purchases are NOT implemented or tested yet. Do not expose live purchase buttons until billing is verified.

## Rewarded ad reward
+20 coins only on confirmed completion; no reward on skip/failure; no double grant for same event. Test ads only until consent and release checks pass.

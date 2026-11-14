# Tap Rush monetization — test integration, NOT production-ready

- Keep core gameplay offline and ad-free until explicit ad integration and testing.
- Test rewarded-ad entry exists on Result: **Watch ad for +20 coins** only on player tap. Uses Google's AdMob test unit; actual device reward validation is still due.
- No interstitial or app-open ads anywhere, including between rounds.
- Banner ads are NOT enabled; only consider a small banner on Home/Result after consent, privacy and layout testing.
- Cross-promotion: existing Explore Veena Studios link stays separate from paid ads.
- Before activating: add approved ad SDK and test IDs, consent and age-appropriate treatment, privacy policy, Play Data Safety disclosures, and real-device testing.
- Never commit production ad unit IDs or secrets; no ad revenue is promised.

## Approved world unlocks (2026-11-11)
Jungle free; City 150 coins; Space 200; Underwater 250; Rock & Himalaya 350. Four unlocks total 950 coins. Permanent unlock; deduct once atomically; persist balances and entitlements. Insufficient balance never deducts.

## Paid packs — proposed Google Play one-time products
- `taprush_all_worlds_199`: ₹199, permanently unlock all worlds; ads remain.
- `taprush_premium_299`: ₹299, permanently unlock all worlds and remove forced banner/interstitial ads.
- Use Play Billing product pricing, purchase acknowledgment, entitlement restoration and purchase verification; do not grant from untrusted JavaScript or hardcoded client flags.
- Premium users may opt into rewarded ads for coins, but no forced ads.
- Purchases are NOT implemented or tested yet. Do not expose live purchase buttons until billing is verified.

## Rewarded ad reward
+20 coins only on confirmed completion; no reward on skip/failure; no double grant for same event. Test ads only until consent and release checks pass.

## Player-friendly ad policy (approved)
- No interstitial/full-screen forced ads, including at launch, between rounds or mid-game.
- Small adaptive banner only on Home and/or Result screen if it does not obscure controls; hide during gameplay.
- Rewarded video only after explicit user tap; grant 20 coins only after verified reward callback.
- Rewarded ads can be full-screen and their duration cannot be guaranteed; clearly label as optional.
- Respect premium ₹299 ad-free entitlement: no banners or forced ads. Optional rewarded ads only by player choice.
- Use AdMob test units until privacy/consent, Play policies and device testing pass. Do not claim SDK integration alone means live ads are working.

## Release blockers / final verification
- Play Billing library, product catalog, server-side purchase verification, acknowledgment, restore and premium entitlement handling are NOT implemented. ₹199/₹299 purchase UI must remain hidden.
- Test AdMob IDs are used; production ad IDs and privacy/consent flow have NOT been configured. No production ad release until compliant.
- Release AAB artifact says `SIGNATURE-REQUIRES-VERIFICATION`; confirm release keystore and signing in Play Console before upload.
- Real-device checks required: map badges, saved coins after relaunch, all world unlocks, no duplicate deduction, game pause/resume, no forced ads, rewarded completed/skip/unavailable and reward persistence.
- No live banner is required for the first release; do not introduce one merely to meet a monetization plan.

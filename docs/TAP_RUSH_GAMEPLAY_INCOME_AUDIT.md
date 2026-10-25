# Tap Rush — Gameplay & Income Audit
Date: 2026-10-25
Status: static inspection only; NOT gameplay QA or revenue verification.

## Confirmed from current bundled JavaScript
- World metadata includes Jungle Adventure and City Adventure.
- Treasure tapping and hazard avoidance are described in world guidance.
- LocalStorage references for tapRushBest and srCoins exist.
- Web Audio, pointer/touch input and vibration APIs appear in the bundle.
- A world-map navigation control exists.
- No exact 'daily', 'reward', 'revive', 'admob', 'shop' or 'challenge' token was found in the bundle; this is an indicator, not proof no equivalent feature exists under another name.

## First small monetization candidate
- Preserve the current tap/dodge/scoring game and existing coins.
- After verified end-of-round/results flow, consider a **frequency-capped interstitial** at a natural break; never interrupt active gameplay or launch.
- Test with test ad IDs only and follow Play policies and audience/child-directed restrictions.
- Optional rewarded ad for a *specific in-game benefit* is second-phase ONLY if gameplay supports a meaningful benefit and explicit opt-in, reward verification, and no forced viewing.
- No premium shop, payment flow, or new world before core QA and retention testing.
- Google Play digital purchases generally require Play Billing, with jurisdictional program exceptions.

## Verification still required
1. Read and map actual state transitions for start, game over, result, replay, world unlock and coins.
2. Verify that Jungle/City are playable, not just displayed as metadata.
3. Confirm Android debug build and offline local assets on device.
4. Choose ad format and frequency after measuring actual round length.
5. Review target audience, privacy/data safety, SDK and store policies before enabling production ads.

## Guardrails
No ads implemented; no revenue claimed; no public website changes; no new gameplay fabricated.

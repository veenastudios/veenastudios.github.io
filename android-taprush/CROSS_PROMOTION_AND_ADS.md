# SR GAMERS cross-promotion and monetization contract

Status: architecture specification only; **not yet integrated into gameplay**.

## Game hub
- A visible "More SR Games" entry on home or results screen.
- Show Tap Rush, Jungle Friends Quiz, and future games.
- Each item has a title, optional icon, and a destination that can be updated from an approved configuration.
- Unreleased games must display "Coming soon" and must not have dead install links.
- For published games, open their verified Google Play listing externally.
- Keep an offline fallback hub with locally bundled metadata so website outages do not break gameplay.
- Veena Studios hub: https://veenastudios.in/ for books, short stories and other products.

## Advertising placements
- Rewarded ad: optional bonus after a completed round, only after a tap; reward only after SDK confirms completion.
- Interstitial: only at natural transitions and frequency-capped, never during a timed round.
- Banner: only on a non-gameplay surface, without blocking controls.
- No forced ads before core gameplay is tested.
- All placements are **disabled** until a supported SDK, test ad IDs, privacy policy, consent, age-rating and Play Data Safety disclosures are completed.
- App should remain playable when offline or when ad loading fails.

## Revenue strategy
- Track gross ad revenue, provider adjustments, and actual net receipts separately.
- The business goal is to reinvest available net app revenue in marketing for 6–8 months.
- Revenue cannot be assumed before ads are approved and serving.

## Release acceptance criteria
- All five worlds playable in airplane mode.
- Cross-promotion hub displays without connectivity and has no dead buttons.
- External links open outside the WebView.
- Ads do not cover gameplay, do not block offline play, and reward only after verified completion.
- Real-device testing, signed AAB and store compliance review before release.

# Tap Rush — Stage 1 game acceptance (Play Store/monetization deferred)
Per SR_GAMERS_GAME_RELEASE_RULES.md. Never treat CI success as phone-test success.

## Previously verified on phone (historical builds)
- [x] Debug APK installs and launches
- [x] Jungle gameplay, score and result
- [x] City gameplay and permanent 150-coin unlock
- [x] Coin earning and persistence after restart
- [x] Debug rewarded test ad can award +20 coins

## Verified CI milestone — 13 November 2026
- Build #309 (run 43440815985): **SUCCESS**; debug APK artifact `taprush-offline-debug-apk` (artifact ID 14044389499, 12,456,783 bytes).
- This CI pass includes duplicate world-unlock prompt guard, dialog focus restoration, Android Back cancellation and premium modal visibility regression checks.
- Additional static checks for world price constants, coin affordability, offline WebView routing and storage security were committed afterward; **not yet CI-verified**.
- Build success does not establish actual device behavior.

## CI/code verified, latest phone confirmation required
- [ ] Adventure Pass opens and stays open; ₹199 and ₹299 packs remain preview-only
- [ ] Premium button visible on Home and World Map; absent in gameplay/results
- [ ] Android Back closes Adventure Pass rather than exiting
- [ ] World Map price badges do not cover labels on actual phone
- [ ] Home layout has no obstructive blank/overlap areas on phone

## Remaining phone-only acceptance
- [ ] Space gameplay and scoring
- [ ] Underwater gameplay and scoring
- [ ] Himalaya gameplay and scoring
- [ ] All worlds: coins deducted once; unlock persists through restart
- [ ] No negative coins, duplicate unlock charge or stuck level
- [ ] Rewarded ad completion/skip/failure and exactly-once grant
- [ ] Pause/resume, background/resume and Android Back in gameplay
- [ ] Offline game start and play after airplane-mode restart
- [ ] Portrait phone layouts at narrow and tall aspect ratios
- [ ] Final candidate full smoke test with no critical blocker

## Stage 2 — explicitly excluded
Play Console login/registration, developer fee, live payments, production ads, signing and publishing.

## Release gate
A Stage 1 completion claim requires all applicable boxes above verified with actual test evidence. Do not convert unchecked phone tests to PASS from code inspection.

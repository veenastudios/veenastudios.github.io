# Tap Rush — Luxury Home trial visual QA

This is a trial-only checklist. Never merge into the approved stable build before on-device acceptance.

## Automated gates
- GitHub Actions: collage JavaScript syntax, collage isolation, offline assets, gameplay/premium regressions, Android debug APK, release safety.
- Banner files `sr_gamers_banner.webp` and `sr_kids_banner.webp` must be present in `android-taprush/` and byte-for-byte copied to APK assets before visual sign-off.
- If files are missing, readable banner text is intentionally shown; this is NOT final visual approval.

## On-device acceptance (portrait and short screen)
1. Top SR GAMERS image banner visible, tappable and opens intended Games destination.
2. Original tiger Home artwork and PLAY/Settings/coins/carousel remain unchanged and tappable.
3. Bottom SR KIDS image banner visible, tappable and opens intended Kids destination.
4. Golden PREMIUM left and purple SHARE GAME right are both fully visible, equally sized, and independently tappable.
5. Share opens Android chooser or copies the correct URL. No +100 coins for share without verified installation.
6. Premium opens store safely; no unverified purchase is granted.
7. World Map, pause/resume, Back, exit confirmation, locked worlds, and game rounds work without collage overlays.
8. Test 360px-wide and taller/shorter screens; rotate device if supported. Verify no clipping or overlap.

## Current status
Automated checks alone do not prove actual device visual or tap behavior. Require screenshots or phone test before final approval.

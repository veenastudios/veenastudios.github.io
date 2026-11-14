# Luxury home underlay — isolated trial

Branch: `experiment/taprush-luxury-home-underlay`. Do not merge into `taprush-android-offline-v6` until explicitly approved after device testing.

## Composition
- Keep approved original home artwork as the foreground at its existing aspect ratio and retain every existing hitbox and coin display.
- Use the new luxury design only as an underlay behind the foreground. The center must be fully occluded; only top and bottom extensions may be visible.
- Do not stretch the foreground image or duplicate the tiger, PLAY, carousel, or Premium.
- Avoid placing critical copy under status/navigation bars. Respect Android insets and tall/short phone dimensions.
- New SR KIDS card must have its own bounded click target and must not intercept existing controls. Link only to a verified destination.
- Premium must remain one working action, not two overlaid targets.

## Acceptance gates
1. Asset added to this trial branch and the build compiles.
2. No visible seams, duplicate elements, clipping, or unwanted overlays at target device dimensions.
3. All foreground hitboxes (PLAY, carousel, Settings, coins, Premium) still work.
4. Game world selection, gameplay, Pause, Home, results, and rewards are unaffected.
5. Compare screenshots against approved Build #358 and obtain explicit approval before any merge.

**Status:** trial branch and acceptance criteria prepared. New generated art has not yet been committed as a binary asset; no trial APK is claimed ready.

## Approved three-panel collage direction (14 Nov)
- TOP: separate luxury 3D SR GAMERS landscape banner; tap opens verified Veena Studios Games section (not an invented URL).
- MIDDLE: preserve approved Tap Rush Home artwork and every current interactive hotspot; no flattened replacement of working controls.
- BOTTOM: separate luxury 3D SR KIDS landscape banner; tap opens verified SR KIDS website section.
- Thin golden dividers are intentional; avoid overlap. Layout must respect safe areas and available viewport, not simply stretch all three images.
- Keep current Premium entry, coins and Settings working; do not add duplicate touch targets.
- Validate web destinations, Android external-link behavior and Back navigation; avoid redirecting players unexpectedly.
- Existing CSS-only underlay experiment is superseded as the preferred visual design, but do not delete or merge it before an actual collage trial passes.
- Do not claim the image-generation preview is a deployable UI asset: source assets, crop boundaries and tap regions must be prepared and committed independently.
- Explicit user acceptance required after on-device trial before merging into the stable branch.

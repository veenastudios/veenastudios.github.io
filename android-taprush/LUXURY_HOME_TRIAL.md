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

#!/usr/bin/env python3
"""Static regression checks for premium integration; run after prepare_offline.py."""
from pathlib import Path
root = Path(__file__).resolve().parent
html = (root / "app/src/main/assets/index.html").read_text(encoding="utf-8")
activity = (root / "app/src/main/java/in/veenastudios/taprush/MainActivity.java").read_text()
billing = (root / "app/src/main/java/in/veenastudios/taprush/TapRushBilling.java").read_text()
gradle = (root / "app/build.gradle").read_text()
checks = {
    "world unlock dialog has exactly-once settle": "if(settled)return;settled=true" in html,
    "world unlock confirms through game logic": "await window.srConfirmUnlock(L.name,cost)" in (root / "app/src/main/assets/assets/index-B_be548G.js").read_text(encoding="utf-8"),
    "reward grant native exactly once": "rewardGranted.compareAndSet(false,true)" in activity,
    "debug-only rewarded bridge": "if (BuildConfig.DEBUG)" in activity and "new GameBridge()" in activity,
    "five world prices": "worldPrices=[0,150,200,250,350]" in html,
    "world unlock persistence lookup": "srWorldUnlocked_" in html and "localStorage.getItem(k)==='yes'" in html,
    "coin affordability guard": "if(coins>=price)return" in html and "e.stopImmediatePropagation()" in html,
    "offline host resource restriction": 'Offline resource blocked' in activity and 'name.contains("..")' in activity,
    "WebView storage and JavaScript": "s.setDomStorageEnabled(true)" in activity and "s.setJavaScriptEnabled(true)" in activity,
    "WebView mixed-content restricted": "MIXED_CONTENT_NEVER_ALLOW" in activity,
    "world unlock repeated taps guarded": "if(document.querySelector('.srWorldUnlockDialog')){resolve(false);return;}" in html,
    "world unlock restores focus": "previousFocus.focus()" in html,
    "world unlock backdrop cancels": "if(event.target===overlay)finish(false)" in html,
    "world unlock dialog tracked": "overlay.className='srWorldUnlockDialog'" in html and "overlay.srCancelUnlock=()=>finish(false)" in html,
    "world unlock Android back cancels": "document.querySelector('.srWorldUnlockDialog')" in activity and "u.srCancelUnlock()" in activity,
    "premium aligned with home artwork": "const below=rect.bottom+12" in html and "storeButton.style.top=" in html,
    "premium launcher hidden for unlock dialog": "document.querySelector('.srStoreOverlay,.srWorldUnlockDialog,.srWorldLockNotice" in html,
    "premium overlay mutations observed": "new MutationObserver(syncPremiumVisibility).observe(document.body" in html,
    "premium store overlay": "srStoreOverlay" in html,
    "Android back dismisses premium dialog": "document.querySelector(\'.srStoreOverlay\')" in activity and "evaluateJavascript" in activity,
    "premium dialog keyboard dismissal": "storeButton.focus()" in html and "e.key===\'Escape\'" in html,
    "premium dialog persists while launcher hidden": "if(active||!allowed)document.querySelector(\'.srStoreOverlay\')?.remove()" in html and "if(storeButton.hidden)document.querySelector" not in html,
    "premium hidden during gameplay": "function syncPremiumVisibility()" in html and "storeButton.hidden=active||!allowed||dialogOpen" in html,
    "world price badges positioned away from titles": "right:3%;top:9%;width:24%" in html,
    "all-worlds button": "buyAllWorlds" in html and "buyAllWorlds()" in activity,
    "premium button": "buyPremium" in html and "buyPremium()" in activity,
    "restore button": "Restore purchases" in html and "restore()" in activity,
    "checkout disabled without verification": "BILLING_VERIFICATION_ENABLED', 'false'" in gradle and
        "if (!BuildConfig.BILLING_VERIFICATION_ENABLED)" in billing,
    "billing connection and restore": "billing.connect()" in activity and
        "billing.restorePurchases()" in activity,
    "no client-side entitlement grant": "Deliberately no local unlock" in billing,
    "no production rewarded ads": "if (BuildConfig.DEBUG)" in activity,
    "pause when backgrounded": "visibilitychange" in html and "pause.click()" in html,
}
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if not all(checks.values()):
    raise SystemExit(1)
print("Static regression checks PASS. Android compilation and on-device testing still required.")

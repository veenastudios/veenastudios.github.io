#!/usr/bin/env python3
"""Static regression checks for premium integration; run after prepare_offline.py."""
from pathlib import Path
root = Path(__file__).resolve().parent
html = (root / "app/src/main/assets/index.html").read_text(encoding="utf-8")
activity = (root / "app/src/main/java/in/veenastudios/taprush/MainActivity.java").read_text()
billing = (root / "app/src/main/java/in/veenastudios/taprush/TapRushBilling.java").read_text()
gradle = (root / "app/build.gradle").read_text()
checks = {
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

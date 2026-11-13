# Removes the old default Capacitor splash image. The system splash becomes plain emerald green,
# then the animated icon inside the app (index.html) plays.
import os, re, glob
res = "android/app/src/main/res"
for p in glob.glob(res + "/drawable*/splash.*"):
    os.remove(p); print("removed", p)
os.makedirs(res + "/drawable", exist_ok=True)
open(res + "/drawable/splash.xml", "w").write(
 '<?xml version="1.0" encoding="utf-8"?>\n<shape xmlns:android="http://schemas.android.com/apk/res/android"><solid android:color="#0F5132"/></shape>\n')
open(res + "/drawable/splash_empty.xml", "w").write(
 '<?xml version="1.0" encoding="utf-8"?>\n<layer-list xmlns:android="http://schemas.android.com/apk/res/android"><item android:width="1dp" android:height="1dp"><shape android:shape="rectangle"><solid android:color="#00000000"/></shape></item></layer-list>\n')
sp = res + "/values/styles.xml"
s = open(sp, encoding="utf-8").read()
m = re.search(r'(<style name="AppTheme\.NoActionBarLaunch"[^>]*parent="([^"]*)"[^>]*>)(.*?)(</style>)', s, re.S)
if m and m.group(2) == "Theme.SplashScreen":
    body = re.sub(r'\s*<item name="(windowSplashScreenBackground|windowSplashScreenAnimatedIcon)">[^<]*</item>', "", m.group(3))
    body += '\n        <item name="windowSplashScreenBackground">#0F5132</item>\n        <item name="windowSplashScreenAnimatedIcon">@drawable/splash_empty</item>\n    '
    s = s[:m.start()] + m.group(1) + body + m.group(4) + s[m.end():]
    open(sp, "w", encoding="utf-8").write(s)
    print("styles patched")
else:
    print("styles not patched (parent:", m.group(2) if m else None, ")")

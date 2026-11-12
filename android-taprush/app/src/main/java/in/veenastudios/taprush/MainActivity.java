package in.veenastudios.taprush;
import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.net.Uri;
import android.webkit.*;
import java.io.*;
import java.util.Locale;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.rewarded.RewardedAd;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.FullScreenContentCallback;
import com.google.android.gms.ads.AdError;
import android.webkit.JavascriptInterface;
public class MainActivity extends Activity {
 private WebView web;
 private TapRushBilling billing;
 private static final String HOST="appassets.androidplatform.net";
 private RewardedAd rewardedAd;
 private boolean adShowing=false;
 private boolean adLoading=false;
 private void sendEvent(String event){if(web!=null)web.evaluateJavascript("window.dispatchEvent(new Event("+org.json.JSONObject.quote(event)+"))",null);}
 private void loadRewarded(){if(!BuildConfig.DEBUG||adLoading||adShowing||isFinishing()||isDestroyed())return;adLoading=true;RewardedAd.load(this,BuildConfig.DEBUG?"ca-app-pub-3940256099942544/5224354917":BuildConfig.REWARDED_AD_UNIT_ID,new AdRequest.Builder().build(),new RewardedAdLoadCallback(){@Override public void onAdLoaded(RewardedAd ad){adLoading=false;rewardedAd=ad;sendEvent("srAdReady");}@Override public void onAdFailedToLoad(LoadAdError error){adLoading=false;rewardedAd=null;/* Preload failures are silent; only a user-requested ad reports unavailability. */}});}
 private final class BillingBridge {
  @JavascriptInterface public void buyAllWorlds(){runOnUiThread(()->{if(billing!=null)billing.launchPurchase(TapRushBilling.ALL_WORLDS);});}
  @JavascriptInterface public void buyPremium(){runOnUiThread(()->{if(billing!=null)billing.launchPurchase(TapRushBilling.PREMIUM);});}
  @JavascriptInterface public void restore(){runOnUiThread(()->{if(billing!=null)billing.restorePurchases();});}
  @JavascriptInterface public boolean isCheckoutEnabled(){return BuildConfig.BILLING_VERIFICATION_ENABLED;}
 }
 private final class GameBridge { @JavascriptInterface public void showRewarded(){runOnUiThread(()->{if(adShowing)return;if(rewardedAd==null){sendEvent("srAdUnavailable");loadRewarded();return;}RewardedAd ad=rewardedAd;rewardedAd=null;adShowing=true;final java.util.concurrent.atomic.AtomicBoolean rewardGranted=new java.util.concurrent.atomic.AtomicBoolean(false);ad.setFullScreenContentCallback(new FullScreenContentCallback(){@Override public void onAdDismissedFullScreenContent(){adShowing=false;loadRewarded();}@Override public void onAdFailedToShowFullScreenContent(AdError error){adShowing=false;sendEvent("srAdUnavailable");loadRewarded();}});ad.show(MainActivity.this,rewardItem->{if(rewardGranted.compareAndSet(false,true))sendEvent("srReward20");});});} }
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG);
  web=new WebView(this); setContentView(web);
  web.addJavascriptInterface(new BillingBridge(),"TapRushBilling");
  billing=new TapRushBilling(this);
  billing.connect();
  // Rewarded ads remain test-only until consent, privacy and production IDs are approved.
  if (BuildConfig.DEBUG) {
   web.addJavascriptInterface(new GameBridge(),"TapRushAds");
   MobileAds.initialize(this,status->loadRewarded());
  }
  WebSettings s=web.getSettings();
  s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);
  s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setAllowFileAccessFromFileURLs(false);s.setAllowUniversalAccessFromFileURLs(false);s.setJavaScriptCanOpenWindowsAutomatically(false);s.setSupportMultipleWindows(false);android.webkit.CookieManager.getInstance().setAcceptThirdPartyCookies(web,false);
  s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
  web.setWebChromeClient(new WebChromeClient());
  web.setWebViewClient(new WebViewClient(){
   @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest req){
    Uri u=req.getUrl();
    if("https".equals(u.getScheme())&&HOST.equals(u.getHost()))return false;
    if(req.isForMainFrame()&&"https".equals(u.getScheme()))try{startActivity(new Intent(Intent.ACTION_VIEW,u));}catch(Exception ignored){}
    return true;
   }
   @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest req){
    Uri u=req.getUrl();if(!"https".equals(u.getScheme())||!HOST.equals(u.getHost()))return new WebResourceResponse("text/plain","UTF-8",403,"Offline resource blocked",null,new ByteArrayInputStream(new byte[0]));
    String path=u.getPath();
    if(path==null||!path.startsWith("/tap-rush/"))return error();
    String name=path.substring("/tap-rush/".length());
    if(name.isEmpty())name="index.html";
    if(name.contains("..")||name.startsWith("/")||name.contains("\\")||name.indexOf(0)>=0)return error();
    String p=name.toLowerCase(Locale.ROOT);
    String mime=p.endsWith(".js")?"application/javascript":p.endsWith(".css")?"text/css":p.endsWith(".html")?"text/html":p.endsWith(".webp")?"image/webp":p.endsWith(".png")?"image/png":p.endsWith(".svg")?"image/svg+xml":p.endsWith(".json")||p.endsWith(".webmanifest")?"application/json":p.endsWith(".mp3")?"audio/mpeg":p.endsWith(".ogg")?"audio/ogg":p.endsWith(".wav")?"audio/wav":"application/octet-stream";
    try{return new WebResourceResponse(mime,"UTF-8",getAssets().open(name));}catch(IOException e){return error();}
   }
   private WebResourceResponse error(){return new WebResourceResponse("text/plain","UTF-8",404,"Not Found",null,new ByteArrayInputStream(new byte[0]));}
  });
  web.loadUrl("https://"+HOST+"/tap-rush/");
 }
 @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();}
 @Override protected void onPause(){if(web!=null)web.onPause();super.onPause();}
 @Override protected void onResume(){super.onResume();if(web!=null)web.onResume();if(billing!=null)billing.restorePurchases();}
 @Override protected void onDestroy(){if(billing!=null){billing.close();billing=null;}if(web!=null){web.stopLoading();web.destroy();web=null;}super.onDestroy();}
}
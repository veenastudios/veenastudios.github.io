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
 private static final String HOST="appassets.androidplatform.net";
 private RewardedAd rewardedAd;
 private boolean adShowing=false;
 private void sendEvent(String event){if(web!=null)web.evaluateJavascript("window.dispatchEvent(new Event("+org.json.JSONObject.quote(event)+"))",null);}
 private void loadRewarded(){RewardedAd.load(this,"ca-app-pub-3940256099942544/5224354917",new AdRequest.Builder().build(),new RewardedAdLoadCallback(){@Override public void onAdLoaded(RewardedAd ad){rewardedAd=ad;sendEvent("srAdReady");}@Override public void onAdFailedToLoad(LoadAdError error){rewardedAd=null;sendEvent("srAdUnavailable");}});}
 private final class GameBridge { @JavascriptInterface public void showRewarded(){runOnUiThread(()->{if(adShowing)return;if(rewardedAd==null){sendEvent("srAdUnavailable");loadRewarded();return;}RewardedAd ad=rewardedAd;rewardedAd=null;adShowing=true;ad.setFullScreenContentCallback(new FullScreenContentCallback(){@Override public void onAdDismissedFullScreenContent(){adShowing=false;loadRewarded();}@Override public void onAdFailedToShowFullScreenContent(AdError error){adShowing=false;sendEvent("srAdUnavailable");loadRewarded();}});ad.show(MainActivity.this,rewardItem->sendEvent("srReward20"));});} }
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  web=new WebView(this); setContentView(web);
  web.addJavascriptInterface(new GameBridge(),"TapRushAds");
  MobileAds.initialize(this,status->loadRewarded());
  WebSettings s=web.getSettings();
  s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);
  s.setAllowFileAccess(false);s.setAllowContentAccess(false);
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
    Uri u=req.getUrl();if(!"https".equals(u.getScheme())||!HOST.equals(u.getHost()))return null;
    String path=u.getPath();
    if(path==null||!path.startsWith("/tap-rush/"))return error();
    String name=path.substring("/tap-rush/".length());
    if(name.isEmpty())name="index.html";
    if(name.contains("..")||name.startsWith("/"))return error();
    String p=name.toLowerCase(Locale.ROOT);
    String mime=p.endsWith(".js")?"application/javascript":p.endsWith(".css")?"text/css":p.endsWith(".html")?"text/html":p.endsWith(".webp")?"image/webp":p.endsWith(".png")?"image/png":p.endsWith(".svg")?"image/svg+xml":p.endsWith(".json")||p.endsWith(".webmanifest")?"application/json":p.endsWith(".mp3")?"audio/mpeg":p.endsWith(".ogg")?"audio/ogg":p.endsWith(".wav")?"audio/wav":"application/octet-stream";
    try{return new WebResourceResponse(mime,"UTF-8",getAssets().open(name));}catch(IOException e){return error();}
   }
   private WebResourceResponse error(){return new WebResourceResponse("text/plain","UTF-8",404,"Not Found",null,new ByteArrayInputStream(new byte[0]));}
  });
  web.loadUrl("https://"+HOST+"/tap-rush/");
 }
 @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){web.destroy();super.onDestroy();}
}
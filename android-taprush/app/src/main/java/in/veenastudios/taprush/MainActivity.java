package in.veenastudios.taprush;
import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.content.Intent;
import android.net.Uri;
import android.webkit.*;
import java.io.*;
import java.util.Locale;
public class MainActivity extends Activity {
 private WebView web;
 private static final String HOST="appassets.androidplatform.net";
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  web=new WebView(this); setContentView(web);
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
 @Override public boolean onCreateOptionsMenu(Menu menu){menu.add(0,101,0,"More SR Games").setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);return true;}
 @Override public boolean onOptionsItemSelected(MenuItem item){if(item.getItemId()==101){web.loadUrl("https://"+HOST+"/tap-rush/game-hub.html");return true;}return super.onOptionsItemSelected(item);}
 @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
 @Override protected void onDestroy(){web.destroy();super.onDestroy();}
}
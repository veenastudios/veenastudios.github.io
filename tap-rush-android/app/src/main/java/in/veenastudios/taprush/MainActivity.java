package in.veenastudios.taprush;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
public class MainActivity extends Activity {
 private WebView view;
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  view = new WebView(this);
  view.setWebViewClient(new WebViewClient());
  WebSettings settings=view.getSettings();
  settings.setJavaScriptEnabled(true);
  settings.setDomStorageEnabled(true);
  view.loadUrl("https://veenastudios.in/tap-rush/");
  setContentView(view);
 }
 @Override public void onBackPressed() { if(view!=null && view.canGoBack()) view.goBack(); else super.onBackPressed(); }
 @Override protected void onDestroy() { if(view!=null) view.destroy(); super.onDestroy(); }
}

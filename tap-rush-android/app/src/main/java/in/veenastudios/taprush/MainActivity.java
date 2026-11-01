package in.veenastudios.taprush;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Button;
import android.view.Gravity;
import android.view.View;

public class MainActivity extends Activity {
 private static final String GAME_URL = "https://veenastudios.in/tap-rush/";
 private WebView view;
 private LinearLayout errorPanel;
 private FrameLayout root;

 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  root = new FrameLayout(this);
  view = new WebView(this);
  WebSettings settings = view.getSettings();
  settings.setJavaScriptEnabled(true);
  settings.setDomStorageEnabled(true);
  settings.setAllowFileAccess(false);
  settings.setAllowContentAccess(false);
  settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
  view.setWebViewClient(new WebViewClient() {
   @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest request) {
    String url = request.getUrl().toString();
    return !(url.equals(GAME_URL) || url.startsWith(GAME_URL));
   }
   @Override public void onReceivedError(WebView v, WebResourceRequest request, WebResourceError error) {
    if (request.isForMainFrame()) showError();
   }
   @Override public void onPageFinished(WebView v, String url) {
    if (url.startsWith(GAME_URL) && v.getProgress() == 100) {
     // A successful page load hides the network error panel.
     errorPanel.setVisibility(View.GONE);
    }
   }
  });
  root.addView(view, new FrameLayout.LayoutParams(-1, -1));
  errorPanel = new LinearLayout(this);
  errorPanel.setOrientation(LinearLayout.VERTICAL);
  errorPanel.setGravity(Gravity.CENTER);
  errorPanel.setPadding(32, 32, 32, 32);
  errorPanel.setBackgroundColor(0xff102d20);
  TextView message = new TextView(this);
  message.setText("Tap Rush needs an internet connection. Check your connection and try again.");
  message.setTextColor(0xffffffff);
  message.setTextSize(18);
  message.setGravity(Gravity.CENTER);
  Button retry = new Button(this);
  retry.setText("Retry");
  retry.setOnClickListener(v -> { errorPanel.setVisibility(View.GONE); view.loadUrl(GAME_URL); });
  errorPanel.addView(message);
  errorPanel.addView(retry);
  root.addView(errorPanel, new FrameLayout.LayoutParams(-1, -1));
  errorPanel.setVisibility(View.GONE);
  setContentView(root);
  view.loadUrl(GAME_URL);
 }
 private void showError() { runOnUiThread(() -> errorPanel.setVisibility(View.VISIBLE)); }
 @Override public void onBackPressed() {
  if (errorPanel != null && errorPanel.getVisibility() == View.VISIBLE) { view.loadUrl(GAME_URL); errorPanel.setVisibility(View.GONE); }
  else if (view != null && view.canGoBack()) view.goBack();
  else super.onBackPressed();
 }
 @Override protected void onDestroy() { if (view != null) view.destroy(); super.onDestroy(); }
}

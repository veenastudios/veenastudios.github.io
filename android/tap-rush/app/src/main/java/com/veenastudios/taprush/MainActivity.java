package com.veenastudios.taprush;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewClientCompat;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;

public final class MainActivity extends Activity {
  private WebView web;
  @Override public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    web = new WebView(this);
    setContentView(web);
    WebSettings settings = web.getSettings();
    settings.setJavaScriptEnabled(true);
    settings.setDomStorageEnabled(true);
    settings.setAllowFileAccess(false);
    settings.setAllowContentAccess(false);
    settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
    WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
      .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
      .build();
    web.setWebViewClient(new WebViewClientCompat() {
      @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        Uri uri = request.getUrl();
        if ("appassets.androidplatform.net".equals(uri.getHost()) && "https".equals(uri.getScheme())
            && uri.getPath() != null && uri.getPath().startsWith("/assets/tap-rush/")) return false;
        if (request.isForMainFrame() && ("https".equals(uri.getScheme()) || "http".equals(uri.getScheme()))) {
          try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (android.content.ActivityNotFoundException ignored) { }
        }
        return true;
      }
      @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
        return loader.shouldInterceptRequest(request.getUrl());
      }
    });
    web.setWebChromeClient(new WebChromeClient());
    web.loadUrl("https://appassets.androidplatform.net/assets/tap-rush/index.html");
  }
  @Override public void onBackPressed() {
    if (web != null && web.canGoBack()) web.goBack(); else super.onBackPressed();
  }
  @Override protected void onDestroy() {
    if (web != null) { web.destroy(); web = null; }
    super.onDestroy();
  }
}

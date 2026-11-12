package in.veenastudios.taprush;

import android.app.Activity;
import android.util.Log;
import com.android.billingclient.api.*;
import java.util.Arrays;
import java.util.List;

/**
 * Google Play one-time product transport only.
 * SECURITY: Do not grant coins/worlds from client-side purchase callbacks.
 * A trusted purchase-token verification service is required before entitlements.
 */
public final class TapRushBilling {
    public static final String ALL_WORLDS = "taprush_all_worlds_199";
    public static final String PREMIUM = "taprush_premium_299";
    private static final String TAG = "TapRushBilling";
    private final Activity activity;
    private final BillingClient client;
    private boolean connected;
    private boolean connecting;
    private boolean restoreRequested;

    public TapRushBilling(Activity activity) {
        this.activity = activity;
        client = BillingClient.newBuilder(activity)
            .setListener((result, purchases) -> {
                if (result.getResponseCode() != BillingClient.BillingResponseCode.OK || purchases == null) {
                    Log.w(TAG, "Purchase update code=" + result.getResponseCode());
                    return;
                }
                for (Purchase purchase : purchases) {
                    // Deliberately no local unlock. A backend must verify purchaseToken
                    // against Google Play Developer API before acknowledging/granting.
                    Log.i(TAG, "Purchase received; awaiting trusted verification");
                }
            })
            .enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())
            .build();
    }

    public void connect() {
        if (connected || connecting) return;
        connecting = true;
        client.startConnection(new BillingClientStateListener() {
            @Override public void onBillingSetupFinished(BillingResult result) {
                connecting = false;
                connected = result.getResponseCode() == BillingClient.BillingResponseCode.OK;
                if (connected) {
                    queryProducts();
                    if (restoreRequested) restorePurchases();
                }
            }
            @Override public void onBillingServiceDisconnected() { connected = false; connecting = false; }
        });
    }

    public void queryProducts() {
        if (!connected) return;
        List<QueryProductDetailsParams.Product> products = Arrays.asList(
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId(ALL_WORLDS).setProductType(BillingClient.ProductType.INAPP).build(),
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId(PREMIUM).setProductType(BillingClient.ProductType.INAPP).build());
        client.queryProductDetailsAsync(
            QueryProductDetailsParams.newBuilder().setProductList(products).build(),
            (result, details) -> {
                // Price and offer details must be taken from Google Play, never hardcoded.
                if (result.getResponseCode() != BillingClient.BillingResponseCode.OK)
                    Log.w(TAG, "Product query failed: " + result.getResponseCode());
            });
    }

    public void restorePurchases() {
        restoreRequested = true;
        if (!connected) { connect(); return; }
        restoreRequested = false;
        client.queryPurchasesAsync(
            QueryPurchasesParams.newBuilder().setProductType(BillingClient.ProductType.INAPP).build(),
            (result, purchases) -> {
                if (result.getResponseCode() == BillingClient.BillingResponseCode.OK) {
                    // Send tokens to a trusted backend when configured; never trust local flags.
                    Log.i(TAG, "Restore queried; backend verification required");
                }
            });
    }

    public void close() { client.endConnection(); }
}

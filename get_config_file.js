/**
 * X Token Extractor - Console Script
 *
 * Instructions:
 * 1. Go to x.com and make sure you're logged in
 * 2. Open Developer Tools (F12)
 * 3. Go to Network tab and refresh the page
 * 4. Look for any request and check its Authorization header
 * 5. Go to Console tab
 * 6. Copy and paste this entire script
 * 7. Press Enter
 * 8. Your config.json will be downloaded automatically
 *
 * Repository: https://github.com/rei-iku/x-interest-cleaner
 */

(function () {
  "use strict";

  console.log("🔑 X Token Extractor v1.0");
  console.log("================================");

  try {
    // Extract tokens
    const tokens = {};
    let foundTokens = 0;

    // Get ct0 and auth_token cookies
    const cookies = document.cookie.split(";");
    cookies.forEach((cookie) => {
      const [name, value] = cookie.trim().split("=");
      if (name === "ct0") {
        tokens.ct0 = value;
        tokens.csrf_token = value; // Same value for both
        foundTokens += 2;
        console.log("✅ Found ct0/csrf_token:", value.substring(0, 20) + "...");
      } else if (name === "auth_token") {
        tokens.auth_token = value;
        foundTokens++;
        console.log("✅ Found auth_token:", value.substring(0, 20) + "...");
      }
    });

    // Use X's default web app bearer token
    // This is the standard token used by X's web interface
    tokens.bearer_token = "AAAAAAAAAAAAAAAAAAAAAMLheAAAAAAA0%2BuSeid%2BULvsea4JtiGRiSDyJug%3D";
    foundTokens++;
    console.log("✅ Found bearer_token");

    // Validate we have all essential tokens
    if (!tokens.ct0) {
      console.error("❌ Could not find ct0 cookie!");
      console.error("💡 Make sure you are logged in to X");
      console.error("💡 Try refreshing the page and running this script again");
      return;
    }
    
    if (!tokens.auth_token) {
      console.error("❌ Could not find auth_token cookie!");
      console.error("💡 Make sure you are logged in to X");
      console.error("💡 Try refreshing the page and running this script again");
      return;
    }

    console.log(`\n🎉 Successfully extracted ${foundTokens} tokens:`);
    console.log("- bearer_token: ✅");
    console.log("- csrf_token: ✅");
    console.log("- ct0: ✅");
    console.log("- auth_token: ✅");

    // Create config JSON
    const config = JSON.stringify(tokens, null, 2);
    console.log("\n📄 Generated config.json:");
    console.log(config);

    // Download config file
    const blob = new Blob([config], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "config.json";
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log("\n💾 config.json downloaded successfully!");
    console.log("\n🚀 Next steps:");
    console.log("1. Save the downloaded config.json in your project folder");
    console.log("2. Run: python x_interest_cleaner.py");
    console.log("3. Stop seeing trash in your timeline! 🎉");

    // Also copy to clipboard if possible
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard
        .writeText(config)
        .then(() => {
          console.log("\n📋 Config also copied to clipboard!");
        })
        .catch(() => {
          console.log("\n📋 Could not copy to clipboard, but download worked!");
        });
    }
  } catch (error) {
    console.error("❌ Error extracting tokens:", error);
    console.error("\n🔧 Troubleshooting:");
    console.error("1. Make sure you are on x.com");
    console.error("2. Make sure you are logged in");
    console.error("3. Try refreshing the page");
    console.error(
      "4. Check if you have any browser extensions blocking scripts"
    );
  }
})();

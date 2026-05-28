// Cloudflare Turnstile - Free CAPTCHA alternative for GitHub Pages
// Sign up at: https://dash.cloudflare.com/sign-up (free)
// Then get your site key from: https://dash.cloudflare.com/?to=/:account/turnstile

// Add this to your HTML form:
/*
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
<div class="cf-turnstile" data-sitekey="YOUR_SITE_KEY" data-callback="onTurnstileSuccess"></div>
<script>
function onTurnstileSuccess(token) {
    document.getElementById('submit-btn').disabled = false;
}
</script>
*/

// Free alternative: Honeypot field (invisible to humans)
// Add this to your form - bots will fill it, humans won't see it:
/*
<div style="position: absolute; left: -5000px;" aria-hidden="true">
    <input type="text" name="website" tabindex="-1" value="" autocomplete="off">
</div>
*/

// Even simpler: Add a checkbox that says "I'm not a robot"
// Most bots won't check it:
/*
<div style="margin: 15px 0;">
    <label>
        <input type="checkbox" name="human_check" required 
               style="margin-right: 8px;">
        I'm a human (not a bot)
    </label>
</div>
*/

// Current protection:
// - ConvertKit has built-in spam filtering
// - Double opt-in prevents fake emails
// - But no visual CAPTCHA currently

// RECOMMENDED: Add Cloudflare Turnstile (free, privacy-friendly)
// OR: Enable reCAPTCHA in ConvertKit settings (requires Google account)

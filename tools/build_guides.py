#!/usr/bin/env python3
"""Generator for the English /guides/ pages and the /guides/ hub.

Every guide is defined below with guide(...). Only slugs listed in NEW_SLUGS are
(re)written, so editing one guide doesn't touch the others' dates; the hub is always
rebuilt. Some guides were later given extra related links by hand-edits, so check
the diff when you regenerate an older one.

Run order after editing:
  python3 tools/build_guides.py .
  python3 tools/build_ar.py          # re-adds the hreflang links on English twins
  python3 tools/sync_partials.py
  python3 tools/build_llms_full.py

Usage: python3 tools/build_guides.py <repo root> [slug ...]   (slugs override NEW_SLUGS)
"""
import html, json, pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
SITE = "https://nuevoautomations.com"
DATE = "2026-11-28"
DATE_H = "28 November 2026"
WA = "https://wa.me/15557738409?text=Hi%2C%20I%20read%20your%20guide%20and%20have%20a%20question."

GUIDES = []

def guide(**kw):
    GUIDES.append(kw)

# ---------------------------------------------------------------- 1
guide(
    slug="whatsapp-business-api-pricing-uae",
    title="WhatsApp Business API Pricing in the UAE, 2026 | Nuevo",
    desc="How Meta charges for WhatsApp Business API messages in the UAE in 2026: per-message billing, the October 2026 service-message change and free ad windows.",
    h1="WhatsApp Business API pricing in the UAE, explained for 2026",
    card="Per-message billing, the 1 October 2026 change to service messages, and the free window after a click-to-WhatsApp ad.",
    lead="Meta charges per delivered message, by message type and by the customer's country. Here is how that works for a UAE business, what changed on 1 October 2026, and how to estimate your own bill.",
    answer="Since 1 July 2025, Meta bills the WhatsApp Business API per delivered message, not per conversation. The price depends on the message category (marketing, utility, authentication or service) and on the country code of the customer who receives it. The UAE is its own market on Meta's rate card. From 1 October 2026, each business number gets 1,000 free service messages a month and pays for service messages beyond that. Chats that start from a click-to-WhatsApp ad open a free entry point window in which Meta doesn't charge for messages.",
    body="""
<h2>How Meta bills WhatsApp messages now</h2>
<p>Meta moved the WhatsApp Business Platform to per-message pricing on 1 July 2025. You pay only for messages your business sends that are actually delivered. Messages your customers send you are never charged.</p>
<p>Every message falls into a category, and each category has its own price in each market:</p>
<div class="prose-table"><table>
<thead><tr><th>Category</th><th>What it's for</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Marketing template</td><td>Offers, launches, reminders that aim to sell</td><td>An abandoned-cart reminder, a restock alert</td></tr>
<tr><td>Utility template</td><td>Updates about something the customer already did</td><td>Order confirmed, out for delivery</td></tr>
<tr><td>Authentication template</td><td>One-time codes</td><td>Login or checkout code</td></tr>
<tr><td>Service message</td><td>Free-form replies while the 24-hour customer-service window is open</td><td>Answering "do you deliver to Al Ain?"</td></tr>
<tr><td>Meta Business Agent</td><td>Replies written by Meta's own AI agent</td><td>Billed by tokens, separately</td></tr>
</tbody></table></div>
<p>Meta decides the category when it approves a template, and it can reclassify a "utility" template that is really marketing. Writing a sales message as a utility template to save money rarely works.</p>

<h2>The rate depends on your customer's country, not yours</h2>
<p>Meta prices each message by the country code of the person receiving it. A UAE business messaging a +971 number pays the UAE rate, but the same business messaging a customer in Saudi Arabia or India pays that country's rate. The UAE is listed as a standalone market on Meta's rate card, and Meta's pricing documentation lists the dirham (AED) as a billing currency from April 2026.</p>
<p>Rates change several times a year, so we don't print them here. The current numbers are on <a href="https://developers.facebook.com/docs/whatsapp/pricing/" target="_blank" rel="noopener">Meta's WhatsApp pricing page</a>; pick "United Arab Emirates" and your billing currency.</p>

<h2>What changed on 1 October 2026</h2>
<ul>
<li><strong>Service messages are no longer unlimited and free.</strong> Each business phone number gets 1,000 free service messages a month. Unused messages don't roll over. After that, service messages are charged. Meta keeps them free beyond the tier only for eligible government and non-profit accounts.</li>
<li><strong>Utility templates sent inside an open customer-service window are charged again.</strong> They had been free inside the window since July 2025.</li>
<li><strong>No payment method, no messages past the tier.</strong> If your WhatsApp Business account has no payment method, Meta still delivers service messages within the 1,000 free ones and stops delivering them after that.</li>
</ul>
<p>For a busy store this matters: a sales chat that runs to fifteen replies now uses fifteen service messages. Most small brands stay inside or near the free tier; brands running ads at volume do not.</p>

<h2>The free entry point window after a click-to-WhatsApp ad</h2>
<p>When a customer taps a click-to-WhatsApp ad (or a Facebook Page's WhatsApp button) on their phone and you reply within 24 hours, Meta opens a <strong>free entry point window</strong>. While it's open, Meta does not charge for marketing, utility, authentication or service messages to that customer. Meta Business Agent replies are still charged.</p>
<p>Meta's developer documentation says the window can stay open for up to 7 days; its marketing pages still describe 72 hours. Plan on the shorter number. The window only opens for chats started on Android or iOS, not from desktop or WhatsApp Web.</p>
<p>This is one reason click-to-WhatsApp ads suit UAE brands: the whole first sales conversation, including a follow-up template a day later, can cost nothing in message fees. Read our <a href="/guides/click-to-whatsapp-ads/">guide to click-to-WhatsApp ads</a> for the rest.</p>

<h2>Other costs besides Meta's message fees</h2>
<ol>
<li><strong>A platform or provider.</strong> The API has no inbox of its own. You use a Business Solution Provider or a platform built on Meta's Cloud API, and most charge a monthly fee, sometimes a markup per message.</li>
<li><strong>AI replies.</strong> If an AI assistant answers, someone pays for the model, either inside the platform fee or as Meta Business Agent tokens (Meta's own estimate is roughly 4–5 US cents a message at typical lengths).</li>
<li><strong>Setup.</strong> Connecting your number, writing and getting templates approved, linking your store and training the assistant.</li>
<li><strong>Ad spend</strong>, if chats come from ads. That's paid to Meta separately.</li>
</ol>

<h2>How to estimate your own monthly bill</h2>
<p>Take last month's numbers and multiply by the current UAE rate for each line:</p>
<ol>
<li><strong>Marketing templates:</strong> cart reminders, offers and re-engagement messages sent outside a free window.</li>
<li><strong>Utility templates:</strong> order and delivery updates.</li>
<li><strong>Service messages:</strong> total replies your team or assistant sends, minus 1,000 per number, minus replies inside free entry point windows.</li>
<li><strong>Authentication:</strong> one-time codes, if you send them on WhatsApp.</li>
</ol>
<p>Add the platform fee and you have a realistic monthly number. Customers outside the UAE use their own country's rate.</p>

<h2>Five ways to keep the bill down without losing sales</h2>
<ul>
<li>Reply fast, so the conversation stays inside the 24-hour window and you don't need a template to restart it.</li>
<li>Send ad traffic to WhatsApp from phones, where the free entry point window applies.</li>
<li>Write one clear follow-up instead of three; each template costs money and patience.</li>
<li>Stop sequences the moment a customer replies or buys, and never message people who said stop.</li>
<li>Keep order updates as genuine utility messages and sales messages as marketing; misfiled templates get reclassified.</li>
</ul>
<p class="note">Sources: Meta's <a href="https://developers.facebook.com/docs/whatsapp/pricing/" target="_blank" rel="noopener">WhatsApp Business Platform pricing documentation</a> and <a href="https://developers.facebook.com/docs/whatsapp/pricing/updates-to-pricing/" target="_blank" rel="noopener">pricing updates</a>, read on 26 November 2026. Meta changes pricing often; check the source before you budget.</p>
""",
    faqs=[
        ("Is the WhatsApp Business app free?", "Yes. The free WhatsApp Business app on your phone has no per-message charges. Per-message pricing applies to the WhatsApp Business API (the Business Platform), which you need for an AI assistant, team inboxes, ad tracking and scheduled follow-ups."),
        ("Do I pay when a customer messages my business?", "No. Meta only charges for messages your business sends that are delivered. Messages customers send you are free."),
        ("Which country's rate applies to a UAE business?", "The rate of the country code of the customer receiving the message. Messages to +971 numbers use the UAE rate; messages to customers abroad use their country's rate."),
        ("Are replies to customers still free after October 2026?", "Each business number gets 1,000 free service messages a month. Beyond that, service messages are charged at Meta's published rate, except for eligible government and non-profit accounts."),
        ("How long is the free window after a click-to-WhatsApp ad?", "Meta's developer documentation says the free entry point window can stay open for up to 7 days once you reply within 24 hours; its marketing pages say 72 hours. During it, Meta doesn't charge for template or service messages to that customer."),
    ],
    related=[("/whatsapp-automation-uae/", "WhatsApp Business API setup on your own number"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads guide"), ("/pricing/", "How Nuevo pricing works")],
)

# ---------------------------------------------------------------- 2
guide(
    slug="click-to-whatsapp-ads",
    title="Click-to-WhatsApp Ads: A Guide for UAE Brands | Nuevo",
    desc="How click-to-WhatsApp ads work on Instagram and Facebook, when they beat a landing page, how to set them up and how to report the sales they make.",
    h1="Click-to-WhatsApp ads: how they work and how to make them sell",
    card="When an ad that opens a chat beats a landing page, how to set one up in Ads Manager, and what to do in the first minute.",
    lead="A click-to-WhatsApp ad sends the buyer straight into a chat with your business instead of to a web page. Here is when that sells better, how to set one up, and the part most brands get wrong: what happens after the tap.",
    answer="A click-to-WhatsApp ad is an Instagram or Facebook ad whose button opens a WhatsApp chat with your business, often with a pre-filled first message. It works best when buyers have questions before they pay, such as dosage, delivery or authenticity, which is common for premium wellness products in the UAE. The ad only starts the conversation: the sale depends on replying within seconds and on reporting chat sales back to Meta so it can find more buyers.",
    body="""
<h2>What a click-to-WhatsApp ad is</h2>
<p>It's a normal Meta ad on Instagram, Facebook or Messenger whose call to action is "Send message" or "WhatsApp". Tapping it opens WhatsApp on the buyer's phone with your business number and a first message you wrote, such as "Hi, I'd like the price of the 60-capsule pack". The buyer presses send and the conversation starts.</p>
<p>Inside WhatsApp, the chat carries a small card showing which ad it came from, and the API passes your system a click ID for that ad. That ID is what lets you report the sale back to Meta later.</p>

<h2>When a chat beats a landing page</h2>
<div class="prose-table"><table>
<thead><tr><th>Send to WhatsApp when…</th><th>Send to your website when…</th></tr></thead>
<tbody>
<tr><td>Buyers ask questions before paying (ingredients, dosage, authenticity)</td><td>The product is cheap and self-explanatory</td></tr>
<tr><td>Orders are often cash on delivery or need a delivery date</td><td>Your checkout is fast and buyers rarely need help</td></tr>
<tr><td>Many buyers prefer to talk in Arabic</td><td>You can't reply within minutes, day and night</td></tr>
<tr><td>Bundles or subscriptions need a recommendation</td><td>Your buyers are mostly on desktop</td></tr>
</tbody></table></div>
<p>The second column matters. A WhatsApp ad that gets a reply three hours later usually performs worse than a plain product page, because the buyer has already scrolled on.</p>

<h2>How to set one up in Meta Ads Manager</h2>
<ol>
<li><strong>Connect your WhatsApp number</strong> to your Facebook Page or Instagram account through Meta's Accounts Center. Use the number customers already know.</li>
<li><strong>Pick the objective.</strong> Engagement, Leads or Sales can all send people to a chat; choose "Messaging apps" and then WhatsApp as the conversion location.</li>
<li><strong>Write the pre-filled message</strong> so it tells you what they want: "Price for the 60-capsule pack, please" beats "Hi".</li>
<li><strong>Add a greeting</strong> and two or three suggested questions if you use Meta's message template in the ad.</li>
<li><strong>Build the creative around one product and one question.</strong> The ad's job is to start a specific conversation, not to explain the whole brand.</li>
<li><strong>Target adults.</strong> Meta requires ads for dietary, health and herbal supplements to target people aged 18 or over. See our <a href="/guides/advertising-supplements-uae/">guide to advertising supplements in the UAE</a>.</li>
</ol>

<h2>The first minute decides the sale</h2>
<p>Someone who taps your ad is interested right now and has WhatsApp open. If the first reply takes hours, the moment has passed. What a good first reply does:</p>
<ul>
<li>Answers the exact question in the pre-filled message, with the price, in the buyer's language.</li>
<li>Asks one question back that moves toward an order: "Is it for you, or a gift?", "Which emirate shall we deliver to?"</li>
<li>Offers a way to pay in the chat, by payment link or cash on delivery, as soon as they're ready.</li>
</ul>
<p>This is the job <a href="/m2s/">M2S</a> does: an AI assistant trained on your own products and prices replies in seconds, in English or Arabic, and hands the chat to your team with a summary when it should.</p>

<h2>Why click-to-WhatsApp chats can cost less in message fees</h2>
<p>When a chat starts from one of these ads on a phone and you reply within 24 hours, Meta opens a free entry point window in which it doesn't charge message fees for that customer. Details and the October 2026 pricing change are in our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp API pricing guide</a>.</p>

<h2>Reporting sales back to Meta</h2>
<p>By default, Ads Manager reports "messaging conversations started" and a cost per conversation. It has no idea which chats bought. If you optimise on conversations, Meta learns to find people who like to chat, not people who pay.</p>
<p>The fix is to send each sale made in a chat back to Meta through the Conversions API, tied to the ad's click ID, with the order value. Then you can see real return on ad spend per ad and let Meta optimise for buyers. We cover how in <a href="/guides/track-whatsapp-ad-sales/">how to track sales from WhatsApp ads</a>.</p>

<h2>Common mistakes</h2>
<ul>
<li>Sending ads to a personal phone that one person checks when they can.</li>
<li>A vague pre-filled message, so the first reply has to be "how can I help?"</li>
<li>Judging the campaign on cost per conversation instead of cost per sale.</li>
<li>No follow-up: most chats that go quiet never hear from the business again.</li>
<li>Claims in the ad (or the chat) that the product's approval doesn't allow.</li>
</ul>
""",
    faqs=[
        ("Do click-to-WhatsApp ads work on Instagram?", "Yes. They run on Instagram, Facebook and Messenger placements. Tapping the button opens WhatsApp on the buyer's phone with your business number."),
        ("Do I need the WhatsApp Business API for click-to-WhatsApp ads?", "No, the ads can open chats on the WhatsApp Business app. You need the API to reply automatically, tag each chat with its ad, run follow-ups and report sales back to Meta."),
        ("Which campaign objective should I use?", "Engagement, Leads or Sales can all use WhatsApp as the conversion location. Once you send sales back through the Conversions API, a Sales objective lets Meta optimise for buyers rather than for conversations."),
        ("How fast do I need to reply?", "As fast as possible, ideally within seconds. The buyer has just tapped the ad and has WhatsApp open; a reply hours later usually loses the sale."),
    ],
    related=[("/instagram-dm-automation-dubai/", "Instagram ads that open a conversation"), ("/guides/track-whatsapp-ad-sales/", "Track sales from WhatsApp ads"), ("/m2s/", "How M2S works")],
)

# ---------------------------------------------------------------- 3
guide(
    slug="advertising-supplements-uae",
    title="Advertising Supplements in the UAE: 2026 Rules | Nuevo",
    desc="Meta's rules for supplement ads, the UAE's November 2026 medical-advertising clarification and the influencer ban, and how to keep WhatsApp sales chats compliant.",
    h1="Advertising supplements in the UAE: Meta's rules and the local ones",
    card="Meta's 18+ and claims rules, the Emirates Drug Establishment's November 2026 clarification, and keeping sales chats compliant.",
    lead="Supplement and wellness brands in the UAE answer to two rulebooks: Meta's advertising standards and the UAE's own approval rules. Here is what each says as of November 2026, and how to keep the ad and the WhatsApp chat behind it on the right side of both.",
    answer="On Meta, ads for dietary, health and herbal supplements must target people aged 18 or over, can't use before-and-after images or make people feel bad about their bodies, and can't promise a specific result in a set time. In the UAE, the Emirates Drug Establishment said on 18 November 2026 that every advertisement for a medical product needs its approval before it runs, on any channel including social media, and that influencers may not promote medical products. Supplements have their own registration and approval routes, which differ by product and emirate, so check your product's classification with the regulator before you advertise.",
    body="""
<p class="note">This is a plain-language summary for marketing teams, not legal advice. Rules change and depend on how your product is registered. Confirm with the regulator or a regulatory consultant before you spend.</p>

<h2>Meta's rules for supplement and wellness ads</h2>
<p>Meta's <a href="https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness" target="_blank" rel="noopener">Health and Wellness advertising standards</a> apply everywhere, including the UAE:</p>
<ul>
<li><strong>18 and over only.</strong> Ads for dietary, health, herbal or weight-loss products must be targeted to people aged at least 18.</li>
<li><strong>No negative self-image.</strong> Ads can't imply or try to create a negative view of someone's body to sell a health product. Before-and-after photos and a person on a scale are Meta's own examples of what's not allowed.</li>
<li><strong>No promised outcomes in a timeframe.</strong> "Lose 5% of your body weight in a month" is the kind of claim Meta rejects.</li>
<li><strong>Prescription products are a different policy.</strong> Weight-loss drugs and other prescription medicines fall under Meta's drugs and pharmaceuticals rules, which need written permission and country targeting.</li>
</ul>

<h2>Meta's data restrictions for health and wellness websites</h2>
<p>Industry sources report that from January 2025 Meta began restricting the data it accepts from websites it classifies as health and wellness. Depending on the classification, it can strip URL details, stop some lower-funnel events such as Lead, AddToCart and Purchase from being used for optimisation, or block a domain's events entirely; outside Europe, reports say certain standard events are blocked rather than all data. We couldn't read this on a Meta page ourselves, so check your pixel's data source settings in Events Manager. If your store is affected, a click-to-WhatsApp campaign that reports sales from the chat may give Meta more to learn from than the website pixel. See <a href="/guides/track-whatsapp-ad-sales/">tracking sales from WhatsApp ads</a>.</p>

<h2>The UAE rules: what changed in November 2026</h2>
<p>On 18 November 2026 the Emirates Drug Establishment (EDE) issued a clarification on medical product advertising, reported by <a href="https://www.thenationalnews.com/news/uae/2026/11/19/uae-drug-regulator-bans-social-media-influencers-from-promoting-medical-products/" target="_blank" rel="noopener">The National</a> and <a href="https://gulfnews.com/uae/health/emirates-drug-establishment-bans-influencer-promotion-of-medical-products-1.500755088" target="_blank" rel="noopener">Gulf News</a>:</p>
<ul>
<li>Every advertisement for a medical product must be approved by the EDE before it's published, on social media, websites, TV, radio, outdoor screens or print.</li>
<li>Social media influencers may not promote medical products, whether in paid posts, sponsored content or endorsements.</li>
</ul>
<p>Whether your product counts as a "medical product" depends on how it is registered. Supplements, herbal products and cosmetics have their own registration routes, and some emirates add their own approval step. Regulatory consultants report, for example, that Dubai Municipality requires prior approval through its Montaji system for health supplement advertising and promotions.</p>
<p>Separately, anyone in the UAE who advertises on social media for payment needs the National Media Authority's advertiser permit (formerly issued by the UAE Media Council).</p>

<h2>A practical checklist before you launch</h2>
<ol>
<li>Confirm how each product is registered and which authority approves its advertising.</li>
<li>Get the approval, and keep the approved claims written down in English and Arabic.</li>
<li>Build every ad from those approved claims only; the Arabic version says the same thing as the English one.</li>
<li>Set the audience to 18+ in Ads Manager.</li>
<li>Drop before-and-after imagery and time-bound results.</li>
<li>If you work with creators, check they hold the advertiser permit and that the product category allows creator promotion at all.</li>
</ol>

<h2>The WhatsApp chat is part of your marketing too</h2>
<p>A click-to-WhatsApp ad can be fully compliant and the sales chat behind it can still overclaim, especially when a busy team or an unchecked chatbot is answering "will this help me lose weight?" at midnight.</p>
<p>When we set up <a href="/m2s/">M2S</a> for a wellness brand, the AI assistant answers from the brand's own product sheet and approved claims. It doesn't diagnose or promise results, and it hands medical questions to a person with a summary of the chat. That keeps the conversation honest and in line with what the ad said.</p>
""",
    faqs=[
        ("Can I target supplement ads to under-18s on Instagram?", "No. Meta requires ads for dietary, health and herbal supplements, and weight-loss products, to target people aged 18 or over."),
        ("Do supplement ads in the UAE need approval?", "Often, yes. Medical product ads need Emirates Drug Establishment approval before they run, and supplements have their own registration and approval routes that can differ by emirate. Check your product's classification with the regulator."),
        ("Can influencers promote supplements in the UAE?", "Influencers may not promote medical products, under the Emirates Drug Establishment's November 2026 clarification. Whether a supplement falls under that depends on its classification, and paid creators also need the National Media Authority's advertiser permit (formerly issued by the UAE Media Council)."),
        ("Are before-and-after photos allowed in Meta wellness ads?", "No. Meta lists before-and-after weight-loss photos as an example of content that creates negative self-perception, which its health and wellness standards don't allow."),
    ],
    related=[("/ecommerce-automation-uae/", "WhatsApp sales for wellness and supplement stores"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads guide"), ("/wellness-brands/", "M2S for wellness brands")],
)

# ---------------------------------------------------------------- 4
guide(
    slug="whatsapp-abandoned-cart-recovery",
    title="WhatsApp Abandoned Cart Recovery: How It Works | Nuevo",
    desc="How to recover abandoned carts on WhatsApp: what you need, when to send, what to write in English and Arabic, what it costs and how to measure it.",
    h1="WhatsApp abandoned cart recovery, step by step",
    card="What you need, when to send, example messages in English and Arabic, and how to measure what came back.",
    lead="A cart reminder on WhatsApp gets read in a way an email often doesn't. Here is how to set one up properly: the consent, the timing, the wording, the cost and the way to tell if it's working.",
    answer="WhatsApp abandoned cart recovery means sending an approved WhatsApp template to a shopper who left items in their cart, with a way to finish the order. You need the WhatsApp Business API, the shopper's number and consent from checkout, a Meta-approved marketing template, and a link from your store that tells the system a cart was left. Send the first reminder within about an hour, at most one more the next day, stop the moment they reply or buy, and never at night.",
    body="""
<h2>What you need before the first reminder</h2>
<ol>
<li><strong>The WhatsApp Business API</strong> on your brand's number. The free app can't send automated messages. See <a href="/whatsapp-automation-uae/">WhatsApp API setup on your own number</a>.</li>
<li><strong>The shopper's number and consent.</strong> Ask for the WhatsApp number at checkout with a clear tick box or line saying you'll message them about their order.</li>
<li><strong>A cart signal from your store.</strong> Shopify, WooCommerce and most platforms can send an "abandoned checkout" event to your system, directly or through a tool like n8n, Make or Zapier.</li>
<li><strong>An approved template.</strong> Outside a 24-hour window, WhatsApp only lets businesses start a chat with a template Meta has approved. Cart reminders are classed as marketing.</li>
</ol>

<h2>When to send</h2>
<div class="prose-table"><table>
<thead><tr><th>Message</th><th>When</th><th>Goal</th></tr></thead>
<tbody>
<tr><td>Reminder 1</td><td>30–60 minutes after the cart is left</td><td>Bring them back while they still remember</td></tr>
<tr><td>Reminder 2 (optional)</td><td>The next day, during the day</td><td>Answer the question that stopped them</td></tr>
<tr><td>Stop</td><td>As soon as they reply, buy or say stop</td><td>Respect, and cost control</td></tr>
</tbody></table></div>
<p>Two messages is usually enough. Never send at night, and don't put a customer into more than one sequence a week.</p>

<h2>What to write</h2>
<p>Name the product, make finishing easy and invite a reply. A reply reopens the 24-hour window, so the conversation can continue normally.</p>
<blockquote><p>Hi Sara, you left the Magnesium Glycinate 120 caps in your cart. Want me to hold it for you? I can send a payment link here, or you can pay cash on delivery.</p></blockquote>
<blockquote><p lang="ar" dir="rtl">مرحباً سارة، تركتِ مغنيسيوم جلايسينات ١٢٠ كبسولة في السلة. هل أحجزه لكِ؟ أقدر أرسل لك رابط الدفع هنا، أو الدفع عند الاستلام.</p></blockquote>
<p>The second reminder works best when it removes a reason not to buy: delivery time to their emirate, how to take the product, or a smaller size. Avoid fake urgency; Meta reviews templates and customers can block or report you, which hurts your number's quality rating.</p>

<h2>Cash on delivery and payment links</h2>
<p>Many UAE shoppers abandon at the card step, not because they changed their mind. Offering cash on delivery or a payment link inside the chat often recovers those orders. If you offer cash on delivery, confirm the address and delivery slot in the chat to cut refusals at the door.</p>

<h2>What it costs</h2>
<p>Each reminder is a marketing template, charged per delivered message at the rate for the customer's country. There's no charge for the customer's reply. If the customer replies, your answers are service messages, covered by 1,000 free a month per number from October 2026. Full details are in our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp API pricing guide</a>.</p>

<h2>How to measure it honestly</h2>
<ul>
<li>Count only orders from carts that got a reminder, placed after the reminder, within a set window (we use 72 hours).</li>
<li>For cash on delivery, count delivered orders, not placed ones.</li>
<li>Compare with a period, or a slice of carts, that got no reminder. Some of those shoppers would have come back anyway.</li>
</ul>
<p>In M2S's monthly report, recovered carts are listed separately from new sales so you can see exactly what the follow-ups brought back.</p>
""",
    faqs=[
        ("Can I send cart reminders from the free WhatsApp Business app?", "Not automatically. Automated reminders need the WhatsApp Business API and a Meta-approved template."),
        ("Is an abandoned-cart message marketing or utility?", "Meta treats cart reminders as marketing messages, so they need a marketing template and are charged at the marketing rate."),
        ("How many reminders should I send?", "One within about an hour, and at most one more the next day. Stop as soon as the shopper replies, buys or asks you to stop."),
        ("Do I need consent to message shoppers on WhatsApp?", "Yes. WhatsApp requires opt-in. Ask for the number at checkout with a clear statement that you'll message them about their order, and honour every stop request."),
    ],
    related=[("/ecommerce-automation-uae/", "WhatsApp automation for online stores"), ("/crm-automation-uae/", "Follow-ups and pipeline"), ("/n8n-make-zapier-automation-uae/", "Store and CRM integrations")],
)

# ---------------------------------------------------------------- 5
guide(
    slug="track-whatsapp-ad-sales",
    title="How to Track Sales From WhatsApp Ads (Real ROAS) | Nuevo",
    desc="Why Ads Manager shows conversations, not sales, for WhatsApp ads, and how to send chat sales back to Meta with the Conversions API to see real return on ad spend.",
    h1="How to track sales from WhatsApp ads and see your real ROAS",
    card="Why Ads Manager only sees conversations, and how sending chat sales back to Meta shows real return on ad spend.",
    lead="Click-to-WhatsApp ads are easy to launch and hard to measure: the sale happens in a chat Meta can't see. Here is how to connect each order back to the ad that started it.",
    answer="Ads Manager can't see what happens inside a WhatsApp chat, so for click-to-WhatsApp ads it reports conversations started, not sales. To see real return on ad spend, capture the click ID WhatsApp passes with each chat that starts from an ad, and when that chat turns into an order, send a Purchase event with the order value to Meta's Conversions API. Meta then attributes the sale to the ad and can optimise for buyers instead of chatters.",
    body="""
<h2>Why Ads Manager shows conversations, not sales</h2>
<p>On a website, the Meta Pixel sees the purchase page. In WhatsApp there's no pixel: the order is agreed in a chat and paid by link or on delivery. Unless you tell Meta, it only knows a conversation started. Brands then judge ads on cost per conversation, and Meta learns to find people who like to chat.</p>

<h2>The pieces that connect a chat to an ad</h2>
<ol>
<li><strong>The click ID.</strong> When a chat starts from a click-to-WhatsApp ad, the WhatsApp Business API includes a referral with the ad's details and a click ID (<code>ctwa_clid</code>) in the first message your system receives. Store it on the chat.</li>
<li><strong>The order.</strong> When the chat becomes a paid or delivered order, record its value and currency against the same chat.</li>
<li><strong>The Conversions API.</strong> Send Meta a Purchase event for business messaging, with the click ID, value and currency. Meta matches it to the ad.</li>
</ol>
<p>Meta documents this as the <a href="https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging" target="_blank" rel="noopener">Conversions API for business messaging</a>. The dataset needs to be linked to your WhatsApp Business account.</p>

<h2>Which events to send</h2>
<ul>
<li><strong>Lead:</strong> the buyer gave real intent, such as asking for a price for a specific product.</li>
<li><strong>Initiate checkout:</strong> a payment link was sent or a cash-on-delivery order was started.</li>
<li><strong>Purchase:</strong> the order was paid, or delivered for cash on delivery, with the value.</li>
</ul>
<p>Send Purchase only once per order, and only when the money is real. Counting placed cash-on-delivery orders that later get refused at the door inflates ROAS.</p>

<h2>Reading the numbers honestly</h2>
<ul>
<li><strong>Meta's ROAS is an estimate.</strong> It depends on the attribution window and modelled conversions. Compare it with your store's own orders each month.</li>
<li><strong>Don't credit the ad with every order.</strong> Repeat customers who message you directly aren't ad sales.</li>
<li><strong>Look per ad, not only per campaign.</strong> One creative often carries the account.</li>
</ul>
<p>Our <a href="/results/khaleej-parapharma/">Khaleej ParaPharma case study</a> shows what this looks like in practice: a 19.6x average return on ad spend across 14 campaigns as Meta estimates it, reported beside the store's own figures. It's one brand's result, not a typical one.</p>

<h2>Once sales flow back</h2>
<p>With purchases reaching Meta, you can run a Sales objective that optimises for buyers, set cost caps on real orders and drop ads that start chats but never sell. This is built into <a href="/m2s/">M2S</a>: each chat is tagged with the ad that started it, and sales made in the chat are reported back to Meta automatically.</p>
""",
    faqs=[
        ("Can Meta Pixel track WhatsApp sales?", "No. The pixel only runs on web pages. Sales made inside WhatsApp chats need to be sent to Meta through the Conversions API, tied to the ad's click ID."),
        ("What is ctwa_clid?", "It's the click ID the WhatsApp Business API passes with the first message of a chat that started from a click-to-WhatsApp ad. Sending it back with a Purchase event lets Meta attribute the sale to that ad."),
        ("Should I optimise click-to-WhatsApp ads for conversations or sales?", "For sales, once purchases are reaching Meta. Optimising for conversations teaches Meta to find people who start chats, not people who buy."),
        ("Is Meta's reported ROAS accurate?", "It's an estimate based on its attribution window and modelling. Compare it every month with your store's own delivered orders."),
    ],
    related=[("/results/", "M2S results"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads guide"), ("/instagram-dm-automation-dubai/", "Instagram ads and DMs")],
)


# ---------------------------------------------------------------- 6
guide(
    slug="whatsapp-chatbot-cost-uae",
    title="WhatsApp Chatbot Cost in the UAE, 2026 | Nuevo Automations",
    desc="What a WhatsApp chatbot really costs a UAE business in 2026: Meta's message fees, platform subscriptions like Wati and Respond.io, AI credits and setup.",
    h1="How much does a WhatsApp chatbot cost in the UAE?",
    card="The four costs behind a WhatsApp chatbot in 2026: Meta's message fees, the platform, AI usage and setup, with real platform prices.",
    lead="A WhatsApp chatbot is never one price. You pay Meta for messages, a platform for the inbox and automation, someone for the AI, and someone to set it up. Here is each part for a UAE business in 2026, with list prices from the platforms themselves.",
    answer="A WhatsApp chatbot in the UAE has four costs. First, Meta's per-message fees on the WhatsApp Business Platform, priced by message type at the UAE rate; customer messages are free, and chats from click-to-WhatsApp ads open a free window. Second, a platform subscription: on their own pricing pages in November 2026, Wati starts at $59 a month (billed annually), Respond.io at $79 a month (annually) or $99 monthly, Gallabox at AED 412 a month (annually), and Twilio charges $0.005 per message with no subscription. Third, AI usage, usually as platform AI credits. Fourth, setup: connecting your number, templates, store integration and training the bot.",
    body="""
<h2>Cost 1: Meta's message fees</h2>
<p>Every WhatsApp chatbot that runs on the official API pays Meta per delivered message. The price depends on the message category (marketing, utility, authentication or service) and on the country code of the customer receiving it. The UAE is its own market on Meta's rate card, and Meta lists the dirham as a billing currency from 1 April 2026.</p>
<ul>
<li><strong>Messages customers send you are free.</strong></li>
<li><strong>Service replies:</strong> from 1 October 2026 each business number gets 1,000 free service messages a month, then pays per message.</li>
<li><strong>Click-to-WhatsApp ads:</strong> if you reply within 24 hours, Meta opens a free entry point window of up to 7 days in which template and service messages to that customer aren't charged.</li>
<li><strong>Meta Business Agent</strong> (Meta's own AI) is billed separately at $2 per million tokens.</li>
</ul>
<p>Rates change several times a year, so check <a href="https://developers.facebook.com/docs/whatsapp/pricing/" target="_blank" rel="noopener">Meta's pricing page</a> before you budget. Our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp Business API pricing guide</a> explains the rules in full.</p>

<h2>Cost 2: the platform</h2>
<p>The API has no inbox or chatbot builder of its own, so almost every business uses a platform on top. These are the list prices on each platform's own pricing page on 26 November 2026. They exclude Meta's message fees.</p>
<div class="prose-table"><table>
<thead><tr><th>Platform</th><th>Entry price</th><th>What you get at that price</th><th>Message fees</th></tr></thead>
<tbody>
<tr><td>Wati</td><td>$59 a month, billed annually (Growth)</td><td>3 users, 2,000 AI credits, 1 AI agent. Pro is $119, Business $279.</td><td>Meta's fees, paid through Wati's wallet; markup not stated</td></tr>
<tr><td>Respond.io</td><td>$79 a month annually, $99 monthly (Starter)</td><td>5 users, 5,000 AI credits. AI agents start on Growth ($159 annually, $199 monthly).</td><td>Not included; Respond.io says it does not mark up Meta's rates</td></tr>
<tr><td>Interakt</td><td>$55 a month plus taxes (Growth)</td><td>AI Agents is an add-on at $74.99</td><td>Enterprise lists "no template markups", which implies lower plans have one</td></tr>
<tr><td>Gallabox</td><td>AED 412 a month annually, AED 549 quarterly (Basic)</td><td>3 users, 500 AI credits</td><td>Enterprise lists a discounted markup, which implies standard plans have one</td></tr>
<tr><td>Twilio</td><td>No subscription</td><td>API only: you build or buy the chatbot yourself</td><td>$0.005 per message on top of Meta's fees</td></tr>
</tbody></table></div>
<p>Two things change the real cost more than the headline price: how many team members need the inbox (extra users cost $12 to $89 each a month depending on platform and plan) and whether the platform adds a margin to Meta's message fees.</p>

<h2>Cost 3: the AI</h2>
<p>A rules-based bot with buttons costs nothing extra. A bot that understands free-text questions, in English and Arabic, uses a language model, and someone pays for it:</p>
<ul>
<li><strong>Platform AI credits.</strong> Wati, Respond.io and Gallabox include a monthly allowance and sell more: Wati charges $25 for 2,000 extra credits, Respond.io $15 per 1,000.</li>
<li><strong>Meta Business Agent tokens</strong>, if you use Meta's own AI, at $2 per million tokens.</li>
<li><strong>Your own model</strong>, if a developer builds the bot on the API directly.</li>
</ul>
<p>The cheapest AI is the one that answers correctly the first time. A bot that guesses at prices or stock costs you sales, not credits, so make sure it is trained on your real catalogue and hands hard questions to a person.</p>

<h2>Cost 4: setup and running it</h2>
<p>Someone has to connect your number to the API, verify your business with Meta, write and get templates approved, connect your store (Shopify, WooCommerce or Zid), load your products and policies, write the flows for carts and payment links, and then watch the first weeks of chats and fix what the bot gets wrong. You can do this yourself on a platform, or pay an agency or developer to do it. We haven't found a credible public benchmark for setup fees in the UAE, so ask for a fixed quote in writing.</p>

<h2>A simple way to compare quotes</h2>
<ol>
<li>Estimate your monthly messages by type (cart reminders, order updates, replies).</li>
<li>Price them at Meta's current UAE rate, then ask each platform whether it adds anything per message.</li>
<li>Add the platform fee for the plan and number of users you actually need.</li>
<li>Add AI usage at your expected volume, not the free allowance.</li>
<li>Add setup and any monthly management.</li>
</ol>
<p>Then compare that total with the sales it brings back. A bot that recovers a handful of abandoned carts a week usually pays for itself; one that only answers FAQs often doesn't.</p>
<p class="note">Sources: Meta's <a href="https://developers.facebook.com/docs/whatsapp/pricing/" target="_blank" rel="noopener">WhatsApp pricing documentation</a>; pricing pages of <a href="https://www.wati.io/pricing/" target="_blank" rel="noopener">Wati</a>, <a href="https://respond.io/pricing" target="_blank" rel="noopener">Respond.io</a>, <a href="https://www.interakt.shop/pricing/" target="_blank" rel="noopener">Interakt</a>, <a href="https://gallabox.com/pricing" target="_blank" rel="noopener">Gallabox</a> and <a href="https://www.twilio.com/en-us/whatsapp/pricing" target="_blank" rel="noopener">Twilio</a>, read on 26 November 2026. Prices change; check the source before you buy. Nuevo Automations isn't affiliated with these platforms.</p>
""",
    faqs=[
        ("Is there a free WhatsApp chatbot?", "The free WhatsApp Business app has quick replies and a greeting message but no real chatbot or AI. A chatbot needs the WhatsApp Business API, which means Meta's per-message fees plus a platform or developer."),
        ("What is the cheapest way to run a WhatsApp chatbot?", "Building directly on the API with a provider like Twilio has no subscription ($0.005 a message plus Meta's fees) but needs a developer. For most small brands, a platform's entry plan is cheaper overall once you count build and maintenance time."),
        ("Do WhatsApp platforms charge more than Meta for messages?", "Some do. Respond.io says it doesn't mark up Meta's rates. Interakt and Gallabox list markup discounts on enterprise plans, which implies a markup on lower plans. Wati shows its rates only after login. Ask each provider in writing."),
        ("Can a WhatsApp chatbot reply in Arabic?", "Yes. AI-based bots on the main platforms can reply in Arabic and English. Check how well the bot handles Gulf dialect and mixed Arabic-English messages before you commit."),
        ("Does the chatbot cost more if customers come from ads?", "Usually less. Chats that start from a click-to-WhatsApp ad on a phone open Meta's free entry point window when you reply within 24 hours, so Meta doesn't charge for messages to that customer for up to 7 days."),
    ],
    related=[("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing in the UAE"), ("/guides/respond-io-vs-wati/", "Respond.io vs Wati"), ("/ai-chatbot-development-uae/", "AI sales chatbot for UAE brands")],
)

# ---------------------------------------------------------------- 7
guide(
    slug="meta-ads-ecommerce-uae",
    title="Meta Ads for E-commerce Brands in the UAE, 2026 | Nuevo",
    desc="Running Meta ads for an online store in the UAE in 2026: sales campaigns, Conversions API, ad rules for health products, VAT and the advertiser permit.",
    h1="Meta ads for e-commerce brands in the UAE: what to know in 2026",
    card="Campaign types, tracking with the Conversions API, health product rules, VAT on ad spend and the UAE advertiser permit.",
    lead="Instagram and Facebook are where most UAE online stores find buyers. This guide covers the campaign setup, tracking, rules and paperwork that matter for a UAE brand in 2026, without the guesswork benchmarks.",
    answer="For a UAE online store, Meta ads in 2026 mean Advantage+ sales campaigns (the renamed Advantage+ shopping campaigns) or manual sales campaigns, optimised on purchases tracked through the Meta pixel plus the Conversions API. Health and supplement ads must target people 18 or older and avoid miracle claims. Meta charges 5% UAE VAT on ad spend unless you add your 15-digit tax registration number. Influencers and creators who promote products in the UAE need an advertiser permit from the National Media Authority, enforced from early 2026, and brands should check the permit before paying them.",
    body="""
<h2>Pick the right campaign</h2>
<p>Meta renamed Advantage+ shopping campaigns to <strong>Advantage+ sales campaigns</strong> in February 2025. They now share one setup with the Sales objective. You can let Meta automate audience, placements and budget, or turn settings off and run what Meta calls a manual sales campaign.</p>
<ul>
<li><strong>Advantage+ sales</strong> works best once your pixel sees steady purchases. Meta's system needs conversions to learn from.</li>
<li><strong>Manual sales campaigns</strong> give more control when you're testing products, audiences or creative, or when purchase volume is low.</li>
<li><strong>Click-to-WhatsApp (messages) campaigns</strong> suit products people want to ask about first: supplements, skincare, anything with sizing or dosage questions. They skip the landing page. See our <a href="/guides/click-to-whatsapp-ads/">click-to-WhatsApp ads guide</a>.</li>
</ul>

<h2>Track purchases properly: pixel plus Conversions API</h2>
<p>Browser tracking alone misses sales because of ad blockers, iOS privacy settings and in-app browsers. Meta's <strong>Conversions API</strong> sends purchase events from your server, store platform or CRM straight to Meta. Setting it up from Events Manager has no fees. Run it alongside the pixel and make sure events are deduplicated, so one sale isn't counted twice.</p>
<p>If you sell in WhatsApp chats, the pixel never sees the sale at all. You need to send those purchases back to Meta with the ad's click ID; our <a href="/guides/track-whatsapp-ad-sales/">guide to tracking WhatsApp ad sales</a> shows how.</p>

<h2>Rules for health, wellness and supplement products</h2>
<p>Meta's Health and Wellness policy applies to diet, weight-loss and supplement products:</p>
<ul>
<li>Target people <strong>18 or older</strong>.</li>
<li>No claims to cure diseases, no clickbait health claims, no close-ups of pinched fat.</li>
<li>Meta can block supplements it considers potentially unsafe.</li>
</ul>
<p>The UAE has its own rules on top of Meta's. Our <a href="/guides/advertising-supplements-uae/">guide to advertising supplements in the UAE</a> covers the Emirates Drug Establishment's position on medical product ads.</p>

<h2>VAT on your Meta ad spend</h2>
<p>When Meta started charging VAT in the UAE, it billed 5% VAT to UAE accounts that hadn't added a tax registration number. If your business is VAT-registered, add your 15-digit TRN in your ad account's payment settings; tax advisers then treat the spend under the reverse charge mechanism. Ask your accountant how to record it, and check your Meta invoices to confirm which treatment applies.</p>

<h2>The UAE advertiser permit for influencers</h2>
<p>Under the UAE's 2023 media law, anyone who promotes products on social media in the UAE, paid or unpaid, needs an advertiser permit. The National Media Authority now runs it, and enforcement began at the end of January 2026. Reported details:</p>
<ul>
<li>The permit is free for the first three years, then AED 1,000 a year. Visiting creators can get a three-month permit for AED 500 through a licensed agency.</li>
<li>Creators must show the permit number on their profile.</li>
<li>Brands and agencies should check the creator's permit before paying and put the permit number in the contract.</li>
<li>Reported fines for posting without a permit start at AED 10,000.</li>
</ul>
<p>Promoting your own business from your own account is reported to be exempt. Confirm the current rules with the National Media Authority before a campaign.</p>

<h2>What actually moves results</h2>
<ol>
<li><strong>Creative.</strong> With broad targeting, the ad itself picks the audience. Test several angles, show the product in use, and refresh what fatigues.</li>
<li><strong>Arabic and English.</strong> Test both. Many UAE buyers respond better to the language they think in, and Gulf Arabic copy reads differently from translated copy.</li>
<li><strong>Speed after the click.</strong> A buyer who messages and waits an hour is usually gone. Fast replies, by a person or an AI assistant, protect the money you spent on the click.</li>
<li><strong>Cash on delivery and fast delivery.</strong> If you offer them, say so in the ad.</li>
</ol>
<p>We don't publish CPM or CPC benchmarks for the UAE here: we haven't found a reliable public source, and costs vary widely by product, season (Ramadan, White Friday, DSF) and creative.</p>
<p class="note">Sources: Meta's <a href="https://developers.facebook.com/docs/marketing-api/advantage-campaigns" target="_blank" rel="noopener">Advantage+ campaigns documentation</a>, <a href="https://developers.facebook.com/docs/marketing-api/conversions-api" target="_blank" rel="noopener">Conversions API documentation</a> and <a href="https://transparency.meta.com/policies/ad-standards/restricted-goods-services/health-wellness" target="_blank" rel="noopener">Health and Wellness ad policy</a>; reporting by <a href="https://www.pinsentmasons.com/out-law/news/uae-influencer-licence-deadline-looms" target="_blank" rel="noopener">Pinsent Masons</a> and <a href="https://www.thenationalnews.com/news/uae/2025/07/30/uae-social-media-advertiser-permit" target="_blank" rel="noopener">The National</a> on the advertiser permit, and <a href="https://gulfnews.com/technology/now-vat-for-uae-ads-on-facebook-1.1576560764009" target="_blank" rel="noopener">Gulf News</a> on VAT. Read on 26 November 2026. This isn't legal or tax advice.</p>
""",
    faqs=[
        ("What happened to Advantage+ shopping campaigns?", "Meta renamed them Advantage+ sales campaigns in February 2025 and merged them into the Sales objective setup. Turning off certain automated settings makes it a manual sales campaign."),
        ("Do I need the Conversions API if I have the Meta pixel?", "It's strongly recommended. The pixel misses purchases blocked by browsers and privacy settings; the Conversions API sends them from your server or store. Meta charges nothing for it when set up through Events Manager."),
        ("Do I pay VAT on Facebook and Instagram ads in the UAE?", "Meta charges 5% VAT to UAE ad accounts without a tax registration number. VAT-registered businesses can add their 15-digit TRN in payment settings; check with your accountant how to account for it."),
        ("Do influencers in the UAE need a licence to promote my products?", "Yes. Since early 2026, people promoting products on social media in the UAE need an advertiser permit from the National Media Authority. Check the permit before you pay and put the number in the contract."),
        ("Can I target under-18s with supplement ads?", "No. Meta requires health, diet, weight-loss and supplement ads to target people 18 or older."),
    ],
    related=[("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads guide"), ("/guides/advertising-supplements-uae/", "Advertising supplements in the UAE"), ("/ecommerce-automation-uae/", "Automation for online stores")],
)

# ---------------------------------------------------------------- 8
guide(
    slug="respond-io-vs-wati",
    title="Respond.io vs Wati for UAE Businesses (2026) | Nuevo",
    desc="Respond.io vs Wati compared for UAE brands in 2026: prices, users, AI credits, WhatsApp fee markups, channels, Shopify and CRM integrations.",
    h1="Respond.io vs Wati: which WhatsApp platform fits a UAE brand?",
    card="Plans and prices, users, AI, message-fee markups, channels and integrations, side by side from each company's own pages.",
    lead="Respond.io and Wati are two of the platforms UAE businesses most often use to run WhatsApp on the official API. Both add a team inbox, automation and AI on top of Meta. Here is how they compare in November 2026, using each company's own pricing and help pages.",
    answer="Wati is cheaper to start: Growth is $59 a month billed annually with 3 users, and it has strong e-commerce integrations including Shopify, WooCommerce, Zoho CRM and Klaviyo. Respond.io starts at $79 a month annually ($99 monthly) with 5 users, covers more channels (WhatsApp, Instagram, Messenger, TikTok, Telegram, LINE, Viber, WeChat, email, SMS and more), and states that it does not mark up Meta's WhatsApp rates. Wati shows its message rates only after login. Both offer 7-day free trials and AI agents. Pick Wati for a Shopify-led store on a budget; pick Respond.io for a multi-channel team that wants transparent message pricing.",
    body="""
<h2>Price and plans</h2>
<p>Prices below are from each company's pricing page on 26 November 2026, in US dollars per month, and exclude Meta's WhatsApp message fees.</p>
<div class="prose-table"><table>
<thead><tr><th></th><th>Wati</th><th>Respond.io</th></tr></thead>
<tbody>
<tr><td>Entry plan</td><td>Growth: $59 (billed annually)</td><td>Starter: $79 annually, $99 monthly</td></tr>
<tr><td>Middle plan</td><td>Pro: $119</td><td>Growth: $159 annually, $199 monthly</td></tr>
<tr><td>Top listed plan</td><td>Business: $279</td><td>Advanced: $279 annually, $349 monthly</td></tr>
<tr><td>Users included</td><td>3 on Growth, 5 on Pro and Business</td><td>5 on Starter, 10 on Growth and Advanced</td></tr>
<tr><td>Extra users</td><td>Not on Growth; $39 (Pro), $89 (Business)</td><td>$12 to $24 depending on plan</td></tr>
<tr><td>Contacts</td><td>Not stated on the pricing page</td><td>Priced by monthly active contacts, from 1,000</td></tr>
<tr><td>Free trial</td><td>7 days</td><td>7 days, no card</td></tr>
</tbody></table></div>
<p>Wati's page lists annual prices only and says annual billing saves up to 20%. Respond.io's contact and user limits were laid out ambiguously on its page; confirm them with sales before you sign.</p>

<h2>WhatsApp message fees and markups</h2>
<p>Both platforms pass on Meta's per-message fees. The difference is transparency:</p>
<ul>
<li><strong>Respond.io</strong> says WhatsApp fees aren't included in any subscription and that it does not mark up WhatsApp's official rates.</li>
<li><strong>Wati</strong> shows its per-message rates inside the account (Wallet, then Pricing Overview), not on the public pricing page, and doesn't state publicly whether it adds a margin.</li>
</ul>
<p>At low volume the difference is small. If you send tens of thousands of cart reminders or broadcasts a month, ask Wati for its UAE rates in writing and compare them with <a href="https://developers.facebook.com/docs/whatsapp/pricing/" target="_blank" rel="noopener">Meta's rate card</a>.</p>

<h2>AI</h2>
<ul>
<li><strong>Wati</strong>: AI agents ("Astra") on every plan: 1 on Growth, 2 on Pro, unlimited on Business, with 2,000 to 20,000 AI credits a month. Extra credits are $25 per 2,000.</li>
<li><strong>Respond.io</strong>: AI agents from the Growth plan up, with 5,000 to 40,000 AI credits a month depending on plan. Extra credits are $15 per 1,000.</li>
</ul>
<p>Credits run out faster than you'd expect once an AI answers every chat, so price the plan at your real volume.</p>

<h2>Channels</h2>
<p><strong>Respond.io</strong> is built as a multi-channel inbox: WhatsApp (including calling), Instagram, Messenger, TikTok, Telegram, LINE, Viber, WeChat, RCS, email, SMS, webchat and VoIP. <strong>Wati</strong> centres on WhatsApp and adds Instagram, Facebook Messenger, TikTok, webchat and RCS. For most UAE e-commerce brands, WhatsApp and Instagram are what matter, and both cover them.</p>

<h2>Integrations</h2>
<ul>
<li><strong>Wati</strong>: Shopify (an add-on at $4.99 a month on some plans), WooCommerce, Zoho CRM, Klaviyo, Zapier and Make; HubSpot from Pro, Salesforce on Business.</li>
<li><strong>Respond.io</strong>: HubSpot and Salesforce directly (contacts sync into respond.io); WooCommerce through Zapier; Shopify only as a webchat widget; Zoho not listed.</li>
</ul>
<p>For a Shopify or WooCommerce store that wants order data in its WhatsApp flows, Wati's native store integrations are the stronger fit. For a sales team living in HubSpot or Salesforce, either works.</p>

<h2>Data hosting</h2>
<p>Wati says each customer gets its own database with backups on Google Cloud across several regions, and offers dedicated hosting in a location you choose for $1,000 a month. Respond.io's pricing page mentions ISO 27001 certification but doesn't state where data is hosted. If you handle health data, ask both where it's stored.</p>

<h2>Which to pick</h2>
<ul>
<li><strong>Wati</strong> if you're a small Shopify or WooCommerce store, WhatsApp is your main channel, and budget matters most.</li>
<li><strong>Respond.io</strong> if your team answers several channels in one inbox, you want published, no-markup message pricing, or you need more users per plan.</li>
<li><strong>Neither</strong>, on its own, will run your ads or close your sales. A platform is the tool; you still need the flows, the AI trained on your products, and someone watching the results.</li>
</ul>
<p class="note">Sources: <a href="https://www.wati.io/pricing/" target="_blank" rel="noopener">Wati pricing</a>, <a href="https://support.wati.io/en/articles/11463219-wati-security-overview-data-protection-backups-and-hosting" target="_blank" rel="noopener">Wati security overview</a>, <a href="https://respond.io/pricing" target="_blank" rel="noopener">Respond.io pricing</a>, <a href="https://respond.io/integrations" target="_blank" rel="noopener">Respond.io integrations</a> and <a href="https://respond.io/faqs/how-much-does-whatsapp-business-api-cost-and-are-there-any-hidden-charges" target="_blank" rel="noopener">Respond.io's WhatsApp fees FAQ</a>, read on 26 November 2026. Nuevo Automations isn't affiliated with either company; M2S runs on OrcaFlo, our own platform.</p>
""",
    faqs=[
        ("Is Wati cheaper than Respond.io?", "At the entry level, yes: Wati Growth is $59 a month billed annually, Respond.io Starter is $79 annually or $99 monthly. Respond.io includes more users per plan, so for a larger team the gap narrows."),
        ("Does Respond.io charge extra for WhatsApp messages?", "Respond.io says it passes on WhatsApp's official rates without a markup. Meta's message fees are billed on top of the subscription."),
        ("Does Wati integrate with Shopify?", "Yes. Wati lists a Shopify integration, sold as an add-on at $4.99 a month on some plans, plus WooCommerce, Zoho CRM and Klaviyo."),
        ("Do both platforms have AI agents?", "Yes. Wati includes AI agents on every plan; Respond.io includes them from the Growth plan up. Both sell AI credits, with monthly allowances that differ by plan."),
        ("Can I try them before paying?", "Both offer a 7-day free trial. Respond.io's trial needs no card and includes Growth features for 5 users and 1,000 contacts."),
    ],
    related=[("/guides/whatsapp-chatbot-cost-uae/", "How much a WhatsApp chatbot costs"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing"), ("/whatsapp-automation-uae/", "WhatsApp sales automation on your own number")],
)


# ================================================================ batch 3 (28 Nov 2026)

guide(
    slug="whatsapp-payment-links-uae",
    title="How to Take Payments on WhatsApp in the UAE, 2026 | Nuevo",
    desc="WhatsApp Pay isn't live in the UAE, so brands sell in the chat with payment links. Fees for Stripe, Ziina, Telr and others, plus Tabby and Tamara.",
    h1="How to take payments on WhatsApp in the UAE",
    card="Why WhatsApp's own payments don't work in the UAE yet, how payment links fill the gap, and what Stripe, Ziina, Telr and the BNPL providers charge.",
    lead="Customers in the UAE are happy to buy in a WhatsApp chat, but WhatsApp itself can't take their money here. The fix is a payment link from your payment provider. This guide covers what works, what each provider charges, and how to keep the sale in the chat.",
    answer="WhatsApp's built-in payments, including the \"Review and Pay\" order message, are only documented by Meta for India, Brazil and Singapore, not the UAE. UAE businesses take payment in WhatsApp by sending a payment link from their own provider: Stripe charges 2.9% plus AED 1 for domestic cards, Ziina lists 2.6% plus AED 1 on its business page, and Telr has monthly plans with unlimited payment links. Tabby and Tamara can also create payment links, though their documentation describes sending them by SMS or email. The customer taps the link, pays on the provider's page, and your team or AI confirms the order in the chat.",
    body="""
<h2>WhatsApp Pay isn't available to UAE businesses</h2>
<p>Meta does have native payments on the WhatsApp Business Platform: an order message where the customer taps <strong>Review and Pay</strong> and pays without leaving WhatsApp. But Meta's documentation covers only three markets. In India it works with UPI and payment gateways in rupees only, in Brazil with Pix, boleto and payment links, and in Singapore through Stripe for Singapore businesses. We found no UAE version as of November 2026.</p>
<p>So a UAE brand can't use the native order and payment messages. What it can do is send a normal link, or a template with a link button, that opens a secure payment page from a licensed provider.</p>

<h2>Payment link providers for UAE businesses</h2>
<p>These are the fees each provider publishes on its own UAE page, read on 28 November 2026. Card fees change, and some providers negotiate, so confirm before you sign.</p>
<div class="prose-table"><table>
<thead><tr><th>Provider</th><th>Published UAE fees</th><th>Payment links</th></tr></thead>
<tbody>
<tr><td>Stripe</td><td>2.9% + AED 1 for domestic cards; +1% for international cards; +1% if currency conversion is needed</td><td>Included at no extra cost. Stripe's docs say links can be shared by email, SMS or social media.</td></tr>
<tr><td>Ziina</td><td>2.6% + AED 1 on its business page, +1.5% for international cards (its separate fees page shows 2.9% + AED 1, so confirm which applies)</td><td>Says links can be shared "on any platform, including WhatsApp".</td></tr>
<tr><td>Telr</td><td>Plans from AED 0 to AED 249 a month, with card fees from 0% to 2.45% + AED 1 depending on volume, plus 5% VAT</td><td>Unlimited, branded payment links on every plan.</td></tr>
<tr><td>Network International (N-Genius)</td><td>Not published</td><td>"Pay By Link" with an option to share links through messaging apps.</td></tr>
<tr><td>Checkout.com</td><td>Not published</td><td>One-time links that expire after 24 hours by default; enabled through an account manager.</td></tr>
<tr><td>PayTabs</td><td>No UAE rates published (only Saudi pricing)</td><td>Offers PayLinks and digital invoices.</td></tr>
</tbody></table></div>

<h2>Buy now, pay later in the chat: Tabby and Tamara</h2>
<p>Instalments help with higher-priced orders, such as a three-month supplement bundle. Both big UAE providers can create payment links:</p>
<ul>
<li><strong>Tabby</strong> lets merchants create payment links in its merchant dashboard and business app. Its help pages describe sending them by SMS or email.</li>
<li><strong>Tamara</strong> documents a payment link that is sent to the customer by SMS and expires after 15 minutes by default.</li>
</ul>
<p>Neither documents WhatsApp as a channel. Some payment gateways offer Tabby or Tamara inside their own links, which you can send in WhatsApp. Ask your provider how they want it done before you build a flow around it.</p>

<h2>How a sale in WhatsApp should run</h2>
<ol>
<li><strong>Answer the questions first.</strong> Price, ingredients, delivery time. Buyers who ask before they pay are the ones a landing page loses.</li>
<li><strong>Confirm the order in writing:</strong> product, quantity, price including VAT, delivery address and date.</li>
<li><strong>Send the link with the amount in the message</strong>, so the customer knows exactly what they are paying for.</li>
<li><strong>Watch for the payment.</strong> Most providers send a webhook or email when a link is paid. Connect it so the chat updates automatically.</li>
<li><strong>Follow up on unpaid links.</strong> A polite reminder a few hours later recovers a share of buyers who got distracted. Inside the 24-hour customer service window this is a normal reply; outside it you need an approved template.</li>
<li><strong>Offer cash on delivery as a fallback</strong> if your logistics support it, for customers who won't pay online.</li>
</ol>

<h2>What WhatsApp messages cost along the way</h2>
<p>Meta charges per delivered message. From 1 October 2026 utility messages, such as an order confirmation, are charged even inside the 24-hour window, and service replies are free only up to 1,000 a month per number. Chats that start from a click-to-WhatsApp ad still open a free entry point window when you reply within 24 hours. Our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp Business API pricing guide</a> has the details.</p>
<p class="note">Sources: Meta's WhatsApp payments documentation for India and Brazil; pricing pages of <a href="https://stripe.com/ae/pricing" target="_blank" rel="noopener">Stripe UAE</a>, <a href="https://ziina.com/business" target="_blank" rel="noopener">Ziina</a> and <a href="https://telr.com/pricing" target="_blank" rel="noopener">Telr</a>; Tabby and Tamara merchant documentation; all read on 28 November 2026. Nuevo Automations isn't affiliated with any of these providers.</p>
""",
    faqs=[
        ("Is WhatsApp Pay available in the UAE?", "Not for businesses, as of November 2026. Meta documents WhatsApp's native business payments only for India, Brazil and Singapore. UAE businesses send a payment link from their own provider instead."),
        ("What is the cheapest way to take a payment in WhatsApp?", "It depends on volume. Stripe has no monthly fee and charges 2.9% plus AED 1 for domestic cards. Telr's higher-volume plans go down to 2.25% plus AED 0.50 with no monthly fee. Compare the total on your real monthly sales, including international cards."),
        ("Can I send a Tabby or Tamara link on WhatsApp?", "Both can create payment links, but their own documentation describes sending them by SMS or email, not WhatsApp. Some gateways offer BNPL inside links you can share in WhatsApp. Ask the provider before building it into your flow."),
        ("Do I need the WhatsApp Business API to send payment links?", "No, you can paste a link in the free WhatsApp Business app. You need the API to automate it: sending links from an AI assistant, tracking which are paid, and following up on unpaid ones."),
        ("Is it safe for customers to pay through a WhatsApp link?", "Yes, when the link opens a page from a licensed payment provider on its own domain. Tell customers which provider you use, and never ask for card details inside the chat itself."),
    ],
    related=[("/guides/whatsapp-abandoned-cart-recovery/", "WhatsApp abandoned cart recovery"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing"), ("/ecommerce-automation-uae/", "WhatsApp sales for online stores")],
)

guide(
    slug="sell-supplements-online-uae",
    title="How to Sell Supplements Online in the UAE, 2026 | Nuevo",
    desc="Selling supplements online in the UAE: who registers products (EDE, Dubai Municipality), e-commerce licences, Arabic rules, ad approvals and payments.",
    h1="How to sell supplements online in the UAE",
    card="Product registration with the Emirates Drug Establishment and Dubai Municipality, e-commerce licences, Arabic requirements, advertising rules and payments.",
    lead="Supplements are one of the fastest-moving online categories in the UAE, and one of the most regulated. This guide pulls together what the official sources say in November 2026, and flags where they leave questions only the regulator can answer.",
    answer="To sell supplements online in the UAE you need a trade licence that allows e-commerce (for example Dubai's eTrader or Abu Dhabi's Tajer licence, or a free zone e-commerce licence), and your products must be registered. Federally, the Emirates Drug Establishment (EDE) took over medical product services from the Ministry of Health from 29 December 2025 and lists food supplements under its healthcare product marketing authorisation, which only a licensed medical warehouse can apply for. In Dubai, Dubai Municipality requires health supplements to be registered in its Montaji system before they are imported, advertised or sold. Product details and invoices must be available in Arabic, VAT is 5%, and ads for medical products need EDE approval.",
    body="""
<p class="note">This guide is general information, not legal advice. Rules on supplements changed several times in 2025 and 2026. Confirm your route with the Emirates Drug Establishment (800 33784) and, in Dubai, Dubai Municipality (800900) before you import or advertise.</p>

<h2>1. Work out what your product legally is</h2>
<p>The same capsule can be a food supplement or a medicine depending on what it contains and what you claim. EDE's healthcare product route covers preparations for general health that are <strong>not intended to diagnose, treat, cure or prevent disease</strong>, and names food supplements, herbal and homeopathic products among them. A product that makes disease claims, or contains restricted ingredients or medicinal doses, falls into the medicine route, which is far stricter and limits where it can be sold.</p>
<p>Peptides deserve a special warning. In July 2026 EDE acted against 71 sources selling unapproved peptide products for weight loss and referred 14 influencers to the media regulator, according to Gulf News. EDE's position was that calling something a "peptide" doesn't make it an approved product. Treat injectable or therapeutic peptides as medical products, not supplements.</p>

<h2>2. Register the products</h2>
<ul>
<li><strong>Emirates Drug Establishment (federal).</strong> The "Marketing Authorisation for a Healthcare Product" service lists food supplements. The applicant must be an EDE-licensed medical warehouse, the service takes 45 working days, the certificate lasts 5 years, and the application fee is AED 100 (other fees depend on the product). Documents include a free-sale certificate, a halal certificate, a declaration that the product is free of hormones, steroids, heavy metals and pork-derived material, the artwork and the full composition.</li>
<li><strong>Dubai Municipality (Dubai).</strong> Its technical guidelines for health supplements say no health supplement may be manufactured, imported, advertised, sold or distributed in Dubai unless it is registered in the Montaji system.</li>
<li><strong>Abu Dhabi and the other emirates.</strong> Local food and health authorities have their own requirements; check with them.</li>
</ul>
<p>The official pages overlap, and we couldn't confirm from primary sources whether a basic vitamin needs EDE registration, Montaji registration or both. In practice most brands work with a licensed importer or warehouse that handles registration. Ask them which applies to each product, in writing.</p>

<h2>3. Get the right licence to sell online</h2>
<p>According to the UAE government portal, mainland sellers need a licence with an e-commerce activity from their emirate's economic department, such as Dubai's eTrader licence or Abu Dhabi's Tajer licence, and e-commerce licences also need approval from the TDRA. Free zones issue e-commerce licences too, but selling directly to mainland customers may need a local distributor. Online trade is governed by Federal Decree-Law No. 14 of 2023.</p>

<h2>4. Arabic, labels and claims</h2>
<ul>
<li>Under UAE consumer protection law, online sellers must give product details, terms, payment and warranty information <strong>in Arabic</strong> (other languages can be added), issue invoices in Arabic, and say which authority licenses them.</li>
<li>Labels follow the UAE's food supplement, nutrition labelling and health claims standards. Most brands use Arabic and English on pack; confirm with your registration agent.</li>
<li>Keep claims to general wellbeing. A claim to treat or prevent a condition can move the product into the medicine route.</li>
</ul>

<h2>5. Advertising: what changed in 2026</h2>
<ul>
<li>On 18 November 2026, EDE announced that ads for medical products need its approval before they run, and that social media influencers may not advertise or endorse medical products, as The National reported the next day. The report doesn't say whether supplements registered as healthcare products are included, so ask EDE before you brief creators.</li>
<li>Anyone promoting products on social media in the UAE, paid or not, needs an Advertiser Permit, now run by the National Media Authority. Check a creator's permit before you pay them.</li>
<li>On Meta, health and wellness ads must be targeted at people 18 or older and avoid before-and-after and "miracle" claims. Our <a href="/guides/advertising-supplements-uae/">guide to advertising supplements in the UAE</a> covers Meta's rules in detail.</li>
</ul>

<h2>6. Payments, VAT and delivery</h2>
<ul>
<li><strong>VAT</strong> is 5%. Registration is mandatory above AED 375,000 in taxable sales a year and voluntary from AED 187,500.</li>
<li><strong>Card payments:</strong> Shopify Payments lists the UAE as a supported country, and Stripe, Network International, Telr, Tabby and Tamara all serve UAE stores. Read your provider's restricted business list: Stripe, for example, prohibits nutraceuticals that are unsafe or make harmful claims.</li>
<li><strong>Selling in WhatsApp:</strong> many UAE supplement buyers ask questions before paying. Our guide to <a href="/guides/whatsapp-payment-links-uae/">taking payments on WhatsApp</a> shows how to close those sales in the chat.</li>
</ul>
<p class="note">Sources: <a href="https://www.ede.gov.ae/en/w/issuance-of-marketing-authorization-for-a-healthcare-product" target="_blank" rel="noopener">EDE healthcare product marketing authorisation</a>; <a href="https://mohap.gov.ae/en/mte" target="_blank" rel="noopener">MOHAP service transfer notice</a>; Dubai Municipality technical guidelines for health supplements (V2, 2024); u.ae pages on <a href="https://u.ae/en/information-and-services/business/Managing-and-growing-your-business/ecommerce" target="_blank" rel="noopener">e-commerce</a> and <a href="https://u.ae/en/information-and-services/justice-safety-and-the-law/consumer-protection" target="_blank" rel="noopener">consumer protection</a>; The National (19 November 2026) and Gulf News (25 July 2026) reporting. Read 28 November 2026.</p>
""",
    faqs=[
        ("Do I need to register supplements before selling them online in the UAE?", "Yes. In Dubai, Dubai Municipality requires health supplements to be registered in its Montaji system before they are sold or advertised. Federally, the Emirates Drug Establishment lists food supplements under its healthcare product marketing authorisation. Confirm which applies to your product with both."),
        ("Who regulates supplements in the UAE now?", "Medical product services, including marketing authorisations and advertising approvals, moved from the Ministry of Health and Prevention to the Emirates Drug Establishment from 29 December 2025. Dubai Municipality and other local authorities also register health supplements in their emirates."),
        ("Can I sell supplements from a free zone company?", "Free zones issue e-commerce licences, but selling directly to mainland UAE customers may need a local distributor or extra approvals, and product registration still applies. Check with your free zone and a registration agent."),
        ("Can influencers promote my supplements?", "Every creator promoting products in the UAE needs an Advertiser Permit. Since November 2026, influencers may not promote medical products, and ads for them need EDE approval. Ask EDE whether your registered supplement counts before you brief anyone."),
        ("Are peptides treated as supplements in the UAE?", "No. In July 2026 the Emirates Drug Establishment acted against sellers of unapproved peptide products and said the label \"peptide\" doesn't make something an approved product. Treat therapeutic peptides as medical products."),
    ],
    related=[("/guides/advertising-supplements-uae/", "Advertising supplements in the UAE"), ("/guides/meta-ads-ecommerce-uae/", "Meta ads for UAE e-commerce"), ("/m2s/", "How M2S sells for supplement brands")],
)

guide(
    slug="shopify-whatsapp-integration",
    title="Shopify WhatsApp Integration for UAE Stores, 2026 | Nuevo",
    desc="How to connect Shopify to WhatsApp in 2026: Shopify Messaging, Meta's official app, Zoko, Interakt, Wati and others, with prices and what each automates.",
    h1="Shopify WhatsApp integration: the options in 2026",
    card="Shopify Messaging, Meta's own WhatsApp app and the main third-party apps compared, plus which messages Meta treats as marketing.",
    lead="Shopify now has WhatsApp built in, Meta has its own Shopify app, and there are dozens of third-party apps. They don't do the same job. Here is what each one covers for a UAE store, with the prices listed on 28 November 2026.",
    answer="There are three ways to connect Shopify to WhatsApp in 2026. Shopify Messaging, built into Shopify, sends WhatsApp marketing campaigns and abandoned cart, checkout and browse automations, with an opt-in at checkout; in the UAE it charges US$0.10 per marketing message. Meta's official WhatsApp app for Shopify is free to install and sends order updates and abandoned cart messages, with Meta billing messages separately. Third-party apps such as Zoko, Interakt, Wati, SuperLemon and Gallabox add a shared team inbox, cash on delivery confirmation and AI chat. Shopify Inbox, Shopify's chat tool, does not connect to WhatsApp.",
    body="""
<h2>Option 1: Shopify Messaging (built in)</h2>
<p>Shopify added WhatsApp to Shopify Messaging, the tool formerly called Shopify Email, on 29 July 2026, and added WhatsApp marketing automations on 28 October 2026.</p>
<ul>
<li><strong>What it does:</strong> campaigns (back in stock, upcoming sale, product showcase, VIP offers) and pre-built abandoned browse, cart and checkout automations.</li>
<li><strong>Consent:</strong> you switch on a WhatsApp marketing opt-in that shows at checkout, and you can import existing consent by CSV. Messages only go to subscribed customers, and every message carries a STOP line you can't remove.</li>
<li><strong>UAE pricing:</strong> US$0.100 per marketing message and US$0.0157 per service message, with 1,000 free service messages a month, billed on your Shopify invoice.</li>
<li><strong>Limits:</strong> it is a marketing tool. Shopify's documentation doesn't cover order confirmations or shipping updates, new accounts are capped at 2,000 messages a day until Meta raises the limit, and if your number is already connected to another WhatsApp provider you must disconnect it first.</li>
</ul>

<h2>Option 2: Meta's official WhatsApp app for Shopify</h2>
<p>Meta publishes its own app on the Shopify App Store, launched in July 2025. It was rated 4.4 from 1,002 reviews on 28 November 2026, is free to install, and sends automated order updates and abandoned cart messages in several languages including Arabic. Meta bills the messages directly. It is a notification tool, not a team inbox or a chatbot.</p>

<h2>Option 3: third-party WhatsApp apps</h2>
<p>These apps run on the WhatsApp Business API and add a shared inbox, automations and, on some plans, AI. Prices are the app's own Shopify App Store listing on 28 November 2026; WhatsApp message charges are extra.</p>
<div class="prose-table"><table>
<thead><tr><th>App</th><th>Rating</th><th>Listed price</th><th>Notable for a UAE store</th></tr></thead>
<tbody>
<tr><td>Zoko</td><td>4.9 (486 reviews)</td><td>From $49.99 a month</td><td>Catalogue checkout in WhatsApp, cart recovery, shared inbox; AI is an add-on</td></tr>
<tr><td>Interakt</td><td>4.3 (240)</td><td>From $21 a month</td><td>Order and shipping updates, cash on delivery confirmation; cart reminders on the top plan</td></tr>
<tr><td>Wati</td><td>3.7 (121)</td><td>From $69 a month</td><td>Cart recovery, leads from click-to-WhatsApp ads, AI agents</td></tr>
<tr><td>SuperLemon</td><td>3.5 (344)</td><td>Free, $9.99 or $29.99 a month</td><td>Cash on delivery confirmation and order updates; your own API number from $29.99</td></tr>
<tr><td>Gallabox</td><td>4.2 (5)</td><td>From $5 a month as an add-on to a Gallabox plan</td><td>Order notifications and cart recovery; Dubai office</td></tr>
</tbody></table></div>
<p>Respond.io has no Shopify App Store app; it connects through a website widget and tools like Zapier, Make or n8n.</p>

<h2>Which messages Meta counts as marketing</h2>
<p>This decides both the price and who you can message. Meta's template rules say:</p>
<ul>
<li><strong>Order confirmations and shipping updates</strong> are utility messages, as long as they contain no promotion.</li>
<li><strong>Abandoned cart reminders are marketing</strong>, "even if requested by users", in Meta's words. They need marketing consent and are priced as marketing.</li>
<li>A template that mixes order details with a discount or product suggestion counts as marketing. Since April 2025 Meta automatically recategorises utility templates that look like marketing.</li>
</ul>
<p>Shopify itself treats a checkout as abandoned once it stays incomplete for more than 10 minutes after the customer gives an email address. You can trigger WhatsApp flows from that with Shopify Flow or the checkout webhooks.</p>

<h2>What about Zid and Salla?</h2>
<p>Zid has WhatsApp built in, with abandoned cart reminders, nine order status notifications and back-in-stock alerts, included in its Professional plan or SAR 109 a month otherwise. Salla relies on third-party WhatsApp apps from its app store.</p>

<h2>Which one should you pick?</h2>
<ul>
<li><strong>Just order updates:</strong> Meta's free app is enough.</li>
<li><strong>Campaigns and cart recovery, no inbox:</strong> Shopify Messaging keeps billing and consent in Shopify.</li>
<li><strong>Customers who ask questions before buying</strong>, which is most supplement and wellness buyers: you need an inbox and someone, or an AI, answering in seconds. That is where a third-party platform or a service like <a href="/m2s/">M2S</a> comes in.</li>
</ul>
<p class="note">Sources: Shopify Help Center pages on Shopify Messaging WhatsApp requirements, setup and pricing, abandoned checkouts and Shopify Flow; Shopify changelog (29 July and 28 October 2026); Shopify App Store listings; Meta's WhatsApp template categorisation guidelines; Zid's WhatsApp page. Read 28 November 2026. Ratings and prices change often.</p>
""",
    faqs=[
        ("Does Shopify have WhatsApp built in?", "Yes, since July 2026. Shopify Messaging can send WhatsApp marketing campaigns and, since October 2026, abandoned cart, checkout and browse automations. In the UAE it costs US$0.10 per marketing message."),
        ("Does Shopify Inbox work with WhatsApp?", "No. Shopify Inbox is a chat tool for your online store; its help pages don't mention WhatsApp. For WhatsApp conversations you need Shopify Messaging for campaigns, or a WhatsApp app with an inbox."),
        ("Is there a free WhatsApp app for Shopify?", "Meta's official WhatsApp app is free to install, and Meta bills each message separately. SuperLemon also has a free plan. Every option still pays Meta's per-message fees."),
        ("Are abandoned cart messages on WhatsApp utility or marketing?", "Marketing. Meta's template guidelines list cart reminders as marketing even when the customer asked for them, so you need marketing consent and pay the marketing rate."),
        ("Can I use my existing WhatsApp number with Shopify?", "Usually yes, through the WhatsApp Business API. If the number is already connected to another WhatsApp provider, Shopify Messaging requires you to disconnect it first."),
    ],
    related=[("/guides/whatsapp-abandoned-cart-recovery/", "WhatsApp abandoned cart recovery"), ("/guides/whatsapp-payment-links-uae/", "Taking payments on WhatsApp"), ("/ecommerce-automation-uae/", "WhatsApp sales for online stores")],
)

guide(
    slug="arabic-whatsapp-chatbot",
    title="Arabic WhatsApp Chatbots: Gulf Dialect and AI, 2026 | Nuevo",
    desc="What makes an Arabic WhatsApp chatbot work in the UAE: Gulf dialect, Arabizi, mixed Arabic and English, right-to-left templates, and what research shows.",
    h1="Arabic WhatsApp chatbots: what works in the UAE",
    card="Gulf dialect, Arabizi and mixed Arabic-English messages, what published research says about AI in Arabic dialects, and how to test a bot before launch.",
    lead="Most chatbot platforms say they \"support Arabic\". Your customers don't write textbook Arabic, though. They write Gulf dialect, Arabic in Latin letters, and English and Arabic in the same message. Here is what that means for a WhatsApp chatbot, and how to test one properly.",
    answer="An Arabic WhatsApp chatbot for the UAE has to handle three kinds of writing: Gulf and Emirati dialect, Arabizi (Arabic written in Latin letters and numbers, like \"7abibi\"), and messages that mix Arabic and English. Published research shows AI models still do worse in Arabic dialects than in English: in the 2025 DialectalArabicMMLU benchmark, 19 open models averaged about 48% accuracy in dialects, 52% in Modern Standard Arabic and 63% in English. Templates need the right Arabic language code (such as ar_AE) and testing for right-to-left layout. The best test is to send the bot real messages from your own customers before launch.",
    body="""
<h2>Three ways UAE customers write Arabic</h2>
<ul>
<li><strong>Gulf and Emirati dialect.</strong> Everyday words and grammar differ from Modern Standard Arabic, the formal Arabic most AI models are trained on.</li>
<li><strong>Arabizi.</strong> Arabic typed in Latin letters, with numbers for sounds English lacks: 3 for ع, 7 for ح, 5 for خ. Common on phones.</li>
<li><strong>Code-switching.</strong> English and Arabic in one message: "Hi, عندكم vitamin D 5000؟ how much". A 2025 academic survey of code-switched Arabic calls this widespread and says handling it is vital for language technology.</li>
</ul>
<p>A bot that only handles formal Arabic will answer some customers in a register that sounds stiff, and misunderstand others.</p>

<h2>What the research says about AI and Arabic dialects</h2>
<ul>
<li><strong>DialectalArabicMMLU</strong> (IBM, NYU Abu Dhabi and MBZUAI, 2025) asked the same questions in five dialects, Modern Standard Arabic and English. Across 19 open models, average accuracy was about 47.7% in dialects, 51.9% in Modern Standard Arabic and 62.8% in English. Emirati scored highest of the dialects, at 49.8%.</li>
<li><strong>AraDiCE</strong> (Qatar Computing Research Institute, 2025) found that Arabic-focused models such as Jais and AceGPT beat general multilingual models on dialect tasks, and that models are better at understanding dialects than writing them.</li>
<li>The <strong>Open Arabic LLM Leaderboard</strong> mostly measures Modern Standard Arabic, so a high score there says little about Gulf dialect.</li>
<li>We found no published benchmark for Gulf Arabizi or Gulf Arabic-English mixing in chat. Nobody can tell you from a leaderboard how a bot will handle your customers; you have to test it.</li>
</ul>
<p>The UAE is also building its own models: the Technology Innovation Institute released Falcon Arabic in May 2025 and models trained on the Emirati dialect in October 2026.</p>

<h2>Right-to-left templates on WhatsApp</h2>
<p>Messages you send outside the 24-hour window use Meta-approved templates, and each language is its own version. Meta offers several Arabic language codes, including <code>ar</code> and <code>ar_AE</code>; it doesn't translate for you. Two practical points:</p>
<ul>
<li>English product names, prices and order numbers inside an Arabic sentence can appear in the wrong order on screen. Put variables at natural break points and preview on a real phone.</li>
<li>Variables must be numbered in order and a template can't start or end with one, in any language.</li>
</ul>

<h2>What the main platforms say</h2>
<p>On their own websites in November 2026, Respond.io offers a full Arabic interface for agents, Wati demonstrates Arabic voice replies, and Interakt has an Arabic marketing site. None of them makes a written claim about Gulf dialect accuracy for its AI. Meta's AI agent for WhatsApp Business became available globally in June 2026, without published language details. Treat any "supports Arabic" claim as something to verify.</p>

<h2>How to test an Arabic chatbot before launch</h2>
<ol>
<li>Collect 50 real customer messages from your WhatsApp history, in every style above.</li>
<li>Send each one to the bot and check three things: did it understand, is the answer correct, and does it sound like a person from here?</li>
<li>Check it replies in the language the customer used, and doesn't switch to formal Arabic for a casual question.</li>
<li>Try the hard ones: prices, stock, delivery to a specific area, a complaint. A good bot hands these to a person when unsure rather than guessing.</li>
<li>Send your templates to yourself and read them on both iPhone and Android.</li>
</ol>
<p>M2S replies in the language the customer writes in and never invents prices or products; anything it can't answer goes to your team with a summary. See <a href="/ai-chatbot-development-uae/">how we build and test the assistant</a>.</p>
<p class="note">Sources: Altakrori et al., <a href="https://arxiv.org/abs/2510.27543" target="_blank" rel="noopener">DialectalArabicMMLU</a> (2025); Mousi et al., <a href="https://arxiv.org/abs/2409.11404" target="_blank" rel="noopener">AraDiCE</a> (COLING 2025); Hamed et al., <a href="https://arxiv.org/abs/2501.13419" target="_blank" rel="noopener">A Survey of Code-switched Arabic NLP</a> (COLING 2025); Hugging Face, Open Arabic LLM Leaderboard v2; Meta's WhatsApp template documentation. Read 28 November 2026.</p>
""",
    faqs=[
        ("Can a WhatsApp chatbot reply in Arabic?", "Yes. AI chatbots on the WhatsApp Business API can reply in Arabic and English. How well they handle Gulf dialect, Arabizi and mixed messages varies a lot, so test with real customer messages."),
        ("What is Arabizi?", "Arabic written in Latin letters, with numbers standing in for Arabic sounds, for example 3 for ع and 7 for ح. Many people in the UAE type this way on their phones, so a chatbot should understand it."),
        ("Is AI worse in Arabic than in English?", "On published benchmarks, yes. In the 2025 DialectalArabicMMLU study, 19 open models averaged about 63% accuracy in English, 52% in Modern Standard Arabic and 48% in Arabic dialects."),
        ("Which Arabic language code should UAE templates use?", "Meta offers several Arabic codes, including ar and ar_AE. Pick one and keep it consistent, then supply your own Arabic text; Meta doesn't translate templates."),
        ("Should the chatbot reply in formal Arabic or dialect?", "Match the customer. Formal Arabic is safe for templates and policies, but a casual question in Gulf dialect reads better with a natural, simple reply."),
    ],
    related=[("/ai-chatbot-development-uae/", "How we build an AI sales chatbot"), ("/guides/whatsapp-chatbot-cost-uae/", "WhatsApp chatbot cost in the UAE"), ("/guides/respond-io-vs-wati/", "Respond.io vs Wati")],
)

guide(
    slug="wati-alternatives",
    title="Wati Alternatives for UAE Businesses, 2026 Prices | Nuevo",
    desc="Wati alternatives compared for UAE businesses in 2026: Respond.io, SleekFlow, Gallabox, Interakt, Zoko, AiSensy, Twilio and more, with real list prices.",
    h1="Wati alternatives for UAE businesses in 2026",
    card="Ten WhatsApp platforms compared with Wati on entry price, users, AI and message fees, including the two with Dubai offices.",
    lead="Wati is one of the best-known WhatsApp Business API platforms, but it isn't the only option, and for some UAE teams it isn't the cheapest. Here are the main alternatives with the prices on their own pricing pages on 28 November 2026.",
    answer="The main Wati alternatives in 2026 are Respond.io (from $79 a month billed annually, 5 users), SleekFlow (from AED 399 a month billed annually, 10 users, with a DIFC office), Gallabox (from AED 412 a month billed annually, 3 users, with a Dubai office), Interakt (from $55 a month), Zoko (from $49.99 a month, no markup on Meta fees), AiSensy (from $45 a month), Twilio (no subscription, $0.005 per message on top of Meta's fees), Trengo, Callbell and Kommo. For comparison, Wati's Growth plan is $59 a month billed annually for 3 users. Meta's own message fees are extra on all of them.",
    body="""
<h2>Wati for reference</h2>
<p>Wati's pricing page lists Growth at $59 a month, Pro at $119 and Business at $279, billed annually. Growth includes 3 users and Pro and Business 5, with extra users at $39 or $89 each. AI agents and AI credits are included on every plan. Wati doesn't state on its pricing page whether it adds a margin to Meta's message fees; a third-party analysis of its October 2026 rate card estimated about 1.6 times Meta's marketing rate.</p>

<h2>The alternatives, side by side</h2>
<p>Entry prices are from each platform's own pricing page, read on 28 November 2026. Pages vary by country and billing period, so check the price you are shown.</p>
<div class="prose-table"><table>
<thead><tr><th>Platform</th><th>Entry price</th><th>Users</th><th>AI</th><th>Meta message fees</th></tr></thead>
<tbody>
<tr><td>Respond.io</td><td>$79/mo annually</td><td>5</td><td>AI assist on Starter; AI agents from Growth ($159)</td><td>Not included in the plan; billed by usage</td></tr>
<tr><td>SleekFlow</td><td>AED 399/mo annually (Pro)</td><td>10</td><td>Basic AI replies, 3,000 AI credits, 1 AI agent</td><td>Per SleekFlow's rate card</td></tr>
<tr><td>Gallabox</td><td>AED 412/mo annually, AED 549 quarterly</td><td>3</td><td>500 AI credits; WhatsApp AI agents from Essential</td><td>Enterprise lists a "discounted markup"</td></tr>
<tr><td>Interakt</td><td>$55/mo (Growth)</td><td>Unlimited</td><td>AI agents add-on, $74.99</td><td>Only Enterprise says no markup</td></tr>
<tr><td>Zoko</td><td>$49.99/mo (Starter)</td><td>Unlimited</td><td>AI add-ons from $24.99</td><td>No markup: you pay Meta directly, plus $0.015 per conversation to Zoko</td></tr>
<tr><td>AiSensy</td><td>$45/mo (Basic, per its July 2025 update)</td><td>Unlimited (fair use)</td><td>AI agent builder add-on, $50/mo</td><td>Not stated</td></tr>
<tr><td>Twilio</td><td>No subscription</td><td>API only</td><td>Build your own</td><td>Meta's fees plus $0.005 per message</td></tr>
<tr><td>Trengo</td><td>€149/mo monthly, €119 annually</td><td>3</td><td>AI agent, charged per AI conversation</td><td>Not stated</td></tr>
<tr><td>Callbell</td><td>€14 per agent/mo plus WhatsApp from €20/mo</td><td>Per agent</td><td>Bot add-on €59; ChatGPT on Enterprise</td><td>Meta's rates; no markup stated</td></tr>
<tr><td>Kommo</td><td>$25 per user/mo, 6-month minimum</td><td>Per user</td><td>AI credits; AI agents from $35</td><td>Not explained</td></tr>
</tbody></table></div>

<h2>Which alternative fits which team</h2>
<ul>
<li><strong>You want someone local:</strong> SleekFlow (DIFC) and Gallabox (Sheikh Zayed Road) list Dubai offices on their contact pages. We didn't find a UAE office for Wati or Respond.io.</li>
<li><strong>A bigger team on one inbox:</strong> SleekFlow includes 10 seats and Respond.io 5; Interakt, Zoko and AiSensy don't charge per user.</li>
<li><strong>Shopify store:</strong> Zoko has the highest rating of the WhatsApp apps on the Shopify App Store (4.9 from 486 reviews). See our <a href="/guides/shopify-whatsapp-integration/">Shopify WhatsApp guide</a>.</li>
<li><strong>Lowest message costs at volume:</strong> Zoko and Twilio are clear that Meta's fees pass through, with their own small charge on top.</li>
<li><strong>You have developers:</strong> Twilio gives you the API without a subscription, and you build the inbox and AI yourself.</li>
</ul>

<h2>What none of them does for you</h2>
<p>Every platform here is software. Someone still has to write the answers the AI gives, load your products and prices, set up and tune the follow-ups, run the ads that start the chats, and check every week what the AI got wrong. If you would rather not do that in-house, that's the work <a href="/m2s/">M2S</a> covers.</p>
<p class="note">Sources: pricing pages of Wati, Respond.io, SleekFlow, Gallabox, Interakt, AiSensy (July 2025 pricing update), Zoko, Twilio, Trengo, Callbell and Kommo; contact pages of SleekFlow and Gallabox; eesel.ai analysis of Wati's rate card (October 2026). Read 28 November 2026. Nuevo Automations isn't affiliated with any of these platforms.</p>
""",
    faqs=[
        ("What is the best Wati alternative in the UAE?", "It depends on the team. SleekFlow and Gallabox have Dubai offices, Respond.io includes 5 users on its entry plan, and Zoko and Twilio pass Meta's message fees through without a markup. Compare total monthly cost, including messages and users."),
        ("Is there a cheaper alternative to Wati?", "On entry price, AiSensy ($45 a month), Zoko ($49.99) and Interakt ($55) list lower prices than Wati's Growth plan ($59 a month billed annually). Twilio has no subscription at all but needs developers."),
        ("Do WhatsApp platforms mark up Meta's message fees?", "Some do. Zoko says you pay Meta directly, Twilio adds $0.005 per message, and Interakt and Gallabox mention reduced or no markup only on enterprise plans. Ask each provider for its UAE per-message rate in writing."),
        ("Can I move my WhatsApp number from Wati to another platform?", "Yes. A WhatsApp Business API number can be migrated between providers. Plan for a short changeover, and note that templates may need to be recreated."),
        ("Which WhatsApp platforms have an office in Dubai?", "SleekFlow lists an office in DIFC and Gallabox one on Sheikh Zayed Road. We didn't find a UAE office for Wati or Respond.io in November 2026."),
    ],
    related=[("/guides/respond-io-vs-wati/", "Respond.io vs Wati"), ("/guides/whatsapp-chatbot-cost-uae/", "WhatsApp chatbot cost in the UAE"), ("/whatsapp-automation-uae/", "WhatsApp sales automation")],
)


# ================================================================ batch 4 (28 Nov 2026)

guide(
    slug="whatsapp-marketing-rules-uae",
    title="WhatsApp Marketing Rules in the UAE, 2026 | Nuevo",
    desc="The rules for WhatsApp marketing in the UAE in 2026: Meta's opt-in policy, messaging limits, per-user caps, the telemarketing resolution and the PDPL.",
    h1="WhatsApp marketing rules in the UAE: what to follow in 2026",
    card="Meta's opt-in and opt-out rules, messaging limits and penalties, plus the UAE telemarketing resolution and data protection law, in plain terms.",
    lead="Two sets of rules apply when a UAE brand sends marketing on WhatsApp: Meta's, which decide whether your number keeps working, and the UAE's, which decide whether you get fined. Here is what each says as of November 2026, and where the law leaves room for interpretation.",
    answer="To send WhatsApp marketing in the UAE, you need the customer's number and their opt-in, which must name your business and make clear they are agreeing to messages from you. You must honour opt-out requests made on or off WhatsApp. Messages outside the 24-hour customer service window must use Meta-approved templates, new accounts can message 250 people a day until Meta raises the limit, and Meta can cap marketing messages to people who don't engage. Under UAE law, Cabinet Resolution No. 56 of 2024 defines telemarketing to include marketing messages through social media applications, and the data protection law (Federal Decree-Law No. 45 of 2021) requires consent to process personal data, with some exceptions.",
    body="""
<p class="note">This guide is general information, not legal advice. Where the law isn't explicit about WhatsApp, we say so.</p>

<h2>Meta's rules: opt-in and opt-out</h2>
<p>WhatsApp's Business Messaging Policy (last updated 23 September 2026) lets you message people only if they gave you their number <strong>and</strong> agreed to hear from you. Meta's developer documentation adds that the opt-in must:</p>
<ul>
<li>clearly state that the person is opting in to receive messages from the business;</li>
<li>clearly name the business;</li>
<li>comply with local law. It can be general rather than WhatsApp-specific.</li>
</ul>
<p>You must respect every request to stop, "either on or off WhatsApp", and remove the person from your list. Meta's documentation doesn't require a STOP keyword, but templates can carry an optional opt-out button, and customers can also turn off "offers and announcements" from your business in WhatsApp itself. Good practice: separate opt-ins for order updates and for offers, so someone can keep one and drop the other.</p>

<h2>Templates and the 24-hour window</h2>
<p>When a customer messages you, a 24-hour customer service window opens and you can reply freely. Outside it, you can only send pre-approved templates in three categories:</p>
<ul>
<li><strong>Marketing:</strong> offers, announcements, cart reminders, anything promotional. Mixed content counts as marketing.</li>
<li><strong>Utility:</strong> non-promotional messages about something the customer did, such as an order confirmation.</li>
<li><strong>Authentication:</strong> one-time passcodes only.</li>
</ul>
<p>If you submit a marketing message as utility, Meta relabels it as marketing, and repeat misuse leads to rate limits and restrictions on utility templates for 7 to 30 days.</p>

<h2>Messaging limits in 2026</h2>
<p>Meta caps how many different people you can start conversations with in a rolling 24 hours. Since 7 October 2025 the limit is shared by every number in your business portfolio.</p>
<div class="prose-table"><table>
<thead><tr><th>Tier</th><th>How you get there</th></tr></thead>
<tbody>
<tr><td>250</td><td>The default for a new business portfolio</td></tr>
<tr><td>2,000</td><td>Verify your business, be verified by your partner, or send 2,000 high-quality template messages to unique people within 30 days</td></tr>
<tr><td>10,000, 100,000, unlimited</td><td>Automatic, one step at a time, when your messages are high quality and you used at least half your limit in the last 7 days; upgrades take up to 6 hours</td></tr>
</tbody></table></div>
<p>The old 1,000 tier and the "Flagged" quality state no longer exist, so older guides that mention them are out of date.</p>

<h2>Per-user marketing caps</h2>
<p>Separately, WhatsApp may limit how many marketing templates one person receives from all businesses, when that person is unlikely to engage. There is no published number. A blocked message fails with error 131049, and Meta says to wait at least 24 hours before trying again. Marketing messages inside an open 24-hour window don't count towards the cap.</p>

<h2>What happens when customers block or report you</h2>
<p>Templates get a quality rating (green, yellow or red) from blocks, reports and read rates, and low-quality templates can be paused. Policy breaches follow a ladder: a warning, then 1 to 3 days without templates, then 5 to 30 days without sending anything, then an indefinite account lock, then a permanent ban. Scams and illegal drug sales lead straight to removal. Appeals go through Business Support Home and usually take 24 to 48 hours.</p>

<h2>UAE law: the telemarketing rules</h2>
<p>Cabinet Resolution No. 56 of 2024 on telemarketing has applied since August 2024. Its definition of telemarketing includes "marketing text messages and marketing messages through social media applications". WhatsApp isn't named, and the Ministry of Economy's summary talks only about calls, so whether it covers WhatsApp is a matter of interpretation. Its main rules, written mostly for calls, are:</p>
<ul>
<li>prior approval from the authority, and only local numbers registered to the company;</li>
<li>marketing only to consumers who asked for it, and never to numbers on the Do Not Call Register;</li>
<li>marketing calls only between 9am and 6pm, and at most once a day and twice a week to someone who didn't answer;</li>
<li>saying who you are and why you are contacting the person at the start.</li>
</ul>
<p>According to the Ministry of Economy, the accompanying penalties resolution sets fines of AED 10,000 to 150,000 for companies. Khaleej Times reported in August 2026 that AED 19.19 million in fines had been issued to individuals and 9,433 numbers disconnected.</p>
<p>The safe reading for a brand: message only people who opted in, identify yourself in every first message, keep marketing to sensible hours, and stop immediately when asked.</p>

<h2>UAE law: personal data</h2>
<p>Federal Decree-Law No. 45 of 2021 on personal data protection has been in force since 2 January 2022. It prohibits processing personal data without consent, with listed exceptions, and lets people restrict or stop processing. Secondary sources say its executive regulations still hadn't been issued as of August 2026, and fine amounts quoted online don't trace to an official source. DIFC and ADGM have their own data protection laws.</p>
<p>In practice: record when and how each customer opted in, keep that record, and delete people who ask you to.</p>

<h2>A compliant setup, step by step</h2>
<ol>
<li>Collect opt-in at checkout, in your forms or in the chat, naming your brand and the kind of messages.</li>
<li>Store the opt-in with a date and source.</li>
<li>Use utility templates only for order updates; everything promotional is marketing.</li>
<li>Add an opt-out button to marketing templates and honour it automatically.</li>
<li>Send fewer, better messages. Engagement keeps your quality rating, and your limits, healthy.</li>
</ol>
<p>M2S handles opt-in, opt-out and quiet hours automatically; see <a href="/whatsapp-automation-uae/">WhatsApp sales automation</a>.</p>
<p class="note">Sources: <a href="https://whatsappbusiness.com/policy/" target="_blank" rel="noopener">WhatsApp Business Messaging Policy</a>; Meta developer documentation on opt-in, template categorisation, messaging limits, per-user marketing limits, template quality and policy enforcement; English text of Cabinet Resolution No. 56 of 2024; Ministry of Economy summary (29 August 2024); <a href="https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws" target="_blank" rel="noopener">u.ae on data protection laws</a>; Khaleej Times (5 August 2026). Read 28 November 2026.</p>
""",
    faqs=[
        ("Is WhatsApp marketing legal in the UAE?", "Yes, with consent. Meta requires an opt-in that names your business, and UAE law requires consent to process personal data. The 2024 telemarketing resolution's definition also covers marketing messages through social media applications, so treat its rules as applying."),
        ("What counts as a valid WhatsApp opt-in?", "Meta says the opt-in must clearly state that the person agrees to receive messages from your business and must name the business. It can be collected anywhere, such as at checkout, in a form or in the chat, and doesn't have to mention WhatsApp specifically."),
        ("How many WhatsApp messages can I send per day?", "A new business portfolio can start conversations with 250 unique people in 24 hours. Verifying your business unlocks 2,000, and Meta raises the limit to 10,000, 100,000 and then unlimited as you use it with high-quality messages."),
        ("What time can I send marketing messages in the UAE?", "Cabinet Resolution No. 56 of 2024 limits marketing calls to 9am to 6pm. It doesn't spell out hours for messages, but keeping WhatsApp marketing in that window is the safe choice."),
        ("What happens if customers report my WhatsApp messages as spam?", "Your template and number quality drops, and Meta can pause templates, block sending for 1 to 30 days, lock the account or ban it permanently. Message only people who opted in, and make it easy to stop."),
    ],
    related=[("/whatsapp-automation-uae/", "WhatsApp sales automation, compliant by design"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing"), ("/guides/whatsapp-abandoned-cart-recovery/", "WhatsApp abandoned cart recovery")],
)

guide(
    slug="whatsapp-business-app-vs-api",
    title="WhatsApp Business App vs API: Which One in 2026? | Nuevo",
    desc="WhatsApp Business app vs the API in 2026: devices, broadcasts, automation, pricing, the blue tick, Meta One and coexistence (using both on one number).",
    h1="WhatsApp Business app vs WhatsApp Business API in 2026",
    card="What the free app does, what the API adds, what each costs, how the blue tick and Meta One work, and how coexistence lets you use both on one number.",
    lead="The free WhatsApp Business app is where most UAE businesses start. The WhatsApp Business Platform, usually called the API, is what you need to automate. Since 2025 you can even run both on the same number. Here is how to choose, with Meta's own limits as of November 2026.",
    answer="The WhatsApp Business app is free, runs on one phone plus up to four linked devices (ten with multi-agent), and has quick replies, greeting messages and broadcast lists of up to 256 people who must have saved your number. The WhatsApp Business API (Cloud API) has no inbox of its own, so you use it through a platform, but it allows unlimited agents, chatbots and AI, approved templates to anyone who opted in, and integrations, with Meta charging per message. Coexistence lets one number use both: the app for one-to-one chats, the API for automation. The free blue tick is available only on the API; Meta One sells a verified badge for the app.",
    body="""
<h2>Side by side</h2>
<div class="prose-table"><table>
<thead><tr><th></th><th>WhatsApp Business app</th><th>WhatsApp Business API</th></tr></thead>
<tbody>
<tr><td>Cost</td><td>Free; messages from the app are free</td><td>Meta charges per delivered message by category and country, plus your platform's fee</td></tr>
<tr><td>People and devices</td><td>One phone and up to 4 linked devices; up to 10 with multi-agent</td><td>As many agents as your platform allows</td></tr>
<tr><td>Reaching many customers</td><td>Broadcast lists of up to 256, only to people who saved your number; paid "business broadcasts" in some countries</td><td>Approved templates to anyone who opted in, within your messaging limit</td></tr>
<tr><td>Automation</td><td>Greeting and away messages, quick replies, Meta's business AI</td><td>Chatbots, AI assistants, follow-up sequences, store and CRM integrations</td></tr>
<tr><td>Inbox</td><td>The app itself</td><td>None built in: you use a platform or build one</td></tr>
<tr><td>Verification</td><td>Paid verified badge through Meta One</td><td>Free Official Business Account (blue tick) if eligible</td></tr>
</tbody></table></div>

<h2>When the free app is enough</h2>
<ul>
<li>One or two people answer every chat.</li>
<li>Fewer than a few dozen conversations a day.</li>
<li>You don't run ads that send people to WhatsApp at volume.</li>
<li>You don't need messages to go out automatically when someone abandons a cart or doesn't pay.</li>
</ul>
<p>Note that the app's linked devices sign out if the main phone is idle for more than 14 days, and linked devices can't create broadcast lists.</p>

<h2>When you need the API</h2>
<ul>
<li>You run <a href="/guides/click-to-whatsapp-ads/">click-to-WhatsApp ads</a> and chats arrive faster than people can answer.</li>
<li>You want an AI assistant replying in seconds, at night and in Arabic and English.</li>
<li>You want automatic follow-ups on carts, unpaid payment links and quiet leads.</li>
<li>You want sales from chats reported back to Meta to <a href="/guides/track-whatsapp-ad-sales/">measure real return on ad spend</a>.</li>
</ul>

<h2>What the API costs</h2>
<p>Since 1 July 2025 Meta charges per delivered message, priced by category (marketing, utility, authentication, service) and by the customer's country code. The UAE has its own rate card, billable in dirhams since 1 April 2026. Each number gets 1,000 free service messages a month, and chats that start from a click-to-WhatsApp ad are free for up to 7 days when you reply within 24 hours. Our <a href="/guides/whatsapp-business-api-pricing-uae/">API pricing guide</a> covers the details, and the <a href="/guides/whatsapp-chatbot-cost-uae/">chatbot cost guide</a> adds platform prices.</p>

<h2>Coexistence: the app and the API on one number</h2>
<p>Meta now lets a business connect its existing WhatsApp Business app number to the Cloud API through a partner, and keep using the app. Per Meta's documentation:</p>
<ul>
<li>You need app version 2.24.17 or later, and you onboard through a Meta partner.</li>
<li>Up to 180 days of one-to-one chat history is imported, and chats stay in sync between the app and the API.</li>
<li>Messages you send from the app stay free; API messages are charged at the normal rates.</li>
<li>Limits: throughput is fixed at 20 messages a second, broadcast lists become read-only, group chats don't sync, and up to 4 companion devices are supported.</li>
<li>If the main phone is inactive for about 14 days, the connection drops.</li>
</ul>
<p>This is what lets an AI assistant such as <a href="/m2s/">M2S</a> run on a brand's own number while the team keeps answering in the WhatsApp app they already use.</p>

<h2>The blue tick and Meta One</h2>
<ul>
<li><strong>Official Business Account</strong> (the free blue tick) is only for API numbers. Meta requires a verified business portfolio, at least 30 days on the platform, two-step verification and an approved display name. If refused, you can reapply after 30 days. One provider's documentation says it isn't available on coexistence numbers.</li>
<li><strong>Meta One</strong>, launched on 15 September 2026, is Meta's paid subscription that is absorbing Meta Verified. Its business plans include a verified badge on the WhatsApp Business app. Khaleej Times and Gulf News reported UAE prices from AED 46.99 a month for Essential and AED 119 for Advanced.</li>
</ul>
<p class="note">Sources: WhatsApp Help Center articles on linked devices, multi-agent and broadcast lists; Meta developer documentation on the Cloud API, pricing, coexistence onboarding and Official Business Accounts; Meta newsroom (3 April 2025 and 15 September 2026); Khaleej Times and Gulf News (September 2026). Read 28 November 2026.</p>
""",
    faqs=[
        ("Is the WhatsApp Business API free?", "No. Meta charges per delivered message, by category and country, and most businesses also pay a platform for the inbox and automation. Each number gets 1,000 free service messages a month, and chats from click-to-WhatsApp ads open a free window of up to 7 days."),
        ("Can I use the WhatsApp Business app and the API on the same number?", "Yes, through Meta's coexistence feature, set up via a Meta partner. You keep chatting in the app while the API handles automation; there are limits, such as read-only broadcast lists and 20 messages a second."),
        ("How many people can use one WhatsApp Business app account?", "One phone plus up to 4 linked devices, or up to 10 devices with multi-agent. The API has no such limit; it depends on your platform."),
        ("How do I get the green or blue tick on WhatsApp?", "The free Official Business Account badge is only for API numbers with a verified business, 30 days on the platform and two-step verification. App users can get a verified badge through a paid Meta One subscription."),
        ("Why can't my broadcast reach some customers?", "In the WhatsApp Business app, broadcasts only reach people who have saved your number, up to 256 per list. To reach everyone who opted in, you need API templates or the app's paid business broadcasts where available."),
    ],
    related=[("/whatsapp-automation-uae/", "WhatsApp Business API automation on your own number"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing"), ("/guides/whatsapp-marketing-rules-uae/", "WhatsApp marketing rules in the UAE")],
)


# ================================================================ batch 5 (28 Nov 2026)

guide(
    slug="whatsapp-green-tick-uae",
    title="How to Get the WhatsApp Green Tick in the UAE, 2026 | Nuevo",
    desc="How UAE businesses get verified on WhatsApp in 2026: the free Official Business Account badge on the API, and Meta One's paid verified badge for the app.",
    h1="How to get the WhatsApp green tick (verified badge) in the UAE",
    card="The two ways to a verified badge in 2026: Meta's free Official Business Account on the API, and the paid Meta One subscription for the Business app.",
    lead="The \"green tick\" is now a blue verified badge, and there are two ways to get one. Which applies depends on whether you use the WhatsApp Business app or the API. Here are Meta's requirements as of November 2026.",
    answer="In 2026 a UAE business can get a verified badge on WhatsApp in two ways. On the WhatsApp Business API, Meta's Official Business Account status is free: your business portfolio must be verified, the number must have been on the platform for at least 30 days, two-step verification must be on, your display name must be approved, and you must follow WhatsApp's policies; you request it in WhatsApp Manager and can reapply after 30 days if refused. On the free WhatsApp Business app, the verified badge comes with Meta One, Meta's paid subscription launched on 15 September 2026, which UAE press reported from AED 46.99 a month.",
    body="""
<h2>Green tick, blue tick: what changed</h2>
<p>WhatsApp used to show a green tick next to verified businesses. Meta has since moved to a blue verified badge across its apps. People in the UAE still search for the "WhatsApp green tick", but what you can apply for today is one of the two badges below.</p>

<h2>Option 1: Official Business Account (free, API only)</h2>
<p>If your number runs on the WhatsApp Business Platform (the API), you can request Official Business Account status at no cost. Meta's requirements:</p>
<ul>
<li>Your number complies with the WhatsApp Business Messaging Policy.</li>
<li>It has been registered on the platform for at least 30 days.</li>
<li>Your Meta business portfolio is verified.</li>
<li>Two-step verification is turned on for the number.</li>
<li>Your display name has been approved.</li>
</ul>
<p>To apply, open WhatsApp Manager, go to the phone number's profile and submit a request for an official business account. Meta doesn't grant it to employees' personal accounts, test accounts or numbers on the WhatsApp Business app. If you're refused, you can apply again after 30 days.</p>
<p>One provider's documentation says the badge isn't available on numbers using coexistence, where the same number runs on both the app and the API. If the badge matters to you, ask your provider before you connect.</p>

<h2>Option 2: Meta One (paid, works on the Business app)</h2>
<p>On 15 September 2026 Meta launched Meta One, a subscription that is absorbing Meta Verified. Its business plans include a verified badge on the WhatsApp Business app, a verified channel and impersonation protection once your business is verified, plus access to Meta's AI agent. Higher plans add more linked devices and business broadcast credits.</p>
<p>Khaleej Times and Gulf News reported these UAE prices for the business plans in September 2026: Essential from AED 46.99 a month, Advanced from AED 119, Expert from AED 359 and Max from AED 1,199. Meta says prices vary by region, and existing Meta Verified subscribers keep their plan for now.</p>

<h2>Which one should you get?</h2>
<ul>
<li><strong>You only use the free Business app:</strong> Meta One is the only route to a badge.</li>
<li><strong>You're on the API, or moving there to automate:</strong> apply for the free Official Business Account once you meet the 30-day and verification rules.</li>
<li><strong>Either way:</strong> verify your business in Meta Business Manager first. It's also what lifts your <a href="/guides/whatsapp-marketing-rules-uae/">messaging limit</a> from 250 to 2,000 people a day on the API.</li>
</ul>

<h2>Does the badge help you sell?</h2>
<p>It helps customers trust that they're talking to the real brand, which matters in a market with copycat accounts. It doesn't change Meta's message prices, your template approvals or your messaging limits. What sells is answering fast and well, which is what <a href="/m2s/">M2S</a> is built to do.</p>
<p class="note">Sources: Meta developer documentation on <a href="https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts" target="_blank" rel="noopener">Official Business Accounts</a>; Meta newsroom, "Introducing Meta One" (15 September 2026); WhatsApp Business page on Meta One; Khaleej Times (17 September 2026) and Gulf News (16 September 2026); 360dialog documentation on coexistence. Read 28 November 2026.</p>
""",
    faqs=[
        ("How do I get the green tick on WhatsApp in the UAE?", "WhatsApp now shows a blue verified badge. On the WhatsApp Business API, request a free Official Business Account in WhatsApp Manager once your business is verified, your number has been on the platform for 30 days and two-step verification is on. On the Business app, subscribe to Meta One."),
        ("Is the WhatsApp verified badge free?", "On the API, yes: the Official Business Account badge costs nothing if you meet Meta's requirements. On the WhatsApp Business app, the badge comes with a paid Meta One plan, reported from AED 46.99 a month in the UAE."),
        ("Do I need to be a famous brand to get verified?", "Meta's current Official Business Account requirements are a verified business portfolio, 30 days on the platform, two-step verification, an approved display name and policy compliance. Its documentation doesn't list a separate notability test."),
        ("What happens if my request is rejected?", "You can submit a new request after 30 days. Use the time to complete business verification and make sure your display name matches your business."),
        ("Does a verified badge increase my WhatsApp messaging limit?", "No. Messaging limits depend on business verification and message quality. Verifying your business, which you need for the badge anyway, is what raises the limit from 250 to 2,000."),
    ],
    related=[("/guides/whatsapp-business-app-vs-api/", "WhatsApp Business app vs API"), ("/guides/whatsapp-marketing-rules-uae/", "WhatsApp marketing rules in the UAE"), ("/whatsapp-automation-uae/", "WhatsApp automation on your own number")],
)

guide(
    slug="bulk-whatsapp-messages-uae",
    title="How to Send Bulk WhatsApp Messages in the UAE, 2026 | Nuevo",
    desc="How to send bulk WhatsApp messages in the UAE legally in 2026: broadcast lists, business broadcasts, API templates, limits, costs and consent rules.",
    h1="How to send bulk WhatsApp messages in the UAE, the legal way",
    card="Broadcast lists, paid business broadcasts and API templates compared, with Meta's limits, the cost per message and the consent rules that keep your number safe.",
    lead="Sending one message to hundreds of customers is easy to do badly. Unofficial \"bulk sender\" tools get numbers banned, and messages to people who never opted in break both Meta's rules and UAE law. Here are the three legitimate ways to do it in 2026.",
    answer="There are three legitimate ways to send bulk WhatsApp messages in the UAE. The free WhatsApp Business app has broadcast lists of up to 256 contacts, which only reach people who saved your number. The app also offers paid business broadcasts that reach customers who haven't saved it, in the countries where Meta offers them. For larger volumes, the WhatsApp Business API sends Meta-approved marketing templates to anyone who opted in, starting at 250 people a day for a new account and rising to 2,000 after business verification, with Meta charging per delivered message. Every method needs the customer's opt-in, and you must stop messaging anyone who asks.",
    body="""
<h2>Method 1: broadcast lists in the Business app (free)</h2>
<ul>
<li>Up to 256 contacts per list.</li>
<li>Only people who saved your number in their phone receive it. Everyone else silently misses it.</li>
<li>Each person gets it as a private message, and replies come back to you one to one.</li>
<li>Linked devices can't create broadcast lists; you need the main phone.</li>
</ul>
<p>Fine for a small store with loyal customers. Not a way to reach new leads from ads, most of whom won't have saved your number.</p>

<h2>Method 2: business broadcasts in the app (paid)</h2>
<p>Since April 2025 Meta has offered paid business broadcasts in the WhatsApp Business app. They reach customers even if they haven't saved your number, and you pay per message delivered, at a rate set by the customer's country. Meta says the feature is only available in limited countries, and we couldn't confirm UAE availability in November 2026, so check in your app under the broadcast tools.</p>

<h2>Method 3: marketing templates on the WhatsApp Business API</h2>
<p>This is how brands send to thousands of customers. You write a template, Meta approves it, and your platform sends it to your opted-in list.</p>
<div class="prose-table"><table>
<thead><tr><th>What</th><th>The rule in 2026</th></tr></thead>
<tbody>
<tr><td>Daily reach</td><td>250 unique people in 24 hours for a new business portfolio; 2,000 once your business is verified; then 10,000, 100,000 and unlimited as Meta scales you up</td></tr>
<tr><td>Speed</td><td>80 messages a second per number by default</td></tr>
<tr><td>Cost</td><td>Meta charges per delivered marketing message at the UAE rate, plus your platform's fee</td></tr>
<tr><td>Who you can message</td><td>Only people who opted in to messages from your business</td></tr>
<tr><td>Per-person caps</td><td>Meta may hold back marketing messages to people who rarely engage (error 131049)</td></tr>
</tbody></table></div>
<p>See our guides to <a href="/guides/whatsapp-business-api-pricing-uae/">API pricing</a> and <a href="/guides/wati-alternatives/">platforms</a>.</p>

<h2>Avoid unofficial bulk senders</h2>
<p>Tools that automate the normal WhatsApp app or WhatsApp Web to blast messages break WhatsApp's terms. Numbers used this way are regularly restricted or banned, and you lose the number and its chat history. Use the app's own broadcast tools or the official API.</p>

<h2>The consent rules</h2>
<ul>
<li><strong>Meta:</strong> the customer must have opted in to messages from your business, with your business named. You must honour opt-outs made on or off WhatsApp.</li>
<li><strong>UAE telemarketing rules:</strong> Cabinet Resolution No. 56 of 2024 defines telemarketing to include marketing messages through social media applications, bans contacting numbers on the Do Not Call Register, and allows marketing calls only from 9am to 6pm. Applying the same discipline to WhatsApp is the safe reading.</li>
<li><strong>UAE data protection law:</strong> processing personal data needs consent, with listed exceptions.</li>
</ul>
<p>The full picture is in our <a href="/guides/whatsapp-marketing-rules-uae/">WhatsApp marketing rules guide</a>.</p>

<h2>How to get replies, not blocks</h2>
<ol>
<li>Segment: send the restock message only to people who bought that product.</li>
<li>Lead with something useful, not "Dear customer".</li>
<li>One clear action per message, with a button.</li>
<li>Add an opt-out button and respect it automatically.</li>
<li>Have someone, or an AI, ready to answer the replies within minutes. A broadcast that gets questions and no answers wastes the send.</li>
</ol>
<p class="note">Sources: WhatsApp Help Center articles on broadcast lists and business broadcasts; Meta newsroom (3 April 2025); Meta developer documentation on messaging limits, per-user marketing limits and the Cloud API; WhatsApp Business Messaging Policy; English text of Cabinet Resolution No. 56 of 2024. Read 28 November 2026.</p>
""",
    faqs=[
        ("How many people can I send a WhatsApp broadcast to?", "In the WhatsApp Business app, up to 256 contacts per broadcast list, and only those who saved your number receive it. On the API, a new account can reach 250 people a day, rising to 2,000 after business verification and higher as Meta scales you."),
        ("Is bulk WhatsApp messaging legal in the UAE?", "Yes, to people who opted in, through WhatsApp's own tools or the official API. UAE telemarketing rules cover marketing messages through social media applications, and data protection law requires consent, so never message bought or scraped lists."),
        ("Why didn't some people receive my broadcast?", "In the Business app, broadcasts only reach contacts who saved your number. On the API, Meta may hold back marketing messages to people who rarely engage, which shows as error 131049."),
        ("How much does it cost to send bulk WhatsApp messages?", "Broadcast lists in the Business app are free. Business broadcasts in the app and marketing templates on the API are charged per delivered message at a rate for the customer's country, plus any platform fee for the API."),
        ("Will my number get banned for sending bulk messages?", "Not if you use official tools and message only people who opted in. Numbers get restricted when many recipients block or report them, or when unofficial bulk-sending tools are used."),
    ],
    related=[("/guides/whatsapp-marketing-rules-uae/", "WhatsApp marketing rules in the UAE"), ("/guides/whatsapp-business-app-vs-api/", "WhatsApp Business app vs API"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing")],
)


# ================================================================ batch 6 (28 Nov 2026)

guide(
    slug="instagram-dm-automation-rules",
    title="Instagram DM Automation Rules and Limits, 2026 | Nuevo",
    desc="Meta's rules for automating Instagram DMs in 2026: the 24-hour window, the human agent tag, comment-to-DM private replies, rate limits and click-to-Direct ads.",
    h1="Instagram DM automation: Meta's rules and limits in 2026",
    card="The 24-hour window, the 7-day human agent tag, comment-to-DM replies, rate limits, and how Instagram DMs compare with WhatsApp for selling.",
    lead="Automated Instagram DMs can answer every comment and story reply in seconds, but Meta sets firm rules on when and how a business can message. Here they are, from Meta's developer documentation as of November 2026.",
    answer="Automating Instagram DMs needs an Instagram professional account connected to a tool on Meta's Instagram messaging API, and the customer has to message first. You can reply freely, including with offers, for 24 hours after the customer's last message, or up to 7 days after their first message when the chat started from a click-to-Instagram-Direct ad. After that, a person can reply for up to 7 days using the human agent tag, but not with promotional content. A comment can get one private reply within 7 days. Bots must offer a way to reach a human and must not spam.",
    body="""
<h2>What you need to automate Instagram DMs</h2>
<ul>
<li>An Instagram professional account (business or creator).</li>
<li>A tool connected through Meta's Instagram messaging API, with the permission to manage messages. Tools that serve many businesses need Meta's advanced access.</li>
<li>The customer must start the conversation: a DM, a story reply, a comment you reply to privately, or a tap on an ad. Group chats aren't supported.</li>
</ul>

<h2>The messaging windows</h2>
<div class="prose-table"><table>
<thead><tr><th>Window</th><th>How long</th><th>What you can send</th></tr></thead>
<tbody>
<tr><td>Standard</td><td>24 hours after the customer's last message</td><td>Anything, including promotional messages</td></tr>
<tr><td>Click-to-Instagram-Direct ad</td><td>Up to 7 days from the customer's first message</td><td>Anything, including promotional messages</td></tr>
<tr><td>Human agent tag</td><td>Up to 7 days after the customer's last message</td><td>Manual replies from a person to a support issue; no promotions</td></tr>
</tbody></table></div>
<p>The human agent tag needs Meta's app review and business verification, and it's meant for issues that couldn't be solved within 24 hours. Message tags can't carry promotional content.</p>

<h2>Comment-to-DM (private replies)</h2>
<p>The popular "comment PRICE and we'll DM you" campaigns use private replies. Meta allows <strong>one private reply per comment, within 7 days of the comment</strong>. On a live broadcast, only while it's live. If the person answers, the normal 24-hour window opens.</p>

<h2>Rate limits and inbox features</h2>
<ul>
<li>Text messages: 300 API calls per second per account; audio and video: 10 per second. Private replies: 750 an hour on posts and reels.</li>
<li>Ice breakers (suggested first questions): up to 4. Quick reply buttons: up to 13, 20 characters each. Neither shows on desktop.</li>
<li>Story mentions reach your tool only if the mentioning account is public, or private and following you.</li>
</ul>
<p>The "200 automated DMs an hour" figure you may see quoted comes from third-party tool blogs, not from Meta's documentation.</p>

<h2>Meta's policy on bots</h2>
<ul>
<li>Tell people they're talking to an automated assistant where the law requires it.</li>
<li>Always offer a way to reach a person.</li>
<li>Don't send or engage at very high frequency; Meta's spam rules cover automated activity too.</li>
</ul>

<h2>Instagram DMs or WhatsApp for selling?</h2>
<div class="prose-table"><table>
<thead><tr><th></th><th>Instagram DMs</th><th>WhatsApp Business API</th></tr></thead>
<tbody>
<tr><td>Message fees</td><td>None per message</td><td>Meta charges per delivered message</td></tr>
<tr><td>Follow up after the window closes</td><td>Not for sales; only a person, for support, within 7 days</td><td>Yes, with approved paid templates to anyone who opted in</td></tr>
<tr><td>After an ad click</td><td>Up to 7 days to reply freely</td><td>Free entry point window of up to 7 days</td></tr>
<tr><td>Payments and orders</td><td>Send a payment link</td><td>Send a payment link; order and shipping updates as templates</td></tr>
</tbody></table></div>
<p>For a supplement brand the deciding factor is usually follow-up: buyers who go quiet on Instagram can't be reminded once the window closes, while on WhatsApp they can. Many brands use Instagram to start the conversation and move serious buyers to WhatsApp. See <a href="/instagram-dm-automation-dubai/">how we run Instagram ads and DMs</a> and our <a href="/guides/click-to-whatsapp-ads/">click-to-WhatsApp ads guide</a>.</p>
<p class="note">Sources: Meta developer documentation for the Instagram Platform (messaging API, private replies, human agent tag, rate limits, ice breakers, quick replies, webhooks) and Meta's community standards on spam. Read 28 November 2026.</p>
""",
    faqs=[
        ("Is it allowed to automate Instagram DMs?", "Yes, through Meta's Instagram messaging API and the tools built on it, as long as the customer messages first, you reply inside Meta's windows, you offer a way to reach a person and you don't spam."),
        ("How long can I reply to an Instagram DM?", "Freely for 24 hours after the customer's last message, or up to 7 days after their first message if the chat came from a click-to-Instagram-Direct ad. A person can reply to a support issue for up to 7 days with the human agent tag, without promotions."),
        ("How does comment-to-DM work on Instagram?", "When someone comments on your post or reel, your tool can send one private reply to that comment within 7 days. If they reply, a normal 24-hour conversation window opens."),
        ("Is there a limit on automated Instagram DMs per hour?", "Meta's documentation sets API rate limits, such as 300 text messages per second per account and 750 private replies an hour on posts and reels. The often-quoted 200 DMs an hour isn't in Meta's documentation."),
        ("Should I sell on Instagram DMs or WhatsApp?", "Instagram has no message fees but no way to follow up for sales after the window closes. WhatsApp charges per message but lets you re-engage opted-in customers with templates. Many brands start on Instagram and close on WhatsApp."),
    ],
    related=[("/instagram-dm-automation-dubai/", "Instagram ads and DM automation"), ("/guides/manychat-pricing/", "ManyChat pricing in 2026"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads")],
)

guide(
    slug="manychat-pricing",
    title="ManyChat Pricing 2026 for UAE Brands, Plans Explained | Nuevo",
    desc="ManyChat's 2026 plans explained: Free, Essential, Pro, Business and Advanced, active contact limits, WhatsApp costs, and how it compares with WhatsApp tools.",
    h1="ManyChat pricing in 2026, and when a UAE brand needs more",
    card="ManyChat's five plans since March 2026, how active contacts drive the bill, what WhatsApp costs on top, and how it compares with WhatsApp-first platforms.",
    lead="ManyChat is the default tool for Instagram DM automation, and it changed its pricing in March 2026. Here is what each plan includes, how the bill grows, and what changes when you add WhatsApp, from ManyChat's own pages on 28 November 2026.",
    answer="Since 2 March 2026 ManyChat has five plans: Free (25 active contacts a month, 1 user), Essential at $17 a month or $14 billed annually (250 contacts, 2 users), Pro at $39 or $29 annually (2,500 contacts, 3 users), Business at $99 or $69 annually (7,500 contacts, 5 users) and Advanced at $199 or $139 annually (25,000 contacts, 10 users). An active contact is anyone you message or who messages you in a month, and extra contacts are charged per contact. Instagram, Messenger, TikTok and Telegram are on every plan; WhatsApp, SMS, email and AI features start on Pro. ManyChat says it adds no markup to Meta's WhatsApp message fees.",
    body="""
<h2>The plans</h2>
<div class="prose-table"><table>
<thead><tr><th>Plan</th><th>Monthly</th><th>Billed annually (per month)</th><th>Active contacts a month</th><th>Users</th></tr></thead>
<tbody>
<tr><td>Free</td><td>$0</td><td>n/a</td><td>25</td><td>1</td></tr>
<tr><td>Essential</td><td>$17</td><td>$14</td><td>250</td><td>2</td></tr>
<tr><td>Pro</td><td>$39</td><td>$29</td><td>2,500</td><td>3</td></tr>
<tr><td>Business</td><td>$99</td><td>$69</td><td>7,500</td><td>5</td></tr>
<tr><td>Advanced</td><td>$199</td><td>$139</td><td>25,000</td><td>10</td></tr>
</tbody></table></div>
<p>The old Pro and Elite plans and the separate AI add-on were replaced in this model; accounts on older plans may still see them.</p>

<h2>How the bill grows: active contacts</h2>
<p>ManyChat counts an <strong>active contact</strong> as anyone you message or who messages you in a month. Go over your plan's allowance and each extra contact is charged: $0.10 on Essential, $0.05 on Pro, $0.025 on Business and $0.004 on Advanced on monthly billing, a little less on annual. Extra inbox seats cost $25 each. A brand running comment-to-DM campaigns can pass a plan's allowance quickly, so estimate contacts, not just messages.</p>

<h2>Channels and AI by plan</h2>
<ul>
<li><strong>Every plan:</strong> Instagram, Facebook Messenger, TikTok and Telegram.</li>
<li><strong>Pro and above:</strong> WhatsApp, SMS, email, broadcasts and ManyChat's AI features, which are now included rather than sold as an add-on.</li>
</ul>

<h2>Adding WhatsApp to ManyChat</h2>
<ul>
<li>WhatsApp needs a paid plan from Pro up. You can connect your own number or buy one through ManyChat, and keeping the WhatsApp Business app on the same number is supported.</li>
<li>Meta's message fees are paid on top, from a ManyChat wallet. ManyChat says it adds no markup to Meta's rates.</li>
<li>ManyChat must be the only billing method on the WhatsApp account, or templates won't send.</li>
<li>ManyChat lists marketing and utility templates; we didn't find authentication templates in its documentation.</li>
</ul>
<p>Meta's WhatsApp rules apply in full, including charges for service replies beyond 1,000 a month per number from 1 October 2026. See our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp API pricing guide</a>.</p>

<h2>ManyChat or a WhatsApp-first platform?</h2>
<ul>
<li><strong>Instagram is your main sales channel:</strong> ManyChat is built around Instagram and Messenger flows, and it's hard to beat on price for comment-to-DM and story automations.</li>
<li><strong>WhatsApp is your main sales channel:</strong> WhatsApp-first platforms such as Wati, Respond.io, SleekFlow or Gallabox put more into the team inbox, templates and WhatsApp reporting. Compare them in our <a href="/guides/wati-alternatives/">Wati alternatives guide</a>.</li>
<li><strong>Either way:</strong> the tool doesn't write the answers, run the ads or follow up for you. That's the part <a href="/m2s/">M2S</a> covers.</li>
</ul>
<p class="note">Sources: ManyChat's pricing page and help center articles on plans, active contacts, WhatsApp setup and WhatsApp pricing, read 28 November 2026; Meta's WhatsApp pricing documentation. Nuevo Automations isn't affiliated with ManyChat.</p>
""",
    faqs=[
        ("How much does ManyChat cost in 2026?", "ManyChat has a free plan for 25 active contacts a month. Paid plans are Essential at $17 a month ($14 annually), Pro at $39 ($29), Business at $99 ($69) and Advanced at $199 ($139), with more contacts and users at each step."),
        ("What is an active contact in ManyChat?", "Anyone you message or who messages you in a given month. Each plan includes a number of active contacts, and extra ones are charged per contact, from $0.10 on Essential down to $0.004 on Advanced."),
        ("Does ManyChat support WhatsApp?", "Yes, from the Pro plan up. You connect your own number or buy one through ManyChat and pay Meta's message fees from a ManyChat wallet; ManyChat says it doesn't mark them up."),
        ("Is ManyChat's AI free?", "In the plans introduced in March 2026, ManyChat's AI features are included from the Pro plan up instead of being sold as a separate add-on."),
        ("Is ManyChat good for UAE businesses?", "For Instagram-led selling, yes: comment-to-DM and story automations are its strength. If WhatsApp is where you close sales, compare WhatsApp-first platforms with stronger team inboxes and template tools."),
    ],
    related=[("/guides/instagram-dm-automation-rules/", "Instagram DM automation rules"), ("/guides/wati-alternatives/", "Wati alternatives compared"), ("/instagram-dm-automation-dubai/", "Instagram ads and DM automation")],
)


# ================================================================ batch 7 (28 Nov 2026)

guide(
    slug="meta-business-ai-whatsapp",
    title="Meta Business AI on WhatsApp vs a Custom AI Assistant | Nuevo",
    desc="Meta's own AI agent for WhatsApp Business in 2026: what it does, what it costs, which businesses are excluded, and when a custom AI sales assistant fits better.",
    h1="Meta's AI agent for WhatsApp Business vs a custom AI assistant",
    card="What Meta Business Agent does, its price per token, the industries it excludes (including health), its limits, and when a custom assistant is the better choice.",
    lead="Meta now offers its own AI agent that answers your customers on WhatsApp. For many small businesses it's a quick start. For a supplement or wellness brand, there are important limits. Here is what Meta's documentation says as of November 2026.",
    answer="Meta Business Agent, announced on 3 June 2026, is Meta's own AI that answers customers on WhatsApp, Messenger and Instagram using your Facebook Page, website, catalogue, FAQs and past chats, and hands complex cases to a person. On the WhatsApp Business app it is set up under Tools; on the API it costs US$2.00 per million tokens, about 4 to 5 US cents a message by Meta's estimate. Meta's developer documentation excludes Finance, Government, Health, Alcohol, Gambling, over-the-counter drugs and matrimony services. It only replies within 24 hours of a customer's message, can't start conversations, and you can't set when it hands off to a person.",
    body="""
<h2>What Meta Business Agent does</h2>
<ul>
<li>Answers questions, recommends products from your catalogue, books appointments, qualifies leads and hands off to a person.</li>
<li>Learns from your Facebook Page posts, past WhatsApp chats, your website, catalogues and price lists, FAQs and documents you add.</li>
<li>In the WhatsApp Business app you can choose who it answers (everyone, only new customers, or customers from ads), set its tone and test it as a customer.</li>
</ul>
<p>Meta says over a million businesses already use it across WhatsApp and Messenger. Access is rolling out to selected businesses and markets, with a waitlist, and Meta doesn't publish the list of countries.</p>

<h2>What it costs</h2>
<ul>
<li><strong>On the WhatsApp Business API:</strong> US$2.00 per million tokens since 1 August 2026, one global rate that covers the AI and delivery. Meta estimates 20,000 to 25,000 tokens, about 4 to 5 US cents, for a typical message; a simple enquiry of four messages around 16 to 20 cents. There are no free messages, and tokens are charged even inside the free window after a click-to-WhatsApp ad.</li>
<li><strong>On the WhatsApp Business app:</strong> it comes with Meta's paid Meta One plans, reported in the UAE from AED 46.99 a month. Meta doesn't publish how many AI replies each plan includes.</li>
</ul>

<h2>Who can't use it</h2>
<p>Meta's developer documentation states that all business categories are supported "except Finance, Government, Health, Alcohol, Gambling, over-the-counter drugs, and matrimony services". Supplements aren't named either way, so whether a supplement or wellness brand qualifies depends on how Meta classifies the business. On the API, Meta's eligibility check for your number is the only definite answer.</p>

<h2>Its limits</h2>
<ul>
<li>It only replies within 24 hours of the customer's last message. It can't start conversations, so it can't chase an abandoned cart or an unpaid link a day later.</li>
<li>You can't set the rules for handing a chat to a person; Meta decides.</li>
<li>It can't read videos, PDFs or Office files, and re-reads websites periodically rather than live.</li>
<li>Meta doesn't publish a language list and says English gives the best quality. We found no confirmation of Arabic support.</li>
<li>One AI agent per number: you can't run Meta's and another AI on the same number.</li>
<li>It doesn't take payments itself; that only works through systems you connect.</li>
</ul>

<h2>When a custom AI sales assistant fits better</h2>
<div class="prose-table"><table>
<thead><tr><th></th><th>Meta Business Agent</th><th>Custom assistant (such as M2S)</th></tr></thead>
<tbody>
<tr><td>Setup</td><td>Quick, inside Meta's tools</td><td>Built and tested on your catalogue and policies</td></tr>
<tr><td>Health and supplement brands</td><td>Health and OTC drugs excluded; supplements unclear</td><td>Built for them, with rules on what it may and may not claim</td></tr>
<tr><td>Follow-ups</td><td>Replies only; can't start conversations</td><td>Template follow-ups on carts, unpaid links and quiet leads</td></tr>
<tr><td>Hand-off rules</td><td>Decided by Meta</td><td>Set by you: price questions, complaints, large orders</td></tr>
<tr><td>Arabic</td><td>Not documented</td><td>Tested with your customers' own messages</td></tr>
<tr><td>Reporting</td><td>Meta's insights</td><td>Sales by ad, sent back to Meta's Conversions API</td></tr>
</tbody></table></div>
<p>If you're a small business answering simple questions, try Meta's agent first; it's quick and cheap. If you sell health or wellness products, need follow-ups that bring back silent buyers, or need sales reported by ad, a custom assistant is the safer route. See <a href="/m2s/">how M2S works</a> or <a href="/ai-chatbot-development-uae/">how we build the assistant</a>.</p>
<p class="note">Sources: Meta newsroom, "Meta Business Agent" (3 June 2026); Meta developer documentation for Meta Business Agent (overview, requirements) and WhatsApp pricing for non-template messages; WhatsApp Business page on the business AI agent; Khaleej Times (17 September 2026). Read 28 November 2026.</p>
""",
    faqs=[
        ("What is Meta Business Agent on WhatsApp?", "Meta's own AI that answers customers on WhatsApp, Messenger and Instagram for a business, using its Page, website, catalogue, FAQs and past chats, and passes complex cases to a person. Meta announced it on 3 June 2026."),
        ("How much does Meta's WhatsApp AI cost?", "On the WhatsApp Business API it costs US$2.00 per million tokens, which Meta estimates at about 4 to 5 US cents per message. On the WhatsApp Business app it comes with paid Meta One plans."),
        ("Can supplement or health brands use Meta Business Agent?", "Meta's documentation excludes Health and over-the-counter drug businesses, among others. Supplements aren't named, so a supplement brand should run Meta's eligibility check for its number before relying on it."),
        ("Can Meta's AI follow up with customers who stopped replying?", "No. It only replies within 24 hours of the customer's last message and can't start conversations, so cart and payment follow-ups need approved templates sent by your own system."),
        ("Does Meta Business Agent reply in Arabic?", "Meta doesn't publish a list of supported languages and says quality is best in English. Test it with real Arabic messages from your customers before relying on it."),
    ],
    related=[("/ai-chatbot-development-uae/", "How we build an AI sales assistant"), ("/guides/arabic-whatsapp-chatbot/", "Arabic WhatsApp chatbots"), ("/guides/whatsapp-chatbot-cost-uae/", "WhatsApp chatbot cost in the UAE")],
)

guide(
    slug="whatsapp-flows",
    title="WhatsApp Flows Explained: In-Chat Forms for UAE Brands | Nuevo",
    desc="What WhatsApp Flows are, how businesses use them for lead forms, bookings and product choice, how they're sent, device support, limits and costs in 2026.",
    h1="WhatsApp Flows: forms and screens inside the chat",
    card="In-chat forms for leads, bookings and product choice: how Flows are sent, which phones support them, Meta's limits and what they cost.",
    lead="WhatsApp Flows let a customer fill in a form, pick a date or choose a product without leaving the chat. Here is how they work on the WhatsApp Business Platform in 2026, and where they help a UAE brand sell.",
    answer="WhatsApp Flows are forms and screens that open inside a WhatsApp chat, with text fields, dropdowns, date pickers and file uploads, and they can pull live data such as available slots from your system. A business sends a Flow either as a Meta-approved template with a Flow button, which needs a verified business and good message quality, or as an interactive message after the customer writes in. Flows work on Android 6.0 and iOS 12 or later, not on WhatsApp Web. They are part of the WhatsApp Business API; we found no separate Flow fee, so you pay for the message that carries it.",
    body="""
<h2>What a Flow looks like</h2>
<p>The customer taps a button in the chat and a screen opens over it, like a small app: fields to fill, options to pick, a date to choose. When they submit, the answers come back to your system and the chat continues. Meta lists lead capture, offers, quotes and appointment booking as typical uses, and publishes a case study that reports 2.6 times more appointments.</p>

<h2>How Flows are sent</h2>
<ul>
<li><strong>As a template with a Flow button:</strong> for starting a conversation, for example after a lead form or a purchase. Needs an approved template, a verified business and good message quality.</li>
<li><strong>As an interactive message:</strong> inside an open conversation, for example when a customer asks to book.</li>
</ul>

<h2>Limits to plan around</h2>
<ul>
<li>Phones only: Android 6.0+ and iOS 12+. Customers on WhatsApp Web or desktop can't open them.</li>
<li>Meta recommends no more than 3 screens in a sub-flow; long forms lose people.</li>
<li>Customers can upload up to 10 files, 100 MiB in total.</li>
<li>Flows are a WhatsApp Business API feature; we found no documentation of them in the free WhatsApp Business app.</li>
</ul>
<p>You may see "10 screens" quoted as a limit; that's one provider's own limit, not Meta's.</p>

<h2>Where Flows help a wellness or supplement brand</h2>
<ul>
<li><strong>Product finder:</strong> three quick questions (goal, age group, preference) and the assistant recommends the right product.</li>
<li><strong>Consultation booking:</strong> pick a date and time for a call with a nutritionist or the brand's team.</li>
<li><strong>Delivery details:</strong> collect area, building and preferred delivery time in one screen instead of five messages.</li>
<li><strong>Subscription sign-up:</strong> choose the product, quantity and frequency for a monthly refill.</li>
</ul>
<p>A good AI assistant does much of this in plain conversation too. Flows earn their place where a structured answer matters, such as an address or a booking slot.</p>

<h2>What Flows cost</h2>
<p>We found no Flow-specific fee in Meta's documentation. A Flow travels in a message, so you pay what that message costs: a marketing or utility template if you start the conversation, a service message inside an open window. See our <a href="/guides/whatsapp-business-api-pricing-uae/">WhatsApp API pricing guide</a>.</p>
<p class="note">Sources: Meta developer documentation for WhatsApp Flows (overview, sending Flows, components, limits) and Meta's Flows business page and case study. Read 28 November 2026.</p>
""",
    faqs=[
        ("What are WhatsApp Flows?", "Forms and screens that open inside a WhatsApp chat, with fields, dropdowns, date pickers and file uploads, so customers can book, sign up or choose products without leaving WhatsApp."),
        ("Do WhatsApp Flows cost extra?", "We found no Flow-specific fee in Meta's documentation. You pay for the message that carries the Flow, at Meta's normal per-message rates."),
        ("Can I use WhatsApp Flows in the WhatsApp Business app?", "Flows are a WhatsApp Business API feature. We found no documentation of them in the free WhatsApp Business app."),
        ("Do WhatsApp Flows work on desktop?", "No. Flows open on Android 6.0 or later and iOS 12 or later; customers on WhatsApp Web or desktop can't use them."),
        ("What can I build with WhatsApp Flows?", "Meta lists lead capture, offers, quotes and appointment booking. Brands also use them for product finders, delivery details and subscription sign-ups."),
    ],
    related=[("/guides/whatsapp-business-app-vs-api/", "WhatsApp Business app vs API"), ("/ai-receptionist-uae/", "AI receptionist and bookings"), ("/guides/whatsapp-business-api-pricing-uae/", "WhatsApp Business API pricing")],
)

guide(
    slug="cash-on-delivery-whatsapp-confirmation-uae",
    title="Cash on Delivery Confirmation on WhatsApp, UAE | Nuevo",
    desc="How UAE online stores confirm cash on delivery orders on WhatsApp in 2026: the utility template rules, a simple confirmation flow, and moving buyers to prepaid.",
    h1="Confirming cash on delivery orders on WhatsApp in the UAE",
    card="How to confirm COD orders by WhatsApp without breaking Meta's template rules, what the data says about COD in the region, and how to move buyers to prepaid.",
    lead="Cash on delivery is shrinking in the UAE but hasn't gone away, and unconfirmed COD orders are a classic source of failed deliveries. A short WhatsApp confirmation before dispatch is one of the simplest fixes. Here is how to do it within Meta's rules.",
    answer="To confirm cash on delivery orders on WhatsApp, send an approved utility template right after the order with the order number, items, total and delivery address, and buttons to confirm or change the order. Meta counts it as a utility message only if it contains no promotion; adding an offer or upsell makes it marketing, and Meta relabels such templates automatically. Checkout.com reported that cash on delivery preference in the region fell from 41% in 2020 to 20% in 2023, and as low as 10% in the UAE, Saudi Arabia and Kuwait, so a confirmation message is also a good moment to offer a payment link.",
    body="""
<h2>Why confirm COD orders at all</h2>
<p>A cash on delivery order costs you the delivery whether or not the customer pays at the door. Orders placed by mistake, duplicates, wrong addresses and buyers who changed their mind all show up as failed deliveries. Asking the customer to confirm in WhatsApp before you dispatch catches most of these, and the customer gets a chance to fix the address.</p>

<h2>What the data says about COD in the region</h2>
<ul>
<li>Checkout.com reported in 2024 that cash on delivery preference across the region fell from 41% in 2020 to 20% in 2023, and to as low as 10% in the UAE, Saudi Arabia and Kuwait.</li>
<li>Its 2025 report, as covered by Khaleej Times, said COD usage had fallen 53% since 2020.</li>
<li>EZDubai and Euromonitor put UAE e-commerce at AED 42.2 billion in 2025, about 15.7% of retail, as reported by WAM.</li>
</ul>
<p>We found no reliable published figure for COD return rates in the UAE, so we don't quote one.</p>

<h2>Stay inside Meta's utility rules</h2>
<ul>
<li>An order confirmation is a <strong>utility</strong> template only if it is about the order and nothing else.</li>
<li>Add a discount, "you may also like" or any promotion and it becomes <strong>marketing</strong>, priced as marketing and subject to marketing consent. Meta relabels misfiled templates automatically, and repeat misuse leads to restrictions.</li>
<li>Since 1 October 2026 utility templates are charged even inside an open conversation window, so keep it to one confirmation message.</li>
</ul>

<h2>A simple confirmation flow</h2>
<ol>
<li><strong>Order placed:</strong> a utility template with the order number, items, total including VAT, delivery area and expected date, and two buttons: Confirm order, Change something.</li>
<li><strong>Customer taps Confirm:</strong> a 24-hour conversation window is now open. Reply with a thank-you and, if you like, a payment link for those who would rather pay now.</li>
<li><strong>Customer taps Change:</strong> your team or AI assistant fixes the address or quantity in the chat.</li>
<li><strong>No reply after a few hours:</strong> one reminder, then a call or hold the order, whichever your logistics prefer.</li>
<li><strong>Dispatched:</strong> a second utility template with the tracking link.</li>
</ol>

<h2>Moving buyers from COD to prepaid</h2>
<p>Once the customer replies, you're inside the conversation window and can offer a <a href="/guides/whatsapp-payment-links-uae/">payment link</a>, including buy now, pay later options where your provider supports them. Keep it optional: buyers who prefer cash will still say yes to the order.</p>
<p>On Shopify, apps such as Interakt and SuperLemon list COD confirmation among their features; see our <a href="/guides/shopify-whatsapp-integration/">Shopify WhatsApp guide</a>.</p>
<p class="note">Sources: Meta's WhatsApp template categorisation guidelines and pricing documentation; Checkout.com (2024 MENA consumer research release); Khaleej Times on Checkout.com's 2025 report; WAM and Zawya on the EZDubai and Euromonitor e-commerce report. Read 28 November 2026.</p>
""",
    faqs=[
        ("Is a COD confirmation message on WhatsApp utility or marketing?", "Utility, if it only covers the order: number, items, total, address and confirm or change buttons. Add any offer or upsell and Meta treats it as marketing."),
        ("How common is cash on delivery in the UAE now?", "Falling. Checkout.com reported that cash on delivery preference was as low as 10% in the UAE, Saudi Arabia and Kuwait in 2023, down from much higher levels in 2020."),
        ("Can I ask COD customers to pay online instead?", "Yes. Once the customer replies to the confirmation, a 24-hour conversation window opens and you can send a payment link, keeping cash on delivery as an option."),
        ("How much does a WhatsApp COD confirmation cost?", "Meta charges the utility rate for the customer's country for each delivered template. Since 1 October 2026 utility templates are charged even inside an open conversation window."),
        ("Can a Shopify store automate COD confirmation on WhatsApp?", "Yes. Several Shopify WhatsApp apps, including Interakt and SuperLemon, list cash on delivery confirmation among their features."),
    ],
    related=[("/guides/whatsapp-payment-links-uae/", "Taking payments on WhatsApp"), ("/guides/shopify-whatsapp-integration/", "Shopify WhatsApp integration"), ("/ecommerce-automation-uae/", "WhatsApp sales for online stores")],
)


# ================================================================ batch 8 (28 Nov 2026)

guide(
    slug="dubai-real-estate-ad-permit-whatsapp",
    title="Dubai Property Ad Permits and WhatsApp Leads, 2026 | Nuevo",
    desc="Dubai property ads in 2026: the DLD Trakheesi ad permit, the Madmoun QR code, fines for violations, Abu Dhabi rules, and handling WhatsApp leads within them.",
    h1="Dubai property ad permits and WhatsApp leads: the rules in 2026",
    card="The DLD advertising permit, the Madmoun QR code, reported fines, the Abu Dhabi rules, and how to run WhatsApp lead campaigns within them.",
    lead="Real estate is one of the most regulated categories to advertise in the UAE, and most property leads now arrive on WhatsApp. Here is what the Dubai Land Department and other official sources require before an ad runs, and how to handle the chats it starts.",
    answer="Every property ad in Dubai needs a Real Estate Advertisement Permit from the Dubai Land Department, applied for through the Trakheesi system; the DLD lists a fee of AED 1,000 plus AED 20, and about one working day. Since 24 April 2023 each permit comes with a Madmoun QR code that must appear on the ad, and scanning it shows the approved advertiser and the property's status. Press reports describe fines of AED 50,000 per violation for brokers. In Abu Dhabi, Madhmoun permits through ADREC have been required for property ads since July 2025. Social media creators promoting property also need the UAE Advertiser Permit.",
    body="""
<p class="note">General information, not legal advice. Check the current rules with the Dubai Land Department or your emirate's regulator before you advertise.</p>

<h2>The DLD advertising permit</h2>
<ul>
<li>Every real estate advertisement in Dubai needs a permit from the Dubai Land Department, issued through the <strong>Trakheesi</strong> system.</li>
<li>The DLD lists the fee as AED 1,000 plus AED 20 in fees per permit (AED 5,000 for project launch events), with a processing time of about one working day.</li>
<li>Brokers need a marketing agreement with the property owner before they can advertise it.</li>
<li>The DLD's service page covers electronic and online ads. It doesn't name social media or WhatsApp specifically, but online ads, including paid social, are where the permit matters most in practice.</li>
</ul>

<h2>The Madmoun QR code</h2>
<p>According to the Dubai Media Office, from 24 April 2023 every advertising permit comes with a Madmoun QR code, and companies must show it on their ads. Anyone who scans it sees that the ad is approved, who the advertiser is, and whether the property is still available. Gulf News reported in April 2025 that a DLD AI system automatically adjusted 29% of 279,000 property listings.</p>

<h2>Enforcement</h2>
<ul>
<li>Press reports describe fines of AED 50,000 per violation, sometimes with suspension of up to three months.</li>
<li>In February 2024 agents were given three days to remove misleading listings and 30 firms were fined; in April 2024 brokers were given five days to remove non-compliant portal ads, with no more than three brokers allowed to advertise one property.</li>
</ul>

<h2>Abu Dhabi and creators</h2>
<ul>
<li><strong>Abu Dhabi:</strong> Madhmoun advertising permits through ADREC and the DARI platform have been required for property ads since 7 July 2025, according to law firm and portal summaries. ADGM runs its own permit.</li>
<li><strong>Creators and influencers:</strong> anyone promoting products or services on social media in the UAE needs the Advertiser Permit from the national media regulator.</li>
</ul>

<h2>Running WhatsApp lead campaigns within the rules</h2>
<ol>
<li><strong>Permit first, ad second.</strong> Every ad that names a property gets its own permit and shows its Madmoun QR code.</li>
<li><strong>Match the ad to the permit.</strong> Price, size and location in the ad and in the first WhatsApp reply should match what was approved.</li>
<li><strong>Answer in seconds, qualify in the chat.</strong> Ask budget, area, move-in date and whether they are buying or renting, then hand qualified leads to an agent with a summary.</li>
<li><strong>Stop when the unit is gone.</strong> Update the reply the moment a property is sold or let; the QR code will say so too.</li>
<li><strong>Keep marketing messages to people who opted in,</strong> under WhatsApp's rules and the UAE telemarketing resolution. See our <a href="/guides/whatsapp-marketing-rules-uae/">WhatsApp marketing rules guide</a>.</li>
</ol>
<p>Property Finder offers WhatsApp leads to its partner brokers at no extra cost, according to its partner pages. Whatever the source of the chat, the lead is only worth something if someone answers it fast. That's what our <a href="/real-estate-automation-dubai/">real estate lead automation</a> does.</p>
<p class="note">Sources: Dubai Land Department service page for the Real Estate Advertisement Permit; Dubai Media Office (18 April 2023) on Madmoun; Gulf News (April 2025) and other press reports on enforcement; law firm and Bayut summaries of Abu Dhabi's Madhmoun rules; Property Finder partner pages. Read 28 November 2026.</p>
""",
    faqs=[
        ("Do I need a permit to advertise property in Dubai?", "Yes. Every real estate advertisement in Dubai needs a permit from the Dubai Land Department through the Trakheesi system. The DLD lists the fee as AED 1,000 plus AED 20 per permit."),
        ("What is the Madmoun QR code?", "A QR code issued with every Dubai property advertising permit since 24 April 2023. It must appear on the ad, and scanning it shows the approved advertiser and whether the property is still available."),
        ("What is the fine for advertising property without a permit in Dubai?", "Press reports describe fines of AED 50,000 per violation, sometimes with suspension. Check the current penalty with the Dubai Land Department."),
        ("Do Abu Dhabi property ads need a permit?", "Yes. Madhmoun advertising permits through ADREC and the DARI platform have been required for property ads in Abu Dhabi since July 2025. ADGM has its own permit."),
        ("Can I use WhatsApp for property leads in Dubai?", "Yes. The ad that starts the chat needs its permit and QR code, the details you share should match it, and marketing messages should only go to people who opted in."),
    ],
    related=[("/real-estate-automation-dubai/", "Real estate lead automation in Dubai"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads"), ("/guides/whatsapp-marketing-rules-uae/", "WhatsApp marketing rules in the UAE")],
)

guide(
    slug="google-ads-to-whatsapp",
    title="Google Ads to WhatsApp: Message Assets and Tracking | Nuevo",
    desc="How to send Google Ads clicks to WhatsApp in 2026: message assets, the verification rules, landing pages, and tracking WhatsApp leads as Google Ads conversions.",
    h1="Google Ads to WhatsApp: how to start chats from search ads",
    card="Google's message assets for WhatsApp, their requirements and beta status, why a landing page still matters, and how to count WhatsApp leads as conversions.",
    lead="Meta ads can open WhatsApp directly. Google Ads can too, with more conditions. Here is what Google's own help pages say in November 2026, and how to measure the chats your search ads start.",
    answer="Google Ads can start WhatsApp chats through message assets, a beta feature that adds a WhatsApp button to Search and Performance Max ads. Google requires advertiser verification, a good policy history and an eligible industry, and the WhatsApp link must be verified, either by showing it on the website you advertise or by proving you own the domain. Once approved, a Leads from Messages conversion goal becomes available. Where message assets aren't available, the usual route is a landing page on your own domain with a clear WhatsApp button, tracked with GA4's outbound click events imported into Google Ads.",
    body="""
<h2>Option 1: message assets (beta)</h2>
<ul>
<li>A message asset adds a WhatsApp (or SMS, Messenger or Zalo) button to your Search or Performance Max ads.</li>
<li><strong>Requirements:</strong> advertiser verification, a good policy history and an eligible industry.</li>
<li><strong>Link verification:</strong> the WhatsApp number or link must appear on the website you advertise, on the same domain as the ad, or you must prove you own the domain.</li>
<li><strong>Measurement:</strong> once approved, Google offers a Leads from Messages conversion goal.</li>
<li><strong>Trade-off:</strong> while the message button shows, other assets such as calls and lead forms don't show with it.</li>
</ul>
<p>Google's help pages don't list the countries where message assets are available, and the feature is still in beta, so check eligibility inside your account.</p>

<h2>Option 2: a landing page with a WhatsApp button</h2>
<p>Google requires an ad's destination to match its domain without redirecting elsewhere, so sending a search ad straight to a wa.me link is risky. The reliable route is a fast landing page on your own domain that answers the search and offers WhatsApp as the main action. That page also carries the price, delivery details and trust signals a searcher wants before they message.</p>

<h2>Tracking WhatsApp leads in Google Ads</h2>
<ol>
<li><strong>Clicks:</strong> GA4 records clicks on outbound links, including wa.me links, automatically. Mark the click as a key event and import it into Google Ads. A click isn't a message sent, so treat it as a soft conversion.</li>
<li><strong>Leads:</strong> when the chat becomes a real lead, record it with the Google click ID (GCLID) captured on the landing page, and send it to Google with enhanced conversions for leads.</li>
<li><strong>Sales:</strong> upload sales from the chat as offline conversions with the order value. Since 15 June 2026, Google takes these uploads through its Data Manager API.</li>
</ol>
<p>The same idea applies on Meta, where chat sales go back through the Conversions API. See <a href="/guides/track-whatsapp-ad-sales/">tracking sales from WhatsApp ads</a>.</p>

<h2>Search or Meta for WhatsApp leads?</h2>
<ul>
<li><strong>Google search</strong> catches people already looking: "vitamin D delivery Dubai", "collagen powder UAE". Intent is high, volume is limited by what people search.</li>
<li><strong>Meta</strong> creates demand among people who weren't searching, and opens WhatsApp directly with a free messaging window.</li>
</ul>
<p>Many brands use both. M2S answers the chats from either in seconds; see <a href="/m2s/">how it works</a>.</p>
<p class="note">Sources: Google Ads Help articles on message assets, destination requirements, lead form assets, enhanced conversions for leads and offline conversion imports; GA4 help on enhanced measurement outbound clicks. Read 28 November 2026.</p>
""",
    faqs=[
        ("Can Google Ads open WhatsApp directly?", "Yes, through message assets, a beta feature that adds a WhatsApp button to Search and Performance Max ads. It needs advertiser verification, an eligible industry and a verified WhatsApp link."),
        ("Can I use a wa.me link as my Google Ads final URL?", "Google requires an ad's destination to match the ad's domain without redirecting to another domain, so a wa.me link as the final URL is risky. Use a landing page on your own domain with a WhatsApp button."),
        ("How do I track WhatsApp clicks from Google Ads?", "GA4 records outbound link clicks, including wa.me links. Mark them as a key event and import them into Google Ads, then record real leads and sales with the Google click ID for better optimisation."),
        ("Are Google message assets available in the UAE?", "Google's help pages don't list countries for message assets, which are in beta. Check eligibility in your Google Ads account."),
        ("Should I use Google or Meta to get WhatsApp leads?", "Google catches people already searching, with high intent but limited volume. Meta reaches people who weren't searching and opens WhatsApp directly. Most brands do best with both."),
    ],
    related=[("/guides/track-whatsapp-ad-sales/", "Tracking sales from WhatsApp ads"), ("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads on Meta"), ("/ai-automation-agency-dubai/", "AI automation agency in Dubai")],
)

guide(
    slug="restaurant-whatsapp-ordering-uae",
    title="WhatsApp Ordering for UAE Restaurants vs Delivery Apps | Nuevo",
    desc="Taking restaurant orders on WhatsApp in the UAE: catalog and cart limits, delivery app fees on the record, and Dubai's 2025 transparency rules.",
    h1="WhatsApp ordering for UAE restaurants: next to the delivery apps",
    card="WhatsApp catalog and cart limits, what is actually on record about delivery app fees in the UAE, Dubai's 2025 transparency circular, and how to run direct orders.",
    lead="Delivery apps bring restaurants new customers. WhatsApp keeps the regulars. Here is how WhatsApp ordering works in 2026, what is publicly known about delivery app fees in the UAE, and how to run both side by side.",
    answer="UAE restaurants can take direct orders on WhatsApp with a catalog of up to 500 items and a cart that sends the whole order as one message; WhatsApp's cart doesn't take payment, so you add a payment link or cash on delivery. No delivery platform publishes a standard UAE commission rate. Figures on record vary widely, from Noon Food's Dubai SME offer starting at 10% to roughly 25% reported in 2020 press, and Deliveroo UAE introduced a monthly platform fee from February 2026. Dubai's 2025 circular on delivery platforms requires notice of changes and itemised statements but sets no commission cap.",
    body="""
<h2>How WhatsApp ordering works</h2>
<ul>
<li><strong>Catalog:</strong> up to 500 items in the WhatsApp Business catalog, each with up to 10 photos or videos.</li>
<li><strong>Cart:</strong> customers add items and send the whole order as one message, a feature WhatsApp launched in December 2020 with restaurants as a named use case. On the API, a sent cart can't be edited and allows up to 99 units per item.</li>
<li><strong>Payment:</strong> the cart doesn't take payment. Send a payment link or confirm cash on delivery. See <a href="/guides/whatsapp-payment-links-uae/">taking payments on WhatsApp</a>.</li>
</ul>

<h2>What delivery app fees look like, on the record</h2>
<p>None of the big platforms publishes a standard UAE commission rate, and deals vary by restaurant. What is publicly documented:</p>
<ul>
<li><strong>Noon Food:</strong> launched in 2021 at 15% plus 2%; its Dubai SME programme for eligible Emirati-owned businesses starts at 10% and rises to 20% by year five.</li>
<li><strong>Deliveroo UAE:</strong> its help centre confirms a monthly platform fee for all restaurants from 1 February 2026, without stating the amount.</li>
<li><strong>Careem:</strong> replaced a commission of about 25% with a fixed monthly fee in February 2021; we couldn't confirm the current model.</li>
<li>The often-quoted 25 to 30% range comes from 2020 press coverage.</li>
</ul>
<p>Ask your own account manager for your rate in writing, including payment and delivery fees.</p>

<h2>Dubai's 2025 rules for delivery platforms</h2>
<p>Dubai's consumer protection authority issued Circular No. 2 of 2025 on delivery platforms. It requires 30 days' notice of changes, monthly itemised statements, optional advertising fees and no hidden costs. It does not cap commissions, and we found no commission cap anywhere in the UAE.</p>

<h2>Running WhatsApp next to the apps</h2>
<ol>
<li><strong>Use the apps for discovery,</strong> WhatsApp for repeat orders. Put your WhatsApp number on menus, bags and receipts.</li>
<li><strong>Answer fast.</strong> An order chat that waits ten minutes goes back to the app.</li>
<li><strong>Confirm every order in writing:</strong> items, total, address, time, payment method.</li>
<li><strong>Send order updates as utility templates</strong> and offers only to customers who opted in.</li>
<li><strong>Keep one menu.</strong> Prices and availability in WhatsApp should match the kitchen's, or orders go wrong.</li>
</ol>
<p>See our <a href="/restaurant-whatsapp-automation-uae/">WhatsApp ordering for restaurants</a> page for how M2S handles it.</p>
<p class="note">Sources: WhatsApp Business help on catalogs and carts; Meta developer documentation on cart messages; Deliveroo UAE restaurant help centre; Noon Food and Careem announcements and press coverage; Dubai consumer protection Circular No. 2 of 2025 as reported. Read 28 November 2026. Commission figures vary by restaurant and change often.</p>
""",
    faqs=[
        ("Can restaurants take orders on WhatsApp in the UAE?", "Yes. The WhatsApp Business catalog holds up to 500 items and customers can send a whole cart as one message. Payment is handled with a payment link or cash on delivery."),
        ("How much commission do delivery apps charge restaurants in the UAE?", "No platform publishes a standard UAE rate. Documented figures range from Noon Food's Dubai SME offer starting at 10% to about 25% reported in 2020, and Deliveroo UAE added a monthly platform fee from February 2026. Ask for your own rate in writing."),
        ("Is there a cap on delivery app commissions in Dubai?", "No. Dubai's 2025 circular on delivery platforms requires transparency, such as 30 days' notice of changes and itemised statements, but sets no commission cap."),
        ("Does WhatsApp take payment for restaurant orders?", "Not in the UAE. WhatsApp's cart sends the order but doesn't take payment, so restaurants send a payment link or confirm cash on delivery."),
        ("Should restaurants leave the delivery apps for WhatsApp?", "Usually not. The apps bring new customers; WhatsApp works best for regulars and repeat orders, without a per-order commission."),
    ],
    related=[("/restaurant-whatsapp-automation-uae/", "WhatsApp ordering for restaurants"), ("/guides/whatsapp-payment-links-uae/", "Taking payments on WhatsApp"), ("/guides/whatsapp-business-app-vs-api/", "WhatsApp Business app vs API")],
)


# ================================================================ batch 9 (28 Nov 2026)

guide(
    slug="uae-ecommerce-whatsapp-statistics",
    title="UAE E-commerce & WhatsApp Statistics 2026, Sourced | Nuevo",
    desc="UAE digital statistics for 2026 with sources: population, internet use, social media ad reach, WhatsApp use, e-commerce market size, payments and messaging.",
    h1="UAE e-commerce, social media and WhatsApp statistics, 2026",
    card="Sourced figures on UAE population, internet and WhatsApp use, social media ad reach, the e-commerce market, payments and messaging, with every source linked.",
    lead="The numbers we use when planning campaigns for UAE brands, each with its source and date. We only include figures we could trace to the publisher; where a popular statistic didn't check out, we say so at the end.",
    answer="The UAE had 12.06 million residents at the end of 2025, according to the Federal Competitiveness and Statistics Centre. DataReportal's October 2026 data puts internet use at 99% and mobile connections at 24.9 million, and 84.1% of internet users aged 16 and over used WhatsApp in the past month (GWI, Q2 2026). EZDubai and Euromonitor value UAE e-commerce at AED 42.2 billion in 2025, about 15.7% of retail, forecast to reach about AED 67.2 billion by 2030. Visa reports that 55% of domestic payment volume is now online or in-app, and Checkout.com that cash on delivery use in the UAE is down 53% since 2020.",
    body="""
<h2>Population and connectivity</h2>
<div class="prose-table"><table>
<thead><tr><th>Statistic</th><th>Figure</th><th>Source</th></tr></thead>
<tbody>
<tr><td>UAE population, end of 2025</td><td>12,063,953 (up 7% on 2024)</td><td>FCSC, reported 15 Nov 2026</td></tr>
<tr><td>Dubai population, end of 2025</td><td>4.58 million (up 7.5%)</td><td>Dubai Data and Statistics Establishment, July 2026</td></tr>
<tr><td>Internet users</td><td>11.5 million, 99.0% penetration</td><td>DataReportal Digital 2027: UAE (data Oct 2026)</td></tr>
<tr><td>Mobile connections</td><td>24.9 million, 215% of the population</td><td>DataReportal Digital 2027, citing GSMA Intelligence</td></tr>
<tr><td>Median fixed download speed</td><td>382.40 Mbps</td><td>DataReportal Digital 2027, citing Ookla</td></tr>
</tbody></table></div>
<p>DataReportal uses a UN-based population estimate (11.6 million) that is lower than the official register, so its percentages and the FCSC total shouldn't be combined.</p>

<h2>Social media and WhatsApp</h2>
<div class="prose-table"><table>
<thead><tr><th>Platform</th><th>Ad reach, Oct 2026</th><th>Ad reach, Oct 2025</th></tr></thead>
<tbody>
<tr><td>TikTok (adults 18+)</td><td>13.7 million</td><td>12.5 million</td></tr>
<tr><td>LinkedIn (members)</td><td>12.0 million</td><td>10.0 million</td></tr>
<tr><td>Facebook</td><td>10.2 million</td><td>9.70 million</td></tr>
<tr><td>YouTube</td><td>9.91 million</td><td>8.37 million</td></tr>
<tr><td>Instagram</td><td>8.90 million</td><td>8.05 million</td></tr>
<tr><td>Snapchat</td><td>5.09 million</td><td>5.13 million</td></tr>
<tr><td>X</td><td>2.08 million</td><td>2.85 million</td></tr>
</tbody></table></div>
<p>Source: DataReportal Digital 2027 and Digital 2026: UAE. Ad reach figures come from the platforms' own advertising tools. They are not monthly active users, may not be unique people, and can exceed the population.</p>
<ul>
<li><strong>WhatsApp:</strong> 84.1% of internet users aged 16+ used WhatsApp in the past month, the highest of any platform; Messenger 57.3% (GWI survey, Q2 2026, via DataReportal).</li>
<li><strong>Brand research:</strong> 48.1% of UAE internet users use social networks as a main source when researching brands, and the average user is on 7.7 platforms a month (We Are Social, Digital 2026).</li>
</ul>

<h2>E-commerce</h2>
<div class="prose-table"><table>
<thead><tr><th>Statistic</th><th>Figure</th><th>Source</th></tr></thead>
<tbody>
<tr><td>UAE e-commerce market, 2025</td><td>AED 42.2 billion (US$11.5 billion)</td><td>EZDubai with Euromonitor, Sept 2026</td></tr>
<tr><td>Growth since 2020</td><td>From AED 17.6 billion, 19% a year</td><td>EZDubai with Euromonitor</td></tr>
<tr><td>Share of retail sales</td><td>About 15.7%, forecast above 20% by 2030</td><td>EZDubai with Euromonitor</td></tr>
<tr><td>Forecast for 2030</td><td>About AED 67.2 billion</td><td>EZDubai with Euromonitor</td></tr>
<tr><td>Largest category</td><td>Apparel and footwear, AED 11.4 billion</td><td>EZDubai with Euromonitor</td></tr>
<tr><td>Online shopping on mobile</td><td>37%, the highest of 8 countries surveyed</td><td>Visa, July 2025 (fieldwork Q4 2024)</td></tr>
<tr><td>Shop online at least weekly</td><td>52% of UAE consumers</td><td>Checkout.com, May 2026</td></tr>
<tr><td>Shop through social media</td><td>27% of UAE consumers</td><td>Checkout.com, May 2026</td></tr>
</tbody></table></div>

<h2>Payments</h2>
<ul>
<li><strong>Online share of card payments:</strong> 55% of domestic Visa payment volume in the UAE is online or in-app, up from 35% in 2019 (Visa, October 2026).</li>
<li><strong>Cash on delivery:</strong> use in the UAE is down 53% since 2020 (Checkout.com, 2025). Across the region, cash on delivery preference halved from 41% to 20% (Checkout.com, 2024).</li>
<li><strong>Digital wallets:</strong> 67% of UAE consumers use one at least monthly to buy, budget or manage money (Checkout.com, May 2026).</li>
<li><strong>Checkout friction:</strong> 32% of UAE consumers have abandoned a cart over payment security concerns (Checkout.com, May 2026).</li>
<li><strong>Cash in daily life:</strong> 80% of payments are made digitally, and only 16% of consumers mainly use cash for everyday purchases (Visa, January 2026).</li>
<li><strong>Buy now, pay later:</strong> Tabby and Tamara repayment data has been added to UAE credit reports from July 2026 (Etihad Credit Bureau, via Gulf News).</li>
</ul>

<h2>Messaging and conversational commerce</h2>
<ul>
<li><strong>Businesses:</strong> 55% of large UAE organisations say rich messaging such as WhatsApp will be their top investment channel over the next five years, against 13% for email (BCG and Meta enterprise survey, April 2026).</li>
<li><strong>Consumers, global:</strong> 73.3% of people prefer messaging when contacting a business, and 72.4% are more likely to buy from brands that offer it, across 22 markets including the UAE (Meta and Kantar, 2025 fieldwork). These are global averages, not UAE-only figures.</li>
<li><strong>Consumers, UAE:</strong> 85% of UAE residents want businesses to offer WhatsApp for customer support, and 65% used WhatsApp to ask a business about a product in the past year (Zbooni and YouGov, 2024; vendor-commissioned).</li>
</ul>

<h2>What these numbers mean for a UAE brand</h2>
<ul>
<li>Nearly every customer is online and on WhatsApp, so the question isn't whether to sell there but how fast you answer.</li>
<li>Mobile and social shopping are mainstream, which suits ads that open a chat rather than a desktop checkout. See our <a href="/guides/click-to-whatsapp-ads/">click-to-WhatsApp ads guide</a>.</li>
<li>Cash on delivery is shrinking but still present, so offer a <a href="/guides/whatsapp-payment-links-uae/">payment link in the chat</a> and confirm COD orders.</li>
</ul>

<h2>Statistics we left out</h2>
<ul>
<li><strong>UAE supplements market size:</strong> the figures circulating online either come from vendor models or couldn't be traced to the publisher. Euromonitor's own reports describe steady growth without public values.</li>
<li><strong>"WhatsApp is used by 78%+ of the UAE" and "customers expect a reply within 5 minutes":</strong> we found these only on blogs that name no source.</li>
<li><strong>Year-on-year e-commerce growth</strong> from different editions of the EZDubai report, which may not use the same series.</li>
</ul>
<p class="note">Sources: FCSC via Emirates 24/7 and Gulf Today (15 Nov 2026); <a href="https://datareportal.com/reports/digital-2027-united-arab-emirates" target="_blank" rel="noopener">DataReportal Digital 2027: UAE</a> and <a href="https://datareportal.com/reports/digital-2026-united-arab-emirates" target="_blank" rel="noopener">Digital 2026: UAE</a>; <a href="https://www.wam.ae/en/article/c2h35yn-uae-e-commerce-market-size-reaches-aed422-billion" target="_blank" rel="noopener">WAM on the EZDubai and Euromonitor report</a>; Visa UAE newsroom (2 Jul 2025, 14 Jan 2026, 12 Oct 2026); Checkout.com MENA digital commerce reports (2024, 2025, 2026); <a href="https://whatsappbusiness.com/resources/resource-library/state-of-business-messaging/" target="_blank" rel="noopener">WhatsApp Business, State of Business Messaging</a>; BCG and Meta via TahawulTech (18 Apr 2026); Zbooni and YouGov via Communicate (Feb 2024). Compiled 28 November 2026. You're welcome to quote these figures; please cite the original source.</p>
""",
    faqs=[
        ("What is the population of the UAE in 2026?", "The latest official figure is 12,063,953 at the end of 2025, up 7% on 2024, according to the Federal Competitiveness and Statistics Centre."),
        ("How many people in the UAE use WhatsApp?", "84.1% of internet users aged 16 and over used WhatsApp in the past month, the highest of any platform, according to GWI survey data for Q2 2026 published by DataReportal. Internet use in the UAE is about 99%."),
        ("How big is e-commerce in the UAE?", "EZDubai and Euromonitor value the UAE e-commerce market at AED 42.2 billion (US$11.5 billion) in 2025, about 15.7% of retail sales, forecast to reach about AED 67.2 billion by 2030."),
        ("Is cash on delivery still popular in the UAE?", "It is declining. Checkout.com reported in 2025 that cash on delivery use in the UAE was down 53% since 2020, and Visa reports that 55% of domestic card payment volume is now online or in-app."),
        ("How many Instagram users are there in the UAE?", "Instagram's advertising reach in the UAE was 8.90 million in October 2026, according to DataReportal. Ad reach isn't the same as monthly active users."),
    ],
    related=[("/guides/click-to-whatsapp-ads/", "Click-to-WhatsApp ads"), ("/guides/meta-ads-ecommerce-uae/", "Meta ads for UAE e-commerce"), ("/guides/cash-on-delivery-whatsapp-confirmation-uae/", "Confirming COD orders on WhatsApp")],
)


# ================================================================ batch 10 (28 Nov 2026)

guide(
    slug="clinic-marketing-whatsapp-uae",
    title="Clinic Marketing and WhatsApp Rules in the UAE, 2026 | Nuevo",
    desc="Clinic marketing rules in the UAE for 2026: DHA social media standards and banned words, MOHAP ad licences, health data law, WhatsApp reminders and Meta ad rules.",
    h1="Clinic marketing and patient messaging on WhatsApp in the UAE",
    card="DHA's 2026 social media standards and banned words, MOHAP ad licences, the health data law, WhatsApp appointment reminders and Meta's health ad rules.",
    lead="Clinics in the UAE market under stricter rules than almost any other business, and WhatsApp is now part of that marketing. Here is what the health regulators, the health data law and Meta say as of November 2026, and how to run patient enquiries and reminders on WhatsApp within them.",
    answer="UAE clinics have three sets of rules to follow. The Dubai Health Authority's standards for medical advertising on social media, re-issued in August 2026, cover WhatsApp alongside Instagram and TikTok, ban words such as \"100%\", \"no side effects\", \"the best\" and \"immediate results\", require written patient consent for testimonials and images, and allow before-and-after photos only of the same person, unedited, with a results-may-vary statement. MOHAP issues healthcare advertising licences, including one for social media. Federal Law No. 2 of 2019 limits storing or transferring health data outside the UAE, so WhatsApp messages should carry appointment logistics, not clinical details.",
    body="""
<p class="note">General information, not legal advice. Confirm current requirements with your licensing health authority (DHA, DoH or MOHAP) before you advertise.</p>

<h2>DHA standards for social media advertising (Dubai)</h2>
<p>The DHA re-issued its Standards for Medical Advertisement Content on Social Media in a circular dated 17 August 2026. Its earlier 2022 standard, which press reports of the new circular closely follow, applies to all DHA-licensed facilities and professionals and names WhatsApp among the social media it covers.</p>
<ul>
<li><strong>Banned claims:</strong> press reports of the 2026 circular list words such as "unique", "the best", "exclusive", "safest", "the only", "magic", "miraculous", "assured success", "has no side effects", "100%", "absolutely certain" and "immediate results", plus comparisons like "safer than".</li>
<li><strong>Before-and-after images:</strong> the same person, the same lens, no editing, with a statement that results may vary and the risks, in the same font size as the rest of the ad.</li>
<li><strong>Consent:</strong> documented written consent from any patient who appears or gives a testimonial, and separate parental consent for anyone under 18.</li>
<li><strong>Approval inside the clinic:</strong> posts by staff or influencers that name the facility must be approved by the medical director, and the facility keeps an archive for audits.</li>
<li><strong>Titles:</strong> no job titles that differ from the DHA licence, such as "anti-aging specialist" or "beauty expert".</li>
</ul>
<p>The penalties described are disciplinary action; we found no published fine amounts for these standards.</p>

<h2>Advertising licences</h2>
<ul>
<li><strong>MOHAP:</strong> the 2022 DHA standard requires a facility's official account to show its medical advertisement licence number from MOHAP. MOHAP's service pages list a licence for healthcare advertising on social media at AED 1,000 a month or AED 3,000 a year plus an AED 100 application fee (from MOHAP's pages as seen in search; confirm before applying).</li>
<li><strong>Abu Dhabi:</strong> the Department of Health runs its own health media and advertising system, with mandatory training for licensed facilities. We couldn't confirm its fees.</li>
<li><strong>Medical products:</strong> separately, ads for medical products need Emirates Drug Establishment approval since November 2026, and influencers may not promote them.</li>
</ul>

<h2>Patient data and WhatsApp</h2>
<p>Federal Law No. 2 of 2019 on the use of ICT in health fields applies across the UAE, free zones included:</p>
<ul>
<li>Health data from services provided in the UAE may only be stored, processed or transferred outside the country in cases allowed by the health authorities (Article 13). Ministerial Resolution No. 51 of 2021 lists those exceptions, several of which require patient consent and a copy kept in the UAE.</li>
<li>Using patient data for non-health purposes, such as marketing, needs the patient's written approval (Article 16).</li>
<li>Breaching the storage rule carries a fine of AED 500,000 to 700,000 (Article 24).</li>
</ul>
<p>WhatsApp's own Business Messaging Policy also says not to use WhatsApp to send health information where local rules require stronger protection. The practical approach most clinics take:</p>
<ul>
<li>Keep WhatsApp messages to logistics: appointment date, time, branch, preparation instructions that aren't specific to a diagnosis.</li>
<li>Keep results, diagnoses and clinical notes in your UAE-hosted clinic system, not in chats.</li>
<li>Collect the patient's opt-in for WhatsApp messages at booking, and a separate one for marketing.</li>
</ul>

<h2>Appointment reminders on WhatsApp</h2>
<p>A reminder of an appointment the patient booked fits Meta's definition of a utility message: triggered by the patient, specific to them and non-promotional. Add an offer ("and 20% off fillers this week") and Meta treats the whole message as marketing. Keep reminders and promotions separate. Our <a href="/ai-receptionist-uae/">AI receptionist</a> page covers booking and reminders in more detail.</p>

<h2>Meta's rules for clinic ads</h2>
<ul>
<li><strong>No personal health attributes:</strong> an ad can't imply it knows the viewer's condition. "Do you have diabetes?" is rejected; "New diabetes treatment available" is allowed.</li>
<li><strong>Cosmetic procedures and weight loss:</strong> target 18 and over, and avoid content that creates a negative self-image.</li>
<li><strong>No health-condition targeting:</strong> Meta removed detailed targeting options tied to health conditions in January 2022.</li>
<li><strong>Data restrictions for health websites:</strong> industry sources report that from January 2025 Meta began restricting the data it accepts from websites it classifies as health and wellness, removing URL details and blocking some lower-funnel events such as Lead, Schedule and Purchase for optimisation outside Europe. This comes from secondary sources rather than a Meta page we could read, so check your data source settings in Events Manager.</li>
</ul>
<p>Click-to-WhatsApp ads remain a common route for clinics: the ad starts a conversation, and the booking happens in the chat. See our <a href="/automation-for-clinics-uae/">clinic enquiries page</a> and <a href="/guides/click-to-whatsapp-ads/">click-to-WhatsApp ads guide</a>.</p>
<p class="note">Sources: DHA circular CIR-2026-00000144 (17 August 2026) and the DHA Standards for Medical Advertisement Content on Social Media (2022); Khaleej Times, Gulf News and The National coverage (September 2026); MOHAP healthcare advertising licence pages; DoH circular 26/2023; Federal Law No. 2 of 2019 (official English text) and Ministerial Resolution No. 51 of 2021 as summarised by CMS; WhatsApp Business Messaging Policy; Meta's ad standards on personal attributes and health and wellness; industry reports on Meta's 2025 health data restrictions. Read 28 November 2026.</p>
""",
    faqs=[
        ("Can clinics in Dubai advertise on WhatsApp and Instagram?", "Yes, within the DHA's standards for medical advertising on social media, which name WhatsApp, Instagram, TikTok and others. Claims must be accurate, banned words avoided, and patient images and testimonials need written consent."),
        ("Which words are banned in Dubai clinic ads?", "Press reports of the DHA's August 2026 circular list words such as \"the best\", \"unique\", \"safest\", \"the only\", \"miraculous\", \"100%\", \"no side effects\" and \"immediate results\", along with comparisons like \"safer than\"."),
        ("Are before-and-after photos allowed in UAE clinic ads?", "Under DHA's standards, only of the same person with the same lens and no editing, with a clear statement that results may vary and the risks. Meta separately restricts some before-and-after content."),
        ("Can a clinic send appointment reminders on WhatsApp?", "Yes, with the patient's opt-in. Keep reminders to date, time and location; UAE law restricts storing or transferring health data outside the country, so clinical details belong in your UAE-hosted system."),
        ("Do clinics need a licence to advertise on social media in the UAE?", "MOHAP lists a healthcare advertising licence for social media, and DHA's 2022 standard requires the licence number on the facility's official account. Abu Dhabi's DoH runs its own system. Confirm with your authority."),
    ],
    related=[("/automation-for-clinics-uae/", "Clinic enquiries to booked visits"), ("/ai-receptionist-uae/", "AI receptionist and bookings"), ("/guides/whatsapp-marketing-rules-uae/", "WhatsApp marketing rules in the UAE")],
)


NEW_SLUGS = set()  # pass slugs on the command line to rewrite them

# ---------------------------------------------------------------- template
TPL = (ROOT / "whatsapp-automation-uae/index.html").read_text()
head_part = TPL[TPL.index("  <!-- head:start -->"):TPL.index("<!-- head:end -->") + len("<!-- head:end -->")]
header_part = TPL[TPL.index("  <!-- header:start"):TPL.index("<!-- header:end -->") + len("<!-- header:end -->")].replace("header:start service", "header:start guides")
footer_part = TPL[TPL.index("  <!-- footer:start -->"):TPL.index("<!-- footer:end -->") + len("<!-- footer:end -->")]

def e(s):
    return html.escape(s, quote=True)

def ld(obj):
    return '  <script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n  </script>\n"

def page(url, title, desc, og_title, ld_blocks, main):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#ffffff">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Nuevo Automations">
  <meta property="og:locale" content="en_AE">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(og_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-card.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Nuevo Automations: turn every message into a sale.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(og_title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{SITE}/assets/og-card.jpg">

{head_part}

{''.join(ld(b) for b in ld_blocks)}</head>
<body>
{header_part}

  <main id="top">
{main}
  </main>

{footer_part}
</body>
</html>
"""

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

if len(sys.argv) > 2:
    NEW_SLUGS = set(sys.argv[2:])
for g in GUIDES:
    if g["slug"] not in NEW_SLUGS: continue
    path = f"/guides/{g['slug']}/"
    url = SITE + path
    article = {
        "@context": "https://schema.org", "@type": "Article", "@id": url + "#article",
        "headline": g["h1"], "description": g["desc"], "url": url, "mainEntityOfPage": url,
        "datePublished": DATE, "dateModified": DATE, "inLanguage": "en",
        "image": SITE + "/assets/og-card.jpg",
        "author": {"@type": "Person", "@id": SITE + "/about/#nawaf", "name": "Nawaf Allahham", "jobTitle": "Founder", "url": SITE + "/about/", "sameAs": ["https://www.linkedin.com/in/nawafallahham/"]},
        "publisher": {"@id": SITE + "/#org"},
        "isPartOf": {"@id": SITE + "/guides/#collection"},
        "about": [{"@type": "Thing", "name": "WhatsApp Business"}, {"@type": "Place", "name": "United Arab Emirates"}],
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faqs"]]}
    bc = crumbs([("Home", "/"), ("Guides", "/guides/"), (g["h1"], path)])
    faq_html = "\n".join(f'          <div class="faq__item"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in g["faqs"])
    rel_html = "\n".join(f'          <li><a class="link" href="{u}">{e(t)}</a></li>' for u, t in g["related"])
    main = f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <p class="crumb"><a href="/">Home</a> / <a href="/guides/">Guides</a></p>
        <h1 id="page-h">{e(g['h1'])}</h1>
        <p class="t-lead">{e(g['lead'])}</p>
        <p class="byline">By <a href="/about/">Nawaf Allahham</a>, founder of Nuevo Automations · Updated <time datetime="{DATE}">{DATE_H}</time></p>
        </div>
      </div>
    </section>

    <section class="band" aria-label="Short answer">
      <div class="wrap">
        <div class="answer"><p>{e(g['answer'])}</p></div>
      </div>
    </section>

    <section class="band" aria-label="Guide">
      <div class="wrap">
        <article class="prose">
{g['body'].strip()}
        </article>
      </div>
    </section>

    <section class="band ground-surface" aria-labelledby="faq-h">
      <div class="wrap grid">
        <div class="span-5"><h2 id="faq-h">Common questions</h2></div>
        <div class="faq span-6 start-7">
{faq_html}
        </div>
      </div>
    </section>

    <section class="band" aria-labelledby="related-h">
      <div class="wrap grid">
        <div class="span-5 stack-4">
        <h2 id="related-h">Want this done for your brand?</h2>
        <p>Nuevo Automations runs Meta and Google ads into WhatsApp for UAE wellness and supplement brands, and M2S closes the sale in the chat. The first step is a free 30-minute audit.</p>
        <div class="btn-row">
          <a class="btn btn--primary js-lead" data-lead="guide-{g['slug']}" href="/book/">Book a free audit</a>
          <a class="btn btn--secondary" href="{WA}" target="_blank" rel="noopener">Ask on WhatsApp</a>
        </div>
        </div>
        <ul class="link-list link-list--col span-6 start-7">
{rel_html}
          <li><a class="link" href="/guides/">All guides</a></li>
        </ul>
      </div>
    </section>"""
    out = ROOT / "guides" / g["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(url, g["title"], g["desc"], g["h1"], [article, faq, bc], main))

# ---------------------------------------------------------------- hub
hub_url = SITE + "/guides/"
GROUPS = [
    ("UAE market data", ["uae-ecommerce-whatsapp-statistics"]),
    ("Costs, platforms and setup", ["whatsapp-business-api-pricing-uae", "whatsapp-chatbot-cost-uae", "whatsapp-business-app-vs-api", "respond-io-vs-wati", "wati-alternatives", "whatsapp-green-tick-uae", "shopify-whatsapp-integration", "arabic-whatsapp-chatbot", "manychat-pricing", "meta-business-ai-whatsapp", "whatsapp-flows"]),
    ("Ads that start the chat", ["click-to-whatsapp-ads", "meta-ads-ecommerce-uae", "track-whatsapp-ad-sales", "advertising-supplements-uae", "instagram-dm-automation-rules", "google-ads-to-whatsapp"]),
    ("Selling and following up", ["whatsapp-payment-links-uae", "whatsapp-abandoned-cart-recovery", "bulk-whatsapp-messages-uae", "cash-on-delivery-whatsapp-confirmation-uae"]),
    ("By industry", ["sell-supplements-online-uae", "clinic-marketing-whatsapp-uae", "dubai-real-estate-ad-permit-whatsapp", "restaurant-whatsapp-ordering-uae"]),
    ("Rules and compliance", ["whatsapp-marketing-rules-uae"]),
]
BY = {g["slug"]: g for g in GUIDES}
_seen = {s for _, ss in GROUPS for s in ss}
_rest = [g["slug"] for g in GUIDES if g["slug"] not in _seen]
if _rest:
    GROUPS.append(("More guides", _rest))
ORDER = [BY[s] for _, ss in GROUPS for s in ss if s in BY]

def _card(g):
    return f"""          <article class="card">
            <h3><a href="/guides/{g['slug']}/">{e(g['h1'])}</a></h3>
            <p>{e(g['card'])}</p>
            <a class="link" href="/guides/{g['slug']}/" aria-hidden="true" tabindex="-1">Read the guide</a>
          </article>"""

def _group(n, title, slugs):
    inner = "\n".join(_card(BY[s]) for s in slugs if s in BY)
    return f"""    <section class="band" aria-labelledby="grp-{n}">
      <div class="wrap">
        <div class="section-head"><h2 id="grp-{n}">{e(title)}</h2></div>
        <div class="guide-list">
{inner}
        </div>
      </div>
    </section>"""

groups_html = "\n\n".join(_group(n, t_, ss) for n, (t_, ss) in enumerate(GROUPS))
coll = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": hub_url + "#collection", "url": hub_url,
        "name": "WhatsApp and Meta ads guides for UAE brands", "inLanguage": "en", "publisher": {"@id": SITE + "/#org"},
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/guides/{g['slug']}/", "name": g["h1"]} for i, g in enumerate(ORDER)]}}
hub_main = f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <p class="crumb"><a href="/">Home</a> / Guides</p>
        <h1 id="page-h">Guides to selling on WhatsApp in the UAE</h1>
        <p class="t-lead">Plain answers on WhatsApp Business API costs and platforms, click-to-WhatsApp and Meta ads, payments and cart recovery, supplement rules and WhatsApp marketing law, written from the campaigns we run for UAE brands.</p>
        </div>
      </div>
    </section>

{groups_html}"""
(ROOT / "guides").mkdir(exist_ok=True)
(ROOT / "guides/index.html").write_text(page(
    hub_url, "WhatsApp & Meta Ads Guides for UAE Brands | Nuevo Automations",
    "Guides for UAE brands on WhatsApp API pricing and platforms, click-to-WhatsApp ads, payments, cart recovery, supplement rules and WhatsApp marketing law.",
    "Guides to selling on WhatsApp in the UAE", [coll, crumbs([("Home", "/"), ("Guides", "/guides/")])], hub_main))

print("\n".join(f"/guides/{g['slug']}/" for g in GUIDES))

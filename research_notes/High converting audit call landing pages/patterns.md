# Evidence-backed landing page patterns for booking a sales/audit call

Context: a done-for-you B2B service (AI WhatsApp sales assistant plus Meta ads into WhatsApp) for premium wellness and supplement e-commerce brands. Traffic is mostly mobile Meta ads, and the goal is a free 30-minute audit booked through an embedded Calendly.

Evidence rating key used throughout:
- **Strong**: several controlled tests or large datasets that agree, ideally with method disclosed.
- **Moderate**: one well-documented controlled test, or a large vendor dataset with a clear method but some self-interest.
- **Weak**: single anecdotes, vendor marketing without method, secondhand figures, or correlational data with obvious confounders.

General caveat: nearly all "documented A/B tests" in CRO come from vendors or agencies publishing their own wins. Few disclose sample sizes or significance, and losing tests are under-reported (publication bias). Read lift percentages as direction, not as an expected effect size.

## Headlines: outcome/number-led vs feature-led vs question; specificity; message match with the ad

### Takeaway
The best-supported headline lever is **message match** (the landing headline repeats the ad's promise), plus plain, specific language. The claims that numbers in headlines win, or that question headlines win, rest on weak, mostly secondhand evidence. Treat them as hypotheses to test.

### Cited Findings
- Conversion Rate Experts' Moz case study is the classic message-match and long-page case. It is CRE's own write-up of a challenger-vs-control test and is said to have generated about $1M — [CRE Moz case study](https://conversion-rate-experts.com/moz-case-study/). A secondary roundup attributes a 212% conversion lift to fixing message match and a 31.4% lift to ConversionLab's dynamic text replacement test (headline matched to the search term). I could not verify either number against the original — [Foundry CRO headline benchmarks (secondary)](https://foundrycro.com/blog/landing-page-headline-benchmarks-2026/)
- "Specific numbers beat vague headlines by 36%" is widely repeated. It traces to a 2013 Conductor analysis of *click-through on article headlines*, not landing-page conversion. The sources found were secondary and gave no primary method — [Flint headline testing stats (secondary)](https://www.flint.com/blog/landing-page-headline-testing-statistics); [Keak (secondary)](https://www.keak.com/blog/ab-test-headlines-that-convert)
- GoodUI keeps a pattern specifically for "Vague or Specific Benefits" (Pattern #127), built from A/B tests it has catalogued. The median effects are paywalled — [GoodUI Pattern #127](https://mail.goodui.org/patterns/127)
- Unbounce's 2024 Conversion Benchmark Report found that landing pages written at a 5th–7th grade reading level had an 11.1% median conversion rate, against 5.3% for college-level copy. This is correlational, across tens of thousands of pages — [Unbounce 2024 report via PR Newswire](https://prnewswire.com/news-releases/unbounces-2024-conversion-benchmark-report-proves-that-attention-spans-are-declining-and-so-are-conversion-rates-302239407.html)
- NN/g found that users spend about 57% of page-viewing time above the fold and 74% in the first two screenfuls (2018 eyetracking). So the headline and first screen carry most of the attention — [NN/g Scrolling and Attention](https://www.nngroup.com/articles/scrolling-and-attention/)

### Inferences
- **Message match: moderate.** The mechanism is well established and CRE and ConversionLab cases agree, but the exact lift figures are unverified. For Meta traffic, the hero headline should repeat the specific ad hook, for example "Turn Instagram ad clicks into WhatsApp sales". Running separate landing variants per ad angle is the practical form of dynamic text replacement.
- **Outcome or number-led vs feature-led: weak to moderate.** Specific outcomes, such as "+X% conversion from ad click to WhatsApp sale for [named brand]", are consistent with the GoodUI specificity pattern and the readability data. Most "number" evidence is about clicks, not conversions.
- **Question headlines: weak.** No controlled landing-page evidence was found either way.
- **Readability: moderate (correlational).** A large sample, but simpler copy may simply correlate with simpler offers.

### Gaps
- No primary source verified for the 212% Moz message-match figure, the ConversionLab 31.4%, or the 36% numbers figure.
- No controlled test found comparing question headlines with statement headlines on B2B lead-gen pages.
- GoodUI's median effect sizes for Pattern #127 are paywalled.

## Social proof: logos, named case-study numbers, testimonials with name/photo, video testimonials; placement above vs below the fold

### Takeaway
Social proof changes have a low but real hit rate in aggregated test databases. When they win, the effect is meaningful, but most single tests show small or no effect. The specific, named, results-based form is the most defensible: logos plus one named case-study number near the CTA. The evidence is **moderate** in general and **weak** for any specific format.

### Cited Findings
- Mida's aggregated A/B-test dataset says social-proof changes (reviews, ratings, logos, counts) win about 8% of the time. When one does win, the median lift is +32.5%. This is a vendor dataset with an undisclosed sample — [Mida social proof change types](https://www.mida.so/change-types/social-proof)
- GoodUI keeps separate evidence-backed patterns for Testimonials (#4), Benefit Testimonials (#19, testimonials that state a specific benefit) and Video Testimonials (#48), each built from catalogued A/B tests. The median effects are hidden behind a paywall — [GoodUI #4](https://goodui.org/patterns/4); [GoodUI #19](https://goodui.org/patterns/19); [GoodUI #48](https://goodui.org/patterns/48)
- One commentary on GoodUI's database notes a +25% signup lift that disappeared on retest. This is a reminder that single social-proof wins often regress — [Biggish summary of GoodUI's 603 tests (secondary)](https://thebiggish.pages.dev/news/goodui-s-603-a-b-tests-show-which-enterprise-ui-patterns-actually-convert)
- In a VWO case, FietsPunt reported a 36.73% increase in orders at 99% confidence after adding social-proof elements to product pages. This is e-commerce, not lead gen — [FietsPunt via casestudies.com](https://www.casestudies.com/company/vwo/case-study/fietspunt-improves-its-product-page-to-increase-purchases)
- Placement: attention drops sharply after the fold (57% of viewing time above it, 74% in the first two screens). This supports putting at least a logo strip or one proof point on the first screen — [NN/g](https://www.nngroup.com/articles/scrolling-and-attention/)

### Inferences
- A logo strip plus one named result in or near the hero is the low-risk default. Full case studies and testimonials can sit lower, near repeated CTAs.
- "Benefit testimonials", which name a concrete result, are favoured by GoodUI's pattern taxonomy over generic praise. For this offer, use a named brand plus a metric, such as revenue from WhatsApp, reply rate or ROAS.
- **Video testimonials: weak.** A pattern exists, but no public effect sizes were found.
- With a ~8% win rate, many social-proof additions will be neutral. Don't expect large lifts from adding more of it.

### Gaps
- No controlled test found isolating logos vs named testimonials vs video testimonials on a B2B call-booking page.
- No controlled test found isolating above- vs below-fold placement of social proof. The placement guidance is inferred from attention data.
- GoodUI medians are paywalled.

## Form vs embedded calendar vs two-step; number of fields; qualifying questions and their effect on volume vs show-up and quality

### Takeaway
The strongest evidence in this whole topic is that **instant scheduling right after (or instead of) a form roughly doubles qualified form-to-meeting conversion** compared with manual follow-up. Two vendors' large datasets agree: Chili Piper at 30% vs 66.7%, and RevenueHero with a 62% median. Field count matters less than folklore suggests: removing relevant fields can hurt. Qualifying questions cut volume, but the evidence that they improve show rate is weak.

### Cited Findings
- Chili Piper, ~4 million form submissions (2024, mostly B2B): 66.7% of qualified submissions booked a meeting with instant scheduling, against an industry average of ~30% with manual follow-up. 14.1% of submissions were disqualified (spam, personal emails or failing criteria) — [Chili Piper 2024 Benchmark](https://chilipiper.com/post/form-conversion-rate-benchmark-report)
- Chili Piper: removing a second form (a "double form fill", commonly a form followed by a Calendly that asks again) raised conversion by "up to 50%". This is an unquantified vendor claim and is pointedly framed against Calendly — [Chili Piper 2024 Benchmark](https://chilipiper.com/post/form-conversion-rate-benchmark-report)
- Chili Piper: offering a live-call option converted at 69.2% vs 66.7%. Calendar load time matters: theirs loads in 3–4 seconds and some competitors take 30–45 seconds, but no conversion figure is given — [Chili Piper 2024 Benchmark](https://chilipiper.com/post/form-conversion-rate-benchmark-report)
- Chili Piper's 2026 mid-market benchmark counts *all* submissions, including screened-out ones, and reports a 2.6% booking rate on that base. Definitions differ widely between reports — [Chili Piper 2026 Web Conversion Benchmark](https://www.chilipiper.com/reports/mid-market-conversion-benchmark)
- RevenueHero, 1M+ inbound form fills: the median qualified-to-booked rate is 62%, the top 10% exceed 78% and the best performer reached 88%. Top performers converted at 77% with 2 fields and 76% with 13 fields, so field count was not the differentiator — [RevenueHero 2025 Inbound Benchmark](https://www.revenuehero.io/2025-inbound-benchmark)
- RevenueHero: the "in-between step" (an SDR relaying a link, a second form, manual review, or "we'll be in touch") costs about 40% of qualified pipeline. This rests on a single cybersecurity-startup anecdote, and the article's own maths is inconsistent. A weekly snapshot shows 30,417 demo requests, a 78.2% qualification rate and 59.7% form-to-demo — [RevenueHero Breaking Inbound #21](https://www.revenuehero.io/breaking-inbound/breaking-inbound-21)
- Michael Aagaard's controlled test cut a form from 9 to 6 fields, and conversions *dropped* 14%. The removed fields were the ones visitors engaged with most. CXL concludes that relevance and clarity matter more than raw field count — [CXL: Should You Really Reduce Form Fields?](https://cxl.com/blog/reduce-form-fields/)
- Speero: on average, the number of fields in a form makes no difference to its conversion rate. In a VWO case, Blivakker found that removing unnecessary fields helps, but removing too much hurts — [Speero anatomy of a web form](https://speero.com/post/anatomy-of-a-web-form-the-common-building-blocks-and-what-to-look-out-for-when-optimizing); [VWO form fields](https://vwo.com/blog/ab-testing-form-fields-increase-conversions/)
- Unbounce advises two or fewer fields. A secondary source cites 13.4% median conversion for email-only forms over 1.4M forms, which I could not verify in Unbounce's own report — [Unbounce (via search)](https://unbounce.com/?p=102979); [SaaSHero (secondary)](https://www.saashero.net/google-ppc/landing-page-performance-benchmarks/)
- Show rate: Calendly says its sales users cut no-shows ~28% on average with automated reminders (self-reported; 88% of surveyed users reported fewer no-shows) — [Calendly blog](https://calendly.com/blog/reduce-no-show-rates-sales)
- RevenueHero found a 6.5% aggregate no-show rate across 6,428 meetings, with 76.1% completion — [RevenueHero no-show post](https://revenuehero.io/blog/ways-to-reduce-no-show-rates-in-sales-calls)
- One company blog reports that adding a single qualifying question to its booking form brought no-shows back to 9% within three weeks. The same post found 60-minute calls had 2.5x the cancellation rate of 30-minute calls. These are anecdotes — [Cotera](https://cotera.co/articles/meeting-no-show-tracking-ai)
- Default.com also publishes no-show reduction guidance, but it is advice, not controlled data — [Default](https://www.default.com/post/how-to-reduce-no-shows-appointments)

### Inferences
- **Instant scheduling vs "we'll contact you": strong.** Two independent vendors with million-plus samples agree on roughly 2x. Both sell the product, but the direction is consistent. For this page, the embedded Calendly already captures most of this benefit.
- **Two-step (short form, then calendar) vs calendar only: moderate for "don't ask twice".** If a short qualifying form comes first, its answers must prefill or pass into Calendly so nothing is asked again. Otherwise Chili Piper's double-form penalty applies.
- **Field count: moderate, and it conflicts with folklore.** Aagaard, Speero and RevenueHero's 2 vs 13 field data all argue against cutting fields blindly; Unbounce argues for fewer. Resolution: keep only fields that are relevant and ideally *motivating* for the prospect to answer, such as monthly ad spend, store platform or current WhatsApp use. Drop administrative ones.
- **Qualifying questions and show rate: weak.** The evidence is anecdotal. Plausibly, 2–3 questions (revenue band, ad spend, uses Meta ads) filter out low-fit wellness brands and raise attendance, at the cost of volume. Measure booked-and-held per visitor, not raw bookings.
- **Reminders: moderate.** Calendly is self-reported but large. Turn on email and SMS reminders, plus a WhatsApp reminder, which fits this offer.
- Calendar load speed matters on mobile. Lazy-load the Calendly embed only when it nears the viewport, or show a fast placeholder.

### Gaps
- No independent (non-vendor) controlled test found comparing form-then-calendar against calendar-only.
- No Calendly-published data found on conversion by number of booking-form questions.
- No dataset found reporting show rate as a function of qualifying-question count.
- Benchmarks use inconsistent definitions (qualified vs all submissions, booked vs held), so they are not directly comparable.

## Page length: long vs short for higher-consideration offers; single CTA vs multiple; removing navigation; sticky mobile CTA

### Takeaway
Long pages can win for higher-consideration offers when the extra length answers real objections; the CRE Crazy Egg and Moz cases are the canonical examples. They are not universal. Removing navigation has **moderate** support (HubSpot, VWO and Yuppiechef), and the lift is bigger for mid-funnel pages. Single-goal pages with repeated CTAs are the consistent pattern. I found no rigorous public test on sticky mobile CTAs.

### Cited Findings
- Conversion Rate Experts reports growing Crazy Egg's conversion rate 363% in total. A new homepage about 20x longer than the original lifted sign-ups ~30%, with further optimisation accounting for the rest. Visitors had many questions, and the long page answered them. This is the agency's own case study — [CRE Crazy Egg case study](https://conversion-rate-experts.com/crazy-egg-case-study/); [Koozai summary](https://koozai.com/?p=201591)
- Copyhackers later tested Crazy Egg's homepage messaging and noted that long copy isn't the only way to win — [Copyhackers](https://copyhackers.com/?p=7755)
- Unbounce guidance (correlational benchmark): form-fill pages perform best under ~300 words. This conflicts with the CRE long-page cases — [Unbounce benchmark (via search)](https://unbounce.com/?p=102979)
- HubSpot A/B tested 5 landing pages with and without navigation. Top-of-funnel pages saw a 0–4% lift; middle-of-funnel pages saw 16% and 28% lifts. No sample sizes or significance were published — [HubSpot blog](https://blog.hubspot.com/marketing/landing-page-navigation-ht)
- VWO: Yuppiechef removed the navigation menu from a wedding registry landing page, and conversion rose from 3% to 6% (+100%) — [VWO case study](https://vwo.com/blog/a-b-testing-case-study-navigation-menu/)
- CXL takes a nuanced view: removing navigation suits single-purpose campaign pages, but visitors who need to verify trust may want an exit to supporting info — [CXL navigation on landing pages](https://cxl.com/blog/use-navigation-landing-pages-data-driven-consideration/)
- NN/g: 57% of viewing time is above the fold and 74% in the first two screens, so content further down is seen by fewer people — [NN/g](https://www.nngroup.com/articles/scrolling-and-attention/)

### Inferences
- **Long vs short: moderate, but conflicting.** For a done-for-you, higher-ticket B2B service bought by cold Meta traffic, the CRE logic applies: there are many objections to answer (Will AI sound off-brand? WhatsApp policy compliance? Cost? Setup effort?). Reconcile this with the attention data by putting the CTA and core proof on screen one, then adding objection-handling sections, each followed by a repeated CTA, for those who scroll.
- **Remove navigation: moderate.** The audit-booking page is effectively middle-of-funnel (a high-commitment ask), the stage where HubSpot saw its larger lifts. Keep the logo and maybe a minimal footer link for trust.
- **Single CTA, repeated: moderate (consensus from nav-removal logic).** One action, "Book your free audit", repeated, with no competing CTAs such as "download guide" or "follow us".
- **Sticky mobile CTA: weak.** No controlled public test found. It is low risk and worth A/B testing given mobile-heavy traffic.

### Gaps
- No controlled long-vs-short test found specifically for B2B call-booking pages.
- No published controlled test found for sticky mobile CTA bars on lead-gen pages.
- HubSpot's nav test lacks published sample sizes.

## Video / VSL: does it lift booked calls?

### Takeaway
The evidence is **weak and mixed**. Video sometimes helps for complex offers and sometimes hurts. I found no rigorous public test showing that a VSL lifts *booked calls*. Treat a short explainer or demo video as a test variant, not a default.

### Cited Findings
- A summary of Unbounce's analysis says video is "not a magic bullet" for conversion and should be tested — [martech.zone](https://martech.zone/landing-page-conversion-rates/)
- One agency reports a 27% average lift from explainer videos on complex product pages, with shorter videos performing better. This is self-reported with no method — [Over The Top SEO (secondary)](https://www.overthetopseo.com/?p=53463)
- Single Grain describes a test where a static image beat a video for a less video-savvy audience — [Single Grain](https://www.singlegrain.com/blog-posts/conversions/5-important-landing-page-elements-you-should-be-ab-testing/)
- CXL Institute ran original research on whether the opt-in offer format (video, PDF or web content) affects opt-in rates. I could not retrieve the findings — [CXL research study](https://cxl.com/research-study/email-opt-in-offer-video-pdf-web-content/)
- GoodUI has a Video Testimonials pattern (#48), but its effect is paywalled — [GoodUI #48](https://goodui.org/patterns/48)

### Inferences
- For an AI WhatsApp assistant, a short screen recording of a real WhatsApp conversation (the product working) is more likely to help than a talking-head VSL, because it makes an abstract product concrete. This is an inference.
- Video costs page weight on mobile, which works against the speed evidence below. Use a poster image and click-to-play, and never autoplay a heavy embed above the fold.

### Gaps
- No controlled test found measuring VSL impact on booked or held calls.
- CXL's video vs PDF opt-in study results not retrieved.

## Risk reversal and offer framing: "free audit", guarantees, "you keep the plan", pricing transparency

### Takeaway
Guarantees have **weak to moderate** support from e-commerce tests, mostly confounded single tests with 20–33% lifts. I found no controlled evidence on "free audit" wording, "you keep the plan" framing, or pricing transparency on B2B call-booking pages. These are reasonable hypotheses, not proven patterns.

### Cited Findings
- In a VWO case, Understand Quran Academy added a money-back guarantee icon *and* an App Store icon to its sign-up page. Sales rose 32.57% at 98% significance over 11 days. The two changes are confounded — [VWO success story](https://vwo.com/success-stories/understandquran/); [casestudies.com](https://www.casestudies.com/company/vwo/case-study/education-services-company-tests-elements-to-boost-revenue-using-vwo)
- Blend Commerce: a health brand placed a "No Reaction Money Back Guarantee" below add-to-cart and saw a 30.33% conversion increase. This is supplement e-commerce, relevant to the client's own customers, but not to this B2B page — [Blend Commerce](https://blendcommerce.com/blogs/ab-tests-shopify/30-33-increase-in-conversion-rate)
- A VWO trust-badge test (UptoWork) showed only a 1.25% increase, so not every risk-reduction element moves the needle — [VWO UptoWork](https://vwo.com/blog/uptowork-reduced-the-cart-abandonment-rate/)
- An Unbounce author cautions that large single-test lifts, such as a "160% from one word" claim, are often statistically invalid — [Unbounce](https://unbounce.com/conversion-rate-optimization/the-biggest-little-change-i-ever-made/)
- CRE's own lead-gen offer is a "free strategy session", the same free-audit framing. This shows practitioner adoption, not test evidence — [CRE request-received page](https://conversion-rate-experts.com/request-received)

### Inferences
- "Free 30-minute audit" plus "you keep the plan whether or not you hire us" lowers the perceived cost of booking. This is consistent with the guarantee evidence, but untested here.
- A performance guarantee on the *service* (for example "if we don't hit X in 60 days, you don't pay month 3") is the B2B analogue of the money-back guarantee. Make it only if it is real and can be honoured.
- Pricing transparency ("plans from $X/month") would likely reduce bookings but raise lead quality and show rate. No evidence found either way, so it is a candidate for an A/B test measuring held calls.

### Gaps
- No controlled test found on "free audit" vs "consultation" vs "demo" wording.
- No controlled test found on showing pricing on B2B service landing pages and its effect on bookings or show rate.
- No B2B service-guarantee A/B test found.

## Speed and mobile: Google/Deloitte "Milliseconds make millions", Portent load-time studies, mobile share of Meta traffic

### Takeaway
Speed has **strong directional** evidence: several large datasets agree that faster pages convert better. Most of it is correlational or observational, though, and Deloitte's lead-gen finding is about engagement, not conversion. For mobile-heavy Meta traffic, speed is a top-priority, low-regret investment.

### Cited Findings
- Deloitte and Fifty-five, commissioned by Google, studied 37 brands' mobile sites over 4 weeks. A 0.1s mobile speed improvement was associated with +8.4% conversions for retail and +10.1% for travel. For **lead-gen** sites, the reported effect was +7% page views, along with gains in funnel progression (homepage to form step 1: +5.5%; form step 1 to submission: +21.6%). The study is observational: it compares brands' own speed changes, not randomised tests — [web.dev case study](https://web.dev/case-studies/milliseconds-make-millions); [Deloitte report PDF](https://www2.deloitte.com/content/dam/Deloitte/ie/Documents/Consulting/Milliseconds_Make_Millions_report.pdf)
- Portent (April 2022), 20 sites (14 B2B lead gen, 6 e-commerce), ~100M page views:
  - B2B lead-gen pages loading in 1s convert at about 40%, 34% at 2s and 29% at 3s.
  - A 1s page converts 3x better than a 5s page, and about 5x better than a 10s page.
  - 82% of B2B pages loaded within 5s.

  The method is observational. The page doesn't say how load time was measured or control for confounders, and its "conversion rate" figures are unusually high, so they are likely a site-specific goal metric — [Portent](https://www.portent.com/blog/analytics/research-site-speed-hurting-everyone.htm)
- Chili Piper notes calendar widgets vary from 3–4s to 30–45s to load, and says slow loads cause abandonment. No figure is given — [Chili Piper 2024 Benchmark](https://chilipiper.com/post/form-conversion-rate-benchmark-report)
- Mobile share of Meta traffic: Facebook's last disclosed mobile-only figure was 526M users in Q4 2014 (37.8% of MAU). Mobile was 73% of ad revenue by Q1 2015. A Statista figure cited by Agorapulse (January 2020) put mobile-only Facebook users at 79% — [Search Engine Journal (2015)](https://www.searchenginejournal.com/facebook-reaches-1-39b-monthly-active-users-half-billion-mobile/124675/); [ITPro](https://www.itpro.co.uk/strategy/24495/mobile-now-gives-facebook-73-of-its-ad-revenue); [Agorapulse](https://www.agorapulse.com/social-media-lab/facebook-mobile-ads-vs-desktop-ads/)

### Inferences
- **Speed: strong directional, moderate on magnitude.** Expect real but smaller gains than the headline figures.
- Meta ad clicks open in the in-app browser on phones. The landing page should be judged on a mobile Lighthouse or real-user LCP target of about 2.5s or less. Defer the Calendly script; avoid heavy hero video, large fonts and third-party trackers beyond the Meta Pixel/CAPI.
- The client's own Meta Ads Manager placement and device breakdown is the authoritative mobile-share source. Public figures are outdated.

### Gaps
- No current (2023+) official Meta figure found on the mobile share of ad clicks or traffic.
- No randomised (as opposed to observational) speed test found specifically for B2B lead-gen pages.
- Portent's load-time metric definition is unstated.

## Urgency/scarcity and limited slots: evidence and risks

### Takeaway
The evidence is **weak and conflicting**. Real, believable deadlines can lift conversion. Fake or always-on urgency erodes trust, and one practitioner test showed a 3–4% *drop*. For a B2B audit call, an honest capacity statement ("we onboard N brands per month") is the defensible form; countdown timers are not recommended.

### Cited Findings
- Secondhand summaries of CXL say scarcity works only if it is believable, and that clear deadlines beat vague "limited time" offers. I could not locate the primary CXL source — [Conversion Ledger (secondary)](https://conversionledger.beehiiv.com/p/scarcity-messaging-when-urgency-drives-conversions-and-when-it-backfires); [GrowthSuite (secondary)](https://www.growthsuite.net/blog/a-b-testing-your-urgency-tactics-what-to-measure)
- A practitioner reports a checkout "rate guarantee" countdown timer cut conversions 3–4%, an estimated $250K–$500K loss. This is a single test — [Atticus Li](https://atticusli.com/blog/posts/stop-adding-urgency-timers-to-your-checkout-the-data-says-youre-wrong)
- Obvi tested a live countdown tied to a real price change against a static "Ends Sunday" banner; the countdown won by 7–8%. Single vendor test, e-commerce, real deadline — [Quikly scarcity examples](https://hq.quikly.com/blog/scarcity-marketing-examples)
- Multiple sources warn that resetting timers and stock counts that never change are recognised as fake and damage trust — [GrowthSuite real vs fake urgency](https://www.growthsuite.net/blog/real-urgency-vs-fake-urgency-why-your-countdown-timers-are-not-working)

### Inferences
- The two tests conflict. The differences are a real vs implied deadline, and checkout vs earlier in the funnel. Real constraints help; pressure at the moment of commitment hurts.
- For premium wellness brands, where the founder or marketing lead is evaluating a partner, fake scarcity risks credibility with a sceptical B2B buyer. The calendar's own limited availability is natural, honest scarcity.

### Gaps
- No controlled test found on "limited slots" messaging for B2B call booking.
- Primary CXL scarcity research not retrieved.
- No data found on whether scarcity affects show rate or lead quality.

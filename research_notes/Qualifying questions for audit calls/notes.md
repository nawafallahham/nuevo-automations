# Qualifying questions before the audit call (Nuevo Automations)

Researched 2026-11-20, about 15 searches and fetches. Most sources are vendors that sell scheduling or routing tools (Calendly, Chili Piper, RevenueHero, Default). They have an interest in "qualify before booking" and "embed the calendar", so treat their conversion claims as directional. No source published a controlled A/B test for our exact case: a Meta-ads, mobile, GCC e-commerce audience.

---

## 1. Which questions predict a qualified call that shows up and closes

What the sources agree on:
- Map each must-have criterion to one question with selectable options. Missing a must-have means automatic disqualification. Nice-to-haves only add points. ([orbitforms](https://orbitforms.ai/blog/pre-qualify-leads-with-forms), [Proposify](https://www.proposify.com/blog/disqualify-lead-qualification-process))
- Put the most important qualification questions at the top, and get the rest from data you already have (UTM, ad source) instead of asking. ([Default](https://www.default.com/post/inbound-lead-qualification))
- Warning: asking for budget before the call can filter out good prospects ([orbitforms](https://orbitforms.ai/blog/pre-qualify-leads-with-forms)). That matters here, because the sprint asks the brand to pay only its own ad spend, so an "ad budget" question can read like a fee.
- E-commerce agency application forms usually ask for monthly revenue in ranges, current and planned ad spend, and start timeline ("this month / 1–3 months / just exploring"). Examples: [websitesthatsell](https://www.websitesthatsell.com.au/strategy-session-application), [mbadv](https://www.mbadv.agency/book-a-call), and various Tally forms.

Ranking for this offer (my judgement, based on the page's stated criteria and the sprint's mechanics):

| Rank | Criterion | Why it predicts a good call | Keep? |
|---|---|---|---|
| 1 | Selling online every week (weekly orders) | Without existing demand and checkout the 7-day sprint has nothing to scale or measure. Hard must-have. | **Keep** |
| 2 | Own Meta ad account + willing to fund spend | The sprint needs their ad account and their money. Hard must-have. | **Keep** (one question covering account + spend) |
| 3 | Average order value | AED 150+ makes click-to-WhatsApp CPA work and keeps it worth having a person or AI in the chat. Strong predictor of closeable economics. | **Keep** |
| 4 | Role / decision-maker | Main cause of calls that don't close and of "need to check with my partner". Cheap to ask. | **Keep** |
| 5 | Category (wellness/supplement/peptide) | Mostly already filtered by ad targeting and page copy. Can go in Q1's options or be dropped. | Merge into Q1 wording or drop |
| 6 | Timeline | Weak for a 7-day offer, since most people tapping a Meta ad say "now". Easy to game. | **Drop** |
| 7 | Current WhatsApp use | Useful context for the call, but not a pass/fail filter: we install the assistant anyway. | **Drop** from gate; ask as an optional Calendly booking question |
| — | Revenue | Weekly orders is a better and less sensitive stand-in than revenue for a mobile one-tap step. Owners hesitate to disclose revenue. | Use orders, not revenue |

## 2. Recommended questions, options (AED) and thresholds

Order: easy and identity-type questions first, money questions later (see section 3).

**Q1. What best describes your brand?** (identity, easy opener)
- Online store selling wellness / supplements / peptides → pass
- Online store, another category → pass, flagged in notes (judgement call: could be "soft fail")
- Not selling yet / launching soon → **fail**
- I'm an agency or freelancer → **fail** (soft, see section 4)

**Q2. Roughly how many orders do you get in a typical week?**
- Not selling yet → **fail**
- 1–10 → pass (judgement call: borderline; the page says "every week", so 1+ passes)
- 11–50 → pass
- 51–200 → pass
- 200+ → pass (priority)

**Q3. What's your average order value?**
- Under AED 100 → **fail**
- AED 100–149 → judgement call. Suggest **pass, flagged**, because "around AED 150" on the page is not a hard line and bundles can lift AOV
- AED 150–300 → pass
- AED 300–600 → pass
- AED 600+ → pass (priority)

**Q4. Meta ads: where are you today?** (combines own account + spend; avoids an outright "budget" question)
- Running ads from our own Meta ad account → pass
- Have our own ad account, not running right now → pass
- An agency runs ads in *their* account → pass, flagged (judgement call: they can create their own account; mention it on the call)
- No Meta ad account yet → **fail** (soft: offer a setup guide or WhatsApp)

Role question: four is the cap the brief sets, so add role as a **required Calendly booking question** ("Your role: Founder/owner · Co-founder/partner · Marketing lead · Other"). Don't make it a hard gate. Alternative: swap Q1 for role if ad targeting already guarantees the category. Judgement call: role is the stronger predictor of closing, category the stronger predictor of fit. If you must pick, **keep role and drop category**, because the ad and page already filter for category.

Optional ad-spend floor: if you want one, make Q4 "How much could you put into Meta ads during the 7-day sprint? Under AED 1,000 / 1,000–3,000 / 3,000–7,500 / 7,500+" with under AED 1,000 failing. This is a judgement call and was not found in any source. It adds friction and invites gaming, so I'd rather cover it on the call.

### FINAL recommended 4 (in order)
1. **Your role**: Founder / owner · Co-founder or partner · Head of marketing / e-com · Other (agency, freelancer, staff). Pass: first three. "Other" fails softly (agency message), or passes flagged if you'd rather not lose staff who can bring the owner.
2. **Orders per week**: Not selling yet · 1–10 · 11–50 · 51–200 · 200+. Fail: "Not selling yet". This also confirms they're e-commerce; category is left to the ads and page copy.
3. **Average order value**: Under AED 100 · AED 100–149 · AED 150–300 · AED 300–600 · AED 600+. Fail: under AED 100. AED 100–149 passes, flagged (judgement call).
4. **Meta ads today**: Running from our own ad account · Own account, paused · Agency runs them in their account · No ad account yet. Fail: "No ad account yet". Agency-owned passes, flagged (judgement call).
Then optional Calendly booking questions (not required): WhatsApp use today, product category, website URL.

## 3. Best practices for the question step

- **Multi-step, one question per screen.** Venture Harbour (agency, primary source, first-party data) moved a consulting lead form to multi-step and reported 0.96% → 8.1%. Their own posts quote slightly different baselines, so it's directional. "Up to 300%" is their headline. The often-repeated "86% higher" multi-step figure is unverified (only found in secondary blogs). ([Venture Harbour](https://ventureharbour.com/multi-step-lead-forms-get-300-conversions/), [VH form guide](https://ventureharbour.com/web-form-optimisation-ultimate-guide/))
- **Easy, low-friction question first; sensitive ones last**, once people have "skin in the game" ([Venture Harbour](https://ventureharbour.com/web-form-optimisation-ultimate-guide/)). So: identity → orders → AOV → ad account.
- **Big tap buttons, not dropdowns.** The HubSpot-attributed form study (about 40k landing pages, cited secondhand, original not verified) found select/dropdown fields hurt conversion more than simple inputs. On mobile, radio-style buttons are also one tap instead of two. Calendly routing logic only works on dropdown or radio questions anyway ([Calendly community](https://community.calendly.com/how-do-i-40/can-you-use-routing-in-calendly-to-qualify-based-on-zip-code-1693)).
- **Drop-off per question:** no clean primary source. Secondhand HubSpot numbers: 3 fields converted best (~25%) and going from 4 to 3 fields was cited as ~+50%. Formstack: forms over 7 fields hit ~68% abandonment. Counterpoint: ConversionXL/Unbounce saw removing 3 fields *lower* conversion by 14%, so relevance matters more than count. ([CXL](https://conversionxl.com/reduce-form-fields/), [HubSpot KB](https://knowledge.hubspot.com/forms/increase-form-conversion-rates), [reform](https://www.reform.app/blog/multi-step-form-drop-off-rates-how-to-reduce-them)) Practical reading: 4 one-tap questions with auto-advance is near the sweet spot. Don't add a 5th.
- **Progress indicator:** "1 of 4" or a thin bar. Standard multi-step practice (VH guide). No hard A/B data found.
- **Auto-advance on tap**, with a back link. Pre-select nothing.
- **Wording that doesn't feel like gatekeeping:** frame it as tailoring the audit ("4 quick taps so we can prepare your audit before the call") rather than "see if you qualify". Agency forms commonly use "see if we're a fit". Default recommends letting page copy do self-qualification by saying plainly whom you can and can't help ([Default](https://www.default.com/post/inbound-lead-qualification)), which the page already does.
- Speed-to-lead: Default and Chili Piper both stress a response within 5 minutes and booking inline, right after the form (vendor data). ([Default](https://www.default.com/post/inbound-lead-qualification), [Chili Piper](https://www.chilipiper.com/resources/blog/abandoning-booker-tips))
- Show rate: benchmarks conflict (inbound no-show ~15–35%). Vendors agree booking soon after the form helps (24h vs 3+ days out). Vendor-heavy sources: [RevenueHero](https://revenuehero.io/blog/ways-to-reduce-no-show-rates-in-sales-calls), [focus-digital](https://focus-digital.co/average-no-show-rate-for-booked-sales-meetings-by-booking-channel/). Implication: limit Calendly to the next 3–5 days and send a WhatsApp reminder.

## 4. Handling disqualified visitors

What tools do natively:
- Calendly routing forms have three route types: event type (qualified), **custom message** (disqualified), **external URL**, plus a fallback route ([Calendly](https://calendly.com/help/how-to-create-a-routing-form)). A Calendly community tip: send screened-out people to a message or URL with "next steps or alternative options" ([Calendly community](https://community.calendly.com/featured-tips-tricks-32/12-days-of-calendly-day-10-routing-for-teams-527)).
- RevenueHero: an "If Prospect Disqualified" redirect URL, with different pages for different disqualification reasons ([RevenueHero](https://help.revenuehero.io/rules/redirect-rules)).
- Chili Piper: the calendar shows "assuming you do not disqualify yourself". No documented resources page; redirect is DIY ([Chili Piper help](https://help.chilipiper.com/hc/en-us/articles/360054168674)).
- Default and Close: don't throw them away. Nurture good-fit-but-early leads and keep them out of sales sequences ([Default](https://www.default.com/post/lead-follow-up), [Close](https://close.com/blog/how-to-qualify-leads-fast)).

Recommendations (synthesis; no source gave exact copy):
- **Tailor the decline to the failing answer** (RevenueHero pattern). Example outcomes:
  - Not selling yet / no ad account: "We're built for brands that are already taking orders through their own Meta ad account. Once you're there, we'd love to look at it. Meanwhile, here's [the checklist we use to get a brand sprint-ready]." Add a WhatsApp button: "Ask us a quick question".
  - Low AOV: "At this order value, click-to-WhatsApp ads usually don't pay back yet, so a call wouldn't be a good use of your time. If you're adding bundles or higher-priced products, message us on WhatsApp."
  - Agency: "We work directly with brands. Message us on WhatsApp if you'd like to talk about partnering."
- **Be transparent about the criteria, not the scoring.** The page already says "selling every week, own Meta ad account, AOV around AED 150+". Repeating that in the decline feels honest and matches the page. Don't show a live "you failed because <X>" on each tap, and don't let people step back and change only the failing answer without friction. Judgement call: a back button is fine, because a determined person can game any self-reported form. The call itself is the real check.
- **Anti-gaming:** ranges instead of exact numbers; failing options shouldn't look like the "wrong" answer (mix their position, avoid "Under AED 100 (not a fit)"-style labels); store the answers and verify on the call (screen-share of Ads Manager or Shopify). Optional: record the fail in localStorage so a refresh shows the same decline. This is a soft measure only.
- Always give a **next step**: WhatsApp chat (matches the product and the audience), a free resource, or "notify me". Never a dead end.

## 5. Passing answers into Calendly (no second form)

- **Inline embed prefill (official):** `Calendly.initInlineWidget({ url, parentElement, prefill: { name, email, customAnswers: { a1: '...', a2: '...' } } })`. `a1`–`a10` map to the event's custom questions **in the order they appear on the event type**. Use `firstName`/`lastName` if the event splits the name. ([Calendly](https://calendly.com/help/how-to-pre-fill-invitee-information-in-an-embed))
- **URL params** work on booking links too: `?name=..&email=..&a1=Answer%20text` ([Calendly help](https://help.calendly.com/hc/en-us/articles/226766767)).
- **Caveats:** for dropdown or radio booking questions the prefill value must exactly match the option text, not its position ([community](https://community.calendly.com/api-webhook-help-61/scheduling-page-url-parameter-dropdown-not-working-773)). Parameter names can't be customised. Prefilled fields stay visible and editable; there's no official "hide prefilled question" option. Practical tip: make these booking questions **short-answer text (not required)** so any value is accepted and shows in the event notes.
- **Calendly Routing Forms** (Professional plan or above) can do the gating natively: radio/dropdown logic → event / custom message / external URL. They can be prefilled with `?a1=..&autofill=true` to auto-route ([Calendly](https://calendly.com/help/how-to-pre-populate-invitee-answers-in-routing-forms)). But no source confirms routing answers carry over into the booking form ([community thread](https://community.calendly.com/how-do-i-40/pre-populating-booking-form-fields-using-answers-from-routing-form-1647)). Calendly's look is also less on-brand on mobile.
- **Recommendation:** keep the custom 4-tap step on the page (brand control, instant tailored decline, analytics on each tap). On pass, load the inline embed with `customAnswers` prefilled. On fail, show the tailored decline. You get one experience and no second form. Also fire a Meta Pixel / CAPI event for "Qualified" vs "Disqualified" so ads can optimise on qualified leads (my suggestion, not sourced).

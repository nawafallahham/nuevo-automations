#!/usr/bin/env python3
"""Build the Arabic pages under /ar/ (right to left).

They share the <head> assets with the rest of the site (the head:start/end markers
are filled by tools/sync_partials.py), but carry their own Arabic header and footer,
so sync_partials leaves those alone. Each page names its English twin for hreflang;
the English pages carry the matching alternate links (see ALTERNATES below, applied
to the English files by this script too).

Usage: python3 tools/build_ar.py && python3 tools/sync_partials.py
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://nuevoautomations.com"
WA_AR = "https://wa.me/15557738409?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%D8%8C%20%D8%A3%D8%B1%D9%8A%D8%AF%20%D8%A3%D9%86%20%D8%A3%D8%B9%D8%B1%D9%81%20%D8%A7%D9%84%D9%85%D8%B2%D9%8A%D8%AF%20%D8%B9%D9%86%20M2S."
DATE = "2026-11-28"


def e(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '  <script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n  </script>\n"


def alt_links(en_path, ar_path):
    return (f'  <link rel="alternate" hreflang="en" href="{SITE}{en_path}">\n'
            f'  <link rel="alternate" hreflang="ar" href="{SITE}{ar_path}">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{SITE}{en_path}">\n')


HEADER = """  <header class="nav nav--centre">
    <div class="wrap nav__bar">
      <a class="skip-link" href="#top">انتقل إلى المحتوى</a>
      <a class="nav__logo" href="/ar/" aria-label="Nuevo Automations، الصفحة الرئيسية بالعربية"><img class="nav__logo-img" src="/assets/logo-72.webp" alt="" width="28" height="28"><span translate="no">Nuevo Automations</span></a>
      <nav class="nav__links" aria-label="القائمة الرئيسية">
        <div class="nav__item"><a class="nav__link" href="/ar/#how">كيف يعمل M2S</a></div>
        <div class="nav__item"><a class="nav__link" href="/ar/whatsapp-automation-uae/">أتمتة واتساب</a></div>
        <div class="nav__item"><a class="nav__link" href="/ar/guides/">الأدلة</a></div>
        <div class="nav__item"><a class="nav__link" href="/ar/#results">النتائج</a></div>
        <div class="nav__item"><a class="nav__link lang-switch" href="{en}" hreflang="en" lang="en">English</a></div>
      </nav>
      <div class="nav__actions">
        <a class="btn btn--primary js-lead" data-lead="ar-header" href="/book/">احجز تدقيقاً مجانياً</a>
      </div>
      <button class="nav__toggle" type="button" aria-expanded="false" aria-label="القائمة">
        <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
      </button>
    </div>
  </header>"""

FOOTER = """  <footer class="footer closing footer--dark ground-inverse g2m" id="contact" aria-labelledby="close-h">
    <div class="wrap">
      <div class="closing__cta close--word">
        <div class="section-head--split">
          <div><h2 id="close-h">احجز تدقيقاً مجانياً</h2><p class="t-lead">30 دقيقة عبر Zoom بالعربية أو الإنجليزية. تحتفظ بالخطة المكتوبة في كل الأحوال.</p></div>
          <a class="btn btn--primary js-lead" data-lead="ar-footer" href="/book/">احجز تدقيقاً مجانياً</a>
        </div>
        <p class="close__word" aria-hidden="true" translate="no">Nuevo Automations</p>
      </div>
      <div class="closing__links">
        <div class="grid">
          <div class="span-4 stack-4">
            <p class="footer__lede">إعلانات Meta وGoogle تجلب المشترين إلى واتساب، وM2S، مساعد المبيعات بالذكاء الاصطناعي الذي يُتمّ البيع داخل المحادثة.</p>
            <p class="t-small"><span translate="no">Nuevo Automations FZE LLC</span><br>مركز الأعمال، المنطقة الحرة لمدينة الشارقة للنشر<br>الشارقة، الإمارات · رقم الرخصة 4431808.01</p>
          </div>
          <div class="span-2 footer__col"><h3>بالعربية</h3><ul><li><a href="/ar/">الصفحة الرئيسية</a></li><li><a href="/ar/whatsapp-automation-uae/">أتمتة واتساب للأعمال</a></li><li><a href="/ar/guides/whatsapp-green-tick-uae/">توثيق واتساب للأعمال</a></li><li><a href="/ar/guides/bulk-whatsapp-messages-uae/">رسائل واتساب جماعية</a></li><li><a href="/ar/guides/whatsapp-business-api-pricing-uae/">أسعار واتساب API</a></li><li><a href="/ar/guides/whatsapp-business-app-vs-api/">واتساب للأعمال أم API</a></li><li><a href="/ar/guides/whatsapp-marketing-rules-uae/">قواعد التسويق عبر واتساب</a></li><li><a href="/ar/guides/whatsapp-payment-links-uae/">الدفع عبر واتساب</a></li><li><a href="/ar/guides/sell-supplements-online-uae/">بيع المكملات أونلاين</a></li><li><a href="/ar/guides/click-to-whatsapp-ads/">إعلانات النقر إلى واتساب</a></li><li><a href="/ar/guides/whatsapp-abandoned-cart-recovery/">السلات المتروكة</a></li></ul></div>
          <div class="span-2 footer__col" lang="en" dir="ltr"><h3>In English</h3><ul><li><a href="/">Home</a></li><li><a href="/m2s/">How M2S works</a></li><li><a href="/results/">Results</a></li><li><a href="/pricing/">Pricing</a></li><li><a href="/guides/">Guides</a></li></ul></div>
          <div class="span-2 footer__col"><h3>تواصل معنا</h3><ul><li><a href="https://wa.me/15557738409" target="_blank" rel="noopener">واتساب <span dir="ltr">+1 555-773-8409</span></a></li><li><a href="mailto:nawafallahham@nuevoautomations.com">البريد الإلكتروني</a></li><li><a href="https://www.instagram.com/nuevoautomations/" target="_blank" rel="noopener me">Instagram</a></li><li><a href="https://www.linkedin.com/company/nuevoautomations/" target="_blank" rel="noopener me">LinkedIn</a></li></ul></div>
        </div>
        <div class="footer__legal">
          <span>&copy; 2026 <span translate="no">Nuevo Automations FZE LLC</span> &nbsp; <a href="/privacy/">سياسة الخصوصية (بالإنجليزية)</a></span>
        </div>
      </div>
    </div>
  </footer>

  <nav class="actionbar" aria-label="إجراءات سريعة">
    <a class="btn btn--primary js-lead" data-lead="ar-mobile-bar" href="/book/">احجز تدقيقاً مجانياً</a>
  </nav>

  <script type="module" src="/kit/system.js"></script>
  <script type="module" src="/kit/motion/motion.js"></script>
  <script src="/js/track.js" defer></script>
  <script src="/js/script.js" defer></script>"""


def page(path, en_path, title, desc, ld_blocks, main):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{url}">
{alt_links(en_path, path)}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nuevo Automations">
  <meta property="og:locale" content="ar_AE">
  <meta property="og:locale:alternate" content="en_AE">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}/assets/og-card.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{SITE}/assets/og-card.jpg">

  <!-- head:start -->
  <!-- head:end -->

{''.join(ld(b) for b in ld_blocks)}</head>
<body>
{HEADER.replace('{en}', en_path)}

  <main id="top">
{main}
  </main>

{FOOTER}
</body>
</html>
"""


def faq_block(faqs, heading):
    items = "\n".join(f'          <div class="faq__item"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in faqs)
    return f"""    <section class="band ground-surface" aria-labelledby="faq-h">
      <div class="wrap grid">
        <div class="span-5 stack-4"><h2 id="faq-h">{e(heading)}</h2><p><a class="link" href="{WA_AR}" target="_blank" rel="noopener">اسألنا على واتساب</a></p></div>
        <div class="faq span-6 start-7">
{items}
        </div>
      </div>
    </section>"""


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ar", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def webpage(path, name, desc):
    return {"@context": "https://schema.org", "@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path,
            "name": name, "description": desc, "inLanguage": "ar", "dateModified": DATE,
            "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}}


def cta(lead):
    return f"""        <div class="btn-row">
          <a class="btn btn--primary js-lead" data-lead="{lead}" href="/book/">احجز تدقيقاً مجانياً</a>
          <a class="btn btn--secondary" href="{WA_AR}" target="_blank" rel="noopener">راسلنا على واتساب</a>
        </div>"""


# ------------------------------------------------------------------ /ar/
HOME_FAQ = [
    ("لماذا نرسل الإعلانات إلى واتساب بدل الموقع؟", "مشتري المكملات الغذائية يسأل قبل أن يدفع: عن المكونات والجرعة والتوصيل. صفحة الهبوط لا تجيبه، أما في واتساب فيحصل على الإجابة خلال ثوانٍ ويدفع في المحادثة نفسها."),
    ("كم تكلفة M2S؟", "رسوم شهرية ثابتة واحدة، نرسلها مكتوبة بعد التدقيق المجاني. ميزانية الإعلانات تدفعها مباشرة إلى Meta أو Google وليست ضمن رسومنا."),
    ("هل أحتاج إلى رقم واتساب جديد؟", "لا. يعمل M2S على رقمك الحالي، ويستمر فريقك في استخدام تطبيق واتساب للتدخل في أي محادثة."),
    ("هل يرد المساعد بالعربية؟", "نعم. يرد بالعربية أو الإنجليزية، باللغة التي يكتب بها العميل."),
    ("ماذا يفعل المساعد إذا لم يعرف الإجابة؟", "لا يخترع أسعاراً أو منتجات أبداً. يحوّل المحادثة إلى فريقك فوراً مع تنبيه على واتساب وملخص للمحادثة."),
    ("هل تضمنون النتائج؟", "لا. نضمن أن كل محادثة تحصل على رد خلال ثوانٍ وأن كل مشترٍ صامت يحصل على متابعة، ويُظهر التقرير الشهري ما الذي عاد من مبيعات."),
]
HOME_TITLE = "مبيعات واتساب بالذكاء الاصطناعي لعلامات المكملات | Nuevo"
HOME_DESC = "ندير إعلانات Meta وGoogle إلى واتساب لعلامات العافية والمكملات في الإمارات، ويرد M2S خلال ثوانٍ ويُتمّ البيع ويتابع. احجز تدقيقاً مجانياً لمدة 30 دقيقة."
home_main = f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <h1 id="page-h">إعلانات تفتح محادثة واتساب، وذكاء اصطناعي يُتمّ البيع فيها</h1>
        <p class="t-lead">Nuevo Automations وكالة تسويق في الإمارات لعلامات العافية والمكملات الغذائية. ندير إعلانات Instagram وFacebook وGoogle التي ترسل المشترين إلى واتساب، ويرد مساعدنا M2S على كل محادثة خلال ثوانٍ بالعربية أو الإنجليزية، ويُتمّ البيع، ويتابع من لم يدفع.</p>
{cta('ar-hero')}
        </div>
      </div>
    </section>

    <section class="band" aria-label="الإجابة المختصرة">
      <div class="wrap">
        <div class="answer"><p>M2S (من الرسالة إلى البيع) نظام مبيعات على واتساب: إعلانات Meta بنقرة إلى واتساب تجلب المشتري إلى المحادثة، ومساعد بالذكاء الاصطناعي مدرَّب على منتجاتك وأسعارك وسياساتك يجيب ويُتمّ الطلب برابط دفع أو بالدفع عند الاستلام، ثم يتابع السلال المتروكة وروابط الدفع غير المدفوعة والعملاء الصامتين. يعمل على رقم واتساب الخاص بك، وتحصل على تقرير شهري بالمحادثات والطلبات والإيرادات.</p></div>
      </div>
    </section>

    <section class="band" id="how" aria-labelledby="how-h">
      <div class="wrap grid">
        <div class="span-5 stack-4">
          <h2 id="how-h">كيف يبيع M2S في ثلاث خطوات</h2>
          <p>الإعلان والمحادثة والمتابعة يديرها فريق واحد، لذلك نقيس شيئاً واحداً: أي إعلان جلب البيع.</p>
        </div>
        <ol class="rows span-6 start-7" aria-label="خطوات M2S">
          <li><span class="rows__name">1. الإعلان يفتح محادثة</span><p>إعلانات على Instagram وFacebook وGoogle، زرّها يفتح واتساب مباشرة بدل صفحة هبوط.</p></li>
          <li><span class="rows__name">2. المساعد يرد ويبيع</span><p>يجيب عن الأسئلة خلال ثوانٍ، يقترح الباقة المناسبة، ويرسل رابط الدفع أو يؤكد الدفع عند الاستلام.</p></li>
          <li><span class="rows__name">3. المتابعة تستعيد ما ضاع</span><p>رسائل متابعة للسلال المتروكة وروابط الدفع غير المدفوعة والعملاء الصامتين، مع ساعات هادئة واحترام طلبات إيقاف الرسائل.</p></li>
        </ol>
      </div>
    </section>

    <section class="band" id="results" aria-labelledby="results-h">
      <div class="wrap grid">
        <div class="span-5 stack-4">
          <h2 id="results-h">ما تقوله العلامات التي تستخدم M2S</h2>
          <p>أرقام حقيقية من عملائنا، وتختلف النتائج من علامة إلى أخرى. لا نضمن نتائج.</p>
        </div>
        <ul class="rows span-6 start-7" aria-label="النتائج">
          <li><span class="rows__name">Peak Labs: طلبات شهرية أكثر بنسبة 53%</span><p>علامة مكملات إماراتية على M2S منذ يونيو 2026: أول رد أسرع 90 مرة، و74% من المحادثات تُدار دون تدخل بشري (حتى أكتوبر 2026). <a href="/results/peak-labs/" hreflang="en">دراسة الحالة (بالإنجليزية)</a></p></li>
          <li><span class="rows__name">Khaleej ParaPharma: عائد إعلاني 19.6 ضعفاً في المتوسط</span><p>إعلانات Meta إلى واتساب مع M2S منذ مايو 2026، بمتوسط 19.6 ضعفاً عبر 14 حملة حسب تقدير Meta، و29.9 ضعفاً في أفضل حملة. هذه ليست نتيجة نموذجية. <a href="/results/khaleej-parapharma/" hreflang="en">دراسة الحالة (بالإنجليزية)</a></p></li>
        </ul>
      </div>
    </section>

    <section class="band" aria-labelledby="who-h">
      <div class="wrap grid">
        <div class="span-5 stack-4">
          <h2 id="who-h">مصمَّم لعلامات العافية والمكملات المميزة</h2>
          <p>نعمل مع متاجر إلكترونية في دبي وأبوظبي والشارقة وباقي الإمارات تبيع المكملات ومنتجات العافية، وتستثمر في الإعلانات أو مستعدة لذلك، وتريد أن تتحول رسائل أكثر إلى طلبات مدفوعة.</p>
        </div>
        <ul class="rows rows--plain span-6 start-7">
          <li><span class="rows__name">يعمل على رقم واتساب الخاص بك وعلى واجهة WhatsApp Business API الرسمية</span></li>
          <li><span class="rows__name">يرد بالعربية والإنجليزية، باللغة التي يكتب بها العميل</span></li>
          <li><span class="rows__name">لا يخترع أسعاراً أو منتجات، ويحوّل الحالات الصعبة إلى فريقك</span></li>
          <li><span class="rows__name">المبيعات من المحادثات تُرسَل إلى Meta لقياس العائد الحقيقي للإعلانات</span></li>
          <li><span class="rows__name">تقرير شهري: المحادثات والطلبات والإيرادات وما استعادته المتابعات</span></li>
        </ul>
      </div>
    </section>

    <section class="band" aria-labelledby="guides-h">
      <div class="wrap grid">
        <div class="span-5 stack-4">
          <h2 id="guides-h">أدلة بالعربية</h2>
          <p>إجابات واضحة عن أكثر ما يسأل عنه أصحاب المتاجر في الإمارات عن واتساب للأعمال.</p>
        </div>
        <ul class="link-list link-list--col span-6 start-7">
          <li><a class="link" href="/ar/guides/click-to-whatsapp-ads/">إعلانات النقر إلى واتساب: كيف تجعلها تبيع</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-abandoned-cart-recovery/">استرجاع السلات المتروكة عبر واتساب</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-business-api-pricing-uae/">أسعار WhatsApp Business API في الإمارات</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-green-tick-uae/">كيف توثّق حساب واتساب للأعمال</a></li>
          <li><a class="link" href="/ar/guides/bulk-whatsapp-messages-uae/">كيف ترسل رسائل واتساب جماعية بطريقة نظامية</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-business-app-vs-api/">الفرق بين تطبيق واتساب للأعمال وواتساب API</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-marketing-rules-uae/">قواعد التسويق عبر واتساب في الإمارات</a></li>
          <li><a class="link" href="/ar/guides/whatsapp-payment-links-uae/">كيف تستلم المدفوعات عبر واتساب</a></li>
          <li><a class="link" href="/ar/guides/sell-supplements-online-uae/">كيف تبيع المكملات الغذائية أونلاين في الإمارات</a></li>
          <li><a class="link" href="/ar/whatsapp-automation-uae/">أتمتة واتساب للأعمال على رقمك الخاص</a></li>
          <li><a class="link" href="/ar/guides/">كل الأدلة بالعربية</a></li>
        </ul>
      </div>
    </section>

{faq_block(HOME_FAQ, 'أسئلة قبل الحجز')}"""

# ------------------------------------------------------------------ /ar/whatsapp-automation-uae/
WA_FAQ = [
    ("ما الفرق بين تطبيق واتساب للأعمال وWhatsApp Business API؟", "التطبيق مجاني ويعمل على هاتف واحد مع حتى أربعة أجهزة مرتبطة، وقوائم البث فيه محدودة بـ256 جهة اتصال حفظت رقمك. أما الـAPI فيتيح عدداً غير محدود من الموظفين ومساعداً بالذكاء الاصطناعي ورسائل قوالب معتمدة لكل من وافق على استلامها، وتحاسب Meta عليه لكل رسالة."),
    ("هل أحتفظ برقمي الحالي؟", "نعم. يمكن ربط رقمك الحالي بالـAPI، ومع ميزة التعايش من Meta يستمر فريقك في استخدام تطبيق واتساب للأعمال على الرقم نفسه."),
    ("كم تكلفة رسائل واتساب في الإمارات؟", "تحاسب Meta لكل رسالة مُسلَّمة حسب الفئة (تسويق، خدمات، مصادقة، خدمة عملاء) وحسب دولة العميل، وللإمارات سعر خاص يمكن دفعه بالدرهم منذ أبريل 2026. لكل رقم 1,000 رسالة خدمة مجانية شهرياً، والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب مجانية لمدة تصل إلى 7 أيام إذا رددت خلال 24 ساعة."),
    ("هل يجب أن يوافق العميل قبل أن أراسله؟", "نعم. تشترط Meta موافقة واضحة تذكر اسم نشاطك، ويجب احترام أي طلب لإيقاف الرسائل. والقانون الإماراتي لحماية البيانات الشخصية يشترط الموافقة لمعالجة البيانات مع استثناءات محددة."),
    ("هل يفهم المساعد اللهجة الخليجية؟", "يرد M2S بالعربية والإنجليزية حسب لغة العميل، ونختبره قبل الإطلاق برسائل حقيقية من عملائك، بما فيها اللهجة الخليجية والرسائل المختلطة بالعربية والإنجليزية."),
]
WA_TITLE = "أتمتة واتساب للأعمال في الإمارات ودبي | WhatsApp API | Nuevo"
WA_DESC = "أتمتة مبيعات واتساب في الإمارات على رقمك الخاص: WhatsApp Business API، نافذة الـ24 ساعة، القوالب المعتمدة، الموافقة وإيقاف الرسائل، ومساعد ذكاء اصطناعي بالعربية."
wa_main = f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <p class="crumb"><a href="/ar/">الرئيسية</a> / أتمتة واتساب</p>
        <h1 id="page-h">أتمتة واتساب للأعمال في الإمارات، على رقمك الخاص</h1>
        <p class="t-lead">ردود خلال ثوانٍ، ومتابعة تلقائية، وبيع داخل المحادثة، على واجهة WhatsApp Business API الرسمية. نُعدّها ونديرها لعلامات في دبي وأبوظبي والشارقة وباقي الإمارات.</p>
{cta('ar-wa-hero')}
        </div>
      </div>
    </section>

    <section class="band" aria-label="الإجابة المختصرة">
      <div class="wrap">
        <div class="answer"><p>أتمتة واتساب تعني الرد على العملاء وتأهيلهم ومتابعتهم عبر برنامج بدل العمل اليدوي. للأعمال، تعمل على WhatsApp Business API الرسمية، التي تتيح مساعداً بالذكاء الاصطناعي وصندوق وارد للفريق وقوالب رسائل تعتمدها Meta. الرسائل خارج نافذة خدمة العملاء (24 ساعة) يجب أن تستخدم تلك القوالب، ويجب أن يتمكن العميل دائماً من إيقاف الرسائل.</p></div>
      </div>
    </section>

    <section class="band" aria-labelledby="api-h">
      <div class="wrap">
        <article class="prose">
<h2 id="api-h">تطبيق واتساب للأعمال وواجهة API أداتان مختلفتان</h2>
<div class="prose-table"><table>
<thead><tr><th></th><th>تطبيق واتساب للأعمال</th><th>WhatsApp Business API</th></tr></thead>
<tbody>
<tr><td>التكلفة</td><td>مجاني</td><td>تحاسب Meta لكل رسالة، إضافة إلى رسوم المنصة</td></tr>
<tr><td>الموظفون</td><td>هاتف واحد وحتى 4 أجهزة مرتبطة (10 مع ميزة تعدد الموظفين)</td><td>حسب المنصة، دون حد من واتساب</td></tr>
<tr><td>الوصول إلى العملاء</td><td>قوائم بث حتى 256 شخصاً حفظوا رقمك</td><td>قوالب معتمدة لكل من وافق، ضمن حد الرسائل اليومي</td></tr>
<tr><td>الأتمتة</td><td>رسائل ترحيب وغياب وردود سريعة</td><td>مساعد ذكاء اصطناعي، متابعات، ربط بالمتجر وأنظمة CRM</td></tr>
</tbody></table></div>
<p>للتفاصيل الكاملة: <a href="/ar/guides/whatsapp-business-app-vs-api/">الفرق بين تطبيق واتساب للأعمال وWhatsApp Business API</a>.</p>

<h2>نافذة الـ24 ساعة والقوالب المعتمدة</h2>
<p>عندما يراسلك العميل تُفتح نافذة خدمة مدتها 24 ساعة، وتستطيع الرد بحرية داخلها. خارجها لا يمكنك إرسال إلا قوالب معتمدة من Meta في ثلاث فئات: التسويق (العروض وتذكير السلة المتروكة)، والخدمات (تأكيد الطلب والشحن دون أي ترويج)، والمصادقة (رموز التحقق فقط).</p>

<h2>الموافقة وإيقاف الرسائل والساعات الهادئة</h2>
<ul>
<li>تشترط Meta أن تذكر الموافقة اسم نشاطك وأن يكون واضحاً أن العميل يوافق على استلام رسائلك.</li>
<li>يجب احترام أي طلب لإيقاف الرسائل، داخل واتساب أو خارجه.</li>
<li>قرار مجلس الوزراء رقم 56 لسنة 2024 بشأن التسويق عبر الهاتف يشمل في تعريفه رسائل التسويق عبر تطبيقات التواصل الاجتماعي، ويحصر مكالمات التسويق بين 9 صباحاً و6 مساءً. نلتزم بهذه الساعات في رسائل التسويق.</li>
</ul>
<p>التفاصيل في <a href="/ar/guides/whatsapp-marketing-rules-uae/">دليل قواعد التسويق عبر واتساب في الإمارات</a>.</p>
<p>وبالعربية: <a href="/ar/guides/bulk-whatsapp-messages-uae/">كيف ترسل رسائل واتساب جماعية بطريقة نظامية</a> و<a href="/ar/guides/whatsapp-green-tick-uae/">كيف توثّق حساب واتساب للأعمال</a>.</p>

<h2>كم تكلفة رسائل واتساب في الإمارات؟</h2>
<p>منذ 1 يوليو 2025 تحاسب Meta لكل رسالة مُسلَّمة حسب فئتها ودولة العميل، وللإمارات تسعيرة مستقلة بالدرهم منذ 1 أبريل 2026. لكل رقم 1,000 رسالة خدمة مجانية شهرياً منذ 1 أكتوبر 2026، والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب تفتح نافذة مجانية لمدة تصل إلى 7 أيام. التفاصيل: <a href="/ar/guides/whatsapp-business-api-pricing-uae/">أسعار WhatsApp Business API في الإمارات</a>.</p>

<h2>ما الذي يقدمه M2S فوق الأتمتة</h2>
<p>المنصة وحدها لا تبيع. M2S يشمل إعداد رقمك على الـAPI، وتدريب المساعد على منتجاتك وأسعارك وسياساتك، وكتابة القوالب واعتمادها، والمتابعات، وإعلانات Meta التي تفتح المحادثات، وتقريراً شهرياً بالمبيعات حسب الإعلان. <a href="/ar/">اعرف كيف يعمل M2S</a>.</p>
        </article>
      </div>
    </section>

{faq_block(WA_FAQ, 'أسئلة عن أتمتة واتساب')}"""

# ------------------------------------------------------------------ Arabic guides
def guide_main(crumb, h1, lead, answer, body, faqs, faq_h, lead_key):
    return f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <p class="crumb"><a href="/ar/">الرئيسية</a> / {crumb}</p>
        <h1 id="page-h">{e(h1)}</h1>
        <p class="t-lead">{e(lead)}</p>
        <p class="byline">بقلم <a href="/about/" hreflang="en">نواف اللحام</a>، مؤسس Nuevo Automations · آخر تحديث <time datetime="{DATE}">28 نوفمبر 2026</time></p>
        </div>
      </div>
    </section>

    <section class="band" aria-label="الإجابة المختصرة">
      <div class="wrap">
        <div class="answer"><p>{e(answer)}</p></div>
      </div>
    </section>

    <section class="band" aria-label="الدليل">
      <div class="wrap">
        <article class="prose">
{body.strip()}
        </article>
      </div>
    </section>

{faq_block(faqs, faq_h)}

    <section class="band" aria-labelledby="cta-h">
      <div class="wrap">
        <div class="stack-4">
        <h2 id="cta-h">تريد أن نتولى ذلك لعلامتك؟</h2>
        <p>ندير إعلانات Meta وGoogle إلى واتساب لعلامات العافية والمكملات في الإمارات، ويُتمّ M2S البيع داخل المحادثة. الخطوة الأولى تدقيق مجاني لمدة 30 دقيقة.</p>
{cta(lead_key)}
        </div>
      </div>
    </section>"""


def article(path, en_path, h1, desc):
    return {"@context": "https://schema.org", "@type": "Article", "@id": SITE + path + "#article", "headline": h1,
            "description": desc, "url": SITE + path, "mainEntityOfPage": SITE + path, "inLanguage": "ar",
            "datePublished": DATE, "dateModified": DATE, "image": SITE + "/assets/og-card.jpg",
            "author": {"@type": "Person", "@id": SITE + "/about/#nawaf", "name": "Nawaf Allahham"},
            "publisher": {"@id": SITE + "/#org"}, "translationOfWork": {"@id": SITE + en_path + "#article"}}


TICK_H1 = "كيف تحصل على علامة التوثيق في واتساب للأعمال في الإمارات"
TICK_DESC = "طريقتان لتوثيق حساب واتساب للأعمال في الإمارات عام 2026: حساب الأعمال الرسمي المجاني على الـAPI، واشتراك Meta One المدفوع لتطبيق واتساب للأعمال."
TICK_ANSWER = "في عام 2026 يمكن لنشاط تجاري في الإمارات الحصول على علامة توثيق في واتساب بطريقتين. على WhatsApp Business API، حالة حساب الأعمال الرسمي (Official Business Account) مجانية بشروط: توثيق حسابك التجاري في Meta، ومرور 30 يوماً على الأقل على تسجيل الرقم في المنصة، وتفعيل التحقق بخطوتين، واعتماد اسم العرض، والالتزام بسياسات واتساب. وعلى تطبيق واتساب للأعمال المجاني، تأتي علامة التوثيق مع Meta One، اشتراك Meta المدفوع الذي أُطلق في 15 سبتمبر 2026، وذكرت الصحافة الإماراتية أن سعره يبدأ من 46.99 درهماً شهرياً."
TICK_BODY = """
<h2>العلامة الخضراء أصبحت زرقاء</h2>
<p>كان واتساب يعرض علامة خضراء بجانب الحسابات التجارية الموثقة، ثم انتقلت Meta إلى علامة توثيق زرقاء في تطبيقاتها. ما زال كثيرون يبحثون عن "العلامة الخضراء"، لكن ما يمكنك التقديم عليه اليوم هو أحد الخيارين أدناه.</p>

<h2>الخيار الأول: حساب الأعمال الرسمي (مجاني، على الـAPI فقط)</h2>
<p>إذا كان رقمك يعمل على منصة واتساب للأعمال (الـAPI)، يمكنك طلب حالة الحساب الرسمي دون تكلفة. شروط Meta:</p>
<ul>
<li>أن يلتزم الرقم بسياسة رسائل واتساب للأعمال.</li>
<li>أن يكون مسجلاً على المنصة منذ 30 يوماً على الأقل.</li>
<li>أن يكون حسابك التجاري في Meta موثقاً.</li>
<li>أن يكون التحقق بخطوتين مفعّلاً على الرقم.</li>
<li>أن يكون اسم العرض معتمداً.</li>
</ul>
<p>تقدّم بالطلب من WhatsApp Manager، من ملف رقم الهاتف. لا تُمنح هذه الحالة لحسابات الموظفين الشخصية أو حسابات الاختبار أو أرقام تطبيق واتساب للأعمال. وإذا رُفض طلبك يمكنك إعادة التقديم بعد 30 يوماً.</p>
<p>تذكر وثائق أحد المزودين أن هذه العلامة غير متاحة للأرقام التي تستخدم ميزة التعايش (تشغيل التطبيق والـAPI على الرقم نفسه)، فاسأل مزودك قبل الربط إن كانت العلامة مهمة لك.</p>

<h2>الخيار الثاني: Meta One (مدفوع، يعمل على تطبيق واتساب للأعمال)</h2>
<p>أطلقت Meta في 15 سبتمبر 2026 اشتراك Meta One الذي يحلّ تدريجياً محل Meta Verified. تشمل باقاته للأعمال علامة توثيق على تطبيق واتساب للأعمال وحماية من انتحال الهوية بعد توثيق نشاطك، إضافة إلى مساعد Meta بالذكاء الاصطناعي. وذكرت خليج تايمز وغلف نيوز أسعار الباقات في الإمارات: Essential من 46.99 درهماً شهرياً، وAdvanced من 119 درهماً، وExpert من 359 درهماً، وMax من 1,199 درهماً.</p>

<h2>أيهما تختار؟</h2>
<ul>
<li><strong>تستخدم تطبيق واتساب للأعمال المجاني فقط:</strong> Meta One هو الطريق الوحيد للعلامة.</li>
<li><strong>تعمل على الـAPI أو تنتقل إليها للأتمتة:</strong> قدّم على حساب الأعمال الرسمي المجاني بعد استيفاء الشروط.</li>
<li><strong>في الحالتين:</strong> وثّق نشاطك في مدير أعمال Meta أولاً، فهو أيضاً ما يرفع حد الرسائل اليومي على الـAPI من 250 إلى 2,000 شخص.</li>
</ul>
<p>العلامة تزيد ثقة العميل بأنه يتحدث مع العلامة الحقيقية، لكنها لا تغيّر أسعار الرسائل ولا حدودها. ما يبيع فعلاً هو الرد السريع والصحيح، وهذا ما بُني له <a href="/ar/">M2S</a>.</p>
<p class="note">المصادر: وثائق Meta للمطورين عن حسابات الأعمال الرسمية؛ إعلان Meta عن Meta One (15 سبتمبر 2026)؛ خليج تايمز (17 سبتمبر 2026) وغلف نيوز (16 سبتمبر 2026). اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/whatsapp-green-tick-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
TICK_FAQ = [
    ("كيف أوثّق حساب واتساب للأعمال في الإمارات؟", "على WhatsApp Business API قدّم طلب حساب الأعمال الرسمي المجاني من WhatsApp Manager بعد توثيق نشاطك ومرور 30 يوماً وتفعيل التحقق بخطوتين. وعلى تطبيق واتساب للأعمال اشترك في Meta One."),
    ("هل توثيق واتساب مجاني؟", "على الـAPI نعم، إذا استوفيت شروط Meta. أما على تطبيق واتساب للأعمال فالعلامة تأتي مع باقة Meta One المدفوعة، وتبدأ في الإمارات من 46.99 درهماً شهرياً بحسب الصحافة المحلية."),
    ("ماذا أفعل إذا رُفض طلب التوثيق؟", "يمكنك إعادة التقديم بعد 30 يوماً. استغل المدة لإكمال توثيق نشاطك والتأكد من أن اسم العرض يطابق اسم نشاطك."),
    ("هل تزيد علامة التوثيق حد الرسائل اليومي؟", "لا. حد الرسائل يعتمد على توثيق النشاط وجودة الرسائل. توثيق النشاط، المطلوب للعلامة أصلاً، هو ما يرفع الحد من 250 إلى 2,000."),
]

BULK_H1 = "كيف ترسل رسائل واتساب جماعية في الإمارات بالطريقة النظامية"
BULK_DESC = "إرسال رسائل واتساب جماعية في الإمارات عام 2026: قوائم البث، البث المدفوع للأعمال، قوالب الـAPI، الحدود اليومية، التكلفة وقواعد الموافقة."
BULK_ANSWER = "هناك ثلاث طرق نظامية لإرسال رسائل واتساب جماعية في الإمارات. تطبيق واتساب للأعمال المجاني يتيح قوائم بث حتى 256 جهة اتصال، ولا تصل إلا لمن حفظ رقمك. ويتيح التطبيق أيضاً البث المدفوع للأعمال الذي يصل لمن لم يحفظ رقمك، في الدول التي توفره فيها Meta. وللأعداد الكبيرة، ترسل WhatsApp Business API قوالب تسويقية معتمدة من Meta لكل من وافق على استلام رسائلك، بحد يبدأ من 250 شخصاً يومياً للحساب الجديد ويرتفع إلى 2,000 بعد توثيق النشاط، وتحاسب Meta على كل رسالة مُسلَّمة. كل الطرق تتطلب موافقة العميل، ويجب التوقف عن مراسلة كل من يطلب ذلك."
BULK_BODY = """
<h2>الطريقة الأولى: قوائم البث في التطبيق (مجانية)</h2>
<ul>
<li>حتى 256 جهة اتصال في كل قائمة.</li>
<li>لا يستلمها إلا من حفظ رقمك في هاتفه.</li>
<li>تصل لكل شخص كرسالة خاصة، والردود تعود إليك فردياً.</li>
<li>لا يمكن إنشاء قوائم البث من الأجهزة المرتبطة، بل من الهاتف الرئيسي.</li>
</ul>

<h2>الطريقة الثانية: البث المدفوع للأعمال في التطبيق</h2>
<p>منذ أبريل 2025 تقدم Meta بثاً مدفوعاً في تطبيق واتساب للأعمال يصل حتى لمن لم يحفظ رقمك، وتدفع لكل رسالة مُسلَّمة بسعر يحدده بلد العميل. تقول Meta إن الميزة متاحة في دول محدودة، ولم نتمكن من تأكيد توفرها في الإمارات في نوفمبر 2026، فتحقق من أدوات البث في تطبيقك.</p>

<h2>الطريقة الثالثة: قوالب التسويق على WhatsApp Business API</h2>
<div class="prose-table"><table>
<thead><tr><th>البند</th><th>القاعدة في 2026</th></tr></thead>
<tbody>
<tr><td>الوصول اليومي</td><td>250 شخصاً خلال 24 ساعة للحساب الجديد، و2,000 بعد توثيق النشاط، ثم 10,000 و100,000 وبلا حد مع ارتفاع جودة رسائلك</td></tr>
<tr><td>السرعة</td><td>80 رسالة في الثانية لكل رقم افتراضياً</td></tr>
<tr><td>التكلفة</td><td>تحاسب Meta لكل رسالة تسويقية مُسلَّمة بسعر الإمارات، إضافة إلى رسوم المنصة</td></tr>
<tr><td>من يمكنك مراسلته</td><td>فقط من وافق على استلام رسائل نشاطك</td></tr>
</tbody></table></div>

<h2>تجنب برامج الإرسال الجماعي غير الرسمية</h2>
<p>البرامج التي تتحكم بتطبيق واتساب العادي أو واتساب ويب لإرسال الرسائل بالجملة تخالف شروط واتساب، وكثيراً ما تُقيَّد الأرقام التي تستخدمها أو تُحظر، فتخسر الرقم وسجل المحادثات.</p>

<h2>قواعد الموافقة</h2>
<ul>
<li><strong>Meta:</strong> يجب أن يوافق العميل على استلام رسائل من نشاطك مع ذكر اسمه، وأن تحترم طلبات الإيقاف داخل واتساب وخارجه.</li>
<li><strong>قواعد التسويق عبر الهاتف:</strong> قرار مجلس الوزراء رقم 56 لسنة 2024 يشمل في تعريفه رسائل التسويق عبر تطبيقات التواصل الاجتماعي، ويمنع الاتصال بالأرقام المسجلة في سجل عدم الإزعاج، ويحصر مكالمات التسويق بين 9 صباحاً و6 مساءً.</li>
<li><strong>قانون حماية البيانات الشخصية:</strong> معالجة البيانات تتطلب الموافقة، مع استثناءات محددة.</li>
</ul>
<p class="note">المصادر: مركز مساعدة واتساب (قوائم البث والبث للأعمال)؛ وثائق Meta للمطورين (حدود الرسائل وCloud API)؛ سياسة رسائل واتساب للأعمال؛ النص الإنجليزي لقرار مجلس الوزراء رقم 56 لسنة 2024. اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/bulk-whatsapp-messages-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
BULK_FAQ = [
    ("كم شخصاً يمكنني مراسلته في بث واتساب واحد؟", "في تطبيق واتساب للأعمال حتى 256 جهة اتصال في القائمة، ولا يستلمها إلا من حفظ رقمك. وعلى الـAPI يبدأ الحساب الجديد بـ250 شخصاً يومياً، ويرتفع إلى 2,000 بعد توثيق النشاط."),
    ("هل الإرسال الجماعي على واتساب قانوني في الإمارات؟", "نعم لمن وافق على استلام رسائلك، وعبر أدوات واتساب الرسمية أو الـAPI. لا تراسل قوائم مشتراة أو منسوخة أبداً."),
    ("لماذا لم تصل رسالتي لبعض الأشخاص؟", "في التطبيق لا يصل البث إلا لمن حفظ رقمك. وعلى الـAPI قد تحجب Meta الرسائل التسويقية عن الأشخاص الأقل تفاعلاً، ويظهر ذلك بالخطأ 131049."),
    ("هل سيُحظر رقمي إذا أرسلت رسائل جماعية؟", "ليس إذا استخدمت الأدوات الرسمية وراسلت من وافق فقط. تُقيَّد الأرقام عندما يحظرها أو يبلغ عنها كثيرون، أو عند استخدام برامج غير رسمية."),
]

PRICE_H1 = "أسعار WhatsApp Business API في الإمارات لعام 2026"
PRICE_DESC = "كيف تحاسب Meta رسائل WhatsApp Business API في الإمارات عام 2026: التسعير لكل رسالة، تغييرات 1 أكتوبر 2026، النافذة المجانية بعد إعلانات واتساب، وتقدير فاتورتك."
PRICE_ANSWER = "منذ 1 يوليو 2025 تحاسب Meta على WhatsApp Business API لكل رسالة مُسلَّمة، لا لكل محادثة. يعتمد السعر على فئة الرسالة (تسويق، خدمات، مصادقة، خدمة عملاء) وعلى رمز دولة العميل الذي يستلمها، وللإمارات تسعيرة مستقلة. منذ 1 أكتوبر 2026 يحصل كل رقم على 1,000 رسالة خدمة مجانية شهرياً ويدفع عما بعدها. والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب تفتح نافذة مجانية لا تحاسب فيها Meta على الرسائل."
PRICE_BODY = """
<h2>كيف تحاسب Meta رسائل واتساب الآن</h2>
<p>تدفع فقط عن الرسائل التي يرسلها نشاطك وتُسلَّم فعلاً. الرسائل التي يرسلها العملاء إليك مجانية دائماً. ولكل فئة سعرها في كل سوق:</p>
<div class="prose-table"><table>
<thead><tr><th>الفئة</th><th>الاستخدام</th><th>مثال</th></tr></thead>
<tbody>
<tr><td>قالب تسويق</td><td>عروض وإطلاقات وتذكيرات هدفها البيع</td><td>تذكير بسلة متروكة، تنبيه بعودة منتج</td></tr>
<tr><td>قالب خدمات</td><td>تحديثات عن شيء فعله العميل</td><td>تأكيد الطلب، الطلب في الطريق</td></tr>
<tr><td>قالب مصادقة</td><td>رموز التحقق لمرة واحدة</td><td>رمز دخول أو دفع</td></tr>
<tr><td>رسالة خدمة عملاء</td><td>ردود حرة خلال نافذة الـ24 ساعة</td><td>الرد على "هل توصلون إلى العين؟"</td></tr>
<tr><td>مساعد Meta للأعمال</td><td>ردود يكتبها مساعد Meta بالذكاء الاصطناعي</td><td>يُحاسَب بالرموز (tokens) بشكل منفصل</td></tr>
</tbody></table></div>
<p>تحدد Meta الفئة عند اعتماد القالب، ويمكنها إعادة تصنيف قالب "خدمات" إذا كان تسويقياً في الحقيقة.</p>

<h2>السعر يعتمد على دولة العميل لا دولتك</h2>
<p>نشاط إماراتي يراسل رقماً يبدأ بـ+971 يدفع سعر الإمارات، لكن إذا راسل عميلاً في السعودية أو الهند يدفع سعر تلك الدولة. وتدرج وثائق Meta الدرهم الإماراتي عملةً للفوترة منذ أبريل 2026. الأسعار تتغير عدة مرات في السنة، لذلك لا ننشرها هنا: راجع صفحة أسعار واتساب لدى Meta واختر "الإمارات العربية المتحدة".</p>

<h2>ما الذي تغيّر في 1 أكتوبر 2026</h2>
<ul>
<li><strong>رسائل خدمة العملاء لم تعد مجانية بلا حد.</strong> لكل رقم 1,000 رسالة خدمة مجانية شهرياً لا تُرحَّل، وما بعدها مدفوع.</li>
<li><strong>قوالب الخدمات داخل نافذة الـ24 ساعة أصبحت مدفوعة مجدداً</strong> بعد أن كانت مجانية منذ يوليو 2025.</li>
<li><strong>دون وسيلة دفع لا رسائل بعد الحد المجاني.</strong> تتوقف Meta عن تسليم رسائل الخدمة بعد الألف الأولى.</li>
</ul>
<p>محادثة بيع من خمس عشرة رداً تستهلك الآن خمس عشرة رسالة خدمة. معظم العلامات الصغيرة تبقى قرب الحد المجاني، أما العلامات التي تعلن بكثافة فتتجاوزه.</p>

<h2>النافذة المجانية بعد إعلان بنقرة إلى واتساب</h2>
<p>عندما ينقر العميل على إعلان ينقل إلى واتساب من هاتفه وترد خلال 24 ساعة، تفتح Meta نافذة دخول مجانية لا تحاسب فيها على رسائل التسويق والخدمات والمصادقة وخدمة العملاء لذلك العميل، بينما تبقى ردود مساعد Meta مدفوعة. تقول وثائق Meta للمطورين إن النافذة قد تبقى مفتوحة حتى 7 أيام، وتذكر صفحاتها التسويقية 72 ساعة، فخطط على الرقم الأقصر. ولا تُفتح إلا للمحادثات التي بدأت من أندرويد أو iOS.</p>

<h2>تكاليف أخرى غير رسوم Meta</h2>
<ul>
<li><strong>المنصة أو المزود:</strong> الـAPI بلا صندوق وارد، ومعظم المنصات تأخذ رسوماً شهرية وأحياناً هامشاً على كل رسالة.</li>
<li><strong>ردود الذكاء الاصطناعي:</strong> ضمن رسوم المنصة أو كرموز لمساعد Meta.</li>
<li><strong>الإعداد:</strong> ربط الرقم، اعتماد القوالب، ربط المتجر وتدريب المساعد.</li>
<li><strong>ميزانية الإعلانات</strong> إن كانت المحادثات تأتي من الإعلانات، وتُدفع لـMeta منفصلة.</li>
</ul>

<h2>كيف تقلل الفاتورة دون أن تخسر مبيعات</h2>
<ol>
<li>رد بسرعة لتبقى المحادثة داخل نافذة الـ24 ساعة.</li>
<li>وجّه إعلاناتك إلى واتساب على الهاتف حيث تنطبق النافذة المجانية.</li>
<li>أرسل متابعة واحدة واضحة بدل ثلاث.</li>
<li>أوقف التسلسل فور رد العميل أو شرائه، ولا تراسل من طلب التوقف.</li>
<li>اجعل تحديثات الطلب قوالب خدمات حقيقية، ورسائل البيع قوالب تسويق.</li>
</ol>
<p class="note">المصدر: وثائق تسعير منصة واتساب للأعمال لدى Meta وتحديثاتها، اطّلعنا عليها في نوفمبر 2026. تتغير الأسعار كثيراً، فراجع المصدر قبل وضع الميزانية. <a href="/guides/whatsapp-business-api-pricing-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
PRICE_FAQ = [
    ("هل تطبيق واتساب للأعمال مجاني؟", "نعم. تطبيق واتساب للأعمال على هاتفك بلا رسوم على الرسائل. التسعير لكل رسالة يخص WhatsApp Business API، التي تحتاجها للمساعد الذكي وصندوق الفريق وتتبع الإعلانات والمتابعات المجدولة."),
    ("هل أدفع عندما يراسلني العميل؟", "لا. تحاسب Meta فقط على الرسائل التي يرسلها نشاطك وتُسلَّم. رسائل العملاء إليك مجانية."),
    ("أي سعر ينطبق على نشاط في الإمارات؟", "سعر دولة رقم العميل المستلم. الرسائل إلى أرقام +971 بسعر الإمارات، وإلى عملاء في دول أخرى بسعر تلك الدول."),
    ("كم رسالة مجانية أحصل عليها؟", "منذ 1 أكتوبر 2026 يحصل كل رقم على 1,000 رسالة خدمة مجانية شهرياً. والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب على الهاتف تفتح نافذة مجانية إذا رددت خلال 24 ساعة."),
]

APPAPI_H1 = "الفرق بين تطبيق واتساب للأعمال وWhatsApp Business API في 2026"
APPAPI_DESC = "تطبيق واتساب للأعمال أم WhatsApp Business API؟ الأجهزة، البث، الأتمتة، التكلفة، التعايش على رقم واحد، علامة التوثيق وMeta One، بحسب Meta في 2026."
APPAPI_ANSWER = "تطبيق واتساب للأعمال مجاني، ويعمل على هاتف واحد مع حتى أربعة أجهزة مرتبطة (عشرة مع ميزة تعدد الموظفين)، وفيه ردود سريعة ورسائل ترحيب وقوائم بث حتى 256 شخصاً يجب أن يكونوا قد حفظوا رقمك. أما WhatsApp Business API فليس لها صندوق وارد خاص، لذلك تُستخدم عبر منصة، لكنها تتيح عدداً غير محدود من الموظفين ومساعدات ذكاء اصطناعي وقوالب معتمدة لكل من وافق على استلام رسائلك وربطاً بالمتجر، وتحاسب Meta لكل رسالة. وميزة التعايش تتيح استخدام الاثنين على الرقم نفسه."
APPAPI_BODY = """
<h2>مقارنة سريعة</h2>
<div class="prose-table"><table>
<thead><tr><th></th><th>تطبيق واتساب للأعمال</th><th>WhatsApp Business API</th></tr></thead>
<tbody>
<tr><td>التكلفة</td><td>مجاني، والرسائل منه مجانية</td><td>تحاسب Meta لكل رسالة مُسلَّمة حسب الفئة والدولة، إضافة إلى رسوم المنصة</td></tr>
<tr><td>الموظفون والأجهزة</td><td>هاتف واحد وحتى 4 أجهزة مرتبطة، و10 مع تعدد الموظفين</td><td>حسب ما تسمح به المنصة</td></tr>
<tr><td>الوصول إلى العملاء</td><td>قوائم بث حتى 256 شخصاً حفظوا رقمك، وبث مدفوع في بعض الدول</td><td>قوالب معتمدة لكل من وافق، ضمن حد الرسائل اليومي</td></tr>
<tr><td>الأتمتة</td><td>رسائل ترحيب وغياب وردود سريعة ومساعد Meta</td><td>مساعدات ذكاء اصطناعي، متابعات، ربط بالمتجر وأنظمة CRM</td></tr>
<tr><td>التوثيق</td><td>علامة توثيق مدفوعة عبر Meta One</td><td>حساب أعمال رسمي مجاني إذا استوفيت الشروط</td></tr>
</tbody></table></div>

<h2>متى يكفي التطبيق المجاني</h2>
<ul>
<li>شخص أو اثنان يردان على كل المحادثات.</li>
<li>عدد محادثات قليل يومياً.</li>
<li>لا تعلن بكثافة لإرسال الناس إلى واتساب.</li>
<li>لا تحتاج رسائل تلقائية عند ترك السلة أو عدم الدفع.</li>
</ul>

<h2>متى تحتاج الـAPI</h2>
<ul>
<li>تعلن بإعلانات تنقل إلى واتساب والمحادثات أسرع من قدرة فريقك على الرد.</li>
<li>تريد مساعداً بالذكاء الاصطناعي يرد خلال ثوانٍ ليلاً ونهاراً بالعربية والإنجليزية.</li>
<li>تريد متابعات تلقائية للسلال المتروكة وروابط الدفع غير المدفوعة.</li>
<li>تريد إرسال المبيعات من المحادثات إلى Meta لقياس العائد الحقيقي للإعلانات.</li>
</ul>

<h2>التعايش: التطبيق والـAPI على رقم واحد</h2>
<p>تسمح Meta الآن بربط رقم تطبيق واتساب للأعمال الحالي بالـCloud API عبر شريك، مع الاستمرار في استخدام التطبيق. بحسب وثائق Meta:</p>
<ul>
<li>تحتاج إصدار التطبيق 2.24.17 أو أحدث، والربط يتم عبر شريك معتمد من Meta.</li>
<li>يُستورد حتى 180 يوماً من سجل المحادثات الفردية، وتبقى المحادثات متزامنة.</li>
<li>الرسائل من التطبيق تبقى مجانية، ورسائل الـAPI بالسعر المعتاد.</li>
<li>القيود: سرعة ثابتة 20 رسالة في الثانية، قوائم البث للقراءة فقط، المجموعات لا تتزامن، وحتى 4 أجهزة مرافقة.</li>
<li>إذا توقف الهاتف الرئيسي عن العمل نحو 14 يوماً ينقطع الربط.</li>
</ul>

<h2>كم تكلفة الـAPI؟</h2>
<p>منذ 1 يوليو 2025 تحاسب Meta لكل رسالة مُسلَّمة حسب الفئة ودولة العميل، ولكل رقم 1,000 رسالة خدمة مجانية شهرياً، والمحادثات من إعلانات واتساب مجانية حتى 7 أيام إذا رددت خلال 24 ساعة. التفاصيل في <a href="/ar/guides/whatsapp-business-api-pricing-uae/">دليل أسعار واتساب API</a>، وعن التوثيق في <a href="/ar/guides/whatsapp-green-tick-uae/">دليل توثيق واتساب للأعمال</a>.</p>
<p class="note">المصادر: مركز مساعدة واتساب (الأجهزة المرتبطة، تعدد الموظفين، قوائم البث)؛ وثائق Meta للمطورين (Cloud API، الأسعار، التعايش، حسابات الأعمال الرسمية)؛ إعلانات Meta (أبريل 2025 وسبتمبر 2026). اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/whatsapp-business-app-vs-api/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
APPAPI_FAQ = [
    ("هل WhatsApp Business API مجانية؟", "لا. تحاسب Meta لكل رسالة مُسلَّمة حسب الفئة والدولة، ومعظم الأنشطة تدفع أيضاً لمنصة. لكل رقم 1,000 رسالة خدمة مجانية شهرياً، والمحادثات من إعلانات واتساب تفتح نافذة مجانية حتى 7 أيام."),
    ("هل يمكنني استخدام التطبيق والـAPI على الرقم نفسه؟", "نعم، عبر ميزة التعايش من Meta بواسطة شريك معتمد. تستمر في المحادثة من التطبيق بينما تتولى الـAPI الأتمتة، مع قيود مثل قوائم بث للقراءة فقط و20 رسالة في الثانية."),
    ("كم شخصاً يمكنه استخدام حساب واتساب للأعمال؟", "في التطبيق هاتف واحد وحتى 4 أجهزة مرتبطة، أو 10 أجهزة مع ميزة تعدد الموظفين. في الـAPI لا يوجد هذا الحد، والأمر يعتمد على المنصة."),
    ("لماذا لا يصل البث لبعض العملاء؟", "في تطبيق واتساب للأعمال لا يصل البث إلا لمن حفظ رقمك، وبحد 256 شخصاً للقائمة. للوصول لكل من وافق تحتاج قوالب الـAPI أو البث المدفوع حيث يتوفر."),
]

RULES_H1 = "قواعد التسويق عبر واتساب في الإمارات: ما يجب الالتزام به في 2026"
RULES_DESC = "قواعد التسويق عبر واتساب في الإمارات 2026: سياسة Meta للموافقة وإيقاف الرسائل، حدود الرسائل اليومية، قرار التسويق عبر الهاتف رقم 56 لسنة 2024، وقانون حماية البيانات."
RULES_ANSWER = "لإرسال رسائل تسويقية على واتساب في الإمارات تحتاج رقم العميل وموافقته، ويجب أن تذكر الموافقة اسم نشاطك وأن يكون واضحاً أنه يوافق على استلام رسائلك. يجب احترام طلبات الإيقاف داخل واتساب وخارجه. الرسائل خارج نافذة الـ24 ساعة يجب أن تكون قوالب معتمدة من Meta، والحساب الجديد يراسل 250 شخصاً يومياً حتى ترفع Meta الحد. وفي القانون الإماراتي، يشمل تعريف التسويق عبر الهاتف في قرار مجلس الوزراء رقم 56 لسنة 2024 رسائل التسويق عبر تطبيقات التواصل الاجتماعي، ويشترط المرسوم بقانون اتحادي رقم 45 لسنة 2021 الموافقة لمعالجة البيانات الشخصية، مع استثناءات."
RULES_BODY = """
<p class="note">هذا الدليل معلومات عامة وليس استشارة قانونية. حيث لا يذكر القانون واتساب صراحةً، نقول ذلك.</p>

<h2>قواعد Meta: الموافقة وإيقاف الرسائل</h2>
<p>تسمح سياسة رسائل واتساب للأعمال (آخر تحديث 23 سبتمبر 2026) بمراسلة الأشخاص فقط إذا أعطوك رقمهم ووافقوا على تلقي رسائلك. وتضيف وثائق Meta أن الموافقة يجب أن:</p>
<ul>
<li>توضح أن الشخص يوافق على استلام رسائل من النشاط؛</li>
<li>تذكر اسم النشاط بوضوح؛</li>
<li>تلتزم بالقانون المحلي، ويمكن أن تكون عامة لا تخص واتساب وحده.</li>
</ul>
<p>يجب احترام كل طلب إيقاف "داخل واتساب أو خارجه" وحذف الشخص من قائمتك. لا تشترط Meta كلمة STOP، لكن القوالب يمكن أن تحمل زر إيقاف اختيارياً، ويستطيع العميل إيقاف "العروض والإعلانات" من نشاطك داخل واتساب.</p>

<h2>القوالب ونافذة الـ24 ساعة</h2>
<p>عندما يراسلك العميل تُفتح نافذة خدمة مدتها 24 ساعة ترد فيها بحرية. خارجها لا يمكنك إرسال إلا قوالب معتمدة في ثلاث فئات: التسويق (العروض والتذكيرات وكل ما هو ترويجي)، والخدمات (رسائل غير ترويجية عن شيء فعله العميل مثل تأكيد الطلب)، والمصادقة (رموز التحقق فقط). إذا قدّمت رسالة تسويقية على أنها خدمات تعيد Meta تصنيفها، وتكرار ذلك يؤدي إلى قيود.</p>

<h2>حدود الرسائل في 2026</h2>
<div class="prose-table"><table>
<thead><tr><th>المستوى</th><th>كيف تصل إليه</th></tr></thead>
<tbody>
<tr><td>250</td><td>الحد الافتراضي لحساب أعمال جديد</td></tr>
<tr><td>2,000</td><td>توثيق نشاطك، أو توثيقك من شريكك، أو إرسال 2,000 رسالة قوالب عالية الجودة لأشخاص مختلفين خلال 30 يوماً</td></tr>
<tr><td>10,000 ثم 100,000 ثم بلا حد</td><td>تلقائياً عندما تكون رسائلك عالية الجودة واستخدمت نصف حدك على الأقل خلال 7 أيام</td></tr>
</tbody></table></div>
<p>منذ 7 أكتوبر 2025 يُطبَّق الحد على كل الأرقام في حسابك التجاري معاً. ولم يعد مستوى 1,000 ولا حالة "Flagged" موجودين.</p>

<h2>عندما يحظرك العملاء أو يبلّغون عنك</h2>
<p>تحصل القوالب على تقييم جودة من الحظر والبلاغات ونسب القراءة، وقد تُوقَف القوالب منخفضة الجودة. ومخالفة السياسات تمر بتدرج: تحذير، ثم منع القوالب من يوم إلى ثلاثة أيام، ثم منع الإرسال كلياً من 5 إلى 30 يوماً، ثم قفل الحساب، ثم الحظر الدائم.</p>

<h2>القانون الإماراتي: قواعد التسويق عبر الهاتف</h2>
<p>يسري قرار مجلس الوزراء رقم 56 لسنة 2024 بشأن التسويق عبر الهاتف منذ أغسطس 2024، ويشمل تعريفه "رسائل التسويق النصية ورسائل التسويق عبر تطبيقات التواصل الاجتماعي". لا يذكر واتساب بالاسم، وملخص وزارة الاقتصاد يتحدث عن المكالمات فقط، لذا فانطباقه على واتساب مسألة تفسير. أهم قواعده، وهي مكتوبة أساساً للمكالمات:</p>
<ul>
<li>موافقة مسبقة من الجهة المختصة، واستخدام أرقام محلية مسجلة باسم الشركة؛</li>
<li>التسويق فقط لمن طلب ذلك، وعدم الاتصال بالأرقام المسجلة في سجل عدم الإزعاج؛</li>
<li>مكالمات التسويق فقط بين 9 صباحاً و6 مساءً؛</li>
<li>التعريف بالشركة والغرض في بداية التواصل.</li>
</ul>
<p>وبحسب وزارة الاقتصاد تتراوح غرامات الشركات بين 10,000 و150,000 درهم. القراءة الآمنة: راسل من وافق فقط، وعرّف بنفسك، والتزم بساعات معقولة، وتوقف فوراً عند الطلب.</p>

<h2>القانون الإماراتي: البيانات الشخصية</h2>
<p>المرسوم بقانون اتحادي رقم 45 لسنة 2021 بشأن حماية البيانات الشخصية ساري منذ 2 يناير 2022، ويمنع معالجة البيانات دون موافقة صاحبها مع استثناءات محددة. وتذكر مصادر ثانوية أن لائحته التنفيذية لم تصدر حتى أغسطس 2026. عملياً: سجّل متى وكيف وافق كل عميل، واحذف من يطلب ذلك.</p>
<p class="note">المصادر: سياسة رسائل واتساب للأعمال؛ وثائق Meta للمطورين (الموافقة، تصنيف القوالب، حدود الرسائل، جودة القوالب، تطبيق السياسات)؛ النص الإنجليزي لقرار مجلس الوزراء رقم 56 لسنة 2024؛ ملخص وزارة الاقتصاد (29 أغسطس 2024)؛ بوابة u.ae عن حماية البيانات. اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/whatsapp-marketing-rules-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
RULES_FAQ = [
    ("هل التسويق عبر واتساب قانوني في الإمارات؟", "نعم، بموافقة العميل. تشترط Meta موافقة تذكر اسم نشاطك، ويشترط القانون الإماراتي الموافقة لمعالجة البيانات الشخصية. ويشمل تعريف قرار التسويق عبر الهاتف لعام 2024 رسائل التسويق عبر تطبيقات التواصل، فتعامل مع قواعده على أنها تنطبق."),
    ("ما الموافقة الصحيحة على رسائل واتساب؟", "بحسب Meta يجب أن توضح أن الشخص يوافق على استلام رسائل نشاطك وأن تذكر اسم النشاط. يمكن جمعها عند الدفع أو في نموذج أو في المحادثة."),
    ("كم رسالة يمكنني إرسالها يومياً على واتساب؟", "الحساب الجديد يبدأ محادثات مع 250 شخصاً خلال 24 ساعة، ويرتفع إلى 2,000 بعد توثيق النشاط، ثم إلى 10,000 و100,000 وبلا حد مع الاستخدام والجودة العالية."),
    ("في أي وقت يمكنني إرسال رسائل تسويقية في الإمارات؟", "يحصر قرار مجلس الوزراء رقم 56 لسنة 2024 مكالمات التسويق بين 9 صباحاً و6 مساءً. لا يحدد ساعات للرسائل صراحةً، لكن الالتزام بهذه الساعات هو الخيار الآمن."),
]

PAY_H1 = "كيف تستلم المدفوعات عبر واتساب في الإمارات"
PAY_DESC = "الدفع داخل واتساب غير متاح للأعمال في الإمارات، لذلك تبيع العلامات بروابط الدفع. رسوم Stripe وZiina وTelr وغيرها، إضافة إلى تابي وتمارا، في 2026."
PAY_ANSWER = "مدفوعات واتساب المدمجة، ومنها رسالة الطلب بزر Review and Pay، لا توثقها Meta إلا للهند والبرازيل وسنغافورة، وليس للإمارات. لذلك تستلم الأنشطة في الإمارات المدفوعات داخل واتساب بإرسال رابط دفع من مزودها: Stripe تتقاضى 2.9% زائد درهم واحد للبطاقات المحلية، وZiina تذكر 2.6% زائد درهم واحد في صفحة الأعمال، وTelr لديها باقات شهرية بروابط دفع غير محدودة. ويمكن لتابي وتمارا إنشاء روابط دفع أيضاً، لكن وثائقهما تذكر إرسالها برسالة نصية أو بريد إلكتروني. يضغط العميل الرابط ويدفع في صفحة المزود، ثم يؤكد فريقك أو المساعد الذكي الطلب في المحادثة."
PAY_BODY = """
<h2>الدفع داخل واتساب غير متاح للأعمال في الإمارات</h2>
<p>لدى Meta مدفوعات مدمجة في منصة واتساب للأعمال، لكن وثائقها تغطي ثلاث أسواق فقط: الهند (بالروبية فقط)، والبرازيل، وسنغافورة. ولم نجد نسخة للإمارات حتى نوفمبر 2026. البديل العملي رابط عادي، أو قالب بزر رابط، يفتح صفحة دفع آمنة من مزود مرخّص.</p>

<h2>مزودو روابط الدفع للأنشطة في الإمارات</h2>
<p>الرسوم كما ينشرها كل مزود في صفحته للإمارات، اطّلعنا عليها في 28 نوفمبر 2026. تأكد منها قبل التعاقد.</p>
<div class="prose-table"><table>
<thead><tr><th>المزود</th><th>الرسوم المنشورة</th><th>روابط الدفع</th></tr></thead>
<tbody>
<tr><td>Stripe</td><td>2.9% + درهم واحد للبطاقات المحلية، و+1% للبطاقات الدولية، و+1% عند تحويل العملة</td><td>دون تكلفة إضافية</td></tr>
<tr><td>Ziina</td><td>2.6% + درهم واحد في صفحة الأعمال (وصفحة الرسوم تذكر 2.9% + درهم، فتأكد)</td><td>تقول إن الروابط تُشارك "على أي منصة، بما فيها واتساب"</td></tr>
<tr><td>Telr</td><td>باقات من 0 إلى 249 درهماً شهرياً، ورسوم من 0% إلى 2.45% + درهم حسب الحجم، مع ضريبة 5%</td><td>روابط دفع غير محدودة في كل الباقات</td></tr>
<tr><td>Network International</td><td>غير منشورة</td><td>Pay By Link مع خيار المشاركة عبر تطبيقات المراسلة</td></tr>
<tr><td>Checkout.com</td><td>غير منشورة</td><td>روابط لمرة واحدة تنتهي بعد 24 ساعة افتراضياً</td></tr>
</tbody></table></div>

<h2>الشراء الآن والدفع لاحقاً: تابي وتمارا</h2>
<ul>
<li><strong>تابي</strong> تتيح للتجار إنشاء روابط دفع من لوحة التاجر وتطبيق الأعمال، وتذكر إرسالها برسالة نصية أو بريد إلكتروني.</li>
<li><strong>تمارا</strong> توثّق رابط دفع يُرسل للعميل برسالة نصية وينتهي بعد 15 دقيقة افتراضياً.</li>
</ul>
<p>لا تذكر أي منهما واتساب قناةً للإرسال، فاسأل مزودك قبل بناء خطوات البيع عليها.</p>

<h2>كيف يجب أن تسير عملية البيع في واتساب</h2>
<ol>
<li>أجب عن الأسئلة أولاً: السعر والمكونات ومدة التوصيل.</li>
<li>أكّد الطلب كتابياً: المنتج والكمية والسعر شاملاً الضريبة والعنوان.</li>
<li>أرسل الرابط مع المبلغ في الرسالة.</li>
<li>تابع حالة الدفع آلياً عبر إشعارات المزود.</li>
<li>ذكّر بلطف من لم يدفع بعد بضع ساعات، داخل نافذة الـ24 ساعة أو بقالب معتمد خارجها.</li>
<li>أبقِ الدفع عند الاستلام خياراً احتياطياً إن كانت خدمة التوصيل تدعمه.</li>
</ol>
<p class="note">المصادر: وثائق Meta لمدفوعات واتساب في الهند والبرازيل؛ صفحات أسعار Stripe الإمارات وZiina وTelr؛ وثائق تابي وتمارا للتجار. اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/whatsapp-payment-links-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
PAY_FAQ = [
    ("هل الدفع عبر واتساب متاح في الإمارات؟", "ليس للأنشطة التجارية حتى نوفمبر 2026. توثّق Meta مدفوعات واتساب للأعمال في الهند والبرازيل وسنغافورة فقط، لذلك ترسل الأنشطة في الإمارات رابط دفع من مزودها."),
    ("ما أرخص طريقة لاستلام الدفع في واتساب؟", "يعتمد على حجم مبيعاتك. Stripe بلا رسوم شهرية وتتقاضى 2.9% + درهم للبطاقات المحلية، وباقات Telr الأعلى حجماً تصل إلى 2.25% + نصف درهم دون رسوم شهرية. قارن المجموع على مبيعاتك الفعلية."),
    ("هل يمكنني إرسال رابط تابي أو تمارا على واتساب؟", "كلاهما ينشئ روابط دفع، لكن وثائقهما تذكر الرسائل النصية أو البريد الإلكتروني لا واتساب. بعض بوابات الدفع توفر الشراء الآن والدفع لاحقاً داخل روابط يمكن مشاركتها في واتساب، فاسأل مزودك."),
    ("هل الدفع عبر رابط في واتساب آمن للعميل؟", "نعم عندما يفتح الرابط صفحة مزود دفع مرخّص على نطاقه الخاص. أخبر عملاءك باسم المزود، ولا تطلب بيانات البطاقة داخل المحادثة أبداً."),
]

SUPP_H1 = "كيف تبيع المكملات الغذائية أونلاين في الإمارات"
SUPP_DESC = "بيع المكملات الغذائية أونلاين في الإمارات: من يسجّل المنتجات (مؤسسة الإمارات للدواء وبلدية دبي)، رخص التجارة الإلكترونية، اشتراطات العربية، الإعلانات والدفع."
SUPP_ANSWER = "لبيع المكملات الغذائية أونلاين في الإمارات تحتاج رخصة تجارية تتيح نشاط التجارة الإلكترونية (مثل رخصة تاجر إلكتروني في دبي أو رخصة تاجر أبوظبي، أو رخصة تجارة إلكترونية من منطقة حرة)، ويجب تسجيل منتجاتك. على المستوى الاتحادي، تسلّمت مؤسسة الإمارات للدواء خدمات المنتجات الطبية من وزارة الصحة اعتباراً من 29 ديسمبر 2025، وتدرج المكملات الغذائية ضمن إذن تسويق منتجات الرعاية الصحية الذي لا يتقدم به إلا مستودع طبي مرخّص. وفي دبي تشترط بلدية دبي تسجيل المكملات الصحية في نظام منتجي قبل استيرادها أو الإعلان عنها أو بيعها. ويجب توفير تفاصيل المنتج والفواتير بالعربية، وضريبة القيمة المضافة 5%."
SUPP_BODY = """
<p class="note">هذا الدليل معلومات عامة وليس استشارة قانونية. تغيّرت قواعد المكملات مرات عدة في 2025 و2026، فتأكد من مسارك مع مؤسسة الإمارات للدواء (800 33784)، ومع بلدية دبي (800900) إن كنت في دبي، قبل الاستيراد أو الإعلان.</p>

<h2>1. حدّد التصنيف القانوني لمنتجك</h2>
<p>الكبسولة نفسها قد تكون مكملاً غذائياً أو دواءً حسب مكوناتها وادعاءاتك. مسار منتجات الرعاية الصحية لدى مؤسسة الإمارات للدواء يغطي المستحضرات للصحة العامة <strong>غير المخصصة لتشخيص مرض أو علاجه أو الوقاية منه</strong>، ويذكر المكملات الغذائية والمنتجات العشبية بينها. أما المنتج الذي يدّعي علاج مرض أو يحتوي مكونات مقيدة فيدخل مسار الأدوية الأشد.</p>
<p>وتحذير خاص بالببتيدات: في يوليو 2026 اتخذت مؤسسة الإمارات للدواء إجراءات ضد 71 جهة تبيع منتجات ببتيدات غير معتمدة لإنقاص الوزن، وأحالت 14 مؤثراً إلى الجهة المنظمة للإعلام، بحسب غلف نيوز. وموقف المؤسسة أن تسمية المنتج "ببتيد" لا تجعله معتمداً.</p>

<h2>2. سجّل المنتجات</h2>
<ul>
<li><strong>مؤسسة الإمارات للدواء (اتحادياً):</strong> خدمة "إذن تسويق منتج رعاية صحية" تشمل المكملات الغذائية. يتقدم بها مستودع طبي مرخّص من المؤسسة، وتستغرق 45 يوم عمل، والشهادة صالحة 5 سنوات، ورسم الطلب 100 درهم.</li>
<li><strong>بلدية دبي:</strong> إرشاداتها الفنية للمكملات الصحية تمنع تصنيعها أو استيرادها أو الإعلان عنها أو بيعها في دبي ما لم تُسجَّل في نظام منتجي.</li>
<li><strong>أبوظبي والإمارات الأخرى:</strong> لجهات الغذاء والصحة المحلية متطلباتها، فراجعها.</li>
</ul>
<p>الصفحات الرسمية متداخلة، ولم نتمكن من تأكيد ما إذا كان الفيتامين البسيط يحتاج تسجيل المؤسسة أو منتجي أو كليهما. عملياً تعمل معظم العلامات مع مستورد أو مستودع مرخّص يتولى التسجيل، فاطلب منه الجواب كتابةً لكل منتج.</p>

<h2>3. الرخصة المناسبة للبيع أونلاين</h2>
<p>بحسب البوابة الرسمية u.ae يحتاج البائع في البر الرئيسي رخصة بنشاط تجارة إلكترونية من الدائرة الاقتصادية في إمارته، مثل رخصة تاجر إلكتروني في دبي أو رخصة تاجر أبوظبي، كما تحتاج رخص التجارة الإلكترونية موافقة هيئة تنظيم الاتصالات والحكومة الرقمية. وتصدر المناطق الحرة رخص تجارة إلكترونية أيضاً، لكن البيع المباشر لعملاء البر الرئيسي قد يتطلب موزعاً محلياً.</p>

<h2>4. العربية والملصقات والادعاءات</h2>
<ul>
<li>بموجب قانون حماية المستهلك يجب على البائع أونلاين تقديم تفاصيل المنتج والشروط والدفع والضمان <strong>بالعربية</strong>، وإصدار الفواتير بالعربية، وذكر الجهة المرخِّصة.</li>
<li>اجعل الادعاءات في حدود الصحة العامة؛ ادعاء علاج حالة قد ينقل المنتج إلى مسار الأدوية.</li>
</ul>

<h2>5. الإعلانات: ما تغيّر في 2026</h2>
<ul>
<li>في 19 نوفمبر 2026 أعلنت مؤسسة الإمارات للدواء أن إعلانات المنتجات الطبية تحتاج موافقتها قبل النشر، وأن المؤثرين ممنوعون من الترويج لها، بحسب ذا ناشيونال. لم يوضح التقرير إن كانت المكملات المسجلة منتجات رعاية صحية مشمولة، فاسأل المؤسسة قبل التعاقد مع صناع المحتوى.</li>
<li>كل من يروّج لمنتجات على وسائل التواصل في الإمارات يحتاج تصريح معلن من الهيئة الوطنية للإعلام.</li>
<li>على Meta يجب استهداف إعلانات الصحة والعافية لمن هم 18 عاماً فأكثر وتجنب ادعاءات "قبل وبعد" والنتائج الخارقة.</li>
</ul>

<h2>6. الدفع والضريبة</h2>
<ul>
<li><strong>ضريبة القيمة المضافة</strong> 5%، والتسجيل إلزامي فوق 375,000 درهم من المبيعات الخاضعة سنوياً واختياري من 187,500 درهم.</li>
<li><strong>الدفع بالبطاقات:</strong> Shopify Payments تدرج الإمارات بين الدول المدعومة، وتخدم Stripe وNetwork International وTelr وتابي وتمارا المتاجر الإماراتية. راجع قائمة الأنشطة المقيدة لدى مزودك؛ فـStripe مثلاً تمنع المكملات غير الآمنة أو ذات الادعاءات الضارة.</li>
<li><strong>البيع في واتساب:</strong> كثير من مشتري المكملات يسألون قبل الدفع. راجع <a href="/ar/guides/whatsapp-payment-links-uae/">دليل استلام المدفوعات عبر واتساب</a>.</li>
</ul>
<p class="note">المصادر: خدمة إذن تسويق منتج رعاية صحية لدى مؤسسة الإمارات للدواء؛ إشعار نقل خدمات وزارة الصحة؛ إرشادات بلدية دبي الفنية للمكملات الصحية (الإصدار الثاني 2024)؛ صفحات u.ae عن التجارة الإلكترونية وحماية المستهلك؛ تقارير ذا ناشيونال (19 نوفمبر 2026) وغلف نيوز (25 يوليو 2026). اطّلعنا عليها في 28 نوفمبر 2026. <a href="/guides/sell-supplements-online-uae/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
SUPP_FAQ = [
    ("هل يجب تسجيل المكملات قبل بيعها أونلاين في الإمارات؟", "نعم. في دبي تشترط بلدية دبي تسجيل المكملات الصحية في نظام منتجي قبل بيعها أو الإعلان عنها. واتحادياً تدرج مؤسسة الإمارات للدواء المكملات الغذائية ضمن إذن تسويق منتجات الرعاية الصحية. تأكد من الجهتين أيهما ينطبق على منتجك."),
    ("من ينظّم المكملات في الإمارات الآن؟", "انتقلت خدمات المنتجات الطبية، ومنها أذونات التسويق وموافقات الإعلان، من وزارة الصحة ووقاية المجتمع إلى مؤسسة الإمارات للدواء اعتباراً من 29 ديسمبر 2025. وتسجّل بلدية دبي والجهات المحلية الأخرى المكملات الصحية في إماراتها."),
    ("هل يمكن للمؤثرين الترويج لمكملاتي؟", "كل صانع محتوى يروّج لمنتجات في الإمارات يحتاج تصريح معلن. ومنذ نوفمبر 2026 يُمنع المؤثرون من الترويج للمنتجات الطبية وتحتاج إعلاناتها موافقة المؤسسة. اسأل المؤسسة إن كان مكملك المسجل مشمولاً."),
    ("هل تُعامل الببتيدات كمكملات في الإمارات؟", "لا. في يوليو 2026 اتخذت مؤسسة الإمارات للدواء إجراءات ضد بائعي منتجات ببتيدات غير معتمدة، وقالت إن تسمية «ببتيد» لا تجعل المنتج معتمداً. تعامل مع الببتيدات العلاجية كمنتجات طبية."),
]

CTWA_H1 = "إعلانات النقر إلى واتساب: كيف تعمل وكيف تجعلها تبيع"
CTWA_DESC = "إعلانات النقر إلى واتساب على إنستغرام وفيسبوك: متى تتفوق المحادثة على صفحة الهبوط، الإعداد في مدير الإعلانات، الدقيقة الأولى، وقياس المبيعات الحقيقية."
CTWA_ANSWER = "إعلان النقر إلى واتساب هو إعلان على إنستغرام أو فيسبوك يفتح زرّه محادثة واتساب مع نشاطك، غالباً برسالة أولى جاهزة. ينجح أكثر عندما يسأل المشتري قبل أن يدفع، عن الجرعة أو التوصيل أو أصالة المنتج، وهذا شائع في منتجات العافية الفاخرة في الإمارات. الإعلان يبدأ المحادثة فقط: البيع يعتمد على الرد خلال ثوانٍ، وعلى إرسال مبيعات المحادثات إلى Meta لتجد مشترين أكثر."
CTWA_BODY = """
<h2>ما هو إعلان النقر إلى واتساب</h2>
<p>إعلان عادي من Meta على إنستغرام أو فيسبوك أو ماسنجر، زر الدعوة فيه "إرسال رسالة" أو "واتساب". عند الضغط يفتح واتساب على هاتف المشتري برقم نشاطك ورسالة أولى كتبتها أنت، مثل "مرحباً، أريد سعر عبوة 60 كبسولة". يضغط المشتري إرسال فتبدأ المحادثة. وداخل واتساب تحمل المحادثة بطاقة صغيرة تُظهر الإعلان الذي جاءت منه، وتمرّر الـAPI لنظامك معرّف النقرة الذي يتيح لك لاحقاً إبلاغ Meta بالبيع.</p>

<h2>متى تتفوق المحادثة على صفحة الهبوط</h2>
<div class="prose-table"><table>
<thead><tr><th>أرسل إلى واتساب عندما…</th><th>أرسل إلى موقعك عندما…</th></tr></thead>
<tbody>
<tr><td>يسأل المشترون قبل الدفع (المكونات، الجرعة، الأصالة)</td><td>المنتج رخيص وواضح بذاته</td></tr>
<tr><td>كثير من الطلبات دفع عند الاستلام أو تحتاج موعد توصيل</td><td>صفحة الدفع سريعة ونادراً ما يحتاج المشتري مساعدة</td></tr>
<tr><td>كثير من المشترين يفضلون الحديث بالعربية</td><td>لا تستطيع الرد خلال دقائق ليلاً ونهاراً</td></tr>
<tr><td>الباقات والاشتراكات تحتاج توصية</td><td>معظم مشتريك على الكمبيوتر</td></tr>
</tbody></table></div>
<p>العمود الثاني مهم: إعلان واتساب يحصل على رد بعد ثلاث ساعات يؤدي غالباً أسوأ من صفحة منتج عادية.</p>

<h2>كيف تُعدّه في مدير إعلانات Meta</h2>
<ol>
<li>اربط رقم واتساب بصفحة فيسبوك أو حساب إنستغرام عبر مركز الحسابات، واستخدم الرقم الذي يعرفه عملاؤك.</li>
<li>اختر الهدف: التفاعل أو العملاء المحتملون أو المبيعات، ثم "تطبيقات المراسلة" وواتساب كوجهة.</li>
<li>اكتب الرسالة الجاهزة بحيث تخبرك بما يريد العميل: "سعر عبوة 60 كبسولة من فضلك" أفضل من "مرحباً".</li>
<li>ابنِ الإعلان حول منتج واحد وسؤال واحد.</li>
<li>استهدف البالغين: تشترط Meta أن تستهدف إعلانات المكملات الغذائية والصحية والعشبية من هم 18 عاماً فأكثر.</li>
</ol>

<h2>الدقيقة الأولى تحسم البيع</h2>
<p>من يضغط إعلانك مهتم الآن وواتساب مفتوح أمامه. الرد الأول الجيد:</p>
<ul>
<li>يجيب عن السؤال في الرسالة الجاهزة بالضبط، مع السعر، بلغة المشتري.</li>
<li>يسأل سؤالاً واحداً يقرّب الطلب: "هل هو لك أم هدية؟"، "إلى أي إمارة نوصّل؟"</li>
<li>يعرض طريقة الدفع داخل المحادثة، رابط دفع أو عند الاستلام، فور استعداد المشتري.</li>
</ul>
<p>هذا ما يفعله <a href="/ar/">M2S</a>: مساعد ذكاء اصطناعي مدرَّب على منتجاتك وأسعارك يرد خلال ثوانٍ بالعربية أو الإنجليزية، ويحوّل المحادثة لفريقك مع ملخص عند الحاجة.</p>

<h2>لماذا قد تكلّف هذه المحادثات أقل في رسوم الرسائل</h2>
<p>عندما تبدأ المحادثة من هذا الإعلان على الهاتف وترد خلال 24 ساعة، تفتح Meta نافذة دخول مجانية لا تحاسب فيها على الرسائل لذلك العميل. التفاصيل في <a href="/ar/guides/whatsapp-business-api-pricing-uae/">دليل أسعار واتساب API</a>.</p>

<h2>إبلاغ Meta بالمبيعات</h2>
<p>افتراضياً يعرض مدير الإعلانات "المحادثات التي بدأت" وتكلفة كل محادثة، ولا يعرف أي محادثة اشترت. إذا حسّنت على المحادثات تتعلم Meta إيجاد من يحب الدردشة لا من يدفع. الحل إرسال كل بيع من المحادثة إلى Meta عبر Conversions API مع معرّف النقرة وقيمة الطلب، فترى العائد الحقيقي لكل إعلان.</p>

<h2>أخطاء شائعة</h2>
<ul>
<li>توجيه الإعلانات إلى هاتف شخصي يتفقده شخص واحد حين يتسنى له.</li>
<li>رسالة جاهزة غامضة تجعل الرد الأول "كيف أساعدك؟".</li>
<li>الحكم على الحملة بتكلفة المحادثة بدل تكلفة البيع.</li>
<li>غياب المتابعة: معظم المحادثات الصامتة لا تسمع من النشاط مجدداً.</li>
</ul>
<p class="note">المصادر: وثائق Meta للإعلانات وواتساب للأعمال، اطّلعنا عليها في نوفمبر 2026. <a href="/guides/click-to-whatsapp-ads/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
CTWA_FAQ = [
    ("هل تعمل إعلانات النقر إلى واتساب على إنستغرام؟", "نعم. تعمل على مواضع إنستغرام وفيسبوك وماسنجر، والضغط على الزر يفتح واتساب على هاتف المشتري برقم نشاطك."),
    ("هل أحتاج WhatsApp Business API لهذه الإعلانات؟", "لا، يمكن أن تفتح الإعلانات محادثات على تطبيق واتساب للأعمال. تحتاج الـAPI للرد الآلي وربط كل محادثة بإعلانها والمتابعات وإبلاغ Meta بالمبيعات."),
    ("ما الهدف الذي أختاره للحملة؟", "التفاعل أو العملاء المحتملون أو المبيعات كلها تتيح واتساب وجهةً. وبعد إرسال المبيعات عبر Conversions API يتيح هدف المبيعات لـMeta التحسين على المشترين."),
    ("ما سرعة الرد المطلوبة؟", "أسرع ما يمكن، والأفضل خلال ثوانٍ. المشتري ضغط الإعلان للتو وواتساب مفتوح، والرد بعد ساعات يخسر البيع غالباً."),
]

CART_H1 = "استرجاع السلات المتروكة عبر واتساب خطوة بخطوة"
CART_DESC = "استرجاع السلات المتروكة عبر واتساب: الموافقة، التوقيت، الصياغة بالعربية والإنجليزية، التكلفة، وكيف تقيس ما استرجعته فعلاً، لمتاجر الإمارات في 2026."
CART_ANSWER = "استرجاع السلة المتروكة عبر واتساب يعني إرسال قالب واتساب معتمد لمتسوق ترك منتجات في سلته، مع طريقة لإكمال الطلب. تحتاج WhatsApp Business API، ورقم المتسوق وموافقته عند الدفع، وقالباً تسويقياً معتمداً من Meta، وإشارة من متجرك بأن السلة تُركت. أرسل التذكير الأول خلال ساعة تقريباً، وتذكيراً ثانياً على الأكثر في اليوم التالي، وتوقف فور الرد أو الشراء، ولا ترسل ليلاً أبداً."
CART_BODY = """
<h2>ما تحتاجه قبل التذكير الأول</h2>
<ul>
<li><strong>WhatsApp Business API على رقم علامتك.</strong> التطبيق المجاني لا يرسل رسائل آلية.</li>
<li><strong>رقم المتسوق وموافقته:</strong> اطلب رقم واتساب عند الدفع مع خانة أو سطر واضح بأنك ستراسله بخصوص طلبه.</li>
<li><strong>إشارة السلة من متجرك:</strong> Shopify وWooCommerce ومعظم المنصات ترسل حدث "دفع متروك" لنظامك مباشرة أو عبر n8n أو Make أو Zapier.</li>
<li><strong>قالب معتمد:</strong> تذكيرات السلة تصنَّف تسويقاً لدى Meta، حتى لو طلبها العميل.</li>
</ul>

<h2>متى ترسل</h2>
<div class="prose-table"><table>
<thead><tr><th>الرسالة</th><th>التوقيت</th><th>الهدف</th></tr></thead>
<tbody>
<tr><td>التذكير الأول</td><td>بعد 30 إلى 60 دقيقة من ترك السلة</td><td>إعادته وهو ما زال يتذكر</td></tr>
<tr><td>التذكير الثاني (اختياري)</td><td>في اليوم التالي، نهاراً</td><td>الإجابة عن السؤال الذي أوقفه</td></tr>
<tr><td>التوقف</td><td>فور الرد أو الشراء أو طلب الإيقاف</td><td>الاحترام وضبط التكلفة</td></tr>
</tbody></table></div>

<h2>ماذا تكتب</h2>
<p>اذكر المنتج، وسهّل الإكمال، وادعُ للرد، فالرد يعيد فتح نافذة الـ24 ساعة:</p>
<blockquote><p>مرحباً سارة، تركتِ مغنيسيوم جلايسينات 120 كبسولة في السلة. هل أحجزه لكِ؟ أستطيع إرسال رابط الدفع هنا، أو الدفع عند الاستلام.</p></blockquote>
<p>التذكير الثاني ينجح أكثر عندما يزيل سبباً للتردد: مدة التوصيل إلى إمارته، طريقة الاستخدام، أو حجم أصغر. تجنب الاستعجال المصطنع، فالعملاء يستطيعون الحظر والإبلاغ، وهذا يضر بتقييم رقمك.</p>

<h2>الدفع عند الاستلام وروابط الدفع</h2>
<p>كثير من المتسوقين في الإمارات يتركون السلة عند خطوة البطاقة لا لأنهم غيّروا رأيهم. عرض الدفع عند الاستلام أو رابط دفع داخل المحادثة يسترجع كثيراً من هذه الطلبات. راجع <a href="/ar/guides/whatsapp-payment-links-uae/">دليل الدفع عبر واتساب</a>.</p>

<h2>التكلفة</h2>
<p>كل تذكير قالب تسويقي يُحاسَب لكل رسالة مُسلَّمة بسعر دولة العميل، ورد العميل مجاني. وردودك بعدها رسائل خدمة ضمن 1,000 رسالة مجانية شهرياً لكل رقم منذ أكتوبر 2026.</p>

<h2>كيف تقيس بصدق</h2>
<ul>
<li>احسب فقط طلبات السلات التي وصلها تذكير، بعد التذكير، خلال مدة محددة (نستخدم 72 ساعة).</li>
<li>في الدفع عند الاستلام احسب الطلبات المُسلَّمة لا المُقدَّمة.</li>
<li>قارن بفترة أو بشريحة من السلات لم تصلها تذكيرات، فبعض المتسوقين كانوا سيعودون على أي حال.</li>
</ul>
<p class="note">المصادر: إرشادات Meta لتصنيف قوالب واتساب ووثائق التسعير، اطّلعنا عليها في نوفمبر 2026. <a href="/guides/whatsapp-abandoned-cart-recovery/" hreflang="en">النسخة الإنجليزية</a>.</p>
"""
CART_FAQ = [
    ("هل أستطيع إرسال تذكيرات السلة من تطبيق واتساب للأعمال المجاني؟", "ليس آلياً. التذكيرات الآلية تحتاج WhatsApp Business API وقالباً معتمداً من Meta."),
    ("هل رسالة السلة المتروكة تسويق أم خدمات؟", "تعاملها Meta كرسالة تسويقية، لذلك تحتاج قالباً تسويقياً وتُحاسَب بسعر التسويق."),
    ("كم تذكيراً أرسل؟", "واحد خلال ساعة تقريباً، وواحد آخر على الأكثر في اليوم التالي. توقف فور رد المتسوق أو شرائه أو طلبه الإيقاف."),
    ("هل أحتاج موافقة لمراسلة المتسوقين على واتساب؟", "نعم. يشترط واتساب الموافقة. اطلب الرقم عند الدفع مع توضيح أنك ستراسله بخصوص طلبه، واحترم كل طلب إيقاف."),
]

GUIDE_PAGES = [
    ("/ar/guides/whatsapp-green-tick-uae/", "/guides/whatsapp-green-tick-uae/", "توثيق واتساب للأعمال في الإمارات: العلامة الخضراء | Nuevo", TICK_DESC,
     guide_main("توثيق واتساب", TICK_H1, "العلامة الخضراء أصبحت علامة توثيق زرقاء، وهناك طريقتان للحصول عليها حسب استخدامك لتطبيق واتساب للأعمال أو الـAPI. هذه شروط Meta في نوفمبر 2026.", TICK_ANSWER, TICK_BODY, TICK_FAQ, "أسئلة عن توثيق واتساب", "ar-guide-tick"),
     TICK_FAQ, TICK_H1),
    ("/ar/guides/bulk-whatsapp-messages-uae/", "/guides/bulk-whatsapp-messages-uae/", "إرسال رسائل واتساب جماعية في الإمارات بطريقة نظامية | Nuevo", BULK_DESC,
     guide_main("رسائل واتساب جماعية", BULK_H1, "إرسال رسالة واحدة لمئات العملاء سهل، لكن الخطأ فيه مكلف: برامج الإرسال غير الرسمية تعرّض الرقم للحظر، ومراسلة من لم يوافق تخالف قواعد Meta والقانون الإماراتي. هذه الطرق النظامية الثلاث في 2026.", BULK_ANSWER, BULK_BODY, BULK_FAQ, "أسئلة عن الرسائل الجماعية", "ar-guide-bulk"),
     BULK_FAQ, BULK_H1),
    ("/ar/guides/whatsapp-business-api-pricing-uae/", "/guides/whatsapp-business-api-pricing-uae/", "أسعار واتساب بزنس API في الإمارات 2026 | Nuevo", PRICE_DESC,
     guide_main("أسعار واتساب API", PRICE_H1, "تحاسب Meta لكل رسالة مُسلَّمة حسب نوعها ودولة العميل. هذا ما يعنيه ذلك لنشاط في الإمارات، وما تغيّر في 1 أكتوبر 2026، وكيف تقدّر فاتورتك.", PRICE_ANSWER, PRICE_BODY, PRICE_FAQ, "أسئلة عن أسعار واتساب API", "ar-guide-price"),
     PRICE_FAQ, PRICE_H1),
    ("/ar/guides/whatsapp-business-app-vs-api/", "/guides/whatsapp-business-app-vs-api/", "الفرق بين واتساب للأعمال وواتساب API في 2026 | Nuevo", APPAPI_DESC,
     guide_main("واتساب للأعمال أم API", APPAPI_H1, "معظم الأنشطة في الإمارات تبدأ بتطبيق واتساب للأعمال المجاني، والـAPI هي ما تحتاجه للأتمتة. ومنذ 2025 يمكنك تشغيل الاثنين على الرقم نفسه. هكذا تختار، بحسب حدود Meta في نوفمبر 2026.", APPAPI_ANSWER, APPAPI_BODY, APPAPI_FAQ, "أسئلة عن التطبيق والـAPI", "ar-guide-appapi"),
     APPAPI_FAQ, APPAPI_H1),
    ("/ar/guides/whatsapp-marketing-rules-uae/", "/guides/whatsapp-marketing-rules-uae/", "قواعد التسويق عبر واتساب في الإمارات 2026 | Nuevo", RULES_DESC,
     guide_main("قواعد التسويق عبر واتساب", RULES_H1, "قاعدتان تنطبقان عندما ترسل علامة إماراتية رسائل تسويق على واتساب: قواعد Meta التي تقرر بقاء رقمك يعمل، وقواعد الدولة التي تقرر الغرامات. هذا ما تقوله كل منهما في نوفمبر 2026، وأين يترك القانون مجالاً للتفسير.", RULES_ANSWER, RULES_BODY, RULES_FAQ, "أسئلة عن قواعد التسويق عبر واتساب", "ar-guide-rules"),
     RULES_FAQ, RULES_H1),
    ("/ar/guides/whatsapp-payment-links-uae/", "/guides/whatsapp-payment-links-uae/", "الدفع عبر واتساب في الإمارات: روابط الدفع 2026 | Nuevo", PAY_DESC,
     guide_main("الدفع عبر واتساب", PAY_H1, "العملاء في الإمارات مستعدون للشراء داخل محادثة واتساب، لكن واتساب نفسه لا يستطيع استلام أموالهم هنا. الحل رابط دفع من مزودك. هذا الدليل يشرح ما ينجح وكم يتقاضى كل مزود وكيف تُبقي البيع داخل المحادثة.", PAY_ANSWER, PAY_BODY, PAY_FAQ, "أسئلة عن الدفع عبر واتساب", "ar-guide-pay"),
     PAY_FAQ, PAY_H1),
    ("/ar/guides/sell-supplements-online-uae/", "/guides/sell-supplements-online-uae/", "بيع المكملات الغذائية أونلاين في الإمارات 2026 | Nuevo", SUPP_DESC,
     guide_main("بيع المكملات أونلاين", SUPP_H1, "المكملات من أسرع الفئات نمواً في التجارة الإلكترونية بالإمارات، ومن أكثرها تنظيماً. هذا الدليل يجمع ما تقوله المصادر الرسمية في نوفمبر 2026، ويشير إلى ما لا يجيب عنه إلا المنظّم.", SUPP_ANSWER, SUPP_BODY, SUPP_FAQ, "أسئلة عن بيع المكملات", "ar-guide-supp"),
     SUPP_FAQ, SUPP_H1),
    ("/ar/guides/click-to-whatsapp-ads/", "/guides/click-to-whatsapp-ads/", "إعلانات النقر إلى واتساب: الإعداد والبيع | Nuevo", CTWA_DESC,
     guide_main("إعلانات النقر إلى واتساب", CTWA_H1, "إعلان النقر إلى واتساب يرسل المشتري مباشرة إلى محادثة مع نشاطك بدل صفحة ويب. متى يبيع أكثر، وكيف تُعدّه، والجزء الذي تخطئ فيه معظم العلامات: ما يحدث بعد الضغط.", CTWA_ANSWER, CTWA_BODY, CTWA_FAQ, "أسئلة عن إعلانات واتساب", "ar-guide-ctwa"),
     CTWA_FAQ, CTWA_H1),
    ("/ar/guides/whatsapp-abandoned-cart-recovery/", "/guides/whatsapp-abandoned-cart-recovery/", "استرجاع السلات المتروكة عبر واتساب | Nuevo", CART_DESC,
     guide_main("السلات المتروكة", CART_H1, "تذكير السلة على واتساب يُقرأ بطريقة لا يحظى بها البريد الإلكتروني غالباً. هكذا تُعدّه بشكل صحيح: الموافقة والتوقيت والصياغة والتكلفة وطريقة معرفة إن كان ينجح.", CART_ANSWER, CART_BODY, CART_FAQ, "أسئلة عن استرجاع السلات", "ar-guide-cart"),
     CART_FAQ, CART_H1),
]

PAGES = [
    ("/ar/", "/", HOME_TITLE, HOME_DESC, home_main, HOME_FAQ, [("الرئيسية", "/ar/")]),
    ("/ar/whatsapp-automation-uae/", "/whatsapp-automation-uae/", WA_TITLE, WA_DESC, wa_main, WA_FAQ,
     [("الرئيسية", "/ar/"), ("أتمتة واتساب", "/ar/whatsapp-automation-uae/")]),
]

ARTICLES = {}
for path, en_path, title, desc, main, faqs, h1 in GUIDE_PAGES:
    bc = [("الرئيسية", "/ar/"), (h1, path)]
    PAGES.append((path, en_path, title, desc, main, faqs, bc))
    ARTICLES[path] = article(path, en_path, h1, desc)

# ------------------------------------------------------------------ /ar/guides/ hub
_cards = "\n".join(f"""          <article class="card">
            <h2><a href="{gp}">{e(h1)}</a></h2>
            <p>{e(desc)}</p>
            <a class="link" href="{gp}" aria-hidden="true" tabindex="-1">اقرأ الدليل</a>
          </article>""" for gp, _en, _ti, desc, _m, _f, h1 in GUIDE_PAGES)
HUB_TITLE = "أدلة واتساب وإعلانات Meta للعلامات في الإمارات | Nuevo"
HUB_DESC = "أدلة بالعربية عن أسعار WhatsApp Business API، التوثيق، الرسائل الجماعية، قواعد التسويق، الدفع عبر واتساب، إعلانات واتساب وبيع المكملات في الإمارات."
hub_main = f"""    <section class="page-head" aria-labelledby="page-h">
      <div class="wrap">
        <div class="hero-text">
        <p class="crumb"><a href="/ar/">الرئيسية</a> / الأدلة</p>
        <h1 id="page-h">أدلة البيع عبر واتساب في الإمارات</h1>
        <p class="t-lead">إجابات واضحة عن تكاليف واتساب للأعمال ومنصاته، وإعلانات النقر إلى واتساب، والدفع واسترجاع السلات، وقواعد المكملات والتسويق، من واقع الحملات التي نديرها لعلامات في الإمارات.</p>
        </div>
      </div>
    </section>

    <section class="band" aria-label="كل الأدلة">
      <div class="wrap">
        <div class="guide-list">
{_cards}
        </div>
        <p><a class="link" href="/guides/" hreflang="en">أدلة أخرى بالإنجليزية</a></p>
      </div>
    </section>"""
_hub_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE + "/ar/guides/#collection", "url": SITE + "/ar/guides/",
           "name": "أدلة البيع عبر واتساب في الإمارات", "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"},
           "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": SITE + gp, "name": h1} for i, (gp, _en, _ti, _d, _m, _f, h1) in enumerate(GUIDE_PAGES)]}}
HUB = ("/ar/guides/", "/guides/", HUB_TITLE, HUB_DESC, hub_main, [("الرئيسية", "/ar/"), ("الأدلة", "/ar/guides/")], _hub_ld)

ALT_RE = re.compile(r'  <link rel="alternate" hreflang="[^"]+" href="[^"]+">\n')

for path, en_path, title, desc, main, faqs, bc in PAGES:
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(path, en_path, title, desc, [ARTICLES.get(path) or webpage(path, title, desc), faq_ld(faqs), crumbs(bc)], main))
    # matching alternates on the English twin, right after its canonical
    en = ROOT / en_path.strip("/") / "index.html" if en_path != "/" else ROOT / "index.html"
    t = ALT_RE.sub("", en.read_text())
    canon = f'  <link rel="canonical" href="{SITE}{en_path}">\n'
    assert canon in t, en
    en.write_text(t.replace(canon, canon + alt_links(en_path, path)))
    print(path)

# the hub (no FAQ)
_p, _en, _ti, _d, _m, _bc, _ld = HUB
_out = ROOT / "ar/guides/index.html"
_out.write_text(page(_p, _en, _ti, _d, [_ld, crumbs(_bc)], _m))
_en_file = ROOT / "guides/index.html"
_tx = ALT_RE.sub("", _en_file.read_text())
_canon = f'  <link rel="canonical" href="{SITE}/guides/">\n'
assert _canon in _tx
_en_file.write_text(_tx.replace(_canon, _canon + alt_links("/guides/", "/ar/guides/")))
print("/ar/guides/")

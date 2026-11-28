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
          <div class="span-2 footer__col"><h3>بالعربية</h3><ul><li><a href="/ar/">الصفحة الرئيسية</a></li><li><a href="/ar/whatsapp-automation-uae/">أتمتة واتساب للأعمال</a></li><li><a href="/ar/guides/whatsapp-green-tick-uae/">توثيق واتساب للأعمال</a></li><li><a href="/ar/guides/bulk-whatsapp-messages-uae/">رسائل واتساب جماعية</a></li></ul></div>
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
<p>للتفاصيل الكاملة بالإنجليزية: <a href="/guides/whatsapp-business-app-vs-api/" hreflang="en">WhatsApp Business app vs API</a>.</p>

<h2>نافذة الـ24 ساعة والقوالب المعتمدة</h2>
<p>عندما يراسلك العميل تُفتح نافذة خدمة مدتها 24 ساعة، وتستطيع الرد بحرية داخلها. خارجها لا يمكنك إرسال إلا قوالب معتمدة من Meta في ثلاث فئات: التسويق (العروض وتذكير السلة المتروكة)، والخدمات (تأكيد الطلب والشحن دون أي ترويج)، والمصادقة (رموز التحقق فقط).</p>

<h2>الموافقة وإيقاف الرسائل والساعات الهادئة</h2>
<ul>
<li>تشترط Meta أن تذكر الموافقة اسم نشاطك وأن يكون واضحاً أن العميل يوافق على استلام رسائلك.</li>
<li>يجب احترام أي طلب لإيقاف الرسائل، داخل واتساب أو خارجه.</li>
<li>قرار مجلس الوزراء رقم 56 لسنة 2024 بشأن التسويق عبر الهاتف يشمل في تعريفه رسائل التسويق عبر تطبيقات التواصل الاجتماعي، ويحصر مكالمات التسويق بين 9 صباحاً و6 مساءً. نلتزم بهذه الساعات في رسائل التسويق.</li>
</ul>
<p>دليلنا بالإنجليزية: <a href="/guides/whatsapp-marketing-rules-uae/" hreflang="en">WhatsApp marketing rules in the UAE</a>.</p>
<p>وبالعربية: <a href="/ar/guides/bulk-whatsapp-messages-uae/">كيف ترسل رسائل واتساب جماعية بطريقة نظامية</a> و<a href="/ar/guides/whatsapp-green-tick-uae/">كيف توثّق حساب واتساب للأعمال</a>.</p>

<h2>كم تكلفة رسائل واتساب في الإمارات؟</h2>
<p>منذ 1 يوليو 2025 تحاسب Meta لكل رسالة مُسلَّمة حسب فئتها ودولة العميل، وللإمارات تسعيرة مستقلة بالدرهم منذ 1 أبريل 2026. لكل رقم 1,000 رسالة خدمة مجانية شهرياً منذ 1 أكتوبر 2026، والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب تفتح نافذة مجانية لمدة تصل إلى 7 أيام. التفاصيل: <a href="/guides/whatsapp-business-api-pricing-uae/" hreflang="en">WhatsApp Business API pricing in the UAE</a>.</p>

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

GUIDE_PAGES = [
    ("/ar/guides/whatsapp-green-tick-uae/", "/guides/whatsapp-green-tick-uae/", "توثيق واتساب للأعمال في الإمارات: العلامة الخضراء | Nuevo", TICK_DESC,
     guide_main("توثيق واتساب", TICK_H1, "العلامة الخضراء أصبحت علامة توثيق زرقاء، وهناك طريقتان للحصول عليها حسب استخدامك لتطبيق واتساب للأعمال أو الـAPI. هذه شروط Meta في نوفمبر 2026.", TICK_ANSWER, TICK_BODY, TICK_FAQ, "أسئلة عن توثيق واتساب", "ar-guide-tick"),
     TICK_FAQ, TICK_H1),
    ("/ar/guides/bulk-whatsapp-messages-uae/", "/guides/bulk-whatsapp-messages-uae/", "إرسال رسائل واتساب جماعية في الإمارات بطريقة نظامية | Nuevo", BULK_DESC,
     guide_main("رسائل واتساب جماعية", BULK_H1, "إرسال رسالة واحدة لمئات العملاء سهل، لكن الخطأ فيه مكلف: برامج الإرسال غير الرسمية تعرّض الرقم للحظر، ومراسلة من لم يوافق تخالف قواعد Meta والقانون الإماراتي. هذه الطرق النظامية الثلاث في 2026.", BULK_ANSWER, BULK_BODY, BULK_FAQ, "أسئلة عن الرسائل الجماعية", "ar-guide-bulk"),
     BULK_FAQ, BULK_H1),
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

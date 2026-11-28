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
          <div class="span-2 footer__col"><h3>بالعربية</h3><ul><li><a href="/ar/">الصفحة الرئيسية</a></li><li><a href="/ar/whatsapp-automation-uae/">أتمتة واتساب للأعمال</a></li></ul></div>
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
HOME_TITLE = "مبيعات واتساب بالذكاء الاصطناعي لعلامات المكملات في الإمارات | Nuevo"
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

<h2>كم تكلفة رسائل واتساب في الإمارات؟</h2>
<p>منذ 1 يوليو 2025 تحاسب Meta لكل رسالة مُسلَّمة حسب فئتها ودولة العميل، وللإمارات تسعيرة مستقلة بالدرهم منذ 1 أبريل 2026. لكل رقم 1,000 رسالة خدمة مجانية شهرياً منذ 1 أكتوبر 2026، والمحادثات التي تبدأ من إعلان بنقرة إلى واتساب تفتح نافذة مجانية لمدة تصل إلى 7 أيام. التفاصيل: <a href="/guides/whatsapp-business-api-pricing-uae/" hreflang="en">WhatsApp Business API pricing in the UAE</a>.</p>

<h2>ما الذي يقدمه M2S فوق الأتمتة</h2>
<p>المنصة وحدها لا تبيع. M2S يشمل إعداد رقمك على الـAPI، وتدريب المساعد على منتجاتك وأسعارك وسياساتك، وكتابة القوالب واعتمادها، والمتابعات، وإعلانات Meta التي تفتح المحادثات، وتقريراً شهرياً بالمبيعات حسب الإعلان. <a href="/ar/">اعرف كيف يعمل M2S</a>.</p>
        </article>
      </div>
    </section>

{faq_block(WA_FAQ, 'أسئلة عن أتمتة واتساب')}"""

PAGES = [
    ("/ar/", "/", HOME_TITLE, HOME_DESC, home_main, HOME_FAQ, [("الرئيسية", "/ar/")]),
    ("/ar/whatsapp-automation-uae/", "/whatsapp-automation-uae/", WA_TITLE, WA_DESC, wa_main, WA_FAQ,
     [("الرئيسية", "/ar/"), ("أتمتة واتساب", "/ar/whatsapp-automation-uae/")]),
]

ALT_RE = re.compile(r'  <link rel="alternate" hreflang="[^"]+" href="[^"]+">\n')

for path, en_path, title, desc, main, faqs, bc in PAGES:
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(path, en_path, title, desc, [webpage(path, title, desc), faq_ld(faqs), crumbs(bc)], main))
    # matching alternates on the English twin, right after its canonical
    en = ROOT / en_path.strip("/") / "index.html" if en_path != "/" else ROOT / "index.html"
    t = ALT_RE.sub("", en.read_text())
    canon = f'  <link rel="canonical" href="{SITE}{en_path}">\n'
    assert canon in t, en
    en.write_text(t.replace(canon, canon + alt_links(en_path, path)))
    print(path)

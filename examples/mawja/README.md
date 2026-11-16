# Worked example: Mawja · مثال تطبيقي: موجة

Mawja is a **fictional** pre-seed startup in Riyadh that tells independent café owners what to reorder each morning. Every name, number and decision here was invented to show what finished artefacts look like. None of it is market data.

«موجة» شركة ناشئة **افتراضية** في الرياض تخبر أصحاب المقاهي المستقلة بما يطلبونه كل صباح. كل الأسماء والأرقام والقرارات هنا مختلقة لعرض شكل المُخرَجات المكتملة، وليست بيانات سوقية.

## Context pack · حزمة السياق

| | |
|---|---|
| English | [context/en/](context/en/) |
| العربية | [context/ar/](context/ar/) |

Both pass the linter with no findings · تجتاز الحزمتان الفاحص دون ملاحظات:

```bash
python shared/scripts/context_lint.py examples/mawja/context/en
python shared/scripts/context_lint.py examples/mawja/context/ar
```

Things to notice · ما يستحق الانتباه:

- Layer 3 records a market fact as "not yet sourced; do not quote a figure" instead of guessing · الطبقة 3 تسجّل معلومة سوقية على أنها «لم توثَّق بعد» بدل التخمين.
- Layer 6 puts the product's core boundary in writing: agents suggest orders and never place them · الطبقة 6 تدوّن الحد الأساسي للمنتج: الوكلاء يقترحون الطلبات ولا يقدّمونها أبدًا.
- Layer 7 keeps the reason for each decision · الطبقة 7 تحفظ سبب كل قرار.

## Financial model · النموذج المالي

Built from [assumptions.json](assumptions.json) · مبني من ملف الافتراضات:

| | Summary · الملخص | Workbook · ملف Excel | Monthly · الشهري |
|---|---|---|---|
| English | [model.en.md](model.en.md) | [model.en.xlsx](model.en.xlsx) | [model.en.csv](model.en.csv) |
| العربية | [model.ar.md](model.ar.md) | [model.ar.xlsx](model.ar.xlsx) | [model.ar.csv](model.ar.csv) |

Rebuild · لإعادة البناء:

```bash
python shared/scripts/build_model.py examples/mawja/assumptions.json --out examples/mawja/model.en --lang en
python shared/scripts/build_model.py examples/mawja/assumptions.json --out examples/mawja/model.ar --lang ar
```

Try removing the funding entry from the assumptions and rebuilding: the script reports that cash runs out and exits with status 1 · جرّب حذف بند التمويل من الافتراضات ثم أعد البناء: سيبلغك البرنامج بنفاد النقد ويعيد رمز الخطأ 1.

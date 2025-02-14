# core/tasks.py
from celery import shared_task
from core.models import NewsArticle
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from django.db.models import Q

@shared_task
def fetch_and_translate_news():
    # まずは RSS 取得（ここでは管理コマンドで取得した記事が既に DB にある前提）
    # 次に、翻訳処理を実行する（既に translate_news コマンドで行っている処理を再利用）
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # 翻訳対象の言語設定：英語→日本語（ここでは NLLB を利用）
    source_lang = "eng_Latn"
    target_lang = "jpn_Hani"
    tokenizer.src_lang = source_lang
    forced_bos_token_id = tokenizer.convert_tokens_to_ids(f"<{target_lang}>")
    if forced_bos_token_id is None:
        raise ValueError(f"Cannot determine forced BOS token for target language {target_lang}")

    articles = NewsArticle.objects.filter(Q(translated_content__exact='') | Q(translated_content__isnull=True))[:10]
    for article in articles:
        if not article.content:
            continue
        inputs = tokenizer(article.content, return_tensors="pt", truncation=True, padding=True)
        translated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        article.translated_content = translated_text
        article.save()

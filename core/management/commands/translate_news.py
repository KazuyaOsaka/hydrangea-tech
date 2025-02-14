from django.core.management.base import BaseCommand
from core.models import NewsArticle
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from django.db.models import Q

class Command(BaseCommand):
    help = 'Translate untranslated news articles from English to Japanese using NLLB model.'

    def handle(self, *args, **options):
        model_name = "facebook/nllb-200-distilled-600M"
        self.stdout.write("Loading translation model...")

        # NLLBモデル用のトークナイザーとモデルをロード
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # 翻訳対象の言語設定：英語入力、出力を日本語（漢字主体）に
        source_lang = "eng_Latn"
        target_lang = "jpn_Hani"
        tokenizer.src_lang = source_lang

        # forced_bos_token_id を取得する
        try:
            forced_bos_token_id = tokenizer.get_lang_id(target_lang)
        except AttributeError:
            # get_lang_id が使えない場合、トークン "<jpn_Hani>" として取得する（必要に応じて調整）
            forced_bos_token_id = tokenizer.convert_tokens_to_ids(f"<{target_lang}>")
            if forced_bos_token_id is None:
                raise ValueError(f"Cannot determine token id for target language {target_lang}")

        # translated_content が空またはNULLの記事を対象にする（初回は10件に制限）
        articles = NewsArticle.objects.filter(
            Q(translated_content__exact='') | Q(translated_content__isnull=True)
        )[:10]

        if not articles:
            self.stdout.write("No untranslated articles found.")
            return

        for article in articles:
            self.stdout.write(f"Translating: {article.title}")
            if not article.content:
                self.stdout.write(f"Article content is empty: {article.title}")
                continue

            # 入力テキストをトークン化
            inputs = tokenizer(article.content, return_tensors="pt", truncation=True, padding=True)
            # 翻訳実行時にターゲット言語を強制する
            translated = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id)
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            article.translated_content = translated_text
            article.save()
            self.stdout.write(self.style.SUCCESS(f"Translated and saved: {article.title}"))

        self.stdout.write(self.style.SUCCESS("Finished translating articles."))

# Erişimle Zenginleştirilmiş Üretim (RAG)

Erişimle Zenginleştirilmiş Üretim, kısaca RAG (Retrieval-Augmented Generation), bir dil modelinin cevaplarını senin kendi verilerine dayandıran bir yapay zeka tasarım desenidir. Model, yalnızca eğitim sırasında ezberlediklerine güvenmek yerine, bir belge koleksiyonundan ilgili bilgiyi getirir ve bu bilgiyi bağlam olarak modele verir.

## Üç adım

RAG, adını veren üç adımdan oluşur. Getir (Retrieve): kullanıcının sorusuyla en alakalı pasajları bilgi tabanından bul. Zenginleştir (Augment): bu pasajları bağlam olarak modelin istemine (prompt) ekle. Üret (Generate): modelin bu bağlamı kullanarak bir cevap yazmasını sağla.

## RAG neden faydalı

Cevap, getirilen pasajlardan oluşturulduğu için RAG halüsinasyonları azaltır — halüsinasyon, modelin yanlış bir bilgiyi kendinden emin şekilde söylemesidir. Ayrıca modelin hiç eğitilmediği özel veya güncel bilgiler hakkında cevap verebilmesini sağlar ve bir bilginin tam olarak hangi kaynaktan geldiğini belirtmeyi (kaynak gösterme) mümkün kılar.

## RAG ile ince ayar (fine-tuning) karşılaştırması

İnce ayar, modeli kendi verinle daha fazla eğiterek ağırlıklarını değiştirir; bu pahalıdır ve veri her değiştiğinde tekrarlanmalıdır. RAG ise modeli olduğu gibi bırakır ve veriyi sorgu anında devreye sokar. Küçük ve sık değişen bir bilgi tabanı için RAG çok daha basittir: belgeler değiştiğinde yalnızca ingestion (veri alma) işlemini yeniden çalıştırırsın.

## Bağlama dayalı sistem promptu

Bir RAG cevabının kalitesi büyük ölçüde sistem promptuna bağlıdır. İyi bir prompt, modele yalnızca verilen bağlamı kullanmasını ve bağlam yetersizse bilmediğini söylemesini emreder. Bu, asistanı dürüst tutar ve cevap uydurmasını engeller.
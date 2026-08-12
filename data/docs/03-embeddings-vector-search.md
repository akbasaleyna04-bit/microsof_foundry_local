# Embedding'ler ve Vektör Arama

Embedding, bir metin parçasının anlamını temsil eden sayısal bir vektördür. Bir embedding modeli, metni; anlamı benzer olan metinlerin birbirine yakın düştüğü çok boyutlu bir uzaya eşler. Bu projede kullanılan `qwen3-embedding-0.6b` modeli, her girdi metni için bir vektör üretir.

## Anlamsal arama

Benzer anlamlar birbirine yakın vektörler ürettiği için, tam kelime eşleşmesi yerine anlama göre arama yapabiliriz. Buna anlamsal arama (semantic search) denir. "SDK hangi dilleri destekliyor?" gibi bir soru, farklı kelimelerle yazılmış olsa bile "SDK Python, C#, JavaScript ve Rust ile çalışır" diyen bir pasajla eşleşebilir.

## Kosinüs benzerliği

İki vektörün ne kadar yakın olduğunu ölçmek için kosinüs benzerliğini (cosine similarity) kullanırız. Bu, vektörler arasındaki açının kosinüsünü hesaplar ve uzunluklarını dikkate almaz. 1.0'a yakın bir skor, iki metnin neredeyse aynı yönü gösterdiğini ve çok benzer olduğunu; 0'a yakın bir skor ise alakasız olduklarını ifade eder. Her belgeyi sorguya olan kosinüs benzerliğine göre sıralamak ve en iyi sonuçları almak, getirmenin (retrieval) çekirdeğidir.

## Küçük veri için kaba kuvvet getirme

Küçük bir bilgi tabanı için, saklanan her embedding'i belleğe alıp sorgu embedding'iyle kosinüs benzerliğini hesaplamak ve en yüksek skorlu ilk k sonucu tutmak yeterlidir. Bu kaba kuvvet (brute-force) tarama, yüzlerce ya da birkaç bin parça için hızlı ve doğrudur. Çok büyük koleksiyonlar için ise özel bir vektör veritabanı veya yaklaşık en yakın komşu (approximate nearest-neighbor) indeksi kullanırsın.

## Parçalama (chunking)

Uzun belgeler, embedding'e çevrilmeden önce daha küçük pasajlara, yani parçalara (chunk) bölünür. Parçalama, getirmeyi daha isabetli yapar çünkü tek bir parça tek bir odaklı fikri kapsar; ayrıca getirilen her pasajı sohbet modelinin bağlam penceresine rahatça sığacak kadar küçük tutar. Yaygın bir strateji, paragraf sınırlarından bölmek ve birkaç paragrafı bir karakter bütçesine kadar birlikte paketlemektir.
# Soru-Cevap için Prompt Mühendisliği

Prompt mühendisliği, bir dil modelini istediğin çıktıya yönlendiren talimatlar yazma pratiğidir. Bir sohbet modelinde konuşma, her biri bir role sahip mesajlardan oluşan bir listedir. Sistem mesajı asistanın davranışını ve kurallarını belirlerken, kullanıcı mesajları asıl soruları taşır.

## Sistem promptu ile kullanıcı promptu

Sistem promptu, asistanın görevini tanımladığın yerdir. Bir RAG asistanı için genellikle şuna benzer: yalnızca verilen bağlamı kullan, kısa ol ve kaynağı belirt. Kullanıcı promptu ise kişinin yazdığı sorudan ibarettir. İkisini ayırmak, sorular değişirken kuralları sabit tutar.

## Modeli bağlama dayandırma

RAG için en önemli talimat, yalnızca verilen bağlamdan cevap vermektir. Bu talimat olmadan model, eğitim verisine geri dönüp makul ama yanlış cevaplar üretebilir. İyi dayandırılmış bir prompt, getirilen parçaları sistem mesajına yerleştirir ve modelin bunların ötesine geçmesini yasaklar.

## Eksik bilgiyi ele alma

Sorumlu bir asistan, cevaplayamadığı durumu kabul eder. Prompt, modele bağlam cevabı içermiyorsa tahmin etmek yerine bunu söylemesi gerektiğini belirtmelidir. Bu projede talimat, getirilen pasajlar yetersiz olduğunda "Bu bilgi belgelerimde bulunmuyor." yanıtını vermektir.

## Kaynak gösterme

Getirilen her parça, geldiği belgenin adını taşıdığı için prompt, modelden cevabında bu kaynağı belirtmesini isteyebilir. Kaynak gösterimi asistanı güvenilir kılar: kullanıcı, atıfta bulunulan belgeyi açarak bir iddiayı doğrulayabilir. Bu, kapalı bir cevabı denetlenebilir bir cevaba dönüştürür.
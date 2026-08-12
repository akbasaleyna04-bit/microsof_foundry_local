# Yerel Depolama için SQLite

SQLite, sunucusuz ve kendi kendine yeten (self-contained) bir SQL veritabanı motorudur. Tüm veritabanı diskte tek bir dosyada yaşar, kurulup çalıştırılacak ayrı bir sunucu süreci yoktur ve destek, `sqlite3` modülü aracılığıyla doğrudan Python'un standart kütüphanesine gömülüdür. Bu özellikler onu yerel ve çevrimdışı bir uygulama için mükemmel bir seçim yapar.

## Bu projede SQLite neden kullanılıyor

Bu RAG asistanında SQLite, her belge parçasını embedding vektörüyle birlikte saklar. İndeksi bir dosyada tutmak, bilgi tabanının çalıştırmalar arasında korunması demektir: indeksi ingestion betiğiyle bir kez oluşturursun ve ardından embedding'leri yeniden hesaplamadan defalarca sorgularsın. Bu önbellekleme önemlidir çünkü embedding üretmek, işlem hattının en yavaş adımıdır.

## Şema

Ana tablonun adı `chunks`'tır. Her satır; otomatik artan bir id, kaynak belgenin dosya adı, parçanın o belge içindeki konumu, parça metni ve JSON metni olarak saklanan embedding'i tutar. Küçük bir `meta` tablosu, indeksi hangi embedding modelinin oluşturduğunu kaydeder; böylece ayarlanan model sonradan değişirse uygulama uyarabilir.

## Vektörleri saklama

Embedding'ler ikili bir blob olarak da, JSON metni olarak da saklanabilir. Bu proje JSON metnini kullanır çünkü basit, taşınabilir ve incelemesi kolaydır. Küçük bir bilgi tabanı için uygulama her vektörü belleğe alır ve Python tarafında karşılaştırır; bu, gayet hızlıdır. Büyük ölçekte ise bir SQLite vektör uzantısı ya da özel bir vektör veritabanı kullanırsın.

## Temel işlemler

SQLite ile çalışmak sıradan SQL kullanır. `CREATE TABLE` şemayı tanımlar, `INSERT` ingestion sırasında parçaları ekler ve `SELECT` sorgu anında onları geri okur. Her şey tek bir dosya olduğu için, bilgi tabanını yedeklemek veya paylaşmak `data/rag.db` dosyasını kopyalamak kadar kolaydır.
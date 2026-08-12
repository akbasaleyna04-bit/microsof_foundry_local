# Microsoft Foundry Local

Foundry Local, büyük dil modellerini tamamen kullanıcının cihazında çalıştırmak için hafif bir çalışma zamanı (runtime) ve SDK sağlayan uçtan uca bir yerel yapay zeka çözümüdür. İnternet, Azure aboneliği ya da özel bir GPU gerektirmeden indirip çalıştırabileceğin, önceden optimize edilmiş modellerden oluşan bir katalogla birlikte gelir.

## Modelleri neden yerelde çalıştırmalı

Çıkarımı (inference) cihaz üzerinde yapmanın üç temel faydası vardır. Birincisi gizlilik: verilerin makineden hiç çıkmaz, bu da hassas belgeler için önemlidir. İkincisi maliyet: model bir kez indirildikten sonra istek başına API ücreti yoktur. Üçüncüsü erişilebilirlik: asistan sıfır ağ çağrısıyla çalışmaya devam eder, yani ilk kurulumdan sonra tamamen çevrimdışı çalışır.

## Donanım hızlandırma

Foundry Local, mevcut en iyi donanımı otomatik olarak kullanır. Varsayılan olarak CPU üzerinde çalışır; ONNX Runtime ve çalıştırma sağlayıcıları (execution providers) sayesinde bir GPU veya NPU mevcutsa ondan da yararlanabilir. Bu, aynı kodun çok çeşitli dizüstü bilgisayarlarda değişiklik gerektirmeden çalışması anlamına gelir.

## Model kataloğu

Katalog, kısa takma adlarla (alias) tanımlanan, önceden optimize edilmiş modelleri içerir. Örneğin `qwen3-embedding-0.6b` metni vektöre çeviren bir embedding modeli, `qwen2.5-0.5b` ise cevap üreten küçük bir sohbet modelidir. Daha küçük modeller daha hızlı yanıt verir ama daha büyükleri genelde daha iyi cevap üretir; bu yüzden hız mı kalite mi istediğine göre seçim yaparsın.

## SDK

Foundry Local SDK; Python, C#, JavaScript ve Rust için mevcuttur. Python'da bir `FoundryLocalManager` başlatır, `manager.catalog` üzerinden bir model alır, indirip yükler ve ardından bir embedding istemcisi ya da bir sohbet istemcisi istersin. Sohbet istemcisi, tek bir yanıt için `complete_chat`, üretilen token'ları anlık akıtmak için ise `complete_streaming_chat` yöntemini sunar.
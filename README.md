## 📊 Veri Seti (Dataset) ve Erişim Linki

Bu projede, iç tehdit tespiti ve kullanıcı davranış analitiği (UEBA) alanında kabul edilen **CERT Insider Threat Dataset (v4.2)** kullanılmıştır. 

* 🔗 **Resmi Veri Seti ve Kaynak Erişimi:** Veri setinin (v4.2) orijinal yayın bültenine, dokümantasyonuna ve indirme talebi sayfasına doğrudan Carnegie Mellon Üniversitesi Yazılım Mühendisliği Enstitüsü üzerinden erişebilirsiniz: [Carnegie Mellon University SEI - CERT Insider Threat Dataset]
https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24856766
* 💾 **Depodaki İşlenmiş Veri (`final_risk_table.csv`):**  Colab ortamında ön işleme tabi tutulmuş, SMOTE ve LSTM Autoencoder modelinin eğitimi ile test süreçlerinde kullanılan özetlenmiş anomali skorları tablosu platformun çalışabilmesi için projeye dahil edilmiştir.

🛠️ Veri Ön İşleme ve Mühendislik Adımları (Colab Süreci)
Ham CERT v4.2 veri seti üzerinde LSTM modelinin eğitilmesinden önce, veriyi anlamlı bir zaman serisi formatına sokmak için Colab ortamında aşağıdaki veri işleme boru hattı (pipeline) uygulanmıştır:

1. Logların Birleştirilmesi (Data Aggregation)
CERT veri seti içerisinde dağınık halde bulunan farklı log dosyaları (logon.csv, email.csv, file.csv, device.csv) tekil kullanıcı kimlikleri (User ID) ve zaman damgaları (Timestamp) baz alınarak birleştirilmiş; her personelin günlük hareket dökümü tek bir tabloya indirilmiştir.

2. Öznitelik Çıkarımı (Feature Engineering)
Modelin "anormal" davranışları öğrenebilmesi için ham loglardan anlamlı matematiksel öznitelikler türetilmiştir. Örneğin:

Mesai saatleri dışı (gece/hafta sonu) sisteme giriş yapma sıklığı.

Günlük gönderilen e-posta sayısındaki ani artışlar.

Harici diske (USB) aktarılan dosya boyutları.

Rolüyle eşleşmeyen bilgisayarlara (PC) erişim denemeleri.

3. Kategorik Verilerin Dönüştürülmesi ve Ölçeklendirme (Scaling)
Kullanıcı departmanı, rolü veya bağlandığı PC adı gibi metinsel ifadeler (kategorik veriler) Label Encoding / One-Hot Encoding teknikleriyle sayısal vektörlere dönüştürülmüştür. Ardından, özelliklerin değer aralıklarının (örneğin USB'ye atılan 500 MB veri ile 1 kez yapılan giriş işlemi) modeli yanıltmaması için MinMaxScaler/StandardScaler kullanılarak tüm veriler ortak bir ölçeğe (0 ile 1 arasına) standardize edilmiştir. (Bu ölçekleyici, web arayüzünde canlı verileri işlemek için ueba_scaler.pkl olarak dışa aktarılmıştır.)

4. Zaman Serisi Pencereleme (Sequencing / Sliding Window)
Kullanılan LSTM (Long Short-Term Memory) mimarisi olayları tekil olarak değil, ardışık seriler halinde öğrenir. Bu nedenle kullanıcıların günlük davranışları, "Zaman Pencereleri" (Sliding Windows - örn: 5 günlük davranış blokları) halinde gruplandırılmış ve modelin giriş katmanının beklediği 3 boyutlu [Örnek Sayısı, Zaman Adımı, Öznitelik Sayısı] matris formatına (Tensor) dönüştürülmüştür.

5. Sınıf Dengesizliğinin Giderilmesi (SMOTE)
Veri setinde milyonlarca normal kullanıcı hareketine karşılık sadece 72 adet gerçek hacker (tehdit) eylemi bulunması, modelin azınlık sınıfını ezberlemesine veya körleşmesine yol açmaktadır. Bu durumu çözmek için SMOTE (Synthetic Minority Over-sampling Technique) algoritması kullanılmış ve tehdit sınıfının veri uzayındaki sentetik örnekleri üretilerek modelin her iki sınıfı da adil bir şekilde öğrenmesi sağlanmıştır.

6. Model Eğitimi ve Final Çıktısının Üretilmesi
LSTM Autoencoder ağı bu işlenmiş veri üzerinde eğitilmiş, her bir personelin davranış serisi için bir "Yeniden Yapılandırma Hatası" (Reconstruction Error / Anomaly Score) hesaplanmıştır. Eşik değeri (Threshold) dinamik olarak %84'e sabitlendikten sonra, elde edilen risk skorları web arayüzünün (Flask) kullanabilmesi için final_risk_table.csv olarak dışa aktarılmıştır.

## 📚 Referanslar ve Akademik Literatür

Bu projenin makine öğrenmesi mimarisi, veri ön işleme adımları ve XAI (Açıklanabilir Yapay Zeka) entegrasyonu, siber güvenlik literatüründe kabul görmüş aşağıdaki akademik çalışmalara dayandırılarak geliştirilmiştir:

* Ana Mimari (LSTM & Zaman Serisi Analizi):
  > Tuor, A., Kaplan, S., Hutchinson, B., Nichols, N., & Robinson, S. (2017). *"Deep Learning for Unsupervised Insider Threat Detection in Structured Cybersecurity Data Streams"*. arXiv preprint. 
  > Resmi Kaynak: [https://arxiv.org/abs/1710.00811](https://arxiv.org/abs/1710.00811)

* Sınıf Dengesizliği Çözümü (SMOTE):
  > Bin Sarhan, B., & Altwaijry, N. (2023). *"Insider Threat Detection Using Machine Learning Approach"*. Applied Sciences (MDPI), 13(1), 259. 
  > Resmi Kaynak: [https://www.mdpi.com/2076-3417/13/1/259](https://www.mdpi.com/2076-3417/13/1/259)

* Açıklanabilir Yapay Zeka (XAI) Entegrasyonu:
  > Alketbi, K. S., & Mehmood, A. (2025). *"A Comprehensive Survey of Explainable Artificial Intelligence Techniques for Malicious Insider Threat Detection"*. IEEE Access, Vol. 13.
  > Resmi Kaynak: [https://ieeexplore.ieee.org/document/11075748](https://ieeexplore.ieee.org/document/11075748)


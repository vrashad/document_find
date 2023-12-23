# Sənəd axtarışı
[multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) və [ChromaDB](https://www.trychroma.com/) istifadə edərək, təbii dildə sənəd axtarışını həyata keçirən proyekt.


## İstifadə qaydası:


### 1- Sənədlərin vektorlaşdırılması

İlk olaraq [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) modelindən istifadə edərək, txt formatında olan sənədləri vektorlaşdırmaq lazımdır və sonra əldə olunan vektorları [ChromaDB](https://www.trychroma.com/) vasitəsilə tərtib edilən vektor məlumatlar bazasına daxil etmək lazımdır

Mən test üçün Dövlət Yol Polisinə aid olan qanunvericilik toplusundan istifadə edirəm. Siz istədiyiniz sənədlərdən istifadə edə bilərsiniz

Sənədləri hazırladıqdan sonra, onları bir qovluğda toplayırıq. Bu mövzuda sənədlərin normallaşdırılmasına toxunmayacağıq

Sonra vektorların saxlanacağı boş qovluğu təyin etməliyik

Gəlin bu məqsədlə `vectors` adlı boş qovluqdan istifadə edək

Bu etapları bitirdikdən sonra, lazım olan paketləri yükləməliyik

```bash
pip install chromadb sentence-transformers
```

Paketlərin yüklənilməsi başa çatdıqdan sonra, sənədlərin vektorlaşdırılması əməliyyata keçirik

```bash
vector_generate.py
```

Script-i icra edərkən bizdən bəzi məlumatların daxil edilməsi tələb olunacaq

**Please enter collection name:** Vektorların saxlanıldığı kolleksiyanın adı (misal üçün `DYP`)<br>
**Please enter collection folder:** Vektorların saxlanılacağı boş qovluğun tam ünvanı (misal üçün `D:\GitHub\document_find\vectors`)<br>
**Please enter source TXT files folder:** Sənədlərin yerləşdiyi qovluğun tam ünvanı (misal üçün `D:\GitHub\document_find\documents`)<br>
**Use default model ? Y/N (Default: intfloat/multilingual-e5-large:** Burada əgər başqa bir modeldən istifadə edilməyəcəksə, o zaman sadəcə `Y` daxil etmək lazımdır


Vektorlaşma prosesi bitdikdən sonra, `vectors` qovluğunda SQLite formatında fayl və indeks adına uyğun olaraq qovluq əmələ gələcək

Bu o deməkdir ki, vektorlaşma başa çatdı və sənədlərin vektorları fiziki olaraq məhz bu qovluqda saxlanılır

### 2- Sənədlərin axtarışı

Sənədləri vektorlaşdırdıqdan sonra, axtarış prosessinə keçə bilərik

```bash
seach.py
```

Script-i icra edərkən bizdən bəzi məlumatların daxil edilməsi tələb olunacaq

**Please enter search query:** Axtarış sorğusu (misal üçün `Baş Dövlət Yol Polisi İdarəsinin rəisinin əlaqə nömrəsi`)<br>
**Count of most suitable documents:** Axtarışa ən çox uyğun olan sənədlərin sayı (misal üçün `5`)<br>
**Please enter collection name:** Vektorların saxlanıldığı kolleksiyanın adı `DYP`. Bu ad axtarışın həyata keçiriləcəyi sənədlərin vektorlarının saxlanıldığı kolleksiyanın adına tam uyğun olmalıdır<br>
**Please enter collection folder:** Vektorların saxlanılacağı boş qovluğun tam ünvanı `D:\GitHub\document_find\vectors`. Bu ad ünvan axtarışın həyata keçiriləcəyi sənədlərin vektorlarının saxlanıldığı qovluğun ünvanına tam uyğun olmalıdır<br>
**Use default model ? Y/N (Default: intfloat/multilingual-e5-large:** Burada əgər başqa bir modeldən istifadə edilməyəcəksə, o zaman sadəcə `Y` daxil etmək lazımdır. Sənədləri vektorlaşdırdıqda hansı modeldən istifadə etmişiksə, axtarışda da o modeldən istifadə etməliyik


Misal üçün əgər belə bir axtarış həyata keçirsək
`İçkili halda avtomobil idarə etmənin cəriməsi`

Belə bir nəticə əldə edəcəyik
```
ID: 8, Distance: 0.35491715843068655, Source: Cərimələr.txt
ID: 14, Distance: 0.3563939807194985, Source: Piyadanın məsuliyyəti.txt
ID: 25, Distance: 0.3725210719916774, Source: Nəqliyyat vasitələri sürücülərinin hazırlanması və onların ixtisasının artırılması kursları haqqında Əsasnamə.txt
ID: 23, Distance: 0.3793541471490398, Source: Sürücülük vəsiqəsinin verilməsi və dəyişdirilməsi.txt
ID: 18, Distance: 0.38118660012431993, Source: Sürücülük vəsiqələrinin verilməsi və dəyişdirilməsi qaydaları haqqında TƏLİMAT.txt
```

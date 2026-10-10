# Swagger UI vs. Redoc — Decision Report (US-5.4)

**Шийдвэр:** Олон нийтэд нээлттэй баримтад **Redoc**, багийн дотоод туршилтад **Swagger UI** ашиглана.

**Хайлт:** Redoc нь endpoint, параметр, тайлбар дундаас шууд хайдаг суурилагдсан хайлттай; Swagger UI зөвхөн tag-аар шүүдэг тул 6 endpoint-оос илүү болоход хайх нь удаашрана.
**Уншигдах байдал:** Redoc-ийн гурван баганат layout нь тайлбар, schema, Python `x-codeSamples`-ыг зэрэгцүүлж, нэг HTML файлд prerender хийгддэг. Swagger UI нэг баганатай, schema нь эвхэгддэг.
**Try-It-Out:** Swagger UI-ийн sandbox нь Authorize → Execute-ээр хүсэлтийг шууд илгээж, curl командыг үүсгэдэг; Redoc-д энэ боломж үнэгүй хувилбарт байхгүй. Манай Swagger UI нь GitHub Pages дээр service worker mock-оор backend-гүйгээр хариу өгдөг.

Иймээс уншигч Redoc-оор ойлгож, хөгжүүлэгч Swagger UI-аар туршина.

# AI Workbench MCP — Sıfırdan Kullanım Rehberi

MCP'yi daha önce hiç kullanmadıysan buradan başla.

Model Context Protocol'ün bütün teknik ayrıntılarını bilmen gerekmiyor.

En basit model:

**AI hostun → adı belli bir tool çağırır → AI Workbench MCP yerel katalogdan metin döndürür**

Bu sunucu bilerek küçük ve salt-okunur tutuldu.

---

## 1. MCP server nedir?

MCP server, uyumlu bir AI hostuna şeması belli araçlar/kaynaklar sunar.

AI Workbench MCP sadece üç tool sunar:

| Tool | Ne zaman? | Sonuç |
| --- | --- | --- |
| `list_prompts` | geçerli prompt/asistan ID'lerini bilmiyorsan | katalog bilgisi |
| `render_prompt` | bir prompt şablonunu kendi girdilerinle doldurmak istiyorsan | düz prompt metni |
| `get_assistant` | tekrar kullanılabilir assistant blueprint istiyorsan | host formatında Markdown |

---

## 2. Bu sunucu ne YAPMAZ?

- web'e çıkmaz;
- ChatGPT/Claude/Gemini/Grok API çağrısı yapmaz;
- shell komutu çalıştırmaz;
- dosya yazmaz/silmez;
- hesaba giriş yapmaz;
- sosyal medya paylaşımı yapmaz;
- cookie/credential okumaz.

Amaç zaten küçük ve incelenebilir bir MCP sınırı oluşturmaktır.

---

## 3. Gerekenler

- Python 3.10+
- terminal
- gerçek host kullanımı için MCP destekli bir istemci

Yerel doctor testi için API key gerekmez.

---

## 4. Güncel alpha sürümünü kur

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a2"
```

Birden fazla Python ortamın varsa, MCP hostunun çalıştıracağı Python ortamına kur.

---

## 5. İlk test: doctor

Host ayarı yapmadan önce:

```bash
alptugharun-ai-workbench-mcp --doctor
```

Sağlıklı JSON çıktısında şunlar olur:

- `"status": "pass"`
- paket sürümü
- Python sürümü
- üç public tool
- prompt/asistan sayıları
- yerel permission sınırı

### Doctor neyi kanıtlar?

Paket ve yerel katalog yüklenebiliyor.

### Neyi kanıtlamaz?

Cursor/Claude/başka host ayarının doğru olduğunu kanıtlamaz.

---

## 6. Üç tool'u nasıl seçersin?

### A — önce list_prompts

ID bilmiyorsan önce bunu çağır.

Prompt ve assistant ID/title/purpose listesini alırsın.

### B — render_prompt

Bir promptu değişkenlerle doldurup **son prompt metni** istiyorsan kullan.

Eksik/fazla variable varsa sunucu hata verir.

Assistant blueprint istiyorsan bunun yerine `get_assistant` kullan.

### C — get_assistant

Aynı işi:

- ChatGPT;
- Claude;
- Gemini;
- Grok;
- Agent Skill

formatında reusable instruction olarak istiyorsan kullan.

Bu tool hesabında otomatik assistant oluşturmaz veya yayınlamaz.

Tek seferlik doldurulmuş prompt istiyorsan `render_prompt` kullan.

---

## 7. Gerçek MCP hostuna bağla

Gerçek test yaptığımız host Cursor.

Kullan:

- `CURSOR-SETUP_TR.md`
- `HOST-VERIFICATION.md`

Başka MCP istemcisinin ayar formatı farklı olabilir.

Cursor config'ini evrensel sayma.

---

## 8. Doğrulama merdiveni

Sıra:

**kuruldu → doctor PASS → handshake → host 3 tool'u gördü → tool çağrıldı → beklenen çıktı**

Bir adımın başarılı olması diğerini otomatik kanıtlamaz.

---

## 9. Hata olursa

`TROUBLESHOOTING.md` dosyasını kullan.

Sık sorunlar:

- command not found → yanlış Python/PATH
- host connected ama tool yok → discovery/config/reload
- unknown ID → önce list_prompts
- variable mismatch → exact variable seti
- Windows/WSL → host hangi taraftan çalışıyorsa paketi aynı tarafta kur

---

## 10. Güvenlik modeli

Her tool:

```json
{
  "readOnlyHint": true,
  "destructiveHint": false,
  "idempotentHint": true,
  "openWorldHint": false
}
```

bildirir.

Bu sadece **bu implementation** için kanıttır.

“Bütün MCP server'lar güvenli” demek değildir.

---

## 11. PyPI / Registry

Güncel alpha:

`alptugharun-ai-workbench-mcp==0.1.0a2`

Resmi MCP Registry adı:

`io.github.alptugharun/ai-workbench-mcp`

PyPI yayını GitHub OIDC Trusted Publishing kullanır ve release wheel'i Sigstore ile imzalanır.

---

## 12. İlk neyi deneyeyim?

Sadece mantığı görmek istiyorsan:

1. kur;
2. `--doctor`;
3. üç tool açıklamasını oku.

Gerçek host testi istiyorsan:

1. doctor;
2. Cursor kurulumu;
3. list_prompts;
4. bir prompt render;
5. bir assistant blueprint;
6. PASS/FAIL/BLOCKED raporu.

---

## 13. Ne zaman bunu kullanmamalıyım?

Şunlara ihtiyacın varsa bu server doğru araç değil:

- web araştırması;
- dosya düzenleme;
- sosyal paylaşım;
- hesap yönetimi;
- model API çağrısı;
- geniş yetkili otonom agent.

İşe yarayan en küçük permission yüzeyini kullan.

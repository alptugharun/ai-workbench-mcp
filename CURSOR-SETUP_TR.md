# Cursor kurulumu — AI Workbench MCP

Bu rehber, yayınlanmış `alptugharun-ai-workbench-mcp==0.1.0a1` paketini Cursor içinde çalışan yerel bir stdio MCP sunucusuna dönüştürür.

Şu an kayıtlı maintainer doğrulaması Cursor 3.20.21 üzerindedir. Host davranışı değişebileceği için hata raporlarında Cursor ve paket sürümünü birlikte belirt.

## Kurulum sonunda ne olacak?

Cursor şu üç salt-okunur tool'u görmeli:

- `list_prompts`
- `render_prompt`
- `get_assistant`

Sunucu ağ erişimi, shell çalıştırma, hesap erişimi, dosya yazma veya provider API erişimi istemez.

## 1. Python sürümünü kontrol et

Python 3.10 veya üstü gerekir.

```bash
python --version
```

Bilgisayarında Python 3 için farklı bir komut kullanıyorsan sonraki adımlarda da aynı komutu kullan.

## 2. PyPI'deki exact sürümü kur

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a1"
```

Aynı Python ortamının paketi gördüğünü doğrula:

```bash
python -c "import ai_workbench_mcp; print(ai_workbench_mcp.__version__)"
```

Beklenen çıktı:

```text
0.1.0a1
```

## 3. Cursor MCP ayarını ekle

Cursor proje bazlı ayarı burada okuyabilir:

```text
.cursor/mcp.json
```

Global kullanıcı ayarı ise burada olabilir:

```text
~/.cursor/mcp.json
```

Repodaki test edilebilir örnek: [examples/cursor-mcp.json](examples/cursor-mcp.json)

```json
{
  "mcpServers": {
    "ai-workbench-mcp": {
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "ai_workbench_mcp.server"
      ]
    }
  }
}
```

Buradaki kritik nokta: Cursor'ın çalıştırdığı `python`, paketi kurduğun Python ortamı olmalı.

### Cursor farklı Python kullanıyorsa

Kurulum yaptığın interpreter yolunu bul:

```bash
python -c "import sys; print(sys.executable)"
```

Ardından config içindeki `"command": "python"` değerini bu tam yolla değiştir.

Windows JSON yollarında ters bölü işaretlerini kaçır:

```json
{
  "mcpServers": {
    "ai-workbench-mcp": {
      "type": "stdio",
      "command": "C:\\Path\\To\\python.exe",
      "args": [
        "-m",
        "ai_workbench_mcp.server"
      ]
    }
  }
}
```

## 4. Cursor'ın sunucuyu gördüğünü kontrol et

Cursor'ın MCP / Customize ekranında `ai-workbench-mcp` bağlantısının göründüğünü kontrol et.

Cursor CLI kullanıyorsan güncel Cursor dokümantasyonunda şu komutlar da bulunuyor:

```bash
agent mcp list
agent mcp list-tools ai-workbench-mcp
```

Tool listesinde tam olarak şunları görmelisin:

```text
list_prompts
render_prompt
get_assistant
```

## 5. Üç gerçek host testini çalıştır

Sadece “Connected” yazması yeterli kanıt değildir. Tool'ları gerçekten çağır.

### Test A — katalog

Cursor'a şunu yaz:

```text
Use the MCP server ai-workbench-mcp. Call list_prompts. Return only the tool result.
```

Beklenen kanıt:

- prompt kayıtları gelir;
- assistant kayıtları gelir;
- güncel paket kataloğunda 12 prompt ve 4 assistant bulunur.

### Test B — prompt render

Cursor'a şunu yaz:

```text
Use the MCP server ai-workbench-mcp. Call render_prompt with prompt ID evidence-brief.
Use question = Should we publish this as a public alpha?
Use sources = S1: The package is installed. S2: The host called list_prompts successfully.
Use language = English.
Do not invent evidence. Return only the rendered prompt.
```

Beklenen:

- `render_prompt` gerçekten çağrılır;
- verdiğin değişkenler rendered prompt içine girer;
- yeni/uydurma kaynak eklenmez.

### Test C — assistant export

Cursor'a şunu yaz:

```text
Use the MCP server ai-workbench-mcp. Call get_assistant with assistant ID evidence-desk and target chatgpt. Do not answer from memory. Return only the tool result.
```

Beklenen sonuç içinde şunlar bulunur:

- Status
- Instructions
- Conversation starters
- Acceptance checks

## Sorun çözme

### Cursor “disconnected” diyorsa

Önce config'teki Python'ın paketi görebildiğini kontrol et:

```bash
python -c "import ai_workbench_mcp; print(ai_workbench_mcp.__version__)"
```

Çalışmıyorsa paketi o interpreter'a kur veya config'te paketin kurulu olduğu interpreter'ın tam yolunu kullan.

### `alptugharun-ai-workbench-mcp` komutu bulunamıyorsa

Console-script klasörü PATH içinde olmayabilir. Bu rehberdeki config bu sorunu azaltmak için doğrudan şunu çalıştırır:

```text
python -m ai_workbench_mcp.server
```

### Terminalde çalıştırınca hiçbir şey olmuyorsa

Bu normal olabilir. Bu bir stdio MCP sunucusudur; stdin üzerinden MCP JSON-RPC mesajı bekler. Normal interaktif terminal uygulaması gibi menü göstermez.

### Cursor bağlanıyor ama tool hata veriyorsa

Şunları kaydet:

- Cursor sürümü;
- paket sürümü;
- Python executable yolu;
- tool adı;
- gönderilen argümanlar;
- beklenen sonuç;
- dönen hata.

Yalnız bağlantı başarılı diye host'u “verified” sayma.

## Repo testleri

Repoyu clone ettiysen:

```bash
python -m unittest discover -s tests -v
python examples/smoke_client.py
```

Bunlar paket/protokol davranışını doğrular. Cursor içindeki gerçek tool çağrılarının yerine geçmez.

## Kaldırma

Önce ilgili Cursor `mcp.json` dosyasından `ai-workbench-mcp` kaydını kaldır.

Ardından:

```bash
python -m pip uninstall alptugharun-ai-workbench-mcp
```

## Kanıt sınırı

Başarılı Cursor testi, belirli bir host/sürümün belirli ortamda tool'ları çağırabildiğini kanıtlar. Tüm MCP istemcilerinde evrensel uyumluluk anlamına gelmez.

Dated maintainer doğrulaması için [HOST-VERIFICATION.md](HOST-VERIFICATION.md) dosyasına bak.

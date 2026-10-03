# AI Workbench MCP

[![English](https://img.shields.io/badge/English-0D1117?style=flat-square)](README.md) [![Türkçe](https://img.shields.io/badge/Türkçe-E30A17?style=flat-square)](README_TR.md)

**Yeniden kullanılabilir AI promptları ve asistan blueprint'leri için küçük, salt-okunur bir MCP sunucusu.**

AI Workbench MCP, yerel bir kataloğu Model Context Protocol stdio üzerinden sunar. Tasarım amacı özellikle dar tutuldu:

- ağ çağrısı yok;
- shell çalıştırma yok;
- hesap erişimi yok;
- dosya yazma yok;
- gizli model/provider çağrısı yok;
- runtime tarafında Python standart kütüphanesi dışında bağımlılık yok.

## Üç araç

| Araç | Ne döndürür? |
| --- | --- |
| `list_prompts` | Paket içindeki prompt ve asistan kataloğunu listeler |
| `render_prompt` | Bir prompt şablonunu verilen string değişkenlerle doldurur |
| `get_assistant` | ChatGPT, Claude, Gemini, Grok veya Agent Skill için asistan blueprint'i döndürür |

## Hızlı başlangıç

PyPI'deki yayınlanmış alpha sürümünü kur:

```bash
python -m pip install "alptugharun-ai-workbench-mcp==0.1.0a1"
```

Ardından stdio destekli MCP hostunun çalıştıracağı komut:

```text
alptugharun-ai-workbench-mcp
```

Gerçek host testi yaptığımız Cursor için kopyala-yapıştır [Cursor kurulum + 3 tool doğrulama rehberini](CURSOR-SETUP_TR.md) kullan. Diğer MCP istemcilerinin config yapısı farklı olabilir; Cursor ayarını evrensel varsayma.

## Güvenlik modeli

Her tool açık biçimde şunları bildirir:

- `readOnlyHint: true`
- `destructiveHint: false`
- `idempotentHint: true`
- `openWorldHint: false`

Kod ayrıca network, subprocess, dosya yazma veya provider SDK modülleri kullanmaması için test edilir.

## Test

```bash
python -m unittest discover -s tests -v
python examples/smoke_client.py
```

CI Linux ve Windows üzerinde çalışır.

## PyPI / MCP Registry

**PyPI:** `alptugharun-ai-workbench-mcp==0.1.0a1` GitHub OIDC Trusted Publishing ile yayınlandı. Release workflow'u wheel dosyasını keyless Sigstore ile de imzalıyor.

Temiz bir Windows sanal ortamında PyPI'den exact version kurulumu başarıyla doğrulandı; MCP `2025-06-18` handshake'i, üç tool'un listelenmesi, başarılı `render_prompt` / `get_assistant` çağrıları ve bilinmeyen tool için kontrollü hata yolu test edildi.

**Resmi MCP Registry:** `io.github.alptugharun/ai-workbench-mcp` production registry'de yayınlandı ve şu anda `active` görünüyor.

**Gerçek host doğrulaması:** maintainer-run Cursor 3.20.21 testinde `list_prompts`, `render_prompt` ve `get_assistant` başarıyla çağrıldı. Bu kanıt bağımsız üçüncü taraf doğrulaması veya tüm MCP hostları için evrensel uyumluluk iddiası değildir.

Ayrıntılar: [REGISTRY-PUBLISHING.md](REGISTRY-PUBLISHING.md) · [HOST-VERIFICATION.md](HOST-VERIFICATION.md) · [Cursor kurulum rehberi](CURSOR-SETUP_TR.md).

Bu proje [AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit) içinden ayrıştırıldı.

**Alptuğ Harun** tarafından geliştiriliyor.

## Lisans

MIT.

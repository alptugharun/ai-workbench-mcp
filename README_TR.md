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

```bash
python -m venv .venv
python -m pip install -e .
python examples/smoke_client.py
```

Başarılı çalıştırmada MCP handshake sonucu ve üç tool adı görünür.

MCP hostunun çalıştıracağı komut:

```text
alptugharun-ai-workbench-mcp
```

Host'a özel ayarlar zamanla değişebildiği için kullandığın MCP istemcisinin güncel dokümantasyonunu takip et.

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

İlk paket adayı `0.1.0a1`.

PyPI ve resmi MCP Registry yayını, gerçek yayın ve temiz kurulum doğrulanmadan "tamamlandı" olarak gösterilmeyecek. Ayrıntılar için [REGISTRY-PUBLISHING.md](REGISTRY-PUBLISHING.md).

Bu proje [AI Social Media Toolkit](https://github.com/alptugharun/ai-social-media-toolkit) içinden ayrıştırıldı.

**Alptuğ Harun** tarafından geliştiriliyor.

## Lisans

MIT.

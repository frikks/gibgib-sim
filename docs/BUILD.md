# Сборка веб-версии 3.4.0

`GibGib-Sim-3.4.0.html` — сгенерированный файл. **Не редактируйте его вручную.** Ниже описано, как он получается.

## Исходники

| Что | Значение |
|---|---|
| Архив исходников | `GibGib-Sim-3.3.3.3-source-NO-KEY.zip` (приватный репозиторий `frikks/gibgib-sim-source`, локальная резервная копия) |
| Версия в Cargo.toml / `lib.rs` | 3.4.0 (было 3.3.3 / 3.3.3.3) |
| Инструмент | Rust 1.99.1, цель `wasm32-unknown-unknown` |
| wasm-bindgen CLI | 0.2.130 |

## Подготовка сборки

Исходники приватные, поэтому patch-файлы в этот репозиторий не попадают. Для wasm-цели применяются следующие изменения:

1. `Cargo.toml`: `eframe` перенесён в target-зависимости; для `wasm32` добавлены `eframe` (glow + default_fonts), `wasm-bindgen-futures`, `js-sys`, `web-sys` (Url, HtmlAnchorElement, Blob, Document, Window, Element), `web-time`.
2. `src/web.rs`: точка входа `#[wasm_bindgen(start)]`, создающая `eframe::WebRunner` на canvas `#gibgib_canvas`.
3. `src/lib.rs`: алиасы `Instant`/`SystemTime`/`UNIX_EPOCH` из `web-time`, вспомогательная функция `instant_ago()` (web-time-INSTANT начинается с загрузки страницы), синхронная замена `std::thread` для wasm.
4. Вызовы `std::thread::spawn` / `thread::scope` заменены на синхронный шим (браузер однопоточен).
5. `save_bytes` / `print_bytes`: на wasm файлы отдаются через Blob + `URL.createObjectURL` вместо `std::fs`.
6. `VERSION` выставлен в `3.4.0`.

## Команды

```sh
cargo build --release --target wasm32-unknown-unknown --lib
wasm-bindgen target/wasm32-unknown-unknown/release/listogib_native.wasm \
  --out-dir webout --target web
python3 build_wasm_html.py   # встраивает .js и base64 .wasm в один HTML
```

Скрипт `build_wasm_html.py` живёт в рабочей среде сборки и в публичный репозиторий не входит: он подставляет сгенерированный JS и base64 WASM в HTML-шаблон с canvas и экраном загрузки.

## Контрольная сумма

Ожидаемый SHA-256 готового файла:

```
ab376799b5cc1cbe646569a1f9a8be3d36821bb42ccdd0720ee0d01feab09c71
```

Проверка:

```sh
sha256sum GibGib-Sim-3.4.0.html
git show origin/main:GibGib-Sim-3.4.0.html | sha256sum
```

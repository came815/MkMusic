# MkMusic
煩雑に並んだ音楽ファイルのメタデータの読み取り、アーティスト名→アルバム名のディレクリを作り、整理します。
また、音楽ファイル本体の名前も"アーティスト名-アルバム名-曲名.拡張子"に変更します。
ex.)amazarashi - 季節は次々死んでいく - 季節は次々死んでいく.mp3

# Requirement

* mutagen 1.45.1
* Pillow 8.1.0

# Usage

1. musicSrcフォルダに整理したい音楽ファイルを入れてください。
   この時、音楽ファイルがディレクリの下の階層にあったり、音楽以外のファイルがあっても、音楽ファイルだけ抽出しますので気にしないでください。
2. 以下のコマンドまたは、musicEdit.batを実行してください。

```bash
python ./MusicSortID3.py ./musicSrc ../musicEdited
```

3. musicEditedフォルダが作れられますので、そこに整理された音楽フォルダがあります。

# Note

音楽ファイルのID3タグの読み込んで実行してるので、ID3タグが入力されていない場合失敗することがあります。
通常は最初からID3タグ情報が入力されているはずですが、もしなかった場合は先にタグ情報を入力してから実行してください。

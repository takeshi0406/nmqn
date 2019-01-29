# nmqn

サイトの変更をCSSの差分でレポーティングするためのツールです。

## Installation

pandocに依存しています。

```bash
brew install pandoc
pip install nmqn
```

## Usage

設定ファイルの仕様は、GitHubリポジトリの `sample.yaml` を確認してください。

```bash
# sample.yamlの設定を基にクロール
nmqn crawl -c sample.yaml

# 前日分と比較し、HTMLのレポートを生成
nmqn compare -c sample.yaml
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web PCK Editor - Local Development Server
ローカルでHTMLファイルを実行するための簡易HTTPサーバー
"""

import http.server
import socketserver
import os
import sys
import socket
from pathlib import Path

# ポート番号（環境変数で変更可能）
PORT = int(os.environ.get('PORT', 8000))

# このスクリプトがあるディレクトリをルートとする
os.chdir(Path(__file__).parent)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """カスタムHTTPリクエストハンドラー"""
    
    def end_headers(self):
        # CORSヘッダーを追加（必要に応じて）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # キャッシュを無効化（開発時に便利）
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        """ログメッセージをカスタマイズ"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def get_local_ip():
    """ローカルIPアドレスを取得"""
    try:
        # ダミー接続を作成してローカルIPを取得
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "不明"

def main():
    """メイン関数"""
    try:
        # TCPサーバーを作成（再利用可能に設定）
        socketserver.TCPServer.allow_reuse_address = True
        
        # 0.0.0.0 でバインド（すべてのネットワークインターフェースで待機）
        with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
            local_ip = get_local_ip()
            
            print("=" * 60)
            print("🚀 Web PCK Editor - ローカルサーバー起動")
            print("=" * 60)
            print(f"📂 ルートディレクトリ: {os.getcwd()}")
            print()
            print("🌐 アクセス方法:")
            print(f"   PC本体から: http://localhost:{PORT}/WebPCKEditor.html")
            if local_ip != "不明":
                print(f"   スマホから: http://{local_ip}:{PORT}/WebPCKEditor.html")
                print()
                print(f"💡 スマホのブラウザで上記のURLを入力してください")
                print(f"   （PCとスマホが同じWi-Fiに接続されている必要があります）")
            print("=" * 60)
            print("✋ 停止するには Ctrl+C を押してください")
            print("=" * 60)
            print()
            
            # ブラウザを自動的に開く（オプション：--browserフラグで有効化）
            if '--browser' in sys.argv:
                try:
                    import webbrowser
                    webbrowser.open(f'http://localhost:{PORT}/WebPCKEditor.html')
                    print("🌐 PCのブラウザを起動しました\n")
                except Exception as e:
                    print(f"⚠️ ブラウザの自動起動に失敗: {e}\n")
            
            # サーバー起動
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 サーバーを停止しました")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:  # Address already in use
            print(f"\n❌ エラー: ポート {PORT} は既に使用されています")
            print(f"💡 別のポートを使用するには: PORT=8080 python server.py")
            sys.exit(1)
        else:
            raise

if __name__ == '__main__':
    main()

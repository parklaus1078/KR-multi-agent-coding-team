#!/bin/bash
# MACT CLI 설치 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
CLI_NAME="mact"

echo "🚀 MACT CLI 설치 시작..."
echo ""

# .local/bin 디렉토리 생성
mkdir -p "$INSTALL_DIR"

# 심볼릭 링크 생성
if [ -L "$INSTALL_DIR/$CLI_NAME" ]; then
    echo "⚠️  기존 설치 발견. 덮어쓰는 중..."
    rm "$INSTALL_DIR/$CLI_NAME"
fi

ln -s "$SCRIPT_DIR/mact.py" "$INSTALL_DIR/$CLI_NAME"
chmod +x "$SCRIPT_DIR/mact.py"

echo "✅ 심볼릭 링크 생성: $INSTALL_DIR/$CLI_NAME"

# PATH 확인
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  $INSTALL_DIR 가 PATH에 없습니다."
    echo ""
    echo "다음 명령어를 실행하여 PATH에 추가하세요:"
    echo ""

    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
    else
        echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    fi
    echo ""
else
    echo "✅ PATH 설정 확인됨"
fi

echo ""
echo "🎉 설치 완료!"
echo ""
echo "사용법:"
echo "  mact --help         # 도움말"
echo "  mact projects       # 프로젝트 목록"
echo "  mact init --name my-project"
echo ""
echo "시작하기:"
echo "  cd $SCRIPT_DIR"
echo "  mact projects"
echo ""

#!/usr/bin/env sh

sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

rm ~/.zshrc

ln -s ./dotfiles/.zshrc ~/.zshrc && sudo ln -s ./tmuxscripts/setterm /bin/setterm

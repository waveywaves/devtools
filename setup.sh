#!/usr/bin/env sh

# Tmux terminal init script
sudo ln -s $(pwd)/tmuxscripts/settermvibhav /usr/local/bin/

# zshrc setup
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
rm ~/.zshrc
cp $(pwd)/dotfiles/.zshrc ~/.zshrc 

# tmux setup
sudo cp $(pwd)/dotfiles/.tmux.conf ~/.tmux.conf
tmux source-file ~/.tmux.conf

# JenkinsInstallPlugin 
sudo ln -s $(pwd)/jenkinstools/jenkinsInstallPlugin/jip /usr/local/bin/

# Openshift Setup
sudo ln -s $(pwd)/openshiftscripts/* /usr/local/bin/

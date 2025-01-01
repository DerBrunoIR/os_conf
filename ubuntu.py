from lib import *
from unix import *



def main():
    config = Chain(
            Print("# install apt packages"),
            Chain(
                Apt('zsh'),
                Apt('xclip'),
                Apt('evince'),
                # Apt('vim'),
                Apt('firefox'),
                Apt('autojump'),

                Apt('jq'),
                Apt('git'),
                Apt('sed'),
                Apt('mawk'),
                Apt('grep'),
                Apt('tree'),
                Apt('bat'),
                Apt('tar'),
                Apt('zip'),
                Apt('ripgrep'),

                Apt('nmap'),
                Apt('dnsutils'),
                Apt('curl'),
                Apt('wget'),

                # Apt('maven'),
                Apt('clang'),
                Apt('gdb'),
            ),

            Print("# install flatpaks"),
            Chain(
                Apt('flatpak'),
                AddFlatpakRemote('flathub', 'https://dl.flathub.org/repo/flathub.flatpakrepo'),
                #Flatpak('com.google.Chrome'),
                Flatpak('com.discordapp.Discord'),
                Flatpak('com.spotify.Client'),
                Flatpak('org.mozilla.Thunderbird'),
                Flatpak('net.ankiweb.Anki'),
                Flatpak('org.kde.kdenlive'),
                Flatpak('com.github.jeromerobert.pdfarranger'),
                Flatpak('com.nextcloud.desktopclient.nextcloud'),
                Flatpak('org.onlyoffice.desktopeditors'),
                Flatpak('com.mattjakeman.ExtensionManager'),
                Flatpak('io.github.Qalculate'),
            ),

            Print("# install docker"),
            Chain(
                Command(
                    Shell('sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc'),
                    Shell('sudo rm /etc/apt/keyrings/docker.asc'),
                    Shell('test -f /etc/apt/keyrings/docker.asc'),
                    ),
                AddAptRepository('deb https://download.docker.com/linux/ubuntu focal stable'),
                Apt('docker-ce'),
                Apt('docker-ce-cli'),
                Apt('containerd.io'),
                Apt('docker-buildx-plugin'),
                Apt('docker-compose-plugin'),
            ),

            Print("# snap packages"),
            Chain(
                Snap('drawio'),
            ),

            Print("# setup python env"),
            Chain(
                    Apt('python3-pip'),
                    Apt('python3.12'),
                    Apt('python3.12-venv'),
                    Pip('ipython'),
                    Pip('ipdb'),
                    Pip('grip'),
                    Pip('docker'),
                    Pip('neovim'),
                    Pip('numpy'),
                    Pip('pandas'),
                    ),

            Print("# setup nvim"),
            Chain(
                    Print("## install nvim"),
                    Command(
                        Shell('sudo wget https://github.com/neovim/neovim/releases/download/v0.10.3/nvim.appimage -O /usr/local/bin/nvim'),
                        Shell('sudo rm /usr/local/bin/nvim'),
                        Shell('test -f /usr/local/bin/nvim'),
                        ),
                    Print("## clone nvim configuration"),
                    GitClone('git@github.com:DerBrunoIR/NeoVimConfig.git', '~/.config/nvim'),
                    ),

            Print("# install dotfiles"),
            Chain(
                GitClone('git@github.com:DerBrunoIR/dotfiles.git', '~/dotfiles'),
                Command(
                    Shell('~/dotfiles/install'),
                    Shell('~/dotfiles/uninstall'),
                    Shell('test -f ~/.zshrc'),
                ),
            ),

            Print("# install sdkman "),
            Chain(
                Command(
                    Shell("curl -s 'https://get.sdkman.io' | bash"),
                    Shell("rm -rf ~/.sdkman"),
                    Shell("test -f ~/.sdkman/bin/sdkman-init.sh"),
                ),
            ),

            Print("# install golang"),
            Chain(
                Command(
                    Shell('wget -qO- https://go.dev/dl/go1.20.1.linux-amd64.tar.gz | sudo tar xzf- -C /usr/local '),
                    Shell('sudo rm -rf /usr/local/go'),
                    Shell('test -d /usr/local/go'),
                    ),
            ),

            Print("# ohmyzsh"),
            Chain(
                Command(
                    Shell("sh -c $(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"),
                    Shell("yes | uninstall_oh_my_zsh"),
                    Shell("test -f ~/.oh-my-zsh"),
                ),
            ),

            Print("# starship prompt"),
            Chain(
                Print("## install starship"),
                From(
                    Command(
                        Shell("wget https://starship.rs/install.sh -O /tmp/install.sh && chmod u+x /tmp/starship_install.sh"),
                        Shell("rm /tmp/starship_install.sh"),
                        Shell("test -f /tmp/starship_install.sh"),
                    ), 
                    Command(
                        Shell("/tmp/starship_install.sh -y"),
                        Shell("rm '$(which starship)'"),
                        Shell("which starship"),
                    ),
                ),
                Print("## load starship config"),
                Command(
                    Shell('wgeth ttps://starship.rs/presets/toml/nerd-font-symbols.toml -o ~/.config/starship.toml'),
                    Shell('rm ~/.config/starship.toml'),
                    Shell('test -f ~/.config/starship.toml'),
                ),
            ),

            Print("# install JetBrainsMono nerd font"),
            Chain(
                From(
                    Command(
                        Shell("wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.zip -qO /tmp/JetrBrainsMono"),
                        Shell("rm /tmp/JetrBrainsMono.zip"),
                        Shell("test -f /tmp/JetBrainsMono.zip"),
                    ),
                    Command(
                        Shell("unzip /tmp/JetBrainsMono.zip -d ~/.fonts"),
                        Shell("rm ~/.fonts/JetBrainsMonoNerdFont*.ttf"),
                        Shell("test -f ~/.fonts/JetBrainsMonoNerdFont-Regular.ttf"),
                    ),
                ),
            ),

            Print("# install bat "),
            Chain(
                Apt('bat'),
                Command(
                    Shell('sudo ln -s /bin/batcat /bin/bat'),
                    Shell('sudo rm /bin/bat'),
                    Shell('test -L /bin/bat'),
                ),
            ),

            Print("# install pandoc "),
            From(
                Command(
                    Shell('wget https://github.com/jgm/pandoc/releases/download/3.6.1/pandoc-3.6.1-1-amd64.deb -O /tmp/pandoc.deb'),
                    Shell('rm /tmp/pandoc.deb'),
                    Shell('stat /tmp/pandoc.deb'),
                    ),
                Dpkg('/tmp/pandoc.deb'),
            ),
        )

    config.ensure_installed()



if __name__ == "__main__":
    main()



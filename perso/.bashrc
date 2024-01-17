shopt -s expand_aliases
export DEVEL_PATH=/home/odoo/devel

PATH=$PATH:$ODOO_PATH:/opt:$DEVEL_PATH/scripts/perso

ODOO_CUSTOM=$DEVEL_PATH/custom

export PYTHONPATH="$DEVEL_PATH/scripts/perso"

export INTERNAL=$DEVEL_PATH/internal

export SAAS=$INTERNAL/default,$INTERNAL/trial

export PRIVATE=$INTERNAL/private

alias posdd="sudo dd bs=4M status=progress"

# function cdcomm() {
# 	repo=0
# 	if [ ! -z $1 ]; then 
# 		repo=${1}
# 	fi
#     cd "$DEVEL_PATH/distr${repo}/odoo"
# }

# function cdent() {
# 	repo=0
# 	if [ ! -z $1 ]; then 
# 		repo=${1}
# 	fi
#     cd "$DEVEL_PATH/distr${repo}/enterprise"
# }

function ocd() {
    cd "$(odoo-worktree path $@)"
}

function __complete_ocd() {
    COMPREPLY=($(odoo-worktree bashcomplete $COMP_LINE));
}
complete -o nospace -S "/" -F __complete_ocd ocd

function __complete_orun() {
    COMPREPLY=($(odoo-worktree bashcomplete $COMP_LINE));
}
complete -o nospace -F __complete_orun orun

function cdowl() {
        repo=0
        if [ ! -z $1 ]; then
                repo=${1}
        fi

	cd "$DEVEL_PATH/distr${repo}/owl"
}

function gitsubl() {
    git config --global core.editor "subl -n -w"
}

function gitnano() {
    git config --global core.editor "nano"
}

function venv() {
	source $HOME/.python/venv${1}/bin/activate
}

# pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

#FORMER git integration for bash
#force_color_prompt=yes
# Add git branch if its present to PS1
# parse_git_branch() {
# git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
#}
#if [ "$color_prompt" = yes ]; then
# PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
#else
# PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w$(parse_git_branch)\$ '
#fi
#unset color_prompt force_color_prompt
# source /etc/bash_completion.d/git-prompt
# source ~/.scripts/git-completion.bash

# ## Print nickname for git/hg/bzr/svn version control in CWD
# ## Optional $1 of format string for printf, default "(%s) "
# function be_get_branch {
# 	local dir="$PWD"
# 	local vcs
# 	local nick
# 	while [[ "$dir" != "/" ]]; do
# 		for vcs in git hg svn bzr; do
# 		if [[ -d "$dir/.$vcs" ]] && hash "$vcs" &>/dev/null; then
# 			case "$vcs" in
# 				git) __git_ps1 "${1:-(%s) }"; return;;
# 				hg) nick=$(hg branch 2>/dev/null);;
# 				svn) nick=$(svn info 2>/dev/null\	
# 					| grep -e '^Repository Root:'\
# 					| sed -e 's#.*/##');;
# 				bzr)
# 					local conf="${dir}/.bzr/branch/branch.conf" # normal branch
# 					[[ -f "$conf" ]] && nick=$(grep -E '^nickname =' "$conf" | cut -d' ' -f 3)
# 					conf="${dir}/.bzr/branch/location" # colo/lightweight branch
# 					[[ -z "$nick" ]] && [[ -f "$conf" ]] && nick="$(basename "$(< $conf)")"
# 					[[ -z "$nick" ]] && nick="$(basename "$(readlink -f "$dir")")";;
# 			esac
# 			[[ -n "$nick" ]] && printf "${1:-(%s) }" "$nick"
# 			return 0
# 		fi
# 	done
# 	dir="$(dirname "$dir")"
# 	done
# 	}
# ## Add branch to PS1 (based on $PS1 or $1), formatted as $2
# export GIT_PS1_SHOWDIRTYSTATE=yes
# export PS1="\[\033[1;32m\]\$(be_get_branch "$2")\[\e[0m\]${PS1}";


#[alias]
#find = log --pretty=\"format:%Cgreen%H %Cblue%s\" --name-status --grep

_GITPROMPTPATH="$HOME/devel/.bash-git-prompt"

if [ -f "$_GITPROMPTPATH/gitprompt.sh" ]; then
	GIT_PROMPT_FETCH_REMOTE_STATUS=0
    GIT_PROMPT_ONLY_IN_REPO=1
    source $_GITPROMPTPATH/gitprompt.sh
fi

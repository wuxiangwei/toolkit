set encoding=utf-8
set termencoding=utf-8
set fileformat=unix
set relativenumber

set rtp+=~/.vim/bundle/Vundle.vim
" set rtp+=~/.vim/bundle/solarized/vim-colors-solarized  " colors
set rtp+=~/.vim/bundle/ethanschoonover.com/projects/solarized/vim-colors-solarized " colors
set rtp+=~/.vim/bundle/molokai

if has("win32")
    set fileencoding=chinese
    set nocompatible
    source $VIMRUNTIME/vimrc_example.vim
    source $VIMRUNTIME/mswin.vim
    behave mswin
else
    set fileencoding=utf-8
endif

" GUI设置
if has("gui_running")
    set guioptions-=m " 菜单栏
    set guioptions-=T " 工具栏
    " set guioptions-=r " 滚动栏
endif

" Begin vundle
filetype off  " required
call vundle#begin()
" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
" Plugin 'brantb/solarized'
Plugin 'altercation/ethanschoonover.com'
Plugin 'majutsushi/tagbar'
Plugin 'godlygeek/tabular'
Plugin 'plasticboy/vim-markdown'
Plugin 'jszakmeister/markdown2ctags'
Plugin 'joker1007/vim-markdown-quote-syntax'
Plugin 'Valloric/YouCompleteMe'
" Plugin 'Shougo/neocomplete.vim'
Plugin 'easymotion/vim-easymotion'
Plugin 'tpope/vim-surround'
Plugin 'Lokaltog/vim-powerline'
Plugin 'Yggdroot/LeaderF'
" Plugin 'brookhong/cscope.vim'
Plugin 'tomasr/molokai'
Plugin 'vim-syntastic/syntastic'
Plugin 'SirVer/ultisnips'
Plugin 'derekwyatt/vim-fswitch'
Plugin 'vim-scripts/AutoClose'
Plugin 'kien/rainbow_parentheses.vim'
Plugin 'chazy/cscope_maps'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'Xuyuanp/nerdtree-git-plugin'
Plugin 'bronson/vim-trailing-whitespace'
" Plugin 'vim-scripts/c.vim'
Plugin 'python-mode/python-mode'
Plugin 'Raimondi/delimitMate'
Plugin 'Chiel92/vim-autoformat'
Plugin 'scrooloose/nerdcommenter'
Plugin 'hashrocket/vim-macdown'

call vundle#end()  " required
filetype plugin indent on  " required
" End vundle


" tagbar配置
" 增加tagbar对markdown文件的支持
let g:tagbar_type_markdown = {
    \ 'ctagstype': 'markdown',
    \ 'ctagsbin' : '~/.vim/bundle/markdown2ctags/markdown2ctags.py',
    \ 'ctagsargs' : '-f - --sort=yes',
    \ 'kinds' : [
        \ 's:sections',
        \ 'i:images'
    \ ],
    \ 'sro' : '|',
    \ 'kind2scope' : {
        \ 's' : 'section',
    \ },
    \ 'sort': 0,
\ }
" 打开tagbar
nmap <F8> :TagbarToggle<CR>
let g:tagbar_autofocus = 0  " 打开tagbar时光标自动到tagbar窗口
let g:tagbar_autoclose = 1  " 跳转后直接关闭tagbar窗口
" 对指定后缀的文件，自动打开tagbar窗口
autocmd BufReadPost *.cpp,*.c,*.h,*.hpp,*.cc,*.cxx,*.md,*.py call tagbar#autoopen()


"" cscope配置
set cscopequickfix=c-,d-,e-,g-,i-,s-,t- " 显示在quickfix窗口，并且清空先前的显示结果
set cst  " cscopetag
set csto=0 " cscopeorder
set cspc=3 " 显示路径，显示路径的最后3个部分


" Leaderf配置
" let g:Lf_DefaultMode = 'FullPath'
let g:Lf_DefaultMode = 'Fuzzy'
let g:Lf_RootMarkers = ['.git']
" 当前工作目录为最近的.git所在目录，避免使用当前路径找不到其它目录中的文件
let g:Lf_WorkingDirectoryMode = 'a'  
" let g:Lf_ShortcutF = '<C-P>'

let g:Powerline_symbols = 'fancy'

set conceallevel=2
let g:vim_markdown_folding_disabled = 1


let g:markdown_quote_syntax_on_filetypes = ['text']

let g:rbpt_colorpairs = [
    \ ['brown',       'RoyalBlue3'],
    \ ['Darkblue',    'SeaGreen3'],
    \ ['darkgray',    'DarkOrchid3'],
    \ ['darkgreen',   'firebrick3'],
    \ ['darkcyan',    'RoyalBlue3'],
    \ ['darkred',     'SeaGreen3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['brown',       'firebrick3'],
    \ ['gray',        'RoyalBlue3'],
    \ ['darkmagenta', 'DarkOrchid3'],
    \ ['Darkblue',    'firebrick3'],
    \ ['darkgreen',   'RoyalBlue3'],
    \ ['darkcyan',    'SeaGreen3'],
    \ ['darkred',     'DarkOrchid3'],
    \ ['red',         'firebrick3'],
    \ ]

let g:rbpt_max = 16
let g:rbpt_loadcmd_toggle = 0
au VimEnter * RainbowParenthesesToggle
au Syntax * RainbowParenthesesLoadRound
au Syntax * RainbowParenthesesLoadSquare
au Syntax * RainbowParenthesesLoadBraces

syntax on
set colorcolumn=81
set t_Co=256
" colorscheme solarized " 设置背景方案
" colorscheme molokai " 设置背景方案
colorscheme ron " 设置背景方案
set background=dark " light\dark
let g:solarized_termcolors=256
let g:solarized_termtrans=1
let g:solarized_contrast="normal"
let g:solarized_visibility="high"
set guifontset=
set guifont=Source_Code_Pro:h11:cANSI


nmap <F10> :NERDTreeToggle<CR>
autocmd StdinReadPre * let s:std_in=1
" autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
" autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | endif
let NERDTreeShowLineNumbers=1
let NERDTreeAutoCenter=1
let NERDTreeShowHidden=1
let NERDTreeWinSize=31
" let g:nerdtree_tabs_open_on_console_startup=1
let NERDTreeIgnores=['\.pyc','\~$','\.swp']
let NERDTreeShowBookmarks=1


set tags=tags;
set autochdir
" map <C-F12> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q .<CR>


set report=0
set cmdheight=2
set cmdheight=2
set showcmd " 显示命令
set nocompatible
set cursorline " 高亮当前行
set paste " 设置粘贴模式，使粘贴不错位
set novisualbell " 设置不闪烁
set wrap " 自动换行
set autoindent " 继承前行的缩进方式
set smartindent " cindent使能时，不起作用
set cindent
set tabstop=4 " 制表符为4
set softtabstop=4 " 按backspace按键时可以删掉4个空格
set shiftwidth=4 " 设置<<或>>移动的宽度为4
set shiftround "
set expandtab
set smarttab " 为C程序提供自动缩进
set number
set history=1000
" set textwidth=120 " 设置每行120个字符自动换行
set textwidth=80 " 设置每行120个字符自动换行
set autochdir " 自动切换当前目录为当前文件所在目录
" Search and Case
set hlsearch " 高亮
set incsearch
set ignorecase " 忽略大小写
set whichwrap+=<,>,h,l " 光标滑动到行的首尾时，左右滑动可以移动到上下行
set showmatch " 高亮显示匹配的括号
set matchtime=1  " 匹配括号高亮的时间（单位：十分之一秒）
set iskeyword+=_,$,@,%,#,-  " 带有这些符号的单词不要被换行分割
" 补全
set wildmenu
set wildmode=longest,full
set completeopt=menu,menuone,longest
" set completeopt=preview,menu " 代码补全
set switchbuf=useopen,usetab
set shortmess=a
" Rule
set noshowmode
set ruler " 显示光标所在的行、列坐标
set winaltkeys=no " Window中alt键来选择编辑器的菜单

filetype on
filetype plugin on
filetype indent on

au BufRead,BufNewFile SConstruct set filetype=python

set autoread " 设置当文件被改动时自动载入
set autowrite " 自动保存
set confirm  " 在处理未保存或只读的文件时，弹出确认

" No backup files
set nobackup
set nowritebackup
set noswapfile

" 折叠
" set foldenable " zi命令打开折叠
" set foldmethod=syntax
" 使用空格来打开关闭折叠
nnoremap zc @=((foldclosed(line('.')) < 0) ? 'zc' : 'zo')<CR>

" 自动括号
" inoremap ( ()<ESC>i
" inoremap { {}<ESC>i
" nnoremap <leader>h <C-w>h
" nnoremap <leader>j <C-w>j
" nnoremap <leader>k <C-w>k
" nnoremap <leader>l <C-w>l
" inoremap <silent> <C-h> <Left>
" inoremap <silent> <C-j> <Down>
" inoremap <silent> <C-k> <Up>
" inoremap <silent> <C-l> <Right>


" 设置文件头
autocmd BufNewFile *.cpp,*.cc,*.[ch],*.py,*.sh exec ":call SetTitle()"
func SetTitle()
	"如果文件类型为.sh文件
	if &filetype == 'sh'
		call setline(1,"\#!/bin/bash")
		call append(line("."), "")
    elseif &filetype == 'python'
        call setline(1,"#!/usr/bin/env python")
        call append(line("."),"# coding=utf-8")
	    call append(line(".")+1, "")
	    call append(line(".")+2, "")
	    call append(line(".")+3, "def main():")
	    call append(line(".")+4, "  print 'hello, world'")
	    call append(line(".")+5, "")
	    call append(line(".")+6, "")
	    call append(line(".")+7, "if __name__ == '__main__':")
	    call append(line(".")+8, "  main()")
	else
		call setline(1, "/*************************************************************************")
		call append(line("."), "	> File Name: ".expand("%"))
		call append(line(".")+1, "	> Author: wuxiangwei")
		call append(line(".")+2, "	> Mail: wuxiangwei@corp.netease.com")
		call append(line(".")+3, "	> Created Time: ".strftime("%c"))
		call append(line(".")+4, " ************************************************************************/")
		call append(line(".")+5, "")
	endif
	if expand("%:e") == 'cpp'
		call append(line(".")+6, "#include<iostream>")
		call append(line(".")+7, "using namespace std;")
		call append(line(".")+8, "")
	endif
	if &filetype == 'c'
		call append(line(".")+6, "#include<stdio.h>")
		call append(line(".")+7, "")
	endif
	if expand("%:e") == 'h'
		call append(line(".")+6, "#ifndef _".toupper(expand("%:r"))."_H")
		call append(line(".")+7, "#define _".toupper(expand("%:r"))."_H")
		call append(line(".")+8, "#endif")
	endif
endfunc
autocmd BufNewFile * normal G

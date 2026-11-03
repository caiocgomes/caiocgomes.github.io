# What Can We Learn from a Coin Toss?
## O que se aprende com uma cara

Caio Gomes · Como pensar em aprendizado de máquina / How to Think About Machine Learning

Livro aberto para leitura em português brasileiro e inglês. Os sete capítulos da primeira parte estão completos nas duas edições. A Parte II, sobre regressão, aparece no sumário como planejada. A pasta **docs** já contém o site pronto para publicar, com HTML, equações MathML, figuras vetoriais, índices de busca, PDFs e os fontes LaTeX de cada edição.

## Publicar no GitHub Pages

1. Crie um repositório público para o livro. Uma sugestão de nome é **learning-from-a-coin-toss**. Um repositório dedicado mantém o livro ao lado de uma página pessoal que já exista.
2. Extraia o ZIP e envie **o conteúdo** para a raiz da branch **main**. Ao abrir a raiz do repositório, você deve ver **docs/**, **content/**, **tools/** e este README. O arquivo **docs/.nojekyll** faz parte do pacote.
3. Abra **Settings → Pages → Build and deployment**. Em **Source**, selecione **Deploy from a branch**. Selecione **main** e **/docs** e clique em **Save**.
4. Depois do deploy, use **Visit site** na mesma tela. Os links relativos funcionam tanto na raiz de um domínio quanto no caminho de projeto que o GitHub atribui ao repositório.

A página inicial oferece os dois idiomas. A busca é local, e o controle PT-BR / EN leva ao capítulo correspondente. As definições de termos de reutilização do texto e do código ficam a cargo do autor.

[Documentação do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Ler e testar no computador

Na raiz do pacote, rode o comando abaixo e abra <http://localhost:8000/>. O servidor também permite testar a busca, que carrega o índice de cada idioma por HTTP.

    python3 -m http.server 8000 --directory docs

## Atualizar as edições

Edite os capítulos em **content/pt-br/** e **content/en/**. Cada arquivo numerado tem o texto integral do capítulo e a mesma posição nos dois idiomas. Os preâmbulos tipográficos estão em **content/preamble-pt-br.tex** e **content/preamble-en.tex**. Os arquivos em **docs/** são a saída já construída. O CSS e o JavaScript do leitor vivem diretamente em **docs/assets/**.

Para reconstruir, use Python 3.12+, Pandoc 3, TeX Live com latexmk, TikZ, standalone e fontes Palatino (mathpazo), e Poppler com pdftocairo. Os scripts Python usam a biblioteca padrão.

    python3 tools/print_editions.py
    python3 tools/build.py

O primeiro comando gera os dois PDFs, os fontes completos em LaTeX e as figuras. O segundo gera a capa bilíngue, as duas páginas de apresentação, as páginas dos capítulos e os índices de busca. Suba as mudanças nos fontes e em **docs/** para atualizar o site.

Para acrescentar um capítulo, crie o mesmo número nas duas pastas de idioma, ajuste em **tools/layout.py** a descrição e a divisão das partes no sumário, e reconstrua. As capas, legendas acessíveis e textos de navegação estão em **tools/gateway.py**, **tools/layout.py** e **tools/build.py**.

## English

This repository contains the seven completed chapters in Brazilian Portuguese and English. It includes both PDFs and the editable LaTeX sources. To publish the prebuilt reader, upload the contents to a repository and select **Settings → Pages → Deploy from a branch → main → /docs**. To work on the book locally, edit the numbered chapters under **content/** and run the two build commands above.

The chapter navigation, search and organization into parts take inspiration from Matheus Facure’s [Causal Inference for the Brave and True](https://matheusfacure.github.io/python-causality-handbook/landing-page.html).

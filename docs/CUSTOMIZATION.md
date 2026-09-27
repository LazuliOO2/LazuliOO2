# Personalização e publicação

O perfil está pronto para o repositório público **LazuliOO2/LazuliOO2**. Copie `README.md` e a pasta `assets` para a raiz desse repositório. Mantenha `scripts` e `docs` se quiser editar e atualizar os painéis depois. A publicação não foi feita automaticamente.

## Editar conteúdo

1. Abra `assets/profile.json`.
2. Edite os contatos, a stack e os quatro projetos.
3. Execute `python scripts/build.py` na raiz do projeto, com Python 3.
4. Publique o README e os SVGs gerados juntos.

Cada projeto tem quatro campos explícitos. Por exemplo:

```json
"REPO_BACKEND_URL": "https://github.com/LazuliOO2/Back-End",
"REPO_BACKEND_NAME": "Back-End",
"REPO_BACKEND_DESCRIPTION": "Descrição do projeto.",
"REPO_BACKEND_STACK": "JavaScript • PHP • TypeScript • SQL"
```

Os outros prefixos são `REPO_FRONTEND`, `REPO_FULLSTACK` e `REPO_WORKBENCH`. Foram incluídos somente os quatro repositórios solicitados. `Full-Stack-` tem um hífen final e `workbench` é a grafia real do repositório.

Os campos de descrição são quebrados em linhas automaticamente. Mantenha nomes curtos, descrições com até cerca de 105 caracteres e stack com até 40 caracteres para preservar o espaço dos cards. Se aumentar esses limites, revise o SVG mobile e ajuste a altura em `scripts/build.py`.

Os contatos estão em `GITHUB_URL`, `LINKEDIN_URL`, `EMAIL_URL` e `PORTFOLIO_URL`. O LinkedIn veio do portfólio público; o e-mail foi informado pelo proprietário. As tecnologias foram extraídas dos READMEs públicos e do perfil existente; a listagem não atribui nível de domínio.

A apresentação, missão, localização e textos do terminal podem ser editados em `scripts/build.py`. Alterações diretas nos SVGs ou no README serão substituídas na próxima geração.

## Atualizar telemetria

```powershell
python scripts/update_telemetry.py
python scripts/build.py
```

O primeiro comando consulta a API pública e o calendário de contribuições do GitHub e salva `assets/telemetry.json`. O segundo gera os painéis locais. Ambos usam apenas a biblioteca padrão do Python. Nenhum script roda no navegador ou no README.

Os dados são um **snapshot datado**, não uma conexão em tempo real. O atualizador preserva o arquivo anterior se uma requisição falhar ou o formato do calendário mudar. A API pública pode limitar requisições; opcionalmente, o script aceita `GITHUB_TOKEN` pelo ambiente. Nunca coloque tokens nos arquivos do perfil.

O gráfico usa os últimos 31 dias do calendário público. A sequência atual permite hoje ainda vazio; a maior sequência considera apenas a janela coletada, não toda a história da conta. O calendário pode refletir contribuições privadas anonimizadas conforme a configuração pública do GitHub. Linguagens usam bytes dos repositórios públicos próprios, sem forks; incluem Jupyter Notebook e não são um ranking de habilidades.

## Compatibilidade e decisões visuais

- O GitHub sanitiza HTML. O README não usa `<style>`, JavaScript, CSS externo, React, Tailwind ou `iframe`.
- O fundo geral pertence ao tema do GitHub; o preto, o grid e as bordas são desenhados dentro dos SVGs, preservando a identidade em temas claro e escuro.
- `<picture>` seleciona uma composição própria de 420 px para telas de até 600 px. O SVG desktop usa 900 px; ambos escalam para a largura disponível.
- Os projetos usam uma coluna para manter a legibilidade em celular. Contatos são imagens pequenas em linha, com quebra natural quando falta espaço.
- Os links envolvem as imagens no HTML do README. Links internos de SVG carregado como imagem não servem como navegação do card.
- Fontes são locais, com alternativas padrão. Os SVGs não carregam fontes, imagens ou scripts externos.
- Indicadores e cursor são estáticos: a documentação do GitHub não garante animações SVG. A estética de terminal não depende de movimento.
- Os SVGs têm títulos e as imagens têm textos alternativos. Stack e apresentação também estão disponíveis em texto selecionável.
- Os botões são SVGs locais para evitar dependência desnecessária de shields.io. As tecnologias ficam agrupadas dentro dos módulos.
- A instância pública consultada do Activity Graph respondeu `DEPLOYMENT_DISABLED`; o projeto original GitHub Readme Stats informa que não é mais mantido. Por isso, estatísticas, linguagens, streak e atividade usam painéis locais com dados reais, no mesmo tema.

Referências consultadas:

- [GitHub: imagens, caminhos relativos e picture](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [GitHub: formatos de imagem e limitações de SVG](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)
- [GitHub Readme Stats: manutenção e disponibilidade](https://github.com/anuraghazra/github-readme-stats)
- [GitHub Activity Graph](https://github.com/ashutosh00710/github-readme-activity-graph)

## Arquivos

```text
README.md                    Perfil publicável
assets/profile.json          Projetos, contatos e stack
assets/telemetry.json        Snapshot dos dados públicos
assets/*.svg                 Painéis desktop, mobile e botões
scripts/build.py             Geração local do README e dos painéis
scripts/update_telemetry.py   Atualização dos dados públicos
docs/CUSTOMIZATION.md        Este guia
```

## Revisão realizada

Os quatro links de repositórios, o perfil e o portfólio responderam HTTP 200. O LinkedIn respondeu HTTP 999, bloqueando a verificação automatizada; foi mantido o endereço publicado no portfólio. O e-mail foi confirmado pelo proprietário, sem envio de mensagem.

O README foi processado pela API `/markdown` do próprio GitHub: foram preservados os 13 elementos `picture` e seus 13 `source`. Todos os 30 SVGs foram validados como XML, com checagem dos limites dos textos e das referências de imagens. As composições desktop e mobile foram renderizadas e inspecionadas; não houve teste manual em um perfil já publicado.

`docs/previews/desktop.png` e `docs/previews/mobile.png` mostram os painéis em sequência, incluindo os botões. São pranchas visuais; a navegação, apresentação em Markdown e detalhes expansíveis são exibidos no README real.

Para repetir a revisão visual no Windows, instale `Pillow` e `resvg-py` e execute `python scripts/review.py`. Essas dependências são opcionais e não participam da geração nem da publicação do perfil.

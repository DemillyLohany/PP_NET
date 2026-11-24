const formulario = document.querySelector('.pesquisa-menu');
const campo = document.getElementById('pesquisa-menu');
const painel = document.getElementById('resultados-menu');
let vez = 0;

formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  const atual = ++vez;
  const termo = campo.value.trim();
  painel.replaceChildren();
  painel.hidden = !termo;
  if (!termo) return;
  const aviso = document.createElement('p');
  aviso.setAttribute('role', 'status');
  aviso.textContent = 'Pesquisando…';
  painel.append(aviso);

  try {
    const endereco = new URL(formulario.action);
    endereco.searchParams.set('q', termo);
    const resposta = await fetch(endereco);
    if (!resposta.ok) throw new Error();
    const dados = await resposta.json();
    if (atual !== vez) return;
    aviso.textContent = dados.total ? `${dados.total} resultado(s)` : 'Nenhum resultado encontrado.';
    if (dados.total > dados.resultados.length) aviso.textContent += ' — mostrando os primeiros 50';
    for (const [tipo, titulo, link] of dados.resultados) {
      const item = document.createElement('a');
      item.href = link;
      item.textContent = `${titulo} — ${tipo}`;
      painel.append(item);
    }
  } catch {
    if (atual === vez) aviso.textContent = 'Não foi possível pesquisar. Tente novamente.';
  }
});

function fecharPesquisa() {
  vez++;
  painel.hidden = true;
}

campo.addEventListener('input', fecharPesquisa);
formulario.addEventListener('keydown', (evento) => {
  if (evento.key === 'Escape') {
    fecharPesquisa();
    campo.focus();
  }
});
document.addEventListener('click', (evento) => {
  if (!formulario.contains(evento.target)) fecharPesquisa();
});

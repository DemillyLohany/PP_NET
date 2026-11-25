document.addEventListener('DOMContentLoaded', function() {
    const abrir_janela = document.getElementById('abrir-janela');
    const fechar_janela = document.getElementById('fechar-janela');
    const janela_flutuante = document.getElementById('janela-flutuante');

    if (!abrir_janela || !fechar_janela || !janela_flutuante) return;

    abrir_janela.onclick = function() {
        janela_flutuante.style.display = 'flex'; //Agora a janela não se esconde mais
    };

    fechar_janela.onclick = function() {
        janela_flutuante.style.display = 'none';//Agora a janela volta a se esconder
    };
});
document.querySelectorAll('[data-editar]').forEach(function (botao) {
    botao.addEventListener('click', function () {
        const cartao = botao.closest('.card-disciplina');
        const formulario = document.getElementById(botao.dataset.editar);
        const dados = cartao.querySelector('[data-dados-disciplina]');
        formulario.hidden = !formulario.hidden;
        dados.hidden = !formulario.hidden;
        const editar = cartao.querySelector('button[aria-expanded]');
        editar.setAttribute('aria-expanded', String(!formulario.hidden));
        if (formulario.hidden) {
            formulario.reset();
            editar.focus();
        } else {
            formulario.querySelector("input")?.focus();
        }
    });
});

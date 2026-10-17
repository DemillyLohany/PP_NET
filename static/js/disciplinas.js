const abrir_janela = document.getElementById('abrir-janela');
const fechar_janela = document.getElementById('fechar-janela');
const janela_flutuante = document.getElementById('janela-flutuante');

abrir_janela.onclick = function() {
    janela_flutuante.style.display = 'flex'; //Agora a janela não se esconde mais
};

fechar_janela.onclick = function() {
    janela_flutuante.style.display = 'none';//Agora a janela volta a se esconder
};
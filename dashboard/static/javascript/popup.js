JS:

// MODAL COMPRA
document.getElementById('openModalBtnCompra').addEventListener('click', function() {
    document.getElementById('modalCompra').style.display = 'block';
});

document.getElementById('closeModalBtnCompra').addEventListener('click', function() {
    document.getElementById('modalCompra').style.display = 'none';
});

// Fecha o modal quando o usuário clica fora do conteúdo do modal
window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('modalCompra')) {
        document.getElementById('modalCompra').style.display = 'none';
    }
});


// MODAL VENDA
document.getElementById('openModalBtnVenda').addEventListener('click', function() {
    document.getElementById('modalVenda').style.display = 'block';
});

document.getElementById('closeModalBtnVenda').addEventListener('click', function() {
    document.getElementById('modalVenda').style.display = 'none';
});

// Fecha o modal quando o usuário clica fora do conteúdo do modal
window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('modalVenda')) {
        document.getElementById('modalVenda').style.display = 'none';
    }
});
// main.js — students will add JavaScript here as features are built

(function () {
    var trigger = document.getElementById('see-how-it-works');
    var overlay = document.getElementById('demo-modal-overlay');
    var closeBtn = document.getElementById('demo-modal-close');
    var iframe = document.getElementById('demo-modal-iframe');

    if (!trigger || !overlay || !closeBtn || !iframe) return;

    function openModal(event) {
        event.preventDefault();
        iframe.src = iframe.dataset.src + '?autoplay=1';
        overlay.hidden = false;
    }

    function closeModal() {
        overlay.hidden = true;
        iframe.src = '';
    }

    trigger.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);

    overlay.addEventListener('click', function (event) {
        if (event.target === overlay) closeModal();
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !overlay.hidden) closeModal();
    });
})();

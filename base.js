(() => {
  document.addEventListener('click', (event) => {
    const episode = event.target.closest('[data-episode], .episode, .episode_item, .anthology_item');
    if (episode && episode.parentElement) {
      episode.parentElement.querySelectorAll('.active, .current, .selected').forEach((item) => {
        if (item !== episode) item.classList.remove('active', 'current', 'selected');
      });
      episode.classList.add('active');
    }

    const modalClose = event.target.closest('[data-close], .close, .icon-close, .iconclose');
    if (modalClose) {
      const modal = modalClose.closest('.modal, .dialog, .popup, .loginnew_login_mask, [role="dialog"]');
      if (modal) modal.style.display = 'none';
    }

    const pageItem = event.target.closest('.pagination a, .pagination button, [data-page]');
    if (pageItem) {
      pageItem.parentElement?.querySelectorAll('.active, .current, .selected').forEach((item) => {
        if (item !== pageItem) item.classList.remove('active', 'current', 'selected');
      });
      pageItem.classList.add('active');
    }
  });

  document.querySelectorAll('.video-player-container').forEach((player) => {
    player.setAttribute('aria-label', `Youku video player ${player.dataset.vid || ''}`.trim());
  });
})();

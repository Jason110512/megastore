// =============================================
//  MEGA STORE — Global JavaScript
// =============================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss alerts ──────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 4000);
  });

  // ── Active sidebar link ───────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ── Confirm delete forms ──────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ── Image preview on file input ───────────
  document.querySelectorAll('input[type="file"][data-preview]').forEach(function (input) {
    input.addEventListener('change', function () {
      const targetId = this.dataset.preview;
      const target = document.getElementById(targetId);
      if (!target || !this.files[0]) return;
      const reader = new FileReader();
      reader.onload = function (e) { target.src = e.target.result; };
      reader.readAsDataURL(this.files[0]);
    });
  });

  // ── Cart AJAX update ──────────────────────
  function updateCartBadge(count) {
    const badge = document.querySelector('.badge-cart');
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    } else if (count > 0) {
      const cartIcon = document.querySelector('a[href*="envio"] i.fa-shopping-cart');
      if (cartIcon) {
        const span = document.createElement('span');
        span.className = 'badge-cart';
        span.textContent = count;
        cartIcon.parentElement.appendChild(span);
      }
    }
  }

  // ── Qty buttons AJAX ─────────────────────
  document.querySelectorAll('.qty-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.getAttribute('href');
      fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin',
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            updateCartBadge(data.total_items);
            // Actualizar número en botón
            const card = this.closest('.product-card, .qty-control-wrap');
            if (card) {
              const num = card.querySelector('.qty-num');
              if (num) {
                let current = parseInt(num.textContent) || 0;
                if (url.includes('agregar')) current++;
                else current = Math.max(0, current - 1);
                num.textContent = current;
              }
            }
          }
        })
        .catch(() => { window.location.href = url; });
    });
  });

  // ── Tooltips Bootstrap ────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ── Mobile sidebar toggle ─────────────────
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('open');
    });
  }

  // ── Close modal on outside click ──────────
  const deleteModal = document.getElementById('deleteModal');
  if (deleteModal) {
    deleteModal.addEventListener('click', function (e) {
      if (e.target === this) closeModal();
    });
  }

});

// Expose globally for inline onclick handlers
function showDeleteModal(id, nombre, baseUrl) {
  const modal = document.getElementById('deleteModal');
  const msg = document.getElementById('modalMsg');
  const form = document.getElementById('deleteForm');
  if (!modal) return;
  msg.textContent = `¿Estás seguro que deseas eliminar el producto "${nombre}"?`;
  form.action = baseUrl.replace('0', id);
  modal.style.display = 'flex';
}

function closeModal() {
  const modal = document.getElementById('deleteModal');
  if (modal) modal.style.display = 'none';
}

// ═══════════════════════════════════════════════════════════════
//  Antigravity Skills Portal — Application Logic
//  Version: Elite 2026
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  const app = new SkillsPortal();
  app.init();
});

class SkillsPortal {
  constructor() {
    this.currentFilter = 'all';
    this.searchQuery = '';
    this.elements = {};
  }

  init() {
    this.cacheElements();
    this.renderStats();
    this.renderFilters();
    this.renderSkills();
    this.bindEvents();
    this.animateProgressBar();
    this.initMouseGlow();
  }

  cacheElements() {
    this.elements = {
      statsRow: document.getElementById('stats-row'),
      filterRow: document.getElementById('filter-row'),
      searchInput: document.getElementById('search-input'),
      skillsContainer: document.getElementById('skills-container'),
      modalOverlay: document.getElementById('modal-overlay'),
      modalTitle: document.getElementById('modal-title'),
      modalTitleVi: document.getElementById('modal-title-vi'),
      modalBody: document.getElementById('modal-body'),
      modalClose: document.getElementById('modal-close'),
      progressFill: document.getElementById('progress-fill'),
      progressPercent: document.getElementById('progress-percent'),
      totalCount: document.getElementById('total-count'),
      eliteCount: document.getElementById('elite-count'),
      pendingCount: document.getElementById('pending-count'),
      categoryCount: document.getElementById('category-count'),
    };
  }

  // ─── Statistics ──────────────────────────────────────────
  getStats() {
    const total = SKILLS_DATA.length;
    const elite = SKILLS_DATA.filter(s => s.status === 'elite').length;
    const pending = total - elite;
    const percent = Math.round((elite / total) * 100);
    const categories = SKILL_CATEGORIES.length;
    return { total, elite, pending, percent, categories };
  }

  renderStats() {
    const { total, elite, pending, categories } = this.getStats();
    this.elements.totalCount.textContent = total;
    this.elements.eliteCount.textContent = elite;
    this.elements.pendingCount.textContent = pending;
    this.elements.categoryCount.textContent = categories;
  }

  animateProgressBar() {
    const { percent } = this.getStats();
    requestAnimationFrame(() => {
      setTimeout(() => {
        this.elements.progressFill.style.width = `${percent}%`;
        this.elements.progressPercent.textContent = `${percent}%`;
      }, 300);
    });
  }

  // ─── Filters ─────────────────────────────────────────────
  renderFilters() {
    const container = this.elements.filterRow;
    // All button
    const allBtn = this.createFilterBtn('all', '🌐 All');
    allBtn.classList.add('active');
    container.appendChild(allBtn);
    // Status filters
    container.appendChild(this.createFilterBtn('elite', '✅ Elite'));
    container.appendChild(this.createFilterBtn('pending', '⏳ Pending'));
    // Separator
    const sep = document.createElement('div');
    sep.style.cssText = 'width:1px;height:24px;background:rgba(255,255,255,0.08);margin:0 4px;flex-shrink:0;';
    container.appendChild(sep);
    // Category filters
    SKILL_CATEGORIES.forEach(cat => {
      container.appendChild(this.createFilterBtn(cat.id, `${cat.icon} ${cat.name}`));
    });
  }

  createFilterBtn(id, label) {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.dataset.filter = id;
    btn.textContent = label;
    return btn;
  }

  // ─── Skills Rendering ────────────────────────────────────
  renderSkills() {
    const container = this.elements.skillsContainer;
    container.innerHTML = '';
    const filtered = this.getFilteredSkills();

    if (filtered.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state__icon">🔍</div>
          <div class="empty-state__text">Không tìm thấy kỹ năng nào</div>
          <div class="empty-state__hint">Thử tìm kiếm với từ khóa khác hoặc bỏ bộ lọc</div>
        </div>`;
      return;
    }

    // Group by category
    if (this.currentFilter === 'all' || this.currentFilter === 'elite' || this.currentFilter === 'pending') {
      const grouped = this.groupByCategory(filtered);
      Object.entries(grouped).forEach(([catId, skills]) => {
        const cat = SKILL_CATEGORIES.find(c => c.id === catId);
        if (!cat || skills.length === 0) return;
        const section = this.createCategorySection(cat, skills);
        container.appendChild(section);
      });
    } else {
      // Single category — no header needed, grid directly
      const grid = document.createElement('div');
      grid.className = 'skills-grid';
      filtered.forEach(skill => grid.appendChild(this.createSkillCard(skill)));
      container.appendChild(grid);
    }
  }

  getFilteredSkills() {
    let skills = [...SKILLS_DATA];

    // Status filter
    if (this.currentFilter === 'elite') {
      skills = skills.filter(s => s.status === 'elite');
    } else if (this.currentFilter === 'pending') {
      skills = skills.filter(s => s.status === 'pending');
    } else if (this.currentFilter !== 'all') {
      // Category filter
      skills = skills.filter(s => s.category === this.currentFilter);
    }

    // Search
    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      skills = skills.filter(s =>
        s.name.toLowerCase().includes(q) ||
        s.nameVi.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q) ||
        s.pillars.toLowerCase().includes(q)
      );
    }

    return skills;
  }

  groupByCategory(skills) {
    const groups = {};
    SKILL_CATEGORIES.forEach(c => groups[c.id] = []);
    skills.forEach(s => {
      if (groups[s.category]) groups[s.category].push(s);
    });
    return groups;
  }

  createCategorySection(cat, skills) {
    const section = document.createElement('div');
    section.className = 'category-section';
    section.innerHTML = `
      <div class="category-header">
        <span class="category-header__icon">${cat.icon}</span>
        <span class="category-header__name">${cat.name}</span>
        <span class="category-header__count">${skills.length} skill${skills.length > 1 ? 's' : ''}</span>
      </div>`;
    const grid = document.createElement('div');
    grid.className = 'skills-grid';
    skills.forEach(skill => grid.appendChild(this.createSkillCard(skill)));
    section.appendChild(grid);
    return section;
  }

  createSkillCard(skill) {
    const card = document.createElement('div');
    card.className = 'skill-card';
    card.dataset.category = skill.category;
    card.dataset.folder = skill.folder;

    const badgeClass = skill.status === 'elite' ? 'skill-card__badge--elite' : 'skill-card__badge--pending';
    const badgeText = skill.status === 'elite' ? '✅ ELITE' : '⏳ PENDING';

    const pillarsHTML = skill.pillars.split(', ').map(p =>
      `<span class="skill-card__pillar">${p}</span>`
    ).join('');

    const metaHTML = skill.status === 'elite'
      ? `<span class="skill-card__meta-item">📦 v${skill.version}</span>
         <span class="skill-card__meta-item">📅 ${skill.date}</span>`
      : `<span class="skill-card__meta-item">🔧 Chưa nâng cấp Elite</span>`;

    card.innerHTML = `
      <div class="skill-card__top">
        <div>
          <div class="skill-card__name">${skill.name}</div>
          <div class="skill-card__name-vi">${skill.nameVi}</div>
        </div>
        <span class="skill-card__badge ${badgeClass}">${badgeText}</span>
      </div>
      <div class="skill-card__desc">${skill.description}</div>
      <div class="skill-card__pillars">${pillarsHTML}</div>
      <div class="skill-card__meta">${metaHTML}</div>`;

    card.addEventListener('click', () => this.openSkillModal(skill));
    return card;
  }

  // ─── Modal & Markdown ────────────────────────────────────
  async openSkillModal(skill) {
    const overlay = this.elements.modalOverlay;
    this.elements.modalTitle.textContent = skill.name;
    this.elements.modalTitleVi.textContent = skill.nameVi;
    this.elements.modalBody.innerHTML = `
      <div class="modal__loading">
        <div class="spinner"></div>
        <div>Đang tải SKILL.md...</div>
      </div>`;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';

    try {
      // Try fetching SKILL.md from the skill folder
      const mdPath = `../${skill.folder}/SKILL.md`;
      const response = await fetch(mdPath);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const markdown = await response.text();
      this.elements.modalBody.innerHTML = `<div class="md-content">${this.renderMarkdown(markdown)}</div>`;
    } catch (err) {
      // Fallback: render skill info card
      this.elements.modalBody.innerHTML = `
        <div class="md-content">
          <h1>${skill.name}</h1>
          <p><strong>Tên tiếng Việt:</strong> ${skill.nameVi}</p>
          <p>${skill.description}</p>
          <h3>Key Pillars</h3>
          <ul>${skill.pillars.split(', ').map(p => `<li>${p}</li>`).join('')}</ul>
          ${skill.status === 'elite'
            ? `<p><strong>Status:</strong> ✅ Elite Certified | Version ${skill.version} | ${skill.date}</p>`
            : `<p><strong>Status:</strong> ⏳ Pending Elite Upgrade</p>`}
          <hr>
          <p style="color: var(--text-muted); font-size: 0.82rem;">
            📁 Folder: <code>${skill.folder}</code><br>
            ℹ️ Không thể tải file SKILL.md trực tiếp. Hãy chạy server local: <code>npx serve</code> từ thư mục <code>Skills/</code>.
          </p>
        </div>`;
    }
  }

  closeModal() {
    this.elements.modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  // ─── Lightweight Markdown to HTML ────────────────────────
  renderMarkdown(md) {
    let html = md;

    // Remove frontmatter (---...---)
    html = html.replace(/^---[\s\S]*?---\n*/m, '');

    // Escape HTML (basic)
    html = html.replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Fenced code blocks ```lang ... ```
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Callout blocks > [!TYPE]
    html = html.replace(/&gt; \[!(TIP|IMPORTANT|WARNING|CAUTION)\]\n&gt; (.*?)(?=\n(?!&gt;)|\n*$)/gs, (_, type, content) => {
      const t = type.toLowerCase();
      const body = content.replace(/\n&gt; /g, '<br>');
      return `<div class="md-callout md-callout--${t}"><div class="md-callout__title">${type}</div><p>${body}</p></div>`;
    });

    // Blockquotes (remaining)
    html = html.replace(/^&gt; (.*$)/gm, '<blockquote><p>$1</p></blockquote>');
    // Merge consecutive blockquotes
    html = html.replace(/<\/blockquote>\n<blockquote>/g, '\n');

    // Tables
    html = html.replace(/((?:\|.*\|(?:\n|$))+)/g, (match) => {
      const rows = match.trim().split('\n').filter(r => r.trim());
      if (rows.length < 2) return match;

      // Check if row 2 is a separator
      const isSep = /^\|[\s:-]+\|/.test(rows[1]);
      if (!isSep) return match;

      const headerCells = rows[0].split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
      const bodyRows = rows.slice(2).map(row => {
        const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
        return `<tr>${cells}</tr>`;
      }).join('');

      return `<table><thead><tr>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table>`;
    });

    // Headings
    html = html.replace(/^##### (.*$)/gm, '<h5>$1</h5>');
    html = html.replace(/^#### (.*$)/gm, '<h4>$1</h4>');
    html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gm, '<h1>$1</h1>');

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');

    // Bold and italic
    html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Links [text](url) — handle escaped angles
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Unordered lists
    html = html.replace(/((?:^- .*$\n?)+)/gm, (match) => {
      const items = match.trim().split('\n').map(l => `<li>${l.replace(/^- /, '')}</li>`).join('');
      return `<ul>${items}</ul>`;
    });

    // Ordered lists
    html = html.replace(/((?:^\d+\. .*$\n?)+)/gm, (match) => {
      const items = match.trim().split('\n').map(l => `<li>${l.replace(/^\d+\. /, '')}</li>`).join('');
      return `<ol>${items}</ol>`;
    });

    // Paragraphs — wrap remaining text lines
    html = html.split('\n\n').map(block => {
      block = block.trim();
      if (!block) return '';
      if (block.startsWith('<')) return block; // Already HTML
      return `<p>${block.replace(/\n/g, '<br>')}</p>`;
    }).join('\n');

    return html;
  }

  // ─── Events ──────────────────────────────────────────────
  bindEvents() {
    // Search
    this.elements.searchInput.addEventListener('input', (e) => {
      this.searchQuery = e.target.value.trim();
      this.renderSkills();
    });

    // Filters
    this.elements.filterRow.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      this.elements.filterRow.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      this.currentFilter = btn.dataset.filter;
      this.renderSkills();
    });

    // Modal close
    this.elements.modalClose.addEventListener('click', () => this.closeModal());
    this.elements.modalOverlay.addEventListener('click', (e) => {
      if (e.target === this.elements.modalOverlay) this.closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.closeModal();
    });
  }

  // ─── Mouse Glow Effect ───────────────────────────────────
  initMouseGlow() {
    document.addEventListener('mousemove', (e) => {
      const cards = document.querySelectorAll('.skill-card');
      cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  }
}

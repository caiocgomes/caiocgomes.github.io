(() => {
  'use strict';
  const language = document.documentElement.dataset.edition;
  const pt = language === 'pt-br';
  const menu = document.querySelector('.book-menu');
  if (menu) {
    const query = window.matchMedia('(max-width: 820px)');
    const syncMenu = () => { menu.open = !query.matches; };
    syncMenu();
    query.addEventListener?.('change', syncMenu);
  }
  const dialog = document.querySelector('.search-dialog');
  const opener = document.querySelector('[data-search-open]');
  if (!dialog || !opener || typeof dialog.showModal !== 'function') return;
  opener.hidden = false;
  const input = dialog.querySelector('input');
  const status = dialog.querySelector('.search-status');
  const results = dialog.querySelector('.search-results');
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const initial = Array.from(document.querySelectorAll('[data-chapter-title]'), item => ({
    label: item.dataset.pageLabel, title: item.dataset.chapterTitle, url: item.getAttribute('href'), text: ''
  }));
  let records = initial;
  let loading;
  let fallback = false;
  const text = (tag, cls, value) => {
    const el = document.createElement(tag);
    el.className = cls;
    el.textContent = value;
    return el;
  };
  function render() {
    const term = normalize(input.value.trim());
    results.replaceChildren();
    if (!term) {
      status.textContent = pt ? 'Busque um conceito, um exemplo ou um capítulo.' : 'Find a concept, an example, or a chapter.';
      return;
    }
    const matches = records.map(row => ({
      row, index: normalize(row.text || '').indexOf(term), heading: normalize(row.title).includes(term)
    })).filter(hit => hit.heading || hit.index >= 0);
    matches.sort((a,b) => Number(b.heading) - Number(a.heading));
    status.textContent = matches.length ? (pt ? 'Resultados encontrados: ' : 'Matching results: ') + matches.length :
      (pt ? 'Nenhum resultado encontrado.' : 'No matching results.');
    if (fallback) status.textContent += pt ? ' Busca por título.' : ' Searching titles only.';
    for (const {row,index} of matches) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = row.url;
      a.append(text('small','',row.label),text('b','',row.title));
      if (index >= 0) {
        const original = row.text;
        const start = Math.max(0,index-65);
        a.append(text('span','excerpt',(start ? '…' : '')+original.slice(start,index+term.length+88)+(index+term.length+88<original.length?'…':'')));
      }
      li.append(a); results.append(li);
    }
  }
  async function loadIndex() {
    try {
      const response = await fetch('../assets/search-'+language+'.json');
      if (!response.ok) throw Error();
      const rows = await response.json();
      if (!Array.isArray(rows) || !rows.every(r => typeof r.title==='string' && typeof r.label==='string' && /^(?:introduction|(?:interlude-)?\d{2})\.html$/.test(r.url))) throw Error();
      records = rows;
    } catch (_) { fallback = true; }
    render();
  }
  function open() {
    if (dialog.open) return;
    input.value = ''; render();
    dialog.showModal(); input.focus();
    loading ??= loadIndex();
  }
  opener.addEventListener('click',open);
  dialog.querySelector('[data-search-close]').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{ if(e.target!==dialog)return; const r=dialog.getBoundingClientRect(); if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close(); });
  dialog.addEventListener('close',()=>opener.focus());
  input.addEventListener('input',render);
  input.addEventListener('keydown', e=>{ if(e.key==='ArrowDown'){const first=results.querySelector('a');if(first){e.preventDefault();first.focus();}} });
  document.addEventListener('keydown',e=>{ if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();open();} });
})();

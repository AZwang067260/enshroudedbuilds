/*! Enshrouded skill planner for enshroudedbuilds.org
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Tree data: rossicler/enshrouded-skill-tree (GPL-3.0-or-later), exported from the Enshrouded 1.0 game files.
 * Source: https://github.com/AZwang067260/enshroudedbuilds
 */
(function () {
  var D = window.EB_TREE; if (!D) return;
  var NS = 'http://www.w3.org/2000/svg';
  var $ = function (s) { return document.querySelector(s); };
  var T = D.types, N = {}, ORDER = [], ADJ = {}, sel = {}, focus = null, query = '', zoomTo = null;
  var FLAME = { THICK_SKIN: 'CONS', BARBARIAN: 'STR', EXALTED: 'INT', ARCANE_CONCENTRATION: 'SPIRIT', GRACEFUL_STRIDE: 'DEX', ENDURANCE_OF_THE_FLAME: 'ENDURANCE' };
  var B36 = '0123456789abcdefghijklmnopqrstuvwxyz';
  D.nodes.forEach(function (r) {
    N[r[0]] = { id: r[0], t: r[1], x: r[2], y: r[3], base: r.length > 4, ax: r[4], ay: r[5] };
    ORDER.push(r[0]); ADJ[r[0]] = [];
  });
  D.edges.forEach(function (e) { ADJ[e[0]].push(e[1]); ADJ[e[1]].push(e[0]); });

  var svg = $('#tree-svg'), view = $('#tree-view'), lv = $('#pl-level'), fl = $('#pl-flame'), pre = $('#pl-preset');
  var vt = { k: 1, x: 0, y: 0 };
  function el(tag, attrs, parent) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function type(id) { return T[N[id].t]; }
  function color(id) { return D.colors[type(id).a] || D.colors.Core; }
  function isAttr(id) { return N[id].t.indexOf('ATTR_') === 0; }
  function initials(name) { return name.replace(/[^A-Za-z ]/g, '').split(' ').filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join(''); }

  // ---------- drawing
  var gLinks = el('g', {}, view), gNodes = el('g', {}, view), linkEls = [], nodeEls = {};
  el('circle', { cx: 0, cy: 0, r: 198, class: 'tr-core' }, gLinks);
  ORDER.forEach(function (id) { var n = N[id]; if (n.base) linkEls.push([el('line', { x1: n.x, y1: n.y, x2: n.ax, y2: n.ay, class: 'tr-link' }, gLinks), id, null]); });
  D.edges.forEach(function (e) { var a = N[e[0]], b = N[e[1]]; linkEls.push([el('line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: 'tr-link' }, gLinks), e[0], e[1]]); });
  ORDER.forEach(function (id) {
    var n = N[id], t = type(id), big = t.c >= 4, r = isAttr(id) ? 7 : big ? 16 : 13;
    var g = el('g', { transform: 'translate(' + n.x + ' ' + n.y + ')', class: 'tr-node', 'data-node': id, tabindex: '-1' }, gNodes);
    g.style.setProperty('--c', color(id));
    el('circle', { r: r + 9, class: 'tr-hit' }, g);
    el('circle', { r: r, class: 'tr-dot' }, g);
    if (!isAttr(id)) { var tx = el('text', { class: 'tr-ini', 'text-anchor': 'middle', dy: '3.5' }, g); tx.textContent = initials(t.n); }
    var rk = null;
    if (t.m > 1) { rk = el('text', { class: 'tr-rank', 'text-anchor': 'middle', y: r + 12 }, g); }
    nodeEls[id] = { g: g, rank: rk };
  });
  // group labels at the outer edge of each archetype
  var groups = {};
  ORDER.forEach(function (id) { var t = type(id); if (!t.g || isAttr(id)) return; var k = t.g; groups[k] = groups[k] || { x: 0, y: 0, n: 0, a: t.a }; groups[k].x += N[id].x; groups[k].y += N[id].y; groups[k].n++; });
  Object.keys(groups).forEach(function (k) {
    var g = groups[k], cx = g.x / g.n, cy = g.y / g.n, d = Math.hypot(cx, cy) || 1, f = (d + 230) / d;
    var tx = el('text', { x: cx * f, y: cy * f, 'text-anchor': 'middle', class: 'tr-label' }, gLinks); tx.textContent = k.toUpperCase(); tx.style.fill = D.colors[g.a];
  });

  // ---------- rules
  function budget() {
    var l = Math.max(1, Math.min(D.levelCap, +lv.value || 1)), b = 2 * (l - 1);
    document.querySelectorAll('[data-biome]').forEach(function (c) { if (c.checked) b += +c.getAttribute('data-points'); });
    return b;
  }
  function spent() { var s = 0; for (var id in sel) s += sel[id] * type(id).c; return s; }
  function selectable(id) {
    if (sel[id]) return false;
    if (N[id].base) return true;
    return ADJ[id].some(function (o) { return sel[o]; });
  }
  function reachable(without) {
    var seen = {}, stack = [];
    for (var id in sel) if (id !== without && N[id].base) { seen[id] = 1; stack.push(id); }
    while (stack.length) { var u = stack.pop(); ADJ[u].forEach(function (v) { if (sel[v] && v !== without && !seen[v]) { seen[v] = 1; stack.push(v); } }); }
    return seen;
  }
  function notice(msg) { var n = $('#pl-notice'); n.textContent = msg; n.hidden = !msg; clearTimeout(notice.t); if (msg) notice.t = setTimeout(function () { n.hidden = true; }, 3500); }
  function add(id) {
    var t = type(id);
    if (!sel[id] && !selectable(id)) return notice('Locked: connect ' + t.n + ' to a skill you already have first.');
    if ((sel[id] || 0) >= t.m) return notice(t.n + ' is already at max rank.');
    if (spent() + t.c > budget()) return notice('Not enough points for ' + t.n + ' (' + t.c + ' pt). Raise your level or explored biomes.');
    sel[id] = (sel[id] || 0) + 1; pre.value = ''; render();
  }
  function remove(id) {
    if (!sel[id]) return;
    if (sel[id] > 1) { sel[id]--; pre.value = ''; return render(); }
    var keep = reachable(id), lost = Object.keys(sel).filter(function (x) { return x !== id && !keep[x]; });
    if (lost.length && !window.confirm('Removing ' + type(id).n + ' also refunds ' + lost.length + ' connected skill' + (lost.length > 1 ? 's' : '') + '. Continue?')) return;
    delete sel[id]; lost.forEach(function (x) { delete sel[x]; }); pre.value = ''; render();
  }

  // ---------- text and stats
  function fmt(id, rank) {
    var t = type(id);
    return t.d.map(function (line) {
      return line.replace(/\{\{(\w+)\}\}/g, function (m, k) {
        if (t.lv[k]) return rank ? t.lv[k][rank - 1] : t.lv[k].join(' / ');
        return t.v[k] !== undefined ? t.v[k] : m;
      });
    }).join('<br>');
  }
  function stats() {
    var s = { STR: 0, DEX: 0, INT: 0, CONS: 0, SPIRIT: 0, ENDURANCE: 0 }, flame = Math.max(1, Math.min(D.flameCap, +fl.value || 1));
    Object.keys(s).forEach(function (k) { s[k] += flame - 1; });
    for (var id in sel) {
      var t = type(id), key = N[id].t;
      for (var k in t.s) s[k] += t.s[k] * sel[id];
      if (key === 'RANGER') { s.DEX += sel[id]; s.ENDURANCE += sel[id]; }
      if (FLAME[key]) s[FLAME[key]] += Math.floor(flame / 2);
    }
    return s;
  }

  // ---------- render
  function render() {
    var b = budget(), s = spent(), left = b - s;
    ORDER.forEach(function (id) {
      var e = nodeEls[id], t = type(id), r = sel[id] || 0;
      e.g.setAttribute('data-state', r ? (r >= t.m ? 'max' : 'on') : selectable(id) ? 'open' : 'locked');
      if (e.rank) e.rank.textContent = r + '/' + t.m;
      e.g.classList.toggle('tr-hitq', !!query && t.n.toLowerCase().indexOf(query) >= 0);
      e.g.classList.toggle('tr-focus', id === focus);
    });
    linkEls.forEach(function (l) { l[0].classList.toggle('tr-on', !!sel[l[1]] && (l[2] === null || !!sel[l[2]])); });
    svg.classList.toggle('tr-searching', !!query);
    $('#pl-spent').textContent = s; $('#pl-budget').textContent = b;
    var le = $('#pl-left'); le.textContent = left; le.classList.toggle('text-destructive', left < 0);
    $('#pl-bar').style.width = Math.min(100, b ? s / b * 100 : 0) + '%';
    $('#pl-over').hidden = left >= 0;
    var st = stats(), rows = [['Strength', st.STR, '+' + st.STR * 5 + '% melee damage'], ['Dexterity', st.DEX, '+' + st.DEX * 5 + '% bow &amp; dagger damage'],
      ['Intelligence', st.INT, '+' + st.INT * 5 + '% magic damage'], ['Constitution', st.CONS, '+' + st.CONS * 50 + ' max health'],
      ['Spirit', st.SPIRIT, '+' + st.SPIRIT * 20 + ' max mana'], ['Endurance', st.ENDURANCE, '+' + st.ENDURANCE * 10 + ' max stamina']];
    $('#pl-attrs').innerHTML = rows.map(function (x) { return '<li class="flex justify-between gap-2"><span>' + x[0] + ' <strong>' + x[1] + '</strong></span><span class="text-muted-foreground">' + x[2] + '</span></li>'; }).join('');
    var areas = { Core: 0, Mage: 0, Warrior: 0, Ranger: 0 };
    for (var id in sel) areas[type(id).a] = (areas[type(id).a] || 0) + sel[id] * type(id).c;
    $('#pl-areas').innerHTML = Object.keys(areas).map(function (a) { return '<span class="inline-flex items-center gap-1.5"><i class="inline-block h-2.5 w-2.5 rounded-full" style="background:' + D.colors[a] + '"></i>' + a + ' <strong>' + areas[a] + '</strong></span>'; }).join('');
    info();
    var code = ORDER.map(function (id) { return B36[sel[id] || 0]; }).join('').replace(/0+$/, '');
    var bm = 0; document.querySelectorAll('[data-biome]').forEach(function (c, i) { if (c.checked) bm |= 1 << i; });
    history.replaceState(null, '', '#t=' + code + '&l=' + lv.value + '&e=' + bm + '&f=' + fl.value + (pre.value ? '&b=' + pre.value : ''));
  }
  function info() {
    var box = $('#pl-info');
    if (!focus) { box.innerHTML = '<p class="text-sm text-muted-foreground">Click a glowing entry node next to the center to start. Click to add a rank, right-click (or use −) to refund. Hover any node for details.</p>'; return; }
    var t = type(focus), r = sel[focus] || 0, st = r ? (r >= t.m ? 'Maxed' : 'Learned') : selectable(focus) ? 'Available' : 'Locked';
    var tags = (t.f.indexOf('new') >= 0 ? '<span class="rounded bg-primary px-1.5 py-0.5 text-[11px] font-semibold text-primary-foreground">New in 1.0</span>' : '');
    box.innerHTML = '<div class="flex items-start justify-between gap-2"><div><p class="font-semibold">' + t.n + '</p><p class="text-xs text-muted-foreground">' + t.a + (t.g ? ' · ' + t.g : '') + ' · ' + st + '</p></div>' + tags + '</div>' +
      '<p class="mt-2 text-sm leading-relaxed">' + fmt(focus, r) + '</p>' +
      '<div class="mt-3 flex items-center justify-between text-sm"><span>Rank <strong>' + r + '/' + t.m + '</strong> · ' + t.c + ' pt per rank</span>' +
      '<span class="flex gap-1.5"><button type="button" data-act="minus" class="tr-btn" aria-label="Refund a rank">−</button><button type="button" data-act="plus" class="tr-btn" aria-label="Add a rank">+</button></span></div>';
  }

  // ---------- view: fit, pan, zoom, pinch
  function apply() { view.setAttribute('transform', 'translate(' + vt.x + ' ' + vt.y + ') scale(' + vt.k + ')'); }
  function fit() { vt = { k: 1, x: 0, y: 0 }; apply(); }
  function toSvg(cx, cy) { var p = svg.createSVGPoint(); p.x = cx; p.y = cy; return p.matrixTransform(svg.getScreenCTM().inverse()); }
  function zoomAt(f, cx, cy) {
    var p = toSvg(cx, cy), k = Math.max(0.6, Math.min(5, vt.k * f)); f = k / vt.k;
    vt.x = p.x - (p.x - vt.x) * f; vt.y = p.y - (p.y - vt.y) * f; vt.k = k; apply();
  }
  svg.addEventListener('wheel', function (ev) { ev.preventDefault(); zoomAt(ev.deltaY < 0 ? 1.15 : 1 / 1.15, ev.clientX, ev.clientY); }, { passive: false });
  var ptrs = {}, drag = null, pinch = null, moved = false, downNode = null;
  svg.addEventListener('pointerdown', function (ev) {
    ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY }; moved = false;
    var dn = ev.target.closest('[data-node]'); downNode = dn ? dn.getAttribute('data-node') : null;
    var ids = Object.keys(ptrs);
    if (ids.length === 1) drag = { x: ev.clientX, y: ev.clientY, vx: vt.x, vy: vt.y };
    if (ids.length === 2) { var a = ptrs[ids[0]], b = ptrs[ids[1]]; pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), k: vt.k }; drag = null; }
  });
  svg.addEventListener('pointermove', function (ev) {
    if (!ptrs[ev.pointerId]) return; ptrs[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
    var ids = Object.keys(ptrs);
    if (pinch && ids.length === 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a.x - b.x, a.y - b.y);
      zoomAt(pinch.k * d / pinch.d / vt.k, (a.x + b.x) / 2, (a.y + b.y) / 2); moved = true; return;
    }
    if (!drag) return;
    if (!moved && Math.hypot(ev.clientX - drag.x, ev.clientY - drag.y) > 5) { moved = true; try { svg.setPointerCapture(ev.pointerId); } catch (e) {} }
    if (moved) { var s = svg.getScreenCTM().a; vt.x = drag.vx + (ev.clientX - drag.x) / s; vt.y = drag.vy + (ev.clientY - drag.y) / s; apply(); }
  });
  function up(ev) {
    var wasDrag = moved; delete ptrs[ev.pointerId]; if (Object.keys(ptrs).length < 2) pinch = null;
    if (!Object.keys(ptrs).length) drag = null;
    var id = downNode; downNode = null;
    if (ev.type !== 'pointerup' || wasDrag || ev.button !== 0 || !id) return;
    if (ev.pointerType === 'touch' && focus !== id) { focus = id; return render(); }
    focus = id; add(id); render();
  }
  svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
  svg.addEventListener('contextmenu', function (ev) { var g = ev.target.closest('[data-node]'); ev.preventDefault(); if (g) { focus = g.getAttribute('data-node'); remove(focus); render(); } });
  svg.addEventListener('mouseover', function (ev) { var g = ev.target.closest('[data-node]'); if (g && g.getAttribute('data-node') !== focus) { focus = g.getAttribute('data-node'); render(); } });
  $('#pl-info').addEventListener('click', function (ev) { var b = ev.target.closest('[data-act]'); if (!b || !focus) return; b.getAttribute('data-act') === 'plus' ? add(focus) : remove(focus); render(); });
  $('#tr-zoom-in').addEventListener('click', function () { var r = svg.getBoundingClientRect(); zoomAt(1.3, r.left + r.width / 2, r.top + r.height / 2); });
  $('#tr-zoom-out').addEventListener('click', function () { var r = svg.getBoundingClientRect(); zoomAt(1 / 1.3, r.left + r.width / 2, r.top + r.height / 2); });
  $('#tr-fit').addEventListener('click', fit);

  // ---------- controls, presets, sharing
  var STAGE = { 1: [15, 2], 2: [35, 4] };
  function loadPreset(b, stage) {
    var st = STAGE[stage], p = D.presets[st ? b + ':' + stage : b] || {};
    sel = {}; for (var id in p) sel[id] = p[id];
    lv.value = st ? st[0] : D.levelCap;
    document.querySelectorAll('[data-biome]').forEach(function (c, i) { c.checked = !st || i < st[1]; });
  }
  pre.addEventListener('change', function () { var v = pre.value; if (v) loadPreset(v); pre.value = v; render(); });
  document.querySelectorAll('[data-load]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      var b = a.getAttribute('data-load'), st = +a.getAttribute('data-stage');
      loadPreset(b, st); pre.value = b; fit(); render();
      document.querySelectorAll('[data-load]').forEach(function (x) { x.toggleAttribute('data-on', x === a); });
      document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
    });
  });
  [lv, fl].forEach(function (x) { x.addEventListener('input', render); });
  document.querySelectorAll('[data-biome]').forEach(function (c) { c.addEventListener('change', render); });
  $('#pl-reset').addEventListener('click', function () { if (!Object.keys(sel).length || window.confirm('Reset every skill point?')) { sel = {}; pre.value = ''; render(); } });
  $('#pl-copy').addEventListener('click', function () {
    var t = $('#pl-copy'), done = function () { t.textContent = 'Link copied'; setTimeout(function () { t.textContent = 'Copy build link'; }, 1600); };
    try { navigator.clipboard.writeText(location.href).then(done, done); } catch (e) { done(); }
  });
  $('#pl-search').addEventListener('input', function () { query = this.value.trim().toLowerCase(); render(); });
  document.querySelectorAll('[data-find]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault(); var key = a.getAttribute('data-find');
      var id = ORDER.filter(function (x) { return N[x].t === key; })[0]; if (!id) return;
      focus = id; vt.k = 2.5; vt.x = -N[id].x * vt.k; vt.y = -N[id].y * vt.k; apply(); render();
      document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
    });
  });
  (function fromHash() {
    var h = {}; location.hash.slice(1).split('&').forEach(function (kv) { var a = kv.split('='); if (a[0]) h[a[0]] = decodeURIComponent(a[1] || ''); });
    if (h.b && D.presets[h.b]) { loadPreset(h.b, +h.s || 0); pre.value = h.b; }
    if (h.l) lv.value = h.l; if (h.f) fl.value = h.f;
    if (h.e !== undefined) document.querySelectorAll('[data-biome]').forEach(function (c, i) { c.checked = !!(+h.e & (1 << i)); });
    if (h.t !== undefined) {
      sel = {};
      for (var i = 0; i < h.t.length && i < ORDER.length; i++) { var r = B36.indexOf(h.t[i]); if (r > 0) sel[ORDER[i]] = Math.min(r, type(ORDER[i]).m); }
      var ok = reachable(null); Object.keys(sel).forEach(function (id) { if (!ok[id]) delete sel[id]; });
    }
    if (h.n) { var nid = ORDER.filter(function (x) { return N[x].t === h.n; })[0]; if (nid) { focus = nid; zoomTo = nid; } }
  })();
  document.querySelectorAll('[data-pl-js]').forEach(function (x) { x.hidden = false; });
  fit(); if (zoomTo) { vt.k = 2.5; vt.x = -N[zoomTo].x * vt.k; vt.y = -N[zoomTo].y * vt.k; apply(); } render();
})();

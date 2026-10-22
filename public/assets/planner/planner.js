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
  // ---------- share image: drawn on a canvas from the current build, no server involved
  function roundRect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
  function drawImage() {
    var W = 1200, H = 675, S = 2, cv = document.createElement('canvas'), c = cv.getContext('2d');
    cv.width = W * S; cv.height = H * S; c.scale(S, S);
    c.fillStyle = '#0b0b10'; c.fillRect(0, 0, W, H);
    var glow = c.createRadialGradient(330, 337, 40, 330, 337, 420); glow.addColorStop(0, 'rgba(249,115,22,.10)'); glow.addColorStop(1, 'rgba(249,115,22,0)');
    c.fillStyle = glow; c.fillRect(0, 0, 680, H);
    // tree
    var k = 640 / 1960, ox = 340, oy = 337, P = function (x, y) { return [ox + x * k, oy + y * k]; };
    c.lineCap = 'round';
    function line(a, b, on) { var p = P(a[0], a[1]), q = P(b[0], b[1]); c.strokeStyle = on ? '#fb923c' : 'rgba(160,160,180,.22)'; c.lineWidth = on ? 2.2 : 1; c.beginPath(); c.moveTo(p[0], p[1]); c.lineTo(q[0], q[1]); c.stroke(); }
    D.edges.forEach(function (e) { line([N[e[0]].x, N[e[0]].y], [N[e[1]].x, N[e[1]].y], sel[e[0]] && sel[e[1]]); });
    ORDER.forEach(function (id) { var n = N[id]; if (n.base) line([n.x, n.y], [n.ax, n.ay], !!sel[id]); });
    ORDER.forEach(function (id) {
      var n = N[id], t = type(id), p = P(n.x, n.y), r = isAttr(id) ? 2.4 : t.c >= 4 ? 5.2 : 4.2, col = color(id);
      c.beginPath(); c.arc(p[0], p[1], r, 0, Math.PI * 2);
      if (sel[id]) { c.fillStyle = col; c.shadowColor = col; c.shadowBlur = 8; c.fill(); c.shadowBlur = 0; }
      else { c.fillStyle = '#16161d'; c.fill(); c.strokeStyle = col; c.globalAlpha = .45; c.lineWidth = 1; c.stroke(); c.globalAlpha = 1; }
    });
    c.textAlign = 'center'; c.font = '700 11px Cinzel, serif';
    Object.keys(groups).forEach(function (g) {
      var o = groups[g], cx = o.x / o.n, cy = o.y / o.n, d = Math.hypot(cx, cy) || 1, f = (d + 200) / d, p = P(cx * f, cy * f);
      c.fillStyle = D.colors[o.a]; c.globalAlpha = .7; c.fillText(g.toUpperCase(), p[0], p[1]); c.globalAlpha = 1;
    });
    // panel
    var x = 700, y = 56, st = stats(), sp = spent(), bu = budget();
    var name = ($('#pl-name') && $('#pl-name').value.trim()) || (pre.value ? pre.options[pre.selectedIndex].text : 'My Enshrouded build');
    c.textAlign = 'left'; c.fillStyle = '#f97316'; c.font = '600 13px Inter, sans-serif'; c.fillText('ENSHROUDED 1.0 BUILD', x, y);
    c.fillStyle = '#f4f4f5'; c.font = '700 30px Cinzel, serif';
    var title = name; while (c.measureText(title).width > 460 && title.length > 4) title = title.slice(0, -2);
    c.fillText(title === name ? title : title + '…', x, y + 40);
    c.fillStyle = '#a1a1aa'; c.font = '500 15px Inter, sans-serif';
    c.fillText('Level ' + (lv.value || D.levelCap) + '  ·  Flame ' + (fl.value || 1) + '  ·  ' + sp + ' / ' + bu + ' skill points', x, y + 70);
    roundRect(c, x, y + 84, 460, 8, 4); c.fillStyle = '#27272a'; c.fill();
    if (sp > 0) { roundRect(c, x, y + 84, Math.max(8, Math.min(1, bu ? sp / bu : 0) * 460), 8, 4); c.fillStyle = '#f97316'; c.fill(); }
    var areas = { Mage: 0, Warrior: 0, Ranger: 0, Core: 0 }; for (var id in sel) areas[type(id).a] = (areas[type(id).a] || 0) + sel[id] * type(id).c;
    var ax = x; c.font = '500 13px Inter, sans-serif';
    Object.keys(areas).forEach(function (a) { c.fillStyle = D.colors[a]; c.beginPath(); c.arc(ax + 5, y + 114, 5, 0, Math.PI * 2); c.fill(); c.fillStyle = '#d4d4d8'; var s = a + ' ' + areas[a]; c.fillText(s, ax + 15, y + 119); ax += c.measureText(s).width + 32; });
    var attrs = [['Strength', st.STR], ['Dexterity', st.DEX], ['Intelligence', st.INT], ['Constitution', st.CONS], ['Spirit', st.SPIRIT], ['Endurance', st.ENDURANCE]];
    attrs.forEach(function (a, i) {
      var cx = x + (i % 3) * 155, cy = y + 146 + Math.floor(i / 3) * 52;
      roundRect(c, cx, cy, 145, 44, 8); c.fillStyle = '#18181b'; c.fill();
      c.fillStyle = '#a1a1aa'; c.font = '500 11px Inter, sans-serif'; c.fillText(a[0].toUpperCase(), cx + 12, cy + 17);
      c.fillStyle = '#f4f4f5'; c.font = '700 18px Inter, sans-serif'; c.fillText(String(a[1]), cx + 12, cy + 37);
    });
    var skills = Object.keys(sel).filter(function (id) { return !isAttr(id); }).map(function (id) { var t = type(id); return { n: t.n, r: sel[id], m: t.m, p: sel[id] * t.c, a: t.a }; });
    skills.sort(function (a, b) { return b.p - a.p || a.n.localeCompare(b.n); });
    c.fillStyle = '#a1a1aa'; c.font = '600 12px Inter, sans-serif'; c.fillText('KEY SKILLS (' + skills.length + ' TOTAL)', x, y + 276);
    c.font = '500 14px Inter, sans-serif';
    skills.slice(0, 14).forEach(function (s, i) {
      var cx = x + (i % 2) * 235, cy = y + 302 + Math.floor(i / 2) * 26, label = s.n + (s.m > 1 ? '  ' + s.r + '/' + s.m : '');
      c.fillStyle = D.colors[s.a]; c.beginPath(); c.arc(cx + 4, cy - 5, 3.5, 0, Math.PI * 2); c.fill();
      c.fillStyle = '#e4e4e7'; while (c.measureText(label).width > 210 && label.length > 4) label = label.slice(0, -2);
      c.fillText(label, cx + 14, cy);
    });
    if (!skills.length) { c.fillStyle = '#71717a'; c.fillText('No skills learned yet', x, y + 302); }
    // footer
    c.strokeStyle = '#27272a'; c.lineWidth = 1; c.beginPath(); c.moveTo(x, H - 62); c.lineTo(W - 40, H - 62); c.stroke();
    c.fillStyle = '#f97316'; c.font = '700 16px Cinzel, serif'; c.fillText('ENSHROUDED BUILDS', x, H - 34);
    c.fillStyle = '#a1a1aa'; c.font = '500 13px Inter, sans-serif'; c.fillText('Plan yours: enshroudedbuilds.org/skill-planner', x, H - 15);
    return { canvas: cv, name: name };
  }
  $('#pl-image') && $('#pl-image').addEventListener('click', function () {
    var btn = this, label = btn.textContent;
    btn.textContent = 'Drawing…';
    var fonts = document.fonts ? Promise.all([document.fonts.load('700 30px Cinzel'), document.fonts.load('500 14px Inter'), document.fonts.load('700 18px Inter')]).catch(function () {}) : Promise.resolve();
    fonts.then(function () {
      var out = drawImage(), file = (out.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'enshrouded-build') + '.png';
      out.canvas.toBlob(function (blob) {
        btn.textContent = label;
        if (!blob) return notice('Could not create the image in this browser.');
        var f = typeof File === 'function' ? new File([blob], file, { type: 'image/png' }) : null;
        var link = 'https://enshroudedbuilds.org/skill-planner/' + location.hash;
        if (f && navigator.canShare && navigator.canShare({ files: [f] }) && /Android|iPhone|iPad/i.test(navigator.userAgent)) {
          navigator.share({ files: [f], title: out.name, text: link }).catch(function () {});
          return;
        }
        var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = file;
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
        notice('Image saved. Post it with your build link so others can open it.');
      }, 'image/png');
    });
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

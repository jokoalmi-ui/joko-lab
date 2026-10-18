// Inyección temporal de verificación estructural (checklist 17/17 + corte vertical)
(function () {
  const out = [];
  out.push('scrollHeight=' + document.body.scrollHeight);
  const pie = document.querySelector('.pie');
  if (pie) out.push('pieBottom=' + Math.round(pie.getBoundingClientRect().bottom));
  else out.push('pie=MISSING');
  const checks = {
    '1_titulo': !!document.querySelector('h1') && document.querySelector('h1').textContent.trim(),
    '2_casa': !!document.querySelector('.casa') && document.querySelector('.casa').textContent.trim(),
    '3_fecha': !!document.querySelector('.fecha-sep') && document.querySelector('.fecha-sep').textContent.trim(),
    '4_año': (document.body.textContent.match(/2020/) ? '2020' : 'MISSING'),
    '5_concentracion': (document.body.textContent.match(/Extrait de Parfum/) ? 'Extrait de Parfum' : 'MISSING'),
    '6_genero': (document.body.textContent.match(/Unisex/) ? 'Unisex' : 'MISSING'),
    '7_familia': (document.body.textContent.match(/Oriental Woody/) ? 'Oriental Woody' : 'MISSING'),
    '8_perfumista': (document.body.textContent.match(/Quentin Bisch/) ? 'Quentin Bisch' : 'MISSING'),
    '9_rating': (document.body.textContent.match(/4,06/) ? '4,06' : 'MISSING'),
    '10_piramide': (document.body.textContent.match(/PIMIENTA · COMINO/) ? 'OK' : 'MISSING'),
    '11_longevidad': (document.body.textContent.match(/8 h\+/) ? '8 h+' : 'MISSING'),
    '12_estela': (document.body.textContent.match(/intensa/) ? 'intensa' : 'MISSING'),
    '13_precio': (document.body.textContent.match(/275 €/) ? '275 €' : 'MISSING'),
    '14_alternativas': (document.body.textContent.match(/Bois Impérial/) && document.body.textContent.match(/Ganymede/) && document.body.textContent.match(/B683/) ? '3 alt' : 'MISSING'),
    '15_cita': (document.body.textContent.match(/Miguel Matos/) ? 'OK' : 'MISSING'),
    '16_qr': !!document.querySelector('.qr') && document.querySelector('.qr').getAttribute('src'),
    '17_pie': !!pie,
    'nota_fondo': (document.body.textContent.match(/ComfyUI/) ? 'OK' : 'MISSING')
  };
  for (const k in checks) out.push(k + '=' + checks[k]);
  const pre = document.createElement('pre');
  pre.id = 'checkout';
  pre.textContent = out.join('\n');
  document.body.appendChild(pre);
})();

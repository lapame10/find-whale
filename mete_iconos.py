#!/usr/bin/env python3
"""Mete los iconos profesionales (Material Symbols) en Find Whale.

Pam dijo que los dibujos a mano parecian de un niño de 5 años. Los cambio por
los de Google: pin de gota con parapente (volando) y circulo con persona
(aterrizado), como los de una app de mapas de verdad.
"""

RUTA = '/Users/lapame10/.hermes/workspace/find-whale/index.html'

para = open('/tmp/path_para.txt').read().strip()
hik = open('/tmp/path_hik.txt').read().strip()

s = open(RUTA, encoding='utf-8').read()

ini = s.find('function iconoPiloto(p){')
fin = s.find('/* ==========================================================================\n   EL MAPA (OpenStreetMap')

if ini < 0:
    raise SystemExit('no encuentro iconoPiloto')
if fin < 0:
    raise SystemExit('no encuentro el bloque del mapa')

nuevo = """const ICONO_PARA = '%s';
const ICONO_PERSONA = '%s';

function iconoPiloto(p){
  const col = (COLORES.find(c => c.id === p.color) || {}).c || '#888';
  const enTierra = (p.estado === 'tierra');
  const icono = enTierra ? ICONO_PERSONA : ICONO_PARA;

  /* VOLANDO: pin de gota (la punta señala el sitio exacto donde esta)
     EN TIERRA: circulo con una sombra debajo (esta en el suelo) */
  let cuerpo, ix, iy, ancla;
  if (enTierra){
    cuerpo = '<ellipse cx="19" cy="50" rx="13" ry="4" fill="rgba(0,0,0,.16)"/>'
           + '<circle cx="19" cy="22" r="19" fill="' + col + '" stroke="#fff" stroke-width="2.6"/>';
    ix = 7; iy = 10; ancla = [19, 22];
  } else {
    cuerpo = '<path d="M19 2C10 2 3 9 3 18c0 12.5 16 28 16 28s16-15.5 16-28C35 9 28 2 19 2z"'
           + ' fill="' + col + '" stroke="#fff" stroke-width="2.6"/>';
    ix = 7; iy = 6; ancla = [19, 46];
  }

  return L.divIcon({
    className: 'pinPil',
    html: '<svg viewBox="0 0 38 56" width="38" height="56">' + cuerpo
        + '<svg x="' + ix + '" y="' + iy + '" width="24" height="24" viewBox="0 -960 960 960">'
        + '<path d="' + icono + '" fill="#fff"/></svg></svg>',
    iconSize: [38, 56],
    iconAnchor: ancla
  });
}

""" % (para, hik)

s = s[:ini] + nuevo + s[fin:]
open(RUTA, 'w', encoding='utf-8').write(s)
print('  hecho.')
print('  parapente:', len(para), 'chars')
print('  persona :', len(hik), 'chars')
print('  archivo :', len(s), 'bytes')

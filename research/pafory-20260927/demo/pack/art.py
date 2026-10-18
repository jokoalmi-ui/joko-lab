"""Frascos en SVG inline. Determinista: ids por crc32, no por hash()."""
import zlib


def _id(p, s):
    return p + str(zlib.crc32(s.encode()) % 99999)


def vial(w=110, h=210, tint=("#F0DCA6", "#A97F2E"), cap=("#EDE3C8", "#8E7429")):
    """Decant 10 ml: cristal cilindrico, collar y tapon metalizado."""
    gl, cp = _id("lg", str(tint)), _id("cp", str(cap))
    t1, t2 = tint
    c1, c2 = cap
    svg = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 110 210" fill="none">',
        "<defs>",
        f'<linearGradient id="{gl}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{t1}"/><stop offset="1" stop-color="{t2}"/></linearGradient>',
        f'<linearGradient id="{cp}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>',
        "</defs>",
        f'<rect x="37" y="2" width="36" height="30" rx="9" fill="url(#{cp})"/>',
        '<rect x="43" y="7" width="7" height="21" rx="3.5" fill="rgba(255,255,255,.45)"/>',
        '<rect x="31" y="32" width="48" height="15" rx="5" fill="#242730" stroke="rgba(255,255,255,.13)"/>',
        '<rect x="45" y="46" width="20" height="9" fill="#1C1F26"/>',
        '<rect x="19" y="52" width="72" height="154" rx="22" fill="rgba(255,255,255,.05)" '
        'stroke="rgba(255,255,255,.24)" stroke-width="1.6"/>',
        f'<rect x="26" y="104" width="58" height="96" rx="16" fill="url(#{gl})" opacity=".92"/>',
        '<rect x="26" y="104" width="58" height="7" rx="3.5" fill="rgba(255,255,255,.28)"/>',
        '<rect x="31" y="126" width="48" height="52" rx="8" fill="rgba(9,10,13,.55)" '
        'stroke="rgba(255,255,255,.14)"/>',
        '<rect x="39" y="140" width="32" height="4" rx="2" fill="rgba(255,255,255,.62)"/>',
        '<rect x="39" y="151" width="22" height="4" rx="2" fill="rgba(255,255,255,.36)"/>',
        '<rect x="39" y="162" width="27" height="3" rx="1.5" fill="rgba(255,255,255,.2)"/>',
        '<rect x="28" y="66" width="9" height="128" rx="4.5" fill="rgba(255,255,255,.12)"/>',
        '<rect x="82" y="72" width="4" height="118" rx="2" fill="rgba(255,255,255,.07)"/>',
        "</svg>",
    ]
    return "".join(svg)


def bottle(w=150, h=250, tint=("#F0DCA6", "#A97F2E"), cap=("#EDE3C8", "#8E7429")):
    """Frasco con atomizador: hombros, collar, boquilla y placa de etiqueta."""
    gl, cp = _id("bg", str(tint)), _id("bp", str(cap))
    t1, t2 = tint
    c1, c2 = cap
    svg = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 150 250" fill="none">',
        "<defs>",
        f'<linearGradient id="{gl}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{t1}"/><stop offset="1" stop-color="{t2}"/></linearGradient>',
        f'<linearGradient id="{cp}" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>',
        "</defs>",
        '<rect x="67" y="22" width="16" height="14" rx="3" fill="#2E323B"/>',
        f'<rect x="59" y="4" width="32" height="34" rx="8" fill="url(#{cp})"/>',
        '<rect x="65" y="9" width="7" height="24" rx="3.5" fill="rgba(255,255,255,.42)"/>',
        '<rect x="50" y="36" width="50" height="16" rx="5" fill="#242730" stroke="rgba(255,255,255,.13)"/>',
        '<rect x="24" y="52" width="102" height="190" rx="26" fill="rgba(255,255,255,.055)" '
        'stroke="rgba(255,255,255,.22)" stroke-width="1.6"/>',
        f'<rect x="31" y="116" width="88" height="119" rx="20" fill="url(#{gl})" opacity=".9"/>',
        '<rect x="31" y="116" width="88" height="8" rx="4" fill="rgba(255,255,255,.26)"/>',
        '<rect x="46" y="146" width="58" height="62" rx="9" fill="rgba(9,10,13,.5)" '
        'stroke="rgba(255,255,255,.13)"/>',
        '<rect x="56" y="160" width="38" height="5" rx="2.5" fill="rgba(255,255,255,.6)"/>',
        '<rect x="56" y="172" width="26" height="4" rx="2" fill="rgba(255,255,255,.36)"/>',
        '<rect x="56" y="183" width="32" height="3" rx="1.5" fill="rgba(255,255,255,.2)"/>',
        '<rect x="35" y="70" width="11" height="150" rx="5.5" fill="rgba(255,255,255,.1)"/>',
        '<rect x="112" y="78" width="5" height="138" rx="2.5" fill="rgba(255,255,255,.06)"/>',
        "</svg>",
    ]
    return "".join(svg)

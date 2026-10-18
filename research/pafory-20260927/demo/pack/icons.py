"""Iconos y piezas de interfaz en SVG/CSS inline (sin assets externos)."""


def star(filled=True, size=24, color="#E7CB84"):
    c = color if filled else "rgba(255,255,255,.22)"
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{c}">'
        '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 21 12 17.77 5.82 21 7 14.14l-5-4.87 '
        '6.91-1.01L12 2z"/></svg>'
    )


def stars(n=5, size=24):
    out = "".join(star(i < n, size) for i in range(5))
    return f'<div class="stars">{out}</div>'


def avatar(initials, size=64):
    return (
        f'<div class="avatar" style="width:{size}px;height:{size}px;font-size:{int(size * 0.36)}px;'
        f'background:linear-gradient(140deg,#E7CB84,#C9A24A)">{initials}</div>'
    )


def _ic(body, size, color, sw="1.8"):
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
        f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def ic_link(size=28, color="#D8B45C"):
    return _ic('<path d="M10 13a5 5 0 007.07 0l1.66-1.66a5 5 0 10-7.07-7.07L10.5 5.5"/>'
               '<path d="M14 11a5 5 0 00-7.07 0L5.27 12.66a5 5 0 107.07 7.07L13.5 18.5"/>',
               size, color)


def ic_code(size=28, color="#D8B45C"):
    return _ic('<path d="M9 18l-6-6 6-6"/><path d="M15 6l6 6-6 6"/>', size, color, "1.9")


def ic_cart(size=28, color="#D8B45C"):
    return _ic('<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/>'
               '<path d="M2 3h3l2.4 11.2A2 2 0 009.35 16H18a2 2 0 002-1.65L21.5 7H6"/>',
               size, color)


def ic_chart(size=28, color="#D8B45C"):
    return _ic('<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/>'
               '<path d="M22 20H2"/>', size, color, "1.9")


def ic_check(size=28, color="#D8B45C"):
    return _ic('<path d="M20 6L9 17l-5-5"/>', size, color, "2.1")


def ic_pay(size=28, color="#D8B45C"):
    return _ic('<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20"/>'
               '<path d="M6 15h4"/>', size, color)


def ic_block(size=28, color="#7B828F"):
    return _ic('<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>', size, color, "2")


def ic_clock(size=28, color="#D8B45C"):
    return _ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l4 2"/>', size, color)

/* AgroSolo: comportamento das telas, sem dependências além do Plotly nas páginas de gráfico. */
(function () {
    "use strict";

    const raiz = document.documentElement;
    const reduzMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");

    function ler(chave) {
        try {
            return JSON.parse(localStorage.getItem(chave));
        } catch (e) {
            return null;
        }
    }

    function gravar(chave, valor) {
        try {
            if (valor === null) localStorage.removeItem(chave);
            else localStorage.setItem(chave, JSON.stringify(valor));
        } catch (e) {
            /* sem armazenamento: a tela funciona igual, só não lembra a escolha */
        }
    }

    /* ---------------- Tema claro/escuro ---------------- */
    // claro por padrão; escuro só pelo botão
    function temaAtual() {
        return raiz.dataset.theme === "dark" ? "dark" : "light";
    }

    function atualizarBotoesTema() {
        const escuro = temaAtual() === "dark";
        document.querySelectorAll("[data-alternar-tema]").forEach(function (botao) {
            botao.setAttribute("aria-label", escuro ? "Usar tema claro" : "Usar tema escuro");
            botao.setAttribute("title", escuro ? "Usar tema claro" : "Usar tema escuro");
            botao.querySelector("[data-icone-sol]").hidden = !escuro;
            botao.querySelector("[data-icone-lua]").hidden = escuro;
        });
    }

    document.addEventListener("click", function (ev) {
        if (!ev.target.closest("[data-alternar-tema]")) return;
        const novo = temaAtual() === "dark" ? "light" : "dark";
        raiz.dataset.theme = novo;
        gravar("agrosolo:tema", novo);
        atualizarBotoesTema();
        document.dispatchEvent(new CustomEvent("agrosolo:tema"));
    });

    atualizarBotoesTema();

    /* ---------------- Menu lateral (gaveta no celular) ---------------- */
    const app = document.querySelector(".app");
    const rail = document.getElementById("rail");
    const botaoRail = document.querySelector("[data-abrir-rail]");

    function abrirRail(abrir) {
        if (!app || !rail) return;
        app.classList.toggle("app--rail-aberto", abrir);
        if (botaoRail) botaoRail.setAttribute("aria-expanded", String(abrir));
        if (abrir) {
            const atual = rail.querySelector('[aria-current="page"]') || rail.querySelector("a");
            if (atual) atual.focus();
        } else if (botaoRail && rail.contains(document.activeElement)) {
            botaoRail.focus();
        }
    }

    if (botaoRail) botaoRail.addEventListener("click", function () { abrirRail(true); });
    document.querySelectorAll("[data-fechar-rail]").forEach(function (el) {
        el.addEventListener("click", function () { abrirRail(false); });
    });

    /* ---------------- Dropdown menu ---------------- */
    function fecharDropdowns(exceto) {
        document.querySelectorAll("[data-dropdown]").forEach(function (dd) {
            if (dd === exceto) return;
            const menu = dd.querySelector("[data-dropdown-menu]");
            const gatilho = dd.querySelector("[data-dropdown-gatilho]");
            if (menu && !menu.hidden) {
                menu.hidden = true;
                gatilho.setAttribute("aria-expanded", "false");
            }
        });
    }

    function itensMenu(menu) {
        return Array.from(menu.querySelectorAll('[role="menuitem"]'));
    }

    document.addEventListener("click", function (ev) {
        const gatilho = ev.target.closest("[data-dropdown-gatilho]");
        if (gatilho) {
            const dd = gatilho.closest("[data-dropdown]");
            const menu = dd.querySelector("[data-dropdown-menu]");
            const abrir = menu.hidden;
            fecharDropdowns(dd);
            menu.hidden = !abrir;
            gatilho.setAttribute("aria-expanded", String(abrir));
            if (abrir && ev.detail === 0) {
                const primeiro = itensMenu(menu)[0];
                if (primeiro) primeiro.focus();
            }
            return;
        }
        if (ev.target.closest("[data-dropdown-menu] [role='menuitem']")) {
            fecharDropdowns();
            return;
        }
        if (!ev.target.closest("[data-dropdown]")) fecharDropdowns();
    });

    document.addEventListener("keydown", function (ev) {
        const menu = ev.target.closest && ev.target.closest("[data-dropdown-menu]");
        const dd = ev.target.closest && ev.target.closest("[data-dropdown]");

        if (ev.key === "Escape") {
            if (dd) {
                const aberto = dd.querySelector("[data-dropdown-menu]:not([hidden])");
                if (aberto) {
                    fecharDropdowns();
                    dd.querySelector("[data-dropdown-gatilho]").focus();
                    return;
                }
            }
            if (app && app.classList.contains("app--rail-aberto")) abrirRail(false);
            return;
        }

        if (dd && !menu && ev.key === "ArrowDown" && ev.target.matches("[data-dropdown-gatilho]")) {
            ev.preventDefault();
            ev.target.click();
            const m = dd.querySelector("[data-dropdown-menu]");
            if (!m.hidden) itensMenu(m)[0].focus();
            return;
        }

        if (menu && (ev.key === "ArrowDown" || ev.key === "ArrowUp" || ev.key === "Home" || ev.key === "End")) {
            ev.preventDefault();
            const itens = itensMenu(menu);
            let i = itens.indexOf(document.activeElement);
            if (ev.key === "ArrowDown") i = (i + 1) % itens.length;
            if (ev.key === "ArrowUp") i = (i - 1 + itens.length) % itens.length;
            if (ev.key === "Home") i = 0;
            if (ev.key === "End") i = itens.length - 1;
            itens[i].focus();
        }

        if (menu && ev.key === "Tab") fecharDropdowns();
    });

    /* ---------------- Mostrar senha ---------------- */
    document.querySelectorAll("[data-mostrar-senha]").forEach(function (botao) {
        const campo = document.getElementById(botao.getAttribute("aria-controls"));
        botao.addEventListener("click", function () {
            const mostrar = campo.type === "password";
            campo.type = mostrar ? "text" : "password";
            botao.setAttribute("aria-pressed", String(mostrar));
            botao.setAttribute("aria-label", mostrar ? "Esconder senha" : "Mostrar senha");
            botao.querySelector("[data-icone-olho]").hidden = mostrar;
            botao.querySelector("[data-icone-olho-fechado]").hidden = !mostrar;
        });
    });

    /* ---------------- Confirmação de ações destrutivas ---------------- */
    document.addEventListener("submit", function (ev) {
        const mensagem = ev.target.getAttribute("data-confirmar");
        if (mensagem && !window.confirm(mensagem)) ev.preventDefault();
    });

    /* ---------------- Fechar mensagens ---------------- */
    document.addEventListener("click", function (ev) {
        const botao = ev.target.closest("[data-fechar-alerta]");
        if (botao) botao.closest(".alerta").remove();
    });

    /* ---------------- Gráficos (Plotly com o tema da página) ---------------- */
    const graficos = new Map();

    function coresTema() {
        const css = getComputedStyle(raiz);
        const v = function (nome) { return css.getPropertyValue(nome).trim(); };
        return { tinta: v("--tinta"), tinta2: v("--tinta-2"), linha: v("--linha"), superficie: v("--superficie") };
    }

    function comTema(figura) {
        const c = coresTema();
        const data = JSON.parse(JSON.stringify(figura.data));
        const layout = JSON.parse(JSON.stringify(figura.layout || {}));

        layout.font = Object.assign({}, layout.font, { color: c.tinta2 });
        layout.hoverlabel = Object.assign({}, layout.hoverlabel, {
            bgcolor: c.superficie,
            bordercolor: c.linha,
            font: Object.assign({}, (layout.hoverlabel || {}).font, { color: c.tinta })
        });
        layout.legend = Object.assign({}, layout.legend, { font: { color: c.tinta2 } });
        Object.keys(layout).forEach(function (chave) {
            if (/^[xy]axis\d*$/.test(chave)) layout[chave] = Object.assign({}, layout[chave], { gridcolor: c.linha });
        });

        (layout.annotations || []).forEach(function (a) {
            if (a.bgcolor) a.bgcolor = c.superficie;
        });

        // pontos vazados, como no line chart do kit: miolo da cor do fundo
        data.forEach(function (t) {
            if (t.marker && t.marker.color === "#ffffff") t.marker.color = c.superficie;
        });

        return { data: data, layout: layout };
    }

    function desenhar(area, figura) {
        const f = comTema(figura);
        return window.Plotly.react(area, f.data, f.layout, {
            responsive: true,
            displayModeBar: false,
            displaylogo: false,
            doubleClick: "reset"
        });
    }

    document.querySelectorAll("[data-grafico]").forEach(function (el) {
        const fonte = el.querySelector('script[type="application/json"]');
        const area = el.querySelector(".grafico__area");
        if (!fonte || !area) return;

        if (!window.Plotly) {
            const erro = document.createElement("p");
            erro.className = "grafico__erro";
            erro.textContent = "O gráfico não carregou. Recarregue a página para tentar de novo.";
            area.replaceWith(erro);
            return;
        }

        const figura = JSON.parse(fonte.textContent);
        graficos.set(el.id, { area: area, figura: figura });
        desenhar(area, figura);
    });

    document.addEventListener("agrosolo:tema", function () {
        graficos.forEach(function (g) { desenhar(g.area, g.figura); });
    });

    document.addEventListener("click", function (ev) {
        const botao = ev.target.closest("[data-grafico-acao]");
        if (!botao) return;
        const g = graficos.get(botao.getAttribute("data-alvo"));
        if (!g) return;
        const acao = botao.getAttribute("data-grafico-acao");
        if (acao === "png") {
            window.Plotly.downloadImage(g.area, {
                format: "png",
                filename: botao.getAttribute("data-arquivo") || "agrosolo-grafico",
                scale: 2
            });
        }
        if (acao === "zoom") desenhar(g.area, g.figura);
    });

    /* ---------------- Grade de widgets arrastável ---------------- */
    function iniciarWidgets(grade) {
        const chave = "agrosolo:widgets:" + grade.id;
        const botao = document.querySelector('[data-organizar="' + grade.id + '"]');
        const restaurar = document.querySelector('[data-restaurar="' + grade.id + '"]');
        const dica = document.querySelector('[data-dica="' + grade.id + '"]');
        const anuncio = document.querySelector('[data-anuncio="' + grade.id + '"]');
        const itens = function () { return Array.from(grade.querySelectorAll("[data-widget]")); };
        const ordemPadrao = itens().map(function (e) { return e.dataset.widget; });
        let editando = false;

        function aplicarOrdem(ordem) {
            ordem.forEach(function (id) {
                const el = itens().find(function (e) { return e.dataset.widget === id; });
                if (el) grade.appendChild(el);
            });
        }

        const salva = ler(chave);
        if (Array.isArray(salva)) aplicarOrdem(salva);

        function salvar() {
            gravar(chave, itens().map(function (e) { return e.dataset.widget; }));
        }

        function anunciar(el) {
            const lista = itens();
            if (anuncio) {
                anuncio.textContent = el.getAttribute("aria-label") + ": posição " +
                    (lista.indexOf(el) + 1) + " de " + lista.length + ".";
            }
        }

        // FLIP: mede, reordena, anima cada widget da posição antiga para a nova
        function reordenar(mover, ignorar) {
            const antes = new Map(itens().map(function (e) { return [e, e.getBoundingClientRect()]; }));
            mover();
            if (reduzMovimento.matches) return;
            itens().forEach(function (e) {
                if (e === ignorar) return;
                const a = antes.get(e);
                const d = e.getBoundingClientRect();
                const dx = a.left - d.left;
                const dy = a.top - d.top;
                if (dx || dy) {
                    e.animate(
                        [{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "none" }],
                        { duration: 240, easing: "cubic-bezier(.2,.7,.2,1)" }
                    );
                }
            });
        }

        function alternar(estado) {
            editando = estado;
            grade.classList.toggle("widgets--editando", estado);
            botao.setAttribute("aria-pressed", String(estado));
            botao.querySelector("[data-rotulo]").textContent = estado ? "Concluir" : "Organizar painel";
            if (restaurar) restaurar.hidden = !estado;
            if (dica) dica.hidden = !estado;
            itens().forEach(function (e) {
                if (estado) e.setAttribute("tabindex", "0");
                else e.removeAttribute("tabindex");
            });
        }

        botao.addEventListener("click", function () { alternar(!editando); });

        if (restaurar) {
            restaurar.addEventListener("click", function () {
                reordenar(function () { aplicarOrdem(ordemPadrao); });
                gravar(chave, null);
            });
        }

        // teclado: Alt + setas move o widget em foco (como no componente original)
        grade.addEventListener("keydown", function (ev) {
            if (!editando || !ev.altKey) return;
            const el = ev.target.closest("[data-widget]");
            if (!el || ev.target !== el) return;
            const lista = itens();
            const i = lista.indexOf(el);
            let destino = null;
            if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") destino = i - 1;
            if (ev.key === "ArrowRight" || ev.key === "ArrowDown") destino = i + 1;
            if (destino === null || destino < 0 || destino >= lista.length) return;
            ev.preventDefault();
            reordenar(function () {
                grade.insertBefore(el, destino < i ? lista[destino] : lista[destino].nextSibling);
            });
            el.focus();
            salvar();
            anunciar(el);
        });

        // ponteiro: mouse e caneta arrastam na hora; toque precisa de um toque longo,
        // para a página continuar rolando
        grade.addEventListener("pointerdown", function (ev) {
            if (!editando || ev.button !== 0) return;
            const el = ev.target.closest("[data-widget]");
            if (!el) return;

            if (ev.pointerType !== "touch") {
                ev.preventDefault();
                arrastar(el, ev);
                return;
            }

            const inicioX = ev.clientX;
            const inicioY = ev.clientY;
            const cancelar = function (e) {
                if (e.type !== "pointermove" || Math.hypot(e.clientX - inicioX, e.clientY - inicioY) > 8) {
                    clearTimeout(timer);
                    grade.removeEventListener("pointermove", cancelar);
                    grade.removeEventListener("pointerup", cancelar);
                    grade.removeEventListener("pointercancel", cancelar);
                }
            };
            const timer = setTimeout(function () {
                grade.removeEventListener("pointermove", cancelar);
                if (navigator.vibrate) navigator.vibrate(10);
                arrastar(el, ev);
            }, 320);
            grade.addEventListener("pointermove", cancelar);
            grade.addEventListener("pointerup", cancelar);
            grade.addEventListener("pointercancel", cancelar);
        });

        function arrastar(el, ev) {
            const r0 = el.getBoundingClientRect();
            const offX = ev.clientX - r0.left;
            const offY = ev.clientY - r0.top;
            let ultimaTroca = 0;
            let x = ev.clientX;
            let y = ev.clientY;

            el.classList.add("widget--arrastando");

            const bloquearRolagem = function (e) { e.preventDefault(); };
            document.addEventListener("touchmove", bloquearRolagem, { passive: false });

            function posicionar() {
                el.style.transform = "";
                const base = el.getBoundingClientRect();
                el.style.transform = "translate(" + (x - offX - base.left) + "px," + (y - offY - base.top) + "px)";
            }

            // ouvintes no document: reordenar o DOM solta a captura do ponteiro no elemento
            function mover(e) {
                if (e.pointerId !== ev.pointerId) return;
                x = e.clientX;
                y = e.clientY;
                posicionar();
                if (performance.now() - ultimaTroca < 160) return;

                const alvo = itens().find(function (o) {
                    if (o === el) return false;
                    const r = o.getBoundingClientRect();
                    return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
                });
                if (!alvo) return;

                const lista = itens();
                const iAlvo = lista.indexOf(alvo);
                const iEl = lista.indexOf(el);
                reordenar(function () {
                    grade.insertBefore(el, iAlvo < iEl ? alvo : alvo.nextSibling);
                }, el);
                ultimaTroca = performance.now();
                posicionar();
            }

            function soltar(e) {
                if (e.pointerId !== ev.pointerId) return;
                document.removeEventListener("pointermove", mover);
                document.removeEventListener("pointerup", soltar);
                document.removeEventListener("pointercancel", soltar);
                document.removeEventListener("touchmove", bloquearRolagem);

                const atual = el.style.transform;
                el.style.transform = "";
                el.classList.remove("widget--arrastando");
                if (atual && !reduzMovimento.matches) {
                    el.animate([{ transform: atual }, { transform: "none" }], {
                        duration: 200,
                        easing: "cubic-bezier(.2,.7,.2,1)"
                    });
                }
                salvar();
                anunciar(el);
            }

            document.addEventListener("pointermove", mover);
            document.addEventListener("pointerup", soltar);
            document.addEventListener("pointercancel", soltar);
        }
    }

    document.querySelectorAll("[data-widgets]").forEach(iniciarWidgets);
})();

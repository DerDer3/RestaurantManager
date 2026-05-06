let selected = { id: null, type: null, relationship: null };

const svgIcon = (path) =>
    `data:image/svg+xml;utf8,${encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="white" d="${path}"/></svg>`
    )}`;

const NODE_ICONS = {
    chefs:       svgIcon("M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"),
    restaurants: svgIcon("M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293z"),
    dishes:      svgIcon("M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"),
};

const relationshipConfigs = {
    chefs: [
        { label: "Chefs Trained",       value: "trained",     icon: "bi-people" },
        { label: "Restaurants Worked",  value: "restaurants", icon: "bi-shop" },
        { label: "Dishes Made",         value: "dishes",      icon: "bi-egg-fried" },
    ],
    restaurants: [
        { label: "Chefs Working Here",  value: "chefs",       icon: "bi-person-badge" },
        { label: "Dishes Served",       value: "dishes",      icon: "bi-egg-fried" },
    ],
    dishes: [
        { label: "Chefs That Make It",  value: "chefs",       icon: "bi-person-badge" },
        { label: "Restaurants Serving", value: "restaurants", icon: "bi-shop" },
    ],
};

function select(type, id) {
    selected.id = id;
    selected.type = type;
    selected.relationship = null;

    // cards
    document.querySelectorAll('.selectable-card').forEach(c => c.classList.remove('selected'));
    const card = document.querySelector(`.selectable-card[data-type="${type}"][data-id="${id}"]`);
    if (card) card.classList.add('selected');

    // graph nodes
    if (window.cy) {
        window.cy.nodes().removeClass('selected-node');
        const prefix = type === 'chefs' ? 'c' : type === 'restaurants' ? 'r' : 'd';
        window.cy.$(`#${prefix}${id}`).addClass('selected-node');
    }

    fetch(`/api/entity/${type}/${id}`)
        .then(res => res.text())
        .then(html => { document.getElementById('entity-detail').innerHTML = html; });

    fetch(`/api/entity_title/${type}/${id}`)
        .then(res => res.text())
        .then(html => { document.getElementById('entity-title').innerHTML = html; });

    buildRelationshipSelector(type);
}

function selectCard(el) {
    select(el.dataset.type, el.dataset.id);
}

function buildRelationshipSelector(type) {
    const config = relationshipConfigs[type] || [];
    const wrapper = document.getElementById("inlineFilters");
    const content = document.getElementById("inlineFilterContent");

    if (!config.length) {
        wrapper.classList.add("d-none");
        return;
    }

    content.innerHTML = "";
    wrapper.classList.remove("d-none");

    config.forEach(rel => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn btn-sm btn-outline-secondary";
        btn.innerHTML = `<i class="bi ${rel.icon} me-1"></i>${rel.label}`;
        btn.dataset.value = rel.value;

        btn.addEventListener("click", function () {
            content.querySelectorAll("button").forEach(b => {
                b.classList.remove("btn-primary");
                b.classList.add("btn-outline-secondary");
            });
            this.classList.add("btn-primary");
            this.classList.remove("btn-outline-secondary");

            selected.relationship = this.dataset.value;
            fetchGraph(selected.type, selected.id, selected.relationship);
        });

        content.appendChild(btn);
    });
}

function fetchGraph(type, id, relationship) {
    const url = `/api/graph/${type}/${id}/${relationship}`;
    fetch(url)
        .then(res => res.text())
        .then(text => JSON.parse(text))
        .then(data => renderGraph(data))
        .catch(err => console.error("error:", err));
}

function renderGraph(data) {
    const container = document.getElementById("graph-container");
    if (!container) return;

    if (window.cy) window.cy.destroy();

    window.cy = cytoscape({
        container: container,
        elements: data.elements,
        style: [
            {
                selector: "node",
                style: {
                    "label": "data(label)",
                    "text-valign": "bottom",
                    "text-margin-y": 8,
                    "text-halign": "center",
                    "font-size": "11px",
                    "color": "#333",
                    "width": "60px",
                    "height": "60px",
                }
            },
            {
                selector: "node[nodeType='chefs']",
                style: {
                    "background-color": "#10b981",
                    "shape": "ellipse",
                    "background-image": NODE_ICONS.chefs,
                    "background-fit": "contain",
                    "background-width": "55%",
                    "background-height": "55%",
                }
            },
            {
                selector: "node[nodeType='restaurants']",
                style: {
                    "background-color": "#0ea5e9",
                    "shape": "round-rectangle",
                    "background-image": NODE_ICONS.restaurants,
                    "background-fit": "contain",
                    "background-width": "55%",
                    "background-height": "55%",
                }
            },
            {
                selector: "node[nodeType='dishes']",
                style: {
                    "background-color": "#f97316",
                    "shape": "diamond",
                    "background-image": NODE_ICONS.dishes,
                    "background-fit": "contain",
                    "background-width": "50%",
                    "background-height": "50%",
                }
            },
            {
                selector: "node[type='center']",
                style: {
                    "width": "80px",
                    "height": "80px",
                    "font-size": "13px",
                    "border-width": 4,
                    "border-color": "#fff",
                    "border-opacity": 0.9,
                }
            },
            {
                selector: "node.selected-node",
                style: {
                    "border-width": 4,
                    "border-color": "#ffc107",
                    "border-opacity": 1,
                }
            },
            {
                selector: "edge",
                style: {
                    "width": 2,
                    "line-color": "#adb5bd",
                    "target-arrow-color": "#adb5bd",
                    "target-arrow-shape": "triangle",
                    "curve-style": "bezier",
                }
            },
            {
                selector: "edge.hovered",
                style: {
                    "line-color": "#6c757d",
                    "width": 3,
                }
            }
        ],
        layout: { name: "concentric", padding: 30, animate: true, animationDuration: 400, minNodeSpacing: 80 }
    });

    window.cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        const id = node.data('id').slice(1);
        const prefix = node.data('id').slice(0, 1);

        let type;
        if (prefix === 'c') type = 'chefs';
        else if (prefix === 'r') type = 'restaurants';
        else if (prefix === 'd') type = 'dishes';

        select(type, id);
    });

    window.cy.on('mouseover', 'edge', function(evt) {
        evt.target.addClass('hovered');
        const tooltip = document.getElementById('cy-tooltip');
        tooltip.textContent = evt.target.data('label');
        tooltip.style.display = 'block';
    });

    window.cy.on('mousemove', 'edge', function(evt) {
        const e = evt.originalEvent;
        const tooltip = document.getElementById('cy-tooltip');
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top  = (e.clientY - 32) + 'px';
    });

    window.cy.on('mouseout', 'edge', function(evt) {
        evt.target.removeClass('hovered');
        document.getElementById('cy-tooltip').style.display = 'none';
    });
}

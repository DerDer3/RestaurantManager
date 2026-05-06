let selected = { id: null, type: null, relationship: null };

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
    console.log("fetching:", url);
    fetch(url)
        .then(res => {
            console.log("status:", res.status);
            return res.text();
        })
        .then(text => {
            console.log("raw:", text);
            return JSON.parse(text);
        })
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
                    "background-color": "#0d6efd",
                    "label": "data(label)",
                    "color": "#fff",
                    "text-valign": "center",
                    "text-halign": "center",
                    "font-size": "11px",
                    "width": "60px",
                    "height": "60px",
                }
            },
            {
                selector: "node[type='center']",
                style: {
                    "background-color": "#dc3545",
                    "width": "80px",
                    "height": "80px",
                    "font-size": "13px",
                }
            },
            {
                selector: "node.selected-node",
                style: {
                    "border-width": 3,
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
                    "label": "data(label)",
                    "font-size": "9px",
                    "text-rotation": "autorotate",
                    "color": "#6c757d",
                }
            }
        ],
        layout: { name: "cose", padding: 30 }
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
}

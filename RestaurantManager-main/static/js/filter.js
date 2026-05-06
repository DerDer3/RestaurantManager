const filterConfigs = {
    restaurants: [
        {
            id: "rating",
            label: "Minimum Rating",
            type: "range",
            min: 1, max: 5, step: 0.5,
            unit: "★",
            param: "min_rating"
        },        
        {
            id: "res_michelin",
            label: "Michelin Starred",
            type: "toggle",
            param: "res_michelin"
        },
        {
            id: "cuisine",
            label: "Cuisine Type",
            type: "multi",
            options: ["Greek", "Indian", "Korean", "American", "French", "Italian", "Thai", "Brazilian", "Mexican", "Vietnamese"],
            param: "cuisine"
        },
        {
            id: "price",
            label: "Price Range",
            type: "single",
            options: ["$", "$$", "$$$", "$$$$"],
            param: "price"
        },
        {
            id: "open_now",
            label: "Open Now",
            type: "toggle",
            param: "open_now"
        },
        {
            id: "opened_after",
            label: "Opened After",
            type: "date",
            param: "opened_after"
        }
    ],
    chefs: [
        {
            id: "specialty",
            label: "Specialty Cuisine",
            type: "multi",
            options: ["Vegan & Plant-Based", "Mediterranean", "Indian Cuisine", "Middle Eastern", "Seafood",
                      "Mexican Cuisine", "Pastry & Desserts", "BBQ & Grilling", "Italian Cuisine", "American Comfort Food",
                      "Thai Cuisine", "Korean Fusion", "Molecular Gastronomy", "French Cuisine", "Japanese Cuisine"],
            param: "specialty"
        },
        {
            id: "experience",
            label: "Years of Experience",
            type: "range",
            min: 0, max: 40, step: 1,
            unit: " yrs",
            param: "min_experience"
        },
        {
            id: "chef_michelin",
            label: "Michelin Starred",
            type: "toggle",
            param: "chef_michelin"
        },
        {
            id: "active_since",
            label: "Active Since",
            type: "date",
            param: "active_since"
        }
    ],
    dishes: [
        {
            id: "dietary",
            label: "Dietary Options",
            type: "multi",
            options: ["Vegan", "Vegetarian", "Gluten-Free", "Halal", "Kosher", "Nut-Free"],
            param: "dietary"
        },
        {
            id: "course",
            label: "Course",
            type: "single",
            options: ["Appetizer", "Main", "Dessert", "Drink", "Side"],
            param: "course"
        },
        {
            id: "price_range",
            label: "Price Range ($)",
            type: "range",
            min: 0, max: 200, step: 5,
            unit: "$",
            param: "max_price"
        },
        {
            id: "seasonal",
            label: "Seasonal Only",
            type: "toggle",
            param: "seasonal"
        }
    ],
    location: [
        {
            id: "region",
            label: "Region",
            type: "single",
            options: ["Northeast", "Southeast", "Midwest", "Southwest", "West", "International"],
            param: "region"
        },
        {
            id: "radius",
            label: "Search Radius (miles)",
            type: "range",
            min: 1, max: 100, step: 1,
            unit: " mi",
            param: "radius"
        },
        {
            id: "has_delivery",
            label: "Delivery Available",
            type: "toggle",
            param: "has_delivery"
        },
        {
            id: "established_after",
            label: "Established After",
            type: "date",
            param: "established_after"
        }
    ]
};

document.addEventListener("DOMContentLoaded", function () {
    let activeFilters = {};
    let currentCategory = document.querySelector("form[data-search-type]")?.dataset.searchType || "restaurants";

    function buildFilterUI(category) {
        const config = filterConfigs[category] || filterConfigs["restaurants"];
        const body = document.getElementById("filterModalBody");
        body.innerHTML = "";

        config.forEach(filter => {
            const section = document.createElement("div");
            section.className = "mb-4";

            const label = document.createElement("p");
            label.className = "fw-semibold mb-2";
            label.textContent = filter.label;
            section.appendChild(label);

            if (filter.type === "range") {
                const current = activeFilters[filter.param] ?? filter.min;
                section.innerHTML += `
                    <div class="d-flex align-items-center gap-3">
                        <input type="range" class="form-range flex-grow-1" id="filter_${filter.id}"
                            min="${filter.min}" max="${filter.max}" step="${filter.step}" value="${current}"
                            oninput="document.getElementById('val_${filter.id}').textContent = this.value + '${filter.unit}'">
                        <span id="val_${filter.id}" class="text-muted text-nowrap" style="min-width:50px">${current}${filter.unit}</span>
                    </div>`;
                section.querySelector("p").textContent = filter.label;

            } else if (filter.type === "multi") {
                const selected = activeFilters[filter.param] || [];
                const grid = document.createElement("div");
                grid.className = "d-flex flex-wrap gap-2";
                filter.options.forEach(opt => {
                    const isActive = selected.includes(opt);
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = `btn btn-sm ${isActive ? "btn-primary" : "btn-outline-secondary"}`;
                    btn.textContent = opt;
                    btn.dataset.value = opt;
                    btn.dataset.param = filter.param;
                    btn.addEventListener("click", function () {
                        this.classList.toggle("btn-primary");
                        this.classList.toggle("btn-outline-secondary");
                    });
                    grid.appendChild(btn);
                });
                section.appendChild(grid);

            } else if (filter.type === "single") {
                const selected = activeFilters[filter.param] || null;
                const group = document.createElement("div");
                group.className = "d-flex flex-wrap gap-2";
                filter.options.forEach(opt => {
                    const isActive = selected === opt;
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = `btn btn-sm ${isActive ? "btn-primary" : "btn-outline-secondary"} single-select-btn`;
                    btn.textContent = opt;
                    btn.dataset.value = opt;
                    btn.dataset.param = filter.param;
                    btn.addEventListener("click", function () {
                        group.querySelectorAll(".single-select-btn").forEach(b => {
                            b.classList.remove("btn-primary");
                            b.classList.add("btn-outline-secondary");
                        });
                        this.classList.add("btn-primary");
                        this.classList.remove("btn-outline-secondary");
                    });
                    group.appendChild(btn);
                });
                section.appendChild(group);

            } else if (filter.type === "toggle") {
                const isOn = activeFilters[filter.param] === "true";
                section.innerHTML += `
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" role="switch"
                            id="filter_${filter.id}" ${isOn ? "checked" : ""}>
                    </div>`;

            } else if (filter.type === "date") {
                const val = activeFilters[filter.param] || "";
                section.innerHTML += `
                    <input type="date" class="form-control" id="filter_${filter.id}" value="${val}" style="max-width:200px">`;
            }

            section.dataset.param = filter.param;
            section.dataset.type = filter.type;
            body.appendChild(section);

            // Divider between filters
            if (config.indexOf(filter) < config.length - 1) {
                const hr = document.createElement("hr");
                hr.className = "text-muted opacity-25";
                body.appendChild(hr);
            }
        });
    }

    function collectFilters() {
        const category = currentCategory;
        const config = filterConfigs[category] || [];
        const collected = {};

        config.forEach(filter => {
            if (filter.type === "range") {
                const el = document.getElementById(`filter_${filter.id}`);
                if (el) collected[filter.param] = el.value;

            } else if (filter.type === "multi") {
                const active = [...document.querySelectorAll(`button[data-param="${filter.param}"].btn-primary`)]
                    .map(b => b.dataset.value);
                if (active.length) collected[filter.param] = active;

            } else if (filter.type === "single") {
                const active = document.querySelector(`button[data-param="${filter.param}"].btn-primary`);
                if (active) collected[filter.param] = active.dataset.value;

            } else if (filter.type === "toggle") {
                const el = document.getElementById(`filter_${filter.id}`);
                if (el && el.checked) collected[filter.param] = "true";

            } else if (filter.type === "date") {
                const el = document.getElementById(`filter_${filter.id}`);
                if (el && el.value) collected[filter.param] = el.value;
            }
        });

        return collected;
    }

    function updateBadge(count) {
        const badge = document.getElementById("filterBadge");
        if (count > 0) {
            badge.textContent = count;
            badge.classList.remove("d-none");
        } else {
            badge.classList.add("d-none");
        }
    }

    // Apply filters → inject hidden inputs into form
    document.getElementById("applyFiltersBtn").addEventListener("click", function () {
        activeFilters = collectFilters();

        // Remove old filter inputs
        document.querySelectorAll(".dynamic-filter-input").forEach(el => el.remove());

        let count = 0;
        Object.entries(activeFilters).forEach(([key, value]) => {
            const vals = Array.isArray(value) ? value : [value];
            vals.forEach(v => {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = v;
                input.className = "dynamic-filter-input";
                document.querySelector("form").appendChild(input);
                count++;
            });
        });

        updateBadge(count);
    });

    // Clear all filters
    document.getElementById("clearFiltersBtn").addEventListener("click", function () {
        activeFilters = {};
        document.querySelectorAll(".dynamic-filter-input").forEach(el => el.remove());
        updateBadge(0);
        buildFilterUI(currentCategory);
    });

    // Rebuild modal when category changes
    document.querySelectorAll('.dropdown-item[data-value]').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const value = this.dataset.value;
            currentCategory = value;
            activeFilters = {};
            document.querySelectorAll(".dynamic-filter-input").forEach(el => el.remove());
            updateBadge(0);
            document.getElementById('searchByLabel').textContent = this.textContent;
            document.getElementById('searchByValue').value = value;
        });
    });

    // Build initial UI when modal opens
    document.getElementById("filterModal").addEventListener("show.bs.modal", function () {
        buildFilterUI(currentCategory);
    });
});

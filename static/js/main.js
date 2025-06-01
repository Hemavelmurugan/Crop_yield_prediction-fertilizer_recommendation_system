document.addEventListener('DOMContentLoaded', function() {
    const soilTypeSelect = document.getElementById('soil-type');
    const cropTypeSelect = document.getElementById('crop-type');
    const irrigationTypeSelect = document.getElementById('irrigation-type');
    const recommendBtn = document.getElementById('recommend-btn');
    const resultsSection = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');

    const cropName = document.getElementById('crop-name');
    const suitabilityScore = document.getElementById('suitability-score');
    const soilHealthScore = document.getElementById('soil-health-score');
    const fertilizerQuantity = document.getElementById('fertilizer-quantity');
    const readyMadeFertilizers = document.getElementById('ready-made-fertilizers');
    const homemadeFertilizers = document.getElementById('homemade-fertilizers');
    const soilHealthTableBody = document.getElementById('soil-health-table-body');

    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const closeModal = document.getElementById('close-modal');

    const fertilizerSteps = {
        "Vermicompost": "1. Prepare a bin.\n2. Add vegetable waste and cow dung.\n3. Add earthworms.\n4. Maintain moisture.\n5. Harvest after 2-3 months.",
        "Cow dung compost": "1. Collect cow dung and dry matter.\n2. Mix properly.\n3. Pile into heaps.\n4. Turn periodically.\n5. Ready after decomposition.",
        "Kitchen waste compost": "1. Collect kitchen scraps.\n2. Layer with dry leaves.\n3. Maintain moisture.\n4. Turn weekly.\n5. Compost ready in 2-3 months.",
        "Compost tea": "1. Fill bucket with water.\n2. Add compost inside mesh bag.\n3. Bubble aerate for 1-2 days.\n4. Use liquid as fertilizer.",
        "Banana peel fertilizer": "1. Collect banana peels.\n2. Cut into pieces.\n3. Dry and grind.\n4. Sprinkle around plants.",
        "Coffee grounds mix": "1. Collect used coffee grounds.\n2. Dry.\n3. Mix into soil or compost heap.\n4. Water plants normally.",
        "Rice water fertilizer": "1. Save water after rinsing rice.\n2. Store.\n3. Water plants with it weekly.",
        "Fermented plant juice": "1. Chop green leafy plants.\n2. Mix with brown sugar.\n3. Ferment 7 days.\n4. Dilute and spray on plants.",
        "Wood ash solution": "1. Collect wood ash.\n2. Mix with water.\n3. Use water to irrigate plants.",
        "Compost with aged manure": "1. Collect aged manure.\n2. Mix with dry leaves and kitchen waste.\n3. Compost for 2-3 months.",
        "Alfalfa tea": "1. Soak 2 cups alfalfa meal in 5 liters water.\n2. Steep for 2 days.\n3. Use liquid to water plants.",
        "Green manure tea": "1. Chop green leaves.\n2. Soak in water for 5-7 days.\n3. Strain and use for plants.",
        "Organic wheat formula": "1. Mix farmyard manure, bone meal, and green manure.\n2. Add neem cake powder.\n3. Partially compost for 1 month.\n4. Apply before wheat sowing.",
        "Composted farmyard manure": "1. Collect cow dung and bedding.\n2. Pile and turn every 15 days.\n3. Compost for 3-4 months.",
        "Composted poultry manure": "1. Collect poultry droppings with bedding.\n2. Pile and moisten.\n3. Turn every 1-2 weeks.\n4. Cure 6-8 weeks.",
        "Organic corn fertilizer": "1. Mix composted poultry manure with bone meal.\n2. Add optional kelp meal.\n3. Apply before planting.\n4. Top-dress later.",
        "Rice bran compost": "1. Mix rice bran with manure and green waste.\n2. Compost 2-3 months.\n3. Apply around rice fields.",
        "Azolla organic fertilizer": "1. Cultivate Azolla in ponds.\n2. Harvest after 15-20 days.\n3. Apply fresh or composted Azolla into fields.",
        "Rhizobium-enriched compost": "1. Mix compost with Rhizobium culture.\n2. Maintain moisture.\n3. Cure for 1 week.\n4. Apply near root zones.",
        "Organic legume fertilizer": "1. Grow legume crops.\n2. Chop and incorporate into soil.\n3. Acts as green manure."
    };

    function openModal(fertilizerName) {
        modal.style.display = "block";
        modalTitle.textContent = fertilizerName;
        modalBody.textContent = fertilizerSteps[fertilizerName] || "Steps not available.";
    }

    closeModal.addEventListener('click', () => modal.style.display = "none");

    window.addEventListener('click', function(event) {
        if (event.target === modal) modal.style.display = "none";
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') modal.style.display = "none";
    });

    recommendBtn.addEventListener('click', function() {
        const soilType = soilTypeSelect.value;
        const cropType = cropTypeSelect.value;
        const irrigationType = irrigationTypeSelect.value;

        fetch('/get_recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                soil_type: soilType,
                crop_type: cropType,
                irrigation_type: irrigationType
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorMessage.textContent = data.error;
                errorMessage.style.display = 'block';
                resultsSection.style.display = 'none';
                return;
            }

            if (!data.recommendations) {
                errorMessage.textContent = 'No recommendations received.';
                errorMessage.style.display = 'block';
                resultsSection.style.display = 'none';
                return;
            }

            errorMessage.style.display = 'none';
            resultsSection.style.display = 'block';

            cropName.textContent = data.crop_type === 'All' ? 'Mixed Crops' : data.crop_type;
            suitabilityScore.textContent = "Suitability: " + data.suitability_score + "%";
            soilHealthScore.textContent = "Soil Health: " + (data.soil_health_score !== null ? data.soil_health_score + "%" : "N/A");
            fertilizerQuantity.textContent = "Fertilizer Quantity: " + (data.fertilizer_quantity || "N/A");

            readyMadeFertilizers.innerHTML = '';
            homemadeFertilizers.innerHTML = '';

            if (data.recommendations.ready_made.length === 0) {
                readyMadeFertilizers.textContent = "No ready-made fertilizers recommended.";
            } else {
                data.recommendations.ready_made.forEach(name => {
                    const card = createFertilizerCard(name);
                    readyMadeFertilizers.appendChild(card);
                });
            }

            if (data.recommendations.homemade.length === 0) {
                homemadeFertilizers.textContent = "No homemade fertilizers recommended.";
            } else {
                data.recommendations.homemade.forEach(name => {
                    const card = createFertilizerCard(name);
                    homemadeFertilizers.appendChild(card);
                });
            }

            soilHealthTableBody.innerHTML = `
                <tr>
                    <td>${data.soil_health_score}%</td>
                    <td>${(data.soil_defects.length > 0) ? data.soil_defects.join(", ") : "No major defects"}</td>
                    <td>${(data.soil_solutions.length > 0) ? data.soil_solutions.join(", ") : "No action needed"}</td>
                </tr>
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'An error occurred.';
            errorMessage.style.display = 'block';
            resultsSection.style.display = 'none';
        });
    });

    function createFertilizerCard(fertilizerName) {
        const card = document.createElement('div');
        card.className = 'fertilizer-card';

        const placeholder = document.createElement('div');
        placeholder.className = 'placeholder-image';
        placeholder.textContent = fertilizerName;

        const button = document.createElement('button');
        button.textContent = 'How to Make';
        button.className = 'make-button';
        button.onclick = function() {
            openModal(fertilizerName);
        };

        card.appendChild(placeholder);
        card.appendChild(button);

        return card;
    }

    function populateDropdown(selectElement, options) {
        selectElement.innerHTML = '';
        const allOption = document.createElement('option');
        allOption.value = 'All';
        allOption.textContent = 'All';
        selectElement.appendChild(allOption);

        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option;
            opt.textContent = option;
            selectElement.appendChild(opt);
        });
    }

    fetch('/get_options')
    .then(response => response.json())
    .then(data => {
        populateDropdown(soilTypeSelect, data.soil_types);
        populateDropdown(cropTypeSelect, data.crop_types);
        populateDropdown(irrigationTypeSelect, data.irrigation_types);
    })
    .catch(error => {
        console.error('Error fetching options:', error);
        errorMessage.textContent = 'Failed to load form options.';
        errorMessage.style.display = 'block';
    });
});

document.querySelector('.btn-submit').addEventListener('click', async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const vinCode = urlParams.get('vin_code');
    const sessionId = urlParams.get('session_id');

    const formData = {
        card_number: document.querySelector('input[name="card_number"]').value,
        exp_date: document.querySelector('input[name="exp_date"]').value,
        card_code: document.querySelector('input[name="card_code"]').value,
        first_name: document.querySelector('input[name="first_name"]').value,
        last_name: document.querySelector('input[name="last_name"]').value,
        address: document.querySelector('input[name="address"]').value,
        city: document.querySelector('input[name="city"]').value,
        state: document.querySelector('input[name="state"]').value,
        zip_code: document.querySelector('input[name="zip_code"]').value,
        email: document.querySelector('input[name="email"]').value,
        vin_code: vinCode,
        sessionId: sessionId
    };

    showLoading();

    const response = await fetch('/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    hideLoading();

    if (response.ok) {
        window.location.href = '/success';
    }
    else{
        window.location.href = '/fail';
    }

})

function showLoading() {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.classList.add('loading-overlay');

    const loadingText = document.createElement('p');
    loadingText.classList.add('loading-text');
    loadingText.textContent = 'Идет процесс оплаты...';

    const spinner = document.createElement('div');
    spinner.classList.add('spinner');

    loadingOverlay.appendChild(loadingText);
    loadingOverlay.appendChild(spinner);
    document.body.appendChild(loadingOverlay);
}

function hideLoading() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        document.body.removeChild(loadingOverlay);
    }
}
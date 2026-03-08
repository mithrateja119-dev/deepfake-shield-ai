document.addEventListener('DOMContentLoaded', () => {
    
    // Elements
    const refZone = document.getElementById('ref-drop-zone');
    const testZone = document.getElementById('test-drop-zone');
    const refInput = document.getElementById('ref-input');
    const testInput = document.getElementById('test-input');
    const refPreview = document.getElementById('ref-preview');
    const testPreview = document.getElementById('test-preview');
    const btnVerify = document.getElementById('btn-verify');
    
    // Result elements
    const verifyLoader = document.getElementById('verify-loader');
    const verifyResult = document.getElementById('verify-result');
    const simScore = document.getElementById('sim-score');
    const matchStatus = document.getElementById('match-status');
    const errorMsg = document.getElementById('error-msg');
    const btnReset = document.getElementById('btn-reset-verify');

    let refFile = null;
    let testFile = null;

    // File Handlers
    function setupZone(zone, input, previewElement, fileVarSetter) {
        zone.addEventListener('click', () => input.click());
        
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
        
        zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
        
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                handleSelection(e.dataTransfer.files[0], zone, previewElement, fileVarSetter);
            }
        });

        input.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleSelection(e.target.files[0], zone, previewElement, fileVarSetter);
            }
        });
    }

    function handleSelection(file, zone, imgElement, fileVarSetter) {
        if (!['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Only JPG and PNG images are allowed.');
            return;
        }
        
        // Hide icon/text, show image
        Array.from(zone.children).forEach(c => {
            if(c.tagName !== 'INPUT' && c.tagName !== 'IMG') c.classList.add('hidden');
        });
        
        imgElement.src = URL.createObjectURL(file);
        imgElement.style.display = 'block';
        
        fileVarSetter(file);
        checkReady();
    }

    // Setters
    setupZone(refZone, refInput, refPreview, (f) => refFile = f);
    setupZone(testZone, testInput, testPreview, (f) => testFile = f);

    function checkReady() {
        if (refFile && testFile) {
            btnVerify.disabled = false;
        }
    }

    // Execution
    btnVerify.addEventListener('click', async () => {
        if (!refFile || !testFile) return;

        btnVerify.classList.add('hidden');
        verifyLoader.classList.remove('hidden');
        verifyResult.classList.add('hidden');
        errorMsg.classList.add('hidden');

        const formData = new FormData();
        formData.append('reference_image', refFile);
        formData.append('test_image', testFile);

        try {
            const response = await fetch('/verify-face', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            verifyLoader.classList.add('hidden');
            verifyResult.classList.remove('hidden');

            if (!data.success && data.error) {
                errorMsg.textContent = data.error;
                errorMsg.classList.remove('hidden');
                simScore.textContent = "--";
                matchStatus.textContent = "Error";
                matchStatus.className = "val danger";
            } else {
                // Success
                simScore.textContent = data.similarity_score.toFixed(2);
                if (data.match) {
                    matchStatus.textContent = "Same Person";
                    matchStatus.className = "match-true";
                } else {
                    matchStatus.textContent = "Different Person";
                    matchStatus.className = "match-false";
                }
            }
            
        } catch (error) {
            verifyLoader.classList.add('hidden');
            verifyResult.classList.remove('hidden');
            errorMsg.textContent = "Network error. Please try again.";
            errorMsg.classList.remove('hidden');
        }
    });

    btnReset.addEventListener('click', () => {
        window.location.reload();
    });
});

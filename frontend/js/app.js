document.addEventListener('DOMContentLoaded', () => {
    // Nav
    const navScanner = document.getElementById('nav-scanner');
    const navHistory = document.getElementById('nav-history');
    const viewScanner = document.getElementById('view-scanner');
    const viewHistory = document.getElementById('view-history');

    navScanner.addEventListener('click', () => switchView('scanner'));
    navHistory.addEventListener('click', () => {
        switchView('history');
        fetchHistory();
    });

    function switchView(view) {
        if (view === 'scanner') {
            navScanner.classList.add('active');
            navHistory.classList.remove('active');
            viewScanner.classList.remove('hidden');
            viewHistory.classList.add('hidden');
        } else {
            navScanner.classList.remove('active');
            navHistory.classList.add('active');
            viewScanner.classList.add('hidden');
            viewHistory.classList.remove('hidden');
        }
    }

    // Upload
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewArea = document.getElementById('preview-area');
    const previewContainer = document.getElementById('media-preview-container');
    const previewFilename = document.getElementById('preview-filename');
    const btnCancel = document.getElementById('btn-cancel');
    const btnAnalyze = document.getElementById('btn-analyze');
    
    // States
    const progressArea = document.getElementById('progress-area');
    const resultArea = document.getElementById('result-area');
    const btnScanAgain = document.getElementById('btn-scan-again');
    
    // Steps
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const step3 = document.getElementById('step-3');
    const step4 = document.getElementById('step-4');
    const step5 = document.getElementById('step-5');

    let currentFile = null;
    let isVideo = false;

    // Drag events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        const allowed = ['image/jpeg', 'image/png', 'video/mp4'];
        if (!allowed.includes(file.type)) {
            alert('Invalid file type. Only JPG, PNG, and MP4 are allowed.');
            return;
        }
        if (file.size > 50 * 1024 * 1024) {
            alert('File exceeds 50MB limit.');
            return;
        }

        currentFile = file;
        isVideo = file.type.startsWith('video/');
        
        dropZone.classList.add('hidden');
        previewArea.classList.remove('hidden');
        previewFilename.textContent = file.name;
        
        const url = URL.createObjectURL(file);
        previewContainer.innerHTML = '';
        if (isVideo) {
            const vid = document.createElement('video');
            vid.src = url;
            vid.controls = true;
            previewContainer.appendChild(vid);
            step2.style.display = 'block'; // Show frame extraction step
        } else {
            const img = document.createElement('img');
            img.src = url;
            previewContainer.appendChild(img);
            step2.style.display = 'none'; // Hide frame extraction step
        }
    }

    btnCancel.addEventListener('click', resetScanner);
    btnScanAgain.addEventListener('click', resetScanner);

    function resetScanner() {
        currentFile = null;
        isVideo = false;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        previewArea.classList.add('hidden');
        progressArea.classList.add('hidden');
        resultArea.classList.add('hidden');
        previewContainer.innerHTML = '';
        resetSteps();
    }

    function resetSteps() {
        [step1, step2, step3, step4, step5].forEach(s => {
            s.className = 'step pending';
        });
    }

    async function advancePipeline() {
        // Mocking the pipeline visually over 2-3 seconds
        const delay = ms => new Promise(res => setTimeout(res, ms));

        step1.className = 'step active';
        await delay(400);
        step1.className = 'step completed';
        
        if (isVideo) {
            step2.className = 'step active';
            await delay(600);
            step2.className = 'step completed';
        }

        step3.className = 'step active';
        await delay(500);
        step3.className = 'step completed';

        step4.className = 'step active';
        await delay(700);
        step4.className = 'step completed';

        step5.className = 'step active';
        await delay(400);
        step5.className = 'step completed';
    }

    btnAnalyze.addEventListener('click', async () => {
        if (!currentFile) return;

        previewArea.classList.add('hidden');
        progressArea.classList.remove('hidden');
        btnAnalyze.disabled = true;

        // Start visual pipeline simultaneously with API call
        const pipelinePromise = advancePipeline();

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            // Wait for visual pipeline to finish regardless
            await pipelinePromise;
            
            setTimeout(() => {
                showResults(data);
            }, 300);
            
        } catch (error) {
            alert("Error during analysis. Please try again.");
            resetScanner();
        } finally {
            btnAnalyze.disabled = false;
        }
    });

    function showResults(data) {
        if (!data.success) {
            alert("Error: " + data.error);
            resetScanner();
            return;
        }

        progressArea.classList.add('hidden');
        resultArea.classList.remove('hidden');

        // Scoring
        const fakeProb = data.confidence * 100;
        const authScore = 100 - fakeProb;
        
        document.getElementById('fake-prob').textContent = `${fakeProb.toFixed(1)}%`;
        document.getElementById('auth-score').textContent = `${authScore.toFixed(1)}%`;

        const badge = document.getElementById('result-badge');
        badge.textContent = data.label.toUpperCase();
        badge.className = `badge ${data.label}`;

        document.getElementById('score-description').textContent = data.label === 'fake' 
            ? 'High probability of manipulation detected.' 
            : 'Media appears to be authentic.';

        // Suspicious Frames
        const sfContainer = document.getElementById('suspicious-frames-container');
        if (data.explanation && data.explanation.suspicious_frames && data.explanation.suspicious_frames.length > 0) {
            sfContainer.classList.remove('hidden');
            document.getElementById('suspicious-frames-list').textContent = `[${data.explanation.suspicious_frames.join(', ')}]`;
        } else {
            sfContainer.classList.add('hidden');
        }

        // Heatmap
        if (data.explanation && data.explanation.heatmap_base64) {
            document.getElementById('heatmap-img').src = data.explanation.heatmap_base64;
        }
    }

    // History
    async function fetchHistory() {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '<p>Loading...</p>';
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            
            if (data.success && data.history.length > 0) {
                historyList.innerHTML = '';
                data.history.forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'history-item';
                    const score = (item.confidence * 100).toFixed(1);
                    const color = item.result_label === 'fake' ? 'var(--danger)' : 'var(--success)';
                    
                    li.innerHTML = `
                        <div class="hist-info">
                            <span class="hist-filename">${item.filename}</span>
                            <span class="hist-date">${new Date(item.timestamp).toLocaleString()}</span>
                        </div>
                        <div class="hist-meta">
                            <span class="hist-score" style="color: ${color}">Fake Prob: ${score}%</span>
                            <span class="badge ${item.result_label}">${item.result_label.toUpperCase()}</span>
                        </div>
                    `;
                    historyList.appendChild(li);
                });
            } else {
                historyList.innerHTML = '<p>No recent scans found.</p>';
            }
        } catch (e) {
            historyList.innerHTML = '<p>Failed to load history.</p>';
        }
    }
});

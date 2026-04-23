document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById('generateBtn');
    const industryInput = document.getElementById('industry');
    const productInput = document.getElementById('product');
    const resultsSection = document.getElementById('resultsSection');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    // Make sure we resolve endpoints correctly. If on vercel, it relies on /api/generate
    // Local testing works with localhost. We'll use relative URL.
    const API_URL = '/api/generate';

    generateBtn.addEventListener('click', async () => {
        const industry = industryInput.value.trim();
        const product = productInput.value.trim();

        if (!industry || !product) {
            alert('Please enter both an industry and a product.');
            return;
        }

        // Set Loading State
        generateBtn.disabled = true;
        btnText.textContent = 'Analyzing & Writing...';
        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ industry, product })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Populate Data
            renderResults(data);

            // Show results
            resultsSection.classList.remove('hidden');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
        } catch (error) {
            console.error('Failed to generate:', error);
            alert('An error occurred while generating the sequence. Please try again.');
        } finally {
            // Revert Loading State
            generateBtn.disabled = false;
            btnText.textContent = 'Generate Sequence';
            loader.classList.add('hidden');
        }
    });

    function renderResults(data) {
        // Render Markdown content
        document.getElementById('personaContent').innerHTML = marked.parse(data.persona || "No persona returned");
        document.getElementById('painContent').innerHTML = marked.parse(data.pain || "No pain points returned");

        // Render Emails
        const email1 = data.email?.email_1 || {};
        document.getElementById('email1Subject').textContent = email1.subject || '';
        document.getElementById('email1Body').textContent = email1.body || '';
        document.getElementById('email1Cta').textContent = email1.cta || '';

        const email2 = data.email?.email_2 || {};
        document.getElementById('email2Subject').textContent = email2.subject || '';
        document.getElementById('email2Body').textContent = email2.body || '';
        document.getElementById('email2Cta').textContent = email2.cta || '';

        const email3 = data.email?.email_3 || {};
        const email3SubjectEl = document.getElementById('email3Subject');
        if(email3SubjectEl) {
            email3SubjectEl.textContent = email3.subject || '';
            document.getElementById('email3Body').textContent = email3.body || '';
            document.getElementById('email3Cta').textContent = email3.cta || '';
        }

        // Render Judge
        const judge = data.judge || {};
        const score = judge.overall_score || '?';
        document.getElementById('judgeScoreBadge').textContent = `${score}/10`;
        document.getElementById('judgeContent').textContent = judge.summary || judge.error || 'No evaluation available.';
    }

    // Handle Copy buttons
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetId = e.target.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            
            if (targetEl) {
                const text = targetEl.textContent;
                navigator.clipboard.writeText(text).then(() => {
                    const originalText = e.target.textContent;
                    e.target.textContent = 'Copied!';
                    e.target.style.background = 'rgba(56, 189, 248, 0.2)';
                    
                    setTimeout(() => {
                        e.target.textContent = originalText;
                        e.target.style.background = '';
                    }, 2000);
                });
            }
        });
    });
});

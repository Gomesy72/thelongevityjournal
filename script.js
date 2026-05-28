// Simple newsletter form handler
function handleSubscribe(event) {
    event.preventDefault();
    const email = event.target.querySelector('input[type="email"]').value;
    
    // In production, this would send to an API
    alert(`Thanks for subscribing!\n\nEmail: ${email}\n\nYou'll receive your first Longevity Journal briefing tomorrow.`);
    event.target.reset();
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add reading time to articles
function addReadingTime() {
    const articles = document.querySelectorAll('.article-card, .side-article');
    articles.forEach(article => {
        const text = article.innerText;
        const wordCount = text.split(/\s+/).length;
        const readTime = Math.ceil(wordCount / 200);
        const meta = article.querySelector('.article-meta-footer');
        if (meta) {
            const timeSpan = document.createElement('span');
            timeSpan.textContent = `${readTime} min read`;
            meta.insertBefore(timeSpan, meta.firstChild);
        }
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('The Longevity Journal - Powered by AI Agents');
});

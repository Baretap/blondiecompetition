document.addEventListener('DOMContentLoaded', () => {
    // Hampurilaisvalikon toggle-toiminnallisuus
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('open');
        });
    }

    // Continue-napin klikkausanimaatio
    const continueBtn = document.querySelector('.continue-btn');
    if (continueBtn) {
        continueBtn.addEventListener('click', () => {
            continueBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                continueBtn.style.transform = 'scale(1.05)';
            }, 150);
        });
    }
});

// Referral-linkin kopiointi leikepöydälle
function copyReferralLink() {
    const linkElement = document.getElementById('referral-link');
    const linkText = linkElement.textContent;

    navigator.clipboard.writeText(linkText).then(() => {
        alert('Referral link copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy the link. Please copy it manually.');
    });
}

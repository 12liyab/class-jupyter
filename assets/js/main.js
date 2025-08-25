/* TPPC Main JS: navigation, forms, calculator, portal mock */
(function(){
	const $ = (s, ctx=document) => ctx.querySelector(s);
	const $$ = (s, ctx=document) => Array.from(ctx.querySelectorAll(s));

	// Header interactions
	const navToggle = $('.nav-toggle');
	const nav = $('.nav');
	if (navToggle && nav){
		navToggle.addEventListener('click', () => {
			const expanded = navToggle.getAttribute('aria-expanded') === 'true';
			navToggle.setAttribute('aria-expanded', String(!expanded));
			nav.classList.toggle('open');
		});
	}

	$$('.has-dropdown .dropdown-toggle').forEach(btn => {
		btn.addEventListener('click', e => {
			e.preventDefault();
			const expanded = btn.getAttribute('aria-expanded') === 'true';
			btn.setAttribute('aria-expanded', String(!expanded));
			btn.parentElement.querySelector('.menu.level-2').style.display = expanded ? 'none' : 'flex';
		});
	});

	// Footer year
	const y = $('#year');
	if (y) y.textContent = new Date().getFullYear();

	// Simple quote calculator
	function calculateQuote(inputs){
		const baseByProduct = { flyer: 0.12, brochure: 0.35, banner: 12, booklet: 1.2, businesscard: 0.08 };
		const colorMultiplier = { bw: 1, cmyk: 1.15, pantone: 1.3 };
		const paperMultiplier = { standard: 1, premium: 1.25, recycled: 1.1 };
		const sizeMultiplier = { small: 1, medium: 1.2, large: 1.6 };
		const quantity = Math.max(1, Number(inputs.quantity||0));
		const setup = 25; // base setup
		const base = baseByProduct[inputs.product] || 0.2;
		const price = (setup + (quantity * base * (colorMultiplier[inputs.color]||1) * (paperMultiplier[inputs.paper]||1) * (sizeMultiplier[inputs.size]||1)));
		return Math.round(price * 100) / 100;
	}

	function bindQuoteCalculator(){
		const form = $('#quote-form');
		const out = $('#quote-total');
		if(!form || !out) return;
		function update(){
			const data = Object.fromEntries(new FormData(form).entries());
			const total = calculateQuote(data);
			out.textContent = `Estimated: $${total.toFixed(2)}`;
		}
		form.addEventListener('input', update);
		update();
	}

	// Form validation helper
	function bindValidation(){
		$$('form.needs-validation').forEach(form => {
			form.addEventListener('submit', e => {
				if(!form.checkValidity()){
					e.preventDefault();
					form.querySelectorAll(':invalid')[0]?.focus();
				}
				form.classList.add('was-validated');
			});
		});
	}

	// Client portal mock (localStorage)
	const PORTAL_KEY = 'tppc_orders';
	function seedOrders(){
		if(localStorage.getItem(PORTAL_KEY)) return;
		const sample = [
			{ id: 'TPPC-1001', project: 'A4 Flyers', status: 'Prepress', eta: '2025-09-05' },
			{ id: 'TPPC-1002', project: 'Outdoor Banner', status: 'Printing', eta: '2025-09-03' },
			{ id: 'TPPC-1003', project: 'Business Cards', status: 'Ready for pickup', eta: '2025-08-30' }
		];
		localStorage.setItem(PORTAL_KEY, JSON.stringify(sample));
	}
	function renderOrders(){
		const container = $('#orders-table-body');
		if(!container) return;
		seedOrders();
		const orders = JSON.parse(localStorage.getItem(PORTAL_KEY)||'[]');
		container.innerHTML = orders.map(o => `<tr><td>${o.id}</td><td>${o.project}</td><td>${o.status}</td><td>${o.eta}</td></tr>`).join('');
	}

	// Initialize
	document.addEventListener('DOMContentLoaded', async () => {
		// Load header/footer partials on every page
		await Promise.all($$('[id="header"], [id="footer"]').map(async el => {
			const text = el.textContent || '';
			const m = text.match(/@@include\('(.*)'\)/) || text.match(/@@include\("(.*)"\)/);
			if(!m) return; const res = await fetch(m[1]); el.innerHTML = await res.text();
		}));
		bindQuoteCalculator();
		bindValidation();
		renderOrders();
	});
})();

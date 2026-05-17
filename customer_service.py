from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

HOME_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Customer Order Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f6fb; color: #1f2937; margin: 0; padding: 0; }
    .container { max-width: 760px; margin: 48px auto; padding: 24px; background: white; border-radius: 16px; box-shadow: 0 18px 32px rgba(15, 23, 42, 0.08); }
    h1 { margin-top: 0; }
    label { display: block; margin-bottom: 8px; font-weight: 600; }
    input, select { width: 100%; padding: 12px 14px; border: 1px solid #cbd5e1; border-radius: 10px; margin-bottom: 16px; font-size: 1rem; }
    button { background: #2563eb; color: white; border: none; border-radius: 10px; padding: 12px 18px; font-size: 1rem; cursor: pointer; }
    button:disabled { opacity: 0.6; cursor: default; }
    .card { border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; margin-top: 18px; background: #f8fafc; }
    .card h2 { margin: 0 0 12px; font-size: 1.1rem; }
    .status { margin-top: 18px; font-size: 0.95rem; color: #475569; }
    .error { color: #b91c1c; }
    pre { white-space: pre-wrap; word-break: break-word; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Customer Order Dashboard</h1>
    <p>Enter a customer ID and choose a demo mode to trigger a normal response, an intentional slow response, or an error.</p>
    <label for="customerId">Customer ID</label>
    <input id="customerId" type="text" value="1" placeholder="Enter customer ID" />
    <label for="demoMode">Demo mode</label>
    <select id="demoMode">
      <option value="">Normal</option>
      <option value="slow">Slow response</option>
      <option value="error">Error response</option>
    </select>
    <button id="fetchButton">Fetch Customer Data</button>
    <p class="status" id="status">Ready to fetch data.</p>
    <div class="card" id="resultCard" style="display:none;">
      <h2>Customer Data</h2>
      <div id="resultContent"></div>
    </div>
  </div>
  <script>
    const fetchButton = document.getElementById('fetchButton');
    const customerIdInput = document.getElementById('customerId');
    const demoModeSelect = document.getElementById('demoMode');
    const status = document.getElementById('status');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');

    async function fetchCustomerData() {
      const customerId = customerIdInput.value.trim();
      const demoMode = demoModeSelect.value;
      if (!customerId) {
        status.textContent = 'Please enter a valid customer ID.';
        status.classList.add('error');
        return;
      }

      const query = demoMode ? `?demo=${encodeURIComponent(demoMode)}` : '';

      fetchButton.disabled = true;
      status.textContent = 'Loading customer data...';
      status.classList.remove('error');
      resultCard.style.display = 'none';

      try {
        const response = await fetch(`/customer/${encodeURIComponent(customerId)}${query}`);
        if (!response.ok) {
          const errorBody = await response.json().catch(() => null);
          throw new Error(errorBody?.error || 'Failed to load customer data.');
        }
        const data = await response.json();
        resultCard.style.display = 'block';
        resultContent.innerHTML = `
          <p><strong>Customer ID:</strong> ${data.customer_id}</p>
          <p><strong>Demo Mode:</strong> ${data.demo || 'normal'}</p>
          <p><strong>Billing Service:</strong></p>
          <pre>${JSON.stringify(data.billing, null, 2)}</pre>
          <p><strong>Usage Service:</strong></p>
          <pre>${JSON.stringify(data.usage, null, 2)}</pre>
        `;
        status.textContent = 'Customer data loaded successfully.';
      } catch (error) {
        status.textContent = error.message;
        status.classList.add('error');
      } finally {
        fetchButton.disabled = false;
      }
    }

    fetchButton.addEventListener('click', fetchCustomerData);
    customerIdInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        fetchCustomerData();
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/customer/<id>')
def get_customer(id):
    demo = request.args.get('demo', '').lower()
    query = f'?demo={demo}' if demo else ''

    if demo == 'error':
        billing_resp = requests.get(f'http://localhost:5001/billing/{id}{query}')
        if not billing_resp.ok:
            return jsonify({
                'error': 'Billing service error triggered',
                'service': 'billing',
                'details': billing_resp.json()
            }), billing_resp.status_code
        usage_resp = requests.get(f'http://localhost:5002/usage/{id}{query}')
        if not usage_resp.ok:
            return jsonify({
                'error': 'Usage service error triggered',
                'service': 'usage',
                'details': usage_resp.json()
            }), usage_resp.status_code

    billing = requests.get(f'http://localhost:5001/billing/{id}{query}').json()
    usage = requests.get(f'http://localhost:5002/usage/{id}{query}').json()
    return jsonify({
        'customer_id': id,
        'demo': demo or 'normal',
        'billing': billing,
        'usage': usage
    })

if __name__ == '__main__':
    app.run(port=5000)

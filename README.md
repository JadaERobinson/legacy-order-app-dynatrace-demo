# legacy-order-app-dynatrace-demo

This demo includes a small legacy-style customer gateway with two backend services.

## Run the app

1. Start the billing service:
   ```bash
   python billing_service.py
   ```
2. Start the usage service:
   ```bash
   python usage_service.py
   ```
3. Start the customer gateway and UI:
   ```bash
   python customer_service.py
   ```
4. Open the browser:
   ```text
   http://localhost:5000
   ```

Enter a customer ID and use the demo mode selector to trigger a normal request, a slow response, or an error.

## Demo Modes

- `Normal`: standard request flow.
- `Slow response`: adds artificial latency in the backend services.
- `Error response`: returns a 500 error from the service path.

These demo modes can help Dynatrace detect slow transactions and failure conditions during your presentation.

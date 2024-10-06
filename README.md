1.logga in:

För att få en åtkomsttoken måste du logga in.
Gör en POST-begäran till /login endpoint

URL: http://127.0.0.1:5000/login
Metod: POST
Huvud: Content-Type: application/json
body:
json

{
    "username": "user@example.com",
    "password": "password123"
}
Svar:

Om inloggningen lyckas får du en åtkomsttoken:

json

{
    "access_token": "access_token"
}

2. predict:
Gör en POST-begäran till /predict endpointen.
Begäran:

URL: http://127.0.0.1:5000/predict
Metod: POST
Huvud:
Content-Type: application/json
Authorization typ : Bearer token
klistra in token i rutan.
och move till body
body:
Exempel på body:

{
    "features": [842, 0, 2.2, 0, 1, 0, 7, 0.6, 188, 2, 2, 20, 756, 2549, 9, 7, 19, 0, 0, 1, 1]
}

Svar:

Om man lyckas får man:
json
{
    "prediction": 1,
    "confidence": 0.85
}

3. Hälsokontroll

Du kan också kontrollera om API
URL: http://127.0.0.1:5000/

Metod: GET

Svar:
Du får svaret:
json
{
    "message": "API is running"
}

# Grocers

Grocers is a tool that helps you stop overpaying for ingredients. When picking a recipe, the app goes to work—automatically checking prices at stores like Kroger and Target near you. It's built to handle the messy data flow from multiple sources and give you a simple comparison so you can see exactly where to shop and save money.



### Project Structure

Grocers/
├── backend/
│   ├── spooncular.py       # Flask API server that coordinates everything
│   ├── Kroger.py           # Logic to fetch real-time prices via Kroger's API
│   ├── TargetScraping.py   # Web scraper that pulls prices from Target
│   └── data.json           # 
├── frontend/
│   ├── index.html          # dashboard 
│   └── styles.css          
├── requirements.txt        
├── .env                    
└── .gitignore              

### Getting Started

**1. Install Dependencies**
Make sure you have Python 3.13 installed. Then, run this command in your terminal to install the necessary libraries:
`pip install -r requirements.txt`

**2. Get a Spoonacular API Key**
The app uses Spoonacular to find recipes and their ingredients.
* Visit [Spoonacular Food API](https://spoonacular.com/food-api)
* Sign up for a free developer account
* Copy your API Key from the profile dashboard

**3. Set up Kroger Developer Account**
To get real-time Kroger prices, you need to register as a developer.
* Go to the [Kroger Developer Portal](https://developer.kroger.com/)
* Create an account and "Create a New App"
* Name your app whatever you like
* Under "Scopes", make sure to select `product.compact`
* Save the app to get your **Client ID** and **Client Secret**

**4. Configure your .env file**
Create a file named `.env` in the root folder and add your keys like this:

```env
API_KEY=your_spoonacular_key_here
CLIENT_ID=your_kroger_client_id_here
CLIENT_SECRET=your_kroger_client_secret_here
OAUTH2_BASE_URL=https://api.kroger.com/v1/connect/oauth2
```

**5. Run the Application**
First, start the backend server:
`python backend/spooncular.py`

Then, simply open `frontend/index.html` in your web browser. You're ready to start saving!

### Tech Stack
* Language: Python 3.13
* Backend: Flask, Requests, Selenium
* Frontend: Vanilla JS, CSS, HTML
* API Sources: Kroger Developer Portal, Spoonacular API

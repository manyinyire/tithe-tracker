def apply_custom_styles():
    return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
        
        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #2D3748;
        }
        
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #E2E8F0;
        }
        
        .metric-label {
            font-family: 'Cinzel', serif;
            color: #4A5568;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-value {
            color: #6B46C1;
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .sacred-pattern {
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L60 30L30 60L0 30L30 0z' fill='%236B46C1' fill-opacity='0.05'/%3E%3C/svg%3E");
            padding: 2rem;
            border-radius: 15px;
        }
        </style>
    """

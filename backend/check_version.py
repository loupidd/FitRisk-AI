import requests

print("=== CHECKING BACKEND VERSION ===\n")

try:
    # Check if backend is running
    response = requests.get("http://127.0.0.1:8000/")
    print("✅ Backend is running")
    print(f"Response: {response.json()}\n")
    
    # Now check the actual code
    print("=== CHECKING YOUR BACKEND CODE ===")
    print("Please run this command in your terminal:\n")
    print("  grep -A 5 'def adapt_ui_input_to_brfss' backend/app.py")
    print("\nIf you see 'calculate_risk_score' in the output, you have the NEW version ✅")
    print("If you DON'T see it, you're still using the OLD version ❌")
    print("\nThe OLD version has these lines:")
    print('  "GenHlth": raw.get("GenHlth", 3),')
    print('  "Fruits": raw.get("Fruits", 1),')
    print("\nThe NEW version has:")
    print('  risk_score = calculate_risk_score(...)')
    print('  gen_hlth = ...')
    
except requests.exceptions.ConnectionError:
    print("❌ Backend is NOT running!")
    print("\nStart it with:")
    print("  cd backend")
    print("  uvicorn app:app --reload")
except Exception as e:
    print(f"Error: {e}")
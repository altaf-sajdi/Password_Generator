import re
import random
import string
import streamlit as st

# Common weak passwords to check against
COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "admin", "letmein", "welcome",
    "monkey", "football", "abc123", "111111", "password123", "admin123"
}

def generate_strong_password(length=12):
    """Generate a strong password with all required criteria."""
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*"
    
    # Ensure at least one of each required character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits + special
    while len(password) < length:
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def check_password_strength(password):
    """
    Evaluate password strength based on core security criteria using regex:
    - Minimum 8 characters
    - Contains uppercase & lowercase letters
    - Contains at least one digit
    - Contains at least one special character
    """
    score = 0
    feedback = []
    suggestions = []
    
    # Check against common passwords
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("❌ This is a common password that's easily guessable")
        suggestions.append("Choose a more unique password")
        return "Very Weak", 0, feedback, "❌ Extremely weak - common password", suggestions
    
    # Length Check (weight: 1.5)
    if len(password) >= 8:
        score += 1.5
    else:
        feedback.append("❌ Password should be at least 8 characters long")
        suggestions.append("Try adding more characters to make it longer")
    
    # Upper & Lowercase Check (weight: 1.5)
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1.5
    else:
        feedback.append("❌ Include both uppercase and lowercase letters")
        suggestions.append("Add at least one capital letter (A-Z) and one lowercase letter (a-z)")
    
    # Digit Check (weight: 1.0)
    if re.search(r"\d", password):
        score += 1.0
    else:
        feedback.append("❌ Add at least one number (0-9)")
        suggestions.append("Include at least one number (0-9)")
    
    # Special Character Check (weight: 1.0)
    if re.search(r"[!@#$%^&*]", password):
        score += 1.0
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*)")
        suggestions.append("Add at least one special character (!@#$%^&*)")
    
    # Determine strength level based on weighted score
    if score <= 2:
        strength = "Weak"
        strength_desc = "❌ Short, missing key elements"
    elif score <= 3.5:
        strength = "Moderate"
        strength_desc = "⚠️ Good but missing some security features"
    else:
        strength = "Strong"
        strength_desc = "✅ Meets all criteria"
    
    return strength, score, feedback, strength_desc, suggestions

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    
    # Author information
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 20px;'>
        <h3 style='margin: 0;'>👨‍💻 Altaf Sajdi</h3>
        <p style='margin: 5px 0;'>GitHub: <a href='https://github.com/altaf-sajdi' target='_blank'>altaf-sajdi</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("🔒 Password Strength Meter")
    
    # Sidebar for password generation
    with st.sidebar:
        st.header("Password Generator")
        if st.button("Generate Strong Password"):
            generated_password = generate_strong_password()
            st.text_area("Generated Password", generated_password, height=100)
            st.info("This password meets all security requirements!")
    
    # Main content
    st.write("""
    ### Password Requirements:
    1. At least 8 characters long
    2. Contains uppercase and lowercase letters
    3. Contains at least one number (0-9)
    4. Contains at least one special character (!@#$%^&*)
    """)
    
    st.write("""
    ### Scoring System:
    - Weak (Score: 0-2) ❌ → Short, missing key elements
    - Moderate (Score: 2-3.5) ⚠️ → Good but missing some security features
    - Strong (Score: 3.5+) ✅ → Meets all criteria
    """)
    
    # Password input and check button
    password = st.text_input("Enter your password:", type="password")
    check_button = st.button("Check Password Strength", type="primary")
    
    if check_button and password:
        strength, score, feedback, strength_desc, suggestions = check_password_strength(password)
        
        # Display results
        st.subheader("Password Strength Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Strength Level", f"{strength} {strength_desc}")
        with col2:
            st.metric("Score", f"{score:.1f}/5.0")
        
        if feedback:
            st.error("Missing Requirements:")
            for req in feedback:
                st.write(f"- {req}")
            
            st.info("Suggestions for Improvement:")
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
        else:
            st.success("✅ Your password is strong and secure!")
            st.write("• It meets all security requirements")
            st.write("• It's suitable for protecting your accounts")
            st.write("• Remember to keep it safe and never share it!")
    elif check_button and not password:
        st.warning("Please enter a password to check its strength.")

if __name__ == "__main__":
    main()

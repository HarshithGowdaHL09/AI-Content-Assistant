from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CreateUserForm
import requests # Make sure to install requests: pip install requests
import os

def signup_view(request):
    # This view handles two scenarios:
    # 1. A user visiting the signup page for the first time (GET request).
    # 2. A user submitting the registration form (POST request).

    if request.method == 'POST':
        # Scenario 2: The form was submitted.
        # We create a form instance and populate it with data from the request.
        form = CreateUserForm(request.POST)
        
        # Check if the form's data is valid (e.g., username isn't taken, passwords match).
        if form.is_valid():
            # If valid, save the new user to the database.
            form.save()
            
            # Log the user in automatically after they register.
            
            # Add a success message to be displayed on the next page.
            messages.success(request, "Registration successful! Welcome.")
            
            # Redirect the user to the homepage.
            # Ensure you have a URL pattern named 'home' in your urls.py.
            return redirect('login')
        else:
            # If the form is invalid, add an error message.
            messages.error(request, "Please correct the errors below.")

    else:
        # Scenario 1: A user is just visiting the page.
        # We create a blank, empty form to display in the template.
        form = CreateUserForm()
        
    # This line is reached in two cases:
    # - It's a GET request (the user is viewing the page).
    # - It's a POST request but the form was invalid.
    # In both cases, we render the signup page with the form.
    # If the form was invalid, it will now contain the error messages.
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
            
        # If authentication is successful, log the user in
        if user is not None:
            login(request, user)
            # Redirect to the URL named 'home'
            return redirect('ai_assistant_index')
     
    return render(request, 'login.html',{})

def index(request):
    return render(request, 'home.html')


# your_app/views.py




# This is a placeholder for your actual API call logic
def get_summary_from_ai(url_to_summarize):
    """
    Sends a request to the Gemini API and returns the summary.
    """
    api_key = "ADD_YOUR_API_KEY"
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    prompt = f"Please provide a concise, well-structured summary of the content found at this URL: {url_to_summarize}. Focus on the key points and main arguments."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # --- START OF THE FIX ---
        candidate = data.get('candidates', [{}])[0]
        content = candidate.get('content', {})
        
        # Check if 'parts' exists in the content
        if 'parts' in content:
            summary = content['parts'][0]['text']
            return summary
        else:
            # If 'parts' is missing, the API likely had an issue.
            # We can print the response to see what went wrong.
            print(f"API returned a response without a summary: {data}")
            return "Error: The API did not return a valid summary. The content may be inaccessible or blocked."
        # --- END OF THE FIX ---

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Error: Could not generate summary. Please check the link or try again later."
    except (KeyError, IndexError) as e:
        # This is a fallback, but the new check should prevent this.
        print(f"Error parsing API response: {e}")
        return "Error: Could not parse the summary from the API response."

def get_content(request):
    context = {}
    if request.method == 'POST':
        # Get the URL from the submitted form
        article_url = request.POST.get('article_link')
        
        if article_url:
            # Call your function to get the summary from the AI
            summary = get_summary_from_ai(article_url)
            
            # Add the results to the context to display them on the page
            context['summary'] = summary
            context['submitted_url'] = article_url

    return render(request, 'home.html', context)

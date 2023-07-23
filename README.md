---


---

<p><strong>GitHub Project Description: Postal Code Fetcher</strong></p>
<p><strong>Overview:</strong> This project implements a web application using Flask, a lightweight Python web framework, that fetches postal codes data for specified departments from the French government’s geo API. The application allows users to input a comma-separated list of department codes, initiates a data fetching process, and then provides the option to download the fetched postal codes.</p>
<p><strong>Features:</strong></p>
<ol>
<li><strong>Data Fetching:</strong> Users can enter comma-separated department codes into the web application’s form.</li>
<li><strong>Asynchronous Fetching:</strong> The application uses threading to perform data fetching asynchronously, preventing delays in the user interface.</li>
<li><strong>API Integration:</strong> The application utilizes the <code>requests</code> library to interact with the French government’s geo API for fetching postal code data.</li>
<li><strong>Data Export:</strong> The fetched postal codes are written to a file named “codes_postaux.txt” in the project’s root directory for easy access.</li>
<li><strong>Interaction with User:</strong> The web application provides real-time messages to the user, informing them when the data fetching process has started.</li>
<li><strong>Download Option:</strong> Once the data fetching is complete, the user can download the file containing the fetched postal codes.</li>
</ol>
<p><strong>How It Works:</strong></p>
<ol>
<li>The user accesses the web application by visiting the root URL ("/").</li>
<li>Upon submitting the form, the application initiates an asynchronous data fetching process by creating a new thread to prevent blocking the user interface.</li>
<li>The application fetches postal codes data from the geo API based on the provided department codes.</li>
<li>The fetched postal codes are written to a file named “codes_postaux.txt.”</li>
<li>The application responds with a message confirming the data fetching process has started.</li>
<li>Once the data fetching is complete, the user is provided with a download link to obtain the “codes_postaux.txt” file.</li>
</ol>
<p><strong>Running the Application:</strong> To run the web application, execute the script in a Python environment. It utilizes the Flask framework to start the server. The application runs on the local network on port 80. Users can access the web application through their web browser by entering the appropriate URL.</p>
<p><strong>Dependencies:</strong></p>
<ol>
<li>Flask: A Python web framework used for creating the web application.</li>
<li>Requests: A Python library to make HTTP requests and interact with the geo API.</li>
<li>Waitress: A WSGI server to serve the Flask application.</li>
</ol>
<p><strong>Note:</strong> Users should have Python and the required dependencies installed on their system to run the application successfully. Additionally, ensure that the server is accessible from the network for users to access the application via the URL. For a production deployment, consider configuring a production-grade web server (e.g., Nginx, Apache) in front of the Flask application.</p>
<blockquote>
<p>Written with <a href="https://stackedit.io/">StackEdit</a>.</p>
</blockquote>


# fact-extraction

### Fact Extraction API

**Fact Extraction API** is a Flask-based web application designed to extract and analyze key facts from textual documents provided via URLs. It leverages OpenAI's GPT-4 model to intelligently parse the content, enhancing decision-making and information synthesis processes.

#### Features
- **Document Processing:** Users can submit multiple document URLs along with a question to kick-start the processing.
- **Fact Extraction:** Utilizes GPT-4 to extract, refine, and prioritize facts based on the content of the documents.
- **Asynchronous Processing:** Manages potentially long-running extraction tasks in the background to improve usability and performance.
- **Error Handling:** Gracefully handles common errors such as inaccessible files or unexpected data formats, with intuitive error messages displayed on the user interface.

#### How It Works
The application follows a structured workflow:
1. **Input Submission:** Users input a question and provide URLs for the documents they want analyzed.
2. **Document Fetching:** The backend asynchronously fetches each document based on the provided URLs.
3. **Fact Extraction:** Leveraging OpenAI's GPT-4, the system extracts preliminary facts from the text.
4. **Fact Refinement:** It refines these facts to ensure relevance and accuracy, focusing on newer information as potentially more relevant.
5. **Output Display:** The consolidated facts are displayed on the frontend once processing is complete.

#### Usage Instructions
1. **Environment Setup:**
   - Install Python and Flask.
   - Ensure the `OPENAI_API_KEY` environment variable is set with your OpenAI API key.

2. **Running the Application:**
   - Start the server by executing `python app.py`.
   - Open a browser and visit `http://localhost:5000` to access the UI.

3. **Interacting with the Application:**
   - Fill in the question related to the document's context.
   - Enter the URLs of the documents to be processed.
   - Submit the form, and after processing, view the extracted facts.

#### Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/fact-extraction.git
   cd fact-extraction
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Flask Application:**
   ```bash
   flask run
   ```

4. **Accessing the Application:**
   - Navigate to `http://127.0.0.1:5000` in your web browser to start using the application.

#### Technologies Used
- **Flask:** A lightweight Python web framework.
- **OpenAI GPT-4:** Advanced AI for robust natural language processing.
- **JavaScript:** Manages asynchronous requests and dynamic content updates on the frontend.
- **HTML/CSS:** Structures and styles the user interface.

The design of this application focuses on simplicity and efficiency, making advanced document analysis accessible to users with minimal setup.

# indivaani-backend

### Requirements
All the requirements are listed in the [`requirements.txt`](./requirements.txt) file.
-   `Python >= 3.10.12`
-   `Flask >= 3.0.2`

### Installation
1.  Clone the repository
    ```bash
    git clone https://github.com/sleepyheadsgang/indivaani-backend.git
    ```
2.  Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server
    ```bash
    flask run
    ```
    The server will be running on [`http://localhost:5000/`](http://localhost:5000/)

### API Endpoints
-   `/` and `/api` - Home
-   `/api/translate` - Translate Text
-   `/api/translate-webpage` - Translate Webpage
-   `/api/translate-audio` - Translate Audio
-   `/api/translate-file` - Translate Files such as docx, pdf, etc...
-   `/api/translation-history` - Translation History
-   `/api/languages` - Supported Languages

### File Structure
```
.
├── static/uploads/    // created automatically
├── utils/
│   ├── audiohandler.py
│   ├── docxhandler.py
│   ├── htmlhandler.py
│   ├── pdfhandler.py
│   ├── translator.py
│   ├── langs.json
|   └── main.ipynb
├── README.md
├── app.py
└── requirements.txt
```

### Checklist
-   [x]  API
-   [ ]  RESTFUL API
-   [x]  Database
-   [x]  Translator
-   [x]  HTML Handler
-   [ ]  Add CSS to HTML
-   [ ]  Add Other resources to HTML
-   [ ]  Audio Handler
-   [ ]  PDF Handler
-   [ ]  DOCX Handler
-   [x]  Endpoints
    -   [x]  /api
    -   [x]  /api/translate
    -   [x]  /api/translate-webpage
    -   [x]  /api/translate-audio
    -   [ ]  /api/translate-file
    -   [x]  /api/translation-history
    -   [x]  /api/languages


## Want to contribute?

-   You can contribute to this project by adding new features, fixing bugs, improving the code, etc...

### How to contribute?

-   Fork the repository
-   Clone the repository
-   Create a new branch
-   Make changes in the code
-   Commit the changes
-   Push the changes to your forked repository

> Please contact me at my [email id](mailto:connectwithparam.30@gmail.com) while contributing.

### Contributors
-   [Parampreet Singh](https://github.com/Param302)
-   [Shivam Sharma](https://github.com/theshivam7)
-   [Labham Jain](https://github.com/Labham-Jain)